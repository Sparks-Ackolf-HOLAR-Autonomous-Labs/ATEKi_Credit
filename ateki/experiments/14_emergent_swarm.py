"""Experiment 14: emergent hierarchical swarms versus pre-defined team structures.

Question (ATEKi): when many heterogeneous decision bodies run one discovery
campaign together, does a team that forms its own temporary organisation
(dynamic roles, self-organised tiers, merging into cells) outperform a team
whose structure was fixed by the designer, and how does the credit each body
receives change with the structure?

Setting: the computed Al-Mg-Si campaign (compute/almgsi_campaign). A group wants
the ten most stable orderings at a DFT receiver (QE PBE; held-out receivers
QE HSE06 and GPAW r2SCAN). Each round the team submits a batch of k
candidates, pays their measured receiver cost, and sees the results.

Decision bodies (agents), each with its own local rule and partial knowledge:
  * mace_relax, gpumd_nep89_md, gpumd_nep89_relax, lammps_meam_md, archive_mp:
    each holds one lower-cost ordering of the pool (the archive covers only
    the compounds MP holds) and mixes it with a composition surrogate fitted
    on the receiver results it can see, trusting its ordering by the shrunken
    Kendall tau against those results (the learned-trust rule of campaign.py);
  * surrogate: active learner with no prior ordering;
  * explorer: random scout.
Every agent sees only the receiver results that its position in the
organisation gives it access to (partial knowledge).

Structures:
  solo         no communication: equal slots, each agent sees only its own results
  flat         egalitarian: equal slots, all results shared
  star         fixed supervisor (the active learner) ranks the members' proposals
               by mean rank score and fills the batch; all results shared
  tiers_fixed  designer tiers by nominal fidelity: {MACE, archive} > {MD and
               relaxation potentials} > {surrogate, scout}; slot weights 4:2:1;
               an agent sees results proposed at its tier or above (leaders see all)
  emergent     non-egalitarian emergent hierarchical swarm with an implemented
               promotion protocol: start flat; after each round every agent's
               prequential score (Kendall tau between the scores it gave the
               batch before the reveal and the revealed values, over the results
               it can see) updates an exponential average; agents are re-ranked
               into leader / second / third tiers with an incumbency margin;
               negative-score agents fall to a floor weight; agents whose current
               orderings agree above a threshold merge into a temporary cell that
               proposes jointly with the weight of its strongest member and
               shares results inside the cell; cells dissolve when agreement drops
  emergent_learned  same protocol, its six parameters learned with the cross-entropy
               method on the PBE receiver only, then frozen for HSE06 and r2SCAN
  emergent_nocells / emergent_notiers  ablations: the implemented protocol without
               merging into cells, and without tiers (equal slot weights)
  emergent_morph  temporary tiers with a shape that changes over the campaign: the
               number of tiers and their sizes are re-derived after every batch from
               the gaps between the members' running scores (a new tier starts where
               the drop to the next member exceeds a gap threshold), so the team is
               flat while the records are close, deepens as they separate, and
               flattens again when they converge; the incumbency margin of a member
               lasts only a fixed number of batches after its last change of tier,
               after which the position must be re-earned on the record alone
  emergent_morph_learned  same, its parameters learned on PBE only (as emergent_learned)

Value of a team: early-window recall area (fraction of the ten most stable
compounds found, averaged over the first quarter of the receiver cost), the
metric of campaign.py. Attribution: exact Shapley over the seven agents for
each structure, v(S) = value of the campaign run by sub-swarm S alone under
that structure; v(empty) = random selection. Structural credit of an agent =
Shapley under a structure minus Shapley under flat.

Usage (from ateki/, with an environment holding numpy, scipy and ase):
    python experiments/14_emergent_swarm.py --selftest
    python experiments/14_emergent_swarm.py --stage all
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
import time
import zlib
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
LIVE = ROOT / "compute" / "almgsi_campaign"
sys.path.insert(0, str(LIVE))
import campaign as C  # noqa: E402

OUT = HERE.parent / "results" / "emergent_swarm"
AGENTS = ["mace_relax", "gpumd_nep89_md", "gpumd_nep89_relax", "lammps_meam_md",
          "archive_mp", "surrogate", "explorer"]
LABEL = {"mace_relax": "MACE-MP-0 relaxation", "gpumd_nep89_md": "NEP89 MD",
         "gpumd_nep89_relax": "NEP89 relaxation", "lammps_meam_md": "MEAM MD",
         "archive_mp": "MP archive", "surrogate": "Active learner", "explorer": "Random scout"}
FIXED_TIER = {"mace_relax": 1, "archive_mp": 1, "gpumd_nep89_md": 2, "gpumd_nep89_relax": 2,
              "lammps_meam_md": 2, "surrogate": 3, "explorer": 3}
STRUCTURES = ["solo", "flat", "star", "tiers_fixed", "emergent", "emergent_learned",
              "emergent_nocells", "emergent_notiers", "emergent_morph", "emergent_morph_learned"]
# ablations of the implemented protocol: no merging into cells; no tiers (equal slot weights)
STRUCT_THETA = {"emergent_nocells": {"merge": 1.01}, "emergent_notiers": {"ratio": 1.0, "floor": 1.0}}
# implemented promotion protocol (cold-start defaults)
DEFAULT_THETA = {"ema": 0.4, "ratio": 2.0, "margin": 0.05, "merge": 0.85, "floor": 0.25, "n_lead": 1.0,
                 "gap": 0.08, "tenure": 4.0}
THETA_BOUNDS = {"ema": (0.05, 1.0), "ratio": (1.0, 6.0), "margin": (0.0, 0.3), "merge": (0.5, 1.01),
                "floor": (0.0, 1.0), "n_lead": (1.0, 3.0)}
# morphing protocol: no fixed leader count; tier gap threshold and incumbency tenure (batches)
MORPH_BOUNDS = {k: v for k, v in THETA_BOUNDS.items() if k != "n_lead"}
MORPH_BOUNDS.update({"gap": (0.01, 0.3), "tenure": (1.0, 12.0)})


def crc(s: str) -> int:
    return zlib.crc32(s.encode("utf-8")) & 0x7FFFFFFF


def body_kind(name: str) -> str:
    """Kind of a decision body; "kind#j" and "kind=j" name copy j of that kind."""
    return name.replace("=", "#").split("#")[0]


def ktau(a: np.ndarray, b: np.ndarray) -> float:
    """Kendall tau-a on paired vectors (vectorised; small n)."""
    n = len(a)
    if n < 3:
        return float("nan")
    da = np.sign(a[:, None] - a[None, :])
    db = np.sign(b[:, None] - b[None, :])
    return float((da * db).sum() / (n * (n - 1)))


def rank01(v: np.ndarray) -> np.ndarray:
    """Evenly spaced rank score in [0,1], 1 = largest v."""
    n = len(v)
    out = np.empty(n)
    out[np.argsort(v, kind="stable")] = np.arange(n) / max(1, n - 1)
    return out


# ---------------------------------------------------------------- environment

class Env:
    def __init__(self, receiver: str):
        idx = C.load_index()
        tables = C.load_tables()
        rec = tables[receiver]
        pool = sorted(rec)
        X = {c: C.fractions(c, idx) for c in pool}
        pool = [c for c in pool if (X[c] > 0).sum() >= 2]
        self.receiver = receiver
        self.pool = pool
        self.n = len(pool)
        self.truth = np.array([rec[c]["value"] for c in pool])
        self.cost = np.array([rec[c]["cost"] for c in pool])
        self.total = float(self.cost.sum())
        self.top = set(np.argsort(self.truth, kind="stable")[:C.TOPN].tolist())
        Xa = np.array([X[c] for c in pool])
        d2 = ((Xa[:, None, :] - Xa[None, :, :]) ** 2).sum(-1)
        self.K = np.exp(-d2 / (2 * 0.12 ** 2))
        # donor score vectors (higher = predicted more stable); NaN where the donor has no record
        self.donor = {}
        for a in AGENTS[:5]:
            t = tables[a]
            v = np.array([-t[c]["value"] if c in t else np.nan for c in pool])
            have = ~np.isnan(v)
            s = np.full(self.n, 0.5)
            s[have] = rank01(v[have])
            self.donor[a] = (s, have)


def surrogate(env: Env, vis: np.ndarray, todo: np.ndarray) -> np.ndarray:
    """Composition-kernel LCB from visible results, as rank score over todo (higher = better)."""
    E = np.flatnonzero(vis)
    if len(E) == 0:
        return np.full(len(todo), 0.5)
    y = env.truth[E]
    Kt = env.K[np.ix_(todo, E)]
    sw = Kt.sum(1)
    mu = (Kt @ y + y.mean()) / (sw + 1.0)
    pred = mu - 0.03 / np.sqrt(sw + 1.0)
    return rank01(-pred)


# ---------------------------------------------------------------- campaign

def run(env: Env, members: list[str], structure: str, seed: int, k: int = 4,
        theta: dict | None = None, log: bool = False, max_frac: float | None = None) -> dict:
    th = dict(DEFAULT_THETA, **(theta or {}), **STRUCT_THETA.get(structure, {}))
    rng = np.random.default_rng(seed)
    n = env.n
    jitter = rng.random(n) * 1e-9
    m = len(members)
    evald = np.zeros(n, bool)
    vis = np.zeros((m, n), bool)
    proposer = np.full(n, -1)
    pred = np.full((m, n), np.nan)        # score each agent gave a candidate just before its reveal
    scout = rng.random(n)
    # several decision bodies of one kind may sit in a team: a name "kind#j" is copy j of that kind.
    # A random scout copy draws its own random ordering (its own seed); a copy "kind=j" repeats the
    # plain body exactly. Plain names reproduce the single-copy campaigns of this experiment.
    copy_scout = {a: np.random.default_rng(crc(f"{seed}|{a}")).random(n)
                  for a in members if body_kind(a) == "explorer" and "#" in a}
    ema = np.zeros(m)
    tier = np.full(m, 2)                  # emergent: start flat (everyone in tier 2)
    morph = structure.startswith("emergent_morph")
    ntier = 1
    since = np.zeros(m)                   # batches since each member last changed tier
    if morph:
        tier = np.ones(m, int)            # morphing: one tier until the records separate
    if structure == "tiers_fixed":
        tier = np.array([FIXED_TIER[body_kind(a)] for a in members])
    credit = np.zeros(m)
    cost = 0.0
    curve, events = [], []
    order_rand = rng.permutation(n)
    emergent = structure.startswith("emergent")
    while not evald.all():
        todo = np.flatnonzero(~evald)
        if not members:   # empty team: the lab picks at random
            batch = [c for c in order_rand if not evald[c]][:k]
        else:
            # each agent scores the unevaluated pool with its local rule and its partial knowledge
            S = np.zeros((m, len(todo)))
            for i, a in enumerate(members):
                kind = body_kind(a)
                if kind == "explorer":
                    S[i] = rank01((scout if "#" not in a else copy_scout[a])[todo])
                    continue
                sur = surrogate(env, vis[i], todo)
                if kind == "surrogate":
                    S[i] = sur
                    continue
                ds, have = env.donor[kind]
                E = np.flatnonzero(vis[i] & have)
                t = ktau(ds[E], -env.truth[E]) if len(E) >= 3 else float("nan")
                w = 0.5 if not math.isfinite(t) else max(0.0, t) * len(E) / (len(E) + 8)
                S[i] = w * ds[todo] + (1 - w) * sur
            S += jitter[todo]
            # organisation: units (agents or cells), their slot weights
            if structure == "star":
                units = [list(range(m))]
                hub = 0
                weights = np.array([1.0])
                del hub   # the hub aggregates by mean rank score; its own column is one of the inputs
            elif emergent:
                if morph:
                    base = th["ratio"] ** (ntier - tier).astype(float)
                else:
                    base = np.where(tier == 1, th["ratio"] ** 2, np.where(tier == 2, th["ratio"], 1.0))
                base = np.where(ema < 0, th["floor"], base)
                # merge agents whose current orderings agree into temporary cells
                parent = list(range(m))

                def find(x):
                    while parent[x] != x:
                        parent[x] = parent[parent[x]]
                        x = parent[x]
                    return x
                if th["merge"] <= 1.0 and m > 1:
                    sub = todo if len(todo) <= 60 else rng.choice(len(todo), 60, replace=False)
                    cols = np.arange(len(todo)) if len(todo) <= 60 else sub
                    for i in range(m):
                        for j in range(i + 1, m):
                            if ktau(S[i, cols], S[j, cols]) >= th["merge"]:
                                parent[find(i)] = find(j)
                groups = {}
                for i in range(m):
                    groups.setdefault(find(i), []).append(i)
                units = list(groups.values())
                weights = np.array([base[u].max() for u in units])
            else:
                units = [[i] for i in range(m)]
                if structure == "tiers_fixed":
                    weights = np.array([{1: 4.0, 2: 2.0, 3: 1.0}[tier[i]] for i in range(m)])
                else:
                    weights = np.ones(m)
            # slot allocation: persistent stride credits, a unit takes its best unchosen candidate
            batch = []
            kk = min(k, len(todo))
            if len(units) == 1:
                u = units[0]
                sc = S[u].mean(0)
                pick = np.argsort(-sc, kind="stable")[:kk]
                batch = [int(todo[p]) for p in pick]
                for p in batch:
                    proposer[p] = u[0] if structure != "star" else -2
            else:
                ucred = np.array([credit[u].sum() for u in units]) + kk * weights / weights.sum()
                for ui, u in enumerate(units):
                    credit[u] += (kk * weights[ui] / weights.sum()) / len(u)
                usc = [S[u].mean(0) for u in units]
                chosen = set()
                for _ in range(kk):
                    ui = int(np.argmax(ucred + rng.random(len(units)) * 1e-9))
                    sc = usc[ui]
                    for p in np.argsort(-sc, kind="stable"):
                        if p not in chosen:
                            chosen.add(int(p))
                            batch.append(int(todo[p]))
                            proposer[todo[p]] = units[ui][0]
                            break
                    ucred[ui] -= 1.0
                    credit[units[ui]] -= 1.0 / len(units[ui])
            # predictions on the batch, recorded before the reveal
            pos = {int(c): j for j, c in enumerate(todo)}
            for c in batch:
                pred[:, c] = S[:, pos[c]]
        # reveal
        for c in batch:
            evald[c] = True
            cost += env.cost[c]
        bmask = np.zeros(n, bool)
        bmask[batch] = True
        if not members:
            pass
        elif structure in ("flat", "star"):
            vis |= bmask
        elif structure == "solo":
            for c in batch:
                vis[proposer[c], c] = True
        else:
            # hierarchical sharing: an agent sees results proposed at its tier or above; leaders see all;
            # in the emergent structure, members of one cell also share inside the cell
            cell_of = {}
            if emergent:
                for ui, u in enumerate(units):
                    for i in u:
                        cell_of[i] = ui
            for c in batch:
                p = proposer[c]
                for i in range(m):
                    if tier[i] == 1 or tier[p] <= tier[i] or i == p or (emergent and cell_of.get(i) == cell_of.get(p)):
                        vis[i, c] = True
        if members and emergent:
            # promotion protocol: prequential score on the results each agent can see
            q = np.zeros(m)
            for i in range(m):
                E = np.flatnonzero(vis[i] & evald & ~np.isnan(pred[i]))
                if len(E) >= 3:
                    q[i] = ktau(pred[i, E], -env.truth[E]) * len(E) / (len(E) + 8)
            ema = (1 - th["ema"]) * ema + th["ema"] * q
            if morph:
                # tiers from the gaps between running scores; the incumbency margin expires after
                # `tenure` batches in the same tier, so a position is temporary unless re-earned
                since += 1
                key = ema + th["margin"] * (ntier - tier) * (since <= th["tenure"])
                order = np.argsort(-key, kind="stable")
                new = np.ones(m, int)
                t = 1
                for a_, b_ in zip(order[:-1], order[1:]):
                    if key[a_] - key[b_] > th["gap"]:
                        t += 1
                    new[b_] = t
                ntier = t
                since[new != tier] = 0
            else:
                nl = int(round(th["n_lead"]))
                key = ema + th["margin"] * (3 - tier)       # incumbency margin for agents already higher
                order = np.argsort(-key, kind="stable")
                new = np.full(m, 3)
                new[order[:nl]] = 1
                new[order[nl:nl + 2]] = 2
            if log:
                events.append({"n": int(evald.sum()), "cost": float(cost), "tier": new.tolist(),
                               "ema": ema.round(4).tolist(),
                               "cells": [[members[i] for i in u] for u in units if len(u) > 1]})
            tier = new
        rec = len(env.top & set(np.flatnonzero(evald).tolist())) / C.TOPN
        curve.append({"n": int(evald.sum()), "cost": cost, "recall": rec})
        if max_frac is not None and cost >= max_frac * env.total:
            break
    out = {"curve": curve}
    if log:
        out["events"] = events
    return out


def value(env, members, structure, seeds, theta=None, tag=""):
    vals = []
    for s in seeds:
        r = run(env, members, structure, crc(f"{tag}|{structure}|{'+'.join(members)}|{s}"), theta=theta,
                max_frac=0.3)
        vals.append(C.summarise(r["curve"], env.total)["early_recall_area"])
    return float(np.mean(vals)), vals


def shapley(v: dict, players: list[str]) -> dict:
    n = len(players)
    phi = {}
    for p in players:
        others = [q for q in players if q != p]
        acc = 0.0
        for r in range(n):
            for Sx in itertools.combinations(others, r):
                w = math.factorial(r) * math.factorial(n - r - 1) / math.factorial(n)
                acc += w * (v[frozenset(Sx) | {p}] - v[frozenset(Sx)])
        phi[p] = acc
    return phi


# ---------------------------------------------------------------- stages

def learn_theta(env: Env, seeds, pop=16, iters=6, rng_seed=7, structure="emergent_learned") -> dict:
    bounds = MORPH_BOUNDS if structure.startswith("emergent_morph") else THETA_BOUNDS
    keys = list(bounds)
    lo = np.array([bounds[k][0] for k in keys])
    hi = np.array([bounds[k][1] for k in keys])
    mu = np.array([DEFAULT_THETA[k] for k in keys])
    sd = (hi - lo) / 4
    rng = np.random.default_rng(rng_seed)
    hist = []
    best = (-1.0, dict(DEFAULT_THETA))
    for it in range(iters):
        P = np.clip(mu + sd * rng.standard_normal((pop, len(keys))), lo, hi)
        P[0] = np.clip(mu, lo, hi)
        sc = []
        for row in P:
            th = dict(zip(keys, row.tolist()))
            sc.append(value(env, AGENTS, structure, seeds, theta=th, tag="train")[0])
        sc = np.array(sc)
        el = P[np.argsort(-sc)[:max(2, pop // 4)]]
        mu, sd = el.mean(0), np.maximum(el.std(0), 0.02 * (hi - lo))
        if sc.max() > best[0]:
            best = (float(sc.max()), dict(zip(keys, P[int(np.argmax(sc))].tolist())))
        hist.append({"iter": it, "best": float(sc.max()), "mean": float(sc.mean()), "mu": dict(zip(keys, mu.tolist()))})
        print(f"  CEM iter {it}: best {sc.max():.4f} mean {sc.mean():.4f}", flush=True)
    return {"theta": best[1], "train_value": best[0], "history": hist}


def selftest():
    env = Env("qe_pbe")
    ok = []
    # 1. a full run evaluates the whole pool exactly once and spends the full cost
    for st in STRUCTURES:
        r = run(env, AGENTS, st, 1)
        ok.append(abs(r["curve"][-1]["cost"] - env.total) < 1e-6 * env.total and r["curve"][-1]["n"] == env.n)
    # 2. determinism
    a = run(env, AGENTS, "emergent", 3)["curve"]
    b = run(env, AGENTS, "emergent", 3)["curve"]
    ok.append(a == b)
    # 3. a single agent: flat, solo and emergent coincide (no organisation to form)
    vs = [value(env, ["mace_relax"], st, range(3), tag="t")[0] for st in ("flat", "solo")]
    ok.append(abs(vs[0] - vs[1]) < 1e-12)
    # 4. Shapley efficiency on a toy game
    pl = ["a", "b", "c"]
    vv = {frozenset(S): len(S) ** 2 for r in range(4) for S in itertools.combinations(pl, r)}
    ok.append(abs(sum(shapley(vv, pl).values()) - 9) < 1e-12)
    # 5. tau orientation: a donor equal to -truth scores +1
    ok.append(abs(ktau(-env.truth[:20], -env.truth[:20]) - 1) < 1e-12)
    print("selftest", sum(ok), "/", len(ok), ok)
    return all(ok)


def theta_for(st: str, learned: dict) -> dict | None:
    if st == "emergent_learned":
        return learned.get("emergent_learned")
    if st == "emergent_morph_learned":
        return learned.get("emergent_morph_learned")
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--stage", default="all", choices=["learn", "team", "shapley", "all"])
    ap.add_argument("--train-seeds", type=int, default=8)
    ap.add_argument("--seeds", type=int, default=20)
    ap.add_argument("--shapley-seeds", type=int, default=8)
    ap.add_argument("--receivers", default="qe_pbe,qe_hse06,gpaw_r2scan")
    ap.add_argument("--structures", default=",".join(STRUCTURES),
                    help="subset to (re)run; results are merged into the existing JSON files")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(0 if selftest() else 1)
    OUT.mkdir(parents=True, exist_ok=True)
    recs = args.receivers.split(",")
    sts = args.structures.split(",")
    envs = {r: Env(r) for r in recs}
    learned = {}
    files = {"emergent_learned": OUT / "learned_theta.json",
             "emergent_morph_learned": OUT / "learned_theta_morph.json"}
    for st, f in files.items():
        if args.stage in ("learn", "all") and st in sts:
            t0 = time.time()
            res = learn_theta(envs["qe_pbe"], [1000 + s for s in range(args.train_seeds)], structure=st)
            res["seconds"] = time.time() - t0
            f.write_text(json.dumps(res, indent=1), encoding="utf-8")
            print("learned", st, res["theta"])
        if f.exists():
            learned[st] = json.loads(f.read_text(encoding="utf-8"))["theta"]
    if args.stage in ("team", "all"):
        grid = np.linspace(0, 1, 201)
        tfile = OUT / "team_values.json"
        team = json.loads(tfile.read_text(encoding="utf-8")) if tfile.exists() else {"receivers": {}}
        team["theta_default"] = DEFAULT_THETA
        team["theta_learned"] = learned.get("emergent_learned")
        team["theta_morph_learned"] = learned.get("emergent_morph_learned")
        for r, env in envs.items():
            row = team["receivers"].setdefault(r, {"structures": {}})
            row.update({"n_pool": env.n, "total_cost": env.total})
            for st in sts:
                th = theta_for(st, learned)
                ea, c8, curves, roles = [], [], [], []
                for s in range(args.seeds):
                    rr = run(env, AGENTS, st, crc(f"eval|{st}|{s}"), theta=th, log=st.startswith("emergent"))
                    sm = C.summarise(rr["curve"], env.total)
                    ea.append(sm["early_recall_area"])
                    c8.append(sm["cost_frac_to_8of10"])
                    cx = np.array([0.0] + [p["cost"] / env.total for p in rr["curve"]])
                    cy = np.array([0.0] + [p["recall"] for p in rr["curve"]])
                    curves.append(cy[np.searchsorted(cx, grid, side="right") - 1])
                    if "events" in rr:
                        roles.append(rr["events"])
                g = np.array(curves)
                ent = {"early_recall_area": {"mean": float(np.mean(ea)), "p05": float(np.percentile(ea, 5)),
                                             "p95": float(np.percentile(ea, 95)), "all": ea},
                       "cost_frac_to_8of10": {"mean": float(np.mean(c8)), "p05": float(np.percentile(c8, 5)),
                                              "p95": float(np.percentile(c8, 95))},
                       "band": {"grid": grid.tolist(), "mean": g.mean(0).tolist(),
                                "p05": np.percentile(g, 5, 0).tolist(), "p95": np.percentile(g, 95, 0).tolist()}}
                if roles:
                    ent["roles"] = role_stats(roles)
                    ent["geometry"] = geometry_stats(roles, env.total)
                row["structures"][st] = ent
                print(r, st, round(ent["early_recall_area"]["mean"], 4), round(ent["cost_frac_to_8of10"]["mean"], 4), flush=True)
        tfile.write_text(json.dumps(team, indent=1), encoding="utf-8")
    if args.stage in ("shapley", "all"):
        sfile = OUT / "shapley.json"
        sh = json.loads(sfile.read_text(encoding="utf-8")) if sfile.exists() else {}
        for r in [x for x in recs if x in ("qe_pbe", "qe_hse06")]:
            env = envs[r]
            sh.setdefault(r, {})
            for st in sts:
                th = theta_for(st, learned)
                t0 = time.time()
                v = {}
                for rr_ in range(len(AGENTS) + 1):
                    for Sx in itertools.combinations(AGENTS, rr_):
                        v[frozenset(Sx)] = value(env, list(Sx), st, range(args.shapley_seeds), theta=th, tag="shap")[0]
                phi = shapley(v, AGENTS)
                best = max(v, key=v.get)
                sh[r][st] = {"shapley": phi, "v_empty": v[frozenset()], "v_all": v[frozenset(AGENTS)],
                             "v_best": v[best], "best_coalition": sorted(best),
                             "v": {"+".join(sorted(k)): val for k, val in v.items()}}
                print(r, st, "shapley done", round(time.time() - t0), "s",
                      {a: round(x, 3) for a, x in phi.items()}, flush=True)
                sfile.write_text(json.dumps(sh, indent=1), encoding="utf-8")


def geometry_stats(runs: list[list[dict]], total: float) -> dict:
    """Shape of the organisation over the whole campaign, on a grid of the receiver compute fraction.

    Per batch: number of tiers, size of the top tier, number of cells, and whether the team is flat;
    per run: mean length (batches) of a member's consecutive spell in the top tier, and the number of
    batches in which the number of tiers changed."""
    grid = np.linspace(0, 1, 41)
    nt, top, cl = [], [], []
    spells, morphs = [], []
    for ev in runs:
        cx = np.array([e["cost"] / total for e in ev])
        T = np.array([len(set(e["tier"])) for e in ev], float)
        L = np.array([sum(1 for x in e["tier"] if x == 1) for e in ev], float)
        K = np.array([len(e["cells"]) for e in ev], float)
        ix = np.clip(np.searchsorted(cx, grid, side="right") - 1, 0, len(ev) - 1)
        nt.append(T[ix]); top.append(L[ix]); cl.append(K[ix])
        morphs.append(int((np.diff(T) != 0).sum()))
        for i in range(len(ev[0]["tier"])):
            run_len = 0
            for e in ev:
                if e["tier"][i] == 1:
                    run_len += 1
                elif run_len:
                    spells.append(run_len); run_len = 0
            if run_len:
                spells.append(run_len)
    nt, top, cl = np.array(nt), np.array(top), np.array(cl)

    def band(a):
        return {"mean": a.mean(0).tolist(), "p05": np.percentile(a, 5, 0).tolist(),
                "p95": np.percentile(a, 95, 0).tolist()}
    return {"grid": grid.tolist(), "n_tiers": band(nt), "top_size": band(top), "cells": band(cl),
            "flat_share": (nt == 1).mean(0).tolist(), "tier_count_changes_mean": float(np.mean(morphs)),
            "top_spell_mean": float(np.mean(spells)) if spells else 0.0,
            "top_spell_median": float(np.median(spells)) if spells else 0.0,
            "n_tiers_range": [int(nt.min()), int(nt.max())]}


def role_stats(runs: list[list[dict]]) -> dict:
    """Leader identity, leader changes, tier persistence and cells over the early window."""
    lead_share = {a: 0.0 for a in AGENTS}
    changes, persist, cells, cell_pairs = [], [], [], {}
    for ev in runs:
        ev = ev[:12]   # first twelve rounds = 48 evaluations, about the early window
        prev = None
        same = tot = 0
        ch = 0
        for e in ev:
            t = e["tier"]
            for i, a in enumerate(AGENTS):
                if t[i] == 1:
                    lead_share[a] += 1.0 / (len(ev) * len(runs))
            if prev is not None:
                same += sum(x == y for x, y in zip(t, prev))
                tot += len(t)
                ch += int([i for i, x in enumerate(t) if x == 1] != [i for i, x in enumerate(prev) if x == 1])
            prev = t
            cells.append(len(e["cells"]))
            for c in e["cells"]:
                key = "+".join(sorted(c))
                cell_pairs[key] = cell_pairs.get(key, 0) + 1
        changes.append(ch)
        persist.append(same / tot if tot else 1.0)
    nrounds = sum(min(12, len(ev)) for ev in runs)
    return {"leader_share": lead_share, "leader_changes_mean": float(np.mean(changes)),
            "tier_persistence_mean": float(np.mean(persist)), "cells_per_round_mean": float(np.mean(cells)),
            "cell_frequency": {k: v / nrounds for k, v in sorted(cell_pairs.items(), key=lambda x: -x[1])[:8]}}


if __name__ == "__main__":
    main()
