"""Summarise ATEKi experiment 11 (recorded meetings) at larger scale.
Sets S1 (Qwen3-4B, 5 agents), S2 (Nemotron 30B-A3B, 5 agents),
S3 (Qwen3-4B, 10 agents). Grades the predictions in PREDICTION.md.
Reads campaigns from <set>/campaigns/*.json. ASCII only."""
import importlib.util
import json
import os
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

spec = importlib.util.spec_from_file_location(
    "exp26", str(ATEKI.parent / "tenki" / "TENKi" / "experiments"
                 / "26_paired_campaign.py"))
exp26 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exp26)
UNIVERSE = os.environ.get(
    "BANDGAP_UNIVERSE",
    str(ATEKI.parent / "shared" / "output" / "bandgap_archive_build"
        / "bandgap_universe.jsonl"))
DBL = {"mp_gga": "MP GGA", "mp_r2scan": "MP r2SCAN",
       "jarvis_optb88vdw": "JARVIS OptB88vdW", "jarvis_mbj": "JARVIS TB-mBJ",
       "snumat_hse": "SNUMAT HSE06"}
SETS = {"S1": "Qwen3-4B, 5 agents", "S2": "Nemotron 30B-A3B, 5 agents",
        "S3": "Qwen3-4B, 10 agents"}
rng = np.random.default_rng(0)


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


def max_rule_shares(g):
    P = sorted(g["agents"], key=lambda a: int(a[5:]))
    V = {frozenset(k.split(",")) if k != "-" else frozenset(): v
         for k, v in g["attribution"]["v"].items()}
    H = g["attribution"]["hyperedges"]
    sc = ShapleyEngine(P, lambda S: max(
        [V[c] for c in comps(set(S), H)], default=0.0)).exact().scores
    tot = abs(V[frozenset(P)]) or 1e-9
    return {a: sc[a] / tot for a in P}


def boot_diff(a, b, n=5000):
    a, b = np.asarray(a), np.asarray(b)
    d = [rng.choice(b, len(b)).mean() - rng.choice(a, len(a)).mean()
         for _ in range(n)]
    return [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))]


pc = exp26.load_universe(Path(UNIVERSE), 30)
cl = pc["expt_zhuo"]
out = {"sets": {}}
for s, label in SETS.items():
    files = sorted((HERE / s / "campaigns").glob("*.json"))
    files = [f for f in files if not f.name.endswith(".raw.json")]
    logs = [json.load(open(f, encoding="utf-8")) for f in files]
    if not logs:
        continue
    R = {}
    for arm in ["flat", "orchestrated"]:
        L = [g for g in logs if g["arm"] == arm]
        if not L:
            continue
        P = sorted(L[0]["agents"], key=lambda a: int(a[5:]))
        full = ",".join(sorted(P))
        team = [g["attribution"]["v"][full] for g in L]
        distinct = [len({tuple(sorted(q["query"])) for q in g["queries"]})
                    / len(g["queries"]) for g in L]
        db_share = {}
        for d in DBL:
            db_share[DBL[d]] = float(np.mean([sum(
                g["attribution"]["shapley"][a] for a in P
                if g["agents"][a] == d) / max(1e-9, abs(
                    g["attribution"]["v"][full])) for g in L]))
        top2 = [sorted(db_share, key=db_share.get, reverse=True)[:2]]
        r = {"n": len(L), "team_tau": team,
             "team_tau_mean": float(np.mean(team)),
             "team_tau_sd": float(np.std(team)),
             "distinct_share_mean": float(np.mean(distinct)),
             "messages_mean": float(np.mean([len(g["messages"])
                                             for g in L])),
             "fallback_rate": float(np.mean([g["fallbacks"]
                                             / g["llm_calls"] for g in L])),
             "shapley_share_by_database": db_share, "top2_databases": top2[0]}
        cites = np.asarray([[g["roles"][a]["cited_by_others"] for a in P]
                            for g in L]).mean(0)
        r["cited_by_others_mean"] = dict(zip(P, cites.tolist()))
        r["max_cited_over_median"] = float(cites.max()
                                           / max(1e-9, np.median(cites)))
        if arm == "orchestrated":
            r["coordinator_share_sum_rule"] = float(np.mean([
                g["attribution"]["hypergraph_myerson"]["agent1"]
                / max(1e-9, abs(g["attribution"]["v"][full])) for g in L]))
            r["coordinator_share_best_group_rule"] = float(np.mean([
                max_rule_shares(g)["agent1"] for g in L]))
        R[arm] = r
    budget = logs[0]["rounds"] * len(logs[0]["agents"]) * 4
    ref = []
    for k in range(20):
        t, _ = exp26.run_campaign(cl, "cold", None, 8.0, 4, budget,
                                  [budget], 42 + 1000 * k)
        ref.append(t[-1])
    R["random_trays_same_budget"] = {"mean": float(np.mean(ref)),
                                     "sd": float(np.std(ref)),
                                     "evaluations": budget}
    if "flat" in R and "orchestrated" in R:
        R["coord_minus_flat"] = {
            "mean": R["orchestrated"]["team_tau_mean"]
            - R["flat"]["team_tau_mean"],
            "ci95": boot_diff(R["flat"]["team_tau"],
                              R["orchestrated"]["team_tau"])}
    out["sets"][s] = {"label": label, **R}

