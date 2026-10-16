#!/usr/bin/env python3
"""ATEKi main-text figure: credit depends on the compute charged.

Two systems in one figure, TMLR full width (6.5 in), true print size.
Data (all committed, no new campaigns):
  (a) band gaps, HSE06 receiver computed on demand, 142 candidates without
      halogens, five donors, all 32 coalitions:
      compute/semiconductor_campaign/results/campaigns/qe_hse06_nohalide/summary.json
      (HSE06 compute charged) and qe_hse06_nohalide_combined/summary.json
      (HSE06 plus the PBE relaxations charged). Only coalition means over
      the 40 runs are stored for this game, so the bars carry no interval.
  (b) Al-Mg-Si, PBE receiver, four donors, all 16 coalitions:
      compute/almgsi_campaign/results/campaigns/qe_pbe_shapley_coalitions/coalitions.json
  (c) Al-Mg-Si, HSE06 receiver, five donors, all 32 coalitions:
      qe_hse06_shapley_coalitions/coalitions.json (HSE06 compute) and
      qe_hse06_shapley_combined/coalitions.json (HSE06 plus PBE compute).
  For (b) and (c) the per-run coalition values (40 runs: 20 seeds x
  batches of one and four, MD values drawn from their sampling error) give
  one exact Shapley vector per run; bars are the means (equal to the
  published values) and whiskers the 90% percentile-bootstrap interval of
  the mean over runs (4000 resamples, generator seed 0).
Encoding: colour = donor (QE PBE dark grey in both systems), dark = fixed
trust, light = learned trust, hatched = PBE relaxations also charged.
ASCII only.
"""

import json
import sys
from itertools import combinations
from math import factorial
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import paper_fig_style as st  # noqa: E402

st.apply_style()
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

SO = HERE.parents[2]
SEMI = SO / "compute" / "semiconductor_campaign" / "results" / "campaigns"
ALLOY = SO / "compute" / "almgsi_campaign" / "results" / "campaigns"
OUT = HERE.parent / "ateki_tmlr" / "figures" / "compute_credit.png"

PBE_INK = "#333333"
NAMES = {"qe_pbe": "PBE\n(computed)", "mp_gga": "MP GGA", "jarvis_mbj": "JARVIS\nTB-mBJ",
         "snumat_hse": "SNUMAT\nHSE06", "expt_zhuo": "Measured\ngaps",
         "mace_relax": "MACE-MP-0\nrelaxation", "archive_mp": "MP archive",
         "lammps_meam_md": "MEAM MD\n300 K", "gpumd_nep89_md": "NEP89 MD\n300 K"}
COL = {"qe_pbe": PBE_INK, "mp_gga": st.MP_BLUE, "jarvis_mbj": st.JARVIS_GREEN,
       "snumat_hse": st.SNUMAT_PURPLE, "expt_zhuo": st.EXPT_GOLD,
       # body colours shared with the organisation figures
       "mace_relax": "#2E5FA3", "archive_mp": "#009E73", "gpumd_nep89_md": "#C4452C",
       "lammps_meam_md": "#8C564B"}


def shapley_from(values, players):
    n = len(players)
    phi = {}
    for p in players:
        others = [q for q in players if q != p]
        s = 0.0
        for k in range(n):
            w = factorial(k) * factorial(n - k - 1) / factorial(n)
            for c in combinations(others, k):
                s += w * (values["+".join(sorted(c + (p,)))] - values["+".join(sorted(c))])
        phi[p] = s
    return phi


def per_run_ci(path, mode):
    d = json.loads(path.read_text(encoding="utf-8"))[mode]
    players = d["players"]
    pr = d["per_run"]
    nrun = len(next(iter(pr.values())))
    runs = np.array([[shapley_from({k: v[r] for k, v in pr.items()}, players)[p] for p in players]
                     for r in range(nrun)])
    rng = np.random.default_rng(0)
    boot = runs[rng.integers(0, nrun, (4000, nrun))].mean(1)
    mean = runs.mean(0)
    lo, hi = np.percentile(boot, [5, 95], axis=0)
    return {p: (mean[i], lo[i], hi[i]) for i, p in enumerate(players)}, nrun


