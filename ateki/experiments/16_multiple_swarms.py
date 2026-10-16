"""Experiment 16: several swarms in one campaign, of the same or different sizes.

Question (ATEKi): a discovery campaign is often run by several groups at
once, each organised as its own swarm of decision bodies, sharing one
laboratory or one allocation of compute. How should the same bodies be
grouped into swarms, how should the batch slots be split between swarms of
different sizes, does it help to publish results between swarms, and how is
the credit divided between swarms and between the bodies inside them?

Setting: the computed Al-Mg-Si campaign of experiment 14 (receivers QE PBE,
QE HSE06, GPAW r2SCAN; the team submits batches of k = 4 candidates and
pays their measured receiver cost; value = early-window recall area of the
ten most stable compounds). The seven decision bodies of experiment 14 are
grouped into swarms. Every swarm runs the organisation of experiment 14
inside itself (flat, or the emergent hierarchical swarm with tiers, cells
and the promotion protocol), restricted to its own members. The batch of 4
is shared by all swarms, so every configuration spends the same compute.

Configurations (swarms are listed by their members):
  one_7          the seven bodies as one swarm (reproduces experiment 14)
  split_4_3      {MACE relaxation, NEP89 MD, MEAM MD, scout} + {archive, NEP89 relaxation, active learner}
  split_2_5s     small strong swarm {MACE relaxation, active learner} + the other five
  split_2_5w     small weak swarm {NEP89 MD, scout} + the other five
  split_1_6      {MACE relaxation} alone + the other six
  split_2_2_3    {MACE relaxation, archive} + {NEP89 MD, NEP89 relaxation} + {MEAM MD, active learner, scout}
  split_1x7      seven single-body swarms
  dup_7_7        two copies of the seven-body swarm (14 bodies)
  dup_7_7_7      three copies (21 bodies)
  dup_7_3        the seven-body swarm + a small copy {MACE relaxation, active learner, scout}
A copy of a body in another swarm is named "kind@j". A deterministic rule
copied into another swarm differs from its original only through the
results it can see; a random-scout copy draws its own ordering.

Factors:
  inner   flat | emergent        organisation inside each swarm (experiment 14)
  outer   equal | size | record  split of the batch slots between swarms: equal
                                 share per swarm, share proportional to swarm
                                 size, or by the swarms' running records (the
                                 promotion rule of experiment 14 applied to
                                 swarms: leader swarm weight 4, second 2,
                                 others 1, negative record 0.25)
  share   isolated | published   isolated: a body sees only results of its own
                                 swarm (inside the swarm, by the inner rule);
                                 published: results of other swarms are
                                 visible to every body after each batch

Attribution, with matched campaign seeds (the seed does not depend on the
coalition, as in experiment 15):
  * swarm game: players = swarms, v(T) = campaign run by the swarms in T;
    exact Shapley per campaign;
  * body game: players = the seven bodies, v(S) = campaign run with every
    swarm restricted to its members in S (empty swarms drop out);
    exact Shapley and the Owen value with the swarms as a priori unions
    (Owen 1977): the Owen value first divides v(N) between swarms by their
    Shapley value in the swarm game and then divides each swarm's share
    between its members, so the difference Owen minus Shapley is the credit
    a body gains or loses through the swarm it belongs to.

Outputs: results/multiple_swarms/{team_values.json, games.json, multiple_swarms.md}
Usage (from ateki/, environment with numpy, scipy, ase):
    python experiments/16_multiple_swarms.py --selftest
    python experiments/16_multiple_swarms.py --seeds 100 --game-seeds 100 --workers 8
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
_spec = importlib.util.spec_from_file_location("e14", HERE / "14_emergent_swarm.py")
E14 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(E14)
C = E14.C

OUT = HERE.parent / "results" / "multiple_swarms"
A = E14.AGENTS
RECEIVERS = ["qe_pbe", "qe_hse06", "gpaw_r2scan"]
GAME_RECEIVERS = ["qe_pbe", "qe_hse06"]


def tag(names, j):
    return [x if j == 0 else f"{x}@{j}" for x in names]


SMALL3 = ["mace_relax", "surrogate", "explorer"]
REST5 = ["gpumd_nep89_md", "gpumd_nep89_relax", "lammps_meam_md", "archive_mp", "explorer"]
CONFIGS = {
    "one_7": [A],
    "split_4_3": [["mace_relax", "gpumd_nep89_md", "lammps_meam_md", "explorer"],
                  ["archive_mp", "gpumd_nep89_relax", "surrogate"]],
    "split_2_5s": [["mace_relax", "surrogate"], REST5],
    "split_2_5w": [["gpumd_nep89_md", "explorer"],
                   ["mace_relax", "archive_mp", "gpumd_nep89_relax", "lammps_meam_md", "surrogate"]],
    "split_1_6": [["mace_relax"], [a for a in A if a != "mace_relax"]],
    "split_2_2_3": [["mace_relax", "archive_mp"], ["gpumd_nep89_md", "gpumd_nep89_relax"],
                    ["lammps_meam_md", "surrogate", "explorer"]],
    "split_1x7": [[a] for a in A],
    "dup_7_7": [A, tag(A, 1)],
    "dup_7_7_7": [A, tag(A, 1), tag(A, 2)],
    "dup_7_3": [A, tag(SMALL3, 1)],
}
PARTITIONS = [c for c in CONFIGS if c.startswith("split") and c != "split_1x7"]
INNER = ["flat", "emergent"]
OUTER = ["equal", "size", "record"]
SHARE = ["isolated", "published"]


def kind(name: str) -> str:
    return E14.body_kind(name.split("@")[0])


def unit_sequence(cred, weights, units, kk, rng, draws):
    """Experiment-14 stride allocation of kk slots among units; returns the unit index per slot."""
    if len(units) == 1:
        return [0] * kk
    ucred = np.array([cred[u].sum() for u in units]) + kk * weights / weights.sum()
    for ui, u in enumerate(units):
        cred[u] += (kk * weights[ui] / weights.sum()) / len(u)
    seq = []
    for _ in range(kk):
        ui = int(np.argmax(ucred + rng.random(len(units)) * 1e-9)) if draws else int(np.argmax(ucred))
        seq.append(ui)
        ucred[ui] -= 1.0
        cred[units[ui]] -= 1.0 / len(units[ui])
    return seq


def run_multi(env, swarms, inner="emergent", outer="equal", share="published", seed=0, k=4,
              theta=None, max_frac=None, log=False):
    th = dict(E14.DEFAULT_THETA, **(theta or {}))
    swarms = [list(s) for s in swarms if len(s)]
    ns = len(swarms)
    rng = np.random.default_rng(seed)
    n = env.n
    jitter = rng.random(n) * 1e-9
    members = [a for s in swarms for a in s]
    m = len(members)
    sw = np.array([j for j, s in enumerate(swarms) for _ in s], int)
    idx_of = [np.flatnonzero(sw == j) for j in range(ns)]
    evald = np.zeros(n, bool)
    vis = np.zeros((m, n), bool)
    proposer = np.full(n, -1)
    pred = np.full((m, n), np.nan)
    spred = np.full((ns, n), np.nan)
    scout = rng.random(n)
    own_draw = {a: np.random.default_rng(E14.crc(f"{seed}|{a}")).random(n)
                for a in members if kind(a) == "explorer" and a != "explorer"}
    ema = np.zeros(m)
    tier = np.full(m, 2)
    credit = np.zeros(m)
    sema = np.zeros(ns)
    stier = np.full(ns, 2)
    scred = np.zeros(ns)
    cost = 0.0
    curve, events = [], []
    order_rand = rng.permutation(n)
    emergent = inner == "emergent"
    while not evald.all():
        todo = np.flatnonzero(~evald)
        if m == 0:
            batch = [c for c in order_rand if not evald[c]][:k]
            bunits = []
        else:
            S = np.zeros((m, len(todo)))
            for i, a in enumerate(members):
                kd = kind(a)
                if kd == "explorer":
                    S[i] = E14.rank01((scout if a == "explorer" else own_draw[a])[todo])
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
            # units inside each swarm (experiment 14 rules, restricted to the swarm)
            cols = None
            if emergent and th["merge"] <= 1.0 and m > 1:
                cols = np.arange(len(todo)) if len(todo) <= 60 else rng.choice(len(todo), 60, replace=False)
            sunits, sweights = [], []
            base = np.where(tier == 1, th["ratio"] ** 2, np.where(tier == 2, th["ratio"], 1.0))
            base = np.where(ema < 0, th["floor"], base)
            for j in range(ns):
                ix = idx_of[j]
                if emergent:
                    parent = {int(i): int(i) for i in ix}

                    def find(x):
                        while parent[x] != x:
                            parent[x] = parent[parent[x]]
                            x = parent[x]
                        return x
                    if cols is not None:
                        for a_, b_ in itertools.combinations(ix.tolist(), 2):
                            if E14.ktau(S[a_, cols], S[b_, cols]) >= th["merge"]:
                                parent[find(a_)] = find(b_)
                    groups = {}
                    for i in ix.tolist():
                        groups.setdefault(find(i), []).append(i)
                    units = list(groups.values())
                    weights = np.array([base[u].max() for u in units])
                else:
                    units = [[int(i)] for i in ix]
                    weights = np.ones(len(units))
                sunits.append(units)
                sweights.append(weights)
            kk = min(k, len(todo))
            # outer split of the slots between swarms
            if ns == 1:
                sseq = [0] * kk
            else:
                if outer == "equal":
                    W = np.ones(ns)
                elif outer == "size":
                    W = np.array([len(s) for s in swarms], float)
                else:
                    W = np.where(stier == 1, th["ratio"] ** 2, np.where(stier == 2, th["ratio"], 1.0))
                    W = np.where(sema < 0, th["floor"], W)
                oc = scred + kk * W / W.sum()
                scred += kk * W / W.sum()
                sseq = []
                for _ in range(kk):
                    j = int(np.argmax(oc + rng.random(ns) * 1e-9))
                    sseq.append(j)
                    oc[j] -= 1.0
                    scred[j] -= 1.0
            counts = [sseq.count(j) for j in range(ns)]
            useq = {j: unit_sequence(credit, sweights[j], sunits[j], counts[j], rng, True)
                    for j in range(ns) if counts[j] > 0}
            ptr = {j: 0 for j in useq}
            chosen = set()
            batch = []
            for j in sseq:
                u = sunits[j][useq[j][ptr[j]]]
                ptr[j] += 1
                sc = S[u].mean(0)
                for p in np.argsort(-sc, kind="stable"):
                    if int(p) not in chosen:
                        chosen.add(int(p))
                        batch.append(int(todo[p]))
                        proposer[todo[p]] = u[0]
                        break
            bunits = sunits
            pos = {int(c): jj for jj, c in enumerate(todo)}
            for c in batch:
                pred[:, c] = S[:, pos[c]]
                for j in range(ns):
                    spred[j, c] = S[idx_of[j], pos[c]].mean()
        for c in batch:
            evald[c] = True
            cost += env.cost[c]
        if m:
            cell_of = {}
            for j, units in enumerate(bunits):
                for ui, u in enumerate(units):
                    for i in u:
                        cell_of[i] = (j, ui)
            for c in batch:
                p = proposer[c]
                for i in range(m):
                    if sw[i] != sw[p]:
                        if share == "published":
                            vis[i, c] = True
                    elif not emergent:
                        vis[i, c] = True
                    elif tier[i] == 1 or tier[p] <= tier[i] or i == p or cell_of.get(i) == cell_of.get(p):
                        vis[i, c] = True
            if emergent:
                q = np.zeros(m)
                for i in range(m):
                    E = np.flatnonzero(vis[i] & evald & ~np.isnan(pred[i]))
                    if len(E) >= 3:
                        q[i] = E14.ktau(pred[i, E], -env.truth[E]) * len(E) / (len(E) + 8)
                ema = (1 - th["ema"]) * ema + th["ema"] * q
                new = np.full(m, 3)
                nl = int(round(th["n_lead"]))
                for j in range(ns):
                    ix = idx_of[j]
                    key = ema[ix] + th["margin"] * (3 - tier[ix])
                    order = ix[np.argsort(-key, kind="stable")]
                    new[order[:nl]] = 1
                    new[order[nl:nl + 2]] = 2
                tier = new
            if ns > 1 and outer == "record":
                qs = np.zeros(ns)
                for j in range(ns):
                    seen = vis[idx_of[j]].any(0)
                    E = np.flatnonzero(seen & evald & ~np.isnan(spred[j]))
                    if len(E) >= 3:
                        qs[j] = E14.ktau(spred[j, E], -env.truth[E]) * len(E) / (len(E) + 8)
                sema = (1 - th["ema"]) * sema + th["ema"] * qs
                key = sema + th["margin"] * (3 - stier)
                order = np.argsort(-key, kind="stable")
                ns_ = np.full(ns, 3)
                ns_[order[:1]] = 1
                ns_[order[1:3]] = 2
                stier = ns_
            if log:
                events.append({"cost": float(cost), "swarm_slots": counts if m else [],
                               "swarm_tier": stier.tolist()})
        rec = len(env.top & set(np.flatnonzero(evald).tolist())) / C.TOPN
        curve.append({"n": int(evald.sum()), "cost": cost, "recall": rec})
        if max_frac is not None and cost >= max_frac * env.total:
            break
    out = {"curve": curve}
    if log:
        out["events"] = events
    return out


def seeds_for(receiver, n):
    return [E14.crc(f"exp16|{receiver}|{s}") for s in range(n)]


def campaign_values(env, swarms, inner, outer, share, seeds, max_frac=0.3):
    out = np.empty(len(seeds))
    for j, s in enumerate(seeds):
        r = run_multi(env, swarms, inner, outer, share, s, max_frac=max_frac)
        out[j] = C.summarise(r["curve"], env.total)["early_recall_area"]
    return out


def shapley(v, players):
    n = len(players)
    phi = {}
    for p in players:
        others = [q for q in players if q != p]
        acc = 0.0
        for r in range(n):
            w = math.factorial(r) * math.factorial(n - r - 1) / math.factorial(n)
            for Sx in itertools.combinations(others, r):
                acc = acc + w * (v[frozenset(Sx) | {p}] - v[frozenset(Sx)])
        phi[p] = acc
    return phi


def owen(v, unions):
    """Owen value with a priori unions (lists of players); v maps frozensets of players to values."""
    mu = len(unions)
    f = math.factorial
    phi = {}
    for kx, B in enumerate(unions):
        others = [u for i, u in enumerate(unions) if i != kx]
        b = len(B)
        for i in B:
            rest = [x for x in B if x != i]
            acc = 0.0
            for t in range(mu):
                wT = f(t) * f(mu - t - 1) / f(mu)
                for T in itertools.combinations(others, t):
                    Q = frozenset(x for u in T for x in u)
                    for r in range(b):
                        wR = f(r) * f(b - r - 1) / f(b)
                        for R in itertools.combinations(rest, r):
                            Rs = frozenset(R)
                            acc = acc + wT * wR * (v[Q | Rs | {i}] - v[Q | Rs])
            phi[i] = acc
    return phi


# ------------------------------------------------------------------ jobs

def job_team(args):
    receiver, cfg, inner, outer, share, nseeds = args
    env = E14.Env(receiver)
    sw = CONFIGS[cfg]
    ea, c8 = [], []
    grid = np.linspace(0, 1, 101)
    curves = []
    for s in seeds_for(receiver, nseeds):
        r = run_multi(env, sw, inner, outer, share, s)
        sm = C.summarise(r["curve"], env.total)
        ea.append(sm["early_recall_area"])
        c8.append(sm["cost_frac_to_8of10"])
        cx = np.array([0.0] + [p["cost"] / env.total for p in r["curve"]])
        cy = np.array([0.0] + [p["recall"] for p in r["curve"]])
        curves.append(cy[np.searchsorted(cx, grid, side="right") - 1])
    g = np.array(curves)
    return (receiver, cfg, inner, outer, share,
            {"early_recall_area": ea, "cost_frac_to_8of10": c8,
             "band": {"grid": grid.tolist(), "mean": g.mean(0).tolist(),
                      "p05": np.percentile(g, 5, 0).tolist(), "p95": np.percentile(g, 95, 0).tolist()}})


def job_game(args):
    receiver, cfg, inner, outer, share, nseeds, level = args
    env = E14.Env(receiver)
    sw = CONFIGS[cfg]
    seeds = seeds_for(receiver, nseeds)
    if level == "swarm":
        players = list(range(len(sw)))
        v = {}
        for r in range(len(players) + 1):
            for T in itertools.combinations(players, r):
                v[frozenset(T)] = campaign_values(env, [sw[j] for j in T], inner, outer, share, seeds)
        phi = shapley(v, players)
        res = {"players": [" + ".join(s) for s in sw], "size": [len(s) for s in sw],
               "shapley": [float(np.mean(phi[j])) for j in players],
               "shapley_p05": [float(np.percentile(phi[j], 5)) for j in players],
               "shapley_p95": [float(np.percentile(phi[j], 95)) for j in players],
               "v_alone": [float(np.mean(v[frozenset([j])])) for j in players],
               "v_all": float(np.mean(v[frozenset(players)])), "v_empty": float(np.mean(v[frozenset()]))}
    else:
        bodies = [a for s in sw for a in s]
        v = {}
        for r in range(len(bodies) + 1):
            for S in itertools.combinations(bodies, r):
                Ss = set(S)
                v[frozenset(S)] = campaign_values(env, [[a for a in s if a in Ss] for s in sw],
                                                  inner, outer, share, seeds)
        sh = shapley(v, bodies)
        ow = owen(v, sw)
        d = {a: ow[a] - sh[a] for a in bodies}
        res = {"bodies": bodies, "unions": sw,
               "shapley": {a: float(np.mean(sh[a])) for a in bodies},
               "owen": {a: float(np.mean(ow[a])) for a in bodies},
               "owen_minus_shapley": {a: float(np.mean(d[a])) for a in bodies},
               "owen_minus_shapley_p05": {a: float(np.percentile(d[a], 5)) for a in bodies},
               "owen_minus_shapley_p95": {a: float(np.percentile(d[a], 95)) for a in bodies},
               "union_share_owen": [float(np.mean(sum(ow[a] for a in s))) for s in sw],
               "union_owen_minus_shapley_all": [np.round(sum(d[a] for a in s), 6).tolist() for s in sw],
               "v_all": float(np.mean(v[frozenset(bodies)])), "v_empty": float(np.mean(v[frozenset()]))}
    return (receiver, cfg, inner, outer, share, level, res)


# ------------------------------------------------------------------ self-test

def selftest():
    env = E14.Env("qe_pbe")
    ok = []
    # 1. one swarm reproduces experiment 14 exactly (flat and emergent), whatever outer and share
    for inner in INNER:
        for outer in OUTER:
            for share in SHARE:
                a = run_multi(env, [A], inner, outer, share, 11)["curve"]
                b = E14.run(env, A, inner, 11)["curve"]
                ok.append(a == b)
    # 2. full runs evaluate the whole pool once and spend the full cost
    for cfg in ("split_2_2_3", "dup_7_3"):
        r = run_multi(env, CONFIGS[cfg], "emergent", "record", "isolated", 5)["curve"]
        ok.append(r[-1]["n"] == env.n and abs(r[-1]["cost"] - env.total) < 1e-6 * env.total)
    # 3. determinism, and empty swarms drop out
    ok.append(run_multi(env, CONFIGS["split_4_3"], "emergent", "size", "published", 3)["curve"]
              == run_multi(env, CONFIGS["split_4_3"], "emergent", "size", "published", 3)["curve"])
    ok.append(run_multi(env, [["mace_relax"], []], "flat", "equal", "isolated", 4)["curve"]
              == run_multi(env, [["mace_relax"]], "flat", "equal", "isolated", 4)["curve"])
    # 4. Owen value: efficiency, quotient property, reduction to Shapley for trivial unions
    pl = ["a", "b", "c", "d"]
    rng = np.random.default_rng(0)
    vv = {frozenset(S): (0.0 if not S else float(rng.random() + len(S) ** 1.5))
          for r in range(5) for S in itertools.combinations(pl, r)}
    U = [["a", "b"], ["c", "d"]]
    ow = owen(vv, U)
    ok.append(abs(sum(ow.values()) - vv[frozenset(pl)]) < 1e-12)
    vq = {frozenset(T): vv[frozenset(x for j in T for x in U[j])] for r in range(3) for T in itertools.combinations(range(2), r)}
    shq = shapley(vq, [0, 1])
    ok.append(abs(ow["a"] + ow["b"] - shq[0]) < 1e-12)
    sh = shapley(vv, pl)
    ok.append(all(abs(owen(vv, [pl])[p] - sh[p]) < 1e-12 for p in pl))
    ok.append(all(abs(owen(vv, [[p] for p in pl])[p] - sh[p]) < 1e-12 for p in pl))
    print("selftest", sum(ok), "/", len(ok), ok)
    return all(ok)


# ------------------------------------------------------------------ report

def write_report(team, games):
    L = ["# Experiment 16: several swarms in one campaign", "",
         "Value = early-window recall area of the ten most stable compounds (mean over matched seeds).",
         "Batch of 4 shared by all swarms: every configuration spends the same compute.", ""]
    for r in RECEIVERS:
        if r not in team:
            continue
        L += [f"## Team values, receiver {r}", "",
              "| configuration | inner | outer | isolated | published |", "|---|---|---|---|---|"]
        for cfg in CONFIGS:
            for inner in INNER:
                for outer in OUTER:
                    cells = []
                    for share in SHARE:
                        e = team[r].get(f"{cfg}|{inner}|{outer}|{share}")
                        cells.append("" if e is None else f"{np.mean(e['early_recall_area']):.3f}")
                    if any(cells):
                        L.append(f"| {cfg} | {inner} | {outer} | {cells[0]} | {cells[1]} |")
        L.append("")
    L += ["## Swarm games (Shapley over swarms)", ""]
    for key, g in games.items():
        if not key.endswith("|swarm"):
            continue
        L.append(f"### {key}")
        L.append(f"v(all) {g['v_all']:.3f}, v(empty) {g['v_empty']:.3f}")
        for p, sz, s, va in zip(g["players"], g["size"], g["shapley"], g["v_alone"]):
            L.append(f"- size {sz}: Shapley {s:+.3f} (per body {s / sz:+.3f}), alone {va:.3f}: {p}")
        L.append("")
    L += ["## Body games (Owen value with swarms as unions, minus Shapley)", ""]
    for key, g in games.items():
        if not key.endswith("|body"):
            continue
        L.append(f"### {key}")
        L.append("unions: " + " | ".join(" + ".join(u) for u in g["unions"]))
        for a in g["bodies"]:
            L.append(f"- {a}: Shapley {g['shapley'][a]:+.3f}, Owen {g['owen'][a]:+.3f}, "
                     f"Owen - Shapley {g['owen_minus_shapley'][a]:+.3f} "
                     f"[{g['owen_minus_shapley_p05'][a]:+.3f}, {g['owen_minus_shapley_p95'][a]:+.3f}]")
        L.append("")
    (OUT / "multiple_swarms.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--seeds", type=int, default=100)
    ap.add_argument("--game-seeds", type=int, default=100)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--stage", default="all", choices=["team", "games", "all", "report"])
    args = ap.parse_args()
    if args.selftest:
        raise SystemExit(0 if selftest() else 1)
    OUT.mkdir(parents=True, exist_ok=True)
    tfile, gfile = OUT / "team_values.json", OUT / "games.json"
    team = json.loads(tfile.read_text(encoding="utf-8")) if tfile.exists() else {}
    games = json.loads(gfile.read_text(encoding="utf-8")) if gfile.exists() else {}
    t0 = time.time()
    if args.stage in ("team", "all"):
        jobs = [(r, cfg, inner, outer, share, args.seeds) for r in RECEIVERS for cfg in CONFIGS
                for inner in INNER for outer in (OUTER if len(CONFIGS[cfg]) > 1 else ["equal"])
                for share in (SHARE if len(CONFIGS[cfg]) > 1 else ["published"])]
        with Pool(args.workers) as pool:
            for r, cfg, inner, outer, share, res in pool.imap_unordered(job_team, jobs):
                team.setdefault(r, {})[f"{cfg}|{inner}|{outer}|{share}"] = res
                print(r, cfg, inner, outer, share, round(float(np.mean(res["early_recall_area"])), 4),
                      round(time.time() - t0), "s", flush=True)
        tfile.write_text(json.dumps(team), encoding="utf-8")
    if args.stage in ("games", "all"):
        jobs = []
        for r in GAME_RECEIVERS:
            for share in SHARE:
                for outer in ("equal", "size"):
                    for cfg in CONFIGS:
                        if len(CONFIGS[cfg]) > 1:
                            jobs.append((r, cfg, "emergent", outer, share, args.game_seeds, "swarm"))
                    for cfg in PARTITIONS:
                        jobs.append((r, cfg, "emergent", outer, share, args.game_seeds, "body"))
        with Pool(args.workers) as pool:
            for r, cfg, inner, outer, share, level, res in pool.imap_unordered(job_game, jobs):
                games[f"{r}|{cfg}|{inner}|{outer}|{share}|{level}"] = res
                gfile.write_text(json.dumps(games, indent=1), encoding="utf-8")
                print("game", r, cfg, outer, share, level, round(time.time() - t0), "s", flush=True)
    write_report(team, games)


if __name__ == "__main__":
    main()
