#!/usr/bin/env python3
"""Regenerate ATEKi Figure 7 (attribution over paired campaign arms).

Panels: three, TMLR full width (6.5 in). Data: measured k=4
50-seed paired-campaign attribution from
ateki/results/campaign_attribution/k4_50seed/07_campaign_attribution.json.
  Left  : windows.{early,final}.mean_shapley for the four factor
          players (cold_data, donor_prior, adaptive_trust,
          kway_events); grouped bars, value labels. Shows the veto
          player and the prior's decay (+0.0792 -> +0.0228) against
          the persistent k-way share (~+0.028).
  Centre: histogram of windows.early.per_cell[cell].shapley.
          donor_prior.mean over the 56 donor->receiver cells;
          negative cells coloured red (87.5% positive).
  Right : negative_prior_cells (5 cells): paired horizontal bars of
          prior_shapley (negative, red) vs trust_shapley (positive,
          gold); trust priced as a safeguard exactly where the prior
          harms.

Size and fonts: figsize (TMLR_FULL, 2.9). Factor palette shared with the
physics-prior figure: cold data MP_BLUE, donor prior SNUMAT_PURPLE,
adaptive trust EXPT_GOLD, k-way events JARVIS_GREEN, harmful values
ACCENT_RED. Labels use "data source".
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from paper_fig_style import (  # noqa: E402
    TMLR_FULL, MP_BLUE, JARVIS_GREEN, SNUMAT_PURPLE, EXPT_GOLD,
    ACCENT_RED, GREY, INK, apply_style, save,
)
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
ART = ROOT / "ateki/results/campaign_attribution/k4_50seed/07_campaign_attribution.json"
OUT = ROOT / "writings/papers_2026/ateki_tmlr/figures/07_campaign_attribution.png"

FACTORS = [
    ("cold_data", "own\nmeasure-\nments", MP_BLUE),
    ("donor_prior", "donor\nordering", SNUMAT_PURPLE),
    ("adaptive_trust", "learned\ntrust", EXPT_GOLD),
    ("kway_events", "four-\nsample\ntrays", JARVIS_GREEN),
]

# Compact donor->receiver names for the five negative-prior cells
SHORT = {
    "mp_gga": "MP GGA",
    "mp_gga_expsynth": "MP GGA (ICSD)",
    "jarvis_mbj": "TB-mBJ",
    "snumat_gga": "SNUMAT GGA",
    "snumat_hse": "SNUMAT HSE06",
    "expt_zhuo": "Expt. (Zhuo)",
}


def main():
    apply_style()
    d = json.load(open(ART))
    early = d["windows"]["early"]["mean_shapley"]
    final = d["windows"]["final"]["mean_shapley"]

    fig, (ax1, ax2, ax3) = plt.subplots(
        1, 3, figsize=(TMLR_FULL, 2.9),
        gridspec_kw={"width_ratios": [1.2, 1.0, 1.0]})

    # Left: per-factor mean Shapley, early vs final
    xs = np.arange(len(FACTORS))
    w = 0.38
    for off, window, alpha, tag in ((-w / 2, early, 1.0, "early"),
                                    (w / 2, final, 0.45, "final")):
        vals = [window[k] for k, _, _ in FACTORS]
        cols = [c for _, _, c in FACTORS]
        ax1.bar(xs + off, vals, width=w, color=cols, alpha=alpha,
                edgecolor="none")
        for x, v in zip(xs + off, vals):
            if abs(v) >= 0.05:
                ax1.annotate(f"{v:+.2f}", xy=(x, v), xytext=(0, 2),
                             textcoords="offset points", ha="center",
                             va="bottom", fontsize=7, color=INK)
    ax1.set_xticks(xs)
    ax1.set_xticklabels([lab for _, lab, _ in FACTORS], fontsize=7)
    ax1.axhline(0, color=INK, linewidth=0.8)
    ax1.set_ylabel("mean Shapley value (Kendall $\\tau$)")
    ax1.set_title("(a) per-factor credit,\n56 cells", loc="left")
    ax1.set_ylim(-0.12, 0.88)
    ax1.grid(axis="x", visible=False)
    handles = [plt.Rectangle((0, 0), 1, 1, color=GREY, alpha=a)
               for a in (1.0, 0.45)]
    ax1.legend(handles, ["early window", "final window"],
               loc="upper right")

    # Centre: donor-prior Shapley across the 56 cells (early)
    per_cell = d["windows"]["early"]["per_cell"]
    priors = [c["shapley"]["donor_prior"]["mean"]
              for c in per_cell.values()]
    bins = np.arange(-0.06, 0.221, 0.02)
    counts, edges = np.histogram(priors, bins=bins)
    centres = 0.5 * (edges[:-1] + edges[1:])
    cols = [ACCENT_RED if c < 0 else SNUMAT_PURPLE for c in centres]
    ax2.bar(centres, counts, width=0.019, color=cols)
    ax2.axvline(0, color=INK, linewidth=0.8)
    ax2.set_xlabel("donor-prior Shapley value")
    ax2.set_ylabel("number of cells")
    ax2.set_title("(b) donor prior,\nearly window", loc="left")
    ax2.grid(axis="x", visible=False)
    ax2.set_ylim(0, 8.4)
    ax2.annotate("87.5% of cells\npositive", xy=(0.97, 0.97),
                 xycoords="axes fraction", ha="right", va="top",
                 fontsize=7, color=INK)

    # Right: the five harmful-prior cells, prior vs trust
    cells = d["negative_prior_cells"]
    ys = np.arange(len(cells))[::-1]
    hw = 0.36
    for off, key, col, lab in ((hw / 2, "prior_shapley", ACCENT_RED,
                                "donor prior"),
                               (-hw / 2, "trust_shapley", EXPT_GOLD,
                                "adaptive trust")):
        ax3.barh(ys + off, [c[key] for c in cells], height=hw,
                 color=col, label=lab)
    labels = []
    for c in cells:
        don, rec = c["cell"].split("->")
        labels.append(f"{SHORT[don]} $\\to$\n{SHORT[rec]}")
    ax3.set_yticks(ys)
    ax3.set_yticklabels(labels, fontsize=6.5)
    ax3.axvline(0, color=INK, linewidth=0.8)
    ax3.set_xlabel("Shapley value")
    ax3.set_title("(c) trust as a\nsafeguard", loc="left")
    ax3.grid(axis="y", visible=False)
    ax3.set_ylim(-2.0, len(cells) - 0.5)
    ax3.legend(loc="lower left", ncol=1, fontsize=6.5, handlelength=1.0,
               frameon=True, facecolor="white", edgecolor="none",
               framealpha=1.0)
    save(fig, OUT)


if __name__ == "__main__":
    main()
