"""Experiment 19: credit that is not shared equally.

Question (ATEKi): the Shapley value splits every joint gain of a coalition equally among its members
(symmetry), and experiment 18 splits a member that belongs to two swarms equally between them. A
consortium often divides credit unequally on purpose: by the compute each party spent, by what each
party achieves alone, by seniority, or in proportion to individual merit. What happens to the credit of
the seven computed Al-Mg-Si advisers under such rules, and which conclusions of the equal split hold?

Part A, one swarm of the seven bodies (start one_7, fixed structure, no member rules; the campaign of
experiments 14 to 18 on receivers QE PBE, QE HSE06 and GPAW r2SCAN; value = early-window recall area of
the ten most stable compounds; 100 matched seeds; every one of the 128 coalitions run per seed).
The Harsanyi dividend d(T) of a coalition T is the gain that T produces beyond all its sub-coalitions.
The Shapley value gives each member of T the share 1/|T| of d(T). The weighted Shapley value of
Kalai and Samet (1987) gives member i the share w_i / sum_{j in T} w_j, and with an ordered partition of
the players (seniority) gives d(T) to the most senior members present in T, in equal parts. Every such
rule keeps efficiency (credits sum to v(N) - v(empty)) and gives each member its own solo gain; it
changes only how joint gains and joint losses (negative dividends) are divided. Rules:
  equal        w_i = 1 (Shapley)
  compute      w_i = compute spent producing the body's advice over the pool (seconds, floor 1 s)
  inv_compute  w_i = 1 / that compute (the low-cost source receives the larger share)
  solo         w_i = max(v({i}) - v(empty), 0.01) (merit shown alone, mean over seeds)
  seniority    ordered partition by the fixed tiers of experiment 14 (tier 1 most senior)
  proportional (not a Shapley rule) v(N) - v(empty) divided in proportion to the positive solo gains
A continuous family w_i = compute_i ** alpha, alpha in [-1, 1], joins inv_compute (alpha = -1), equal
(alpha = 0) and compute (alpha = 1).

Part B, a member in two swarms (experiment 18, rule move+share with its learned thresholds, fixed
structure, starts 4+3 and 2+2+3, receivers PBE and HSE06). Experiment 18 averaged the level structure
value over the partitions that place each shared member in its own swarm or in its second swarm with
equal weights. Here the member is placed in its own swarm with weight h and in the second swarm with
weight 1 - h, h in {0, 0.25, 0.5, 0.75, 1}. h = 1 follows the batch slots (a shared member's slots come
from its own swarm); h = 0 follows the information it passes on.

Outputs: results/unequal_credit/{part_a.json, part_b.json, unequal_credit.md}
Usage (from ateki/, environment with numpy, scipy, ase):
    python experiments/19_unequal_credit.py --selftest
    python experiments/19_unequal_credit.py --part a --seeds 100 --workers 12
    python experiments/19_unequal_credit.py --part b --seeds 40 --workers 12
ASCII only.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, HERE / fn)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


E18 = _load("e18", "18_mobile_members.py")
E17, E14 = E18.E17, E18.E14
C = E14.C
A = E14.AGENTS
OUT = HERE.parent / "results" / "unequal_credit"
RECEIVERS_A = ["qe_pbe", "qe_hse06", "gpaw_r2scan"]
RECEIVERS_B = ["qe_pbe", "qe_hse06"]
RULES = ["equal", "compute", "inv_compute", "solo", "seniority", "proportional"]
ALPHAS = [round(x, 2) for x in np.linspace(-1.0, 1.0, 21)]
H_GRID = [0.0, 0.25, 0.5, 0.75, 1.0]
COST_FLOOR = 1.0
NONCOMPUTE = {"surrogate", "explorer"}   # proposals only; no advice table is computed for them


def advice_compute():
    """Seconds of compute each body spends producing its advice over the pool (floor 1 s)."""
    t = C.load_tables()
    out = {}
    for a in A:
        c = sum(r["cost"] for r in t[a].values()) if (a in t and a not in NONCOMPUTE) else 0.0
        out[a] = max(float(c), COST_FLOOR)
    return out


# ------------------------------------------------------------------ dividends and weighted values

def dividends(v, players):
    """Harsanyi dividends d(T) for every non-empty T (arrays over seeds)."""
    d = {}
    for r in range(1, len(players) + 1):
        for T in itertools.combinations(players, r):
            acc = 0.0
            for q in range(0, r + 1):
                for S in itertools.combinations(T, q):
                    acc = acc + ((-1) ** (r - q)) * v[frozenset(S)]
            d[frozenset(T)] = acc
    return d


def weighted_value(d, players, w=None, order=None, sign=None):
    """Kalai-Samet weighted Shapley value from dividends.

    w: player -> positive weight (None = equal); order: player -> class (lower = more senior), the
    dividend of T goes in equal parts to the members of T in the most senior class present.
    sign: None for the full value, "pos" or "neg" to keep only dividends whose mean is of that sign."""
    phi = {p: 0.0 for p in players}
    for T, dT in d.items():
        m = float(np.mean(dT))
        if (sign == "pos" and m <= 0) or (sign == "neg" and m >= 0):
            continue
        mem = sorted(T)
        if order is not None:
            top = min(order[p] for p in mem)
            mem = [p for p in mem if order[p] == top]
        ww = {p: (1.0 if w is None else w[p]) for p in mem}
        tot = sum(ww.values())
        for p in mem:
            phi[p] = phi[p] + dT * (ww[p] / tot)
    return phi


def proportional(v, players):
    v0, vN = v[frozenset()], v[frozenset(players)]
    g = {p: np.maximum(v[frozenset([p])] - v0, 0.0) for p in players}
    tot = sum(g.values())
    tot = np.where(tot > 0, tot, 1.0)
    return {p: (vN - v0) * g[p] / tot for p in players}


def boot(x, n=2000, seed=0):
    x = np.atleast_1d(np.asarray(x, float))
    b = x[np.random.default_rng(seed).integers(0, len(x), (n, len(x)))].mean(1)
    return [float(x.mean()), float(np.percentile(b, 5)), float(np.percentile(b, 95))]


# ------------------------------------------------------------------ part A

def coalition_values(receiver, start, mode, rule, seeds, theta):
    env = E14.Env(receiver)
    v = {}
    for r in range(len(A) + 1):
        for Sx in itertools.combinations(A, r):
            Ss = set(Sx)
            v[frozenset(Sx)] = E18.early_value(env, [[a for a in s if a in Ss] for s in start], mode, rule, seeds, theta)
    return v


def job_a(args):
    receiver, nseeds = args
    seeds = E18.seeds_for(receiver, nseeds, tag="exp19a")
    v = coalition_values(receiver, E17.STARTS["one_7"], "fixed", "none", seeds, None)
    cost = advice_compute()
    d = dividends(v, A)
    solo_w = {p: max(float(np.mean(v[frozenset([p])] - v[frozenset()])), 0.01) for p in A}
    rules = {
        "equal": weighted_value(d, A),
        "compute": weighted_value(d, A, w=cost),
        "inv_compute": weighted_value(d, A, w={p: 1.0 / cost[p] for p in A}),
        "solo": weighted_value(d, A, w=solo_w),
        "seniority": weighted_value(d, A, order=E14.FIXED_TIER),
        "proportional": proportional(v, A),
    }
    parts = {}
    for name, w, order in (("equal", None, None), ("compute", cost, None),
                           ("inv_compute", {p: 1.0 / cost[p] for p in A}, None), ("solo", solo_w, None),
                           ("seniority", None, E14.FIXED_TIER)):
        parts[name] = {s: weighted_value(d, A, w=w, order=order, sign=s) for s in ("pos", "neg")}
    alpha = {str(al): weighted_value(d, A, w={p: cost[p] ** al for p in A}) for al in ALPHAS}
    v0, vN = v[frozenset()], v[frozenset(A)]
    best = max(A, key=lambda p: float(np.mean(v[frozenset([p])])))
    res = {
        "bodies": A, "compute_s": cost, "solo_weights": solo_w, "tiers": E14.FIXED_TIER,
        "v_empty": boot(v0), "v_all": boot(vN), "best_single": best, "v_best_single": boot(v[frozenset([best])]),
        "solo_gain": {p: boot(v[frozenset([p])] - v0) for p in A},
        "credit": {r: {p: boot(x[p]) for p in A} for r, x in rules.items()},
        "minus_equal": {r: {p: boot(x[p] - rules["equal"][p]) for p in A} for r, x in rules.items() if r != "equal"},
        "gains_part": {r: {p: boot(x["pos"][p]) for p in A} for r, x in parts.items()},
        "losses_part": {r: {p: boot(x["neg"][p]) for p in A} for r, x in parts.items()},
        "alpha": {al: {p: boot(x[p]) for p in A} for al, x in alpha.items()},
        "efficiency_gap": {r: float(np.max(np.abs(sum(x[p] for p in A) - (vN - v0)))) for r, x in rules.items()},
        "rank": {r: sorted(A, key=lambda p: -float(np.mean(x[p]))) for r, x in rules.items()},
        "large_dividends": sorted(({"T": sorted(T), "d": boot(dT)} for T, dT in d.items() if len(T) > 1),
                                  key=lambda e: -abs(e["d"][0]))[:10],
    }
    return receiver, res


# ------------------------------------------------------------------ part B

def weighted_covers(structure, guests, h):
    """Partitions from experiment 18's cover_partitions with weights h (own swarm) and 1 - h (second)."""
    parts = E18.cover_partitions(structure, guests)
    loc = {tuple(sorted(sw_)) for g in structure for sw_ in g}
    shared = [a for a, sw in guests.items() if a not in sw and tuple(sw) in loc]
    wts = []
    for pick in itertools.product((0, 1), repeat=len(shared)):
        wts.append(float(np.prod([h if p == 0 else 1.0 - h for p in pick])) if shared else 1.0)
    return list(zip(parts, wts))


