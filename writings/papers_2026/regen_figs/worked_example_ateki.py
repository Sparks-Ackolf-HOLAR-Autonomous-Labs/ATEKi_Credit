#!/usr/bin/env python3
"""ATEKi worked-example figure: from 128 measured campaigns to credit.

Panels: two, all values from the committed coalition cache
(ateki/results/database_attribution/coalitions/expt_zhuo/, one JSON per
coalition; value_early = measured early-window mean tau of a paired
campaign whose pooled prior uses exactly that donor subset, with the ten
per-seed values in per_seed_early) and the committed exact Shapley values
with their seed intervals
(ateki/results/database_attribution/expt_zhuo/database_attribution.json).
(a) The coalition landscape: all 128 measured campaign values sorted,
    coloured by whether the donor subset contains a SNUMAT source, each
    with its 95% percentile-bootstrap interval of the seed mean (2000
    resamples of the ten matched seeds, fixed generator seed); the
    campaign without donor advice, the full seven-donor pool, and the
    best subset (named) are marked.
(b) Exact Shapley credit of each of the seven donors (the size-weighted
    average of its 64 measured marginal jumps), with the 95% interval
    over the ten matched seeds (shapley_seed_cis), coloured by database
    family.

Size and fonts: TMLR full width (6.5 in), fonts per paper_fig_style.
ASCII only.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from paper_fig_style import (  # noqa: E402
    TMLR_FULL, SOURCE_COLOURS, SNUMAT_PURPLE, ACCENT_RED, GREY, INK,
    apply_style, save,
)
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
COAL = ROOT / "ateki/results/database_attribution/coalitions/expt_zhuo"
DBA = ROOT / "ateki/results/database_attribution/expt_zhuo/database_attribution.json"
OUT = ROOT / "writings/papers_2026/ateki_tmlr/figures/worked_example_ateki.png"

NAME = {"mp_gga": "MP GGA", "mp_gga_expsynth": "MP GGA (ICSD subset)",
        "mp_r2scan": "MP r$^2$SCAN", "jarvis_optb88vdw": "JARVIS OptB88vdW",
        "jarvis_mbj": "JARVIS TB-mBJ", "snumat_gga": "SNUMAT GGA",
        "snumat_hse": "SNUMAT HSE06"}


def main():
    apply_style()
    coals, seeds = {}, {}
    for f in COAL.glob("*.json"):
        d = json.load(open(f, encoding="utf-8"))
        k = frozenset(d["members"])
        coals[k] = float(d["value_early"])
        seeds[k] = np.array([float(v) for v in d["per_seed_early"].values()])
    assert len(coals) == 128, len(coals)
    dba = json.load(open(DBA, encoding="utf-8"))
    shap = dba["exact"]["shapley"]
    cis = dba["shapley_seed_cis"]

    fig, axes = plt.subplots(1, 2, figsize=(TMLR_FULL, 2.85),
                             gridspec_kw={"width_ratios": [1.3, 1.0]})

    # (a) the coalition landscape with seed intervals
    ax = axes[0]
    rng = np.random.default_rng(0)
    items = sorted(coals.items(), key=lambda kv: kv[1])
    xs = np.arange(len(items))
    lo, hi = [], []
    for k, _ in items:
        a = seeds[k]
        b = a[rng.integers(0, len(a), (2000, len(a)))].mean(1)
        lo.append(np.percentile(b, 2.5))
        hi.append(np.percentile(b, 97.5))
    snumat = [any(m.startswith("snumat") for m in k) for k, _ in items]
    cols = [SNUMAT_PURPLE if s else GREY for s in snumat]
    ax.vlines(xs, lo, hi, colors=cols, lw=0.6, alpha=0.30, zorder=1)
    ax.scatter(xs, [v for _, v in items], s=8, c=cols, zorder=2)
    full = frozenset(shap.keys())
    empty_v = coals[frozenset()]
    full_v = coals[full]
    best_k, best_v = max(coals.items(), key=lambda kv: kv[1])
    best_name = " + ".join(NAME[m] for m in sorted(best_k, key=lambda m: -shap[m]))
    marks = ((frozenset(), f"no donor advice  {empty_v:.3f}", (6, -0.08), "left"),
             (full, f"all seven donors  {full_v:.3f}", (6, -0.10), "left"),
             (best_k, f"best subset  {best_v:.3f}:\n{best_name}", (-6, 0.08), "right"))
    for k, lbl, (dx, dy), ha in marks:
        x = next(i for i, (kk, _) in enumerate(items) if kk == k)
        v = coals[k]
        ax.scatter([x], [v], s=30, facecolor="white", edgecolor=ACCENT_RED,
                   lw=1.1, zorder=3)
        ax.annotate(lbl, xy=(x, v), xytext=(x + dx, v + dy), fontsize=7,
                    color=ACCENT_RED, ha=ha, va="center",
                    arrowprops=dict(arrowstyle="-", color=ACCENT_RED, lw=0.6))
    ax.scatter([], [], s=8, c=SNUMAT_PURPLE, label="subset holds a SNUMAT database")
    ax.scatter([], [], s=8, c=GREY, label="no SNUMAT database")
    ax.legend(loc="lower right", fontsize=7, handletextpad=0.2)
    ax.set_ylim(0.40, 1.0)
    ax.set_xlabel("the 128 donor subsets, sorted by campaign outcome")
    ax.set_ylabel("early-window campaign\nquality (Kendall $\\tau$)")
    ax.set_title("(a) Every donor subset run (10 seeds each)", loc="left", fontsize=8)

    # (b) exact Shapley credit of the seven donors with seed intervals
    ax = axes[1]
    order = sorted(shap, key=shap.get, reverse=True)
    y = np.arange(len(order))
    vals = np.array([shap[k] for k in order])
    elo = vals - np.array([cis[k]["ci"][0] for k in order])
    ehi = np.array([cis[k]["ci"][1] for k in order]) - vals
    ax.barh(y, vals, color=[SOURCE_COLOURS[k] for k in order], height=0.62)
    ax.errorbar(vals, y, xerr=[elo, ehi], fmt="none", ecolor=INK, elinewidth=0.8,
                capsize=2)
    ax.axvline(0, color=INK, lw=0.7)
    ax.set_xticks([-0.04, -0.02, 0, 0.02, 0.04, 0.06])
    ax.set_yticks(y)
    ax.set_yticklabels([NAME[k] for k in order], fontsize=7)
    ax.invert_yaxis()
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Shapley credit (Kendall $\\tau$ gain)")
    ax.set_title("(b) Credit of each database", loc="left", fontsize=8)
    save(fig, OUT)


if __name__ == "__main__":
    main()
