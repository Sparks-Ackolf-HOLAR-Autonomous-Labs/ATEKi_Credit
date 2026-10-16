#!/usr/bin/env python3
"""ATEKi figure: emergent hierarchical swarm versus pre-defined team structures.

TMLR full width (6.5 in), true print size. Data:
ateki/results/emergent_swarm/{team_values.json, shapley.json}
(ateki/experiments/14_emergent_swarm.py).
  (a) team value (early share of the ten most stable compounds found) per
      structure and receiver: mean over 100 campaigns with the 90% bootstrap
      interval of the mean; dashed: MACE-MP-0 alone (PBE, HSE06);
  (b) share of the ten found against the fraction of HSE06 compute
      (held-out receiver), mean and 5-95% band over campaigns;
  (c) structural credit, Shapley value under the emergent structures (three
      tiers; changing shape) minus Shapley value in the flat team, per body;
  (d) shape of the changing-shape team over the HSE06 campaign: number of
      tiers and members in the top tier, mean and 5-95% band over campaigns
      (learned protocol: mean only).
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
RES = SO / "ateki" / "results" / "emergent_swarm"
OUT = HERE.parent / "ateki_tmlr" / "figures"

plt.rcParams.update({"font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7})

team = json.load(open(RES / "team_values.json", encoding="utf-8"))["receivers"]
shap = json.load(open(RES / "shapley.json", encoding="utf-8"))

ST = ["solo", "flat", "star", "tiers_fixed", "emergent", "emergent_learned", "emergent_morph",
      "emergent_morph_learned", "emergent_nocells", "emergent_notiers"]
STL = ["No communication", "Flat", "Fixed supervisor", "Fixed tiers", "Emergent, three tiers",
       "Three tiers, learned", "Emergent, changing shape", "Changing shape, learned",
       "Three tiers, no merging", "Three tiers, no tiers"]
REC = [("qe_pbe", "PBE (trained on)", "#2E5FA3", "o"), ("qe_hse06", "HSE06", "#C4452C", "s"),
       ("gpaw_r2scan", "r$^2$SCAN", "#009E73", "^")]
AG = ["mace_relax", "archive_mp", "gpumd_nep89_md", "gpumd_nep89_relax", "lammps_meam_md", "surrogate", "explorer"]
AGL = ["MACE-MP-0\nrelaxation", "MP archive", "NEP89 MD", "NEP89\nrelaxation", "MEAM MD", "Active\nlearner", "Random\nscout"]

fig, axs2 = plt.subplots(2, 2, figsize=(6.5, 5.2), gridspec_kw={"width_ratios": [1.2, 1.0]})
axs = axs2.ravel()

# (a) horizontal dot plot: one row per structure
ax = axs[0]
rng = np.random.default_rng(0)
for j, (r, lab, col, mk) in enumerate(REC):
    ys = np.arange(len(ST)) + (j - 1) * 0.24
    for yv, st in zip(ys, ST):
        a = np.array(team[r]["structures"][st]["early_recall_area"]["all"])
        b = [rng.choice(a, len(a)).mean() for _ in range(2000)]
        lo, hi = np.percentile(b, [5, 95])
        ax.errorbar(a.mean(), yv, xerr=[[a.mean() - lo], [hi - a.mean()]], fmt=mk, ms=3.2, color=col,
                    elinewidth=0.8, capsize=0, label=lab if st == "solo" else None)
for r, lab, col, mk in REC[:2]:
    ax.axvline(shap[r]["flat"]["v"]["mace_relax"], color=col, ls="--", lw=0.7)
ax.axhspan(7.55, 9.45, color="#EEEEEE", zorder=0)
ax.set_yticks(range(len(ST)))
ax.set_yticklabels(STL, fontsize=6.5)
ax.invert_yaxis()
ax.set_xlabel("Early share of the ten found")
ax.set_xlim(0.3, 0.85)
ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.17), frameon=False, ncol=3, handletextpad=0.2,
          columnspacing=0.6)
ax.text(0.745, 9.35, "ablations", fontsize=6, color="#666666")
ax.set_title("(a) Team value by structure", loc="left")

# (b)
ax = axs[1]
for st, lab, col in [("flat", "Flat", "#8C8C8C"), ("tiers_fixed", "Fixed tiers", "#B8860B"),
                     ("emergent", "Three tiers", "#C4452C"), ("emergent_morph", "Changing shape", "#6A3D9A")]:
    bd = team["qe_hse06"]["structures"][st]["band"]
    g = np.array(bd["grid"])
    if st in ("tiers_fixed", "emergent_morph"):
        ax.fill_between(g, bd["p05"], bd["p95"], color=col, alpha=0.10, lw=0, step="post")
    ax.step(g, bd["mean"], where="post", color=col, lw=1.1, label=lab)
ax.set_xlim(0, 0.4)
ax.set_ylim(0, 1.02)
ax.set_xlabel("Fraction of HSE06 compute")
ax.set_ylabel("Share of the ten found")
ax.legend(loc="lower right", bbox_to_anchor=(1.02, 0.0), frameon=False)
ax.set_title("(b) Held-out receiver HSE06", loc="left")

# (c)
ax = axs[2]
y = np.arange(len(AG))
bars = [("qe_pbe", "emergent", "#2E5FA3", None, "PBE, three tiers"),
        ("qe_pbe", "emergent_morph", "#9DB4D9", None, "PBE, changing shape"),
        ("qe_hse06", "emergent", "#C4452C", None, "HSE06, three tiers"),
        ("qe_hse06", "emergent_morph", "#E8A898", None, "HSE06, changing shape")]
for j, (r, st, col, _, lab) in enumerate(bars):
    d = [shap[r][st]["shapley"][a] - shap[r]["flat"]["shapley"][a] for a in AG]
    ax.barh(y + (j - 1.5) * 0.2, d, height=0.19, color=col, label=lab)
ax.axvline(0, color="#333333", lw=0.6)
ax.set_yticks(y)
ax.set_yticklabels(AGL, fontsize=6.5)
ax.invert_yaxis()
ax.set_xlabel("Emergent minus flat")
ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.2), frameon=False, ncol=2, fontsize=6.5,
          handlelength=1.2, columnspacing=0.8)
ax.set_title("(c) Structural credit", loc="left")

# (d) shape of the changing-shape team over the HSE06 campaign
ax = axs[3]
for st, col, lab in [("emergent_morph", "#6A3D9A", "Changing shape"),
                     ("emergent_morph_learned", "#B39DDB", "Changing shape, learned")]:
    gm = team["qe_hse06"]["structures"][st]["geometry"]
    g = np.array(gm["grid"])
    if "learned" not in st:
        ax.fill_between(g, gm["n_tiers"]["p05"], gm["n_tiers"]["p95"], color=col, alpha=0.15, lw=0, step="post")
    ax.step(g, gm["n_tiers"]["mean"], where="post", color=col, lw=1.2, label="Tiers" + (", learned" if "learned" in st else ""))
gm = team["qe_hse06"]["structures"]["emergent_morph"]["geometry"]
g = np.array(gm["grid"])
ax.fill_between(g, gm["top_size"]["p05"], gm["top_size"]["p95"], color="#6A3D9A", alpha=0.08, lw=0, step="post")
ax.step(g, gm["top_size"]["mean"], where="post", color="#6A3D9A", lw=1.0, ls="--", label="Members in top tier")
ax.axhline(3, color="#C4452C", lw=0.9, ls=":", label="Three tiers (fixed)")
ax.set_xlim(0, 1)
ax.set_ylim(0, 7.5)
ax.set_xlabel("Fraction of HSE06 compute")
ax.set_ylabel("Count")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), frameon=False, ncol=2, fontsize=6.5,
          handlelength=1.8, columnspacing=0.8)
ax.set_title("(d) Changing shape, HSE06", loc="left")

for a in axs:
    a.spines[["top", "right"]].set_visible(False)
fig.tight_layout(w_pad=0.8, h_pad=1.0)
OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "emergent_swarm.png", dpi=300)
fig.savefig(OUT / "emergent_swarm.pdf")
print("wrote", OUT / "emergent_swarm.png")
