#!/usr/bin/env python3
"""ATEKi figure: credit that is not shared equally (experiment 19).

TMLR full width (6.5 in), true print size. Data: ateki/results/unequal_credit/{part_a.json, part_b.json}
(ateki/experiments/19_unequal_credit.py).
  (a) one swarm of seven, PBE receiver: credit when joint gains and losses are divided in proportion to
      compute ** alpha (alpha = -1 inverse compute, 0 equal, 1 compute); mean and 90% band over 100 seeds;
  (b) PBE receiver: credit under each division rule, mean and 90% interval;
  (c) a member shared by two swarms (2+2+3 start, moving and shared members): credit when the shared
      member is placed in its own swarm with weight h, minus the equal split h = 1/2, HSE06 receiver.
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
RULES = [("equal", "equal"), ("compute", "by compute"), ("inv_compute", "by 1/compute"),
         ("solo", "by solo gain"), ("seniority", "by seniority"), ("proportional", "proportional")]

fig = plt.figure(figsize=(6.5, 2.75))
gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 0.95, 0.85], wspace=0.95)
ax_a, ax_b, ax_c = (fig.add_subplot(gs[0, i]) for i in range(3))

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
ax_a.set_title("(a) Weighting by compute", loc="left")
ax_a.set_xticks([-1, 0, 1])
ax_a.set_xticklabels(["$-1$\ninverse", "0\nequal", "1\ncompute"])

ys = np.arange(len(BODIES))[::-1]
mk = ["o", "s", "D", "^", "v", "x"]
for k, (r, rl) in enumerate(RULES):
    m = np.array([x["credit"][r][b][0] for b, _, _ in BODIES])
    lo = np.array([x["credit"][r][b][1] for b, _, _ in BODIES])
    hi = np.array([x["credit"][r][b][2] for b, _, _ in BODIES])
    col = ["#111111", "#555555", "#555555", "#555555", "#555555", "#555555"][k]
    ax_b.errorbar(m, ys + (k - 2.5) * 0.12, xerr=[m - lo, hi - m], fmt=mk[k], ms=3.0, color=col,
                  elinewidth=0.8, capsize=0, label=rl, mfc="none" if r == "proportional" else col)
ax_b.axvline(0, color="#333333", lw=0.5)
ax_b.set_yticks(ys)
ax_b.set_yticklabels([lab for _, lab, _ in BODIES], fontsize=6.5)
ax_b.set_xlabel("Credit (PBE receiver)")
ax_b.set_title("(b) Division rules", loc="left")
ax_b.set_ylim(-0.6, len(BODIES) - 0.4)
# rule legend below the axes so it does not cover the credit intervals
ax_b.legend(frameon=False, fontsize=6, loc="upper center", bbox_to_anchor=(0.3, -0.25), ncol=3,
            handletextpad=0.1, borderaxespad=0.1, columnspacing=0.6)

y = pb["qe_hse06|split_2_2_3"]
hs = sorted(y["minus_equal_split"], key=float)
hx = np.array([float(h) for h in hs])
for b, lab, col in BODIES:
    m = np.array([y["minus_equal_split"][h][b][0] for h in hs])
    lo = np.array([y["minus_equal_split"][h][b][1] for h in hs])
    hi = np.array([y["minus_equal_split"][h][b][2] for h in hs])
    ax_c.plot(hx, m, color=col, lw=1.1)
    ax_c.fill_between(hx, lo, hi, color=col, alpha=0.25, lw=0)
ax_c.axhline(0, color="#333333", lw=0.5)
ax_c.set_ylim(-0.03, 0.03)
ax_c.set_xticks([0, 0.5, 1])
ax_c.set_xticklabels(["0\nsecond", "0.5", "1\nown"])
ax_c.set_xlabel("Own-swarm weight $h$")
ax_c.set_ylabel("Credit minus equal split")
ax_c.set_title("(c) Shared member", loc="left")

h, l = ax_a.get_legend_handles_labels()
fig.legend(h, l, ncol=7, frameon=False, loc="lower center", bbox_to_anchor=(0.5, -0.02), fontsize=6,
           handlelength=1.0, columnspacing=0.6, handletextpad=0.3)
fig.subplots_adjust(left=0.075, right=0.985, top=0.9, bottom=0.42)
OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "unequal_credit.pdf")
fig.savefig(OUT / "unequal_credit.png", dpi=200)
print("wrote", OUT / "unequal_credit.pdf")
