"""
Experiment 06: Shapley attribution of a physics prior as a PLAYER.

ATEKi's answer to "what is the physics-informed part actually worth?"
PEGKi injects a relative physics prior (a donor
channel's class ordering) into the Plackett-Luce fit; TENKi exp 25 shows
the budget curves. Here the prior itself joins the coalition game:

  players : physics_prior  (the donor-channel relative prior, no cost)
            pair_events    (budget/2 evaluations spent on random pairs)
            kway_events    (budget/2 evaluations spent on random 4-way events)

  v(S)    : Kendall tau between the reference ranking and the ranking
            obtained using ONLY the components in S --
              data only     -> unanchored PL fit on those events
              prior only    -> the prior ordering itself
              prior + data  -> anchored MAP fit (fixed lambda)
              empty         -> 0

Exact 3-player Shapley (ShapleyEngine) at each budget checkpoint, mean over
channels and seeds. The physics share phi_prior / v(N) quantifies how much
of the achieved ranking quality is attributable to imported cross-system
knowledge rather than purchased evaluations -- and how that share decays as
data accumulates. Also reported: the prior's evaluations-equivalent (the
budget at which data alone matches v({prior})).

Data: fixed band-gap archive universe, same retrospective querying and
class construction as TENKi exps 24/25 (no invented observations).

Usage (from ateki/):
    uv run python experiments/06_physics_prior_attribution.py
    uv run python experiments/06_physics_prior_attribution.py --self-test
Outputs: results/physics_attribution/06_physics_prior_attribution.{json,md,png}
ASCII only; seeded and reproducible (--seed).
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
_SHARED = Path(os.environ.get(
    "PEGKI_ROOT", Path(__file__).resolve().parents[2] / "shared")).resolve()
sys.path.insert(1, str(_SHARED))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from analysis.shapley import ShapleyEngine
from src.rating.hypergraph_rating import (
    PlackettLuceModel,
    hyperedge_from_scores,
    _kendall_tau,
)

# Mirrors classify_by_anion and TENKi exps 24/25 exactly.
ANION_PRIORITY = [
    ("halide", {"F", "Cl", "Br", "I"}),
    ("oxide", {"O"}),
    ("nitride", {"N"}),
    ("chalcogenide", {"S", "Se", "Te"}),
    ("carbide", {"C"}),
    ("boride", {"B"}),
    ("pnictide", {"P", "As", "Sb", "Bi"}),
]
MIN_GAP_EV = 0.01
PLAYERS = ["kway_events", "pair_events", "physics_prior"]


def classify_formula(formula: str) -> str:
    species = set(re.findall(r"[A-Z][a-z]?", formula))
    for name, elems in ANION_PRIORITY:
        if species & elems:
            return name
    return "other"


def load_universe(path: Path, min_class_size: int):
    per_channel: dict = {}
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            formula = (rec.get("x") or {}).get("formula")
            gap = (rec.get("y") or {}).get("bandgap_eV")
            channel = rec.get("s")
            if not formula or gap is None or channel is None:
                continue
            gap = float(gap)
            if gap <= MIN_GAP_EV:
                continue
            cls = classify_formula(formula)
            per_channel.setdefault(channel, {}).setdefault(cls, []).append(gap)
    out = {}
    for channel, classes in per_channel.items():
        kept = {c: np.asarray(sorted(v), dtype=float)
                for c, v in classes.items() if len(v) >= min_class_size}
        if len(kept) >= 4:
            out[channel] = kept
    return out


def reference_ranking(classes: dict) -> list:
    med = {c: float(np.median(v)) for c, v in classes.items()}
    return sorted(med, key=lambda c: (-med[c], c))


def donor_prior(receiver_classes: dict, donor_classes: dict) -> dict:
    donor_rank = reference_ranking(donor_classes)
    shared = [c for c in donor_rank if c in receiver_classes]
    prior = {c: 0.0 for c in receiver_classes}
    if len(shared) >= 2:
        for pos, c in enumerate(shared):
            prior[c] = float(1.0 - 2.0 * pos / (len(shared) - 1))
    return prior


def pick_donor(channel: str, per_channel: dict) -> str:
    sizes = {ch: sum(len(v) for v in cls.values())
             for ch, cls in per_channel.items() if ch != channel}
    return max(sorted(sizes), key=lambda ch: sizes[ch])


def generate_events(classes: dict, k: int, budget: int,
                    rng: np.random.Generator) -> list:
    """Random k-subsets, one real archived value per participant, until the
    evaluation budget is spent."""
    names = sorted(classes)
    edges, spent = [], 0
    while spent + k <= budget:
        subset = list(rng.choice(names, size=k, replace=False))
        scores = {c: float(classes[c][rng.integers(0, len(classes[c]))])
                  for c in subset}
        e = hyperedge_from_scores(scores, higher_is_better=True)
        spent += k
        if e is not None:
            edges.append(e)
    return edges


def make_value_fn(classes: dict, prior: dict, pair_edges: list,
                  kway_edges: list, lam: float):
    """v(S) for S subset of PLAYERS; memoized (8 coalitions)."""
    ref = reference_ranking(classes)
    prior_rank = sorted(prior, key=lambda c: (-prior[c], c))
    cache = {}

    def v(S) -> float:
        key = frozenset(S)
        if key in cache:
            return cache[key]
        edges = []
        if "pair_events" in key:
            edges += pair_edges
        if "kway_events" in key:
            edges += kway_edges
        has_prior = "physics_prior" in key
        if edges:
            model = PlackettLuceModel(prior_weight=lam if has_prior else 0.01)
            model.fit(edges, prior_log_strengths=prior if has_prior else None)
            val = _kendall_tau(model.ranking(), ref)
        elif has_prior:
            val = _kendall_tau(prior_rank, ref)
        else:
            val = 0.0
        cache[key] = float(val)
        return cache[key]

    return v


def self_test() -> int:
    """Efficiency axiom + null player on a synthetic coalition game."""
    failures = 0
    rng = np.random.default_rng(3)
    classes = {c: np.sort(rng.normal(mu, 0.3, size=60)).astype(float)
               for c, mu in [("w", 4.0), ("x", 3.0), ("y", 2.0), ("z", 1.0)]}
    prior = {"w": 1.0, "x": 0.33, "y": -0.33, "z": -1.0}
    pair = generate_events(classes, 2, 24, np.random.default_rng(11))
    kway = generate_events(classes, 4, 24, np.random.default_rng(12))
    v = make_value_fn(classes, prior, pair, kway, lam=4.0)
    res = ShapleyEngine(PLAYERS, v).exact()
    total = sum(res.scores.values())
    grand = v(frozenset(PLAYERS))
    ok = abs(total - grand) < 1e-9
    print(f"[{'PASS' if ok else 'FAIL'}] efficiency: sum phi = {total:.6f}, "
          f"v(N) = {grand:.6f}")
    failures += 0 if ok else 1
    # Null player: an empty event list contributes exactly zero
    v2 = make_value_fn(classes, prior, pair, [], lam=4.0)
    res2 = ShapleyEngine(PLAYERS, v2).exact()
    ok = abs(res2.scores["kway_events"]) < 1e-9
    print(f"[{'PASS' if ok else 'FAIL'}] null player: phi(kway with no "
          f"events) = {res2.scores['kway_events']:.2e}")
    failures += 0 if ok else 1
    return failures


def main():
    ap = argparse.ArgumentParser(
        description="ATEKi exp 06: physics prior as a Shapley player")
    ap.add_argument("--universe",
                    default=str(_SHARED / "output" / "bandgap_archive_build" /
                                "bandgap_universe.jsonl"))
    ap.add_argument("--budgets", type=int, nargs="+",
                    default=[16, 48, 96, 192])
    ap.add_argument("--kway", type=int, default=4)
    ap.add_argument("--lam", type=float, default=4.0)
    ap.add_argument("--n-seeds", type=int, default=10)
    ap.add_argument("--min-class-size", type=int, default=30)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--output-dir", default=None)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    universe = Path(args.universe)
    if not universe.exists():
        print(f"[error] universe not found: {universe}; "
              "run compute/bandgap_archive/build_inventory.py first")
        return 1
    out_dir = Path(args.output_dir) if args.output_dir else (
        Path(__file__).resolve().parents[1] / "results" /
        "physics_attribution")
    out_dir.mkdir(parents=True, exist_ok=True)

    per_channel = load_universe(universe, args.min_class_size)
    print(f"[load] {len(per_channel)} channels")
    if not per_channel:
        return 1

    # phi[player][budget] -> list over (channel, seed)
    phi = {p: {b: [] for b in args.budgets} for p in PLAYERS}
    grand = {b: [] for b in args.budgets}
    prior_only = []
    data_only = {b: [] for b in args.budgets}
    for channel in sorted(per_channel):
        classes = per_channel[channel]
        donor = pick_donor(channel, per_channel)
        prior = donor_prior(classes, per_channel[donor])
        for s in range(args.n_seeds):
            for b in args.budgets:
                rng_p = np.random.default_rng(args.seed + 1000 * s + b)
                rng_k = np.random.default_rng(args.seed + 1000 * s + b + 7)
                pair = generate_events(classes, 2, b // 2, rng_p)
                kway = generate_events(classes, args.kway, b // 2, rng_k)
                v = make_value_fn(classes, prior, pair, kway, args.lam)
                res = ShapleyEngine(PLAYERS, v).exact()
                for p in PLAYERS:
                    phi[p][b].append(res.scores[p])
                grand[b].append(v(frozenset(PLAYERS)))
                data_only[b].append(
                    v(frozenset(["pair_events", "kway_events"])))
            prior_only.append(v(frozenset(["physics_prior"])))
        print(f"[done] {channel} (donor={donor})")

    mean_phi = {p: [float(np.mean(phi[p][b])) for b in args.budgets]
                for p in PLAYERS}
    mean_grand = [float(np.mean(grand[b])) for b in args.budgets]
    mean_data = [float(np.mean(data_only[b])) for b in args.budgets]
    v_prior = float(np.mean(prior_only))
    share = [mean_phi["physics_prior"][i] / mean_grand[i]
             if mean_grand[i] > 0 else 0.0
             for i in range(len(args.budgets))]

    # Evaluations-equivalent of the prior: budget where data alone matches
    # the prior-only tau
    eval_equiv = None
    for i, b in enumerate(args.budgets):
        if mean_data[i] >= v_prior:
            eval_equiv = b
            break

    results = {
        "config": {k: v_ for k, v_ in vars(args).items() if k != "self_test"},
        "players": PLAYERS,
        "budgets": args.budgets,
        "mean_phi": mean_phi,
        "mean_grand_value": mean_grand,
        "mean_data_only_value": mean_data,
        "prior_only_value": v_prior,
        "physics_share_of_grand": share,
        "prior_evaluations_equivalent": eval_equiv,
    }
    with open(out_dir / "06_physics_prior_attribution.json", "w",
              encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.3))
    colors = {"physics_prior": "tab:green", "pair_events": "tab:gray",
              "kway_events": "tab:blue"}
    for p in PLAYERS:
        axes[0].plot(args.budgets, mean_phi[p], "o-", color=colors[p],
                     label=p)
    axes[0].set_xlabel("evaluation budget (split pair/kway)")
    axes[0].set_ylabel("Shapley value phi (tau units)")
    axes[0].set_title("Attribution of ranking quality")
    axes[0].legend(fontsize=8)
    axes[0].grid(alpha=0.3)
    axes[1].plot(args.budgets, share, "o-", color="tab:green")
    axes[1].set_xlabel("evaluation budget")
    axes[1].set_ylabel("phi_prior / v(grand)")
    axes[1].set_title("Physics share of the outcome")
    axes[1].grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_dir / "06_physics_prior_attribution.png", dpi=150)
    plt.close(fig)

    lines = [
        "# Experiment 06: the physics prior as a Shapley player",
        "",
        f"Players: {', '.join(PLAYERS)}. Exact 3-player Shapley, "
        f"lambda = {args.lam}, {args.n_seeds} seeds x "
        f"{len(per_channel)} channels.",
        "",
        "| budget | phi(physics_prior) | phi(pair_events) | "
        "phi(kway_events) | v(grand) | physics share |",
        "|---|---|---|---|---|---|",
    ]
    for i, b in enumerate(args.budgets):
        lines.append(
            f"| {b} | {mean_phi['physics_prior'][i]:+.4f} | "
            f"{mean_phi['pair_events'][i]:+.4f} | "
            f"{mean_phi['kway_events'][i]:+.4f} | "
            f"{mean_grand[i]:+.4f} | {100 * share[i]:.1f}% |")
    lines += [
        "",
        f"Prior-only value (tau of the donor ordering alone): "
        f"{v_prior:+.4f}.",
        f"Evaluations-equivalent of the prior: "
        f"{'>' + str(args.budgets[-1]) if eval_equiv is None else eval_equiv}"
        f" evaluations (budget at which data alone matches the prior).",
        "",
        "Efficiency holds exactly (sum phi = v(grand)); see --self-test.",
        "Same frozen-universe retrospective querying as TENKi exps 24/25.",
    ]
    with open(out_dir / "06_physics_prior_attribution.md", "w",
              encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"[save] {out_dir}")
    print("physics share by budget: " +
          ", ".join(f"{b}:{100 * s_:.1f}%"
                    for b, s_ in zip(args.budgets, share)))
    print(f"prior evaluations-equivalent: {eval_equiv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