# grading
G = {}
S_ = out["sets"]
if "S1" in S_ and "coord_minus_flat" in S_["S1"]:
    G["P1"] = (S_["S1"]["coord_minus_flat"]["ci95"][0] > 0
               and S_["S1"]["flat"]["distinct_share_mean"] < 0.20)
if "S2" in S_ and "orchestrated" in S_["S2"]:
    G["P2"] = (S_["S2"]["flat"]["distinct_share_mean"] < 0.30
               and S_["S2"]["coord_minus_flat"]["mean"] >= 0)
if "S3" in S_ and "orchestrated" in S_.get("S3", {}) and "S1" in S_:
    G["P3"] = (S_["S3"]["flat"]["distinct_share_mean"]
               <= S_["S1"]["flat"]["distinct_share_mean"]
               and S_["S3"]["coord_minus_flat"]["mean"] >= 0)
G["P4"] = all(set(S_[s][a]["top2_databases"])
              == {"MP r2SCAN", "SNUMAT HSE06"}
              for s in S_ for a in ("flat", "orchestrated") if a in S_[s])
G["P5"] = all(S_[s]["orchestrated"]["coordinator_share_sum_rule"] < 0
              < S_[s]["orchestrated"]["coordinator_share_best_group_rule"]
              for s in S_ if "orchestrated" in S_[s])
if "S3" in S_ and "flat" in S_["S3"]:
    G["P6"] = S_["S3"]["flat"]["max_cited_over_median"] <= 2.0
out["predictions_pass"] = G
json.dump(out, open(HERE / "scale_summary.json", "w", encoding="utf-8"),
          indent=1)

# figure: team tau per campaign, by set and team type, with random band
fig, ax = plt.subplots(figsize=(5.2, 2.8))
x = 0
ticks, labels = [], []
for s in S_:
    rr = S_[s]["random_trays_same_budget"]
    ax.fill_between([x - 0.4, x + 1.4], rr["mean"] - rr["sd"],
                    rr["mean"] + rr["sd"], color="0.85", lw=0)
    ax.plot([x - 0.4, x + 1.4], [rr["mean"]] * 2, color="0.5", lw=0.8)
    for j, (arm, c) in enumerate([("flat", "#DD8452"),
                                  ("orchestrated", "#4C72B0")]):
        if arm not in S_[s]:
            continue
        t = S_[s][arm]["team_tau"]
        ax.scatter(np.full(len(t), x + j) + rng.uniform(-0.12, 0.12, len(t)),
                   t, s=8, color=c, alpha=0.7)
        ax.errorbar(x + j + 0.22, np.mean(t), yerr=np.std(t), fmt="o",
                    color=c, ms=4, capsize=2, lw=0.8)
        ticks.append(x + j)
        labels.append(("no coord." if arm == "flat" else "coord.")
                      + "\n" + s)
    x += 2.6
ax.set_xticks(ticks)
ax.set_xticklabels(labels, fontsize=7)
ax.set_ylabel("team Kendall tau", fontsize=8)
ax.tick_params(labelsize=7)
fig.tight_layout()
fig.savefig(HERE / "fig_scale.png", dpi=200)
print(json.dumps({s: {a: {k: v for k, v in S_[s][a].items()
                          if k in ("n", "team_tau_mean", "distinct_share_mean",
                                   "coordinator_share_sum_rule",
                                   "coordinator_share_best_group_rule",
                                   "top2_databases", "mean", "ci95")}
                      for a in S_[s] if isinstance(S_[s][a], dict)}
                  for s in S_}, indent=1))
print(G)
