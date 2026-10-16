"""Summarise and grade ATEKi experiment 13 (recorded coordinator-led meetings).
Reads flat/campaigns/*.json and rot<r>/campaigns/*.json from this folder,
writes summary_coordinator.json, GRADING.md (interim if campaigns are missing) and
fig_coordinator.png. Predictions: PREDICTION.md. Run from this folder. ASCII only."""
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ATEKI = HERE.parent.parent
sys.path.insert(0, str(ATEKI))
from analysis.shapley import ShapleyEngine  # noqa: E402

DB_ORDER = ["mp_gga", "mp_r2scan", "jarvis_optb88vdw", "jarvis_mbj",
            "snumat_hse"]
DBL = {"mp_gga": "MP GGA", "mp_r2scan": "MP r2SCAN",
       "jarvis_optb88vdw": "JARVIS OptB88vdW", "jarvis_mbj": "JARVIS TB-mBJ",
       "snumat_hse": "SNUMAT HSE06"}
STANDALONE = {"snumat_hse": 0.90, "mp_r2scan": 0.85, "jarvis_mbj": 0.82,
              "jarvis_optb88vdw": 0.79, "mp_gga": 0.69}
N_EXPECTED = 20
B = 5000
rng = np.random.default_rng(4)


def load(sub):
    out = {}
    for f in sorted((HERE / sub / "campaigns").glob("*_s*.json")):
        if f.name.endswith(".raw.json"):
            continue
        out[int(f.stem.split("_s")[1])] = json.load(open(f, encoding="utf-8"))
    return out


def comps(S, H):
    par = {p: p for p in S}

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for e in H:
        if set(e) <= S:
            r = f(e[0])
            for x in e[1:]:
                par[f(x)] = r
    out = {}
    for p in S:
        out.setdefault(f(p), set()).add(p)
    return [frozenset(c) for c in out.values()]


def full_key(g):
    return ",".join(sorted(g["agents"]))


def team_tau(g):
    return g["attribution"]["v"][full_key(g)]


def rule_shares(g, rule):
    """Shares (of |team score|) of the hypergraph-restricted game on the
    recorded conference structure, with a separated team valued by the
    sum, best-group (max) or member-weighted mean of its groups."""
    P = sorted(g["agents"], key=lambda a: int(a[5:]))
    V = {frozenset(k.split(",")) if k != "-" else frozenset(): v
         for k, v in g["attribution"]["v"].items()}
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
        return sum(len(c) / len(S) * V[c] for c in cs)
    sc = ShapleyEngine(P, val).exact().scores
    tot = abs(V[frozenset(P)]) or 1e-9
    return {a: sc[a] / tot for a in P}


def agent_of(g, db):
    return next(a for a, d in g["agents"].items() if d == db)


def boot_mean_ci(x):
    x = np.asarray(x, float)
    m = x[rng.integers(0, len(x), (B, len(x)))].mean(1)
    return [round(float(np.percentile(m, 2.5)), 3),
            round(float(np.percentile(m, 97.5)), 3)]


def db_credit(gs):
    """Plain Shapley share per database (share of |team score|)."""
    rows = []
    for g in gs:
        tot = abs(team_tau(g)) or 1e-9
        sh = g["attribution"]["shapley"]
        rows.append([sum(sh[a] for a, d in g["agents"].items() if d == db)
                     / tot for db in DB_ORDER])
    M = np.array(rows)
    top2 = np.zeros(5)
    last = np.zeros(5)
    for _ in range(B):
        m = M[rng.integers(0, len(M), len(M))].mean(0)
        o = np.argsort(-m)
        top2[o[:2]] += 1
        last[o[-1]] += 1
    mean = M.mean(0)
    rank_c = np.argsort(np.argsort(-mean))
    rank_s = np.argsort(np.argsort([-STANDALONE[d] for d in DB_ORDER]))
    rho = 1 - 6 * np.sum((rank_c - rank_s) ** 2) / (5 * 24)
    return {"n": len(gs),
            "mean_share": {DBL[d]: round(float(v), 3)
                           for d, v in zip(DB_ORDER, mean)},
            "p_top2": {DBL[d]: round(float(v / B), 3)
                       for d, v in zip(DB_ORDER, top2)},
            "p_last": {DBL[d]: round(float(v / B), 3)
                       for d, v in zip(DB_ORDER, last)},
            "spearman_vs_standalone": round(float(rho), 3)}


