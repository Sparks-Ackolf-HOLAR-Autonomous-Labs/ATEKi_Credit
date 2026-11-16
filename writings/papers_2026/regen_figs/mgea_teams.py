"""MGEA figure: a coordinator raises the team, not itself (language-model agent teams on the band-gap campaign).
(a) Team ranking quality of every recorded campaign, flat team (open) against the same agents with a coordinator (filled), in three
    agent sets; bars, means; dashed, random trays at the same budget.
(b) Effect of the coordinator on team tau in each set and on a finer task (13 anion-element groups, coordinator role rotated over
    the five databases), and the coordinator's own role premium; 95% percentile bootstrap intervals.
Data: ateki/results/recorded_meetings_scale/scale_summary.json; finer-task and role-premium points from ateki/results/recorded_meetings_4b/summary_4b.json, their seed-level intervals from seed_boot_4b.json
      (Section on agent teams).
Output: writings/papers_2026/ateki_mgea/figures/teams.pdf/.png"""
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
s = json.loads((RES / "recorded_meetings_scale/scale_summary.json").read_text())["sets"]
LAB = {"S1": "Qwen3-4B\n5 agents", "S2": "Nemotron 30B\n5 agents", "S3": "Qwen3-4B\n10 agents"}
FLAT, COORD = st.GREY, st.MP_BLUE

fig = plt.figure(figsize=(st.TMLR_FULL, 2.6), layout="none")
ax_a = fig.add_axes([0.085, 0.2, 0.44, 0.68])
ax_b = fig.add_axes([0.72, 0.2, 0.265, 0.68])

# (a) every campaign, flat against coordinated
rng = np.random.default_rng(1)
for i, k in enumerate(["S1", "S2", "S3"]):
    for dx, arm, col, fill in [(-0.17, "flat", FLAT, "white"), (0.17, "orchestrated", COORD, COORD)]:
        y = np.array(s[k][arm]["team_tau"])
        ax_a.scatter(i + dx + rng.uniform(-0.07, 0.07, len(y)), y, s=11, facecolor=fill, edgecolor=col, lw=0.8, alpha=0.8, zorder=2)
        ax_a.plot([i + dx - 0.12, i + dx + 0.12], [y.mean()] * 2, color=col if arm == "orchestrated" else st.INK, lw=1.8, zorder=3)
    r = s[k]["random_trays_same_budget"]["mean"]
    ax_a.plot([i - 0.38, i + 0.38], [r, r], color=st.ACCENT_RED, ls="--", lw=0.9, zorder=1)
ax_a.text(2.42, s["S3"]["random_trays_same_budget"]["mean"], "random\ntrays", color=st.ACCENT_RED, fontsize=6.5, va="center", ha="left")
ax_a.text(-0.08, 1.04, "flat", color=st.INK, fontsize=6.8, ha="right", va="bottom")
ax_a.text(0.06, 1.04, "with\ncoordinator", color=COORD, fontsize=6.8, ha="left", va="bottom")
ax_a.set_xticks(range(3))
ax_a.set_xticklabels([LAB[k] for k in ["S1", "S2", "S3"]], fontsize=6.8)
ax_a.set_xlim(-0.5, 2.75)
ax_a.set_ylim(0.38, 1.16)
ax_a.set_yticks([0.4, 0.6, 0.8, 1.0])
ax_a.set_ylabel(r"team ranking quality ($\tau$)")
ax_a.grid(axis="y", ls="--", lw=0.4, alpha=0.5)
ax_a.set_title("(a) Every recorded campaign", loc="left")

# (b) effects with intervals
F4B = json.loads((RES / "recorded_meetings_4b" / "summary_4b.json").read_text(encoding="utf-8"))
SP = json.loads((RES / "recorded_meetings_scale" / "scale_paired.json").read_text(encoding="utf-8"))["sets"]  # rows 1-3: paired-by-seed intervals
SB4 = json.loads((RES / "recorded_meetings_4b" / "seed_boot_4b.json").read_text(encoding="utf-8"))  # seed-level intervals
rows = [("Qwen3-4B, 5", SP["S1"]["coord_minus_flat"]["mean"], SP["S1"]["coord_minus_flat"]["ci95"], COORD),
        ("Nemotron, 5", SP["S2"]["coord_minus_flat"]["mean"], SP["S2"]["coord_minus_flat"]["ci95"], COORD),
        ("Qwen3-4B, 10", SP["S3"]["coord_minus_flat"]["mean"], SP["S3"]["coord_minus_flat"]["ci95"], COORD),
        ("finer task,\nrotated role", F4B["coordinator_effect"]["pooled_mean"], SB4["coordinator_effect"]["seed_ci95"], COORD),
        ("coordinator's\nown premium", F4B["role_premium"]["mean"]["pooled_mean"], SB4["role_premium_mean"]["seed_ci95"], st.GREY)]
ax_b.axvline(0, color=st.INK, lw=0.6)
for i, (lab, mu, ci, col) in enumerate(rows):
    ax_b.plot(ci, [i, i], color=col, lw=1.6, solid_capstyle="butt")
    ax_b.plot(mu, i, marker="o", ms=5.5, color=col, mfc=col if ci[0] > 0 else "white", mew=1.3)
    ax_b.text(ci[1] + 0.012, i, "%+.3f" % mu, fontsize=6.5, color=col, va="center")
ax_b.set_yticks(range(len(rows)))
ax_b.set_yticklabels([r[0] for r in rows], fontsize=6.6)
ax_b.set_ylim(len(rows) - 0.4, -0.6)
ax_b.set_xlim(-0.06, 0.33)
ax_b.set_xlabel(r"change in team $\tau$")
ax_b.grid(axis="x", ls="--", lw=0.4, alpha=0.5)
ax_b.set_title("(b) Coordination value", loc="left")

OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "teams.pdf")
fig.savefig(OUT / "teams.png", dpi=300)
print("wrote teams", {k: (round(s[k]["flat"]["team_tau_mean"], 3), round(s[k]["orchestrated"]["team_tau_mean"], 3)) for k in s})
