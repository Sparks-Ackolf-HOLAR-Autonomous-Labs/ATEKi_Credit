#!/usr/bin/env python3
"""ATEKi worked-example figure: from 128 measured campaigns to credit.

Panels: two, all values from the committed coalition cache
(ateki/results/database_attribution/coalitions/expt_zhuo/, one JSON per
coalition; value_early = measured early-window mean tau of a paired
campaign whose pooled prior uses exactly that donor subset) and the
committed exact Shapley values
(ateki/results/database_attribution/expt_zhuo/database_attribution.json).
(a) The coalition landscape: all 128 measured campaign values sorted,
    coloured by whether the donor subset contains a SNUMAT source;
    the cold campaign v(empty), the full seven-donor pool, and the best
    coalition are marked.
(b) One player's credit, step by step: the measured jump
    v(S + player) - v(S) over all 64 subsets S for SNUMAT HSE06 and for
    MP GGA, with the committed exact Shapley credit annotated (the
    size-weighted average of exactly these jumps).

Size and fonts: TMLR full width (6.5 in), fonts per paper_fig_style.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from paper_fig_style import (  # noqa: E402
    TMLR_FULL, MP_BLUE, SNUMAT_PURPLE, EXPT_GOLD, ACCENT_RED, GREY, INK,
    apply_style, save,
)
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
COAL = ROOT / "ateki/results/database_attribution/coalitions/expt_zhuo"
DBA = ROOT / "ateki/results/database_attribution/expt_zhuo/database_attribution.json"
OUT = ROOT / "writings/papers_2026/ateki_tmlr/figures/worked_example_ateki.png"


def main():
    apply_style()
    coals = {}
    for f in COAL.glob("*.json"):
        d = json.load(open(f))
        coals[frozenset(d["members"])] = float(d["value_early"])
    assert len(coals) == 128, len(coals)
    dba = json.load(open(DBA))
    shap = dba["exact"]["shapley"]

    fig, axes = plt.subplots(1, 2, figsize=(TMLR_FULL, 2.7),
                             gridspec_kw={"width_ratios": [1.25, 1.0]})

    # (a) the coalition landscape
    ax = axes[0]
    items = sorted(coals.items(), key=lambda kv: kv[1])
    xs = np.arange(len(items))
    snumat = [any(m.startswith("snumat") for m in k) for k, _ in items]
    ax.scatter(xs, [v for _, v in items], s=9,
               c=[SNUMAT_PURPLE if s else GREY for s in snumat], zorder=2)
    full = frozenset(shap.keys())
    empty_v = coals[frozenset()]
    full_v = coals[full]
    best_k, best_v = max(coals.items(), key=lambda kv: kv[1])
    marks = ((empty_v, f"cold campaign  {empty_v:+.3f}", (6, -0.002), "left"),
             (full_v, f"all 7 donors  {full_v:+.3f}", (6, -0.010), "left"),
             (best_v, f"best subset  {best_v:+.3f}",
              (-6, 0.0), "right"))
    for v, lbl, (dx, dy), ha in marks:
        x = next(i for i, (_, vv) in enumerate(items) if vv == v)
        ax.scatter([x], [v], s=34, facecolor="white", edgecolor=ACCENT_RED,
                   lw=1.2, zorder=3)
        ax.annotate(lbl, xy=(x + dx, v + dy), fontsize=6.8, color=ACCENT_RED,
                    ha=ha, va="center")
    ax.scatter([], [], s=9, c=SNUMAT_PURPLE, label="subset contains a SNUMAT donor")
    ax.scatter([], [], s=9, c=GREY, label="no SNUMAT donor")
    ax.legend(loc="lower right", fontsize=6.5)
    ax.set_xlabel("the 128 donor subsets, sorted by campaign outcome")
    ax.set_ylabel("measured early-window\ncampaign quality (Kendall $\\tau$)")
    ax.set_title("(a) every donor subset was actually run", fontsize=8)

    # (b) one player's credit
    ax = axes[1]
    players = [("snumat_hse", "SNUMAT HSE06", SNUMAT_PURPLE),
               ("mp_gga", "MP GGA", MP_BLUE)]
    rng = np.random.default_rng(0)
    for i, (pid, name, col) in enumerate(players):
        margs = []
        for k, v in coals.items():
            if pid not in k:
                margs.append(coals[k | {pid}] - v)
        margs = np.array(margs)
        jitter = rng.uniform(-0.13, 0.13, len(margs))
        ax.scatter(np.full(len(margs), i) + jitter, margs, s=8, color=col,
                   alpha=0.55, zorder=2)
        phi = shap[pid]
        ax.hlines(phi, i - 0.24, i + 0.24, color=ACCENT_RED, lw=1.6, zorder=3)
        ax.annotate(f"Shapley {phi:+.3f}", xy=(i + 0.27, phi),
                    fontsize=6.8, color=ACCENT_RED, va="center")
    ax.axhline(0, color=INK, lw=0.7)
    ax.set_xticks([0, 1])
    ax.set_xticklabels([p[1] for p in players])
    ax.set_xlim(-0.5, 2.05)
    ax.set_ylabel("measured jump when the donor\njoins a subset (Kendall $\\tau$)")
    ax.set_title("(b) credit = size-weighted average\nof 64 measured jumps",
                 fontsize=8)
    save(fig, OUT)


if __name__ == "__main__":
    main()