def job_b(args):
    receiver, start, nseeds, theta = args
    env = E14.Env(receiver)
    seeds = E18.seeds_for(receiver, nseeds, tag="exp17game")
    sw = E17.STARTS[start]
    v = coalition_values(receiver, sw, "fixed", "move+share", seeds, theta)
    sh = E17.level_value(v, A, [])
    lim = 0.25 * env.total
    tv = {h: {a: np.zeros(len(seeds)) for a in A} for h in H_GRID}
    cache = {}
    nshared = np.zeros(len(seeds))
    for j, s in enumerate(seeds):
        r = E18.run_mobile(env, sw, "fixed", "move+share", seed=s, theta=theta, max_frac=0.3, log=True)
        prev, state, wts = 0.0, ([[list(x)] for x in sw], {}), {}
        for e in r["events"]:
            c0, c1 = prev, min(e["cost"], lim)
            if c1 > c0:
                key = json.dumps([sorted(sorted(map(sorted, g)) for g in state[0]),
                                  {a: g for a, g in sorted(state[1].items())}])
                wts[key] = wts.get(key, 0.0) + (c1 - c0)
            prev = e["cost"]
            state = (e["structure"], e["guests"])
            if prev >= lim:
                break
        tot = sum(wts.values())
        for key, w in wts.items():
            st, gu = json.loads(key)
            nshared[j] += (w / tot) * sum(1 for a, g in gu.items() if a not in g)
            for h in H_GRID:
                ck = (key, h)
                if ck not in cache:
                    acc = {a: 0.0 for a in A}
                    for P, pw in weighted_covers(st, gu, h):
                        if pw == 0.0:
                            continue
                        lv = E17.level_value(v, A, E17.structure_levels(P))
                        for a in A:
                            acc[a] = acc[a] + pw * lv[a]
                    cache[ck] = acc
                for a in A:
                    tv[h][a][j] += (w / tot) * cache[ck][a][j]
    vN, v0 = v[frozenset(A)], v[frozenset()]
    res = {
        "bodies": A, "start": start, "mean_shared_members": boot(nshared),
        "shapley": {a: boot(sh[a]) for a in A},
        "credit": {str(h): {a: boot(tv[h][a]) for a in A} for h in H_GRID},
        "minus_shapley": {str(h): {a: boot(tv[h][a] - sh[a]) for a in A} for h in H_GRID},
        "minus_equal_split": {str(h): {a: boot(tv[h][a] - tv[0.5][a]) for a in A} for h in H_GRID},
        "efficiency_gap": {str(h): float(np.max(np.abs(sum(tv[h][a] for a in A) - (vN - v0)))) for h in H_GRID},
    }
    return receiver, start, res


