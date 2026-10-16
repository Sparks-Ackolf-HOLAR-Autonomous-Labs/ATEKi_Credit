#!/usr/bin/env python3
"""ATEKi figure: several decision bodies of one kind as separate players.

TMLR full width (6.5 in), true print size. Data:
ateki/results/replicated_bodies/replicated_bodies.json
(ateki/experiments/15_replicated_bodies.py).
  (a) team value (early share of the ten most stable compounds found) against
      the number of random scouts in a team with MACE-MP-0 and the active
      learner, per receiver; solid: independent draws, dashed: one repeated draw;
  (b) Shapley value per campaign (PBE receiver, 200 campaigns) of copy 1
      against copy 2: two independent random scouts (team with MACE-MP-0, the
      active learner and a third scout) and two copies of MACE-MP-0 that see
      only their own results (team with the active learner and one scout).
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
RES = SO / "ateki" / "results" / "replicated_bodies" / "replicated_bodies.json"
OUT = HERE.parent / "ateki_tmlr" / "figures"

plt.rcParams.update({"font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7})

d = json.load(open(RES, encoding="utf-8"))["receivers"]
REC = [("qe_pbe", "PBE", "#2E5FA3", "o"), ("qe_hse06", "HSE06", "#C4452C", "s"),
       ("gpaw_r2scan", "r$^2$SCAN", "#009E73", "^")]

fig, axs = plt.subplots(1, 2, figsize=(6.5, 2.9), gridspec_kw={"width_ratios": [1.15, 1.0]})

ax = axs[0]
for r, lab, col, mk in REC:
    R = d[r]
    m = [1, 2, 3, 4]
    ind = [R[f"scouts_indep_{k}"]["v_all"] for k in m]
    clo = [R["scouts_indep_1"]["v_all"]] + [R[f"scouts_clone_{k}"]["v_all"] for k in m[1:]]
    ax.plot(m, ind, "-", color=col, marker=mk, ms=4, label=lab)
    ax.plot(m, clo, "--", color=col, lw=1.0)
ax.plot([], [], "k-", label="independent draws")
ax.plot([], [], "k--", lw=1.0, label="one repeated draw")
ax.set_xticks([1, 2, 3, 4])
ax.set_xlabel("Random scouts in the team")
ax.set_ylabel("Team value (early share found)")
ax.set_title("(a) Team value", loc="left")
ax.legend(frameon=False, ncol=2, loc="upper right")
ax.set_ylim(0.25, 0.6)

ax = axs[1]
pc_s = d["qe_pbe"]["scouts_indep_3"]["per_campaign_shapley"]
pc_m = d["qe_pbe"]["mace_separate"]["per_campaign_shapley"]
ax.plot([-0.25, 0.4], [-0.25, 0.4], color="#8C8C8C", lw=0.6)
ax.scatter(pc_s["explorer#1"], pc_s["explorer#2"], s=6, color="#8C8C8C", alpha=0.6,
           label="random scouts,\nindependent draws")
ax.scatter(pc_m["mace_relax#1"], pc_m["mace_relax#2"], s=6, color="#2E5FA3", alpha=0.6,
           label="MACE-MP-0 copies,\nown results only")
ax.set_xlim(-0.25, 0.4)
ax.set_ylim(-0.25, 0.4)
ax.set_aspect("equal")
ax.set_xlabel("Shapley value, copy 1")
ax.set_ylabel("Shapley value, copy 2")
ax.set_title("(b) Credit of two copies per campaign", loc="left")
ax.legend(frameon=False, loc="upper left", markerscale=2)

fig.tight_layout()
OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "replicated_bodies.pdf")
fig.savefig(OUT / "replicated_bodies.png", dpi=300)
print("wrote", OUT / "replicated_bodies.pdf")
