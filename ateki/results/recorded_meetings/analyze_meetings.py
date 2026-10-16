"""Summarise ATEKi exp 11 (recorded meetings). ASCII only.

Per arm (flat, orchestrated): team ranking quality, attribution under the
four structures, how much the recorded structure moves credit relative to
plain Shapley, coordinator share, recorded conference statistics, and role
measures. Reference campaigns with the same budget and no LLM decisions:
random 4-family queries with no prior, and random queries with the
learned-trust prior pooled over the same five databases.
"""
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
spec = importlib.util.spec_from_file_location(
    "exp26", str(ATEKI.parent / "tenki" / "TENKi" / "experiments"
                 / "26_paired_campaign.py"))
exp26 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exp26)

UNIVERSE = os.environ.get(
    "BANDGAP_UNIVERSE",
    str(ATEKI.parent / "shared" / "output" / "bandgap_archive_build"
        / "bandgap_universe.jsonl"))
AGENTS = ["agent1", "agent2", "agent3", "agent4", "agent5"]
METHODS = ["shapley", "myerson_clique", "hypergraph_myerson",
           "declared_myerson"]
MLABEL = {"shapley": "Shapley (no structure)",
          "myerson_clique": "Myerson, recorded pairs",
          "hypergraph_myerson": "Myerson, recorded conferences",
          "declared_myerson": "Myerson, declared structure"}

logs = [json.load(open(p, encoding="utf-8"))
        for p in sorted((HERE / "campaigns").glob("*.json"))]


def kendall(a, b):
    from itertools import combinations
    s = 0
    n = 0
    for i, j in combinations(range(len(a)), 2):
        s += np.sign(a[i] - a[j]) * np.sign(b[i] - b[j])
        n += 1
    return s / n if n else 0.0


out = {"arms": {}}
for arm in ["flat", "orchestrated"]:
    L = [g for g in logs if g["arm"] == arm]
    if not L:
        continue
    team = [g["attribution"]["v"][",".join(AGENTS)] for g in L]
    shares = {m: np.asarray([[g["attribution"][m][a]
                              / max(1e-9, abs(g["attribution"]["v"][
                                  ",".join(AGENTS)])) for a in AGENTS]
                             for g in L]) for m in METHODS}
    move = {m: float(np.mean([np.abs(np.asarray(
        [g["attribution"][m][a] for a in AGENTS])
        - np.asarray([g["attribution"]["shapley"][a] for a in AGENTS])).sum()
        for g in L])) for m in METHODS[1:]}
    rankcorr = {m: float(np.mean([kendall(
        [g["attribution"][m][a] for a in AGENTS],
        [g["attribution"]["shapley"][a] for a in AGENTS]) for g in L]))
        for m in METHODS[1:]}
    nconf = [len(g["attribution"]["hyperedges"]) for g in L]
    sizes = [len(e) for g in L for e in g["attribution"]["hyperedges"]]
    roles = {a: {k: float(np.mean([g["roles"][a][k] for g in L]))
                 for k in ["queries", "msgs_sent", "msgs_received",
                           "cited_by_others"]} for a in AGENTS}
    for a in AGENTS:
        roles[a]["notes"] = {t: float(np.mean([g["roles"][a]["notes"][t]
                                               for g in L]))
                             for t in L[0]["roles"][a]["notes"]}
    distinct = float(np.mean([len({tuple(sorted(q["query"]))
                                   for q in g["queries"]})
                              / len(g["queries"]) for g in L]))
    out["arms"][arm] = {
        "n_campaigns": len(L), "team_tau_mean": float(np.mean(team)),
        "team_tau_all": team,
        "share_mean": {m: dict(zip(AGENTS, shares[m].mean(0).tolist()))
                       for m in METHODS},
        "share_sd": {m: dict(zip(AGENTS, shares[m].std(0).tolist()))
                     for m in METHODS},
        "credit_moved_vs_shapley_L1": move,
        "rank_corr_vs_shapley": rankcorr,
        "conferences_per_campaign": float(np.mean(nconf)),
        "conference_size_counts": {str(s): sizes.count(s)
                                   for s in sorted(set(sizes))},
        "roles": roles, "distinct_query_share": distinct,
        "fallback_rate": float(np.mean([g["fallbacks"] / g["llm_calls"]
                                        for g in L])),
    }

# reference campaigns without LLM decisions (same budget, 20 seeds)
pc = exp26.load_universe(Path(UNIVERSE), 30)
cl = pc["expt_zhuo"]
donors = ["mp_gga", "mp_r2scan", "jarvis_optb88vdw", "jarvis_mbj",
          "snumat_hse"]
pri = {c: float(np.mean([exp26.donor_prior(cl, pc[d], "even")[c]
                         for d in donors])) for c in cl}
rounds = logs[0]["rounds"] if logs else 12
budget = rounds * 5 * 4
cps = [budget]
ref = {"random_no_prior": [], "random_pooled_prior": []}
for s in range(20):
    t, _ = exp26.run_campaign(cl, "cold", None, 8.0, 4, budget, cps,
                              42 + 1000 * s)
    ref["random_no_prior"].append(t[-1])
    t, _ = exp26.run_campaign(cl, "adaptive", pri, 8.0, 4, budget, cps,
                              42 + 1000 * s)
    ref["random_pooled_prior"].append(t[-1])
out["reference"] = {k: {"mean": float(np.mean(v)), "sd": float(np.std(v))}
                    for k, v in ref.items()}
out["budget_evaluations"] = budget
json.dump(out, open(HERE / "meetings_summary.json", "w", encoding="utf-8"),
          indent=1)

# figure: mean credit share per agent, by structure, both arms
arms = [a for a in ["flat", "orchestrated"] if a in out["arms"]]
fig, axes = plt.subplots(1, len(arms), figsize=(7.0, 2.8), sharey=True)
axes = np.atleast_1d(axes)
cols = ["#4C72B0", "#DD8452", "#55A868", "#8172B3"]
db = {"agent1": "MP\nGGA", "agent2": "MP\nr2SCAN", "agent3": "JARVIS\nOptB88",
      "agent4": "JARVIS\nmBJ", "agent5": "SNUMAT\nHSE"}
for ax, arm in zip(axes, arms):
    A = out["arms"][arm]
    x = np.arange(len(AGENTS))
    for j, m in enumerate(METHODS):
        mu = [A["share_mean"][m][a] for a in AGENTS]
        sd = [A["share_sd"][m][a] for a in AGENTS]
        ax.bar(x + (j - 1.5) * 0.2, mu, 0.2, yerr=sd, color=cols[j],
               label=MLABEL[m], error_kw={"lw": 0.6, "capsize": 1.5})
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels([("coord. " if arm == "orchestrated" and a ==
                         "agent1" else "") + db[a] for a in AGENTS],
                       fontsize=6.5)
    ax.set_title("no coordinator" if arm == "flat" else
                 "coordinator-led (MP GGA agent)", fontsize=8)
axes[0].set_ylabel("share of team tau")
axes[-1].legend(frameon=False, fontsize=6)
fig.tight_layout()
fig.savefig(HERE / "fig_meetings.png", dpi=200)
print(json.dumps({k: {kk: vv for kk, vv in v.items()
                      if kk in ("team_tau_mean", "credit_moved_vs_shapley_L1",
                                "rank_corr_vs_shapley",
                                "conferences_per_campaign",
                                "distinct_query_share")}
                  for k, v in out["arms"].items()}, indent=1))
print(out["reference"])
