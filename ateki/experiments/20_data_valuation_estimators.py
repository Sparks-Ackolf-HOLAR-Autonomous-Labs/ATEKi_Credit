"""
Experiment 20: data-valuation estimators on the measured seven-database game.

Checks the ATEKi comparison with the data-valuation literature on the 128
measured coalition campaigns of experiment 08 (seven donor databases advising
the experimental band-gap campaign, receiver expt_zhuo, 10 matched seeds,
early and final windows). No campaign is re-run; every value is a lookup.

Estimators (all on the zero-normalised game w(S) = v(S) - v(empty)):
  - exact Shapley (= Data Shapley, Ghorbani and Zou 2019, with C = 1);
  - Banzhaf (= Data Banzhaf, Wang and Jia 2023);
  - Beta(alpha, beta)-Shapley semivalues (Kwon and Zou 2022), per-subset
    weight Beta(s + beta, n - s - 1 + alpha) / Beta(alpha, beta) for a subset
    of size s not containing the player; (1,1) is Shapley, alpha > 1 puts
    weight on small coalitions, beta > 1 moves the weight towards LOO;
  - leave-one-out (LOO);
  - truncated Monte Carlo Shapley (TMC, Ghorbani and Zou 2019, Algorithm 1):
    scan a random permutation and set later marginal contributions to zero
    once |w(N) - w(prefix)| < tolerance.

Checks:
  (1) the duplicate argument: Ghorbani and Zou motivate Data Shapley with a
      nearest-neighbour learner in which every point has an exact copy, so
      LOO gives every point zero. The SNUMAT GGA and HSE06 orderings are
      identical over the archive; their LOO values are reported together with
      the marginal value of the second copy over all coalitions;
  (2) rank consistency across runs (Wang and Jia 2023): each of the 10 seeds
      is one run of the stochastic campaigns; the mean pairwise Spearman
      correlation of each estimator's values across the 45 seed pairs, and
      the seeds in which the bottom database is the same as in the
      seed-averaged Shapley ranking;
  (3) TMC truncation bias: TMC against exact Shapley at several tolerances
      and permutation budgets (3n permutations, the budget Ghorbani and Zou
      report as usually sufficient, and 1,000).

Second part (--almgsi): the same estimators on the computed Al-Mg-Si donor
games (receivers QE PBE and QE HSE06, four and five donors, fixed and
learned trust), read from the coalition files that
compute/almgsi_campaign/campaign.py --shapley writes (coalitions.json: every
coalition value and its 40 per-run values, k = 1 and 4 by 20 seeds). The
near-duplicate check there is the QE PBE and MACE-MP-0 relaxation pair,
whose orderings agree closely.

Third part (--almgsi-hot): the same estimators on the six higher-temperature
MD games of the temperature study (receivers MEAM, NEP89 and MACE-MP-0 MD at
453 K and 803 K; six donors each: the same potential at 300 K, the two other
potentials at the target temperature, the 0 K MACE-MP-0 relaxation, QE PBE
and QE HSE06), read from the coalition files that
compute/almgsi_campaign/temperature_coalitions.py writes (k = 4 by 20 seeds,
pooled learned trust as published and pooled fixed trust). Near-duplicate
pairs: QE PBE and QE HSE06 in every game, and the MACE-MP-0 relaxation with
MACE-MP-0 MD at 300 K in the MACE receivers.

Usage:
    python experiments/20_data_valuation_estimators.py
    python experiments/20_data_valuation_estimators.py --almgsi
    python experiments/20_data_valuation_estimators.py --almgsi-hot
    python experiments/20_data_valuation_estimators.py --self-test
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from analysis.shapley import ShapleyEngine, BanzhafEngine
from analysis.reports import write_json

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IN = ROOT / "results" / "database_attribution" / "expt_zhuo" / "database_attribution.json"
DEFAULT_CACHE = ROOT / "results" / "database_attribution" / "coalitions" / "expt_zhuo"
DEFAULT_OUT = ROOT / "results" / "data_valuation_estimators"
BETAS = [(1, 1), (4, 1), (16, 1), (1, 4), (1, 16)]
DUPLICATES = ("snumat_gga", "snumat_hse")
NEAR_DUPLICATES = ("mp_gga", "mp_gga_expsynth")


# ---------------------------------------------------------------------------
# Estimators on a lookup game given as {bitmask: value}
# ---------------------------------------------------------------------------

def beta_fn(a, b):
    return math.exp(math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b))


def subset_weight(s, n, alpha, beta):
    """Per-subset Beta(alpha, beta)-Shapley weight for |S| = s, i not in S."""
    return beta_fn(s + beta, n - s - 1 + alpha) / beta_fn(alpha, beta)


def semivalue(vals, n, weight):
    out = np.zeros(n)
    for i in range(n):
        bit = 1 << i
        for m in range(1 << n):
            if m & bit:
                continue
            s = bin(m).count("1")
            out[i] += weight(s) * (vals[m | bit] - vals[m])
    return out


def shapley(vals, n):
    return semivalue(vals, n, lambda s: subset_weight(s, n, 1, 1))


def banzhaf(vals, n):
    return semivalue(vals, n, lambda s: 1.0 / (1 << (n - 1)))


def beta_shapley(vals, n, alpha, beta):
    return semivalue(vals, n, lambda s: subset_weight(s, n, alpha, beta))


def loo(vals, n):
    full = (1 << n) - 1
    return np.array([vals[full] - vals[full ^ (1 << i)] for i in range(n)])


def tmc_shapley(vals, n, n_perm, tol, rng):
    """Ghorbani and Zou (2019), Algorithm 1, on a lookup game."""
    full = (1 << n) - 1
    vN = vals[full]
    phi = np.zeros(n)
    n_eval = 0
    for t in range(1, n_perm + 1):
        perm = rng.permutation(n)
        m, prev = 0, vals[0]
        for i in perm:
            if abs(vN - prev) < tol:
                cur = prev
            else:
                m |= 1 << int(i)
                cur = vals[m]
                n_eval += 1
            phi[i] = (t - 1) / t * phi[i] + (cur - prev) / t
            prev = cur
    return phi, n_eval


def spearman(x, y):
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    # average ranks for ties
    def avg_rank(v):
        order = np.argsort(v, kind="mergesort")
        r = np.empty(len(v))
        i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and abs(v[order[j + 1]] - v[order[i]]) < 1e-12:
                j += 1
            r[order[i:j + 1]] = (i + j) / 2.0
            i = j + 1
        return r
    rx, ry = avg_rank(np.asarray(x)), avg_rank(np.asarray(y))
    if rx.std() == 0 or ry.std() == 0:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def bottom_set(v):
    return {i for i in range(len(v)) if v[i] <= v.min() + 1e-12}


def estimators(vals, n):
    out = {"shapley": shapley(vals, n), "banzhaf": banzhaf(vals, n), "loo": loo(vals, n)}
    for a, b in BETAS:
        if (a, b) != (1, 1):
            out["beta_%d_%d" % (a, b)] = beta_shapley(vals, n, a, b)
    return out


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def self_test():
    ok = True
    rng = np.random.default_rng(0)
    n = 5
    vals = {m: float(rng.normal()) for m in range(1 << n)}
    vals[0] = 0.0
    players = ["p%d" % i for i in range(n)]

    def fn(S):
        return vals[sum(1 << int(p[1:]) for p in S)]
    ref_sh = ShapleyEngine(players, fn).exact().scores
    ref_bz = BanzhafEngine(players, fn).exact().scores
    sh, bz = shapley(vals, n), banzhaf(vals, n)
    e1 = max(abs(sh[i] - ref_sh["p%d" % i]) for i in range(n))
    e2 = max(abs(bz[i] - ref_bz["p%d" % i]) for i in range(n))
    print("  Shapley matches ShapleyEngine: %.1e" % e1); ok &= e1 < 1e-12
    print("  Banzhaf matches BanzhafEngine: %.1e" % e2); ok &= e2 < 1e-12
    for a, b in BETAS:
        tot = sum(math.comb(n - 1, s) * subset_weight(s, n, a, b) for s in range(n))
        ok &= abs(tot - 1) < 1e-12
    print("  Beta weights sum to one over subsets: %s" % ok)
    big = beta_shapley(vals, n, 1, 1e6)
    e3 = float(np.max(np.abs(big - loo(vals, n))))
    print("  Beta(1, 1e6) -> LOO: %.1e" % e3); ok &= e3 < 1e-4
    # TMC with zero tolerance and all permutations equals exact Shapley
    full = (1 << n) - 1
    acc = np.zeros(n)
    perms = list(itertools.permutations(range(n)))
    for p in perms:
        m, prev = 0, vals[0]
        for i in p:
            m |= 1 << i
            acc[i] += vals[m] - prev
            prev = vals[m]
    e4 = float(np.max(np.abs(acc / len(perms) - sh)))
    print("  all-permutation average = Shapley: %.1e" % e4); ok &= e4 < 1e-12
    phi, _ = tmc_shapley(vals, n, 20000, 0.0, np.random.default_rng(1))
    e5 = float(np.max(np.abs(phi - sh)))
    print("  TMC (tol 0, 20000 perms) error: %.3f" % e5); ok &= e5 < 0.05
    ok &= abs(phi.sum() - vals[full]) < 1e-9
    # duplicate check: in a max game an exact copy has LOO zero
    dup = {m: float(m != 0) for m in range(4)}
    ok &= np.allclose(loo(dup, 2), 0.0)
    print("  max game with two copies: LOO = %s" % loo(dup, 2).tolist())
    print("SELF-TEST %s" % ("PASS" if ok else "FAIL"))
    return ok


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def load_games(inp, cache, window):
    d = json.loads(Path(inp).read_text(encoding="utf-8"))
    players = list(d["donors"])
    avg = {int(k): float(v) for k, v in d["coalition_values_%s" % window].items()}
    per_seed = {}
    for f in sorted(Path(cache).glob("*.json")):
        c = json.loads(f.read_text(encoding="utf-8"))
        assert c["donors"] == players
        for s, v in c["per_seed_%s" % window].items():
            per_seed.setdefault(s, {})[c["bitmask"]] = float(v)
    assert all(len(g) == 1 << len(players) for g in per_seed.values())
    norm = lambda g: {m: v - g[0] for m, v in g.items()}
    return players, d["donor_names"], norm(avg), {s: norm(g) for s, g in per_seed.items()}


def duplicate_check(vals, players):
    n = len(players)
    i, j = (players.index(p) for p in DUPLICATES)
    k, l = (players.index(p) for p in NEAR_DUPLICATES)
    full = (1 << n) - 1
    second = []
    for m in range(1 << n):
        if m & (1 << i) and not m & (1 << j):
            second.append(vals[m | (1 << j)] - vals[m])
    rest = [vals[m | (1 << i) | (1 << j)] - vals[m | (1 << i)]
            for m in range(1 << n) if not m & ((1 << i) | (1 << j)) and m]
    lo = loo(vals, n)
    return {
        "loo_duplicates": [float(lo[i]), float(lo[j])],
        "loo_near_duplicates": [float(lo[k]), float(lo[l])],
        "second_copy_alone": float(vals[(1 << i) | (1 << j)] - vals[1 << i]),
        "second_copy_mean_with_others": float(np.mean(rest)),
        "second_copy_range_with_others": [float(min(rest)), float(max(rest))],
        "second_copy_positive_share": float(np.mean(np.array(rest) > 1e-12)),
        "remove_both_duplicates_from_full": float(vals[full] - vals[full ^ (1 << i) ^ (1 << j)]),
    }


def consistency(per_seed, n, avg_est):
    seeds = sorted(per_seed)
    est = {s: estimators(per_seed[s], n) for s in seeds}
    names = list(avg_est)
    bottom_ref = bottom_set(avg_est["shapley"])
    out = {}
    for e in names:
        sp = [spearman(est[a][e], est[b][e]) for a, b in itertools.combinations(seeds, 2)]
        sp = [x for x in sp if not math.isnan(x)]
        to_avg = [spearman(est[s][e], avg_est["shapley"]) for s in seeds]
        out[e] = {
            "mean_pairwise_spearman": float(np.mean(sp)),
            "min_pairwise_spearman": float(np.min(sp)),
            "mean_spearman_to_avg_shapley": float(np.nanmean(to_avg)),
            "seeds_bottom_equals_avg_shapley_bottom": int(sum(bottom_set(est[s][e]) == bottom_ref for s in seeds)),
            "seeds_with_sign_flip_vs_own_shapley": int(sum(
                any(np.sign(round(est[s][e][i], 12)) != np.sign(round(est[s]["shapley"][i], 12))
                    for i in range(n)) for s in seeds)),
        }
    return out


def tmc_study(vals, n, sh, noise):
    rng = np.random.default_rng(20)
    wN = vals[(1 << n) - 1]
    out = []
    for frac in (0.0, 0.01, 0.05, 0.25):
        for n_perm in (3 * n, 1000):
            tol = frac * abs(wN) if frac else 0.0
            errs, flips, evals = [], 0, []
            for r in range(50):
                phi, ne = tmc_shapley(vals, n, n_perm, tol, rng)
                errs.append(float(np.max(np.abs(phi - sh))))
                flips += int(any(np.sign(round(phi[i], 12)) != np.sign(round(sh[i], 12)) for i in range(n)))
                evals.append(ne)
            out.append({"tolerance_fraction_of_wN": frac, "tolerance": tol, "permutations": n_perm,
                        "median_max_abs_error": float(np.median(errs)),
                        "p90_max_abs_error": float(np.percentile(errs, 90)),
                        "repeats_with_sign_flip": flips, "repeats": 50,
                        "mean_value_lookups": float(np.mean(evals))})
    # bias of truncation itself: tolerance at the seed noise of w(N)
    tol = noise
    phis = [tmc_shapley(vals, n, 1000, tol, rng)[0] for _ in range(20)]
    bias = np.mean(phis, axis=0) - sh
    return out, {"tolerance": tol, "permutations": 1000, "repeats": 20,
                 "mean_bias": bias.tolist(), "max_abs_bias": float(np.max(np.abs(bias)))}


def write_md(res, path):
    nm = res["donor_names"]
    pl = res["players"]
    L = ["# Experiment 20: data-valuation estimators on the seven-database game", "",
         "Receiver: experimental band-gap compilation. Window: %s. Games: seed average and %d per-seed games, 128 measured coalitions each. w(N) = %+.4f."
         % (res["window"], res["n_seeds"], res["w_grand"]), "",
         "## Values (seed-averaged game)", "",
         "| Database | " + " | ".join(res["estimators"]) + " |",
         "|---" * (len(res["estimators"]) + 1) + "|"]
    for i, p in enumerate(pl):
        L.append("| %s | " % nm[p] + " | ".join("%+.4f" % res["values"][e][i] for e in res["estimators"]) + " |")
    dc = res["duplicates"]
    L += ["", "## Duplicate check", "",
          "- LOO of the identical SNUMAT pair: %+.4f, %+.4f" % tuple(dc["loo_duplicates"]),
          "- LOO of MP GGA and its ICSD-provenance subset: %+.4f, %+.4f" % tuple(dc["loo_near_duplicates"]),
          "- second SNUMAT copy alone: %+.4f; with other donors present: mean %+.4f, range %+.4f to %+.4f, positive in %.0f%% of coalitions"
          % (dc["second_copy_alone"], dc["second_copy_mean_with_others"], *dc["second_copy_range_with_others"],
             100 * dc["second_copy_positive_share"]),
          "", "## Consistency across seeds", "",
          "| Estimator | mean pairwise Spearman | min | mean Spearman to averaged Shapley | seeds with Shapley bottom | seeds with sign flip vs own Shapley |",
          "|---|---|---|---|---|---|"]
    for e, c in res["consistency"].items():
        L.append("| %s | %.3f | %.3f | %.3f | %d | %d |" % (
            e, c["mean_pairwise_spearman"], c["min_pairwise_spearman"], c["mean_spearman_to_avg_shapley"],
            c["seeds_bottom_equals_avg_shapley_bottom"], c["seeds_with_sign_flip_vs_own_shapley"]))
    L += ["", "## Truncated Monte Carlo Shapley", "",
          "| tolerance / w(N) | permutations | median max error | 90th pct | repeats with sign flip | lookups |",
          "|---|---|---|---|---|---|"]
    for t in res["tmc"]:
        L.append("| %.2f | %d | %.4f | %.4f | %d/50 | %.0f |" % (
            t["tolerance_fraction_of_wN"], t["permutations"], t["median_max_abs_error"],
            t["p90_max_abs_error"], t["repeats_with_sign_flip"], t["mean_value_lookups"]))
    b = res["tmc_bias_at_seed_noise"]
    L += ["", "Truncation at the seed noise of w(N) (tolerance %.4f): max |bias| %.4f." % (b["tolerance"], b["max_abs_bias"])]
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


LIVE = ROOT.parent / "compute" / "almgsi_campaign" / "results" / "campaigns"
ALMGSI_GAMES = {"pbe": "qe_pbe_shapley_coalitions", "hse06": "qe_hse06_shapley_coalitions"}
ALMGSI_NAMES = {"mace_relax": "MACE-MP-0 relaxation", "gpumd_nep89_md": "NEP89 MD", "lammps_meam_md": "MEAM MD",
                "archive_mp": "MP archive", "qe_pbe": "QE PBE"}


def load_almgsi(tag, mode, path=None):
    path = path or (LIVE / tag / "coalitions.json")
    d = json.loads(path.read_text(encoding="utf-8"))[mode]
    players = d["players"]

    def mask(key):
        return sum(1 << players.index(p) for p in key.split("+") if p)
    avg = {mask(k): float(v) for k, v in d["value"].items()}
    per_run = {}
    for k, vals in d["per_run"].items():
        for r, x in zip(d["runs"], vals):
            per_run.setdefault(r, {})[mask(k)] = float(x)
    assert len(avg) == 1 << len(players) and all(len(g) == len(avg) for g in per_run.values())
    norm = lambda g: {m: v - g[0] for m, v in g.items()}
    return players, norm(avg), {r: norm(g) for r, g in per_run.items()}


def pair_check(vals, players, a, b):
    n = len(players)
    if a not in players or b not in players:
        return None
    i, j = players.index(a), players.index(b)
    rest = [vals[m | (1 << i) | (1 << j)] - vals[m | (1 << i)]
            for m in range(1 << n) if not m & ((1 << i) | (1 << j)) and m]
    lo = loo(vals, n)
    return {"pair": [a, b], "loo": [float(lo[i]), float(lo[j])],
            "second_alone": float(vals[(1 << i) | (1 << j)] - vals[1 << i]),
            "second_mean_with_others": float(np.mean(rest)),
            "second_range_with_others": [float(min(rest)), float(max(rest))]}


def main_almgsi(out):
    rows = []
    L = ["# Experiment 20, second part: data-valuation estimators on the computed Al-Mg-Si games", "",
         "Early recall area (share of the 10 most stable compounds found early). Games: run average and 40 "
         "per-run games (k = 1 and 4, 20 seeds), every coalition measured by compute/almgsi_campaign/campaign.py.", ""]
    for rec, tag in ALMGSI_GAMES.items():
        summ = json.loads((LIVE / tag / "summary.json").read_text(encoding="utf-8"))
        for mode in ("pooled_fixed", "pooled_learned"):
            players, avg, per_run = load_almgsi(tag, mode)
            n = len(players)
            est = estimators(avg, n)
            dev = max(abs(est["shapley"][i] - summ["shapley"][mode]["shapley"][p]) for i, p in enumerate(players))
            assert dev < 1e-12, dev
            full = (1 << n) - 1
            noise = float(np.std([g[full] for g in per_run.values()], ddof=1) / math.sqrt(len(per_run)))
            tmc, bias = tmc_study(avg, n, est["shapley"], noise)
            res = {"experiment": "20_data_valuation_estimators_almgsi", "receiver": "qe_" + rec,
                   "trust": mode.split("_")[1], "players": players, "n_runs": len(per_run),
                   "w_grand": avg[full], "w_grand_run_se": noise, "estimators": list(est),
                   "values": {e: v.tolist() for e, v in est.items()},
                   "near_duplicate_pbe_mace": pair_check(avg, players, "qe_pbe", "mace_relax"),
                   "consistency": consistency(per_run, n, est), "tmc": tmc, "tmc_bias_at_run_noise": bias,
                   "check_vs_campaign_shapley": dev}
            name = "almgsi_%s_%s" % (rec, res["trust"])
            write_json(res, out / (name + ".json"))
            rows.append(res)
            L += ["## Receiver QE %s, %s trust (w(N) = %+.4f)" % (rec.upper(), res["trust"], avg[full]), "",
                  "| Donor | " + " | ".join(est) + " |", "|---" * (len(est) + 1) + "|"]
            for i, p in enumerate(players):
                L.append("| %s | " % ALMGSI_NAMES[p] + " | ".join("%+.4f" % est[e][i] for e in est) + " |")
            L += ["", "| Estimator | mean pairwise Spearman (780 run pairs) | runs with sign flip vs own Shapley |",
                  "|---|---|---|"]
            for e, c in res["consistency"].items():
                L.append("| %s | %.3f | %d/%d |" % (e, c["mean_pairwise_spearman"],
                                                   c["seeds_with_sign_flip_vs_own_shapley"], len(per_run)))
            pc = res["near_duplicate_pbe_mace"]
            if pc:
                L += ["", "QE PBE and MACE-MP-0 relaxation: LOO %+.4f, %+.4f; second of the pair alone %+.4f; "
                      "with other donors mean %+.4f (range %+.4f to %+.4f)." % (
                          *pc["loo"], pc["second_alone"], pc["second_mean_with_others"], *pc["second_range_with_others"])]
            t3 = [t for t in res["tmc"] if t["permutations"] == 3 * n]
            L += ["", "TMC at %d permutations (3n): sign flips in %s of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); "
                  "truncation at the run noise of w(N) biases by at most %.4f." % (
                      3 * n, ", ".join(str(t["repeats_with_sign_flip"]) for t in t3), bias["max_abs_bias"]), ""]
    (out / "almgsi_data_valuation.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print((out / "almgsi_data_valuation.md").read_text(encoding="utf-8"))

HOT = ROOT.parent / "compute" / "almgsi_campaign" / "results_T" / "analysis"
HOT_ENGINES = {"lammps_meam_md": "MEAM MD", "gpumd_nep89_md": "NEP89 MD", "mace_md": "MACE-MP-0 MD"}


def hot_label(src):
    eng, _, t = src.partition("@")
    if eng in HOT_ENGINES:
        return "%s %s" % (HOT_ENGINES[eng], t.replace("K", " K"))
    return {"mace_relax": "MACE-MP-0 relaxation", "qe_pbe": "QE PBE", "qe_hse06": "QE HSE06"}[eng]


HOT_VARIANTS = {
    "seeds": ("coalitions.json", "almgsi_hot",
              "Runs differ only in the campaign seed, which breaks exact ties; with a donor present every run makes the "
              "same choices, so the per-run games differ only in v(empty) and the consistency columns are not a noise test."),
    "sem": ("coalitions_sem.json", "almgsi_hot_sem",
            "Each run draws every MD value (receiver and donors) from a normal distribution with the measured standard "
            "error of its time average (temperature_coalitions.py --resample-sem); 0 K sources are fixed. This is the "
            "run-to-run noise from MD sampling."),
}


def distinct_nonempty(per_run):
    runs = list(per_run.values())
    keys = [m for m in runs[0] if m]
    full = max(keys)
    # per-run games are normalised by v(empty); compare non-empty values relative to v(N)
    return len({tuple(round(g[m] - g[full], 9) for m in keys) for g in runs})


def main_almgsi_hot(out, variant="seeds"):
    fname, prefix, note = HOT_VARIANTS[variant]
    ref = json.loads((HOT / "temperature_study.json").read_text(encoding="utf-8"))["ateki"]
    L = ["# Experiment 20, third part: data-valuation estimators on the higher-temperature MD games (%s)" % variant, "",
         "Early recall area (share of the 10 most stable candidates found in the early quarter of the receiver's MD "
         "budget). Games: run average and 20 per-run games (k = 4, 20 runs), 64 coalitions each, every coalition "
         "run by compute/almgsi_campaign/temperature_coalitions.py. " + note, ""]
    summary = []
    for rec in ref:
        path = HOT / "coalitions" / rec.replace("@", "_") / fname
        for mode in ("pooled_learned", "pooled_fixed"):
            players, avg, per_run = load_almgsi(None, mode, path)
            n = len(players)
            est = estimators(avg, n)
            dev = None
            if mode == "pooled_learned" and variant == "seeds":
                dev = max(abs(est["shapley"][i] - ref[rec]["shapley"][p]) for i, p in enumerate(players))
                assert dev < 1e-12, dev
            full = (1 << n) - 1
            noise = float(np.std([g[full] for g in per_run.values()], ddof=1) / math.sqrt(len(per_run)))
            tmc, bias = tmc_study(avg, n, est["shapley"], noise)
            pairs = [pair_check(avg, players, "qe_pbe@0K", "qe_hse06@0K")]
            if rec.startswith("mace_md"):
                pairs.append(pair_check(avg, players, "mace_relax@0K", "mace_md@300K"))
            cons = consistency(per_run, n, est)
            lo, sh = est["loo"], est["shapley"]
            res = {"experiment": "20_data_valuation_estimators_almgsi_hot", "receiver": rec,
                   "trust": mode.split("_")[1], "players": players, "n_runs": len(per_run),
                   "w_grand": avg[full], "w_grand_run_se": noise, "estimators": list(est),
                   "values": {e: v.tolist() for e, v in est.items()}, "near_duplicate_pairs": pairs,
                   "consistency": cons, "tmc": tmc, "tmc_bias_at_run_noise": bias,
                   "check_vs_temperature_study": dev, "variant": variant,
                   "distinct_nonempty_run_games": distinct_nonempty(per_run),
                   "top_by": {e: players[int(np.argmax(v))] for e, v in est.items()},
                   "bottom_by": {e: players[int(np.argmin(v))] for e, v in est.items()},
                   "loo_shapley_sign_disagreements": [players[i] for i in range(n)
                                                      if np.sign(round(lo[i], 12)) != np.sign(round(sh[i], 12))]}
            name = "%s_%s_%s" % (prefix, rec.replace("@", "_"), res["trust"])
            write_json(res, out / (name + ".json"))
            summary.append(res)
            L += ["## Receiver %s, %s trust (w(N) = %+.4f, run s.e. %.4f, %d distinct per-run games)" % (
                hot_label(rec), res["trust"], avg[full], noise, res["distinct_nonempty_run_games"]), "",
                  "| Donor | " + " | ".join(est) + " |", "|---" * (len(est) + 1) + "|"]
            for i, p in enumerate(players):
                L.append("| %s | " % hot_label(p) + " | ".join("%+.4f" % est[e][i] for e in est) + " |")
            L += ["", "| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |",
                  "|---|---|---|"]
            for e, c in cons.items():
                L.append("| %s | %.3f | %d/%d |" % (e, c["mean_pairwise_spearman"],
                                                   c["seeds_with_sign_flip_vs_own_shapley"], len(per_run)))
            for pc in pairs:
                if pc:
                    L += ["", "%s and %s: LOO %+.4f, %+.4f; second of the pair alone %+.4f; with other donors mean %+.4f "
                          "(range %+.4f to %+.4f)." % (hot_label(pc["pair"][0]), hot_label(pc["pair"][1]), *pc["loo"],
                                                      pc["second_alone"], pc["second_mean_with_others"],
                                                      *pc["second_range_with_others"])]
            t3 = [t for t in tmc if t["permutations"] == 3 * n]
            L += ["", "TMC at %d permutations (3n): sign flips in %s of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); "
                  "truncation at the run noise of w(N) biases by at most %.4f." % (
                      3 * n, ", ".join(str(t["repeats_with_sign_flip"]) for t in t3), bias["max_abs_bias"]), ""]
    # cross-game summary
    L += ["## Summary over the 12 games", "",
          "Mean pairwise Spearman over all 12 games: " + ", ".join(
              "%s %.3f" % (e, float(np.mean([r["consistency"][e]["mean_pairwise_spearman"] for r in summary])))
              for e in summary[0]["estimators"]) + ".", "",
          "| Receiver | trust | w(N) | top (Shapley) | top (LOO) | bottom (Shapley) | bottom (LOO) | LOO/Shapley sign disagreements | Spearman Shapley | Spearman Banzhaf | Spearman Beta(16,1) | TMC 3n flips (tol 0) |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in summary:
        c = r["consistency"]
        t0 = [t for t in r["tmc"] if t["permutations"] == 3 * len(r["players"]) and t["tolerance_fraction_of_wN"] == 0][0]
        L.append("| %s | %s | %+.3f | %s | %s | %s | %s | %d | %.3f | %.3f | %.3f | %d/50 |" % (
            hot_label(r["receiver"]), r["trust"], r["w_grand"], hot_label(r["top_by"]["shapley"]),
            hot_label(r["top_by"]["loo"]), hot_label(r["bottom_by"]["shapley"]), hot_label(r["bottom_by"]["loo"]),
            len(r["loo_shapley_sign_disagreements"]), c["shapley"]["mean_pairwise_spearman"],
            c["banzhaf"]["mean_pairwise_spearman"], c["beta_16_1"]["mean_pairwise_spearman"],
            t0["repeats_with_sign_flip"]))
    write_json({"games": [{k: r[k] for k in ("receiver", "trust", "w_grand", "top_by", "bottom_by",
                                            "loo_shapley_sign_disagreements")} for r in summary]},
               out / (prefix + "_summary.json"))
    (out / (prefix + "_data_valuation.md")).write_text("\n".join(L) + "\n", encoding="utf-8")
    print((out / (prefix + "_data_valuation.md")).read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--almgsi", action="store_true", help="run the second part on the Al-Mg-Si games")
    ap.add_argument("--almgsi-hot", action="store_true", help="run the third part on the higher-temperature MD games")
    ap.add_argument("--input", default=str(DEFAULT_IN))
    ap.add_argument("--cache", default=str(DEFAULT_CACHE))
    ap.add_argument("--output-dir", default=str(DEFAULT_OUT))
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if not self_test():
        sys.exit("self-test failed")
    if args.self_test:
        return
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    if args.almgsi:
        main_almgsi(out)
        return
    if args.almgsi_hot:
        main_almgsi_hot(out, "seeds")
        main_almgsi_hot(out, "sem")
        return
    for window in ("early", "final"):
        players, names, avg, per_seed = load_games(args.input, args.cache, window)
        n = len(players)
        est = estimators(avg, n)
        ref = json.loads(Path(args.input).read_text(encoding="utf-8"))
        ref = ref["exact" if window == "early" else "exact_final_window"]
        dev = max(abs(est[k][i] - ref[k][p]) for k in ("shapley", "banzhaf", "loo") for i, p in enumerate(players))
        assert dev < 1e-12, dev
        full = (1 << n) - 1
        noise = float(np.std([g[full] for g in per_seed.values()], ddof=1) / math.sqrt(len(per_seed)))
        tmc, bias = tmc_study(avg, n, est["shapley"], noise)
        res = {"experiment": "20_data_valuation_estimators", "window": window,
               "players": players, "donor_names": names, "n_seeds": len(per_seed),
               "w_grand": avg[full], "w_grand_seed_se": noise,
               "estimators": list(est), "values": {e: v.tolist() for e, v in est.items()},
               "duplicates": duplicate_check(avg, players),
               "duplicates_per_seed_loo": {s: [float(x) for x in loo(g, n)[[players.index(p) for p in DUPLICATES]]]
                                           for s, g in per_seed.items()},
               "consistency": consistency(per_seed, n, est),
               "tmc": tmc, "tmc_bias_at_seed_noise": bias,
               "check_vs_experiment_08": dev}
        suffix = "" if window == "early" else "_final"
        write_json(res, out / ("data_valuation_estimators%s.json" % suffix))
        write_md(res, out / ("data_valuation_estimators%s.md" % suffix))
        print((out / ("data_valuation_estimators%s.md" % suffix)).read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
