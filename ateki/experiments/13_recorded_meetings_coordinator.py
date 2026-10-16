"""
Experiment 13: recorded coordinator-led LLM meetings, with the coordinator
role rotated over the five databases, on a finer task.

Changes from experiment 11 (proposed in
results/recorded_meetings_scale/CREDIT_FIXES.md):
  * Finer task: the team ranks thirteen anion-element groups of the
    experimental band-gap compilation (fluorides, chlorides, bromides,
    iodides, oxides, nitrides, sulfides, selenides, tellurides, borides,
    phosphides, arsenides, antimonides; groups with >= 30 measured
    compounds) instead of seven anion families. On this task the five
    databases' standalone accuracies are all different (HSE06 0.90,
    r2SCAN 0.85, TB-mBJ 0.82, OptB88vdW 0.79, GGA 0.69), so credit by
    database is resolvable; on the seven-family task three databases tied.
  * Rotation: with --rotation r, agent i holds DB_ORDER[(i - 1 + r) % 5],
    so the coordinator (always agent1) holds DB_ORDER[r]. r = 0 is the
    experiment-11 assignment (coordinator holds MP GGA).
Everything else (prompts apart from the task size, budget, value function,
attribution) is imported unchanged from experiment 11.

Run from ateki/ (PEGKI_ROOT set to the repo shared/):
  python experiments/13_recorded_meetings_coordinator.py --universe /abs/universe.jsonl \
      --base-url http://localhost:8020/v1 --model Qwen/Qwen3-4B-Instruct-2507 \
      --arms orchestrated --rotation 2 --seeds 0 1 2 \
      --output-dir results/recorded_meetings_coordinator/rot2
ASCII only; seeded; one JSON per campaign (resume-safe).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location(
    "exp11", str(_HERE / "11_recorded_meetings.py"))
m11 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m11)
exp26 = m11.exp26

# anion element -> group name, in priority order (first match wins; mirrors
# the family priority of experiment 11: halides, oxides, nitrides,
# chalcogenides, carbides, borides, pnictides)
ANION_ELEMENTS = [
    ("F", "fluoride"), ("Cl", "chloride"), ("Br", "bromide"),
    ("I", "iodide"), ("O", "oxide"), ("N", "nitride"), ("S", "sulfide"),
    ("Se", "selenide"), ("Te", "telluride"), ("C", "carbide"),
    ("B", "boride"), ("P", "phosphide"), ("As", "arsenide"),
    ("Sb", "antimonide"), ("Bi", "bismuthide"),
]
NUM_WORD = {7: "seven", 13: "thirteen"}


def classify_anion_element(formula):
    species = set(re.findall(r"[A-Z][a-z]?", formula))
    for el, name in ANION_ELEMENTS:
        if el in species:
            return name
    return None


def load_universe_fine(path, min_class_size):
    """-> {channel: {group: np.array of gaps}}, groups >= min_class_size."""
    per = {}
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            formula = (rec.get("x") or {}).get("formula")
            gap = (rec.get("y") or {}).get("bandgap_eV")
            ch = rec.get("s")
            if not formula or gap is None or ch is None:
                continue
            gap = float(gap)
            if gap <= exp26.MIN_GAP_EV:
                continue
            g = classify_anion_element(formula)
            if g is None:
                continue
            per.setdefault(ch, {}).setdefault(g, []).append(gap)
    return {ch: {g: np.asarray(sorted(v), dtype=float)
                 for g, v in gs.items() if len(v) >= min_class_size}
            for ch, gs in per.items()}


def set_team_rotated(n, rotation):
    m11.AGENTS = {f"agent{i}": m11.DB_ORDER[(i - 1 + rotation) % 5]
                  for i in range(1, n + 1)}
    m11.DECLARED_FLAT = [
        [a for a, d in m11.AGENTS.items() if d in m11.GGA_CLASS],
        [a for a, d in m11.AGENTS.items() if d not in m11.GGA_CLASS]]


class Campaign4b(m11.Campaign):
    def system_prompt(self, agent):
        n = len(self.families)
        return super().system_prompt(agent).replace(
            "seven material families",
            f"{NUM_WORD.get(n, n)} material groups (named by anion)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--universe", required=True)
    ap.add_argument("--base-url", default="http://localhost:8020/v1")
    ap.add_argument("--model", default="Qwen/Qwen3-4B-Instruct-2507")
    ap.add_argument("--arms", nargs="*", default=["flat", "orchestrated"])
    ap.add_argument("--seeds", type=int, nargs="*", default=[0])
    ap.add_argument("--rotation", type=int, default=0)
    ap.add_argument("--rounds", type=int, default=12)
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--min-count", type=int, default=2)
    ap.add_argument("--min-class-size", type=int, default=30)
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()
    set_team_rotated(5, args.rotation)

    # refuse to start when the server does not answer (lesson of exp 4)
    if not m11.chat(args.base_url, args.model, "Reply OK.", "OK?", 0.0, 0,
                    max_tokens=5):
        print("server not answering; abort", flush=True)
        return 2

    out_dir = Path(args.output_dir)
    (out_dir / "campaigns").mkdir(parents=True, exist_ok=True)
    per = load_universe_fine(Path(args.universe), args.min_class_size)
    classes = per[m11.RECEIVER]
    families = sorted(classes)
    for d in set(m11.AGENTS.values()):
        missing = set(classes) - set(per[d])
        assert not missing, (d, missing)
    donor_ranks = {a: [c for c in exp26.reference_ranking(per[d])
                       if c in classes] for a, d in m11.AGENTS.items()}
    priors = {a: exp26.donor_prior(classes, per[d], "even")
              for a, d in m11.AGENTS.items()}

    for arm in args.arms:
        for seed in args.seeds:
            path = out_dir / "campaigns" / f"{arm}_s{seed}.json"
            if path.exists():
                print(f"[skip] {path.name}", flush=True)
                continue
            raw = path.with_suffix(".raw.json")
            if raw.exists():
                with open(raw, encoding="utf-8") as fh:
                    log = json.load(fh)
            else:
                print(f"[run] {arm} rot{args.rotation} seed {seed}",
                      flush=True)
                c = Campaign4b(classes, families, donor_ranks, arm,
                               args.rounds, seed, args.base_url, args.model,
                               args.temperature)
                c.run()
                log = {"experiment": "4b", "arm": arm, "seed": seed,
                       "rotation": args.rotation,
                       "coordinator_db": (m11.AGENTS["agent1"]
                                          if arm == "orchestrated" else None),
                       "task": "anion-element groups",
                       "model": args.model,
                       "temperature": args.temperature,
                       "rounds": args.rounds, "team_size": len(m11.AGENTS),
                       "receiver": m11.RECEIVER, "agents": m11.AGENTS,
                       "donor_ranks": donor_ranks,
                       "reference_ranking": exp26.reference_ranking(classes),
                       "queries": c.queries, "notes": c.notes,
                       "messages": c.messages, "llm_calls": c.calls,
                       "fallbacks": c.fallbacks,
                       "coordinator_retries": c.retries}
                with open(raw, "w", encoding="utf-8") as fh:
                    json.dump(log, fh, indent=1)
            log["attribution"] = m11.attribute(log, classes, priors,
                                               args.min_count)
            log["roles"] = m11.roles(log)
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(log, fh, indent=1)
            raw.unlink(missing_ok=True)
            full = ",".join(sorted(m11.AGENTS))
            print(f"[write] {path.name} team tau "
                  f"{log['attribution']['v'][full]:+.3f}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
