"""
Experiment 07: attribution over the paired campaign arms (exp 26 logs).

Attributes each receiver's campaign outcome across the factors that produced it, using
ONLY measured curves from TENKi experiment 26 (paired cold/full/selective
protocol on the fixed band-gap archive universe). Nothing is simulated here; the
characteristic function is a lookup into committed campaign logs.

Players (main game, per ordered donor->receiver cell):
  cold_data      D : the purchased query stream itself (veto player: no
                     campaign exists without it, v(S)=0 if D not in S)
  donor_prior    P : the donor channel's ordinal class prior
  adaptive_trust T : prequentially learned trust in that prior (inert
                     without P: T alone changes nothing)
  kway_events    K : k-way ranking events instead of pairwise queries

Coalition -> measured exp 26 arm:
  arm       = kway if K in S else pair
  condition = selective if {P,T} <= S else (full if P in S else cold)
  v(S)      = mean tau over the early window (first 5 of 10 checkpoints)
              of that arm's curve for this (donor, receiver, seed);
              v(S) = 0 if D not in S.  Final-tau game reported alongside.

Exact 4-player Shapley (ShapleyEngine), Banzhaf, and leave-one-out per
cell and seed; means with bootstrap CIs over seeds. Shapley is linear in
v, so the mean per-seed Shapley equals the Shapley of the seed-averaged
game (checked in --self-test). Secondary 3-player game (D, pooled_prior,
K) uses the combined|arm curves. The negative-contributor case study
reports the cells with the most negative donor_prior share.

Usage (from ateki/):
    uv run python experiments/07_campaign_attribution.py \
        --checkpoints-dir <exp26 checkpoints dir> --label k4_50seed
    uv run python experiments/07_campaign_attribution.py --self-test
Outputs: results/campaign_attribution/<label>/07_campaign_attribution.{json,md,png}
ASCII only; deterministic given the input logs (--boot-seed for CIs).
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from analysis.shapley import ShapleyEngine, BanzhafEngine

PLAYERS = ["cold_data", "donor_prior", "adaptive_trust", "kway_events"]
POOLED_PLAYERS = ["cold_data", "pooled_prior", "kway_events"]
EARLY_N = 5


def coalition_curve_key(S: frozenset, donor: str) -> str | None:
    """Map a coalition to the exp 26 curve key it corresponds to."""
    if "cold_data" not in S:
        return None
    arm = "kway" if "kway_events" in S else "pair"
    if "donor_prior" not in S:
        return "cold|" + arm
    cond = "selective" if "adaptive_trust" in S else "full"
    return cond + "|" + arm + "|" + donor


def pooled_curve_key(S: frozenset) -> str | None:
    if "cold_data" not in S:
        return None
    arm = "kway" if "kway_events" in S else "pair"
    if "pooled_prior" not in S:
        return "cold|" + arm
    return "combined|" + arm + "|__combined__"


def value_from_curves(curves: dict, key: str | None, window: str) -> float:
    if key is None:
        return 0.0
    c = curves[key]
    return float(np.mean(c[:EARLY_N])) if window == "early" else float(c[-1])


def attribute_cell(curves: dict, donor: str, window: str) -> dict:
    """Exact Shapley, Banzhaf, LOO for one (donor, receiver, seed) cell."""
    def v(S: frozenset) -> float:
        return value_from_curves(curves, coalition_curve_key(S, donor), window)

    shap = ShapleyEngine(PLAYERS, v).exact().scores
    banz = BanzhafEngine(PLAYERS, v).exact().scores
    grand = frozenset(PLAYERS)
    loo = {p: v(grand) - v(grand - {p}) for p in PLAYERS}
    return {"shapley": shap, "banzhaf": banz, "loo": loo, "v_grand": v(grand)}


def attribute_pooled(curves: dict, window: str) -> dict:
    def v(S: frozenset) -> float:
        return value_from_curves(curves, pooled_curve_key(S), window)

    shap = ShapleyEngine(POOLED_PLAYERS, v).exact().scores
    return {"shapley": shap, "v_grand": v(frozenset(POOLED_PLAYERS))}


def bootstrap_ci(samples: np.ndarray, n_boot: int, rng: np.random.Generator):
    if len(samples) < 2:
        return [float(samples[0]), float(samples[0])]
    idx = rng.integers(0, len(samples), size=(n_boot, len(samples)))
    means = samples[idx].mean(axis=1)
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


def load_checkpoints(ckpt_dir: Path) -> dict:
    """-> {receiver: {seed: curves}}; curves maps arm key -> list of tau."""
    out: dict = {}
    for f in sorted(ckpt_dir.glob("*.json")):
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        out.setdefault(d["receiver"], {})[d["seed"]] = d["curves"]
    if not out:
        raise SystemExit("no checkpoint files in " + str(ckpt_dir))
    return out


def donors_of(curves: dict) -> list[str]:
    return sorted({k.split("|", 2)[2] for k in curves
                   if k.count("|") == 2
                   and k.split("|", 2)[2] != "__combined__"})


def run(args) -> dict:
    data = load_checkpoints(Path(args.checkpoints_dir))
    rng = np.random.default_rng(args.boot_seed)
    receivers = sorted(data)
    result: dict = {
        "experiment": "07_campaign_attribution",
        "players": PLAYERS,
        "checkpoints_dir": str(args.checkpoints_dir),
        "label": args.label,
        "early_window_checkpoints": EARLY_N,
        "windows": {},
        "pooled_game": {},
        "negative_prior_cells": [],
    }

    # Separate generator for the cell-mean interval, so the per-cell CIs
    # above keep their original random stream.
    rng_cm = np.random.default_rng(args.boot_seed + 1)
    for window in ("early", "final"):
        per_cell: dict = {}
        agg: dict = {p: [] for p in PLAYERS}
        by_seed: dict = {p: {} for p in PLAYERS}  # seed -> list over cells
        for recv in receivers:
            for donor in donors_of(next(iter(data[recv].values()))):
                cell_scores = {m: {p: [] for p in PLAYERS}
                               for m in ("shapley", "banzhaf", "loo")}
                grands = []
                for seed, curves in data[recv].items():
                    cell = attribute_cell(curves, donor, window)
                    grands.append(cell["v_grand"])
                    for m in cell_scores:
                        for p in PLAYERS:
                            cell_scores[m][p].append(cell[m][p])
                    for p in PLAYERS:
                        by_seed[p].setdefault(seed, []).append(
                            cell["shapley"][p])
                entry = {"n_seeds": len(grands),
                         "v_grand_mean": float(np.mean(grands))}
                for m in cell_scores:
                    entry[m] = {}
                    for p in PLAYERS:
                        s = np.asarray(cell_scores[m][p])
                        entry[m][p] = {"mean": float(s.mean()),
                                       "ci": bootstrap_ci(s, args.n_boot, rng)}
                per_cell[donor + "->" + recv] = entry
                for p in PLAYERS:
                    agg[p].append(entry["shapley"][p]["mean"])
        # 90% interval of the cell mean: per seed, average over the cells
        # that ran that seed; percentile bootstrap over seeds.
        cm_ci = {}
        for p in PLAYERS:
            s = np.asarray([np.mean(v) for _, v in sorted(by_seed[p].items())])
            idx = rng_cm.integers(0, len(s), size=(args.n_boot, len(s)))
            bm = s[idx].mean(axis=1)
            cm_ci[p] = [float(np.percentile(bm, 5)), float(np.percentile(bm, 95))]
        result["windows"][window] = {
            "per_cell": per_cell,
            "mean_shapley": {p: float(np.mean(agg[p])) for p in PLAYERS},
            "mean_shapley_ci90_over_seeds": cm_ci,
            "n_seed_ids": len(by_seed[PLAYERS[0]]),
            "frac_cells_prior_positive": float(np.mean(
                [c["shapley"]["donor_prior"]["mean"] > 0
                 for c in per_cell.values()])),
        }

    # Pooled 3-player game (combined reuse); one cell per receiver.
    for window in ("early", "final"):
        pooled = {}
        for recv in receivers:
            vals = {p: [] for p in POOLED_PLAYERS}
            for seed, curves in data[recv].items():
                sc = attribute_pooled(curves, window)["shapley"]
                for p in POOLED_PLAYERS:
                    vals[p].append(sc[p])
            pooled[recv] = {p: {"mean": float(np.mean(vals[p])),
                                "ci": bootstrap_ci(np.asarray(vals[p]),
                                                   args.n_boot, rng)}
                            for p in POOLED_PLAYERS}
        result["pooled_game"][window] = pooled

    # Negative-contributor case study (early window, per-channel prior).
    cells = result["windows"]["early"]["per_cell"]
    neg = sorted(cells.items(),
                 key=lambda kv: kv[1]["shapley"]["donor_prior"]["mean"])[:5]
    result["negative_prior_cells"] = [
        {"cell": k,
         "prior_shapley": v["shapley"]["donor_prior"]["mean"],
         "prior_ci": v["shapley"]["donor_prior"]["ci"],
         "trust_shapley": v["shapley"]["adaptive_trust"]["mean"],
         "v_grand": v["v_grand_mean"]}
        for k, v in neg]
    return result


def write_outputs(result: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "07_campaign_attribution.json", "w",
              encoding="utf-8") as fh:
        json.dump(result, fh, indent=1, sort_keys=True)

    lines = ["# Experiment 07: attribution over paired campaign arms", ""]
    lines.append("Substrate: `%s` (label: %s). Value = measured exp 26 tau; "
                 "no simulation." % (result["checkpoints_dir"],
                                     result["label"]))
    lines.append("")
    for window in ("early", "final"):
        w = result["windows"][window]
        lines.append("## %s-window game (exact 4-player Shapley, "
                     "mean over all donor->receiver cells)" % window)
        lines.append("")
        lines.append("| player | mean Shapley |")
        lines.append("|---|---|")
        for p in PLAYERS:
            lines.append("| %s | %+0.4f |" % (p, w["mean_shapley"][p]))
        lines.append("")
        lines.append("donor_prior share positive in %.0f%% of cells." %
                     (100 * w["frac_cells_prior_positive"]))
        lines.append("")
    lines.append("## Pooled-prior game (early window, per receiver)")
    lines.append("")
    lines.append("| receiver | cold_data | pooled_prior | kway_events |")
    lines.append("|---|---|---|---|")
    for recv, sc in sorted(result["pooled_game"]["early"].items()):
        lines.append("| %s | %+0.4f | %+0.4f | %+0.4f |" % (
            recv, sc["cold_data"]["mean"], sc["pooled_prior"]["mean"],
            sc["kway_events"]["mean"]))
    lines.append("")
    lines.append("## Most negative donor_prior cells (early window)")
    lines.append("")
    lines.append("| cell | prior Shapley [95% CI] | adaptive_trust Shapley |")
    lines.append("|---|---|---|")
    for c in result["negative_prior_cells"]:
        lines.append("| %s | %+0.4f [%+0.4f, %+0.4f] | %+0.4f |" % (
            c["cell"], c["prior_shapley"], c["prior_ci"][0],
            c["prior_ci"][1], c["trust_shapley"]))
    lines.append("")
    with open(out_dir / "07_campaign_attribution.md", "w",
              encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
    for ax, window in zip(axes[:2], ("early", "final")):
        w = result["windows"][window]
        vals = [w["mean_shapley"][p] for p in PLAYERS]
        ax.bar(range(len(PLAYERS)), vals, color="#4878a8")
        ax.set_xticks(range(len(PLAYERS)))
        ax.set_xticklabels(PLAYERS, rotation=20, ha="right", fontsize=8)
        ax.axhline(0, color="k", lw=0.5)
        ax.set_title("%s window: mean Shapley" % window)
        ax.set_ylabel("Shapley value (tau units)")
    ax = axes[2]
    cells = result["windows"]["early"]["per_cell"]
    pr = [c["shapley"]["donor_prior"]["mean"] for c in cells.values()]
    ax.hist(pr, bins=24, color="#4878a8")
    ax.axvline(0, color="k", lw=0.8)
    ax.set_title("donor_prior Shapley across %d cells (early)" % len(pr))
    ax.set_xlabel("Shapley value")
    fig.tight_layout()
    fig.savefig(out_dir / "07_campaign_attribution.png", dpi=150)
    plt.close(fig)


def self_test() -> int:
    """Synthetic curves with known structure; checks signs + linearity."""
    curves = {
        "cold|pair": [0.30] * 10, "cold|kway": [0.40] * 10,
        "full|pair|d": [0.50] * 10, "full|kway|d": [0.55] * 10,
        "selective|pair|d": [0.52] * 10, "selective|kway|d": [0.58] * 10,
        "combined|pair": [0.45] * 10, "combined|kway": [0.50] * 10,
    }
    cell = attribute_cell(curves, "d", "early")
    ok = True
    # Efficiency: Shapley sums to v(grand).
    ok &= abs(sum(cell["shapley"].values()) - 0.58) < 1e-9
    # Signs: every factor helps in this construction.
    ok &= all(cell["shapley"][p] > 0 for p in PLAYERS)
    # Veto player: cold_data gets the largest share.
    ok &= cell["shapley"]["cold_data"] == max(cell["shapley"].values())
    # Linearity: Shapley of averaged game == average of per-seed Shapley.
    curves2 = {k: [x + 0.1 for x in v] for k, v in curves.items()}
    mean_curves = {k: [(a + b) / 2 for a, b in zip(curves[k], curves2[k])]
                   for k in curves}
    s_mean = attribute_cell(mean_curves, "d", "early")["shapley"]
    s_avg = {p: (cell["shapley"][p] +
                 attribute_cell(curves2, "d", "early")["shapley"][p]) / 2
             for p in PLAYERS}
    ok &= all(abs(s_mean[p] - s_avg[p]) < 1e-9 for p in PLAYERS)
    # Inert trust without prior: dropping T from {D,K} changes nothing.
    ok &= coalition_curve_key(frozenset({"cold_data", "kway_events",
                                         "adaptive_trust"}), "d") == \
        coalition_curve_key(frozenset({"cold_data", "kway_events"}), "d")
    print("self-test: %s" % ("PASS (5/5)" if ok else "FAIL"))
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoints-dir", default=None)
    ap.add_argument("--label", default="local")
    ap.add_argument("--output-dir", default=None)
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--boot-seed", type=int, default=42)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.checkpoints_dir is None:
        ap.error("--checkpoints-dir is required (exp 26 checkpoints)")
    result = run(args)
    out_dir = Path(args.output_dir) if args.output_dir else (
        Path(__file__).resolve().parents[1] / "results" /
        "campaign_attribution" / args.label)
    write_outputs(result, out_dir)
    print("saved: %s" % out_dir)
    for p in PLAYERS:
        print("  %-15s early %+0.4f  final %+0.4f" % (
            p, result["windows"]["early"]["mean_shapley"][p],
            result["windows"]["final"]["mean_shapley"][p]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
