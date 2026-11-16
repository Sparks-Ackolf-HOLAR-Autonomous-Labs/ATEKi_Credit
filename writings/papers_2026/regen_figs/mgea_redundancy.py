"""MGEA figure: redundant knowledge and what a removal screen misses (seven-database measured-gap game, early window).
(a) Value added by the second SNUMAT database (SNUMAT HSE06) to every pool that already holds SNUMAT GGA, against the number of
    other databases in the pool: zero alone, positive in 30 of 31 pools with another database.
(b) Rank of each database under four contribution measures computed on the same 128 measured campaigns (ties share a rank).
(c) Agreement of each measure's ranking between two seeds: mean pairwise Spearman over the 45 seed pairs, with the minimum.
Data: ateki/results/database_attribution/expt_zhuo/database_attribution.json, data_valuation_estimators/data_valuation_estimators.json.
Output: writings/papers_2026/ateki_mgea/figures/redundancy.pdf/.png"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import paper_fig_style as st  # noqa: E402

st.apply_style()
import matplotlib.pyplot as plt  # noqa: E402

SO = HERE.parents[2]
RES = SO / "ateki" / "results"
OUT = HERE.parent / "ateki_mgea" / "figures"
d = json.loads((RES / "database_attribution/expt_zhuo/database_attribution.json").read_text())
e = json.loads((RES / "data_valuation_estimators/data_valuation_estimators.json").read_text())
donors = d["donors"]
bit = {k: 1 << i for i, k in enumerate(donors)}
v = {int(k): x for k, x in d["coalition_values_early"].items()}
NAME = dict(st.SOURCE_NAMES, mp_gga_expsynth="MP GGA (ICSD)")
MARK = {"mp_gga": "o", "mp_gga_expsynth": "s", "mp_r2scan": "^", "jarvis_optb88vdw": "o", "jarvis_mbj": "s", "snumat_gga": "o", "snumat_hse": "s"}

fig = plt.figure(figsize=(st.TMLR_FULL, 2.55), layout="none")
gs = fig.add_gridspec(1, 3, left=0.1, right=0.955, top=0.87, bottom=0.19, width_ratios=[1.0, 1.15, 0.7], wspace=0.95)
ax_a, ax_b, ax_c = (fig.add_subplot(gs[0, i]) for i in range(3))

# (a) the copy alone and in pools
SG, SH = bit["snumat_gga"], bit["snumat_hse"]
rng = np.random.default_rng(0)
pools = [S for S in v if S & SG and not S & SH]
xs, ys = [], []
for S in pools:
    n_other = bin(S).count("1") - 1
    xs.append(n_other), ys.append(v[S | SH] - v[S])
xs, ys = np.array(xs), np.array(ys)
alone = xs == 0
ax_a.axhline(0, color=st.INK, lw=0.6)
ax_a.scatter(xs[~alone] + rng.uniform(-0.18, 0.18, (~alone).sum()), ys[~alone], s=12, color=st.SNUMAT_PURPLE, alpha=0.75, lw=0, label="with other databases")
ax_a.scatter(xs[alone], ys[alone], s=26, facecolor="white", edgecolor=st.SNUMAT_PURPLE, lw=1.2, zorder=3, label="SNUMAT GGA alone")
for k in range(1, 6):
    m = ys[xs == k].mean()
    ax_a.plot([k - 0.3, k + 0.3], [m, m], color=st.INK, lw=1.4, solid_capstyle="butt")
n_pos = int((ys[~alone] > 0).sum())
ax_a.text(4.6, 0.08, "%d of %d pools\ngain" % (n_pos, (~alone).sum()), ha="center", va="center", fontsize=6.5, color=st.INK)
ax_a.set_ylim(-0.016, 0.108)
ax_a.set_xticks(range(6))
ax_a.set_xticklabels(["0\nalone"] + [str(k) for k in range(1, 6)])
ax_a.get_xticklabels()[0].set_color(st.SNUMAT_PURPLE)
ax_a.set_xlabel("other databases in the pool")
ax_a.set_ylabel("gain from adding\nSNUMAT HSE06 (Kendall $\\tau$)")
ax_a.set_title("(a) A copy adds nothing alone", loc="left")
ax_a.grid(axis="y", ls="--", lw=0.4, alpha=0.5)

# (b) the same databases under four measures: Shapley (filled), Banzhaf, leave-one-out (open) and Beta(16,1) (diamond)
meas = [("shapley", "Shapley", "o", "full"), ("banzhaf", "Banzhaf", "|", "full"), ("loo", "leave-one-out", "o", "none"), ("beta_16_1", "Beta(16,1)", "D", "full")]
vals = {m: dict(zip(e["players"], e["values"][m])) for m, *_ in meas}
order = sorted(e["players"], key=lambda q: -vals["shapley"][q] + 1e-6 * e["players"].index(q))
ax_b.axvline(0, color=st.INK, lw=0.6)
for i, q in enumerate(order):
    c = st.SOURCE_COLOURS[q]
    xs_ = [vals[m][q] for m, *_ in meas]
    ax_b.plot([min(xs_), max(xs_)], [i, i], color=c, lw=0.8, alpha=0.5)
    for m, lab, mk, fill in meas:
        ax_b.plot(vals[m][q], i, marker=mk, ms=5 if mk != "|" else 7, color=c, mfc=c if fill == "full" else "white", mec=c, mew=1.1, ls="none")
ax_b.set_yticks(range(7))
ax_b.set_yticklabels([NAME[q] for q in order], fontsize=6.8)
for t, q in zip(ax_b.get_yticklabels(), order):
    t.set_color(st.SOURCE_COLOURS[q])
ax_b.set_ylim(6.6, -0.6)
ax_b.set_xlabel(r"contribution (Kendall $\tau$)")
ax_b.set_title("(b) Four measures, one table", loc="left")
ax_b.grid(axis="x", ls="--", lw=0.4, alpha=0.5)
from matplotlib.lines import Line2D  # noqa: E402
hd = [Line2D([], [], marker=mk, ls="none", color=st.INK, mfc=st.INK if fill == "full" else "white", ms=5 if mk != "|" else 7, label=lab) for _, lab, mk, fill in meas]
ax_b.legend(handles=hd, loc="lower right", frameon=False, fontsize=6.3, handletextpad=0.1, borderaxespad=0.1)

# (c) seed-to-seed agreement
cons = e["consistency"]
lab_c = [("banzhaf", "Banzhaf"), ("shapley", "Shapley"), ("loo", "Leave-one-out")]
for i, (m, lab) in enumerate(lab_c):
    mean, mn = cons[m]["mean_pairwise_spearman"], cons[m]["min_pairwise_spearman"]
    ax_c.plot([mn, mean], [i, i], color=st.GREY, lw=1.2)
    ax_c.plot(mn, i, marker="|", ms=7, color=st.GREY)
    ax_c.plot(mean, i, marker="o", ms=5.5, color=st.INK)
    ax_c.text(mean + 0.06, i - 0.2, "%.2f" % mean, fontsize=7, color=st.INK, va="center")
ax_c.set_yticks(range(3))
ax_c.set_yticklabels([lab for _, lab in lab_c])
ax_c.set_ylim(2.6, -0.6)
ax_c.set_xlim(-1.15, 1.15)
ax_c.axvline(0, color=st.INK, lw=0.5)
ax_c.set_xlabel("seed-to-seed Spearman")
ax_c.set_title("(c) Seed agreement", loc="left", x=-0.55)
ax_c.grid(axis="x", ls="--", lw=0.4, alpha=0.5)

OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "redundancy.pdf")
fig.savefig(OUT / "redundancy.png", dpi=300)
print("wrote redundancy; pools", (~alone).sum(), "gain", n_pos, "mean", ys[~alone].mean().round(4), "max", ys.max().round(4))
print({m: {q: round(vals[m][q], 4) for q in order} for m, *_ in meas})
