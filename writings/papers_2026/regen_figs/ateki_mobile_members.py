#!/usr/bin/env python3
"""ATEKi figure: members that move between swarms or sit in two swarms (experiment 18).

TMLR full width (6.5 in), true print size. Data: ateki/results/mobile_members/{team_values.json, games.json}
(ateki/experiments/18_mobile_members.py); publishing comparison from
ateki/results/morphing_swarms/team_values.json (experiment 17, same campaign seeds).
  (a-c) value minus the fixed grouping with the same start, per start and member rule (learned thresholds),
        one panel per receiver (receiver colour as in the other swarm figures, marker = member
        rule); mean and 90% bootstrap interval over 100 matched campaigns;
  (d)   value of the fixed grouping with results kept within each swarm, with every result published to
        all swarms, and with moving and shared members (learned thresholds), two starts, three receivers;
  (e)   credit with moving and shared members minus the Shapley value, 4 + 3 start, HSE06 and PBE,
        mean and 90% interval over 40 campaigns.
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
RES = SO / "ateki" / "results" / "mobile_members"
R17 = SO / "ateki" / "results" / "morphing_swarms"
OUT = HERE.parent / "ateki_tmlr" / "figures"

plt.rcParams.update({"font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7})

team = json.load(open(RES / "team_values.json", encoding="utf-8"))
games = json.load(open(RES / "games.json", encoding="utf-8"))
t17 = json.load(open(R17 / "team_values.json", encoding="utf-8"))
RECS = [("qe_pbe", "PBE"), ("qe_hse06", "HSE06"), ("gpaw_r2scan", "r$^2$SCAN")]
# one colour per receiver across the swarm figures; marker shape/fill = member rule
RCOL = {"qe_pbe": "#2E5FA3", "qe_hse06": "#C4452C", "gpaw_r2scan": "#009E73"}
STARTS = [("split_1x7", "7 x 1"), ("split_2_2_3", "2+2+3"), ("split_4_3", "4+3"), ("split_2_5w", "2+5")]
RULES = [("move learned", "members move", True, "o"), ("share learned", "members shared", False, "s"),
         ("move+share learned", "both", True, "^")]


def ci(d):
    bs = d[np.random.default_rng(0).choice(len(d), (2000, len(d)))].mean(1)
    return d.mean(), np.percentile(bs, 5), np.percentile(bs, 95)


fig = plt.figure(figsize=(6.5, 4.9))
gs = fig.add_gridspec(2, 6, height_ratios=[1.0, 1.05])
axs = [fig.add_subplot(gs[0, 2 * i:2 * i + 2]) for i in range(3)]
ax_d, ax_e = fig.add_subplot(gs[1, :3]), fig.add_subplot(gs[1, 3:])

for i, (ax, (r, rl)) in enumerate(zip(axs, RECS)):
    col = RCOL[r]
    for k, (rule, lab, filled, mk) in enumerate(RULES):
        m, lo, hi = [], [], []
        for s, _ in STARTS:
            d = np.array(team[r][f"{s}|fixed|{rule}"]["early_recall_area"]) - np.array(team[r][f"{s}|fixed|none"]["early_recall_area"])
            a, b, c = ci(d)
            m.append(a); lo.append(b); hi.append(c)
        m, lo, hi = map(np.array, (m, lo, hi))
        ax.errorbar(np.arange(len(STARTS)) + (k - 1) * 0.2, m, yerr=[m - lo, hi - m], fmt=mk, color=col,
                    mfc=col if filled else "white", ms=3.6, elinewidth=0.9, capsize=0)
    ax.axhline(0, color="#333333", lw=0.6)
    ax.set_xticks(range(len(STARTS)))
    ax.set_xticklabels([s[1] for s in STARTS])
    ax.set_ylim(-0.02, 0.11)
    ax.set_title(f"({'abc'[i]}) {rl} receiver", loc="left")
    if i == 0:
        ax.set_ylabel("Value minus\nfixed grouping")
        for rule, lab, filled, mk in RULES:
            ax.plot([], [], mk, color="#555555", mfc="#555555" if filled else "white", ms=3.6, label=lab)
        ax.legend(frameon=False, loc="upper right", fontsize=7, handletextpad=0.2)
    else:
        ax.set_yticklabels([])
    ax.set_xlabel("Starting grouping")

# (d) keep within swarm / publish everything / moving and shared members
BARS = [("kept within each swarm", "#8C8C8C"), ("every result published", "#56B4E9"),
        ("members move and are shared", "#7A4DD8")]
labels, w = [], 0.26
pos = 0
for r, rl in RECS:
    for s, sl in (("split_1x7", "7 x 1"), ("split_4_3", "4+3")):
        vals = [t17[r][f"{s}|fixed|isolated"]["early_recall_area"], t17[r][f"{s}|fixed|published"]["early_recall_area"],
                team[r][f"{s}|fixed|move+share learned"]["early_recall_area"]]
        for k, (v, (lab, col)) in enumerate(zip(vals, BARS)):
            a = np.array(v)
            m, lo, hi = ci(a)
            ax_d.bar(pos + (k - 1) * w, m, w, color=col, label=lab if pos == 0 else None)
            ax_d.errorbar(pos + (k - 1) * w, m, yerr=[[m - lo], [hi - m]], color="#333333", elinewidth=0.8, capsize=0)
        labels.append(f"{sl}\n{rl}")
        pos += 1
ax_d.set_xticks(range(pos))
ax_d.set_xticklabels(labels, fontsize=7)
ax_d.set_ylim(0.35, 0.80)
ax_d.set_ylabel("Early-window value")
ax_d.set_title("(d) Sharing through members or publishing", loc="left")
ax_d.legend(frameon=False, loc="upper right", fontsize=7, ncol=1)

# (e) credit with moving and shared members
LAB = {"mace_relax": "MACE-MP-0 relax.", "archive_mp": "MP archive", "gpumd_nep89_md": "NEP89 MD",
       "gpumd_nep89_relax": "NEP89 relax.", "lammps_meam_md": "MEAM MD", "surrogate": "Active learner",
       "explorer": "Random scout"}
GK = [("qe_pbe|split_4_3|fixed|move+share", "PBE", "#2E5FA3", "o"),
      ("qe_hse06|split_4_3|fixed|move+share", "HSE06", "#C4452C", "^")]
bodies = games[GK[0][0]]["bodies"]
x = np.arange(len(bodies))
for k, (key, lab, col, mk) in enumerate(GK):
    g = games[key]
    m = np.array([g["tlv_minus_shapley"][a] for a in bodies])
    lo = np.array([g["tlv_minus_shapley_p05"][a] for a in bodies])
    hi = np.array([g["tlv_minus_shapley_p95"][a] for a in bodies])
    ax_e.errorbar(x + (k - 0.5) * 0.24, m, yerr=[m - lo, hi - m], fmt=mk, color=col, ms=3.2, elinewidth=0.9,
                  capsize=0, label=lab)
ax_e.axhline(0, color="#333333", lw=0.6)
ax_e.set_xticks(x)
ax_e.set_xticklabels([LAB[a] for a in bodies], fontsize=7, rotation=40, ha="right",
                     rotation_mode="anchor")
ax_e.set_ylabel("Credit minus\nShapley value")
ax_e.set_title("(e) Credit minus Shapley, 4+3 start, n = 40", loc="left")
ax_e.legend(frameon=False, loc="upper left", fontsize=7, ncol=2)
ax_e.set_ylim(-0.09, 0.11)

fig.tight_layout(h_pad=1.0, w_pad=0.6)
OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "mobile_members.pdf")
fig.savefig(OUT / "mobile_members.png", dpi=300)
print("wrote", OUT / "mobile_members.pdf")
