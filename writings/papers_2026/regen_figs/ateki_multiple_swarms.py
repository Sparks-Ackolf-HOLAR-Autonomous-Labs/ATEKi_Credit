#!/usr/bin/env python3
"""ATEKi figure: several swarms in one campaign, of the same or different sizes.

TMLR full width (6.5 in), true print size. Data:
ateki/results/multiple_swarms/{team_values.json, games.json}
(ateki/experiments/16_multiple_swarms.py). Every swarm uses the emergent
organisation of experiment 14 inside itself; all swarms share one batch of 4.
  (a) the same seven bodies grouped into several swarms (PBE receiver, results
      published between swarms): team value minus the one-swarm value, per
      slot rule, mean and 90% bootstrap interval over 100 matched campaigns;
  (b) extra swarms that copy the team (14 or 21 bodies, or 7 + 3), isolated or
      published, per receiver: value minus the one-swarm value;
  (c) credit moved by swarm membership: Owen value minus Shapley value,
      summed over the members of each swarm, against the swarm size, for the
      five two- and three-swarm groupings (PBE and HSE06 receivers, equal slot
      split, published results), mean and 90% interval over 100 campaigns.
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
RES = SO / "ateki" / "results" / "multiple_swarms"
OUT = HERE.parent / "ateki_tmlr" / "figures"

plt.rcParams.update({"font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7})

team = json.load(open(RES / "team_values.json", encoding="utf-8"))
games = json.load(open(RES / "games.json", encoding="utf-8"))


def diff(r, a, b="one_7|emergent|equal|published"):
    d = np.array(team[r][a]["early_recall_area"]) - np.array(team[r][b]["early_recall_area"])
    rng = np.random.default_rng(0)
    bs = [rng.choice(d, len(d)).mean() for _ in range(2000)]
    return d.mean(), np.percentile(bs, 5), np.percentile(bs, 95)


fig = plt.figure(figsize=(6.5, 4.9))
gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.05])
axs = [fig.add_subplot(gs[0, :]), fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1])]

# (a) grouping the same seven bodies
ax = axs[0]
GROUPS = [("split_1_6", "1 + 6\n(MACE-MP-0 alone)"), ("split_2_5s", "2 + 5\n(strong pair)"),
          ("split_2_5w", "2 + 5\n(weak pair)"), ("split_4_3", "4 + 3"),
          ("split_2_2_3", "2 + 2 + 3"), ("split_1x7", "7 swarms of 1")]
RULES = [("equal", "equal share per swarm", "#8C8C8C", "o"), ("size", "share by size", "#2E5FA3", "s"),
         ("record", "share by record", "#C4452C", "^")]
x = np.arange(len(GROUPS))
for k, (rule, lab, col, mk) in enumerate(RULES):
    m, lo, hi = zip(*[diff("qe_pbe", f"{g}|emergent|{rule}|published") for g, _ in GROUPS])
    xx = x + (k - 1) * 0.22
    ax.errorbar(xx, m, yerr=[np.array(m) - lo, np.array(hi) - m], fmt=mk, color=col, ms=3.5,
                elinewidth=0.9, capsize=0, label=lab)
ax.axhline(0, color="#333333", lw=0.6)
ax.set_xticks(x)
ax.set_xticklabels([g[1] for g in GROUPS], fontsize=7)
ax.set_ylabel("Value minus\none seven-body swarm")
ax.set_title("(a) The same seven bodies grouped into several swarms (PBE receiver)", loc="left")
ax.legend(frameon=False, loc="lower left", ncol=3)

# (b) copies of the team
ax = axs[1]
DUPS = [("dup_7_7", "7 + 7"), ("dup_7_7_7", "7 + 7 + 7"), ("dup_7_3", "7 + 3")]
REC = [("qe_pbe", "PBE", "#2E5FA3"), ("qe_hse06", "HSE06", "#C4452C"), ("gpaw_r2scan", "r$^2$SCAN", "#009E73")]
x = np.arange(len(DUPS))
for k, (r, lab, col) in enumerate(REC):
    for share, mk, fill in (("isolated", "o", col), ("published", "o", "white")):
        m, lo, hi = zip(*[diff(r, f"{g}|emergent|equal|{share}") for g, _ in DUPS])
        xx = x + (k - 1) * 0.24 + (-0.05 if share == "isolated" else 0.05)
        ax.errorbar(xx, m, yerr=[np.array(m) - lo, np.array(hi) - m], fmt=mk, color=col, mfc=fill,
                    ms=3.5, elinewidth=0.9, capsize=0, label=lab if share == "isolated" else None)
ax.plot([], [], "o", color="#333333", ms=3.5, label="kept within swarm")
ax.plot([], [], "o", color="#333333", mfc="white", ms=3.5, label="published")
ax.axhline(0, color="#333333", lw=0.6)
ax.set_xticks(x)
ax.set_xticklabels([g[1] for g in DUPS])
ax.set_ylabel("Value minus\none seven-body swarm")
ax.set_title("(b) Copies of the team, same budget", loc="left")
ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.22), fontsize=7, ncol=5, columnspacing=0.8, handletextpad=0.2)

# (c) credit moved between swarms by the Owen value, against swarm size
ax = axs[2]
PARTS = ["split_1_6", "split_2_5s", "split_2_5w", "split_4_3", "split_2_2_3"]
rng = np.random.default_rng(1)
for k, (r, lab, col) in enumerate(REC[:2]):
    first = True
    for p in PARTS:
        g = games[f"{r}|{p}|emergent|equal|published|body"]
        for u, arr in zip(g["unions"], g["union_owen_minus_shapley_all"]):
            a = np.array(arr)
            bs = [rng.choice(a, len(a)).mean() for _ in range(1000)]
            xx = len(u) + (k - 0.5) * 0.18 + rng.uniform(-0.05, 0.05)
            ax.errorbar(xx, a.mean(), yerr=[[a.mean() - np.percentile(bs, 5)], [np.percentile(bs, 95) - a.mean()]],
                        fmt="o", color=col, ms=3.2, elinewidth=0.9, capsize=0, label=lab if first else None)
            first = False
ax.axhline(0, color="#333333", lw=0.6)
ax.set_xticks(range(1, 7))
ax.set_xlabel("Swarm size (bodies)")
ax.set_ylabel("Owen minus Shapley,\nsummed over the swarm")
ax.set_title("(c) Credit moved by membership", loc="left")
ax.legend(frameon=False, loc="upper right")

fig.tight_layout(h_pad=1.2)
OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "multiple_swarms.pdf")
fig.savefig(OUT / "multiple_swarms.png", dpi=300)
print("wrote", OUT / "multiple_swarms.pdf")