# ------------------------------------------------------------------ self-test

def selftest():
    ok = []
    pl = ["a", "b", "c", "d", "e"]
    rng = np.random.default_rng(1)
    v = {frozenset(S): np.array([0.0 if not S else rng.normal() + len(S) for _ in range(3)])
         for r in range(6) for S in itertools.combinations(pl, r)}
    v[frozenset()] = np.array([0.2, 0.1, 0.3])
    d = dividends(v, pl)
    # 1. dividends reconstruct v
    ok.append(all(np.allclose(sum(d[frozenset(T)] for q in range(1, len(S) + 1) for T in itertools.combinations(S, q))
                              + v[frozenset()], v[frozenset(S)]) for r in range(1, 6) for S in itertools.combinations(pl, r)))
    # 2. equal weights = Shapley (permutation enumeration of experiment 17)
    sh = E17.level_value(v, pl, [])
    eq = weighted_value(d, pl)
    ok.append(all(np.allclose(eq[p], sh[p]) for p in pl))
    # 3. any weights and any seniority order keep efficiency; solo dividend stays with the player
    w = {p: rng.random() + 0.1 for p in pl}
    for x in (weighted_value(d, pl, w=w), weighted_value(d, pl, order={"a": 1, "b": 1, "c": 2, "d": 3, "e": 3}),
              proportional(v, pl)):
        ok.append(np.allclose(sum(x.values()), v[frozenset(pl)] - v[frozenset()]))
    # 4. a one-player game: weights do not matter
    v1 = {frozenset(): np.zeros(1), frozenset(["a"]): np.ones(1)}
    ok.append(np.allclose(weighted_value(dividends(v1, ["a"]), ["a"], w={"a": 5.0})["a"], 1.0))
    # 5. positive and negative parts add up to the full value
    full = weighted_value(d, pl, w=w)
    pos, neg = weighted_value(d, pl, w=w, sign="pos"), weighted_value(d, pl, w=w, sign="neg")
    ok.append(all(np.allclose(full[p], pos[p] + neg[p]) for p in pl))
    # 6. cover weights: h = 0.5 equals experiment 18; weights sum to 1
    st = [[["a", "b"], ["c"]], [["d", "e"]]]
    cw = weighted_covers(st, {"c": ["d", "e"], "a": ["d", "e"]}, 0.3)
    ok.append(abs(sum(w_ for _, w_ in cw) - 1.0) < 1e-12 and len(cw) == 4)
    ok.append([p for p, _ in weighted_covers(st, {"c": ["d", "e"]}, 0.5)] == E18.cover_partitions(st, {"c": ["d", "e"]}))
    ok.append(weighted_covers(st, {}, 0.2) == [(st, 1.0)])
    print("selftest", sum(ok), "/", len(ok), "failed at", [i for i, x in enumerate(ok) if not x])
    return all(ok)


