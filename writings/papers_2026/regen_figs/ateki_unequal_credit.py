#!/usr/bin/env python3
"""ATEKi figures: credit that is not shared equally (experiment 19).

TMLR full width (6.5 in), true print size. Data: ateki/results/unequal_credit/{part_a.json, part_b.json}
(ateki/experiments/19_unequal_credit.py).
Main-text figure unequal_credit.pdf:
  (a) one swarm of seven, PBE receiver: credit when joint gains and losses are divided in proportion to
      compute ** alpha (alpha = -1 inverse compute, 0 equal, 1 compute); mean and 90% band over 100 seeds;
      body legend beside the panel;
  (b) PBE receiver: credit under each division rule as a dot plot, colour = body (as in a),
      marker = rule, mean and 90% interval.
Annex figure shared_member_credit.pdf (moved out of the main text):
  a member shared by two swarms (2+2+3 start, moving and shared members): credit when the shared
  member is placed in its own swarm with weight h, minus the equal split h = 1/2, HSE06 receiver.
ASCII only.
"""

import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
SO = HERE.parents[2]
RES = SO / "ateki" / "results" / "unequal_credit"
OUT = HERE.parent / "ateki_tmlr" / "figures"

plt.rcParams.update({"font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7})

pa = json.load(open(RES / "part_a.json", encoding="utf-8"))
pb = json.load(open(RES / "part_b.json", encoding="utf-8"))
BODIES = [("mace_relax", "MACE-MP-0 relaxation", "#2E5FA3"), ("archive_mp", "MP archive", "#009E73"),
          ("gpumd_nep89_md", "NEP89 MD", "#C4452C"), ("gpumd_nep89_relax", "NEP89 relaxation", "#E69F00"),
          ("lammps_meam_md", "MEAM MD", "#8C564B"), ("surrogate", "Active learner", "#CC79A7"),
          ("explorer", "Random scout", "#7F7F7F")]
RULES = [("equal", "equal shares"), ("compute", "by compute"), ("inv_compute", "by 1/compute"),
         ("solo", "by solo gain"), ("seniority", "by seniority"), ("proportional", "team gain by solo gains")]
MK = ["o", "s", "D", "^", "v", "P"]

fig = plt.figure(figsize=(6.5, 3.0))
gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 0.72, 1.0], wspace=0.1)
ax_a = fig.add_subplot(gs[0, 0])
ax_leg = fig.add_subplot(gs[0, 1])
ax_b = fig.add_subplot(gs[0, 2])
ax_leg.axis("off")

x = pa["qe_pbe"]
al = sorted(x["alpha"], key=float)
xs = np.array([float(a) for a in al])
for b, lab, col in BODIES:
    m = np.array([x["alpha"][a][b][0] for a in al])
    lo = np.array([x["alpha"][a][b][1] for a in al])
    hi = np.array([x["alpha"][a][b][2] for a in al])
    ax_a.plot(xs, m, color=col, lw=1.1, label=lab)
    ax_a.fill_between(xs, lo, hi, color=col, alpha=0.25, lw=0)
ax_a.axhline(0, color="#333333", lw=0.5)
ax_a.axvline(0, color="#333333", lw=0.5, ls=":")
ax_a.set_xlabel("Weight exponent $\\alpha$\n(weight = compute$^{\\alpha}$)")
ax_a.set_ylabel("Credit (PBE receiver)")
ax_a.set_title("(a) Weighting by compute, n = 100", loc="left")
ax_a.set_xticks([-1, 0, 1])
ax_a.set_xticklabels(["$-1$\ninverse", "0\nequal", "1\ncompute"])
h, l = ax_a.get_legend_handles_labels()
leg1 = ax_leg.legend(h, l, loc="upper left", frameon=False, fontsize=7, title="Body", title_fontsize=7,
                     handlelength=1.2, borderaxespad=0.0)
leg1._legend_box.align = "left"
ax_leg.add_artist(leg1)
rh = [Line2D([], [], marker=MK[k], ls="none", color="#444444", ms=3.5,
             mfc="none" if r == "proportional" else "#444444", label=rl) for k, (r, rl) in enumerate(RULES)]
leg2 = ax_leg.legend(handles=rh, loc="lower left", bbox_to_anchor=(0.0, -0.12), frameon=False, fontsize=7, title="Division rule (b)",
                     title_fontsize=7, handletextpad=0.3, borderaxespad=0.0)
leg2._legend_box.align = "left"

ys = np.arange(len(BODIES))[::-1]
for k, (r, rl) in enumerate(RULES):
    for i, (b, _, col) in enumerate(BODIES):
        m, lo, hi = x["credit"][r][b]
        yy = ys[i] + (2.5 - k) * 0.13
        ax_b.plot([lo, hi], [yy, yy], color=col, lw=0.8)
        ax_b.plot(m, yy, marker=MK[k], ms=3.2, color=col, mfc="white" if r == "proportional" else col,
                  mew=0.8, ls="none")
ax_b.axvline(0, color="#333333", lw=0.5)
# one row per body, in the legend order and colour; tick labels omitted
# because the shared body legend sits beside the panel
ax_b.set_yticks(ys)
ax_b.set_yticklabels([])
ax_b.tick_params(axis="y", length=0)
ax_b.set_xlabel("Credit (PBE receiver)")
ax_b.set_title("(b) Six division rules, n = 100", loc="left")
ax_b.set_ylim(-0.6, len(BODIES) - 0.4)
ax_b.grid(axis="x", color="#DDDDDD", lw=0.5)
for a in (ax_a, ax_b):
    a.spines[["top", "right"]].set_visible(False)
fig.subplots_adjust(left=0.08, right=0.99, top=0.9, bottom=0.2)
OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "unequal_credit.pdf")
fig.savefig(OUT / "unequal_credit.png", dpi=200)
print("wrote", OUT / "unequal_credit.pdf")

# annex: shared member weight
fig2, ax_c = plt.subplots(figsize=(4.2, 2.4))
y = pb["qe_hse06|split_2_2_3"]
hs = sorted(y["minus_equal_split"], key=float)
hx = np.array([float(hh) for hh in hs])
for b, lab, col in BODIES:
    m = np.array([y["minus_equal_split"][hh][b][0] for hh in hs])
    lo = np.array([y["minus_equal_split"][hh][b][1] for hh in hs])
    hi = np.array([y["minus_equal_split"][hh][b][2] for hh in hs])
    ax_c.plot(hx, m, color=col, lw=1.1, label=lab)
    ax_c.fill_between(hx, lo, hi, color=col, alpha=0.25, lw=0)
ax_c.axhline(0, color="#333333", lw=0.5)
ax_c.set_ylim(-0.03, 0.03)
ax_c.set_xticks([0, 0.5, 1])
ax_c.set_xticklabels(["0\nsecond swarm", "0.5", "1\nown swarm"])
ax_c.set_xlabel("Own-swarm weight $h$ of the shared member")
ax_c.set_ylabel("Credit minus equal split")
ax_c.spines[["top", "right"]].set_visible(False)
ax_c.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False, fontsize=7, handlelength=1.2)
fig2.tight_layout()
fig2.savefig(OUT / "shared_member_credit.pdf")
fig2.savefig(OUT / "shared_member_credit.png", dpi=200)
print("wrote", OUT / "shared_member_credit.pdf")
