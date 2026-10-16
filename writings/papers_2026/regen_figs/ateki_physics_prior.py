#!/usr/bin/env python3
"""Regenerate ATEKi Figure D.1 (donor ordering as an exact-Shapley player).

Panels: two, TMLR full width (6.5 in). Data: exact three-player
Shapley attribution on the version-locked band-gap archive.
  Means: ateki/results/physics_attribution/06_physics_prior_attribution.json
  Runs:  06_physics_prior_attribution_per_run.json in the same folder, a
         re-run of experiments/06_physics_prior_attribution.py (archive
         hash f2158ecdc78e0229, same seeds) that also stores the 80
         per-run values (8 data sources x 10 seeds) per budget; its means
         equal the stored ones to 1e-9 (checked below).
  Left : mean phi per player vs budget, band = 90% percentile-bootstrap
         interval of the mean over the 80 runs (4000 resamples, seed 0).
  Right: prior share of the grand-coalition value (ratio of means),
         band = 90% bootstrap interval of the same ratio.

Size and fonts: figsize (TMLR_FULL, 2.7), fonts from paper_fig_style.
Palette shared with the campaign-attribution figure: pairwise comparisons
MP_BLUE, four-sample trays JARVIS_GREEN, donor ordering SNUMAT_PURPLE.
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from paper_fig_style import (  # noqa: E402
    TMLR_FULL, MP_BLUE, JARVIS_GREEN, SNUMAT_PURPLE, INK,
    apply_style, save,
)
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
ART = ROOT / "ateki/results/physics_attribution/06_physics_prior_attribution.json"
RUNS = ROOT / "ateki/results/physics_attribution/06_physics_prior_attribution_per_run.json"
OUT = ROOT / "writings/papers_2026/ateki_tmlr/figures/06_physics_prior_attribution.png"

PLAYERS = [
    ("physics_prior", "donor database ordering (e.g. MP GGA)", SNUMAT_PURPLE, "o"),
    ("kway_events", "purchased four-sample trays", JARVIS_GREEN, "s"),
    ("pair_events", "purchased pairwise comparisons", MP_BLUE, "^"),
]


def main():
    apply_style()
    d = json.load(open(ART, encoding="utf-8"))
    r = json.load(open(RUNS, encoding="utf-8"))
    budgets = d["budgets"]
    for key, *_ in PLAYERS:
        for i, b in enumerate(budgets):
            got = float(np.mean(r["phi_per_run"][key][str(b)]))
            assert abs(got - d["mean_phi"][key][i]) < 1e-9, (key, b, got)
    n = len(r["phi_per_run"]["physics_prior"][str(budgets[0])])
    rng = np.random.default_rng(0)
    idx = rng.integers(0, n, (4000, n))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(TMLR_FULL, 2.7))
    for key, label, col, mk in PLAYERS:
        lo, hi = [], []
        for b in budgets:
            bm = np.asarray(r["phi_per_run"][key][str(b)])[idx].mean(1)
            lo.append(np.percentile(bm, 5))
            hi.append(np.percentile(bm, 95))
        ax1.fill_between(budgets, lo, hi, color=col, alpha=0.18, lw=0)
        ax1.plot(budgets, d["mean_phi"][key], marker=mk, markersize=4,
                 color=col, label=label)
    ax1.set_xlabel("evaluation budget (purchased evaluations)")
    ax1.set_ylabel("Shapley value $\\phi$ (Kendall $\\tau$ units)")
    ax1.set_title(f"(a) Credit per contributor, n = {n} runs", loc="left")
    ax1.set_xticks(budgets)
    ax1.set_ylim(0.0, 0.62)
    ax1.legend(loc="upper center", ncol=1, fontsize=7)

    share = [100 * s for s in d["physics_share_of_grand"]]
    lo, hi = [], []
    for b in budgets:
        p = np.asarray(r["phi_per_run"]["physics_prior"][str(b)])[idx].mean(1)
        g = np.asarray(r["grand_per_run"][str(b)])[idx].mean(1)
        lo.append(100 * np.percentile(p / g, 5))
        hi.append(100 * np.percentile(p / g, 95))
    ax2.fill_between(budgets, lo, hi, color=SNUMAT_PURPLE, alpha=0.18, lw=0)
    ax2.plot(budgets, share, marker="o", markersize=4, color=SNUMAT_PURPLE)
    ax2.set_xlabel("evaluation budget (purchased evaluations)")
    ax2.set_ylabel("ordering's share of team value (%)")
    ax2.set_title("(b) Donor ordering's share of the outcome", loc="left")
    ax2.set_xticks(budgets)
    ax2.set_ylim(25, 70)
    for i in (0, len(budgets) - 1):
        ax2.annotate(f"{share[i]:.1f}%", xy=(budgets[i], share[i]),
                     xytext=(4 if i == 0 else -4, 8), textcoords="offset points",
                     ha="left" if i == 0 else "right", fontsize=7, color=INK)
    save(fig, OUT)
    print("share 90% bands:", [f"{a:.1f}-{b:.1f}" for a, b in zip(lo, hi)])


if __name__ == "__main__":
    main()