def distinct_share(g):
    return len({tuple(sorted(q["query"])) for q in g["queries"]}) / len(
        g["queries"])


def main():
    flat = load("flat")
    rot = {r: load(f"rot{r}") for r in range(5)}
    n_done = len(flat) + sum(len(v) for v in rot.values())
    complete = len(flat) == N_EXPECTED and all(
        len(v) == N_EXPECTED for v in rot.values())
    S = {"n_campaigns": n_done, "complete": complete,
         "n_flat": len(flat), "n_rot": {r: len(v) for r, v in rot.items()},
         "fallbacks": sum(g["fallbacks"] for g in flat.values())
         + sum(g["fallbacks"] for v in rot.values() for g in v.values()),
         "llm_calls": sum(g["llm_calls"] for g in flat.values())
         + sum(g["llm_calls"] for v in rot.values() for g in v.values())}

    # team tau per cell
    S["team_tau"] = {"flat": {"mean": round(float(np.mean(
        [team_tau(g) for g in flat.values()])), 3),
        "ci95": boot_mean_ci([team_tau(g) for g in flat.values()])}}
    for r, v in rot.items():
        if v:
            x = [team_tau(g) for g in v.values()]
            S["team_tau"][f"coord_{DBL[DB_ORDER[r]]}"] = {
                "mean": round(float(np.mean(x)), 3), "ci95": boot_mean_ci(x)}

    # role premium (paired by seed) under three rules; Q1, Q2
    flat_sh = {rule: {s: rule_shares(g, rule) for s, g in flat.items()}
               for rule in ("mean", "sum", "max")}
    prem = {rule: {} for rule in flat_sh}
    coord = {rule: {} for rule in flat_sh}
    for rule in flat_sh:
        for r, v in rot.items():
            db = DB_ORDER[r]
            for s, g in v.items():
                if s not in flat:
                    continue
                c = rule_shares(g, rule)["agent1"]
                ctrl = flat_sh[rule][s][agent_of(flat[s], db)]
                prem[rule].setdefault(r, []).append(c - ctrl)
                coord[rule].setdefault(r, []).append(c)
    S["role_premium"] = {}
    for rule in prem:
        pooled = [x for v in prem[rule].values() for x in v]
        S["role_premium"][rule] = {
            "pooled_mean": round(float(np.mean(pooled)), 3) if pooled else None,
            "pooled_ci95": boot_mean_ci(pooled) if pooled else None,
            "n_pairs": len(pooled),
            "coordinator_share_pooled": round(float(np.mean(
                [x for v in coord[rule].values() for x in v])), 3)
            if pooled else None,
            "by_coordinator_db": {DBL[DB_ORDER[r]]: {
                "premium": round(float(np.mean(v)), 3),
                "ci95": boot_mean_ci(v), "n": len(v),
                "coordinator_share": round(float(np.mean(coord[rule][r])), 3)}
                for r, v in prem[rule].items()}}

    # credit by database; Q3
    S["credit_flat"] = db_credit(list(flat.values()))
    pooled_orch = [g for v in rot.values() for g in v.values()]
    S["credit_coord_pooled"] = db_credit(pooled_orch)

    # effect of a coordinator, paired by seed; Q4
    d_all, d_by = [], {}
    for r, v in rot.items():
        for s, g in v.items():
            if s in flat:
                d = team_tau(g) - team_tau(flat[s])
                d_all.append(d)
                d_by.setdefault(r, []).append(d)
    S["coordinator_effect"] = {
        "pooled_mean": round(float(np.mean(d_all)), 3),
        "pooled_ci95": boot_mean_ci(d_all), "n_pairs": len(d_all),
        "coordinator_better": "%d/%d" % (sum(x > 0 for x in d_all),
                                         len(d_all)),
        "by_coordinator_db": {DBL[DB_ORDER[r]]: {
            "mean": round(float(np.mean(v)), 3), "ci95": boot_mean_ci(v)}
            for r, v in d_by.items()}}

    # HSE06 vs GGA coordinator; Q5
    a = np.array([team_tau(g) for g in rot[4].values()])
    b = np.array([team_tau(g) for g in rot[0].values()])
    if len(a) and len(b):
        diffs = (a[rng.integers(0, len(a), (B, len(a)))].mean(1)
                 - b[rng.integers(0, len(b), (B, len(b)))].mean(1))
        S["hse_vs_gga_coordinator"] = {
            "diff": round(float(a.mean() - b.mean()), 3),
            "p_positive": round(float((diffs > 0).mean()), 3)}

    # herding; Q6
    fd = np.array([distinct_share(g) for g in flat.values()])
    od = np.array([distinct_share(g) for g in pooled_orch])
    diffs = (fd[rng.integers(0, len(fd), (B, len(fd)))].mean(1)
             - od[rng.integers(0, len(od), (B, len(od)))].mean(1))
    S["distinct_share"] = {
        "flat": round(float(fd.mean()), 3),
        "coord_pooled": round(float(od.mean()), 3),
        "flat_minus_coord": round(float(fd.mean() - od.mean()), 3),
        "ci95": [round(float(np.percentile(diffs, q)), 3) for q in (2.5, 97.5)]}

    # grading
    rp = S["role_premium"]["mean"]
    G = {}
    G["Q1"] = bool(rp["pooled_ci95"][0] > 0)
    G["Q2"] = bool(sum(v["premium"] > 0 for v in
                       rp["by_coordinator_db"].values()) >= 4)
    G["Q3"] = bool(all(S[k]["p_top2"]["SNUMAT HSE06"] >= 0.9
                       and S[k]["p_last"]["MP GGA"] >= 0.9
                       for k in ("credit_flat", "credit_coord_pooled")))
    G["Q4"] = bool(S["coordinator_effect"]["pooled_ci95"][0] > 0)
    G["Q5"] = bool(S.get("hse_vs_gga_coordinator", {}).get("p_positive", 0)
                   >= 0.9)
    G["Q6"] = bool(S["distinct_share"]["ci95"][1] < 0)
    S["verdicts"] = G
    json.dump(S, open(HERE / "summary_coordinator.json", "w", encoding="utf-8"),
              indent=1)

    # figure
    fig, ax = plt.subplots(1, 3, figsize=(10.5, 3.2))
    labels = ["flat"] + [DBL[d].split()[-1] for d in DB_ORDER]
    cells = [list(flat.values())] + [list(rot[r].values()) for r in range(5)]
    for i, gs in enumerate(cells):
        x = [team_tau(g) for g in gs]
        if x:
            ax[0].errorbar(i, np.mean(x), yerr=np.std(x) / np.sqrt(len(x)),
                           fmt="o", color="k" if i == 0 else "C0")
    ax[0].set_xticks(range(6), labels, rotation=40, fontsize=8)
    ax[0].set_ylabel("team Kendall tau")
    ax[0].set_title("Team score by coordinator database", fontsize=9)
    for i, r in enumerate(range(5)):
        v = prem["mean"].get(r, [])
        if v:
            ci = boot_mean_ci(v)
            ax[1].errorbar(i, np.mean(v), yerr=[[max(0.0, np.mean(v) - ci[0])],
                                                [max(0.0, ci[1] - np.mean(v))]],
                           fmt="o", color="C1")
    ax[1].axhline(0, color="grey", lw=0.8)
    ax[1].set_xticks(range(5), labels[1:], rotation=40, fontsize=8)
    ax[1].set_ylabel("role premium (share)")
    ax[1].set_title("Coordinator role premium, mean rule", fontsize=9)
    w = 0.38
    for j, (k, lab) in enumerate([("credit_flat", "flat"),
                                  ("credit_coord_pooled", "coordinator-led")]):
        vals = [S[k]["mean_share"][DBL[d]] for d in DB_ORDER]
        ax[2].bar(np.arange(5) + (j - 0.5) * w, vals, w, label=lab)
    ax[2].set_xticks(range(5), labels[1:], rotation=40, fontsize=8)
    ax[2].set_ylabel("Shapley share")
    ax[2].set_title("Credit by database", fontsize=9)
    ax[2].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(HERE / "fig_coordinator.png", dpi=200)

    head = "GRADING" if complete else "INTERIM GRADING (incomplete)"
    lines = [f"# Experiment 13: {head}", "",
             f"Campaigns: {n_done} of 120. Numbers: `summary_coordinator.json`.", "",
             "| prediction | verdict |", "| --- | --- |"]
    lines += [f"| {k} | {'pass' if v else 'fail'} |" for k, v in G.items()]
    open(HERE / ("GRADING.md" if complete else "GRADING_INTERIM.md"), "w",
         encoding="utf-8").write("\n".join(lines) + "\n")
    print(json.dumps(S, indent=1))


if __name__ == "__main__":
    main()
