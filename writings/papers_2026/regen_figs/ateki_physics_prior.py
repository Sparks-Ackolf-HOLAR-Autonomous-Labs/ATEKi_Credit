#!/usr/bin/env python3
"""Regenerate ATEKi Figure 6 (physics prior as an exact-Shapley player).

Panels: two, TMLR full width (6.5 in). Data: exact three-player
Shapley attribution on the version-locked band-gap archive, from
ateki/results/physics_attribution/06_physics_prior_attribution.json.
  Left : mean_phi[player] vs budgets for the three knowledge sources
         (physics_prior, kway_events, pair_events); every point is a
         mean over 10 seeds x 8 data sources.
  Right: physics_share_of_grand vs budgets, i.e. the prior's share of
         the grand-coalition value, decaying 59.2% -> 37.2%.
Takeaway (caption): imported physics knowledge leads early, then hands
over to purchased evidence.

Size and fonts: figsize (TMLR_FULL, 2.7), fonts from paper_fig_style (7-8 pt
at print). Factor palette shared with the campaign-attribution figure:
purchased pairwise data MP_BLUE, k-way events JARVIS_GREEN, donor
physics prior SNUMAT_PURPLE. Labels use "data source".
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from paper_fig_style import (  # noqa: E402
    TMLR_FULL, MP_BLUE, JARVIS_GREEN, SNUMAT_PURPLE, INK,
    apply_style, save,
)
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
ART = ROOT / "ateki/results/physics_attribution/06_physics_prior_attribution.json"
OUT = ROOT / "writings/papers_2026/ateki_tmlr/figures/06_physics_prior_attribution.png"

PLAYERS = [
    ("physics_prior", "donor database ordering (e.g. MP GGA)", SNUMAT_PURPLE, "o"),
    ("kway_events", "purchased four-sample trays", JARVIS_GREEN, "s"),
    ("pair_events", "purchased pairwise comparisons", MP_BLUE, "^"),
]


def main():
    apply_style()
    d = json.load(open(ART))
    budgets = d["budgets"]
    phi = d["mean_phi"]
    share = d["physics_share_of_grand"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(TMLR_FULL, 2.7))

    for key, label, col, mk in PLAYERS:
        ax1.plot(budgets, phi[key], marker=mk, markersize=4,
                 color=col, label=label)
    ax1.set_xlabel("evaluation budget")
    ax1.set_ylabel("Shapley value $\\phi$ (Kendall $\\tau$ units)")
    ax1.set_title("Exact three-player attribution")
    ax1.set_xticks(budgets)
    ax1.legend(loc="upper right")
    ax1.set_ylim(0.05, 0.45)

    ax2.plot(budgets, [100 * s for s in share], marker="o",
             markersize=4, color=SNUMAT_PURPLE)
    ax2.set_xlabel("evaluation budget")
    ax2.set_ylabel("prior share of grand-coalition value (%)")
    ax2.set_title("Donor ordering's share of the outcome")
    ax2.set_xticks(budgets)
    ax2.set_ylim(30, 66)
    for i in (0, len(budgets) - 1):
        v = 100 * share[i]
        ax2.annotate(f"{v:.1f}%", xy=(budgets[i], v),
                     xytext=(0, 6), textcoords="offset points",
                     ha="left" if i == 0 else "right", fontsize=7,
                     color=INK)
    save(fig, OUT)


if __name__ == "__main__":
    main()
