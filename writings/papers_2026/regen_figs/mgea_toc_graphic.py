"""MGEA table-of-contents graphic: all 128 measured campaigns of the seven-database game, by how many databases advise them, with the
best pool of each size climbing to three databases and falling to all seven. Square, 300 dpi.
Data: ateki/results/database_attribution/expt_zhuo/database_attribution.json (early-window values, 10 seeds per subset).
Output: writings/papers_2026/ateki_mgea/figures/toc_graphic.{png,pdf}."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
SO = HERE.parents[2]
d = json.loads((SO / "ateki/results/database_attribution/expt_zhuo/database_attribution.json").read_text(encoding="utf-8"))
v = {int(k): x for k, x in d["coalition_values_early"].items()}
OUT = HERE.parent / "ateki_mgea" / "figures"

INK, GREY, GOLD, GOOD, BAD = "#222222", "#9A9A9A", "#D4A017", "#2E8B57", "#C0392B"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(figsize=(3.3, 3.3))
rng = np.random.default_rng(2)
size = {S: bin(S).count("1") for S in v}
xs = np.array([size[S] + (rng.uniform(-0.25, 0.25) if 0 < size[S] < 7 else 0) for S in v])
ax.scatter(xs, list(v.values()), s=9, color=GREY, alpha=0.7, lw=0)
best = [max(x for S, x in v.items() if size[S] == k) for k in range(8)]
ax.plot(range(8), best, color=GOLD, lw=2.2, marker="o", ms=4.5, zorder=3)
ax.axhline(v[0], color=GREY, lw=0.8, ls="--")
ax.annotate("best three\n%.3f" % best[3], (3, best[3]), xytext=(3.25, best[3] + 0.018), color=GOOD, fontsize=9, ha="left")
ax.annotate("all seven\n%.3f" % best[7], (7, best[7]), xytext=(7.25, best[7] - 0.012), color=BAD, fontsize=9, ha="right", va="top")
ax.text(0.2, v[0] - 0.008, "no advice", color=GREY, fontsize=7.5, ha="left", va="top")
ax.set_xticks(range(8))
ax.set_xlim(-0.4, 7.4)
ax.set_ylim(0.6, 0.92)
ax.set_xlabel("databases advising the campaign")
ax.set_ylabel("early ranking quality (Kendall $\\tau$)")
ax.set_title("128 run campaigns: more stored\nknowledge is not a better campaign", fontsize=9.5, color=INK)
fig.tight_layout()
OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "toc_graphic.png", dpi=300)
fig.savefig(OUT / "toc_graphic.pdf")
print("wrote", OUT / "toc_graphic.png")
