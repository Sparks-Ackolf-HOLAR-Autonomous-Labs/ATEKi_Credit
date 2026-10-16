#!/usr/bin/env python3
"""ATEKi figure: the number of swarms changes during the campaign (combine, nest, separate).

TMLR full width (6.5 in), true print size. Data:
ateki/results/morphing_swarms/{team_values.json, games.json}
(ateki/experiments/17_morphing_swarms.py). Results kept within each group
(isolated); the batch is divided between groups by record.
  (a) number of independent groups against receiver compute (PBE), mean and
      5-95 percentile band over 100 campaigns (thin dotted outlines), for
      three cases;
  (b) value minus the fixed structure with the same start, per start and rule
      set, PBE, mean and 90% bootstrap interval over 100 matched campaigns;
  (c) credit moved by membership for the 2 + 2 + 3 start (PBE): Owen value of
      the fixed partition minus Shapley, and the time-averaged level structure
      value of the changing structure minus Shapley, mean and 90% interval
      over 40 campaigns.
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
RES = SO / "ateki" / "results" / "morphing_swarms"
OUT = HERE.parent / "ateki_tmlr" / "figures"

plt.rcParams.update({"font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7})

team = json.load(open(RES / "team_values.json", encoding="utf-8"))
games = json.load(open(RES / "games.json", encoding="utf-8"))
R = "qe_pbe"


def diff(r, a, b):
    d = np.array(team[r][a]["early_recall_area"]) - np.array(team[r][b]["early_recall_area"])
    rng = np.random.default_rng(0)
    bs = rng.choice(d, (2000, len(d))).mean(1)
    return d.mean(), np.percentile(bs, 5), np.percentile(bs, 95)


fig = plt.figure(figsize=(6.5, 4.6))
gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.0], width_ratios=[1.0, 1.15])
ax_a, ax_b, ax_c = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[1, :])

# (a) number of independent groups over the campaign
CASES = [("split_1x7|merge_only|isolated", "7 singles, combine only", "#2E5FA3", "-"),
         ("split_1x7|full_learned|isolated", "7 singles, learned rules", "#C4452C", "-"),
         ("one_7|full_learned|isolated", "one swarm of 7, learned rules", "#009E73", "--")]
for key, lab, col, ls in CASES:
    e = team[R][key]
    x = np.array(e["grid"])
    m = np.array(e["n_groups"]["mean"])
    # 5-95 percentile band drawn as thin outlines so the three bands stay legible
    for q in ("p05", "p95"):
        ax_a.step(x, e["n_groups"][q], where="post", color=col, ls=":", lw=0.6, alpha=0.8)
    ax_a.step(x, m, where="post", color=col, ls=ls, lw=1.2, label=lab)
ax_a.plot([], [], color="#555555", ls=":", lw=0.6, label="5-95% of campaigns")
ax_a.axvline(0.25, color="#999999", lw=0.6, ls=":")
ax_a.set_xlim(0, 0.6)
ax_a.set_ylim(0.5, 11.2)
ax_a.set_yticks(range(1, 8))
ax_a.set_xlabel("Fraction of receiver compute spent")
ax_a.set_ylabel("Independent groups")
ax_a.set_title("(a) Groups during the campaign, n = 100", loc="left")
ax_a.legend(frameon=False, loc="upper right", ncol=1, fontsize=7,
            handlelength=1.6, borderaxespad=0.2, labelspacing=0.25)

# (b) value against the fixed structure with the same start
STARTS = [("split_1x7", "7 x 1"), ("split_2_2_3", "2+2+3"), ("split_4_3", "4+3"), ("split_2_5w", "2+5"),
          ("one_7", "7")]
RULES = [("merge_only", "combine only", "#2E5FA3", "o"), ("split_only", "separate only", "#8C8C8C", "s"),
         ("full", "both, default thresholds", "#E69F00", "D"), ("full_learned", "both, learned thresholds", "#C4452C", "^")]
x = np.arange(len(STARTS))
for k, (rule, lab, col, mk) in enumerate(RULES):
    pts = [(i, diff(R, f"{s}|{rule}|isolated", f"{s}|fixed|isolated")) for i, (s, _) in enumerate(STARTS)
           if f"{s}|{rule}|isolated" in team[R] and not (s == "split_1x7" and rule == "split_only")]
    xx = np.array([i for i, _ in pts]) + (k - 1.5) * 0.17
    m = np.array([p[1][0] for p in pts])
    lo = np.array([p[1][1] for p in pts])
    hi = np.array([p[1][2] for p in pts])
    ax_b.errorbar(xx, m, yerr=[m - lo, hi - m], fmt=mk, color=col, ms=3.2, elinewidth=0.9, capsize=0, label=lab)
ax_b.axhline(0, color="#333333", lw=0.6)
ax_b.set_xticks(x)
ax_b.set_xticklabels([s[1] for s in STARTS])
ax_b.set_xlabel("Starting structure")
ax_b.set_ylabel("Value minus fixed structure")
ax_b.set_title("(b) Changing minus fixed, n = 100", loc="left")
ax_b.legend(frameon=False, loc="upper right", fontsize=7, ncol=1, handletextpad=0.2)
ax_b.set_ylim(-0.052, 0.072)

# (c) credit moved by membership, 2 + 2 + 3 start
LAB = {"mace_relax": "MACE-MP-0\nrelaxation", "archive_mp": "MP archive", "gpumd_nep89_md": "NEP89 MD",
       "gpumd_nep89_relax": "NEP89\nrelaxation", "lammps_meam_md": "MEAM MD", "surrogate": "Active\nlearner",
       "explorer": "Random\nscout"}
GK = [(f"{R}|split_2_2_3|fixed|default", "fixed groups: Owen value", "#8C8C8C", "s"),
      (f"{R}|split_2_2_3|merge_only|default", "combine only: averaged level value", "#2E5FA3", "o"),
      (f"{R}|split_2_2_3|full|learned", "learned rules: averaged level value", "#C4452C", "^")]
bodies = games[GK[0][0]]["bodies"]
x = np.arange(len(bodies))
for k, (key, lab, col, mk) in enumerate(GK):
    g = games[key]
    m = np.array([g["tlv_minus_shapley"][a] for a in bodies])
    lo = np.array([g["tlv_minus_shapley_p05"][a] for a in bodies])
    hi = np.array([g["tlv_minus_shapley_p95"][a] for a in bodies])
    ax_c.errorbar(x + (k - 1) * 0.2, m, yerr=[m - lo, hi - m], fmt=mk, color=col, ms=3.2, elinewidth=0.9,
                  capsize=0, label=lab)
ax_c.axhline(0, color="#333333", lw=0.6)
ax_c.set_xticks(x)
ax_c.set_xticklabels([LAB[a] for a in bodies], fontsize=7)
ax_c.set_ylabel("Credit minus\nShapley value")
ax_c.set_title("(c) Credit moved by group membership, 2+2+3 start, n = 40 campaigns", loc="left")
ax_c.set_ylim(-0.05, 0.08)
ax_c.legend(frameon=False, loc="upper center", fontsize=7, ncol=3, columnspacing=0.8, handletextpad=0.3)

fig.tight_layout(h_pad=1.0)
OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "morphing_swarms.pdf")
fig.savefig(OUT / "morphing_swarms.png", dpi=300)
print("wrote", OUT / "morphing_swarms.pdf")
