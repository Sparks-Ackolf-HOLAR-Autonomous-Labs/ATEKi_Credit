"""MGEA figure: who meets whom reorders the contributions (seven-database measured-gap game, early window).
(a) The declared meetings: one per data provider (Materials Project trio, JARVIS pair, SNUMAT pair) and one beyond-GGA meeting
    (JARVIS TB-mBJ, MP r2SCAN, SNUMAT HSE06). Members combine only through a meeting they share.
(b) Contribution of each database with no structure (Shapley) and under the meetings, valued by the sum rule (a separated pool is
    worth the sum of its meeting groups) and by the best-group rule (worth its best group); pairwise links (clique) for comparison.
Data: ateki/results/materials_structure_attribution/materials_structure_attribution.json (conference_primary),
      component_rule/component_rule.json (conference.A).
Output: writings/papers_2026/ateki_mgea/figures/meetings.pdf/.png"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import paper_fig_style as st  # noqa: E402

st.apply_style()
import matplotlib  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Polygon  # noqa: E402

SO = HERE.parents[2]
RES = SO / "ateki" / "results"
OUT = HERE.parent / "ateki_mgea" / "figures"
m = json.loads((RES / "materials_structure_attribution/materials_structure_attribution.json").read_text())["conference_primary"]
cr = json.loads((RES / "component_rule/component_rule.json").read_text())["conference"]["A"]
NAME = dict(st.SOURCE_NAMES, mp_gga_expsynth="MP GGA (ICSD)")
SHORT = {"mp_gga": "GGA", "mp_gga_expsynth": "ICSD", "mp_r2scan": "r$^2$SCAN", "jarvis_optb88vdw": "OptB88", "jarvis_mbj": "TB-mBJ",
         "snumat_gga": "GGA", "snumat_hse": "HSE06"}

fig = plt.figure(figsize=(st.TMLR_FULL, 2.75), layout="none")
ax_a = fig.add_axes([0.0, 0.05, 0.4, 0.83])
ax_b = fig.add_axes([0.6, 0.16, 0.37, 0.72])

# (a) hypergraph of meetings
pos = {"mp_gga": (0.0, 1.25), "mp_gga_expsynth": (0.0, 0.0), "mp_r2scan": (1.25, 0.62),
       "jarvis_mbj": (2.35, 1.35), "jarvis_optb88vdw": (3.45, 1.6), "snumat_hse": (2.35, -0.1), "snumat_gga": (3.45, -0.35)}
fam = lambda q: st.SOURCE_COLOURS[q]  # noqa: E731
edges = m["hyperedges"]
for e in edges:
    pts = np.array([pos[q] for q in e])
    beyond = set(e) == {"jarvis_mbj", "mp_r2scan", "snumat_hse"}
    col = st.INK if beyond else fam(e[0])
    if beyond:
        ax_a.add_patch(Polygon(pts, closed=True, facecolor="none", edgecolor=col, lw=1.0, ls=(0, (3, 2)), joinstyle="round", zorder=1))
    else:
        pale = tuple(0.84 + 0.16 * np.array(matplotlib.colors.to_rgb(col)))
        ax_a.add_patch(Polygon(pts, closed=True, facecolor=pale, edgecolor=pale, lw=24, joinstyle="round", capstyle="round", zorder=0))
for q, (x, y) in pos.items():
    ax_a.scatter(x, y, s=150, color="white", edgecolor=fam(q), lw=1.6, zorder=3)
    ax_a.text(x, y - 0.27 if y < 0.6 else y + 0.25, SHORT[q], ha="center", va="top" if y < 0.6 else "bottom", fontsize=6.8, color=fam(q))
ax_a.text(-0.35, 1.9, "Materials Project", color=st.MP_BLUE, fontsize=7, ha="left")
ax_a.text(2.9, 2.12, "JARVIS", color=st.JARVIS_GREEN, fontsize=7, ha="center")
ax_a.text(2.9, -0.98, "SNUMAT", color=st.SNUMAT_PURPLE, fontsize=7, ha="center", va="top")
ax_a.text(2.6, 0.62, "beyond-GGA\nmeeting", color=st.INK, fontsize=6.3, ha="left", va="center")
ax_a.set_xlim(-0.45, 3.95)
ax_a.set_ylim(-1.3, 2.3)
ax_a.axis("off")
ax_a.set_title("(a) Four declared meetings", loc="left", x=0.02)

# (b) contributions by structure
conds = [("none", m["conditions"]["none"], "no structure", "o", "none"),
         ("hyper_sum", cr["hyper_sum"]["values"] if "values" in cr["hyper_sum"] else cr["hyper_sum"], "meetings, sum rule", "o", "full"),
         ("hyper_max", cr["hyper_max"]["values"] if "values" in cr["hyper_max"] else cr["hyper_max"], "meetings, best-group rule", "s", "full"),
         ("clique_sum", cr["clique_sum"]["values"] if "values" in cr["clique_sum"] else cr["clique_sum"], "pairwise links, sum rule", "x", "full")]
players = list(conds[0][1])
order = sorted(players, key=lambda q: -conds[0][1][q])
ax_b.axvline(0, color=st.INK, lw=0.6)
for i, q in enumerate(order):
    c = fam(q)
    vals = [d[q] for _, d, *_ in conds]
    ax_b.plot([min(vals), max(vals)], [i, i], color=c, lw=0.8, alpha=0.45)
    for key, d, lab, mk, fill in conds:
        ax_b.plot(d[q], i, marker=mk, ms=5.5 if mk != "x" else 5, color=c, mfc=c if fill == "full" else "white", mec=c,
                  mew=1.1, ls="none", zorder=3, alpha=0.6 if key == "clique_sum" else 1)
ax_b.set_yticks(range(len(order)))
ax_b.set_yticklabels([NAME[q] for q in order], fontsize=6.8)
for t, q in zip(ax_b.get_yticklabels(), order):
    t.set_color(fam(q))
ax_b.set_ylim(len(order) - 0.4, -0.6)
ax_b.set_xlabel(r"contribution (Kendall $\tau$)")
ax_b.grid(axis="x", ls="--", lw=0.4, alpha=0.5)
ax_b.set_title("(b) Meetings split a tie", loc="left")
hd = [Line2D([], [], marker=mk, ls="none", color=st.INK, mfc=st.INK if fill == "full" else "white", ms=5, label=lab)
      for _, _, lab, mk, fill in conds]
ax_b.legend(handles=hd, loc="lower right", frameon=False, fontsize=6.3, handletextpad=0.2, borderaxespad=0.1)

OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "meetings.pdf")
fig.savefig(OUT / "meetings.png", dpi=300)
print("wrote meetings")
for key, d, *_ in conds:
    print(key, {q: round(d[q], 4) for q in order})
