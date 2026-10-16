"""Experiment 18: members that move between swarms, and members that sit in two swarms.

Question (ATEKi): in experiments 16 and 17 every decision body belongs to exactly one swarm, and a body
changes swarm only when its whole swarm fuses, nests or splits. In a consortium a single member often
changes group on its own (a postdoc whose calculations agree with another laboratory's moves there),
and some members sit in two groups at once (a shared student, a liaison who attends both groups'
meetings). Does letting one member at a time move, or letting a member belong to a second swarm,
raise the outcome of the computed Al-Mg-Si campaign, which members move or bridge, and how is credit
divided when membership changes or overlaps?

Setting: the campaign of experiments 14 to 17 (receivers QE PBE, QE HSE06, GPAW r2SCAN; batches of
k = 4 candidates at the measured receiver cost; value = early-window recall area of the ten most
stable compounds). Swarm-level operations are those of experiment 17 (mode fixed, merge_only, full).

Member rules (applied every `period` batches, after the swarm-level operations, by the coordinator
that sees every result; agreement = Kendall tau between a body's scores on the open pool and the mean
scores of a swarm):
  move    a body leaves its swarm for the other swarm it agrees with most, when that agreement exceeds
          its agreement with the rest of its own swarm by at least `move`; the receiving swarm accepts
          it when the swarm record is non-negative and the body's own record is not negative against a
          positive swarm record; a body that moved waits `cool` restructuring steps before moving again.
          Swarm slots, cells and tiers follow the new membership (the mover enters at the lowest tier).
  share   a body keeps its own swarm and also sits in the one other swarm it agrees with most, when that
          agreement is at least `bridge`, on the same acceptance rule; it sees that swarm's results and
          that swarm sees its proposals. Its batch slots still come from its own swarm. The second
          membership is reassessed at every restructuring step.
  Thresholds (move 0.2, bridge 0.6, cool 2) are cold-start defaults; a learned set is fitted with the
  cross-entropy method on training seeds disjoint from the evaluation seeds.

Credit: with moving members the structure in force is a partition at every step, so the credit is the
level structure value of Winter (1989) averaged over the structures in force, weighted by the compute
spent under each in the early window (as in experiment 17). With shared members the structure is a
cover, not a partition; the credit averages the level structure value over the partitions obtained by
assigning each shared member to one of its two swarms (equal weights), so each member's credit is split
between its groupings and efficiency holds.

Outputs: results/mobile_members/{team_values.json, learned_theta.json, games.json, mobile_members.md}
Usage (from ateki/, environment with numpy, scipy, ase):
    python experiments/18_mobile_members.py --selftest
    python experiments/18_mobile_members.py --stage team --seeds 100 --workers 8
    python experiments/18_mobile_members.py --stage learn
    python experiments/18_mobile_members.py --stage learned_team
    python experiments/18_mobile_members.py --stage games --game-seeds 40
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


E17 = _load("e17", "17_morphing_swarms.py")
E14, E16 = E17.E14, E17.E16
C = E14.C
A = E14.AGENTS
OUT = HERE.parent / "results" / "mobile_members"
RECEIVERS = E17.RECEIVERS
GAME_RECEIVERS = E17.GAME_RECEIVERS
STARTS = E17.STARTS
SWARM_MODES = ["fixed", "merge_only", "full"]
RULES = ["none", "move", "share", "move+share"]
DEBUG = False
MOBILE_DEFAULT = {"move": 0.2, "bridge": 0.6, "cool": 2.0}
MOBILE_BOUNDS = {"move": (0.0, 1.0), "bridge": (0.0, 1.01), "cool": (0.0, 6.0)}


def run_mobile(env, start, mode="full", rule="none", outer="record", share="isolated", seed=0, k=4,
               theta=None, max_frac=None, log=False):
    """Experiment-17 campaign plus member moves (rule contains "move") and shared members ("share")."""
    th = {**E14.DEFAULT_THETA, **E17.MORPH_DEFAULT, **MOBILE_DEFAULT, **(theta or {})}
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
    do_move = "move" in rule
    do_share = "share" in rule
    guest = np.full(m, -1)            # anchor body of the second swarm a member also sits in
    last_move = np.full(m, -10 ** 9)
    per = max(1, int(round(th["period"])))

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
                        u = E17.components(s, lambda a_, b_: E14.ktau(S[a_, cols], S[b_, cols]) >= th["merge"])
                    else:
                        u = [[i] for i in s]
                    cells[tuple(s)] = u
            kk = min(k, len(todo))
            # slots: groups -> swarms -> cells
            if len(G) == 1:
                gseq = [0] * kk
            else:
                gq = [record(flat(g)) for g in G] if outer == "record" else [0.0] * len(G)
                gw = E17.ladder(gq, th) if outer == "record" else (
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
                    sseq = E16.unit_sequence(cred_s, E17.ladder([record(s) for s in g], th), g, cg, rng, True)
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
            if do_share:
                # a shared member sees the results of its second swarm, and that swarm sees its proposals
                for c in batch:
                    p = proposer[c]
                    for i in range(m):
                        if guest[i] >= 0 and where[int(guest[i])] == where[p]:
                            vis[i, c] = True
                    if guest[p] >= 0:
                        for i in range(m):
                            if where[i] == where[int(guest[p])]:
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
            if (morph or do_move or do_share) and nb % per == 0 and len(todo) > k:
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
                            comps = E17.components(s, lambda a_, b_: (E14.ktau(S[a_, cols], S[b_, cols]) >= th["split"])
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
                if do_move or do_share:
                    G = [g for g in ([s for s in g if len(s)] for g in G) if g]

                    def locate(i):
                        for gi_, g_ in enumerate(G):
                            for si_, s_ in enumerate(g_):
                                if i in s_:
                                    return gi_, si_

                    def best_other(i):
                        gi_, si_ = locate(i)
                        bt, bk = -2.0, None
                        for gj, g_ in enumerate(G):
                            for sj, s_ in enumerate(g_):
                                if (gj, sj) == (gi_, si_):
                                    continue
                                t = E14.ktau(S[i, cols], S[s_].mean(0)[cols])
                                if t > bt:
                                    bt, bk = t, (gj, sj)
                        return (gi_, si_), bk, bt
                if do_move:
                    # a member leaves its swarm for the swarm whose ordering it agrees with more, by at
                    # least `move`; the receiving swarm accepts it when its record is non-negative and
                    # the member's own record is not negative against a positive swarm record
                    for i in np.argsort(-ema, kind="stable"):
                        i = int(i)
                        if nb - last_move[i] < th["cool"] * per:
                            continue
                        (gi, si), bk, bt = best_other(i)
                        if bk is None:
                            continue
                        own = [j for j in G[gi][si] if j != i]
                        a_own = E14.ktau(S[i, cols], S[own].mean(0)[cols]) if own else 0.0
                        rt = record(G[bk[0]][bk[1]])
                        if bt - a_own < th["move"] or rt < 0 or (ema[i] < 0 and rt > 0):
                            continue
                        src = sorted(members[j] for j in G[gi][si])
                        dst = sorted(members[j] for j in G[bk[0]][bk[1]])
                        G[gi][si] = own
                        G[bk[0]][bk[1]] = G[bk[0]][bk[1]] + [i]
                        G = [g for g in ([s for s in g if len(s)] for g in G) if g]
                        tier[i] = 3
                        last_move[i] = nb
                        changed.append(("move", [members[i], src, dst]))
                if do_share:
                    # a member also sits in the one other swarm it agrees with most (>= bridge), on the
                    # same acceptance rule; reassessed at every restructuring step
                    old = guest.copy()
                    guest[:] = -1
                    for i in range(m):
                        _, bk, bt = best_other(i)
                        if bk is None or bt < th["bridge"]:
                            continue
                        sw_ = G[bk[0]][bk[1]]
                        rt = record(sw_)
                        if rt < 0 or (ema[i] < 0 and rt > 0):
                            continue
                        guest[i] = max(sw_, key=lambda j: (ema[j], -j))
                        if old[i] < 0:
                            changed.append(("share", [members[i], sorted(members[j] for j in sw_)]))
            if log:
                gmap = {}
                for gi_, g_ in enumerate(G):
                    for s_ in g_:
                        for j in s_:
                            gmap[j] = s_
                events.append({"cost": float(cost), "n_groups": len(G), "n_swarms": sum(len(g) for g in G),
                               "n_nested": sum(len(g) - 1 for g in G),
                               "largest": max(len(s) for g in G for s in g),
                               "n_shared": int((guest >= 0).sum()),
                               "guests": {members[i]: sorted(members[j] for j in gmap[int(guest[i])])
                                          for i in range(m) if guest[i] >= 0 and int(guest[i]) in gmap},
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
    # matched with experiment 17, so the rule "none" reproduces its campaigns seed for seed
    return [E14.crc(f"{tag}|{receiver}|{s}") for s in range(n)]


def early_value(env, start, mode, rule, seeds, theta=None):
    return np.array([C.summarise(run_mobile(env, start, mode, rule, seed=s, theta=theta, max_frac=0.3)["curve"],
                                 env.total)["early_recall_area"] for s in seeds])


def job_team(args):
    receiver, start, mode, rule, nseeds, theta, label = args
    env = E14.Env(receiver)
    grid = np.linspace(0, 1, 101)
    ea, c8, curves, nsw, nsh = [], [], [], [], []
    ops = {k_: 0.0 for k_ in ("fuse", "nest", "adopt", "promote", "split", "detach", "move", "share")}
    ops_early = dict(ops)
    movers, sharers = {a: 0.0 for a in A}, {a: 0.0 for a in A}
    routes = {}
    for s in seeds_for(receiver, nseeds):
        r = run_mobile(env, STARTS[start], mode, rule, seed=s, theta=theta, log=True)
        sm = C.summarise(r["curve"], env.total)
        ea.append(sm["early_recall_area"])
        c8.append(sm["cost_frac_to_8of10"])
        cx = np.array([0.0] + [p["cost"] / env.total for p in r["curve"]])
        cy = np.array([0.0] + [p["recall"] for p in r["curve"]])
        ix = np.searchsorted(cx, grid, side="right") - 1
        curves.append(cy[ix])
        ev = r["events"]
        for e in ev:
            early = e["cost"] <= 0.25 * env.total
            for op, det in e["changes"]:
                ops[op] += 1.0 / nseeds
                if early:
                    ops_early[op] += 1.0 / nseeds
                    if op == "move":
                        movers[det[0]] += 1.0 / nseeds
                        key = det[0] + " -> " + "+".join(det[2])
                        routes[key] = routes.get(key, 0.0) + 1.0 / nseeds
            if early:
                for a in e["guests"]:
                    sharers[a] += 1.0 / nseeds / max(1, sum(1 for x in ev if x["cost"] <= 0.25 * env.total))
        ex = np.array([0.0] + [e["cost"] / env.total for e in ev])
        jx = np.clip(np.searchsorted(ex, grid, side="right") - 1, 0, len(ev))
        nsw.append(np.array([len(STARTS[start])] + [e["n_swarms"] for e in ev], float)[jx])
        nsh.append(np.array([0] + [e["n_shared"] for e in ev], float)[jx])
    out = {"early_recall_area": ea, "cost_frac_to_8of10": c8, "grid": grid.tolist(),
           "operations_per_campaign": ops, "operations_early_window": ops_early,
           "moves_per_body_early": movers, "share_fraction_per_body_early": sharers,
           "top_routes_early": dict(sorted(routes.items(), key=lambda kv: -kv[1])[:8])}
    for key, arr in (("recall", curves), ("n_swarms", nsw), ("n_shared", nsh)):
        g = np.array(arr)
        out[key] = {"mean": g.mean(0).tolist(), "p05": np.percentile(g, 5, 0).tolist(),
                    "p95": np.percentile(g, 95, 0).tolist()}
    return receiver, start, mode, rule, label, out


def learn_theta(receiver="qe_pbe", starts=tuple(STARTS), pop=16, iters=6, nseeds=12, rng_seed=18,
                mode="fixed", rule="move+share"):
    env = E14.Env(receiver)
    keys = list(MOBILE_BOUNDS)
    lo = np.array([MOBILE_BOUNDS[k][0] for k in keys])
    hi = np.array([MOBILE_BOUNDS[k][1] for k in keys])
    mu = np.array([MOBILE_DEFAULT[k] for k in keys])
    sd = (hi - lo) / 4
    rng = np.random.default_rng(rng_seed)
    seeds = seeds_for(receiver, nseeds, tag="exp18train")

    def score(x):
        th = dict(zip(keys, x.tolist()))
        return float(np.mean([early_value(env, STARTS[s], mode, rule, seeds, th).mean() for s in starts]))
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
            "default": MOBILE_DEFAULT, "train_receiver": receiver, "train_mode": mode, "train_rule": rule,
            "train_starts": list(starts)}


# ------------------------------------------------------------------ credit over covers

def cover_partitions(structure, guests):
    """Partitions obtained by assigning each shared member to its own swarm or to its second swarm.

    structure: [[swarm, ...] group, ...] of body names (a partition); guests: body -> sorted members of
    the second swarm. Returns a list of structures, one per assignment (equal weights)."""
    loc = {tuple(sorted(sw_)): (gi, si) for gi, g in enumerate(structure) for si, sw_ in enumerate(g)}
    shared = [a for a, sw in guests.items() if a not in sw and tuple(sw) in loc]
    out = []
    for pick in itertools.product((0, 1), repeat=len(shared)):
        st = [[list(s) for s in g] for g in structure]
        movers = [(a, loc[tuple(guests[a])]) for a, p in zip(shared, pick) if p]
        for a, _ in movers:
            for g in st:
                for s in g:
                    if a in s:
                        s.remove(a)
        for a, (gi, si) in movers:
            st[gi][si].append(a)
        st = [g for g in ([s for s in g if s] for g in st) if g]
        out.append(st)
    return out


def job_game(args):
    receiver, start, mode, rule, nseeds, theta, label = args
    env = E14.Env(receiver)
    seeds = seeds_for(receiver, nseeds, tag="exp17game")
    sw = STARTS[start]
    bodies = [a for s in sw for a in s]
    v = {}
    for r in range(len(bodies) + 1):
        for Sx in itertools.combinations(bodies, r):
            Ss = set(Sx)
            v[frozenset(Sx)] = early_value(env, [[a for a in s if a in Ss] for s in sw], mode, rule, seeds, theta)
    sh = E17.level_value(v, bodies, [])
    cache = {}
    tv = {a: np.zeros(len(seeds)) for a in bodies}
    occupancy = {}
    lim = 0.25 * env.total
    for j, s in enumerate(seeds):
        r = run_mobile(env, sw, mode, rule, seed=s, theta=theta, max_frac=0.3, log=True)
        prev = 0.0
        state = ([[list(x)] for x in sw], {})
        wts = {}
        for e in r["events"]:
            c0, c1 = prev, min(e["cost"], lim)
            if c1 > c0:
                key = json.dumps([sorted(sorted(map(sorted, g)) for g in state[0]),
                                  {a: g for a, g in sorted(state[1].items())}])
                wts[key] = wts.get(key, 0.0) + (c1 - c0)
            prev = e["cost"]
            state = (e["structure"], e["guests"])
            if prev >= lim:
                break
        tot = sum(wts.values())
        for key, w in wts.items():
            occupancy[key] = occupancy.get(key, 0.0) + w / tot / len(seeds)
            if key not in cache:
                st, gu = json.loads(key)
                parts = cover_partitions(st, gu)
                acc = {a: 0.0 for a in bodies}
                for P in parts:
                    lv = E17.level_value(v, bodies, E17.structure_levels(P))
                    for a in bodies:
                        acc[a] = acc[a] + lv[a] / len(parts)
                cache[key] = acc
            for a in bodies:
                tv[a][j] += (w / tot) * cache[key][a][j]
    d = {a: tv[a] - sh[a] for a in bodies}
    top = sorted(occupancy.items(), key=lambda kv: -kv[1])[:8]
    return (receiver, start, mode, rule, label, {
        "bodies": bodies,
        "shapley": {a: float(np.mean(sh[a])) for a in bodies},
        "time_level_value": {a: float(np.mean(tv[a])) for a in bodies},
        "tlv_minus_shapley": {a: float(np.mean(d[a])) for a in bodies},
        "tlv_minus_shapley_p05": {a: float(np.percentile(d[a], 5)) for a in bodies},
        "tlv_minus_shapley_p95": {a: float(np.percentile(d[a], 95)) for a in bodies},
        "v_all": float(np.mean(v[frozenset(bodies)])), "v_empty": float(np.mean(v[frozenset()])),
        "efficiency_gap": float(np.max(np.abs(sum(tv[a] for a in bodies) - (v[frozenset(bodies)] - v[frozenset()])))),
        "structures": [{"structure": json.loads(kx)[0], "guests": json.loads(kx)[1], "share": float(w)}
                       for kx, w in top]})


# ------------------------------------------------------------------ self-test

def selftest():
    env = E14.Env("qe_pbe")
    ok = []
    # 1. rule "none" reproduces experiment 17 exactly, for every swarm mode and start
    for mode in E17.MODES:
        for st in ("split_1x7", "split_4_3", "split_2_2_3"):
            for s in (3, 7):
                ok.append(run_mobile(env, STARTS[st], mode, "none", seed=s)["curve"]
                          == E17.run_morph(env, STARTS[st], mode, "record", "isolated", s)["curve"])
    # 2. every rule evaluates the whole pool once, keeps a partition of all seven bodies, and a second
    #    membership never points into the member's own swarm; fixed+move never adds swarms
    for mode in SWARM_MODES:
        for rule in RULES[1:]:
            for st in ("split_1x7", "split_4_3", "split_2_2_3"):
                r = run_mobile(env, STARTS[st], mode, rule, seed=5, log=True)
                c = r["curve"]
                ok.append(c[-1]["n"] == env.n and abs(c[-1]["cost"] - env.total) < 1e-6 * env.total)
                ok.append(all(sorted(a for g in e["structure"] for s in g for a in s) == sorted(A) for e in r["events"]))
                ok.append(all(not any(a in s_ and sorted(s_) == sw for g in e["structure"] for s_ in g)
                              for e in r["events"] for a, sw in e["guests"].items()))
                if rule == "move" and mode == "fixed":
                    ns = [e["n_swarms"] for e in r["events"]]
                    ok.append(all(b <= a for a, b in zip(ns, ns[1:])))
                if rule == "share":
                    ok.append(all(not any(op == "move" for op, _ in e["changes"]) for e in r["events"]))
    # 3. members actually move and share in some campaign
    r = run_mobile(env, STARTS["split_4_3"], "fixed", "move+share", seed=1, log=True)
    ok.append(any(op == "move" for e in r["events"] for op, _ in e["changes"]))
    ok.append(any(e["n_shared"] > 0 for e in r["events"]))
    # 4. determinism
    ok.append(run_mobile(env, STARTS["split_4_3"], "full", "move+share", seed=3)["curve"]
              == run_mobile(env, STARTS["split_4_3"], "full", "move+share", seed=3)["curve"])
    # 5. cover averaging: no shared member gives the structure itself; the averaged credit is efficient
    st = [[["a", "b"], ["c"]], [["d", "e"]]]
    ok.append(cover_partitions(st, {}) == [st])
    parts = cover_partitions(st, {"c": ["d", "e"]})
    ok.append(len(parts) == 2 and parts[1] == [[["a", "b"]], [["d", "e", "c"]]])
    pl = ["a", "b", "c", "d", "e"]
    rng = np.random.default_rng(0)
    vv = {frozenset(Sx): (0.0 if not Sx else float(rng.random() + len(Sx) ** 1.5))
          for r_ in range(6) for Sx in itertools.combinations(pl, r_)}
    acc = {p: 0.0 for p in pl}
    for P in parts:
        lv = E17.level_value(vv, pl, E17.structure_levels(P))
        for p in pl:
            acc[p] += lv[p] / len(parts)
    ok.append(abs(sum(acc.values()) - vv[frozenset(pl)]) < 1e-12)
    print("selftest", sum(ok), "/", len(ok), "failed at", [i for i, x in enumerate(ok) if not x])
    return all(ok)


# ------------------------------------------------------------------ report

def write_report(team, learned, games):
    L = ["# Experiment 18: members that move between swarms or sit in two swarms", "",
         "Value = early-window recall area of the ten most stable compounds; mean [5th, 95th percentile of the",
         "matched-seed mean by bootstrap]. Moves and shared members counted in the early window (25 % of compute).", ""]
    if learned:
        L += ["Learned thresholds: " + ", ".join(f"{k} {v:.3f}" for k, v in learned["theta"].items()),
              f"(defaults {MOBILE_DEFAULT}; training value {learned['train_value']:.3f})", ""]
    for r in RECEIVERS:
        if r not in team:
            continue
        L += [f"## Receiver {r}", "", "| start | swarm mode | member rule | value | minus rule none | moves | mean shared members at 25% |",
              "|---|---|---|---|---|---|---|"]
        for key in sorted(team[r]):
            st, mode, rule = key.split("|")
            e = team[r][key]
            x = np.array(e["early_recall_area"])
            base = team[r].get(f"{st}|{mode}|none") if rule != "none" else None
            if rule.endswith("learned"):
                base = team[r].get(f"{st}|{mode}|none")
            bs = np.random.default_rng(0).choice(len(x), (2000, len(x)))
            dtxt = ""
            if base is not None:
                d = x - np.array(base["early_recall_area"])
                db = d[bs].mean(1)
                dtxt = f"{d.mean():+.3f} [{np.percentile(db, 5):+.3f}, {np.percentile(db, 95):+.3f}]"
            xb = x[bs].mean(1)
            L.append(f"| {st} | {mode} | {rule} | {x.mean():.3f} [{np.percentile(xb, 5):.3f}, {np.percentile(xb, 95):.3f}] | "
                     f"{dtxt} | {e['operations_early_window']['move']:.2f} | {e['n_shared']['mean'][25]:.2f} |")
        L.append("")
        for key in sorted(team[r]):
            e = team[r][key]
            if e["top_routes_early"]:
                L.append(f"- {key}: most frequent moves " + "; ".join(f"{k_} {v_:.2f}" for k_, v_ in list(e['top_routes_early'].items())[:4]))
        L.append("")
    L += ["## Credit with moving or shared members", ""]
    for key, g in games.items():
        L += [f"### {key}", f"v(all) {g['v_all']:.3f}, v(empty) {g['v_empty']:.3f}, efficiency gap {g['efficiency_gap']:.1e}",
              "| body | Shapley | averaged level value | difference [5, 95] |", "|---|---|---|---|"]
        for a in g["bodies"]:
            L.append(f"| {a} | {g['shapley'][a]:+.3f} | {g['time_level_value'][a]:+.3f} | "
                     f"{g['tlv_minus_shapley'][a]:+.3f} [{g['tlv_minus_shapley_p05'][a]:+.3f}, {g['tlv_minus_shapley_p95'][a]:+.3f}] |")
        L.append("")
        L.append("Most occupied structures (share of early-window compute; second memberships after //):")
        for s in g["structures"]:
            gtxt = "; ".join(f"{a} also in {'+'.join(sw)}" for a, sw in s["guests"].items())
            L.append(f"- {s['share']:.2f}: " + " || ".join(" > ".join("+".join(x) for x in grp) for grp in s["structure"])
                     + (f" // {gtxt}" if gtxt else ""))
        L.append("")
    (OUT / "mobile_members.md").write_text("\n".join(L) + "\n", encoding="utf-8")


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
            jobs = [(r, st, mode, rule, args.seeds, None, "default") for r in RECEIVERS for st in STARTS
                    for mode in SWARM_MODES for rule in RULES if not (st == "one_7" and mode == "merge_only")]
        else:
            # the learned thresholds with each member rule, to separate moving from sharing
            jobs = [(r, st, learned["train_mode"], rule, args.seeds, learned["theta"], "learned")
                    for r in RECEIVERS for st in STARTS for rule in RULES[1:]]
        with Pool(args.workers) as pool:
            for r, st, mode, rule, label, res in pool.imap_unordered(job_team, jobs):
                tag = rule if label == "default" else rule + " learned"
                team.setdefault(r, {})[f"{st}|{mode}|{tag}"] = res
                print(r, st, mode, tag, round(float(np.mean(res["early_recall_area"])), 4),
                      round(res["operations_early_window"]["move"], 2), round(res["n_shared"]["mean"][25], 2),
                      round(time.time() - t0), "s", flush=True)
                tfile.write_text(json.dumps(team), encoding="utf-8")
    if args.stage == "learn":
        learned = learn_theta()
        lfile.write_text(json.dumps(learned, indent=1), encoding="utf-8")
    if args.stage == "games":
        jobs = []
        for r in GAME_RECEIVERS:
            for st in ("split_2_2_3", "split_4_3"):
                for rule in ("move", "share", "move+share"):
                    jobs.append((r, st, "fixed", rule, args.game_seeds, None, "default"))
                jobs.append((r, st, "merge_only", "move+share", args.game_seeds, None, "default"))
        with Pool(args.workers) as pool:
            for r, st, mode, rule, label, res in pool.imap_unordered(job_game, jobs):
                games[f"{r}|{st}|{mode}|{rule}"] = res
                gfile.write_text(json.dumps(games, indent=1), encoding="utf-8")
                print("game", r, st, mode, rule, round(time.time() - t0), "s", flush=True)
    write_report(team, learned, games)


if __name__ == "__main__":
    main()
