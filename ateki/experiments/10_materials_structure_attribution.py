"""
Experiment 10: estimator disagreement, team-structure weighting, and
conference structures on the measured seven-database band-gap game.

Inputs are the 128 cached coalition values of experiment 08 (seven donor
databases advising the experimental band-gap campaign, receiver expt_zhuo).
No campaign is re-run: every value below is a lookup into those measured
coalition campaigns.

The game is zero-normalised before any structural restriction:
    w(S) = v(S) - v(empty),
i.e. the Kendall-tau gain over the cold campaign. Shapley, Banzhaf and LOO
are invariant to this shift; the graph and hypergraph restrictions are not
(they sum values over components, so an un-normalised v(empty) would be
counted once per component).

Three analyses:
  (a) baseline: exact Shapley, Banzhaf and leave-one-out; rank and sign
      disagreements of the low-cost estimators against Shapley, plus the
      per-seed frequency of each disagreement (10 matched seeds);
  (b) team structure: star (supervisor) topology with each database as hub
      in turn; betweenness weighting, degree weighting (topology-weight
      equation of the ATEKi paper, additive efficiency shift) and the Myerson value of
      the star-restricted game;
  (c) conference structures: the three database organisations as meetings
      (MP: 3 sources, JARVIS: 2, SNUMAT: 2) joined by one cross-organisation
      beyond-GGA meeting {MP r2SCAN, JARVIS TBmBJ, SNUMAT HSE06}; the
      hypergraph Myerson value against its clique expansion, the
      unrestricted Shapley value and a best-LOO star; a variant adds the
      GGA-level meeting {MP GGA, JARVIS OptB88vdW, SNUMAT GGA}; and the k=2
      reduction check (clique edges fed to the hypergraph code as pure
      pairs reproduce the graph Myerson value).

Usage:
    uv run python experiments/10_materials_structure_attribution.py
    uv run python experiments/10_materials_structure_attribution.py --self-test
    uv run python experiments/10_materials_structure_attribution.py --window final
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np

from analysis.shapley import (
    ShapleyEngine,
    BanzhafEngine,
    GraphRestrictedValue,
    HypergraphRestrictedValue,
    check_pairwise_reduction,
)
from analysis.topology import SupervisorTopology, CustomTopology
from analysis.reports import write_json

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IN = ROOT / "results" / "database_attribution" / "expt_zhuo" / "database_attribution.json"
DEFAULT_CACHE = ROOT / "results" / "database_attribution" / "coalitions" / "expt_zhuo"
DEFAULT_OUT = ROOT / "results" / "materials_structure_attribution"
TOL = 1e-9

ORGANISATIONS = {
    "MP": ["mp_gga", "mp_gga_expsynth", "mp_r2scan"],
    "JARVIS": ["jarvis_optb88vdw", "jarvis_mbj"],
    "SNUMAT": ["snumat_gga", "snumat_hse"],
}
BEYOND_GGA = ["mp_r2scan", "jarvis_mbj", "snumat_hse"]
GGA_LEVEL = ["mp_gga", "jarvis_optb88vdw", "snumat_gga"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def mask_of(S, donors):
    m = 0
    for j, d in enumerate(donors):
        if d in S:
            m |= 1 << j
    return m


def make_game(values_by_mask, donors):
    """Zero-normalised lookup game w(S) = v(S) - v(empty)."""
    v0 = values_by_mask[0]

    def w(S):
        return values_by_mask[mask_of(S, donors)] - v0
    return w


def ranks_of(scores):
    """1-based competition rank, descending; exact ties share a rank."""
    out = {}
    for p, s in scores.items():
        out[p] = 1 + sum(1 for q, t in scores.items() if t > s + 1e-12)
    return out


def adjacency(players, edges):
    idx = {p: i for i, p in enumerate(players)}
    a = np.zeros((len(players), len(players)))
    for x, y in edges:
        a[idx[x], idx[y]] = a[idx[y], idx[x]] = 1.0
    return a


def clique_expansion(hyperedges):
    es = set()
    for e in hyperedges:
        for x, y in itertools.combinations(sorted(e), 2):
            es.add((x, y))
    return sorted(es)


def apply_topology_weights(phi, weights, grand):
    """Eq. (topoweight): n*w_i*phi_i plus an additive efficiency shift.
    Identical to experiments/02_topology_comparison.apply_topology_weights."""
    n = len(phi)
    mean_w = sum(weights[p] for p in phi) / n
    if mean_w < 1e-12:
        mean_w = 1.0
    raw = {p: phi[p] * weights[p] / mean_w for p in phi}
    shift = (grand - sum(raw.values())) / n
    return {p: raw[p] + shift for p in phi}


def exact(players, fn):
    return ShapleyEngine(players, fn).exact().scores


def loo_of(players, fn):
    N = frozenset(players)
    return {p: fn(N) - fn(N - {p}) for p in players}


# ---------------------------------------------------------------------------
# (a) Baseline estimators
# ---------------------------------------------------------------------------

def baseline(players, w):
    sh = exact(players, w)
    bz = BanzhafEngine(players, w).exact().scores
    lo = loo_of(players, w)
    r = {"shapley": ranks_of(sh), "banzhaf": ranks_of(bz), "loo": ranks_of(lo)}
    sign_flips = {
        est: [p for p in players
              if np.sign(round(vals[p], 12)) != np.sign(round(sh[p], 12))]
        for est, vals in (("banzhaf", bz), ("loo", lo))}
    rank_moves = {
        est: {p: [r["shapley"][p], r[est][p]] for p in players
              if r[est][p] != r["shapley"][p]}
        for est in ("banzhaf", "loo")}
    bottom = {est: sorted(p for p, v in vals.items() if v == min(vals.values()))
              for est, vals in (("shapley", sh), ("banzhaf", bz), ("loo", lo))}
    return {"shapley": sh, "banzhaf": bz, "loo": lo, "ranks": r,
            "sign_flips_vs_shapley": sign_flips,
            "rank_moves_vs_shapley": rank_moves,
            "bottom_player": bottom,
            "efficiency_gap": abs(sum(sh.values()) - w(frozenset(players)))}


def per_seed_disagreement(players, cache_dir, window):
    """Per matched seed: does LOO / Banzhaf pick the same bottom player as
    Shapley, and does any player change sign?"""
    key = "per_seed_%s" % window
    files = sorted(cache_dir.glob("*.json"))
    if len(files) != 1 << len(players):
        return None
    per_seed_vals = {}
    for f in files:
        with open(f, encoding="utf-8") as fh:
            c = json.load(fh)
        assert c["donors"] == players
        for s, val in c[key].items():
            per_seed_vals.setdefault(s, {})[c["bitmask"]] = val
    out = {"n_seeds": len(per_seed_vals), "seeds": {}}
    counts = {"loo_bottom_differs": 0, "banzhaf_bottom_differs": 0,
              "loo_bottom_unique_and_equal": 0, "loo_bottom_excludes_shapley_bottom": 0,
              "loo_any_sign_flip": 0, "banzhaf_any_sign_flip": 0,
              "loo_top_differs": 0, "banzhaf_top_differs": 0}
    for s, vals in sorted(per_seed_vals.items()):
        b = baseline(players, make_game(vals, players))
        sb = set(b["bottom_player"]["shapley"])
        top = {est: {p for p, v in b[est].items() if v == max(b[est].values())}
               for est in ("shapley", "banzhaf", "loo")}
        rec = {"shapley_bottom": sorted(sb),
               "loo_bottom": b["bottom_player"]["loo"],
               "banzhaf_bottom": b["bottom_player"]["banzhaf"],
               "loo_sign_flips": b["sign_flips_vs_shapley"]["loo"],
               "banzhaf_sign_flips": b["sign_flips_vs_shapley"]["banzhaf"]}
        out["seeds"][s] = rec
        counts["loo_bottom_differs"] += int(set(rec["loo_bottom"]) != sb)
        counts["loo_bottom_unique_and_equal"] += int(set(rec["loo_bottom"]) == sb and len(sb) == 1)
        counts["loo_bottom_excludes_shapley_bottom"] += int(not (set(rec["loo_bottom"]) & sb))
        counts["banzhaf_bottom_differs"] += int(set(rec["banzhaf_bottom"]) != sb)
        counts["loo_top_differs"] += int(top["loo"] != top["shapley"])
        counts["banzhaf_top_differs"] += int(top["banzhaf"] != top["shapley"])
        counts["loo_any_sign_flip"] += int(bool(rec["loo_sign_flips"]))
        counts["banzhaf_any_sign_flip"] += int(bool(rec["banzhaf_sign_flips"]))
    out["counts"] = counts
    return out


# ---------------------------------------------------------------------------
# (b) Star topology sweep
# ---------------------------------------------------------------------------

def star_analysis(players, w, sh, hub):
    grand = w(frozenset(players))
    topo = SupervisorTopology(players, supervisor_id=hub).build()
    bc = topo.betweenness_centrality
    dc_w = topo.communication_weight  # degree-normalised weights
    bc_w = CustomTopology(players, topo.adjacency, weight_by="betweenness").build().communication_weight
    deg_weighted = apply_topology_weights(sh, dc_w, grand)
    bet_weighted = apply_topology_weights(sh, bc_w, grand)
    my = exact(players, GraphRestrictedValue(players, w, topo.adjacency))
    leaves = [p for p in players if p != hub]

    def leaf_order(sc):
        return sorted(leaves, key=lambda p: (-sc[p], p))
    raw_leaf = leaf_order(sh)
    return {
        "hub": hub,
        "betweenness": bc,
        "betweenness_weight": bc_w,
        "degree_weight": dc_w,
        "raw_shapley": sh,
        "betweenness_weighted": bet_weighted,
        "degree_weighted": deg_weighted,
        "myerson": my,
        "myerson_efficiency_gap": abs(sum(my.values()) - grand),
        "betweenness_leaves_all_equal": (max(bet_weighted[p] for p in leaves)
                                         - min(bet_weighted[p] for p in leaves)) < 1e-12,
        "degree_keeps_leaf_order": leaf_order(deg_weighted) == raw_leaf,
        "myerson_keeps_leaf_order": leaf_order(my) == raw_leaf,
        "raw_leaf_order": raw_leaf,
        "myerson_leaf_order": leaf_order(my),
        "hub_rank_raw": ranks_of(sh)[hub],
        "hub_rank_myerson": ranks_of(my)[hub],
        "hub_myerson_minus_raw": my[hub] - sh[hub],
    }


# ---------------------------------------------------------------------------
# (c) Conference structures
# ---------------------------------------------------------------------------

def is_connected(players, hyperedges):
    comp = HypergraphRestrictedValue(players, lambda S: 0.0, hyperedges)._components(frozenset(players))
    return len(comp) == 1


def conference_analysis(players, w, sh, hyperedges, hub, label):
    assert is_connected(players, hyperedges), "structure must connect N"
    clique_edges = clique_expansion(hyperedges)
    star_edges = [(hub, p) for p in players if p != hub]
    conds = {
        "none": sh,
        "star": exact(players, GraphRestrictedValue(players, w, adjacency(players, star_edges))),
        "hypergraph": exact(players, HypergraphRestrictedValue(players, w, hyperedges)),
        "clique": exact(players, GraphRestrictedValue(players, w, adjacency(players, clique_edges))),
    }
    pairs = exact(players, HypergraphRestrictedValue(players, w, [list(e) for e in clique_edges]))
    max_dev = max(abs(pairs[p] - conds["clique"][p]) for p in players)
    # coalition-level check as well (all 128 coalitions)
    vh = HypergraphRestrictedValue(players, w, [list(e) for e in clique_edges])
    vg = GraphRestrictedValue(players, w, adjacency(players, clique_edges))
    max_dev_coal = max(abs(vh(frozenset(S)) - vg(frozenset(S)))
                       for r in range(len(players) + 1)
                       for S in itertools.combinations(players, r))
    ranks = {c: ranks_of(v) for c, v in conds.items()}
    grand = w(frozenset(players))
    return {
        "label": label,
        "hyperedges": [sorted(e) for e in hyperedges],
        "clique_edges": [list(e) for e in clique_edges],
        "star_hub": hub,
        "conditions": conds,
        "ranks": ranks,
        "efficiency_gaps": {c: abs(sum(v.values()) - grand) for c, v in conds.items()},
        "rank_moves_hypergraph_vs_none": {p: [ranks["none"][p], ranks["hypergraph"][p]]
                                          for p in players if ranks["none"][p] != ranks["hypergraph"][p]},
        "rank_moves_hypergraph_vs_clique": {p: [ranks["clique"][p], ranks["hypergraph"][p]]
                                            for p in players if ranks["clique"][p] != ranks["hypergraph"][p]},
        "hypergraph_minus_clique": {p: conds["hypergraph"][p] - conds["clique"][p] for p in players},
        "top_player": {c: sorted(p for p in players if ranks[c][p] == 1) for c in conds},
        "k2_reduction": {"max_abs_dev_values": max_dev,
                         "max_abs_dev_coalitions": max_dev_coal,
                         "tolerance": TOL,
                         "passed": max_dev <= TOL and max_dev_coal <= TOL},
    }


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def self_test():
    ok = True
    check_pairwise_reduction(tol=TOL)
    print("[PASS] synthetic pairwise-hypergraph reduction")
    # additive game: every structure that connects N leaves Shapley unchanged?
    # No: restriction changes values in general; but for an ADDITIVE game
    # v(S) = sum a_i the Myerson value equals a_i under any structure.
    players = ["a", "b", "c", "d", "e"]
    a = {"a": 1.0, "b": -2.0, "c": 0.5, "d": 3.0, "e": -0.25}

    def v(S):
        return sum(a[p] for p in S)
    for fn in (GraphRestrictedValue(players, v, adjacency(players, [("a", p) for p in players[1:]])),
               HypergraphRestrictedValue(players, v, [["a", "b", "c"], ["c", "d", "e"]])):
        phi = exact(players, fn)
        good = all(abs(phi[p] - a[p]) < 1e-12 for p in players)
        ok &= good
    print("[%s] additive game invariant under graph and hypergraph restriction"
          % ("PASS" if ok else "FAIL"))
    # star betweenness is hub 1 / leaves 0; degree weights hub 0.5
    t = SupervisorTopology(players, supervisor_id="c").build()
    good = (abs(t.betweenness_centrality["c"] - 1) < 1e-12
            and all(abs(t.betweenness_centrality[p]) < 1e-12 for p in players if p != "c")
            and abs(t.communication_weight["c"] - 0.5) < 1e-12)
    ok &= good
    print("[%s] star centralities (hub BC 1, leaf BC 0, hub degree weight 0.5)"
          % ("PASS" if good else "FAIL"))
    # zero-normalisation: Shapley of v and of v - v(empty) coincide
    def v2(S):
        return 5.0 + sum(a[p] for p in S) ** 2
    def w2(S):
        return v2(S) - 5.0
    p1, p2 = exact(players, v2), exact(players, w2)
    good = all(abs(p1[p] - p2[p]) < 1e-12 for p in players)
    ok &= good
    print("[%s] Shapley invariant to the v(empty) shift" % ("PASS" if good else "FAIL"))
    # bitmask convention of experiment 08
    donors = ["x", "y", "z"]
    good = mask_of({"x", "z"}, donors) == 5 and mask_of(set(), donors) == 0
    ok &= good
    print("[%s] bitmask convention (bit j = donors[j])" % ("PASS" if good else "FAIL"))
    return ok


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------

def fmt(x):
    return "%+.4f" % x


def write_md(res, path, names):
    L = []
    P = res["players"]
    L.append("# Experiment 10: estimator disagreement, team structure and conference structures on the seven-database game")
    L.append("")
    L.append("- Source game: `%s` (receiver %s, %s window, 128 measured coalitions)"
             % (res["input"], res["receiver"], res["window"]))
    L.append("- Zero-normalised game w(S) = v(S) - v(empty); v(empty) = %.4f, w(N) = %.4f"
             % (res["v_empty"], res["w_grand"]))
    L.append("")
    b = res["baseline"]
    L.append("## (a) Baseline estimators")
    L.append("")
    L.append("| Database | Shapley | rank | Banzhaf | rank | LOO | rank |")
    L.append("|---|---|---|---|---|---|---|")
    for p in sorted(P, key=lambda q: -b["shapley"][q]):
        L.append("| %s | %s | %d | %s | %d | %s | %d |" % (
            names[p], fmt(b["shapley"][p]), b["ranks"]["shapley"][p],
            fmt(b["banzhaf"][p]), b["ranks"]["banzhaf"][p],
            fmt(b["loo"][p]), b["ranks"]["loo"][p]))
    L.append("")
    L.append("- Sign flips vs Shapley: %s" % json.dumps(b["sign_flips_vs_shapley"]))
    L.append("- Bottom player: %s" % json.dumps(b["bottom_player"]))
    if res.get("per_seed"):
        L.append("- Per-seed disagreement counts (%d seeds): %s"
                 % (res["per_seed"]["n_seeds"], json.dumps(res["per_seed"]["counts"])))
    L.append("")
    L.append("## (b) Star topology, every database as hub")
    L.append("")
    L.append("| Hub | raw phi(hub) | degree-weighted hub | Myerson hub | hub rank raw -> Myerson | BC leaves tied | degree keeps leaf order | Myerson keeps leaf order |")
    L.append("|---|---|---|---|---|---|---|---|")
    for h, s in res["star_sweep"].items():
        L.append("| %s | %s | %s | %s | %d -> %d | %s | %s | %s |" % (
            names[h], fmt(s["raw_shapley"][h]), fmt(s["degree_weighted"][h]),
            fmt(s["myerson"][h]), s["hub_rank_raw"], s["hub_rank_myerson"],
            s["betweenness_leaves_all_equal"], s["degree_keeps_leaf_order"],
            s["myerson_keeps_leaf_order"]))
    hs = res["star_headline"]
    L.append("")
    L.append("Headline hub: %s" % names[hs["hub"]])
    L.append("")
    L.append("| Database | raw Shapley | betweenness-weighted | degree-weighted | Myerson (star) |")
    L.append("|---|---|---|---|---|")
    for p in sorted(P, key=lambda q: -b["shapley"][q]):
        L.append("| %s | %s | %s | %s | %s |" % (
            names[p] + (" (hub)" if p == hs["hub"] else ""), fmt(hs["raw_shapley"][p]),
            fmt(hs["betweenness_weighted"][p]), fmt(hs["degree_weighted"][p]),
            fmt(hs["myerson"][p])))
    for key in ("conference_primary", "conference_two_fidelity_meetings"):
        c = res[key]
        L.append("")
        L.append("## (c) Conference structure: %s" % c["label"])
        L.append("")
        L.append("Hyperedges: %s" % json.dumps(c["hyperedges"]))
        L.append("")
        L.append("| Database | none | star (hub %s) | hypergraph | clique |" % names[c["star_hub"]])
        L.append("|---|---|---|---|---|")
        for p in sorted(P, key=lambda q: -b["shapley"][q]):
            L.append("| %s | %s (%d) | %s (%d) | %s (%d) | %s (%d) |" % (
                names[p],
                *[x for cond in ("none", "star", "hypergraph", "clique")
                  for x in (fmt(c["conditions"][cond][p]), c["ranks"][cond][p])]))
        L.append("")
        L.append("- Rank moves hypergraph vs none: %s" % json.dumps(c["rank_moves_hypergraph_vs_none"]))
        L.append("- Rank moves hypergraph vs clique: %s" % json.dumps(c["rank_moves_hypergraph_vs_clique"]))
        L.append("- k=2 reduction: %s" % json.dumps(c["k2_reduction"]))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--input", default=str(DEFAULT_IN))
    ap.add_argument("--cache", default=str(DEFAULT_CACHE))
    ap.add_argument("--window", default="early", choices=["early", "final"])
    ap.add_argument("--hub", default="mp_gga",
                    help="headline star hub (default: MP GGA, the largest donor database)")
    ap.add_argument("--output-dir", default=str(DEFAULT_OUT))
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if not self_test():
        sys.exit("self-test failed")
    if args.self_test:
        return

    with open(args.input, encoding="utf-8") as f:
        d = json.load(f)
    players = list(d["donors"])
    names = d["donor_names"]
    vals = {int(k): float(v) for k, v in d["coalition_values_%s" % args.window].items()}
    assert len(vals) == 1 << len(players)
    w = make_game(vals, players)
    grand = w(frozenset(players))

    # (a)
    b = baseline(players, w)
    ref = d["exact" if args.window == "early" else "exact_final_window"]
    dev = max(abs(b[k][p] - ref[k][p]) for k in ("shapley", "banzhaf", "loo") for p in players)
    assert dev < 1e-12, "baseline does not match experiment 08 (%.3e)" % dev
    print("Baseline reproduces experiment 08 exact values (max dev %.1e)" % dev)
    per_seed = per_seed_disagreement(players, Path(args.cache), args.window) \
        if Path(args.cache).is_dir() else None

    # (b)
    sweep = {h: star_analysis(players, w, b["shapley"], h) for h in players}

    # (c)
    orgs = [ORGANISATIONS[k] for k in ("MP", "JARVIS", "SNUMAT")]
    for g in orgs + [BEYOND_GGA, GGA_LEVEL]:
        assert set(g) <= set(players), g
    loo_hub = sorted(players, key=lambda p: (-b["loo"][p], p))[0]
    conf1 = conference_analysis(players, w, b["shapley"], orgs + [BEYOND_GGA], loo_hub,
                                "three organisation meetings + beyond-GGA meeting")
    conf2 = conference_analysis(players, w, b["shapley"], orgs + [BEYOND_GGA, GGA_LEVEL], loo_hub,
                                "three organisation meetings + beyond-GGA + GGA-level meetings")
    for c in (conf1, conf2):
        if not c["k2_reduction"]["passed"]:
            sys.exit("k=2 reduction check failed")

    res = {
        "experiment": "10_materials_structure_attribution",
        "input": os.path.relpath(args.input, ROOT),
        "receiver": d["receiver"],
        "window": args.window,
        "players": players,
        "donor_names": names,
        "organisations": ORGANISATIONS,
        "v_empty": vals[0],
        "v_grand": vals[(1 << len(players)) - 1],
        "w_grand": grand,
        "normalisation": "w(S) = v(S) - v(empty) (Kendall-tau gain over the cold campaign)",
        "baseline": b,
        "per_seed": per_seed,
        "star_sweep": sweep,
        "star_headline": sweep[args.hub],
        "star_sweep_summary": {
            "betweenness_leaves_tied_all_hubs": all(s["betweenness_leaves_all_equal"] for s in sweep.values()),
            "degree_keeps_leaf_order_all_hubs": all(s["degree_keeps_leaf_order"] for s in sweep.values()),
            "myerson_keeps_leaf_order_hubs": [h for h, s in sweep.items() if s["myerson_keeps_leaf_order"]],
            "hub_myerson_minus_raw": {h: s["hub_myerson_minus_raw"] for h, s in sweep.items()},
            "hub_rank_myerson": {h: s["hub_rank_myerson"] for h, s in sweep.items()},
            "hub_rank_raw": {h: s["hub_rank_raw"] for h, s in sweep.items()},
        },
        "conference_primary": conf1,
        "conference_two_fidelity_meetings": conf2,
    }
    out = Path(args.output_dir)
    suffix = "" if args.window == "early" else "_final"
    write_json(res, out / ("materials_structure_attribution%s.json" % suffix))
    write_md(res, out / ("materials_structure_attribution%s.md" % suffix), names)
    print("Saved to %s" % out)
    with open(out / ("materials_structure_attribution%s.md" % suffix), encoding="utf-8") as f:
        print(f.read())


if __name__ == "__main__":
    main()
