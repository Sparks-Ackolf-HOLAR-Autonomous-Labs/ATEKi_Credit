#!/usr/bin/env python3
"""Regenerate the ATEKi seven-database attribution figure.

Panels: two, TMLR full width (6.5 in). Data:
ateki/results/database_attribution/expt_zhuo/database_attribution.json.
  Left : exact.shapley (early window) per donor, sorted descending,
         with 95% CIs over 10 matched seeds from shapley_seed_cis;
         bars coloured by database family (SOURCE_COLOURS). SNUMAT
         GGA/HSE exactly tied at +0.054; MP GGA lowest (-0.030).
         Annotated with v(N) and the best four-donor value, read from the artifact.
  Right: mc_validation.curve: median max abs error of
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

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(TMLR_FULL, 3.0),
        gridspec_kw={"width_ratios": [1.25, 1.0]})

    # Left: exact Shapley credit per donor data source
    xs = np.arange(len(order))
    vals = [shap[k] for k in order]
    lo = [shap[k] - cis[k]["ci"][0] for k in order]
    hi = [cis[k]["ci"][1] - shap[k] for k in order]
    cols = [SOURCE_COLOURS[k] for k in order]
    ax1.bar(xs, vals, color=cols, width=0.62)
    ax1.errorbar(xs, vals, yerr=[lo, hi], fmt="none", ecolor=INK,
                 elinewidth=0.8, capsize=2)
    ax1.axhline(0, color=INK, linewidth=0.8)
    ax1.set_xticks(xs)
    ax1.set_xticklabels([SOURCE_NAMES[k] for k in order],
                        rotation=32, ha="right", fontsize=6.5)
    ax1.set_ylabel("exact Shapley value (Kendall $\\tau$)")
    ax1.set_title("Credit for advising the experimental campaign")
    ax1.grid(axis="x", visible=False)
    ax1.annotate("exact tie:\n$+0.054$ each", xy=(0.5, 0.056),
                 xytext=(1.8, 0.066), fontsize=7, color=INK,
                 ha="left", va="center",
                 arrowprops=dict(arrowstyle="-", color=INK, lw=0.7))
    cv = {int(k): v for k, v in d["coalition_values_early"].items()}
    n = len(order)
    vN = cv[(1 << n) - 1]
    best4 = max(v for k, v in cv.items() if bin(k).count("1") == 4)
    ax1.annotate(f"all seven: ${vN:+.3f}$; best four:\n${best4:+.3f}$",
                 xy=(0.03, 0.05), xycoords="axes fraction",
                 fontsize=7, color=INK, ha="left", va="bottom")
    ax1.set_ylim(-0.055, 0.085)

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
