"""Experiment 17: the number of swarms changes during the campaign (merge, nest, split).

Question (ATEKi): in experiment 16 the seven decision bodies were grouped
into swarms that stayed fixed for the whole campaign. In practice groups
combine when their advice agrees, place one group under another when one
is clearly stronger, and separate again when their members stop agreeing.
Does a structure that changes this way, from evidence the campaign itself
produces, outperform the fixed partitions, does it reach the same shape from
different starting partitions, and how is credit divided when the
coalition structure is itself changing?

Setting: the computed Al-Mg-Si campaign of experiments 14 to 16 (receivers
QE PBE, QE HSE06, GPAW r2SCAN; batches of k = 4 candidates paid at the
measured receiver cost; value = early-window recall area of the ten most
stable compounds). Inside every swarm the emergent organisation of
experiment 14 runs unchanged (tiers, temporary cells, promotion rule).

Structure: a list of top-level groups; a group is a head swarm plus zero or
more nested child swarms; a swarm is a list of bodies (two levels of
nesting above the bodies).
  slots     the batch is split between groups by their records (leader
            ratio^2, second ratio, others 1, negative record floor), then
            inside a group between its swarms by the same ladder, then inside
            a swarm between its cells by the experiment-14 tier weights;
            stride credits are held per body, so they survive restructuring
  results   inside a swarm by the experiment-14 rule; in a group the head
            swarm's results are visible to its children and the children's
            results to the head swarm's leader; between groups only when the
            share mode is "published"
  record    q(B) = Kendall tau between the mean pre-reveal score of the bodies
            in B and the receiver value, over all results so far (the
            coordinator that sets slots and structure sees every result; the
            bodies see only what the sharing rule gives them), shrunk by n/(n+8)
  morph     every `period` batches, from the scores the bodies have just given
            the open pool (agreement = Kendall tau between mean scores):
            split     a swarm separates into the components of its agreement
                      graph (edge: agreement >= split; a body with a negative
                      record loses its edges when the swarm has a positive
                      one); a component that still agrees with the head
                      swarm (>= nest) stays nested, the rest leave the group
            detach    a child swarm whose agreement with its head drops below
                      split leaves the group, unless its own record is negative
                      (a separated component with a negative record also
                      stays nested, under supervision)
            promote   a child swarm whose record exceeds its head's by more
                      than delta becomes the head
            adopt     a top-level group with a negative record is placed under
                      the group with the best record, if that exceeds delta
            join      pairs of top-level groups with agreement >= join combine,
                      highest agreement first, each group at most once per
                      step, provided the stronger has a non-negative record:
                      two single swarms with non-negative records within
                      delta fuse into one swarm; otherwise the weaker group
                      nests under the stronger
  All five thresholds are cold-start defaults; a learned set is fitted with
  the cross-entropy method on training seeds disjoint from evaluation seeds.

Modes: fixed (never changes), full, merge_only (join, adopt and promote),
split_only (split, detach and promote), no_nest (fuse, split and detach, no nesting).
Starts: one_7, split_1x7, split_4_3, split_2_5w, split_2_2_3 (experiment 16).

Attribution with a changing structure: the level structure value of Winter
(1989) generalises the Owen value to nested unions (expected marginal
contribution over orderings in which every union at every level is
contiguous). For each campaign seed the structure trajectory of the full
team is logged; the credit is the level structure value averaged over the
structures in force, weighted by the compute spent under each in the early
window. With no unions it is the Shapley value, with one level the Owen
value.

Outputs: results/morphing_swarms/{team_values.json, learned_theta.json, games.json, morphing_swarms.md}
Usage (from ateki/, environment with numpy, scipy, ase):
    python experiments/17_morphing_swarms.py --selftest
    python experiments/17_morphing_swarms.py --stage team --seeds 100 --workers 8
    python experiments/17_morphing_swarms.py --stage learn
    python experiments/17_morphing_swarms.py --stage games --game-seeds 40
ASCII only.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import math
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, HERE / fn)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


E14 = _load("e14", "14_emergent_swarm.py")
E16 = _load("e16", "16_multiple_swarms.py")
C = E14.C
A = E14.AGENTS
OUT = HERE.parent / "results" / "morphing_swarms"
RECEIVERS = ["qe_pbe", "qe_hse06", "gpaw_r2scan"]
GAME_RECEIVERS = ["qe_pbe", "qe_hse06"]
DEBUG = False
STARTS = {k: E16.CONFIGS[k] for k in ("one_7", "split_1x7", "split_4_3", "split_2_5w", "split_2_2_3")}
MODES = ["fixed", "full", "merge_only", "split_only", "no_nest"]
MORPH_DEFAULT = {"join": 0.6, "split": 0.2, "nest": 0.4, "delta": 0.1, "period": 2.0}
MORPH_BOUNDS = {"join": (0.0, 1.01), "split": (-1.01, 0.8), "nest": (0.0, 0.9), "delta": (0.0, 1.0),
                "period": (1.0, 8.0)}


def ladder(q, th):
    """Experiment-14 promotion weights from records: leader ratio^2, second ratio, others 1."""
    q = np.asarray(q, float)
    w = np.ones(len(q))
    if len(q) > 1:
        order = np.argsort(-q, kind="stable")
        w[order[0]] = th["ratio"] ** 2
        w[order[1]] = th["ratio"]
    return np.where(q < 0, th["floor"], w)


def components(nodes, edge):
    parent = {i: i for i in nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in itertools.combinations(nodes, 2):
        if edge(a, b):
            parent[find(a)] = find(b)
    out = {}
    for i in nodes:
        out.setdefault(find(i), []).append(i)
    return list(out.values())


def run_morph(env, start, mode="full", outer="record", share="isolated", seed=0, k=4, theta=None,
              max_frac=None, log=False):
    th = {**E14.DEFAULT_THETA, **MORPH_DEFAULT, **(theta or {})}
    start = [list(s) for s in start if len(s)]
    members = [a for s in start for a in s]
    m = len(members)
    rng = np.random.default_rng(seed)
    n = env.n
    jitter = rng.random(n) * 1e-9
    pos_of = {a: i for i, a in enumerate(members)}
    G = [[[pos_of[a] for a in s]] for s in start]      # groups -> swarms -> body indices
    evald = np.zeros(n, bool)
    vis = np.zeros((m, n), bool)
    proposer = np.full(n, -1)
    pred = np.full((m, n), np.nan)
    scout = rng.random(n)
    ema = np.zeros(m)
    tier = np.full(m, 2)
    cred_g, cred_s, cred_u = np.zeros(m), np.zeros(m), np.zeros(m)
    cost = 0.0
    nb = 0
    curve, events = [], []
    order_rand = rng.permutation(n)
    morph = mode != "fixed"
    do_split = mode in ("full", "split_only", "no_nest")
    do_join = mode in ("full", "merge_only", "no_nest")
    nest_ok = mode in ("full", "merge_only", "split_only")

    def record(ix):
        ix = list(ix)
        # lab-level record: the coordinator that sets slots and structure sees every result
        E = np.flatnonzero(evald)
        if len(E) < 3:
            return 0.0
        return E14.ktau(np.nanmean(pred[ix][:, E], 0), -env.truth[E]) * len(E) / (len(E) + 8)

    def flat(g):
        return [i for s in g for i in s]

    while not evald.all():
        todo = np.flatnonzero(~evald)
        if m == 0:
            batch = [c for c in order_rand if not evald[c]][:k]
            S = None
        else:
            S = np.zeros((m, len(todo)))
            for i, a in enumerate(members):
                kd = E14.body_kind(a)
                if kd == "explorer":
                    S[i] = E14.rank01(scout[todo])
                    continue
                sur = E14.surrogate(env, vis[i], todo)
                if kd == "surrogate":
                    S[i] = sur
                    continue
                ds, have = env.donor[kd]
                E = np.flatnonzero(vis[i] & have)
                t = E14.ktau(ds[E], -env.truth[E]) if len(E) >= 3 else float("nan")
                w = 0.5 if not math.isfinite(t) else max(0.0, t) * len(E) / (len(E) + 8)
                S[i] = w * ds[todo] + (1 - w) * sur
            S += jitter[todo]
            cols = np.arange(len(todo)) if len(todo) <= 60 else rng.choice(len(todo), 60, replace=False)
            base = np.where(tier == 1, th["ratio"] ** 2, np.where(tier == 2, th["ratio"], 1.0))
            base = np.where(ema < 0, th["floor"], base)
            # cells inside every swarm (experiment 14)
            cells = {}
            for g in G:
                for s in g:
                    if th["merge"] <= 1.0 and len(s) > 1:
                        u = components(s, lambda a_, b_: E14.ktau(S[a_, cols], S[b_, cols]) >= th["merge"])
                    else:
                        u = [[i] for i in s]
                    cells[tuple(s)] = u
            kk = min(k, len(todo))
            # slots: groups -> swarms -> cells
            if len(G) == 1:
                gseq = [0] * kk
            else:
                gq = [record(flat(g)) for g in G] if outer == "record" else [0.0] * len(G)
                gw = ladder(gq, th) if outer == "record" else (
                    np.array([len(flat(g)) for g in G], float) if outer == "size" else np.ones(len(G)))
                gseq = E16.unit_sequence(cred_g, gw, [flat(g) for g in G], kk, rng, True)
            slots = []
            for gi in range(len(G)):
                cg = gseq.count(gi)
                if cg == 0:
                    continue
                g = G[gi]
                if len(g) == 1:
                    sseq = [0] * cg
                else:
                    sseq = E16.unit_sequence(cred_s, ladder([record(s) for s in g], th), g, cg, rng, True)
                for si in range(len(g)):
                    cs = sseq.count(si)
                    if cs == 0:
                        continue
                    units = cells[tuple(g[si])]
                    useq = E16.unit_sequence(cred_u, np.array([base[u].max() for u in units]), units, cs, rng, True)
                    slots += [units[ui] for ui in useq]
            # interleave in group order of the stride sequence (deterministic)
            chosen, batch = set(), []
            for u in slots:
                sc = S[u].mean(0)
                for p in np.argsort(-sc, kind="stable"):
                    if int(p) not in chosen:
                        chosen.add(int(p))
                        batch.append(int(todo[p]))
                        proposer[todo[p]] = u[0]
                        break
            pos = {int(c): jj for jj, c in enumerate(todo)}
            for c in batch:
                pred[:, c] = S[:, pos[c]]
        for c in batch:
            evald[c] = True
            cost += env.cost[c]
        nb += 1
        if m:
            where = {}
            for gi, g in enumerate(G):
                for si, s in enumerate(g):
                    for i in s:
                        where[i] = (gi, si)
            cell_of = {}
            for key, units in cells.items():
                for ui, u in enumerate(units):
                    for i in u:
                        cell_of[i] = (key, ui)
            for c in batch:
                p = proposer[c]
                gp, sp = where[p]
                for i in range(m):
                    gi, si = where[i]
                    if gi == gp and si == sp:
                        if tier[i] == 1 or tier[p] <= tier[i] or i == p or cell_of.get(i) == cell_of.get(p):
                            vis[i, c] = True
                    elif gi == gp:
                        # nesting: the head publishes down; a child reports to the head's leader
                        if sp == 0 or (si == 0 and tier[i] == 1):
                            vis[i, c] = True
                    elif share == "published":
                        vis[i, c] = True
            q = np.zeros(m)
            for i in range(m):
                E = np.flatnonzero(vis[i] & evald & ~np.isnan(pred[i]))
                if len(E) >= 3:
                    q[i] = E14.ktau(pred[i, E], -env.truth[E]) * len(E) / (len(E) + 8)
            ema = (1 - th["ema"]) * ema + th["ema"] * q
            # tiers inside every swarm (one leader, two seconds), with incumbency margin
            new = np.full(m, 3)
            for g in G:
                for s in g:
                    ix = np.array(s)
                    key = ema[ix] + th["margin"] * (3 - tier[ix])
                    order = ix[np.argsort(-key, kind="stable")]
                    new[order[:1]] = 1
                    new[order[1:3]] = 2
            tier = new
            # restructuring
            changed = []
            if morph and nb % max(1, int(round(th["period"]))) == 0 and len(todo) > k:
                if DEBUG:
                    print(nb, round(cost / env.total, 3), [[members[i] for i in flat(g)] for g in G], [round(record(flat(g)), 2) for g in G])
                    print(np.round([[E14.ktau(S[flat(a)].mean(0)[cols], S[flat(b)].mean(0)[cols]) for b in G] for a in G], 2))
                def agree(I, J):
                    return E14.ktau(S[list(I)].mean(0)[cols], S[list(J)].mean(0)[cols])
                if do_split:
                    NG = []
                    for g in G:
                        head, kids = g[0], g[1:]
                        out_groups = []
                        newsw = []
                        for si, s in enumerate(g):
                            if len(s) < 2:
                                newsw.append(s)
                                continue
                            pos_rec = (ema[s] > 0).any()
                            comps = components(s, lambda a_, b_: (E14.ktau(S[a_, cols], S[b_, cols]) >= th["split"])
                                               and not (pos_rec and (ema[a_] < 0 or ema[b_] < 0)))
                            if len(comps) == 1:
                                newsw.append(s)
                                continue
                            comps.sort(key=lambda cc: -ema[cc].max())
                            newsw.append(comps[0])
                            changed.append(("split", [members[i] for i in s]))
                            for cc in comps[1:]:
                                if nest_ok and (agree(cc, comps[0] if si == 0 else head) >= th["nest"]
                                                or record(cc) < 0):
                                    newsw.append(cc)
                                else:
                                    out_groups.append([cc])
                        # detach children that no longer agree with the head
                        hd, rest = newsw[0], []
                        for s in newsw[1:]:
                            if agree(s, hd) < th["split"] and (record(s) >= 0 or not nest_ok):
                                out_groups.append([s])
                                changed.append(("detach", [members[i] for i in s]))
                            else:
                                rest.append(s)
                        NG.append([hd] + rest)
                        NG += out_groups
                    G = NG
                if nest_ok:
                    for g in G:
                        if len(g) > 1:
                            qs = [record(s) for s in g]
                            b = int(np.argmax(qs))
                            if b != 0 and qs[b] > qs[0] + th["delta"]:
                                g[0], g[b] = g[b], g[0]
                                changed.append(("promote", [members[i] for i in g[0]]))
                if do_join and len(G) > 1:
                    # greedy over disjoint pairs of top-level groups, highest agreement first
                    pairs = sorted(((agree(flat(G[a_]), flat(G[b_])), a_, b_)
                                    for a_, b_ in itertools.combinations(range(len(G)), 2)), reverse=True)
                    used, merged_all = set(), []
                    for t, a_, b_ in pairs:
                        if t < th["join"]:
                            break
                        if a_ in used or b_ in used:
                            continue
                        qa, qb = record(flat(G[a_])), record(flat(G[b_]))
                        hi, lo = (a_, b_) if qa >= qb else (b_, a_)
                        if max(qa, qb) < 0:
                            continue
                        if len(G[a_]) == 1 and len(G[b_]) == 1 and min(qa, qb) >= 0 and abs(qa - qb) <= th["delta"]:
                            merged = [G[hi][0] + G[lo][0]]
                            changed.append(("fuse", [members[i] for i in merged[0]]))
                        elif nest_ok:
                            merged = G[hi] + G[lo]
                            changed.append(("nest", [members[i] for i in flat(merged)]))
                        else:
                            continue
                        used |= {a_, b_}
                        merged_all.append(merged)
                    if merged_all:
                        G = [g for gi, g in enumerate(G) if gi not in used] + merged_all
                if do_join and nest_ok and len(G) > 1:
                    # adopt: a top-level group whose record is negative is placed under the group
                    # with the best record (its leader then sees the group's results and the group
                    # sees the head's), provided that record exceeds delta
                    qg = [record(flat(g)) for g in G]
                    b = int(np.argmax(qg))
                    if qg[b] > th["delta"]:
                        low = [gi for gi in range(len(G)) if gi != b and qg[gi] < 0]
                        if low:
                            G[b] = G[b] + [s for gi in low for s in G[gi]]
                            changed.append(("adopt", [members[i] for gi in low for i in flat(G[gi])]))
                            G = [g for gi, g in enumerate(G) if gi not in low]
            if log:
                events.append({"cost": float(cost), "n_groups": len(G), "n_swarms": sum(len(g) for g in G),
                               "n_nested": sum(len(g) - 1 for g in G),
                               "largest": max(len(s) for g in G for s in g),
                               "structure": [[sorted(members[i] for i in s) for s in g] for g in G],
                               "changes": changed})
        rec = len(env.top & set(np.flatnonzero(evald).tolist())) / C.TOPN
        curve.append({"n": int(evald.sum()), "cost": cost, "recall": rec})
        if max_frac is not None and cost >= max_frac * env.total:
            break
    out = {"curve": curve}
    if log:
        out["events"] = events
    return out


def seeds_for(receiver, n, tag="exp17"):
    return [E14.crc(f"{tag}|{receiver}|{s}") for s in range(n)]


def early_value(env, start, mode, seeds, theta=None, share="isolated", outer="record"):
    return np.array([C.summarise(run_morph(env, start, mode, outer, share, s, theta=theta, max_frac=0.3)["curve"],
                                 env.total)["early_recall_area"] for s in seeds])


# ------------------------------------------------------------------ level structure value

def level_value(v, players, levels):
    """Winter (1989) level structure value.

    v: dict frozenset(players) -> array (per seed); levels: list of partitions of `players`, finest
    first (each a list of lists); an ordering is admissible when every block of every level is
    contiguous. With levels=[] this is the Shapley value; with one level, the Owen value."""
    block = []
    for P in levels:
        lab = {}
        for bi, B in enumerate(P):
            for p in B:
                lab[p] = bi
        block.append(lab)

    def ok(perm):
        for lab in block:
            seen, last = set(), None
            for p in perm:
                b = lab[p]
                if b != last:
                    if b in seen:
                        return False
                    seen.add(b)
                    last = b
        return True
    phi = {p: 0.0 for p in players}
    cnt = 0
    for perm in itertools.permutations(players):
        if not ok(perm):
            continue
        cnt += 1
        Sx = frozenset()
        for p in perm:
            T = Sx | {p}
            phi[p] = phi[p] + (v[T] - v[Sx])
            Sx = T
    return {p: phi[p] / cnt for p in players}


def structure_levels(structure):
    """[[swarm, ...] group, ...] of body names -> levels (swarms, groups), finest first."""
    swarms = [list(s) for g in structure for s in g]
    groups = [[a for s in g for a in s] for g in structure]
    return [swarms, groups]


# ------------------------------------------------------------------ jobs

def job_team(args):
    receiver, start, mode, share, nseeds, theta, label = args
    env = E14.Env(receiver)
    grid = np.linspace(0, 1, 101)
    ea, c8, curves, ng, nsw, nn, lg = [], [], [], [], [], [], []
    ops = {k_: 0.0 for k_ in ("fuse", "nest", "adopt", "promote", "split", "detach")}
    ops_early = dict(ops)
    for s in seeds_for(receiver, nseeds):
        r = run_morph(env, STARTS[start], mode, "record", share, s, theta=theta, log=True)
        sm = C.summarise(r["curve"], env.total)
        ea.append(sm["early_recall_area"])
        c8.append(sm["cost_frac_to_8of10"])
        cx = np.array([0.0] + [p["cost"] / env.total for p in r["curve"]])
        cy = np.array([0.0] + [p["recall"] for p in r["curve"]])
        ix = np.searchsorted(cx, grid, side="right") - 1
        curves.append(cy[ix])
        ev = r["events"]
        for e in ev:
            for op, _ in e["changes"]:
                ops[op] += 1.0 / nseeds
                if e["cost"] <= 0.25 * env.total:
                    ops_early[op] += 1.0 / nseeds
        ex = np.array([0.0] + [e["cost"] / env.total for e in ev])
        jx = np.clip(np.searchsorted(ex, grid, side="right") - 1, 0, len(ev))
        first = {"n_groups": len(STARTS[start]), "n_swarms": len(STARTS[start]), "n_nested": 0,
                 "largest": max(len(s) for s in STARTS[start])}
        for key, store in (("n_groups", ng), ("n_swarms", nsw), ("n_nested", nn), ("largest", lg)):
            arr = np.array([first[key]] + [e[key] for e in ev], float)
            store.append(arr[jx])
    out = {"early_recall_area": ea, "cost_frac_to_8of10": c8, "grid": grid.tolist(),
           "operations_per_campaign": ops, "operations_early_window": ops_early}
    for key, arr in (("recall", curves), ("n_groups", ng), ("n_swarms", nsw), ("n_nested", nn), ("largest", lg)):
        g = np.array(arr)
        out[key] = {"mean": g.mean(0).tolist(), "p05": np.percentile(g, 5, 0).tolist(),
                    "p50": np.percentile(g, 50, 0).tolist(), "p95": np.percentile(g, 95, 0).tolist()}
    return receiver, start, mode, share, label, out


def learn_theta(receiver="qe_pbe", starts=tuple(STARTS), pop=16, iters=6, nseeds=12,
                rng_seed=17):
    env = E14.Env(receiver)
    keys = list(MORPH_BOUNDS)
    lo = np.array([MORPH_BOUNDS[k][0] for k in keys])
    hi = np.array([MORPH_BOUNDS[k][1] for k in keys])
    mu = np.array([MORPH_DEFAULT[k] for k in keys])
    sd = (hi - lo) / 4
    rng = np.random.default_rng(rng_seed)
    seeds = seeds_for(receiver, nseeds, tag="exp17train")

    def score(x):
        th = dict(zip(keys, x.tolist()))
        return float(np.mean([early_value(env, STARTS[s], "full", seeds, th).mean() for s in starts]))
    best = (score(mu), mu.copy())
    hist = [{"iter": 0, "best": best[0]}]
    for it in range(iters):
        X = np.clip(mu + sd * rng.standard_normal((pop, len(keys))), lo, hi)
        X[0] = best[1]
        f = np.array([score(x) for x in X])
        el = X[np.argsort(-f)[:max(2, pop // 4)]]
        mu, sd = el.mean(0), np.maximum(el.std(0), 0.02 * (hi - lo))
        if f.max() > best[0]:
            best = (float(f.max()), X[int(np.argmax(f))].copy())
        hist.append({"iter": it + 1, "best": best[0], "mean": float(f.mean())})
        print("learn", it, round(best[0], 4), flush=True)
    return {"theta": dict(zip(keys, [float(x) for x in best[1]])), "train_value": best[0], "history": hist,
            "default": MORPH_DEFAULT, "train_receiver": receiver, "train_starts": list(starts)}


def job_game(args):
    receiver, start, mode, nseeds, theta, label = args
    env = E14.Env(receiver)
    seeds = seeds_for(receiver, nseeds, tag="exp17game")
    sw = STARTS[start]
    bodies = [a for s in sw for a in s]
    v = {}
    for r in range(len(bodies) + 1):
        for Sx in itertools.combinations(bodies, r):
            Ss = set(Sx)
            v[frozenset(Sx)] = early_value(env, [[a for a in s if a in Ss] for s in sw], mode, seeds, theta)
    sh = level_value(v, bodies, [])
    start_lv = level_value(v, bodies, structure_levels([[list(s)] for s in sw])) if len(sw) > 1 else sh
    # structure trajectory of the full team, per seed; compute-weighted level value in the early window
    cache = {}
    tv = {a: np.zeros(len(seeds)) for a in bodies}
    occupancy = {}
    for j, s in enumerate(seeds):
        r = run_morph(env, sw, mode, "record", "isolated", s, theta=theta, max_frac=0.3, log=True)
        prev = 0.0
        stru = [[list(x)] for x in sw]
        wts = {}
        lim = 0.25 * env.total
        for e in r["events"]:
            c0, c1 = prev, min(e["cost"], lim)
            if c1 > c0:
                key = json.dumps(sorted(sorted(map(sorted, g)) for g in stru))
                wts[key] = wts.get(key, 0.0) + (c1 - c0)
            prev = e["cost"]
            stru = e["structure"]
            if prev >= lim:
                break
        tot = sum(wts.values())
        for key, w in wts.items():
            occupancy[key] = occupancy.get(key, 0.0) + w / tot / len(seeds)
            if key not in cache:
                st = json.loads(key)
                cache[key] = level_value({kx: vv for kx, vv in v.items()}, bodies, structure_levels(st))
            for a in bodies:
                tv[a][j] += (w / tot) * cache[key][a][j]
    d = {a: tv[a] - sh[a] for a in bodies}
    top = sorted(occupancy.items(), key=lambda kv: -kv[1])[:8]
    return (receiver, start, mode, label, {
        "bodies": bodies,
        "shapley": {a: float(np.mean(sh[a])) for a in bodies},
        "start_owen": {a: float(np.mean(start_lv[a])) for a in bodies},
        "time_level_value": {a: float(np.mean(tv[a])) for a in bodies},
        "tlv_minus_shapley": {a: float(np.mean(d[a])) for a in bodies},
        "tlv_minus_shapley_p05": {a: float(np.percentile(d[a], 5)) for a in bodies},
        "tlv_minus_shapley_p95": {a: float(np.percentile(d[a], 95)) for a in bodies},
        "v_all": float(np.mean(v[frozenset(bodies)])), "v_empty": float(np.mean(v[frozenset()])),
        "efficiency_gap": float(np.max(np.abs(sum(tv[a] for a in bodies) - (v[frozenset(bodies)] - v[frozenset()])))),
        "structures": [{"structure": json.loads(kx), "share": float(w)} for kx, w in top]})


# ------------------------------------------------------------------ self-test

def selftest():
    env = E14.Env("qe_pbe")
    ok = []
    # 1. a fixed single swarm reproduces experiment 14 (emergent) exactly, whatever the share mode
    for share in ("isolated", "published"):
        ok.append(run_morph(env, [A], "fixed", "record", share, 11)["curve"] == E14.run(env, A, "emergent", 11)["curve"])
    # 2. every mode evaluates the whole pool once and keeps all seven bodies; fixed never changes;
    #    merge_only never increases the number of swarms; split_only never decreases it
    for mode in MODES:
        for st in ("split_1x7", "split_2_2_3"):
            r = run_morph(env, STARTS[st], mode, "record", "isolated", 5, log=True)
            c = r["curve"]
            ok.append(c[-1]["n"] == env.n and abs(c[-1]["cost"] - env.total) < 1e-6 * env.total)
            sizes = [sum(len(s) for g in e["structure"] for s in g) for e in r["events"]]
            ok.append(all(x == 7 for x in sizes))
            if mode == "fixed":
                ok.append(all(e["n_swarms"] == len(STARTS[st]) for e in r["events"]))
            if mode == "merge_only":
                ns = [e["n_swarms"] for e in r["events"]]
                ok.append(all(b <= a for a, b in zip(ns, ns[1:])))
            if mode == "split_only":
                ng = [e["n_swarms"] for e in r["events"]]
                ok.append(all(b >= a for a, b in zip(ng, ng[1:])))
    # 3. determinism
    ok.append(run_morph(env, STARTS["split_4_3"], "full", "record", "isolated", 3)["curve"]
              == run_morph(env, STARTS["split_4_3"], "full", "record", "isolated", 3)["curve"])
    # 4. level structure value: Shapley without levels, Owen with one level, efficiency, nesting
    pl = ["a", "b", "c", "d", "e"]
    rng = np.random.default_rng(0)
    vv = {frozenset(Sx): (0.0 if not Sx else float(rng.random() + len(Sx) ** 1.5))
          for r in range(6) for Sx in itertools.combinations(pl, r)}
    sh = E16.shapley(vv, pl)
    lv0 = level_value(vv, pl, [])
    ok.append(all(abs(lv0[p] - sh[p]) < 1e-12 for p in pl))
    U = [["a", "b"], ["c", "d", "e"]]
    ow = E16.owen(vv, U)
    lv1 = level_value(vv, pl, [U])
    ok.append(all(abs(lv1[p] - ow[p]) < 1e-12 for p in pl))
    lv2 = level_value(vv, pl, [[["a"], ["b"], ["c", "d"], ["e"]], U])
    ok.append(abs(sum(lv2.values()) - vv[frozenset(pl)]) < 1e-12)
    # nested level value: the top-level union shares equal the Shapley value of the quotient game
    vq = {frozenset(T): vv[frozenset(x for j in T for x in U[j])] for r in range(3) for T in itertools.combinations(range(2), r)}
    shq = E16.shapley(vq, [0, 1])
    ok.append(abs(lv2["a"] + lv2["b"] - shq[0]) < 1e-12)
    print("selftest", sum(ok), "/", len(ok), ok)
    return all(ok)


# ------------------------------------------------------------------ report

def write_report(team, learned, games):
    L = ["# Experiment 17: morphing swarms (merge, nest, split during the campaign)", "",
         "Value = early-window recall area of the ten most stable compounds; mean [5th, 95th percentile of the",
         "matched-seed mean by bootstrap]. Share mode isolated unless stated. Number of swarms at 25 % of the compute.", ""]
    if learned:
        L += ["Learned thresholds: " + ", ".join(f"{k} {v:.3f}" for k, v in learned["theta"].items()),
              f"(defaults {MORPH_DEFAULT}; training value {learned['train_value']:.3f})", ""]
    for r in RECEIVERS:
        if r not in team:
            continue
        L += [f"## Receiver {r}", "", "| start | mode | value | swarms at 25% | groups at 25% | nested at 25% |",
              "|---|---|---|---|---|---|"]
        for key in sorted(team[r]):
            e = team[r][key]
            x = np.array(e["early_recall_area"])
            bs = np.random.default_rng(0).choice(x, (2000, len(x))).mean(1)
            i25 = 25
            L.append(f"| {key.split('|')[0]} | {'|'.join(key.split('|')[1:])} | {x.mean():.3f} "
                     f"[{np.percentile(bs, 5):.3f}, {np.percentile(bs, 95):.3f}] | "
                     f"{e['n_swarms']['mean'][i25]:.2f} | {e['n_groups']['mean'][i25]:.2f} | {e['n_nested']['mean'][i25]:.2f} |")
        L.append("")
    L += ["## Credit with a changing structure", ""]
    for key, g in games.items():
        L += [f"### {key}", f"v(all) {g['v_all']:.3f}, v(empty) {g['v_empty']:.3f}, efficiency gap {g['efficiency_gap']:.1e}",
              "| body | Shapley | Owen (start structure) | time-averaged level value | difference to Shapley [5, 95] |",
              "|---|---|---|---|---|"]
        for a in g["bodies"]:
            L.append(f"| {a} | {g['shapley'][a]:+.3f} | {g['start_owen'][a]:+.3f} | {g['time_level_value'][a]:+.3f} | "
                     f"{g['tlv_minus_shapley'][a]:+.3f} [{g['tlv_minus_shapley_p05'][a]:+.3f}, {g['tlv_minus_shapley_p95'][a]:+.3f}] |")
        L.append("")
        L.append("Most occupied structures (share of early-window compute):")
        for s in g["structures"]:
            L.append(f"- {s['share']:.2f}: " + " || ".join(" > ".join("+".join(sw) for sw in grp) for grp in s["structure"]))
        L.append("")
    (OUT / "morphing_swarms.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--seeds", type=int, default=100)
    ap.add_argument("--game-seeds", type=int, default=40)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--stage", default="team", choices=["team", "learn", "learned_team", "games", "report"])
    args = ap.parse_args()
    if args.selftest:
        raise SystemExit(0 if selftest() else 1)
    OUT.mkdir(parents=True, exist_ok=True)
    tfile, lfile, gfile = OUT / "team_values.json", OUT / "learned_theta.json", OUT / "games.json"
    team = json.loads(tfile.read_text(encoding="utf-8")) if tfile.exists() else {}
    learned = json.loads(lfile.read_text(encoding="utf-8")) if lfile.exists() else None
    games = json.loads(gfile.read_text(encoding="utf-8")) if gfile.exists() else {}
    t0 = time.time()
    if args.stage in ("team", "learned_team"):
        if args.stage == "team":
            jobs = [(r, st, mode, "isolated", args.seeds, None, "default") for r in RECEIVERS for st in STARTS
                    for mode in MODES if not (st == "one_7" and mode in ("merge_only", "no_nest"))]
            jobs += [(r, st, mode, "published", args.seeds, None, "default") for r in RECEIVERS
                     for st in ("split_1x7", "split_4_3") for mode in ("fixed", "full")]
        else:
            jobs = [(r, st, "full", "isolated", args.seeds, learned["theta"], "learned") for r in RECEIVERS for st in STARTS]
        with Pool(args.workers) as pool:
            for r, st, mode, share, label, res in pool.imap_unordered(job_team, jobs):
                tag = mode if label == "default" else "full_learned"
                team.setdefault(r, {})[f"{st}|{tag}|{share}"] = res
                print(r, st, tag, share, round(float(np.mean(res["early_recall_area"])), 4),
                      round(res["n_swarms"]["mean"][25], 2), round(time.time() - t0), "s", flush=True)
                tfile.write_text(json.dumps(team), encoding="utf-8")
    if args.stage == "learn":
        learned = learn_theta()
        lfile.write_text(json.dumps(learned, indent=1), encoding="utf-8")
    if args.stage == "games":
        jobs = []
        for r in GAME_RECEIVERS:
            for st in ("split_1x7", "split_2_2_3", "split_4_3"):
                jobs.append((r, st, "merge_only", args.game_seeds, None, "default"))
                if learned:
                    jobs.append((r, st, "full", args.game_seeds, learned["theta"], "learned"))
            jobs.append((r, "split_2_2_3", "fixed", args.game_seeds, None, "default"))
        with Pool(args.workers) as pool:
            for r, st, mode, label, res in pool.imap_unordered(job_game, jobs):
                games[f"{r}|{st}|{mode}|{label}"] = res
                gfile.write_text(json.dumps(games, indent=1), encoding="utf-8")
                print("game", r, st, mode, label, round(time.time() - t0), "s", flush=True)
    write_report(team, learned, games)


if __name__ == "__main__":
    main()
