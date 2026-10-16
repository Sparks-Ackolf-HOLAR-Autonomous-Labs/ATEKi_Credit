"""Experiment 15: several decision bodies of the same kind as separate players.

Question (ATEKi): a team may hold several bodies of one kind, for example
three random scouts, or two copies of one interatomic potential run by two
group members. Should the audit treat them as one body or as several, and
how is the credit divided among bodies that are nominally the same?

A body is defined by its decision rule AND by what it outputs in the
campaign. Two copies of one kind give different outputs for two reasons:
  * internal randomness: each random scout draws its own ordering (its own
    seed), as two LLM agents of one model at nonzero temperature or two MD
    runs started from different velocities would;
  * different information: two copies of one potential mixed with the same
    surrogate rule see different receiver results when the team does not
    share results, so their orderings separate during the campaign.
When neither applies (copies that repeat one draw, or copies of a
deterministic rule that see the same results) the copies give identical
outputs at every step and are one body counted several times.

Setting: the computed Al-Mg-Si campaign of experiment 14 (receivers QE PBE,
QE HSE06, GPAW r2SCAN; batches of 4; value = early-window recall area of the
ten most stable compounds). Every coalition of every game is run with the
SAME matched campaign seed, so the differences between coalitions are due
to their members only, and exact Shapley values are computed per campaign.

Games (players; team organisation of experiment 14):
  scouts_indep_m  MACE-MP-0 relaxation, active learner, m random scouts with
                  independent draws (m = 1..4); flat team (results shared)
  scouts_clone_m  same, but the m scouts repeat one draw (m = 2..4)
  mace_shared     active learner, one random scout, two MACE-MP-0 copies;
                  flat team: the copies see the same results
  mace_separate   same players, team without communication: each copy sees
                  only the results it proposed
For scouts_indep_m the type-level game, in which all m scouts enter or
leave together as one player, is evaluated on the same coalition values.

Outputs: results/replicated_bodies/replicated_bodies.{json,md}
Usage (from ateki/, environment with numpy, scipy, ase):
    python experiments/15_replicated_bodies.py --selftest
    python experiments/15_replicated_bodies.py --seeds 200
ASCII only.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import math
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("e14", HERE / "14_emergent_swarm.py")
E14 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(E14)
C = E14.C

OUT = HERE.parent / "results" / "replicated_bodies"
RECEIVERS = ["qe_pbe", "qe_hse06", "gpaw_r2scan"]


def campaign_values(env, members, structure, seeds, receiver):
    """Early recall area per matched campaign seed (seed independent of the coalition)."""
    out = np.empty(len(seeds))
    for j, s in enumerate(seeds):
        r = E14.run(env, list(members), structure, E14.crc(f"exp15|{receiver}|{s}"), max_frac=0.3)
        out[j] = C.summarise(r["curve"], env.total)["early_recall_area"]
    return out


def game(env, players, structure, seeds, receiver):
    v = {}
    for r in range(len(players) + 1):
        for S in itertools.combinations(players, r):
            v[frozenset(S)] = campaign_values(env, S, structure, seeds, receiver)
    return v


def shapley(v, players):
    """Exact Shapley; v maps frozenset -> per-campaign value array, so phi is per campaign."""
    n = len(players)
    phi = {}
    for p in players:
        others = [q for q in players if q != p]
        acc = 0.0
        for r in range(n):
            w = math.factorial(r) * math.factorial(n - r - 1) / math.factorial(n)
            for S in itertools.combinations(others, r):
                acc = acc + w * (v[frozenset(S) | {p}] - v[frozenset(S)])
        phi[p] = acc
    return phi


def ci90(a, rng):
    b = [rng.choice(a, len(a)).mean() for _ in range(2000)]
    return [float(np.percentile(b, 5)), float(np.percentile(b, 95))]


def summarise(v, players, copies, rng):
    phi = shapley(v, players)
    N = frozenset(players)
    out = {"players": players, "v_empty": float(v[frozenset()].mean()), "v_all": float(v[N].mean()),
           "shapley": {p: {"mean": float(phi[p].mean()), "ci90": ci90(phi[p], rng),
                           "sd_over_campaigns": float(phi[p].std(ddof=1)),
                           "frac_campaigns_positive": float((phi[p] > 1e-12).mean())} for p in players}}
    if len(copies) >= 2:
        c1, c2 = copies[0], copies[1]
        diff = phi[c1] - phi[c2]
        e = frozenset()
        div = v[frozenset([c1, c2])] - v[frozenset([c1])] - v[frozenset([c2])] + v[e]
        out["copies"] = {
            "names": copies,
            "credit_total_mean": float(sum(phi[c] for c in copies).mean()),
            "credit_total_ci90": ci90(sum(phi[c] for c in copies), rng),
            "mean_abs_credit_gap": float(np.abs(diff).mean()),
            "frac_campaigns_gap_gt_0p01": float((np.abs(diff) > 0.01).mean()),
            "frac_campaigns_copy1_higher": float((diff > 1e-12).mean()),
            "pair_dividend_mean": float(div.mean()),
            "pair_dividend_ci90": ci90(div, rng),
        }
    return out, phi


def type_level(v, base, copies, rng):
    """Game in which all copies enter or leave together as one player 'scouts'."""
    T = "scouts"
    tv = {}
    for r in range(len(base) + 2):
        for S in itertools.combinations(base + [T], r):
            real = [x for x in S if x != T] + (copies if T in S else [])
            tv[frozenset(S)] = v[frozenset(real)]
    phi = shapley(tv, base + [T])
    return {p: {"mean": float(phi[p].mean()), "ci90": ci90(phi[p], rng)} for p in base + [T]}


def output_divergence(env, members, structure, seeds, receiver):
    """Fraction of batches in which two copies of a potential give different orderings.

    Only the two copies are in the team; the orderings compared are the surrogate parts of their
    scores (the donor part is identical by construction), recorded at every batch."""
    calls = []
    orig = E14.surrogate

    def rec(env_, vis, todo):
        out = orig(env_, vis, todo)
        calls.append(out)
        return out
    E14.surrogate = rec
    diff = []
    try:
        for s in seeds:
            calls.clear()
            E14.run(env, list(members), structure, E14.crc(f"exp15|{receiver}|{s}"), max_frac=0.3)
            diff += [not np.array_equal(a, b) for a, b in zip(calls[0::2], calls[1::2])]
    finally:
        E14.surrogate = orig
    return float(np.mean(diff)), len(diff)


def selftest():
    env = E14.Env("qe_pbe")
    seeds = range(3)
    ok = []
    # 1. clone scouts give identical outputs: credits equal in every campaign
    pl = ["mace_relax", "surrogate", "explorer=1", "explorer=2"]
    v = game(env, pl, "flat", seeds, "qe_pbe")
    phi = shapley(v, pl)
    ok.append(bool(np.allclose(phi["explorer=1"], phi["explorer=2"])))
    # 2. efficiency per campaign
    tot = sum(phi[p] for p in pl)
    ok.append(bool(np.allclose(tot, v[frozenset(pl)] - v[frozenset()])))
    # 3. a single scout copy "explorer=1" behaves as the plain explorer of experiment 14
    a = campaign_values(env, ["mace_relax", "explorer"], "flat", seeds, "qe_pbe")
    b = campaign_values(env, ["mace_relax", "explorer=1"], "flat", seeds, "qe_pbe")
    ok.append(bool(np.allclose(a, b)))
    # 4. independent scouts draw different orderings
    a = campaign_values(env, ["explorer#1"], "flat", range(10), "qe_pbe")
    b = campaign_values(env, ["explorer#2"], "flat", range(10), "qe_pbe")
    ok.append(bool(not np.allclose(a, b)))
    # 5. type-level game satisfies efficiency
    pl = ["mace_relax", "surrogate", "explorer#1", "explorer#2"]
    v = game(env, pl, "flat", seeds, "qe_pbe")
    tl = type_level(v, ["mace_relax", "surrogate"], ["explorer#1", "explorer#2"], np.random.default_rng(0))
    ok.append(abs(sum(x["mean"] for x in tl.values()) - (v[frozenset(pl)] - v[frozenset()]).mean()) < 1e-12)
    print("selftest", sum(ok), "/", len(ok), ok)
    return all(ok)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--seeds", type=int, default=200)
    ap.add_argument("--max-scouts", type=int, default=4)
    args = ap.parse_args()
    if args.selftest:
        raise SystemExit(0 if selftest() else 1)
    OUT.mkdir(parents=True, exist_ok=True)
    seeds = list(range(args.seeds))
    rng = np.random.default_rng(15)
    res = {"seeds": args.seeds, "metric": "early_recall_area", "batch": 4, "receivers": {}}
    t0 = time.time()
    for rec in RECEIVERS:
        env = E14.Env(rec)
        R = {}
        base = ["mace_relax", "surrogate"]
        for m in range(1, args.max_scouts + 1):
            cop = [f"explorer#{j}" for j in range(1, m + 1)]
            v = game(env, base + cop, "flat", seeds, rec)
            s, phi = summarise(v, base + cop, cop, rng)
            s["type_level"] = type_level(v, base, cop, rng)
            if m == 3:
                s["per_campaign_shapley"] = {p: x.round(5).tolist() for p, x in phi.items()}
            R[f"scouts_indep_{m}"] = s
            if m >= 2:
                cop = [f"explorer={j}" for j in range(1, m + 1)]
                v = game(env, base + cop, "flat", seeds, rec)
                s, _ = summarise(v, base + cop, cop, rng)
                s["type_level"] = type_level(v, base, cop, rng)
                R[f"scouts_clone_{m}"] = s
            print(rec, "scouts", m, f"{time.time() - t0:.0f}s", flush=True)
        pl = ["surrogate", "explorer", "mace_relax#1", "mace_relax#2"]
        for name, st in (("mace_shared", "flat"), ("mace_separate", "solo")):
            v = game(env, pl, st, seeds, rec)
            s, phi = summarise(v, pl, ["mace_relax#1", "mace_relax#2"], rng)
            s["structure"] = st
            s["per_campaign_shapley"] = {p: x.round(5).tolist() for p, x in phi.items()}
            f, nb = output_divergence(env, ["mace_relax#1", "mace_relax#2"], st, seeds, rec)
            s["copies"]["frac_batches_outputs_differ"] = f
            s["copies"]["n_batches"] = nb
            R[name] = s
        res["receivers"][rec] = R
        tmp = OUT / "replicated_bodies.json.tmp"
        tmp.write_text(json.dumps(res, indent=1), encoding="utf-8")
        tmp.replace(OUT / "replicated_bodies.json")
    write_md(res)
    print("done", f"{time.time() - t0:.0f}s")


def write_md(res):
    L = ["# Experiment 15: several bodies of one kind as separate players", "",
         f"Computed Al-Mg-Si campaign, batches of 4, {res['seeds']} matched campaigns per coalition; "
         "value = early-window recall area of the ten most stable compounds. Shapley values are exact "
         "and computed per campaign (mean, 90% bootstrap interval of the mean).", ""]
    for rec, R in res["receivers"].items():
        L += [f"## Receiver {rec}", "",
              "| game | v(empty) | v(all) | credit of all copies | type-level credit | |gap| between two copies | campaigns with gap > 0.01 | pair dividend | batches with different outputs |",
              "|---|---|---|---|---|---|---|---|---|"]
        for g, s in R.items():
            c = s.get("copies", {})
            tl = s.get("type_level", {}).get("scouts", {}).get("mean")
            L.append(f"| {g} | {s['v_empty']:.3f} | {s['v_all']:.3f} | "
                     f"{c.get('credit_total_mean', float('nan')):+.3f} | "
                     f"{'' if tl is None else f'{tl:+.3f}'} | {c.get('mean_abs_credit_gap', float('nan')):.3f} | "
                     f"{c.get('frac_campaigns_gap_gt_0p01', float('nan')):.2f} | "
                     f"{c.get('pair_dividend_mean', float('nan')):+.3f} | "
                     f"{c.get('frac_batches_outputs_differ', float('nan')):.2f} |")
        L.append("")
        for g in ("scouts_indep_3", "mace_shared", "mace_separate"):
            if g in R:
                L.append(f"Shapley, {g}: " + ", ".join(
                    f"{p} {x['mean']:+.3f} [{x['ci90'][0]:+.3f}, {x['ci90'][1]:+.3f}]"
                    for p, x in R[g]["shapley"].items()))
                L.append("")
    (OUT / "replicated_bodies.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
