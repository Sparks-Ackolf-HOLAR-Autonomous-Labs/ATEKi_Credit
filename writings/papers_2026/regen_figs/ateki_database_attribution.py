#!/usr/bin/env python3
"""Regenerate the ATEKi seven-database attribution figure.

One panel (0.62 x TMLR width). The per-donor credit panel with its seed
intervals now sits in the main-text worked example
(worked_example_ateki.py). Data:
ateki/results/database_attribution/expt_zhuo/database_attribution.json.
  mc_validation.curve: median max abs error of
         permutation-sampled Shapley vs exact over m in
         {10..3000} (20 replicates, min-max band), plus the
         rank-exact fraction, which is 0 at every m because of the
         true SNUMAT tie.

Size and fonts: figsize (TMLR_FULL, 3.0). Database-of-origin colours from
SOURCE_COLOURS/SOURCE_NAMES; labels use "data source" and
"version-locked archive".
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from paper_fig_style import (  # noqa: E402
    TMLR_FULL, SOURCE_COLOURS, SOURCE_NAMES, ACCENT_RED, MP_BLUE,
    INK, apply_style, save,
)
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
ART = ROOT / "ateki/results/database_attribution/expt_zhuo/database_attribution.json"
OUT = ROOT / "writings/papers_2026/ateki_tmlr/figures/database_attribution.png"


def main():
    apply_style()
    d = json.load(open(ART))
    shap = d["exact"]["shapley"]
    cis = d["shapley_seed_cis"]
    order = sorted(shap, key=shap.get, reverse=True)

    # The credit panel moved to the main-text worked example
    # (worked_example_ateki.py, panel b); this annex figure keeps the
    # sampling check only.
    fig, ax2 = plt.subplots(figsize=(TMLR_FULL * 0.62, 2.6))
    # Right: Monte-Carlo validation on the cached game
    curve = d["mc_validation"]["curve"]
    ms = [c["m"] for c in curve]
    med = [c["max_abs_error_median"] for c in curve]
    mn = [c["max_abs_error_min"] for c in curve]
    mx = [c["max_abs_error_max"] for c in curve]
    frac = [c["frac_replicates_rank_exact"] for c in curve]
    ax2.plot(ms, med, marker="o", markersize=4, color=MP_BLUE,
             label="median largest error")
    ax2.fill_between(ms, mn, mx, color=MP_BLUE, alpha=0.15,
                     linewidth=0, label="replicate range (min to max)")
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlabel("sampled permutations $m$")
    ax2.set_ylabel("largest absolute error vs exact\n(Kendall $\\tau$)")
    ax2.set_title("Sampled vs exact Shapley")
    ax2b = ax2.twinx()
    ax2b.plot(ms, frac, marker="s", markersize=3.5, linestyle="--",
              color=ACCENT_RED, linewidth=1.1,
              label="rank-exact fraction")
    ax2b.set_ylabel("fraction of replicates with exact ranking",
                    color=ACCENT_RED)
    ax2b.set_ylim(-0.04, 1.0)
    ax2b.tick_params(axis="y", colors=ACCENT_RED)
    ax2b.spines["right"].set_visible(True)
    ax2b.spines["right"].set_color(ACCENT_RED)
    ax2b.grid(visible=False)
    h1, l1 = ax2.get_legend_handles_labels()
    h2, l2 = ax2b.get_legend_handles_labels()
    ax2.legend(h1 + h2, l1 + l2, loc="upper right", fontsize=6.5)
    ax2.annotate("rank never exact:\ntrue SNUMAT tie", xy=(300, 0.0),
                 xycoords=("data", "axes fraction"),
                 xytext=(0, 14), textcoords="offset points",
                 fontsize=6.5, color=ACCENT_RED, ha="center")
    save(fig, OUT)


if __name__ == "__main__":
    main()