def bars(ax, donors, series, title):
    """series: list of (offset, dict donor->(mean, lo, hi) or mean, light, hatch)."""
    y = np.arange(len(donors))
    h = 0.8 / len(series)
    for j, (vals, light, hatch) in enumerate(series):
        off = (j - (len(series) - 1) / 2) * h
        for i, dn in enumerate(donors):
            v = vals[dn]
            m = v[0] if isinstance(v, tuple) else v
            c = COL[dn]
            ax.barh(y[i] + off, m, height=h * 0.92, color=c, alpha=0.42 if light else 1.0,
                    hatch="////" if hatch else None, edgecolor="white" if hatch else c, lw=0)
            if isinstance(v, tuple):
                ax.plot([v[1], v[2]], [y[i] + off] * 2, color=st.INK, lw=0.8)
    ax.axvline(0, color=st.INK, lw=0.6)
    ax.set_yticks(y)
    ax.set_yticklabels([NAMES[d] for d in donors], fontsize=7)
    ax.invert_yaxis()
    ax.grid(axis="y", visible=False)
    ax.set_title(title, loc="left", fontsize=8)


def main():
    plt.rcParams["hatch.linewidth"] = 0.6
    fig, axs = plt.subplots(1, 3, figsize=(st.TMLR_FULL, 3.1),
                            gridspec_kw={"width_ratios": [1.0, 0.8, 1.0]})

    # (a) band gaps
    s1 = json.loads((SEMI / "qe_hse06_nohalide" / "summary.json").read_text(encoding="utf-8"))["shapley"]
    s2 = json.loads((SEMI / "qe_hse06_nohalide_combined" / "summary.json").read_text(encoding="utf-8"))["shapley"]
    don = sorted(s1["pooled_fixed"]["shapley"], key=lambda k: -s1["pooled_fixed"]["shapley"][k])
    bars(axs[0], don, [(s1["pooled_fixed"]["shapley"], False, False),
                       (s1["pooled_learned"]["shapley"], True, False),
                       (s2["pooled_fixed"]["shapley"], False, True),
                       (s2["pooled_learned"]["shapley"], True, True)],
         "(a) Band gaps, HSE06 receiver")
    axs[0].set_xlabel("Shapley credit\n(share of ten widest gaps)")

    # (b) Al-Mg-Si PBE receiver
    pf, n1 = per_run_ci(ALLOY / "qe_pbe_shapley_coalitions" / "coalitions.json", "pooled_fixed")
    pl, _ = per_run_ci(ALLOY / "qe_pbe_shapley_coalitions" / "coalitions.json", "pooled_learned")
    don = sorted(pf, key=lambda k: -pf[k][0])
    bars(axs[1], don, [(pf, False, False), (pl, True, False)], "(b) Al-Mg-Si, PBE receiver")
    axs[1].set_xlabel("Shapley credit\n(share of ten most stable)")

    # (c) Al-Mg-Si HSE06 receiver, two accountings
    hf, _ = per_run_ci(ALLOY / "qe_hse06_shapley_coalitions" / "coalitions.json", "pooled_fixed")
    hl, _ = per_run_ci(ALLOY / "qe_hse06_shapley_coalitions" / "coalitions.json", "pooled_learned")
    cf, _ = per_run_ci(ALLOY / "qe_hse06_shapley_combined" / "coalitions.json", "pooled_fixed")
    cl, _ = per_run_ci(ALLOY / "qe_hse06_shapley_combined" / "coalitions.json", "pooled_learned")
    don = sorted(hf, key=lambda k: -hf[k][0])
    bars(axs[2], don, [(hf, False, False), (hl, True, False), (cf, False, True), (cl, True, True)],
         "(c) Al-Mg-Si, HSE06 receiver")
    axs[2].set_xlabel("Shapley credit\n(share of ten most stable)")
    for a in axs:
        a.set_xlim(-0.33, 0.33)
        a.set_xticks([-0.2, 0, 0.2])
    hdl = [Patch(facecolor="#555555", label="fixed trust"),
           Patch(facecolor="#555555", alpha=0.42, label="learned trust"),
           Patch(facecolor="#555555", edgecolor="white", hatch="////", lw=0,
                 label="PBE relaxations also charged"),
           plt.Line2D([], [], color=st.INK, lw=0.8, label="90% interval over 40 runs")]
    fig.legend(handles=hdl, loc="lower center", ncol=4, fontsize=7, frameon=False,
               bbox_to_anchor=(0.5, -0.01), handlelength=1.6, columnspacing=1.2)
    fig.get_layout_engine().set(rect=(0, 0.07, 1, 0.93))
    st.save(fig, OUT)
    print("runs per game:", n1)
    for nm, dd in (("pbe fixed", pf), ("pbe learned", pl), ("hse fixed", hf), ("hse learned", hl),
                   ("hse+pbe fixed", cf), ("hse+pbe learned", cl)):
        print(nm, {k: tuple(round(x, 3) for x in v) for k, v in dd.items()})


if __name__ == "__main__":
    main()
