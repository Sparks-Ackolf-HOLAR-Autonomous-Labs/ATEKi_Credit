"""
Experiment 11: recorded meetings, attribution on conference structures
taken from LLM-agent logs. The shared-notebook organisation and the role
measures follow Agensh (Zhan et al., 2026, "Agensh: Scaling Organizational
Intelligence to 1,024 Agents", arXiv:2609.26781,
doi:10.48550/arXiv.2609.26781).

Five LLM agents rank the material families of the experimental band-gap
compilation (receiver expt_zhuo) by measured gap, widest first. Each agent
holds one computed database as private knowledge (its family ordering only,
no values): MP GGA, MP r2SCAN, JARVIS OptB88vdW, JARVIS TB-mBJ, SNUMAT HSE.
Every round each agent submits one 4-family query; the archive returns the
order of one archived measured compound per family (no invented
observations). Budget: R rounds x 5 agents x 4 evaluations.

Two organisation arms:
  flat          : no coordinator. Agents act at the same time on the same
                  snapshot of a shared notebook (typed entries: observation,
                  fact, failure, claim, summary), the query log, and their
                  messages. They may message any subset of agents and must
                  cite the entries they build on.
  orchestrated  : agent 1 is the coordinator. It reads everything and
                  assigns a query to each agent; workers then act (they may
                  change their assigned query), write notes, and may message
                  the coordinator only.

Recorded conference structure: a message from i to a set T is the
conference {i} U T; a query that cites entries written by other agents is
the conference {author} U {cited authors}. Conferences that recur at least
`--min-count` times form the hypergraph H.

Value of a coalition S (measured, by replay): the queries submitted by the
members of S, refitted as a Plackett--Luce ranking with the members'
database orderings as an anchored prior whose trust is learned
prequentially (TENKi construction); v(S) = Kendall tau to the receiver's
median ranking; v(empty) = 0. All 32 coalitions are evaluated exactly.

Attributions per campaign: Shapley, Myerson value on the clique expansion
of H, hypergraph Myerson value on H, and Myerson value on the declared
structure (orchestrated: star at the coordinator; flat: provenance
conferences {GGA-class databases} and {beyond-GGA databases}).

Role measures: per agent, queries, notes by type, messages sent and
received, and citations received from other agents.

Run (from ateki/), with a vLLM OpenAI-compatible server:
  python experiments/11_recorded_meetings.py --universe /abs/universe.jsonl \
      --base-url http://localhost:8020/v1 --model Qwen/Qwen3-4B-Instruct-2507 \
      --seeds 0 1 2 3 --output-dir results/recorded_meetings
ASCII only in source; seeded; one JSON per campaign (resume-safe).
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import os
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))
from analysis.shapley import (  # noqa: E402
    GraphRestrictedValue,
    HypergraphRestrictedValue,
    ShapleyEngine,
)

_exp26_path = (_HERE.parent.parent / "tenki" / "TENKi" / "experiments"
               / "26_paired_campaign.py")
_spec = importlib.util.spec_from_file_location("exp26", str(_exp26_path))
exp26 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(exp26)
from src.rating.hypergraph_rating import (  # noqa: E402
    AdaptivePriorSelector,
    _kendall_tau,
)

RECEIVER = "expt_zhuo"
AGENTS = {"agent1": "mp_gga", "agent2": "mp_r2scan",
          "agent3": "jarvis_optb88vdw", "agent4": "jarvis_mbj",
          "agent5": "snumat_hse"}
DB_LABEL = {"mp_gga": "Materials Project GGA/GGA+U",
            "mp_r2scan": "Materials Project r2SCAN",
            "jarvis_optb88vdw": "JARVIS-DFT OptB88vdW",
            "jarvis_mbj": "JARVIS-DFT TB-mBJ",
            "snumat_hse": "SNUMAT HSE06"}
DECLARED_FLAT = [["agent1", "agent3"], ["agent2", "agent4", "agent5"]]
DB_ORDER = ["mp_gga", "mp_r2scan", "jarvis_optb88vdw", "jarvis_mbj",
            "snumat_hse"]
GGA_CLASS = {"mp_gga", "jarvis_optb88vdw"}


def set_team(n):
    """Team of n agents; agent i holds database DB_ORDER[(i-1) % 5].
    n = 5 reproduces the original team exactly."""
    global AGENTS, DECLARED_FLAT
    AGENTS = {f"agent{i}": DB_ORDER[(i - 1) % 5] for i in range(1, n + 1)}
    DECLARED_FLAT = [[a for a, d in AGENTS.items() if d in GGA_CLASS],
                     [a for a, d in AGENTS.items() if d not in GGA_CLASS]]


NUM_WORD = {5: "five", 10: "ten", 20: "twenty"}


def agent_num(agent):
    return int(agent[5:])
NOTE_TYPES = ["observation", "fact", "failure", "claim", "summary"]
K = 4


# --------------------------------------------------------------------- LLM
def chat(base_url, model, system, user, temperature, seed, max_tokens=400):
    body = json.dumps({
        "model": model, "temperature": temperature, "seed": seed,
        "max_tokens": max_tokens,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}]}).encode("utf-8")
    req = urllib.request.Request(base_url + "/chat/completions", data=body,
                                 headers={"Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                d = json.loads(r.read().decode("utf-8"))
            return d["choices"][0]["message"]["content"]
        except Exception:  # noqa: BLE001
            time.sleep(2 + 3 * attempt)
    return ""


def parse_json(text):
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


# ------------------------------------------------------------- campaign
class Campaign:
    def __init__(self, classes, families, donor_ranks, arm, rounds, seed,
                 base_url, model, temperature):
        self.classes = classes
        self.families = families
        self.donor_ranks = donor_ranks
        self.arm = arm
        self.rounds = rounds
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.base_url, self.model, self.temp = base_url, model, temperature
        self.notes = []      # {id, author, type, text, round}
        self.queries = []    # {id, author, round, query, result, built_on}
        self.messages = []   # {author, to, text, round}
        self.fallbacks = 0
        self.retries = 0
        self.calls = 0

    # -- prompt pieces
    def system_prompt(self, agent):
        fam = ", ".join(self.families)
        return (
            f"You are {agent}, one of {NUM_WORD.get(len(AGENTS), len(AGENTS))} "
            "agents in a materials screening "
            "team. The team must rank seven material families by measured "
            "optical band gap, widest gap first, for a wide-gap "
            "semiconductor search. Families: " + fam + ". "
            "Each query names exactly 4 different families; the laboratory "
            "measures one archived compound from each and returns their "
            "order by measured gap. One measurement is noisy: a single "
            "compound may not represent its family. "
            f"Your private knowledge: the {DB_LABEL[AGENTS[agent]]} "
            "database orders the families by computed gap as: "
            + " > ".join(self.donor_ranks[agent]) + ". Computed gaps can "
            "disagree with measured ones. Other agents hold other "
            "databases. You may write one entry in the shared notebook "
            "(type: observation, fact, failure, claim, or summary), send "
            "one message to chosen agents, and you must list the ids of "
            "notebook entries (N..) or query results (Q..) that your "
            "query builds on. Reply with JSON only.")

    def board(self, agent, last_q=30, last_n=20):
        lines = ["Query results so far (most recent last):"]
        for q in self.queries[-last_q:]:
            lines.append(f"{q['id']} ({q['author']}, round {q['round']}): "
                         + " > ".join(q["result"]))
        if len(lines) == 1:
            lines.append("(none yet)")
        lines.append("Notebook (most recent last):")
        notes = self.notes[-last_n:]
        for n in notes:
            lines.append(f"{n['id']} [{n['type']}] {n['author']}: "
                         f"{n['text']}")
        if not notes:
            lines.append("(empty)")
        inbox = [m for m in self.messages if agent in m["to"]][-8:]
        lines.append("Messages to you:")
        for m in inbox:
            lines.append(f"from {m['author']} (round {m['round']}): "
                         f"{m['text']}")
        if not inbox:
            lines.append("(none)")
        return "\n".join(lines)

    def valid_query(self, q):
        if not isinstance(q, list):
            return None
        q = [str(x).strip().lower() for x in q]
        q = [x for x in q if x in self.families]
        q = list(dict.fromkeys(q))
        return q if len(q) == K else None

    def worker_turn(self, agent, rnd, assigned=None):
        others = [a for a in AGENTS if a != agent]
        allowed = ["agent1"] if (self.arm == "orchestrated"
                                 and agent != "agent1") else others
        user = (f"Round {rnd} of {self.rounds}.\n" + self.board(agent))
        if assigned:
            user += ("\nThe coordinator (agent1) assigned you the query: "
                     + ", ".join(assigned) + ". You may follow it or "
                     "change it.")
        user += (
            "\nReply as JSON: {\"query\": [4 families], \"built_on\": "
            "[at most 6 ids], \"note\": {\"type\": \"...\", \"text\": \"...\"} or "
            "null, \"message\": {\"to\": [agent names], \"text\": \"...\"} "
            "or null}. Agents you may message: " + ", ".join(allowed) + ".")
        out = None
        for attempt in range(3):   # retry on unparseable or truncated JSON
            self.calls += 1
            out = parse_json(chat(self.base_url, self.model,
                                  self.system_prompt(agent), user, self.temp,
                                  self.seed * 1000 + rnd * 10
                                  + agent_num(agent) + 100 * attempt,
                                  max_tokens=900))
            if out and self.valid_query(out.get("query")) is not None:
                break
            self.retries += 1
        return self.clean(agent, out, allowed, assigned)

    def clean(self, agent, out, allowed, assigned):
        out = out or {}
        q = self.valid_query(out.get("query"))
        if q is None:
            self.fallbacks += 1
            q = assigned or list(self.rng.choice(self.families, size=K,
                                                 replace=False))
        ids = {n["id"]: n["author"] for n in self.notes}
        ids.update({x["id"]: x["author"] for x in self.queries})
        built = [str(b) for b in (out.get("built_on") or [])
                 if str(b) in ids]
        note = out.get("note")
        if not (isinstance(note, dict) and note.get("type") in NOTE_TYPES
                and note.get("text")):
            note = None
        msg = out.get("message")
        if isinstance(msg, dict) and msg.get("text"):
            to = msg.get("to") or []
            if isinstance(to, str):
                to = [to]
            to = [t for t in to if t in allowed]
            msg = ({"to": sorted(set(to)), "text": str(msg["text"])[:300]}
                   if to else None)
        else:
            msg = None
        return {"query": q, "built_on": built, "note": note,
                "message": msg, "cited_authors": sorted(
                    {ids[b] for b in built} - {agent})}

    def coordinator_turn(self, rnd):
        user = (f"Round {rnd} of {self.rounds}. You are the coordinator: "
                f"assign one 4-family query to each agent (agent1 to "
                f"agent{len(AGENTS)}, including yourself).\n" + self.board("agent1")
                + "\nReply as JSON: {\"assignments\": {\"agent1\": [4 "
                "families], ..., \"agent" + str(len(AGENTS)) + "\": [...]}, \"message\": \"text "
                "to all agents, at most 40 words\"}.")
        out = None
        for attempt in range(3):   # retry on unparseable or truncated JSON
            self.calls += 1
            out = parse_json(chat(self.base_url, self.model,
                                  self.system_prompt("agent1"), user,
                                  self.temp,
                                  self.seed * 1000 + rnd * 10 + 100 * attempt,
                                  max_tokens=1000))
            if out and isinstance(out.get("assignments"), dict):
                break
            self.retries += 1
        assign = {}
        for a in AGENTS:
            q = self.valid_query(((out or {}).get("assignments") or {})
                                 .get(a))
            if q is None:
                self.fallbacks += 1
                q = list(self.rng.choice(self.families, size=K,
                                         replace=False))
            assign[a] = q
        text = (out or {}).get("message")
        if text:
            self.messages.append({"author": "agent1",
                                  "to": [a for a in AGENTS if a != "agent1"],
                                  "text": str(text)[:300], "round": rnd,
                                  "kind": "assignment"})
        return assign

    def run(self):
        for rnd in range(1, self.rounds + 1):
            assign = (self.coordinator_turn(rnd)
                      if self.arm == "orchestrated" else {})
            with ThreadPoolExecutor(max_workers=len(AGENTS)) as ex:
                futs = {a: ex.submit(self.worker_turn, a, rnd,
                                     assign.get(a)) for a in AGENTS}
                acts = {a: f.result() for a, f in futs.items()}
            for a in AGENTS:            # apply after all acted (same snapshot)
                act = acts[a]
                ev = exp26.sample_event(self.classes, act["query"], self.rng)
                qid = f"Q{len(self.queries) + 1}"
                built = list(act["built_on"])
                cited = list(act["cited_authors"])
                if self.arm == "orchestrated" and a != "agent1":
                    cited = sorted(set(cited) | {"agent1"})
                self.queries.append({
                    "id": qid, "author": a, "round": rnd,
                    "query": act["query"],
                    "result": list(ev.ranking) if ev else act["query"],
                    "tied": ev is None, "built_on": built,
                    "cited_authors": cited})
                if act["note"]:
                    self.notes.append({"id": f"N{len(self.notes) + 1}",
                                       "author": a, "round": rnd,
                                       "type": act["note"]["type"],
                                       "text": str(act["note"]["text"])[:300]})
                if act["message"]:
                    self.messages.append({"author": a, "round": rnd,
                                          **act["message"], "kind": "message"})
            print(f"  [{self.arm} s{self.seed}] round {rnd} done "
                  f"(fallbacks {self.fallbacks}/{self.calls})", flush=True)


# ---------------------------------------------------------- attribution
def coalition_value(camp_log, classes, priors, S):
    if not S:
        return 0.0
    ref = exp26.reference_ranking(classes)
    members = sorted(S)
    prior = {c: float(np.mean([priors[a][c] for a in members]))
             for c in classes}
    sel = AdaptivePriorSelector(prior, exp26.LAMBDA_GRID, refresh_every=4)
    from src.rating.hypergraph_rating import Hyperedge  # noqa: E402
    for q in camp_log["queries"]:
        if q["author"] in S and not q["tied"]:
            sel.observe(Hyperedge(tuple(q["result"])))
    if sel.edges:
        rank = sel.fit_current().ranking()
    else:
        rank = sorted(prior, key=lambda c: (-prior[c], c))
    return float(_kendall_tau(rank, ref))


def conferences(camp_log):
    from collections import Counter
    cnt = Counter()
    for m in camp_log["messages"]:
        e = frozenset([m["author"], *m["to"]])
        if len(e) >= 2:
            cnt[e] += 1
    for q in camp_log["queries"]:
        e = frozenset([q["author"], *q["cited_authors"]])
        if len(e) >= 2:
            cnt[e] += 1
    return cnt


def attribute(camp_log, classes, priors, min_count):
    players = list(AGENTS)
    cache = {}
    for r in range(len(players) + 1):
        for S in itertools.combinations(players, r):
            cache[frozenset(S)] = coalition_value(camp_log, classes, priors,
                                                  frozenset(S))
    v = cache.__getitem__
    cnt = conferences(camp_log)
    H = [sorted(e) for e, c in cnt.items() if c >= min_count]
    clique = sorted({tuple(sorted(p)) for e in H
                     for p in itertools.combinations(e, 2)})
    adj = [[1.0 if (tuple(sorted((a, b))) in clique) else 0.0
            for b in players] for a in players]
    if camp_log["arm"] == "orchestrated":
        declared = [["agent1", a] for a in players if a != "agent1"]
    else:
        declared = DECLARED_FLAT
    res = {
        "v": {",".join(sorted(S)) or "-": val for S, val in cache.items()},
        "hyperedges": H,
        "conference_counts": {",".join(sorted(e)): c
                              for e, c in cnt.items()},
        "shapley": ShapleyEngine(players, v).exact().scores,
        "myerson_clique": ShapleyEngine(
            players, GraphRestrictedValue(players, v, adj)).exact().scores,
        "hypergraph_myerson": (ShapleyEngine(
            players, HypergraphRestrictedValue(players, v, H)).exact().scores
            if H else {a: v(frozenset([a])) for a in players}),
        "declared_myerson": ShapleyEngine(
            players, HypergraphRestrictedValue(players, v, declared)
        ).exact().scores,
        "declared": declared,
    }
    return res


def roles(camp_log):
    out = {a: {"queries": 0, "notes": {t: 0 for t in NOTE_TYPES},
               "msgs_sent": 0, "msgs_received": 0, "cited_by_others": 0}
           for a in AGENTS}
    for q in camp_log["queries"]:
        out[q["author"]]["queries"] += 1
        for c in set(q["cited_authors"]):
            if c in out and c != q["author"]:
                out[c]["cited_by_others"] += 1
    for n in camp_log["notes"]:
        out[n["author"]]["notes"][n["type"]] += 1
    for m in camp_log["messages"]:
        out[m["author"]]["msgs_sent"] += 1
        for t in m["to"]:
            out[t]["msgs_received"] += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--universe", required=True)
    ap.add_argument("--base-url", default="http://localhost:8020/v1")
    ap.add_argument("--model", default="Qwen/Qwen3-4B-Instruct-2507")
    ap.add_argument("--arms", nargs="*", default=["flat", "orchestrated"])
    ap.add_argument("--seeds", type=int, nargs="*", default=[0, 1, 2, 3])
    ap.add_argument("--rounds", type=int, default=12)
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--min-count", type=int, default=2)
    ap.add_argument("--min-class-size", type=int, default=30)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--team-size", type=int, default=5)
    args = ap.parse_args()
    set_team(args.team_size)

    out_dir = Path(args.output_dir)
    (out_dir / "campaigns").mkdir(parents=True, exist_ok=True)
    per_channel = exp26.load_universe(Path(args.universe),
                                      args.min_class_size)
    classes = per_channel[RECEIVER]
    families = sorted(classes)
    donor_ranks = {a: [c for c in exp26.reference_ranking(per_channel[d])
                       if c in classes] for a, d in AGENTS.items()}
    priors = {a: exp26.donor_prior(classes, per_channel[d], "even")
              for a, d in AGENTS.items()}

    for arm in args.arms:
        for seed in args.seeds:
            path = out_dir / "campaigns" / f"{arm}_s{seed}.json"
            if path.exists():
                print(f"[skip] {path.name}")
                continue
            raw = path.with_suffix(".raw.json")
            if raw.exists():     # LLM part done earlier; attribute only
                print(f"[attribute] {raw.name}", flush=True)
                with open(raw, encoding="utf-8") as fh:
                    log = json.load(fh)
            else:
                print(f"[run] {arm} seed {seed}", flush=True)
                c = Campaign(classes, families, donor_ranks, arm,
                             args.rounds, seed, args.base_url, args.model,
                             args.temperature)
                c.run()
                log = {"arm": arm, "seed": seed, "model": args.model,
                       "temperature": args.temperature,
                       "rounds": args.rounds, "team_size": len(AGENTS),
                       "receiver": RECEIVER, "agents": AGENTS,
                       "donor_ranks": donor_ranks,
                       "reference_ranking": exp26.reference_ranking(classes),
                       "queries": c.queries, "notes": c.notes,
                       "messages": c.messages, "llm_calls": c.calls,
                       "fallbacks": c.fallbacks,
                       "coordinator_retries": c.retries}
                with open(raw, "w", encoding="utf-8") as fh:
                    json.dump(log, fh, indent=1)
            log["attribution"] = attribute(log, classes, priors,
                                           args.min_count)
            log["roles"] = roles(log)
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(log, fh, indent=1)
            raw.unlink(missing_ok=True)
            print(f"[write] {path.name} team tau "
                  f"{log['attribution']['v'][','.join(sorted(AGENTS))]:+.3f}",
                  flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
