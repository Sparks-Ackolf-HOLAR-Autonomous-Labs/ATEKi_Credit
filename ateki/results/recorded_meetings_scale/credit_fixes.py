"""Exploratory (not registered): candidate fixes for the failed P4 and P5 of
experiment 11 at scale, computed on the existing recorded campaigns (no new
LLM runs). Run from this folder. Output: credit_fixes.json, CREDIT_FIXES.md
numbers. ASCII only.

P5 fixes (coordinator credit):
  - mean rule: a separated team is worth the member-weighted average of its
    groups' scores, v(S) = sum_c |c|/|S| v(c); unlike the sum rule it does
    not grow with the number of separated members.
  - role premium: the coordinator's credit minus the credit of the same
    agent (agent1, MP GGA) in the flat team of the same set, with a
    bootstrap interval. This removes the database from the coordinator's
    number and keeps only the role.
  - within-team placebo (S3 only): agent6 holds the same database as the
    coordinator in the same coordinator-led team but has no role.
  - interventional effect: team score of coordinator-led minus flat team,
    paired by seed.
P4 fixes (credit by database):
  - bootstrap probability that each database is in the top two, instead of
    a yes/no on the mean.
  - standalone accuracy of each database's family order (Kendall tau
    against the measured order) and its rank correlation with credit.
"""
import json
from pathlib import Path

import numpy as np
from scipy.stats import kendalltau, spearmanr

HERE = Path(__file__).resolve().parent
src = open(HERE / "analyze_scale.py").read()
pre = src.split("pc = exp26.load_universe")[0]
__file__ = str((HERE / "analyze_scale.py").resolve())
exec(pre)  # ShapleyEngine, comps, max_rule_shares, DBL

rng = np.random.default_rng(1)


def V_of(g):
    return {frozenset(k.split(",")) if k != "-" else frozenset(): v
            for k, v in g["attribution"]["v"].items()}


def shares(g, rule):
    P = sorted(g["agents"], key=lambda a: int(a[5:]))
    V = V_of(g)
    H = g["attribution"]["hyperedges"]

    def val(S):
        S = set(S)
        if not S:
            return 0.0
        cs = comps(S, H)
        if rule == "sum":
            return sum(V[c] for c in cs)
        if rule == "max":
            return max(V[c] for c in cs)
        return sum(len(c) / len(S) * V[c] for c in cs)  # mean rule
    sc = ShapleyEngine(P, val).exact().scores
    tot = abs(V[frozenset(P)]) or 1e-9
    return {a: sc[a] / tot for a in P}


def ci(x, n=5000):
    x = np.asarray(x)
    m = [rng.choice(x, len(x)).mean() for _ in range(n)]
    return [round(float(np.percentile(m, 2.5)), 3),
            round(float(np.percentile(m, 97.5)), 3)]


def load(s, arm):
    fs = sorted((HERE / s / "campaigns").glob(arm + "_s*.json"))
    fs = [f for f in fs if not f.name.endswith(".raw.json")]
    return {int(f.stem.split("_s")[1]): json.load(open(f)) for f in fs}


out = {}
for s in ["S1", "S2", "S3"]:
    fl, orc = load(s, "flat"), load(s, "orchestrated")
    R = {}
    for rule in ["sum", "max", "mean"]:
        co = [shares(g, rule)["agent1"] for g in orc.values()]
        fa = [shares(g, rule)["agent1"] for g in fl.values()]
        prem = [a - b for a, b in zip(
            co, [np.mean(fa)] * len(co))]
        r = {"coordinator": round(float(np.mean(co)), 3),
             "coordinator_ci95": ci(co),
             "coordinator_positive": "%d/%d" % (sum(x > 0 for x in co),
                                                len(co)),
             "same_agent_in_flat_team": round(float(np.mean(fa)), 3),
             "role_premium": round(float(np.mean(co) - np.mean(fa)), 3),
             "role_premium_ci95": [round(float(np.percentile(
                 [rng.choice(co, len(co)).mean()
                  - rng.choice(fa, len(fa)).mean() for _ in range(5000)],
                 q)), 3) for q in (2.5, 97.5)]}
        if s == "S3":
            pl = [shares(g, rule)["agent6"] for g in orc.values()]
            r["placebo_agent6_same_db"] = round(float(np.mean(pl)), 3)
            r["coordinator_minus_placebo"] = round(
                float(np.mean(np.subtract(co, pl))), 3)
            r["coordinator_minus_placebo_ci95"] = ci(np.subtract(co, pl))
        R[rule] = r
    full = lambda g: ",".join(sorted(g["agents"], key=lambda a: int(a[5:])))
    seeds = sorted(set(fl) & set(orc))
    d = [orc[k]["attribution"]["v"][",".join(sorted(orc[k]["agents"]))]
         - fl[k]["attribution"]["v"][",".join(sorted(fl[k]["agents"]))]
         for k in seeds]
    R["interventional_coord_minus_flat_paired"] = {
        "n_pairs": len(seeds), "mean": round(float(np.mean(d)), 3),
        "ci95": ci(d), "coordinator_better": "%d/%d" % (
            sum(x > 0 for x in d), len(d))}
    # P4: credit by database with bootstrap top-two probability
    for arm, L in [("flat", fl), ("orchestrated", orc)]:
        gs = list(L.values())
        P = sorted(gs[0]["agents"], key=lambda a: int(a[5:]))
        per = []
        for g in gs:
            tot = abs(g["attribution"]["v"][",".join(sorted(P))]) or 1e-9
            per.append({DBL[d]: sum(g["attribution"]["shapley"][a]
                                    for a in P if g["agents"][a] == d) / tot
                        for d in DBL})
        names = list(DBL.values())
        M = np.array([[p[n] for n in names] for p in per])
        top2 = np.zeros(len(names))
        first = np.zeros(len(names))
        B = 4000
        for _ in range(B):
            m = M[rng.integers(0, len(M), len(M))].mean(0)
            o = np.argsort(-m)
            top2[o[:2]] += 1
            first[o[0]] += 1
        # standalone accuracy: Kendall tau of each database's own order
        g0 = gs[0]
        ref = g0["reference_ranking"]
        stand = {}
        for d in DBL:
            a = next(a for a in P if g0["agents"][a] == d)
            order = g0["donor_ranks"][a]
            stand[DBL[d]] = round(float(kendalltau(
                [ref.index(f) for f in order], range(len(order)))[0]), 3)
        mean_share = dict(zip(names, M.mean(0).round(3).tolist()))
        rho = spearmanr([stand[n] for n in names],
                        [mean_share[n] for n in names])
        R["credit_" + arm] = {
            "mean_share": mean_share,
            "p_top2": dict(zip(names, (top2 / B).round(3).tolist())),
            "p_first": dict(zip(names, (first / B).round(3).tolist())),
            "standalone_tau": stand,
            "spearman_credit_vs_standalone": [round(float(rho[0]), 3),
                                              round(float(rho[1]), 3)]}
    out[s] = R
json.dump(out, open(HERE / "credit_fixes.json", "w"), indent=1)
print(json.dumps(out, indent=1))
