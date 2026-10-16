"""
Experiment 08: which database earns the credit? Exact 7-player
attribution with Monte-Carlo validation.

The recorded ATEKi limit says exact attribution is feasible only for a
handful of contributors, with sampling approximations beyond. This
experiment (a) scales the measured-coalition game of experiment 07 to
SEVEN players (the seven donor channels advising one receiver campaign
on the fixed band-gap archive universe), computing the EXACT Shapley value from
2^7 = 128 measured coalition campaigns, and (b) validates the sampling
path directly: permutation-sampling Shapley estimates computed from the
SAME cached coalition values, with a convergence curve of estimator
error vs number of sampled permutations.

The materials question: when a measured-band-gap campaign (expt_zhuo
receiver) is advised by the pool of public databases (MP GGA, MP r2SCAN,
MP ICSD-provenance subset, JARVIS OptB88vdW, JARVIS TBmBJ, SNUMAT GGA,
SNUMAT HSE), which database actually earns the credit -- and is credit
concentrated or spread?

Method
------
Characteristic function v(S), S a subset of the 7 donor channels: run
the exp-26-style campaign on the receiver with the COMBINED (pooled)
prior built from ONLY the donors in S (exp 26's combined-condition
prior construction, reused via importlib -- combined_prior() over a
per-channel dict restricted to receiver + S, adaptive learned trust).
v(S) = mean over seeds of the early-window mean tau (first half of
budget checkpoints, as exp 26), with the SAME matched purchase-stream
seeds across all coalitions, so coalition differences are pure prior
effects. v(empty) = the cold campaign. Pairwise arm primary
(--arm kway optional). Nothing is invented: every campaign evaluation
draws one real archived record per participating class per event.

Checkpoint discipline: one JSON per coalition is written ATOMICALLY to
<output-dir>/coalitions/<receiver>/<bitmask>.json as it lands; existing
coalitions are validated and skipped on rerun (resume support).
Coalition evaluation is parallelised with multiprocessing (--workers).

Exact attribution from the 2^7 cached values: Shapley, Banzhaf, LOO per
donor (analysis/shapley.py engines over a cached-value lookup), with
per-seed exact Shapley and bootstrap CIs over seeds (Shapley is linear
in v, so the per-seed mean equals the Shapley of the seed-mean game;
checked). Efficiency: sum(Shapley) == v(N) - v(empty) to machine
precision (asserted).

MC validation (uses ONLY the cached v(S); no new campaigns): the
permutation-sampling estimator (ShapleyEngine.monte_carlo) for
m in {10, 30, 100, 300, 1000, 3000} permutations, 20 seeded independent
replicates each: max-over-players absolute error vs exact, and rank
agreement (Kendall tau of estimated vs exact player ranking). Reports
the smallest m at which the player ranking is stable (tau == 1.0 in
>= 95% of replicates) plus the mean number of DISTINCT coalitions the
sampler actually touched there -- the honest cost comparison against
the 128 exact evaluations.

Success criteria: exact computation feasible at 7 players (wall time
reported); efficiency axiom holds to machine precision; MC ranking
stabilises well below 128-equivalent cost (the crossover is reported
honestly if it does not).

Usage (from ateki/):
    uv run python experiments/08_database_attribution.py
    uv run python experiments/08_database_attribution.py --self-test
    uv run python experiments/08_database_attribution.py --smoke \
        --workers 8 --output-dir results/database_attribution_smoke
Outputs: results/database_attribution/<receiver>/database_attribution.{json,md,png}
Coalition cache: results/database_attribution/coalitions/<receiver>/<bitmask>.json
ASCII only; seeded and reproducible (--seed).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import kendalltau

from analysis.shapley import ShapleyEngine, BanzhafEngine

_HERE = Path(__file__).resolve().parent
_PKG_ROOT = _HERE.parents[1]  # singular_obj/ (_HERE is .../ateki/experiments)
EXP26_PATH = (_PKG_ROOT / "tenki" / "TENKi" / "experiments"
              / "26_paired_campaign.py")

MC_PERMUTATIONS = [10, 30, 100, 300, 1000, 3000]
MC_REPLICATES = 20
STABLE_FRACTION = 0.95

FRIENDLY_NAME = {
    "mp_gga": "MP GGA",
    "mp_r2scan": "MP r2SCAN",
    "mp_gga_expsynth": "MP GGA (ICSD-provenance subset)",
    "jarvis_optb88vdw": "JARVIS OptB88vdW",
    "jarvis_mbj": "JARVIS TBmBJ",
    "snumat_gga": "SNUMAT GGA",
    "snumat_hse": "SNUMAT HSE",
    "expt_zhuo": "measured band gaps (expt_zhuo)",
}


def friendly(channel: str) -> str:
    return FRIENDLY_NAME.get(channel, channel)


# ---------------------------------------------------------------------------
# Coalition indexing
# ---------------------------------------------------------------------------

def mask_to_coalition(mask: int, donors: list[str]) -> frozenset:
    return frozenset(d for j, d in enumerate(donors) if mask & (1 << j))


def coalition_to_mask(S, donors: list[str]) -> int:
    members = frozenset(S)
    return sum(1 << j for j, d in enumerate(donors) if d in members)


# ---------------------------------------------------------------------------
# exp 26 reuse (filename starts with a digit -> importlib, not import)
# ---------------------------------------------------------------------------

def load_exp26():
    if "exp26_paired_campaign" in sys.modules:
        return sys.modules["exp26_paired_campaign"]
    if not EXP26_PATH.exists():
        raise SystemExit("exp 26 not found: %s" % EXP26_PATH)
    spec = importlib.util.spec_from_file_location(
        "exp26_paired_campaign", str(EXP26_PATH))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["exp26_paired_campaign"] = mod
    spec.loader.exec_module(mod)
    return mod


def pegki_root() -> Path:
    env = os.environ.get("PEGKI_ROOT")
    if env:
        return Path(env).resolve()
    return (_PKG_ROOT / "shared").resolve()


# ---------------------------------------------------------------------------
# Coalition campaign evaluation (worker side)
# ---------------------------------------------------------------------------

_WORKER: dict = {}


def _init_worker(universe_path: str, min_class_size: int) -> None:
    mod = load_exp26()
    _WORKER["mod"] = mod
    _WORKER["per_channel"] = mod.load_universe(Path(universe_path),
                                               min_class_size)


def _eval_coalition(task: dict) -> dict:
    """v(S) for one coalition: exp-26-style campaign, matched seeds."""
    mod = _WORKER["mod"]
    per_channel = _WORKER["per_channel"]
    receiver = task["receiver"]
    donors = task["donors"]
    mask = task["bitmask"]
    classes = per_channel[receiver]
    members = sorted(mask_to_coalition(mask, donors))

    checkpoints = list(range(task["budget_step"],
                             task["budget"] + 1, task["budget_step"]))
    half = max(1, len(checkpoints) // 2)
    k = 2 if task["arm"] == "pair" else task["kway"]

    if mask == 0:
        mode, prior = "cold", None
    else:
        # exp 26 combined_prior over ONLY the donors in S: restrict the
        # per-channel dict to receiver + coalition members.
        sub = {receiver: classes}
        for d in members:
            sub[d] = per_channel[d]
        prior = mod.combined_prior(receiver, sub)
        mode = "adaptive"

    t0 = time.time()
    per_seed_early: dict = {}
    per_seed_final: dict = {}
    for s in task["seed_list"]:
        taus, _ = mod.run_campaign(classes, mode, prior, task["lam"], k,
                                   task["budget"], checkpoints, s)
        per_seed_early[str(s)] = float(np.mean(taus[:half]))
        per_seed_final[str(s)] = float(taus[-1])

    return {
        "bitmask": mask,
        "members": members,
        "donors": donors,
        "receiver": receiver,
        "config": {k2: task[k2] for k2 in
                   ("arm", "kway", "budget", "budget_step", "lam",
                    "min_class_size", "seed_list")},
        "per_seed_early": per_seed_early,
        "per_seed_final": per_seed_final,
        "value_early": float(np.mean(list(per_seed_early.values()))),
        "value_final": float(np.mean(list(per_seed_final.values()))),
        "wall_time_s": float(time.time() - t0),
    }


def save_atomic(payload: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
    os.replace(tmp, path)


def load_cached(path: Path, donors: list[str], receiver: str,
                config: dict) -> dict | None:
    """Load a coalition checkpoint if it matches the run configuration."""
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    if d.get("donors") != donors or d.get("receiver") != receiver:
        raise SystemExit(
            "cached coalition %s was computed for different players; "
            "use a fresh --output-dir" % path)
    if d.get("config") != config:
        raise SystemExit(
            "cached coalition %s was computed under a different config; "
            "use a fresh --output-dir" % path)
    return d


# ---------------------------------------------------------------------------
# Exact attribution + MC validation over cached values
# ---------------------------------------------------------------------------

def lookup_value_fn(values_by_mask: dict, donors: list[str]):
    def v(S) -> float:
        return values_by_mask[coalition_to_mask(S, donors)]
    return v


class CountingValue:
    """Value lookup that records which coalitions the sampler touched."""

    def __init__(self, values_by_mask: dict, donors: list[str]):
        self.values = values_by_mask
        self.donors = donors
        self.touched: set = set()

    def __call__(self, S) -> float:
        m = coalition_to_mask(S, self.donors)
        self.touched.add(m)
        return self.values[m]


def exact_attribution(donors: list[str], values_by_mask: dict,
                      eff_tol: float = 1e-10) -> dict:
    v = lookup_value_fn(values_by_mask, donors)
    t0 = time.time()
    shap = ShapleyEngine(donors, v).exact().scores
    banz = BanzhafEngine(donors, v).exact().scores
    grand_mask = (1 << len(donors)) - 1
    v_grand = values_by_mask[grand_mask]
    v_empty = values_by_mask[0]
    loo = {d: v_grand - values_by_mask[grand_mask & ~(1 << j)]
           for j, d in enumerate(donors)}
    wall = time.time() - t0

    gap = abs(sum(shap.values()) - (v_grand - v_empty))
    tol = eff_tol * max(1.0, abs(v_grand - v_empty))
    assert gap <= tol, (
        "efficiency axiom violated: |sum(phi) - (v(N) - v(empty))| = %.3e"
        % gap)
    return {"shapley": shap, "banzhaf": banz, "loo": loo,
            "v_grand": v_grand, "v_empty": v_empty,
            "efficiency_gap": float(gap), "attribution_wall_time_s": wall}


def per_seed_shapley(donors: list[str], coalitions: dict,
                     seed_list: list[int], n_boot: int,
                     boot_seed: int) -> dict:
    """Exact Shapley per seed (linearity) -> bootstrap CIs over seeds."""
    per_seed = {}
    for s in seed_list:
        vals = {m: c["per_seed_early"][str(s)] for m, c in coalitions.items()}
        per_seed[s] = ShapleyEngine(
            donors, lookup_value_fn(vals, donors)).exact().scores
    rng = np.random.default_rng(boot_seed)
    out = {}
    for d in donors:
        samples = np.asarray([per_seed[s][d] for s in seed_list])
        if len(samples) < 2:
            ci = [float(samples[0]), float(samples[0])]
        else:
            idx = rng.integers(0, len(samples), size=(n_boot, len(samples)))
            means = samples[idx].mean(axis=1)
            ci = [float(np.percentile(means, 2.5)),
                  float(np.percentile(means, 97.5))]
        out[d] = {"mean": float(samples.mean()), "ci": ci,
                  "per_seed": [float(x) for x in samples]}
    return out


def mc_validation(donors: list[str], values_by_mask: dict, exact: dict,
                  ms: list[int], n_rep: int, seed: int) -> dict:
    """Permutation-sampling Shapley vs exact, from cached values only."""
    exact_vec = np.asarray([exact[d] for d in donors])
    master = np.random.default_rng(seed)
    curve = []
    stable_m = None
    for m in ms:
        errs, rank_ok, distinct = [], [], []
        for _ in range(n_rep):
            rep_seed = int(master.integers(0, 2**31 - 1))
            cv = CountingValue(values_by_mask, donors)
            est = ShapleyEngine(donors, cv).monte_carlo(
                n_samples=m, seed=rep_seed).scores
            est_vec = np.asarray([est[d] for d in donors])
            errs.append(float(np.max(np.abs(est_vec - exact_vec))))
            tau = float(kendalltau(exact_vec, est_vec)[0])
            rank_ok.append(tau >= 1.0 - 1e-12)
            distinct.append(len(cv.touched))
        frac_stable = float(np.mean(rank_ok))
        entry = {
            "m": m,
            "max_abs_error_median": float(np.median(errs)),
            "max_abs_error_mean": float(np.mean(errs)),
            "max_abs_error_min": float(np.min(errs)),
            "max_abs_error_max": float(np.max(errs)),
            "frac_replicates_rank_exact": frac_stable,
            "mean_distinct_coalitions_touched": float(np.mean(distinct)),
        }
        curve.append(entry)
        if stable_m is None and frac_stable >= STABLE_FRACTION:
            stable_m = m
    return {"permutation_counts": ms, "n_replicates": n_rep,
            "stable_fraction_threshold": STABLE_FRACTION,
            "curve": curve, "rank_stable_m": stable_m}


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def concentration_stats(shapley: dict) -> dict:
    pos = {d: max(v, 0.0) for d, v in shapley.items()}
    total = sum(pos.values())
    if total <= 0:
        return {"top_donor": None, "top_share_of_positive_credit": None,
                "effective_n_donors": None, "verdict": "no positive credit"}
    shares = {d: v / total for d, v in pos.items()}
    top = max(shares, key=shares.get)
    herf = sum(s * s for s in shares.values())
    eff_n = 1.0 / herf if herf > 0 else 0.0
    verdict = "concentrated" if shares[top] > 0.5 else "spread"
    return {"top_donor": top,
            "top_share_of_positive_credit": float(shares[top]),
            "effective_n_donors": float(eff_n),
            "verdict": verdict}


def write_markdown(result: dict, path: Path) -> None:
    donors = result["donors"]
    ex = result["exact"]
    cis = result["shapley_seed_cis"]
    conc = result["concentration"]
    mc = result["mc_validation"]
    order = sorted(donors, key=lambda d: -ex["shapley"][d])

    lines = ["# Experiment 08: which database earns the credit?", ""]
    lines.append(
        "Receiver `%s` advised by %d donor databases on the frozen band-gap archive "
        "universe. v(S) = mean over %d matched seeds of the early-window "
        "mean tau of an exp-26-style campaign whose pooled prior uses ONLY "
        "the donors in S (arm: %s, budget %d). v(empty) = cold campaign. "
        "Every value below comes from the %d measured coalition campaigns; "
        "nothing is simulated beyond retrospective queries into archived "
        "records." % (result["receiver"], len(donors),
                      len(result["config"]["seed_list"]), result["config"]["arm"],
                      result["config"]["budget"], result["n_coalitions"]))
    lines.append("")
    lines.append("## Credit ranking (exact %d-player Shapley, early window)"
                 % len(donors))
    lines.append("")
    lines.append("| rank | database | Shapley [95% CI over seeds] | "
                 "Banzhaf | LOO |")
    lines.append("|---|---|---|---|---|")
    for i, d in enumerate(order):
        ci = cis[d]["ci"]
        lines.append("| %d | %s | %+0.4f [%+0.4f, %+0.4f] | %+0.4f | "
                     "%+0.4f |" % (i + 1, friendly(d), ex["shapley"][d],
                                   ci[0], ci[1], ex["banzhaf"][d],
                                   ex["loo"][d]))
    lines.append("")

    # Materials story, from measured numbers only.
    top = order[0]
    neg = [d for d in order if ex["shapley"][d] < 0]
    near0 = [d for d in order
             if 0 <= ex["shapley"][d] < 0.05 * max(abs(ex["shapley"][top]),
                                                   1e-12)]
    story = ["## The materials story", ""]
    story.append(
        "The measured-band-gap campaign should thank **%s** first: it "
        "holds %.0f%% of the positive credit in this run." % (
            friendly(top),
            100.0 * (conc["top_share_of_positive_credit"] or 0.0)))
    story.append("")
    story.append(
        "Credit is **%s**: the effective number of contributing databases "
        "(inverse Herfindahl over positive Shapley shares) is %.2f of %d."
        % (conc["verdict"], conc["effective_n_donors"] or 0.0, len(donors)))
    if neg:
        story.append("")
        story.append(
            "Negative-credit donors (their pooled-prior contribution "
            "lowered the early-window tau in this run): %s. A donor whose "
            "class ordering misranks against the measured gaps prices at "
            "about zero or below." % ", ".join(friendly(d) for d in neg))
    if near0:
        story.append("")
        story.append("Donors pricing near zero: %s."
                     % ", ".join(friendly(d) for d in near0))
    lines += story
    lines.append("")

    lines.append("## Feasibility and axioms")
    lines.append("")
    lines.append(
        "- %d coalition campaigns; campaign wall time %.1f s total "
        "(%.2f s per coalition mean, %d workers); exact "
        "Shapley+Banzhaf+LOO from the cached values took %.3f s." % (
            result["n_coalitions"],
            result["timing"]["campaign_wall_time_s_total"],
            result["timing"]["campaign_wall_time_s_per_coalition_mean"],
            result["config"]["workers"],
            ex["attribution_wall_time_s"]))
    lines.append(
        "- Efficiency axiom: |sum(phi) - (v(N) - v(empty))| = %.2e "
        "(machine precision; asserted)." % ex["efficiency_gap"])
    lines.append(
        "- v(N) = %+0.4f, v(empty) = %+0.4f; final-window Shapley "
        "reported in the JSON as a no-long-run-harm cross-check."
        % (ex["v_grand"], ex["v_empty"]))
    lines.append("")

    lines.append("## Monte-Carlo validation (from cached values only)")
    lines.append("")
    lines.append("| permutations m | median max-error | rank exact "
                 "(frac of %d reps) | distinct coalitions touched |"
                 % mc["n_replicates"])
    lines.append("|---|---|---|---|")
    for e in mc["curve"]:
        lines.append("| %d | %.4f | %.2f | %.1f |" % (
            e["m"], e["max_abs_error_median"],
            e["frac_replicates_rank_exact"],
            e["mean_distinct_coalitions_touched"]))
    lines.append("")
    if mc["rank_stable_m"] is not None:
        stable = [e for e in mc["curve"]
                  if e["m"] == mc["rank_stable_m"]][0]
        cheaper = stable["mean_distinct_coalitions_touched"] < \
            result["n_coalitions"]
        lines.append(
            "Player ranking stabilises (tau == 1.0 in >= %.0f%% of "
            "replicates) at m = %d permutations, touching %.1f distinct "
            "coalitions on average -- %s the %d coalitions the exact "
            "computation needs." % (
                100 * mc["stable_fraction_threshold"], mc["rank_stable_m"],
                stable["mean_distinct_coalitions_touched"],
                "fewer than" if cheaper else "NOT fewer than",
                result["n_coalitions"]))
        if not cheaper:
            lines.append("")
            lines.append(
                "Honest crossover note: at %d players the sampler does not "
                "beat exact enumeration on distinct-coalition cost; the "
                "sampling path pays off only at larger player counts."
                % len(donors))
    else:
        lines.append(
            "Player ranking did NOT stabilise within the tested "
            "permutation budgets (max m = %d); reported honestly."
            % mc["permutation_counts"][-1])
        vals = sorted(ex["shapley"].values())
        min_gap = min(b - a for a, b in zip(vals, vals[1:]))
        last = mc["curve"][-1]["max_abs_error_median"]
        if min_gap <= last:
            lines.append("")
            lines.append(
                "Mechanism: the smallest exact Shapley gap between "
                "adjacent players is %.2e, at or below the m = %d "
                "median value error (%.2e), so exact rank agreement is "
                "unattainable by sampling REGARDLESS of m -- two players "
                "are measurably (inter)changeable. When two donors carry "
                "the same class-level ordering they are symmetric players "
                "and the symmetry axiom forces equal Shapley values; the "
                "VALUE estimates themselves converge fast (see the "
                "max-error column), which is what the sampling path "
                "needs." % (min_gap, mc["permutation_counts"][-1], last))
    lines.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def write_plot(result: dict, path: Path) -> None:
    donors = result["donors"]
    ex = result["exact"]
    cis = result["shapley_seed_cis"]
    mc = result["mc_validation"]
    order = sorted(donors, key=lambda d: -ex["shapley"][d])

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.6))

    ax = axes[0]
    vals = [ex["shapley"][d] for d in order]
    colors = ["#4878a8" if v >= 0 else "#c44e52" for v in vals]
    lo = [ex["shapley"][d] - cis[d]["ci"][0] for d in order]
    hi = [cis[d]["ci"][1] - ex["shapley"][d] for d in order]
    ax.bar(range(len(order)), vals, color=colors,
           yerr=[lo, hi], capsize=3, error_kw={"lw": 0.8})
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([friendly(d) for d in order], rotation=25,
                       ha="right", fontsize=7)
    ax.axhline(0, color="k", lw=0.6)
    ax.set_ylabel("exact Shapley value (tau units)")
    ax.set_title("Which database earns the credit? (%s, early window)"
                 % result["receiver"])

    ax = axes[1]
    ms = [e["m"] for e in mc["curve"]]
    med = [e["max_abs_error_median"] for e in mc["curve"]]
    emin = [e["max_abs_error_min"] for e in mc["curve"]]
    emax = [e["max_abs_error_max"] for e in mc["curve"]]
    ax.plot(ms, med, "o-", color="#4878a8", label="median max-error")
    ax.fill_between(ms, emin, emax, color="#4878a8", alpha=0.2,
                    label="replicate min-max")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("sampled permutations m")
    ax.set_ylabel("max abs error vs exact (tau units)")
    ax.set_title("MC Shapley convergence (%d replicates per m)"
                 % mc["n_replicates"])
    ax2 = ax.twinx()
    frac = [e["frac_replicates_rank_exact"] for e in mc["curve"]]
    ax2.plot(ms, frac, "s--", color="#c44e52", label="rank-exact fraction")
    ax2.set_ylim(-0.05, 1.05)
    ax2.set_ylabel("fraction of replicates with exact ranking")
    if mc["rank_stable_m"] is not None:
        ax.axvline(mc["rank_stable_m"], color="gray", lw=0.8, ls=":")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=7, loc="lower left")

    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Self-test (no universe needed)
# ---------------------------------------------------------------------------

def self_test() -> int:
    failures = 0

    # (1) 3-player synthetic game with hand-computed Shapley values.
    table = {frozenset(): 0.0, frozenset("a"): 1.0, frozenset("b"): 2.0,
             frozenset("c"): 3.0, frozenset("ab"): 4.0,
             frozenset("ac"): 5.0, frozenset("bc"): 6.0,
             frozenset("abc"): 8.0}
    shap = ShapleyEngine(["a", "b", "c"],
                         lambda S: table[frozenset(S)]).exact().scores
    expected = {"a": 5.0 / 3.0, "b": 8.0 / 3.0, "c": 11.0 / 3.0}
    ok = all(abs(shap[p] - expected[p]) < 1e-12 for p in expected)
    print("[%s] hand-computed 3-player Shapley: got "
          "a=%.6f b=%.6f c=%.6f" % ("PASS" if ok else "FAIL",
                                    shap["a"], shap["b"], shap["c"]))
    failures += 0 if ok else 1

    # (2) Efficiency axiom on a random synthetic 7-player game.
    donors = ["d%d" % i for i in range(7)]
    rng = np.random.default_rng(20260926)
    values = {m: float(v) for m, v in
              enumerate(rng.normal(0.0, 1.0, size=128))}
    ex = exact_attribution(donors, values)  # asserts internally
    gap = ex["efficiency_gap"]
    ok = gap <= 1e-10
    print("[%s] efficiency on random 7-player game: gap %.2e"
          % ("PASS" if ok else "FAIL", gap))
    failures += 0 if ok else 1

    # (3) MC estimator consistency: error shrinks with m.
    mc = mc_validation(donors, values, ex["shapley"],
                       ms=[50, 3000], n_rep=5, seed=7)
    e_small = mc["curve"][0]["max_abs_error_mean"]
    e_large = mc["curve"][1]["max_abs_error_mean"]
    ok = e_large < e_small
    print("[%s] MC consistency: mean max-error %.4f (m=50) -> %.4f "
          "(m=3000)" % ("PASS" if ok else "FAIL", e_small, e_large))
    failures += 0 if ok else 1

    # (4) Bitmask/coalition indexing round-trip.
    ok = all(coalition_to_mask(mask_to_coalition(m, donors), donors) == m
             for m in range(128))
    grand = coalition_to_mask(frozenset(donors), donors)
    ok = ok and grand == 127 and mask_to_coalition(0, donors) == frozenset()
    print("[%s] bitmask round-trip over all 128 masks"
          % ("PASS" if ok else "FAIL"))
    failures += 0 if ok else 1

    print("self-test: %s" % ("PASS (4/4)" if failures == 0 else "FAIL"))
    return failures


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description="ATEKi exp 08: exact 7-database Shapley attribution "
                    "with MC validation")
    ap.add_argument("--receiver", default="expt_zhuo")
    ap.add_argument("--arm", choices=["pair", "kway"], default="pair")
    ap.add_argument("--kway", type=int, default=4)
    ap.add_argument("--seeds", type=int, default=10,
                    help="number of matched purchase-stream seeds")
    ap.add_argument("--budget", type=int, default=240)
    ap.add_argument("--budget-step", type=int, default=24)
    ap.add_argument("--lam", type=float, default=8.0)
    ap.add_argument("--min-class-size", type=int, default=30)
    ap.add_argument("--universe",
                    default="output/bandgap_archive_build/bandgap_universe.jsonl",
                    help="band-gap archive universe jsonl, relative to PEGKI_ROOT")
    ap.add_argument("--workers", type=int, default=None,
                    help="default min(14, cpu)")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--output-dir", default=None)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--smoke", action="store_true",
                    help="3 donors (8 coalitions), 2 seeds, budget 48")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    if args.smoke:
        args.seeds = 2
        args.budget = 48

    workers = args.workers if args.workers else min(14, os.cpu_count() or 1)
    universe = pegki_root() / args.universe
    if not universe.exists():
        print("[error] universe not found: %s" % universe)
        return 1

    t_start = time.time()
    mod = load_exp26()
    per_channel = mod.load_universe(universe, args.min_class_size)
    if args.receiver not in per_channel:
        print("[error] receiver %s not in universe channels: %s"
              % (args.receiver, ", ".join(sorted(per_channel))))
        return 1
    donors = sorted(c for c in per_channel if c != args.receiver)
    if args.smoke:
        donors = donors[:3]
    n = len(donors)
    n_coalitions = 1 << n
    seed_list = [args.seed + 1000 * i for i in range(args.seeds)]
    print("[load] receiver %s; %d donors -> %d coalitions; %d seeds"
          % (args.receiver, n, n_coalitions, len(seed_list)))

    out_root = Path(args.output_dir) if args.output_dir else (
        Path(__file__).resolve().parents[1] / "results"
        / "database_attribution")
    recv_dir = out_root / args.receiver
    cache_dir = out_root / "coalitions" / args.receiver
    recv_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    config = {"arm": args.arm, "kway": args.kway, "budget": args.budget,
              "budget_step": args.budget_step, "lam": args.lam,
              "min_class_size": args.min_class_size,
              "seed_list": seed_list}

    # ---- stage 1: measure the 2^n coalition campaigns (resumable) --------
    coalitions: dict = {}
    pending = []
    for mask in range(n_coalitions):
        cached = load_cached(cache_dir / ("%d.json" % mask), donors,
                             args.receiver, config)
        if cached is not None:
            coalitions[mask] = cached
        else:
            pending.append(mask)
    print("[plan] %d coalitions to run; %d already cached"
          % (len(pending), n_coalitions - len(pending)))

    task_base = dict(config)
    task_base.update({"donors": donors, "receiver": args.receiver})
    tasks = [dict(task_base, bitmask=m) for m in pending]

    t_camp = time.time()
    if tasks and workers > 1:
        with ProcessPoolExecutor(
                max_workers=workers, initializer=_init_worker,
                initargs=(str(universe), args.min_class_size)) as ex:
            futs = {ex.submit(_eval_coalition, t): t["bitmask"]
                    for t in tasks}
            for fut in as_completed(futs):
                res = fut.result()
                save_atomic(res, cache_dir / ("%d.json" % res["bitmask"]))
                coalitions[res["bitmask"]] = res
                print("[done] coalition %3d/%d (|S|=%d) v_early=%+0.4f "
                      "(%.1fs)" % (res["bitmask"], n_coalitions - 1,
                                   len(res["members"]),
                                   res["value_early"], res["wall_time_s"]))
    elif tasks:
        _init_worker(str(universe), args.min_class_size)
        for t in tasks:
            res = _eval_coalition(t)
            save_atomic(res, cache_dir / ("%d.json" % res["bitmask"]))
            coalitions[res["bitmask"]] = res
            print("[done] coalition %3d/%d (|S|=%d) v_early=%+0.4f (%.1fs)"
                  % (res["bitmask"], n_coalitions - 1, len(res["members"]),
                     res["value_early"], res["wall_time_s"]))
    campaign_wall = time.time() - t_camp
    per_coal_times = [coalitions[m]["wall_time_s"]
                      for m in range(n_coalitions)]

    # ---- stage 2: exact attribution from the cached values ---------------
    values_early = {m: coalitions[m]["value_early"]
                    for m in range(n_coalitions)}
    values_final = {m: coalitions[m]["value_final"]
                    for m in range(n_coalitions)}
    exact = exact_attribution(donors, values_early)
    exact_final = exact_attribution(donors, values_final)
    print("[exact] efficiency gap %.2e; attribution %.3f s"
          % (exact["efficiency_gap"], exact["attribution_wall_time_s"]))

    cis = per_seed_shapley(donors, coalitions, seed_list, args.n_boot,
                           args.seed)
    lin_gap = max(abs(cis[d]["mean"] - exact["shapley"][d]) for d in donors)
    if lin_gap > 1e-9:
        print("[warn] linearity gap %.2e (per-seed mean vs mean-game "
              "Shapley)" % lin_gap)

    # ---- stage 3: MC validation from cached values only -------------------
    mc = mc_validation(donors, values_early, exact["shapley"],
                       MC_PERMUTATIONS, MC_REPLICATES, args.seed + 777)

    conc = concentration_stats(exact["shapley"])

    result = {
        "experiment": "08_database_attribution",
        "receiver": args.receiver,
        "donors": donors,
        "donor_names": {d: friendly(d) for d in donors},
        "n_coalitions": n_coalitions,
        "config": dict(config, workers=workers, smoke=args.smoke,
                       universe=str(universe), seed=args.seed),
        "coalition_values_early": {str(m): values_early[m]
                                   for m in range(n_coalitions)},
        "coalition_values_final": {str(m): values_final[m]
                                   for m in range(n_coalitions)},
        "exact": exact,
        "exact_final_window": exact_final,
        "shapley_seed_cis": cis,
        "linearity_gap_per_seed_vs_mean_game": float(lin_gap),
        "concentration": conc,
        "mc_validation": mc,
        "timing": {
            "campaign_wall_time_s_total": float(sum(per_coal_times)),
            "campaign_wall_time_s_per_coalition_mean":
                float(np.mean(per_coal_times)),
            "campaign_stage_elapsed_s": float(campaign_wall),
            "total_elapsed_s": float(time.time() - t_start),
        },
    }

    with open(recv_dir / "database_attribution.json", "w",
              encoding="utf-8") as fh:
        json.dump(result, fh, indent=1, sort_keys=True)
    write_markdown(result, recv_dir / "database_attribution.md")
    write_plot(result, recv_dir / "database_attribution.png")

    print("[save] %s" % recv_dir)
    for d in sorted(donors, key=lambda x: -exact["shapley"][x]):
        print("  %-32s shapley %+0.4f  banzhaf %+0.4f  loo %+0.4f"
              % (friendly(d), exact["shapley"][d], exact["banzhaf"][d],
                 exact["loo"][d]))
    if mc["rank_stable_m"] is not None:
        print("  MC ranking stable at m = %d permutations"
              % mc["rank_stable_m"])
    else:
        print("  MC ranking NOT stable within tested m")
    return 0


if __name__ == "__main__":
    sys.exit(main())
