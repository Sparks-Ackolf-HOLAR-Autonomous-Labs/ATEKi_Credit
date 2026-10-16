#!/usr/bin/env python3
"""Regenerate the ATEKi recorded-meeting figure (LLM agent teams).

Three panels at TMLR full width (6.5 in). Data:
ateki/results/recorded_meetings/campaigns/*.json (team tau, queries,
recorded-conference Myerson values under the sum rule),
max_variant.json (the same under the best-group rule) and
meetings_summary.json (random-tray reference).
  (a) team Kendall tau per campaign, no coordinator vs coordinator-led,
      with the random-tray reference (mean +- sd) as a band;
  (b), (c) share of team tau per agent from the Myerson value on the
      recorded meetings, sum rule vs best-group rule, mean +- sd over
      the five campaigns of each team type.
ASCII only.
"""

import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
SO = HERE.parents[2]
RES = SO / "ateki" / "results" / "recorded_meetings"
OUT = HERE.parent / "ateki_tmlr" / "figures"
AG = ["agent1", "agent2", "agent3", "agent4", "agent5"]
LAB = ["MP\nGGA", "MP\nr$^2$SCAN", "JARVIS\nOptB88vdW", "JARVIS\nTB-mBJ", "SNUMAT\nHSE06"]

plt.rcParams.update({"font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7})

camps = {}
for p in sorted((RES / "campaigns").glob("*.json")):
    camps[p.stem] = json.load(open(p, encoding="utf-8"))
mx = json.load(open(RES / "max_variant.json", encoding="utf-8"))["per_campaign"]
ref = json.load(open(RES / "meetings_summary.json", encoding="utf-8"))["reference"]["random_no_prior"]
summ = json.load(open(RES / "meetings_summary.json", encoding="utf-8"))["arms"]

def grand(g):
    return g["attribution"]["v"][",".join(AG)]

fig, ax = plt.subplots(1, 3, figsize=(6.5, 2.35),
                       gridspec_kw={"width_ratios": [1.0, 1.5, 1.5]})
# (a)
a = ax[0]
a.axhspan(ref["mean"] - ref["sd"], min(1.0, ref["mean"] + ref["sd"]), color="0.88", lw=0)
a.axhline(ref["mean"], color="0.5", lw=0.8)
for i, arm in enumerate(["flat", "orchestrated"]):
    t = summ[arm]["team_tau_all"]
    a.scatter(np.full(len(t), i) + np.linspace(-0.12, 0.12, len(t)), t, s=12,
              color=["#4C72B0", "#C44E52"][i], zorder=3)
    a.plot([i - 0.22, i + 0.22], [np.mean(t)] * 2, color="k", lw=1.2)
a.set_xticks([0, 1]); a.set_xticklabels(["no\ncoordinator", "coordinator-\nled"], fontsize=6.3)
a.set_xlim(-0.6, 1.6); a.set_ylim(0.45, 1.03)
a.set_ylabel("team Kendall $\\tau$")
# label the random-tray band in the empty lower-left corner, clear of the
# band edges and of the campaign points
a.text(-0.55, 0.465, "grey band: random\ntrays, mean $\\pm$ sd", ha="left", va="bottom",
       fontsize=6, color="0.35")
a.set_title("(a) ranking quality")

for k, arm, title in [(1, "flat", "(b) no coordinator"), (2, "orchestrated", "(c) coordinator-led (MP GGA)")]:
    a = ax[k]
    keys = [s for s in camps if s.startswith(arm)]
    s_sum = np.array([[camps[s]["attribution"]["hypergraph_myerson"][g] / abs(grand(camps[s])) for g in AG] for s in keys])
    s_max = np.array([[mx[s][g] for g in AG] for s in keys])
    x = np.arange(len(AG))
    for off, arr, col, lab in [(-0.19, s_sum, "#55A868", "sum of groups"), (0.19, s_max, "#8172B2", "best group")]:
        a.bar(x + off, arr.mean(0), 0.36, yerr=arr.std(0), color=col, label=lab,
              error_kw={"lw": 0.7, "capsize": 1.5})
    a.axhline(0, color="k", lw=0.6)
    a.set_xticks(x); a.set_xticklabels(LAB, fontsize=6, rotation=90)
    a.set_ylim(-1.15, 1.0)
    a.set_title(title)
    if k == 1:
        a.set_ylabel("share of team $\\tau$")
    else:
        a.set_yticklabels([])
        a.legend(loc="lower right", frameon=False)
fig.tight_layout(w_pad=0.6)
OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "recorded_meetings.pdf")
fig.savefig(OUT / "recorded_meetings.png", dpi=200)
print("saved", OUT / "recorded_meetings.pdf")
