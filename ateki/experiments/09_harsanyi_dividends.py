"""
Experiment 09: Harsanyi dividends (Moebius inversion) of the measured
seven-database coalition game of experiment 08.

Question: experiment 08 found that the full seven-donor pool
(v(N) = +0.682) scores below the best four-donor coalitions (+0.764),
i.e. the coalition value function over the Boolean lattice of donor
subsets is non-monotone. Which higher-order interactions between donor
databases produce that non-monotonicity?

Method (no new campaigns; uses ONLY the committed coalition cache):
  * v(S) for all 2^7 = 128 donor subsets S, read from
    results/database_attribution/<receiver>/database_attribution.json
    (coalition_values_early) and cross-checked against the per-coalition
    checkpoint files results/database_attribution/coalitions/<receiver>/
    <bitmask>.json (which also carry the per-seed values).
  * Harsanyi dividends by Moebius inversion on the subset lattice,
        d(S) = sum_{T subset S} (-1)^{|S|-|T|} v(T),
    computed with the fast (bitwise) Moebius transform and checked
    against the brute-force double sum. By construction
        v(S) = sum_{T subset S} d(T)   (zeta transform; checked).
  * Shapley from dividends, phi_i = sum_{S containing i} d(S)/|S|, and
    Banzhaf from dividends, beta_i = sum_{S containing i} d(S)/2^{|S|-1};
    both compared with the committed exact values of experiment 08.
  * Dividend mass by coalition order |S| = 1..7 (signed sum and sum of
    absolute values), largest positive and negative higher-order
    (|S| >= 2) dividends, the full pairwise-dividend matrix, and the
    inclusion-exclusion decomposition of v(N) - v(S*) for the best
    four-donor coalitions S*.
  * Per-seed dividends (Moebius inversion is linear in v, so the mean of
    per-seed dividends equals the dividend of the seed-mean game;
    checked) with percentile-bootstrap 95% CIs over the matched seeds.

Usage (from ateki/):
    uv run python experiments/09_harsanyi_dividends.py --self-test
    uv run python experiments/09_harsanyi_dividends.py
Outputs: results/harsanyi_dividends/<receiver>/harsanyi_dividends.{json,md,png}
ASCII only; deterministic (--boot-seed).
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ATEKI = HERE.parent
SINGULAR = ATEKI.parent
STYLE_DIR = SINGULAR / "writings" / "papers_2026"

FRIENDLY_NAME = {
    "mp_gga": "MP GGA",
    "mp_r2scan": "MP r2SCAN",
    "mp_gga_expsynth": "MP GGA (ICSD-provenance subset)",
    "jarvis_optb88vdw": "JARVIS OptB88vdW",
    "jarvis_mbj": "JARVIS TBmBJ",
    "snumat_gga": "SNUMAT GGA",
    "snumat_hse": "SNUMAT HSE06",
}

SHORT_NAME = {
    "mp_gga": "MP GGA",
    "mp_r2scan": "MP r2SCAN",
    "mp_gga_expsynth": "MP GGA (ICSD)",
    "jarvis_optb88vdw": "JARVIS OptB88",
    "jarvis_mbj": "JARVIS TBmBJ",
    "snumat_gga": "SNUMAT GGA",
    "snumat_hse": "SNUMAT HSE06",
}


def friendly(d: str) -> str:
    return FRIENDLY_NAME.get(d, d)


# ---------------------------------------------------------------------------
# Lattice transforms (bitmask indexing: bit j <-> donors[j], as in exp 08)
# ---------------------------------------------------------------------------

def popcount(m: int) -> int:
    return bin(m).count("1")


def moebius_fast(v: np.ndarray) -> np.ndarray:
    """d = Moebius inverse of v on the subset lattice (O(n 2^n))."""
    d = np.array(v, dtype=float).copy()
    n = int(round(math.log2(len(d))))
    for j in range(n):
        bit = 1 << j
        for m in range(len(d)):
            if m & bit:
                d[m] -= d[m ^ bit]
    return d


def moebius_brute(v: np.ndarray) -> np.ndarray:
    """Literal double sum d(S) = sum_{T subset S} (-1)^{|S|-|T|} v(T)."""
    out = np.zeros(len(v))
    for S in range(len(v)):
        T = S
        acc = 0.0
        while True:
            acc += (-1) ** (popcount(S) - popcount(T)) * v[T]
            if T == 0:
                break
            T = (T - 1) & S
        out[S] = acc
    return out


def zeta(d: np.ndarray) -> np.ndarray:
    """v(S) = sum_{T subset S} d(T)."""
    v = np.array(d, dtype=float).copy()
    n = int(round(math.log2(len(v))))
    for j in range(n):
        bit = 1 << j
        for m in range(len(v)):
            if m & bit:
                v[m] += v[m ^ bit]
    return v


def shapley_from_dividends(d: np.ndarray, n: int) -> np.ndarray:
    phi = np.zeros(n)
    for S in range(1, len(d)):
        k = popcount(S)
        for j in range(n):
            if S & (1 << j):
                phi[j] += d[S] / k
    return phi


def banzhaf_from_dividends(d: np.ndarray, n: int) -> np.ndarray:
    beta = np.zeros(n)
    for S in range(1, len(d)):
        k = popcount(S)
        for j in range(n):
            if S & (1 << j):
                beta[j] += d[S] / 2 ** (k - 1)
    return beta


def shapley_direct(v: np.ndarray, n: int) -> np.ndarray:
    """Permutation-weight formula, eq. (1) of the ATEKi paper."""
    phi = np.zeros(n)
    for j in range(n):
        bit = 1 << j
        for S in range(len(v)):
            if S & bit:
                continue
            s = popcount(S)
            w = math.factorial(s) * math.factorial(n - s - 1) / math.factorial(n)
            phi[j] += w * (v[S | bit] - v[S])
    return phi


def members(mask: int, donors: list[str]) -> list[str]:
    return [d for j, d in enumerate(donors) if mask & (1 << j)]


# ---------------------------------------------------------------------------
# Self-test: toy games with known dividends
# ---------------------------------------------------------------------------

def self_test() -> int:
    failures = 0

    def report(ok: bool, msg: str) -> None:
        nonlocal failures
        print("[%s] %s" % ("PASS" if ok else "FAIL", msg))
        failures += 0 if ok else 1

    # (1) Unanimity game u_T on 4 players, T = {0, 2}: d(T) = 1, else 0;
    #     Shapley = 1/2 for players 0 and 2, 0 otherwise.
    n = 4
    T = 0b0101
    v = np.array([1.0 if (S & T) == T else 0.0 for S in range(1 << n)])
    d = moebius_fast(v)
    expect = np.zeros(1 << n)
    expect[T] = 1.0
    report(np.allclose(d, expect, atol=0, rtol=0),
           "unanimity game u_{0,2}: single unit dividend on {0,2}")
    phi = shapley_from_dividends(d, n)
    report(np.allclose(phi, [0.5, 0.0, 0.5, 0.0], atol=1e-15),
           "unanimity game Shapley = (1/2, 0, 1/2, 0)")

    # (2) Hand game on 3 players: v(a)=1, v(b)=2, v(ab)=5 (d(ab)=+2),
    #     v(c)=0, v(ac)=1, v(bc)=1 (d(bc)=-1), v(abc)=4 (d(abc)=4-5-1-1
    #     +1+2+0 = 0).
    v3 = np.zeros(8)
    v3[0b001], v3[0b010], v3[0b100] = 1.0, 2.0, 0.0
    v3[0b011], v3[0b101], v3[0b110], v3[0b111] = 5.0, 1.0, 1.0, 4.0
    d3 = moebius_fast(v3)
    known = {0b001: 1.0, 0b010: 2.0, 0b100: 0.0, 0b011: 2.0,
             0b101: 0.0, 0b110: -1.0, 0b111: 0.0}
    report(all(abs(d3[m] - x) < 1e-15 for m, x in known.items()),
           "3-player hand game: dividends (a,b,c,ab,ac,bc,abc) = "
           "(1,2,0,2,0,-1,0)")

    # (3) Random dividends on 7 players -> zeta -> Moebius recovers them;
    #     fast == brute; Shapley via dividends == permutation formula;
    #     efficiency sum(phi) = v(N) - v(empty).
    rng = np.random.default_rng(20260927)
    n = 7
    d_true = rng.normal(0.0, 1.0, size=1 << n)
    v7 = zeta(d_true)
    d_fast = moebius_fast(v7)
    d_brute = moebius_brute(v7)
    report(np.max(np.abs(d_fast - d_true)) < 1e-12,
           "random 7-player game: Moebius(zeta(d)) recovers d "
           "(max err %.1e)" % np.max(np.abs(d_fast - d_true)))
    report(np.max(np.abs(d_fast - d_brute)) < 1e-12,
           "fast Moebius == brute-force double sum (max err %.1e)"
           % np.max(np.abs(d_fast - d_brute)))
    phi_d = shapley_from_dividends(d_fast, n)
    phi_p = shapley_direct(v7, n)
    report(np.max(np.abs(phi_d - phi_p)) < 1e-12,
           "Shapley from dividends == permutation formula (max err %.1e)"
           % np.max(np.abs(phi_d - phi_p)))
    report(abs(phi_d.sum() - (v7[-1] - v7[0])) < 1e-12,
           "efficiency from dividends")

    # (4) Symmetric redundant pair (identical players i, j, marginal of
    #     the second copy zero): v(i)=v(j)=v(ij)=a > v(empty)=0 gives
    #     d(ij) = -a, the redundancy signature used in the analysis.
    v2 = np.array([0.0, 0.3, 0.3, 0.3])
    d2 = moebius_fast(v2)
    report(abs(d2[3] + 0.3) < 1e-15,
           "redundant identical pair: d(ij) = -v(i) (= -0.3)")

    print("self-test: %s" % ("PASS (%d checks)" % 8 if failures == 0
                             else "FAIL (%d failures)" % failures))
    return failures


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def bootstrap_ci(samples: np.ndarray, rng, n_boot: int) -> list[float]:
    idx = rng.integers(0, len(samples), size=(n_boot, len(samples)))
    means = samples[idx].mean(axis=1)
    return [float(np.percentile(means, 2.5)),
            float(np.percentile(means, 97.5))]


def analyse(receiver: str, n_boot: int, boot_seed: int) -> dict:
    src = ATEKI / "results" / "database_attribution" / receiver / \
        "database_attribution.json"
    with open(src, encoding="utf-8") as fh:
        res = json.load(fh)
    donors = list(res["donors"])
    n = len(donors)
    N = 1 << n
    cv = res["coalition_values_early"]
    assert len(cv) == N, "expected %d coalition values, found %d" % (N, len(cv))
    v = np.array([float(cv[str(m)]) for m in range(N)])

    # Cross-check against the per-coalition checkpoints; collect per-seed.
    ck_dir = ATEKI / "results" / "database_attribution" / "coalitions" / receiver
    seed_list = [str(s) for s in res["config"]["seed_list"]]
    per_seed = np.zeros((len(seed_list), N))
    max_ck_gap = 0.0
    for m in range(N):
        with open(ck_dir / ("%d.json" % m), encoding="utf-8") as fh:
            ck = json.load(fh)
        assert ck["bitmask"] == m and list(ck["donors"]) == donors
        assert sorted(ck["members"]) == sorted(members(m, donors))
        max_ck_gap = max(max_ck_gap, abs(ck["value_early"] - v[m]))
        for i, s in enumerate(seed_list):
            per_seed[i, m] = ck["per_seed_early"][s]
    assert max_ck_gap < 1e-12, max_ck_gap

    d = moebius_fast(v)
    d_brute = moebius_brute(v)
    moebius_gap = float(np.max(np.abs(d - d_brute)))
    zeta_gap = float(np.max(np.abs(zeta(d) - v)))

    phi = shapley_from_dividends(d, n)
    beta = banzhaf_from_dividends(d, n)
    phi_c = np.array([res["exact"]["shapley"][x] for x in donors])
    beta_c = np.array([res["exact"]["banzhaf"][x] for x in donors])
    shap_gap = float(np.max(np.abs(phi - phi_c)))
    banz_gap = float(np.max(np.abs(beta - beta_c)))

    # Per-seed dividends and linearity check.
    d_seed = np.array([moebius_fast(per_seed[i]) for i in range(len(seed_list))])
    lin_gap = float(np.max(np.abs(d_seed.mean(axis=0) - d)))
    rng = np.random.default_rng(boot_seed)

    def ci(mask: int) -> list[float]:
        return bootstrap_ci(d_seed[:, mask], rng, n_boot)

    # Mass by order.
    by_order = []
    for k in range(1, n + 1):
        ms = [m for m in range(1, N) if popcount(m) == k]
        vals = d[ms]
        seed_net = d_seed[:, ms].sum(axis=1)
        by_order.append({
            "order": k,
            "n_coalitions": len(ms),
            "sum": float(vals.sum()),
            "sum_abs": float(np.abs(vals).sum()),
            "sum_positive": float(vals[vals > 0].sum()),
            "sum_negative": float(vals[vals < 0].sum()),
            "n_positive": int((vals > 0).sum()),
            "n_negative": int((vals < 0).sum()),
            "sum_ci95_over_seeds": bootstrap_ci(seed_net, rng, n_boot),
        })
    total_nonempty = float(d[1:].sum())

    # Largest higher-order dividends.
    hi = [m for m in range(1, N) if popcount(m) >= 2]
    hi_sorted = sorted(hi, key=lambda m: d[m])

    def entry(m: int) -> dict:
        return {"bitmask": m, "order": popcount(m),
                "members": members(m, donors),
                "members_named": [friendly(x) for x in members(m, donors)],
                "dividend": float(d[m]), "ci95_over_seeds": ci(m)}

    top_pos = [entry(m) for m in hi_sorted[::-1][:8]]
    top_neg = [entry(m) for m in hi_sorted[:8]]

    # Pairwise matrix.
    pair = np.zeros((n, n))
    for a, b in itertools.combinations(range(n), 2):
        pair[a, b] = pair[b, a] = d[(1 << a) | (1 << b)]
    pairs_sorted = sorted(
        [entry((1 << a) | (1 << b)) for a, b in itertools.combinations(range(n), 2)],
        key=lambda e: e["dividend"])

    # SNUMAT pair.
    ig, ih = donors.index("snumat_gga"), donors.index("snumat_hse")
    sn_mask = (1 << ig) | (1 << ih)
    snumat = entry(sn_mask)
    snumat.update({
        "v_empty": float(v[0]), "v_snumat_gga": float(v[1 << ig]),
        "v_snumat_hse": float(v[1 << ih]), "v_both": float(v[sn_mask]),
        "rank_among_all_pairwise_dividends": 1 + [e["bitmask"] for e in
                                                  pairs_sorted].index(sn_mask),
        "abs_to_largest_singleton_dividend":
            float(abs(d[sn_mask]) / np.max(np.abs(d[[1 << j for j in range(n)]]))),
    })
    # Redundancy of the pair in every context: v(S+g+h) - v(S+g) for S
    # without either SNUMAT source (the marginal of the second copy).
    rest = [m for m in range(N) if not (m & sn_mask)]
    second_copy = np.array([v[m | sn_mask] - v[m | (1 << ig)] for m in rest])
    swap_gap = np.array([v[m | (1 << ig)] - v[m | (1 << ih)] for m in rest])
    snumat["second_copy_marginal"] = {
        "n_contexts": len(rest), "mean": float(second_copy.mean()),
        "min": float(second_copy.min()), "max": float(second_copy.max())}
    snumat["gga_vs_hse_single_swap_max_abs_gap"] = float(np.max(np.abs(swap_gap)))

    # Seven lose to four: v(N) - v(S*) = sum of d(T), T not subset of S*.
    grand = N - 1
    four = [m for m in range(N) if popcount(m) == 4]
    best4_val = max(v[m] for m in four)
    best4 = [m for m in four if abs(v[m] - best4_val) < 1e-9]
    decomp = []
    for m in best4:
        # T not a subset of m  <=>  T has a member outside m
        outside = [T for T in range(1, N) if (T & ~m & grand)]
        by_k = {}
        for T in outside:
            by_k.setdefault(popcount(T), 0.0)
            by_k[popcount(T)] += d[T]
        tot = float(sum(d[T] for T in outside))
        decomp.append({
            "bitmask": m, "members": members(m, donors),
            "members_named": [friendly(x) for x in members(m, donors)],
            "excluded_named": [friendly(x) for x in donors
                               if x not in members(m, donors)],
            "v_S": float(v[m]), "v_N": float(v[grand]),
            "v_N_minus_v_S": float(v[grand] - v[m]),
            "sum_dividends_outside_S": tot,
            "identity_gap": float(abs(tot - (v[grand] - v[m]))),
            "outside_by_order": {str(k): float(x) for k, x in sorted(by_k.items())},
        })
    best_overall = int(np.argmax(v))

    # Best attainable value per coalition size.
    best_by_size = []
    for k in range(0, n + 1):
        ms = [m for m in range(N) if popcount(m) == k]
        mb = max(ms, key=lambda m: v[m])
        best_by_size.append({"size": k, "v_best": float(v[mb]),
                             "members_named": [friendly(x) for x in
                                               members(mb, donors)]})

    # Share of order-2 dividend mass on pairs containing a SNUMAT source.
    sn_pairs = [e for e in pairs_sorted
                if "snumat_gga" in e["members"] or "snumat_hse" in e["members"]]
    order2 = {
        "n_pairs_with_snumat": len(sn_pairs),
        "n_negative_pairs_with_snumat": sum(e["dividend"] < 0 for e in sn_pairs),
        "sum_pairs_with_snumat": float(sum(e["dividend"] for e in sn_pairs)),
        "sum_pairs_without_snumat": float(sum(
            e["dividend"] for e in pairs_sorted if e not in sn_pairs)),
    }

    return {
        "experiment": "09_harsanyi_dividends",
        "receiver": receiver,
        "source": str(src.relative_to(SINGULAR)).replace("\\", "/"),
        "checkpoint_dir": str(ck_dir.relative_to(SINGULAR)).replace("\\", "/"),
        "window": "early (primary window of exp 08)",
        "donors": donors,
        "donor_names": {x: friendly(x) for x in donors},
        "n_coalitions": N,
        "n_seeds": len(seed_list),
        "n_boot": n_boot, "boot_seed": boot_seed,
        "v_empty": float(v[0]), "v_grand": float(v[grand]),
        "best_coalition": {"bitmask": best_overall,
                           "members_named": [friendly(x) for x in
                                             members(best_overall, donors)],
                           "v": float(v[best_overall])},
        "checks": {
            "checkpoint_vs_json_max_gap": max_ck_gap,
            "moebius_fast_vs_brute_max_gap": moebius_gap,
            "zeta_roundtrip_max_gap": zeta_gap,
            "shapley_from_dividends_vs_committed_max_gap": shap_gap,
            "banzhaf_from_dividends_vs_committed_max_gap": banz_gap,
            "sum_nonempty_dividends_minus_(vN-v0)":
                float(total_nonempty - (v[grand] - v[0])),
            "per_seed_linearity_max_gap": lin_gap,
        },
        "shapley_from_dividends": {x: float(phi[j]) for j, x in enumerate(donors)},
        "banzhaf_from_dividends": {x: float(beta[j]) for j, x in enumerate(donors)},
        "singleton_dividends": {x: float(d[1 << j]) for j, x in enumerate(donors)},
        "mass_by_order": by_order,
        "total_abs_mass_nonempty": float(np.abs(d[1:]).sum()),
        "interaction_net_orders_2_to_n": float(d[1:].sum() - sum(
            d[1 << j] for j in range(n))),
        "best_value_by_size": best_by_size,
        "order2_snumat_breakdown": order2,
        "largest_positive_higher_order": top_pos,
        "largest_negative_higher_order": top_neg,
        "pairwise_dividends_sorted": pairs_sorted,
        "snumat_pair": snumat,
        "seven_vs_best_four": decomp,
        "dividends_all": {str(m): float(d[m]) for m in range(N)},
    }


def fmt_members(e: dict) -> str:
    return " + ".join(e["members_named"])


def write_markdown(r: dict, path: Path) -> None:
    L = []
    L.append("# Experiment 09: Harsanyi dividends of the seven-database game")
    L.append("")
    L.append("Receiver `%s`; characteristic function = the %d measured "
             "coalition values of experiment 08 (%s window; source `%s`, "
             "cross-checked against `%s`). No new campaigns were run."
             % (r["receiver"], r["n_coalitions"], r["window"], r["source"],
                r["checkpoint_dir"]))
    L.append("")
    L.append("d(S) = sum_{T subset S} (-1)^{|S|-|T|} v(T) (Moebius inversion "
             "on the subset lattice). v(empty) = %+.4f, v(N) = %+.4f; best "
             "coalition: %s, v = %+.4f."
             % (r["v_empty"], r["v_grand"],
                " + ".join(r["best_coalition"]["members_named"]),
                r["best_coalition"]["v"]))
    L.append("")
    L.append("## Checks")
    L.append("")
    for k, x in r["checks"].items():
        L.append("- %s: %.2e" % (k, x))
    L.append("")
    L.append("## Dividend mass by coalition order")
    L.append("")
    L.append("| order | #coalitions | sum d | sum abs d | sum d>0 | sum d<0 | "
             "#pos | #neg | sum d, 95% CI over seeds |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for o in r["mass_by_order"]:
        L.append("| %d | %d | %+.4f | %.4f | %+.4f | %+.4f | %d | %d | "
                 "[%+.4f, %+.4f] |"
                 % (o["order"], o["n_coalitions"], o["sum"], o["sum_abs"],
                    o["sum_positive"], o["sum_negative"], o["n_positive"],
                    o["n_negative"], o["sum_ci95_over_seeds"][0],
                    o["sum_ci95_over_seeds"][1]))
    L.append("")
    L.append("Total |d| over nonempty coalitions: %.4f; v(N) - v(empty) = "
             "%+.4f; net of orders 2..7 = %+.4f."
             % (r["total_abs_mass_nonempty"], r["v_grand"] - r["v_empty"],
                r["interaction_net_orders_2_to_n"]))
    L.append("")
    o2 = r["order2_snumat_breakdown"]
    L.append("Order-2 split: the %d pairs containing a SNUMAT source sum to "
             "%+.4f (%d of them negative); the remaining pairs sum to %+.4f."
             % (o2["n_pairs_with_snumat"], o2["sum_pairs_with_snumat"],
                o2["n_negative_pairs_with_snumat"],
                o2["sum_pairs_without_snumat"]))
    L.append("")
    L.append("## Best attainable value by coalition size")
    L.append("")
    L.append("| size | best v(S) | coalition |")
    L.append("|---|---|---|")
    for b in r["best_value_by_size"]:
        L.append("| %d | %+.4f | %s |" % (b["size"], b["v_best"],
                                          " + ".join(b["members_named"]) or
                                          "(cold campaign)"))
    L.append("")
    L.append("## Largest positive higher-order dividends (|S| >= 2)")
    L.append("")
    L.append("| order | coalition | d(S) | 95% CI over seeds |")
    L.append("|---|---|---|---|")
    for e in r["largest_positive_higher_order"]:
        L.append("| %d | %s | %+.4f | [%+.4f, %+.4f] |"
                 % (e["order"], fmt_members(e), e["dividend"],
                    e["ci95_over_seeds"][0], e["ci95_over_seeds"][1]))
    L.append("")
    L.append("## Largest negative higher-order dividends (|S| >= 2)")
    L.append("")
    L.append("| order | coalition | d(S) | 95% CI over seeds |")
    L.append("|---|---|---|---|")
    for e in r["largest_negative_higher_order"]:
        L.append("| %d | %s | %+.4f | [%+.4f, %+.4f] |"
                 % (e["order"], fmt_members(e), e["dividend"],
                    e["ci95_over_seeds"][0], e["ci95_over_seeds"][1]))
    L.append("")
    L.append("## Singleton dividends d({i}) = v({i}) - v(empty)")
    L.append("")
    for x, val in sorted(r["singleton_dividends"].items(), key=lambda t: -t[1]):
        L.append("- %s: %+.4f" % (friendly(x), val))
    L.append("")
    L.append("## All pairwise dividends (sorted)")
    L.append("")
    L.append("| pair | d(S) | 95% CI over seeds |")
    L.append("|---|---|---|")
    for e in r["pairwise_dividends_sorted"]:
        L.append("| %s | %+.4f | [%+.4f, %+.4f] |"
                 % (fmt_members(e), e["dividend"], e["ci95_over_seeds"][0],
                    e["ci95_over_seeds"][1]))
    L.append("")
    s = r["snumat_pair"]
    L.append("## SNUMAT GGA / SNUMAT HSE06 pair")
    L.append("")
    L.append("- v(empty) = %+.4f, v(SNUMAT GGA) = %+.4f, v(SNUMAT HSE06) = "
             "%+.4f, v(both) = %+.4f" % (s["v_empty"], s["v_snumat_gga"],
                                         s["v_snumat_hse"], s["v_both"]))
    L.append("- pairwise dividend d = %+.4f (95%% CI over seeds [%+.4f, "
             "%+.4f]); rank %d of 21 pairwise dividends (1 = most negative); "
             "|d| is %.2f x the largest singleton dividend"
             % (s["dividend"], s["ci95_over_seeds"][0],
                s["ci95_over_seeds"][1], s["rank_among_all_pairwise_dividends"],
                s["abs_to_largest_singleton_dividend"]))
    sc = s["second_copy_marginal"]
    L.append("- marginal value of adding the second SNUMAT source to a "
             "coalition already holding the first, over all %d contexts: "
             "mean %+.4f, min %+.4f, max %+.4f"
             % (sc["n_contexts"], sc["mean"], sc["min"], sc["max"]))
    L.append("- max |v(S + SNUMAT GGA) - v(S + SNUMAT HSE06)| over contexts: "
             "%.2e (interchangeable players)"
             % s["gga_vs_hse_single_swap_max_abs_gap"])
    L.append("")
    L.append("## Seven lose to four: inclusion-exclusion decomposition")
    L.append("")
    L.append("v(N) - v(S*) = sum of d(T) over every T with a member outside "
             "S*, for each best four-donor coalition S*.")
    L.append("")
    for e in r["seven_vs_best_four"]:
        L.append("- S* = %s (v = %+.4f; excluded: %s): v(N) - v(S*) = %+.4f; "
                 "by order of T: %s; identity gap %.1e"
                 % (" + ".join(e["members_named"]), e["v_S"],
                    ", ".join(e["excluded_named"]), e["v_N_minus_v_S"],
                    ", ".join("%s: %+.4f" % (k, x) for k, x in
                              e["outside_by_order"].items()),
                    e["identity_gap"]))
    L.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")


def write_plot(r: dict, path: Path) -> None:
    sys.path.insert(0, str(STYLE_DIR))
    import paper_fig_style as st  # noqa: E402
    import matplotlib.pyplot as plt  # noqa: E402

    st.apply_style()
    fig, axes = plt.subplots(1, 2, figsize=(st.TMLR_FULL, 2.9),
                             gridspec_kw={"width_ratios": [0.9, 1.1]})

    ax = axes[0]
    orders = [o["order"] for o in r["mass_by_order"]]
    pos = [o["sum_positive"] for o in r["mass_by_order"]]
    neg = [o["sum_negative"] for o in r["mass_by_order"]]
    net = [o["sum"] for o in r["mass_by_order"]]
    lo = [o["sum"] - o["sum_ci95_over_seeds"][0] for o in r["mass_by_order"]]
    hi = [o["sum_ci95_over_seeds"][1] - o["sum"] for o in r["mass_by_order"]]
    x = np.arange(len(orders))
    ax.bar(x, pos, width=0.62, color=st.MP_BLUE, alpha=0.85,
           label="positive")
    ax.bar(x, neg, width=0.62, color=st.ACCENT_RED, alpha=0.85,
           label="negative")
    ax.errorbar(x, net, yerr=[lo, hi], fmt="D", color=st.INK, ms=3.5,
                lw=0.8, capsize=2, label="net (95% CI over seeds)")
    ax.axhline(0, color=st.INK, lw=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels(["%d\n(%d)" % (o["order"], o["n_coalitions"])
                        for o in r["mass_by_order"]])
    ax.set_xlabel("coalition order |S| (number of coalitions)")
    ax.set_ylabel(r"dividend mass (Kendall $\tau$)")
    ax.set_title("(a) Harsanyi dividend mass by order", loc="left")
    lo_y, hi_y = ax.get_ylim()
    ax.set_ylim(lo_y - 0.32 * (hi_y - lo_y), hi_y)
    ax.legend(loc="lower left", ncol=2, fontsize=7, handlelength=1.0,
              columnspacing=0.8, handletextpad=0.4, borderaxespad=0.2)

    ax = axes[1]
    donors = r["donors"]
    order = sorted(range(len(donors)),
                   key=lambda j: -r["shapley_from_dividends"][donors[j]])
    n = len(donors)
    M = np.full((n, n), np.nan)
    dall = r["dividends_all"]
    for a in range(n):
        for b in range(n):
            if a > b:
                M[a, b] = 100.0 * dall[str((1 << order[a]) | (1 << order[b]))]
    # Drop the empty first row and last column of the lower triangle.
    M = M[1:, :-1]
    # Symmetric colour range clipped at +-8 so the 20 moderate cells are
    # readable; the one cell beyond the range (the SNUMAT GGA/HSE06 pair)
    # keeps its printed value and is outlined.
    lim = 8.0
    im = ax.imshow(M, cmap="RdBu", vmin=-lim, vmax=lim)
    ax.grid(False)
    # no spines or tick marks on the triangle, so cell labels at the
    # left edge (e.g. the SNUMAT pair) are not cut by the axis line
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    for a in range(n - 1):
        for b in range(n - 1):
            if not np.isnan(M[a, b]):
                ax.text(b, a, "%+.1f" % M[a, b], ha="center", va="center",
                        fontsize=7,
                        color="white" if abs(M[a, b]) > 0.6 * lim else st.INK)
                if abs(M[a, b]) > lim:
                    ax.add_patch(plt.Rectangle((b - 0.5, a - 0.5), 1, 1,
                                               fill=False, ec=st.INK, lw=1.0))
    names = [st.SOURCE_NAMES.get(donors[j], donors[j]) for j in order]
    names = [nm.replace("MP GGA (ICSD-matched)", "MP GGA (ICSD)")
             for nm in names]
    ax.set_xticks(range(n - 1))
    ax.set_yticks(range(n - 1))
    ax.set_xticklabels(names[:-1], rotation=40, ha="right", fontsize=7)
    ax.set_yticklabels(names[1:], fontsize=7)
    ax.set_title(r"(b) Pair dividends, $100\,d(\{i,j\})$", loc="left")
    cb = fig.colorbar(im, ax=ax, shrink=0.9, pad=0.02, extend="both")
    cb.ax.tick_params(labelsize=7)
    # cells hold 100 d({i,j}), i.e. dividends in units of 0.01 Kendall tau
    cb.set_label(r"pair dividend (10$^{-2}$ Kendall $\tau$)", fontsize=7)
    st.save(fig, path)


def main() -> int:
    ap = argparse.ArgumentParser(description="ATEKi exp 09: Harsanyi "
                                 "dividends of the exp 08 database game")
    ap.add_argument("--receiver", default="expt_zhuo")
    ap.add_argument("--n-boot", type=int, default=10000)
    ap.add_argument("--boot-seed", type=int, default=20260927)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return 1 if self_test() else 0
    if self_test():
        print("self-test failed; aborting")
        return 1

    r = analyse(args.receiver, args.n_boot, args.boot_seed)
    tol = 1e-12
    for k in ("moebius_fast_vs_brute_max_gap", "zeta_roundtrip_max_gap",
              "shapley_from_dividends_vs_committed_max_gap",
              "banzhaf_from_dividends_vs_committed_max_gap",
              "per_seed_linearity_max_gap"):
        assert r["checks"][k] < tol, (k, r["checks"][k])
    out = ATEKI / "results" / "harsanyi_dividends" / args.receiver
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "harsanyi_dividends.json", "w", encoding="utf-8") as fh:
        json.dump(r, fh, indent=2)
    write_markdown(r, out / "harsanyi_dividends.md")
    write_plot(r, out / "harsanyi_dividends.png")
    print("wrote %s" % out)
    for o in r["mass_by_order"]:
        print("order %d: sum %+.4f  sum|d| %.4f" % (o["order"], o["sum"],
                                                    o["sum_abs"]))
    print("checks:", json.dumps(r["checks"], indent=1))
    print("SNUMAT pair dividend %+.4f" % r["snumat_pair"]["dividend"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
