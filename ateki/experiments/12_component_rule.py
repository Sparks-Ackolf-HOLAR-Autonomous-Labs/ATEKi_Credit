"""
Experiment 12: sum-of-components versus best-component valuation of a split
team, on the measured seven-database band-gap game (experiment 08 cache).

Myerson's restriction values a coalition S that the communication structure
splits into components C_1..C_m as the SUM of the component values. For a
bounded quality score such as Kendall tau a campaign reports one ranking,
so a split team can also be valued by its BEST component:

    v_sum(S) = sum_j w(C_j)        (Myerson 1977/1980)
    v_max(S) = max_j w(C_j)        (one reported ranking)

where w(S) = v(S) - v(empty) is the zero-normalised game of experiment 10.
Both rules coincide on every coalition the structure keeps connected, so
both values are efficient whenever the structure connects N.

This script recomputes, under both rules, (b) the star (supervisor) sweep
with each database as hub and (c) the two provenance conference structures
(hypergraph value and the clique expansion) of experiment 10. No campaign
is re-run. ASCII only.

Usage:
    python experiments/12_component_rule.py
    python experiments/12_component_rule.py --window final
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from analysis.shapley import ShapleyEngine, HypergraphRestrictedValue
from analysis.reports import write_json

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IN = ROOT / "results" / "database_attribution" / "expt_zhuo" / "database_attribution.json"
DEFAULT_OUT = ROOT / "results" / "component_rule"

ORGS = [["mp_gga", "mp_gga_expsynth", "mp_r2scan"],
        ["jarvis_optb88vdw", "jarvis_mbj"],
        ["snumat_gga", "snumat_hse"]]
BEYOND_GGA = ["mp_r2scan", "jarvis_mbj", "snumat_hse"]
GGA_LEVEL = ["mp_gga", "jarvis_optb88vdw", "snumat_gga"]


class RuleRestricted(HypergraphRestrictedValue):
    """Hypergraph restriction with a choice of component aggregation.
    Graph structures are passed as 2-player hyperedges (exact reduction)."""

    def __init__(self, players, value_fn, hyperedges, rule):
        super().__init__(players, value_fn, hyperedges)
        assert rule in ("sum", "max")
        self.rule = rule

    def __call__(self, S) -> float:
        S = frozenset(S)
        if not S:
            return float(self.value_fn(S))
        vals = [self.value_fn(c) for c in self._components(S)]
        return float(sum(vals) if self.rule == "sum" else max(vals))


def mask_of(S, donors):
    return sum(1 << j for j, d in enumerate(donors) if d in S)


def ranks_of(sc):
    return {p: 1 + sum(1 for t in sc.values() if t > s + 1e-12) for p, s in sc.items()}


def exact(players, fn):
    return dict(ShapleyEngine(players, fn).exact().scores)


def clique(hyperedges):
    es = set()
    for e in hyperedges:
        es.update(itertools.combinations(sorted(e), 2))
    return [list(e) for e in sorted(es)]


def self_test():
    ok = True
    P = ["a", "b", "c"]
    g = {frozenset(): 0.0, frozenset("a"): 0.5, frozenset("b"): 0.4,
         frozenset("c"): 0.1, frozenset("ab"): 0.6, frozenset("ac"): 0.5,
         frozenset("bc"): 0.45, frozenset("abc"): 0.7}
    w = lambda S: g[frozenset(S)]
    star = [["a", "b"], ["a", "c"]]
    for rule in ("sum", "max"):
        v = RuleRestricted(P, w, star, rule)
        # connected coalitions agree with w under both rules
        ok &= abs(v(frozenset("abc")) - 0.7) < 1e-12 and abs(v(frozenset("ab")) - 0.6) < 1e-12
        sh = exact(P, v)
        ok &= abs(sum(sh.values()) - 0.7) < 1e-12
    ok &= abs(RuleRestricted(P, w, star, "sum")(frozenset("bc")) - 0.5) < 1e-12
    ok &= abs(RuleRestricted(P, w, star, "max")(frozenset("bc")) - 0.4) < 1e-12
    print("[%s] component-rule self-test" % ("PASS" if ok else "FAIL"))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(DEFAULT_IN))
    ap.add_argument("--window", default="early", choices=["early", "final"])
    ap.add_argument("--output-dir", default=str(DEFAULT_OUT))
    a = ap.parse_args()
    if not self_test():
        sys.exit("self-test failed")
    d = json.load(open(a.input, encoding="utf-8"))
    P = list(d["donors"])
    vals = {int(k): float(v) for k, v in d["coalition_values_%s" % a.window].items()}
    v0 = vals[0]
    w = lambda S: vals[mask_of(S, P)] - v0
    grand = w(frozenset(P))
    sh = exact(P, w)

    star = {}
    for hub in P:
        edges = [[hub, p] for p in P if p != hub]
        row = {}
        for rule in ("sum", "max"):
            my = exact(P, RuleRestricted(P, w, edges, rule))
            row[rule] = {"values": my, "ranks": ranks_of(my),
                         "efficiency_gap": abs(sum(my.values()) - grand)}
        row["hub_minus_raw"] = {r: row[r]["values"][hub] - sh[hub] for r in ("sum", "max")}
        star[hub] = row

    conf = {}
    for label, H in (("A", ORGS + [BEYOND_GGA]), ("B", ORGS + [BEYOND_GGA, GGA_LEVEL])):
        c = {}
        for kind, edges in (("hyper", H), ("clique", clique(H))):
            for rule in ("sum", "max"):
                my = exact(P, RuleRestricted(P, w, edges, rule))
                c["%s_%s" % (kind, rule)] = {"values": my, "ranks": ranks_of(my),
                                             "top": sorted(p for p in P if ranks_of(my)[p] == 1),
                                             "efficiency_gap": abs(sum(my.values()) - grand)}
        conf[label] = c

    res = {"experiment": "12_component_rule", "window": a.window, "players": P,
           "donor_names": d["donor_names"], "w_grand": grand,
           "unrestricted_shapley": sh, "unrestricted_ranks": ranks_of(sh),
           "star": star, "conference": conf}
    out = Path(a.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    sfx = "" if a.window == "early" else "_final"
    write_json(res, out / ("component_rule%s.json" % sfx))

    nm = d["donor_names"]
    L = ["# Experiment 12: sum vs best-component rule (%s window)" % a.window, "",
         "w(N) = %+.4f; Kendall-tau gain over the cold campaign." % grand, "",
         "## Star: hub value under each rule (raw Shapley in brackets)", "",
         "| hub | raw | hub sum | hub max | hub rank sum | hub rank max |",
         "|---|---:|---:|---:|---:|---:|"]
    for h in P:
        s = star[h]
        L.append("| %s | %+.4f | %+.4f | %+.4f | %d | %d |" % (
            nm.get(h, h), sh[h], s["sum"]["values"][h], s["max"]["values"][h],
            s["sum"]["ranks"][h], s["max"]["ranks"][h]))
    for lab in ("A", "B"):
        L += ["", "## Structure %s" % lab, "",
              "| database | unrestricted | hyper sum | hyper max | clique sum | clique max |",
              "|---|---:|---:|---:|---:|---:|"]
        c = conf[lab]
        for p in sorted(P, key=lambda q: -sh[q]):
            L.append("| %s | %+.4f (%d) | %s | %s | %s | %s |" % (
                nm.get(p, p), sh[p], ranks_of(sh)[p],
                *["%+.4f (%d)" % (c[k]["values"][p], c[k]["ranks"][p])
                  for k in ("hyper_sum", "hyper_max", "clique_sum", "clique_max")]))
    (out / ("component_rule%s.md" % sfx)).write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