# ------------------------------------------------------------------ report

LAB = E14.LABEL
RULE_LAB = {"equal": "equal (Shapley)", "compute": "by compute spent", "inv_compute": "by inverse compute",
            "solo": "by solo gain", "seniority": "by seniority (tiers)", "proportional": "proportional to solo gain"}


def write_report(pa, pb):
    f = lambda x: f"{x[0]:+.3f} [{x[1]:+.3f}, {x[2]:+.3f}]"
    L = ["# Experiment 19: credit that is not shared equally", "",
         "Value = early-window recall area of the ten most stable compounds; mean [5th, 95th percentile of the",
         "matched-seed mean by bootstrap].", ""]
    for r, x in pa.items():
        L += [f"## Part A, receiver {r} (one swarm of seven)",
              f"v(empty) {f(x['v_empty'])}, v(all) {f(x['v_all'])}, best single {x['best_single']} {f(x['v_best_single'])}", "",
              "| body | compute (s) | solo gain | " + " | ".join(RULE_LAB[k] for k in RULES) + " |",
              "|---" * (3 + len(RULES)) + "|"]
        for p in A:
            L.append(f"| {LAB[p]} | {x['compute_s'][p]:.0f} | {f(x['solo_gain'][p])} | "
                     + " | ".join(f(x["credit"][k][p]) for k in RULES) + " |")
        L += ["", "Rank (first to last): " + "; ".join(f"{k}: " + " > ".join(LAB[p] for p in x["rank"][k]) for k in RULES), "",
              "Joint gains and joint losses (positive and negative dividends) received per rule:", "",
              "| body | " + " | ".join(f"{RULE_LAB[k]} gains / losses" for k in x["gains_part"]) + " |",
              "|---" * (1 + len(x["gains_part"])) + "|"]
        for p in A:
            L.append(f"| {LAB[p]} | " + " | ".join(f"{x['gains_part'][k][p][0]:+.3f} / {x['losses_part'][k][p][0]:+.3f}"
                                                  for k in x["gains_part"]) + " |")
        L += ["", "Largest joint dividends: " + "; ".join("+".join(LAB[p] for p in e["T"]) + f" {e['d'][0]:+.3f}"
                                                         for e in x["large_dividends"][:6]),
              f"Efficiency gaps: " + ", ".join(f"{k} {g:.1e}" for k, g in x["efficiency_gap"].items()), ""]
    for key, x in pb.items():
        L += [f"## Part B, {key} (move+share, learned thresholds, fixed structure)",
              f"mean shared members in the early window {f(x['mean_shared_members'])}", "",
              "| body | Shapley | " + " | ".join(f"h = {h}" for h in H_GRID) + " | h = 1 minus h = 0 |", "|---" * (3 + len(H_GRID)) + "|"]
        for a in A:
            d10 = [x["credit"]["1.0"][a][0] - x["credit"]["0.0"][a][0]]
            L.append(f"| {LAB[a]} | {f(x['shapley'][a])} | " + " | ".join(f(x["credit"][str(h)][a]) for h in H_GRID)
                     + f" | {d10[0]:+.3f} |")
        L += ["", "Efficiency gaps: " + ", ".join(f"h={h} {g:.1e}" for h, g in x["efficiency_gap"].items()), ""]
    (OUT / "unequal_credit.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--part", default="a", choices=["a", "b", "report"])
    ap.add_argument("--seeds", type=int, default=100)
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    if args.selftest:
        raise SystemExit(0 if selftest() else 1)
    OUT.mkdir(parents=True, exist_ok=True)
    fa, fb = OUT / "part_a.json", OUT / "part_b.json"
    pa = json.loads(fa.read_text(encoding="utf-8")) if fa.exists() else {}
    pb = json.loads(fb.read_text(encoding="utf-8")) if fb.exists() else {}
    t0 = time.time()
    if args.part == "a":
        with Pool(min(args.workers, len(RECEIVERS_A))) as pool:
            for r, res in pool.imap_unordered(job_a, [(r, args.seeds) for r in RECEIVERS_A]):
                pa[r] = res
                fa.write_text(json.dumps(pa, indent=1), encoding="utf-8")
                print("part a", r, round(time.time() - t0), "s", flush=True)
    if args.part == "b":
        learned = json.loads((E18.OUT / "learned_theta.json").read_text(encoding="utf-8"))["theta"]
        jobs = [(r, st, args.seeds, learned) for r in RECEIVERS_B for st in ("split_4_3", "split_2_2_3")]
        with Pool(min(args.workers, len(jobs))) as pool:
            for r, st, res in pool.imap_unordered(job_b, jobs):
                pb[f"{r}|{st}"] = res
                fb.write_text(json.dumps(pb, indent=1), encoding="utf-8")
                print("part b", r, st, round(time.time() - t0), "s", flush=True)
    write_report(pa, pb)


if __name__ == "__main__":
    main()
