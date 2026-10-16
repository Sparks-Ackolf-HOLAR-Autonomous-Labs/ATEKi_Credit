#!/usr/bin/env python3
"""Per-run coalition values for the band-gap Shapley game (HSE06 receiver,
no-halide pool), so that Fig. 4(a) of the ATEKi draft can carry intervals.

Re-runs only the Shapley block of campaign_gap.py (this folder)
(--receiver qe_hse06 --pool nohalide --shapley [--cost combined]) with the
same deterministic seeds (camp.crc of the same strings), and stores every
coalition value per run (20 seeds x batches of one and four = 40 runs) in
the format of the Al-Mg-Si coalitions.json files. Single process.

Usage: python shapley_per_run.py [--cost receiver|combined] [--time-only]
Output: results/campaigns/qe_hse06_nohalide[_combined]/coalitions.json
"""
import argparse
import importlib.util
import itertools
import json
import math
import os
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"  # single core
from pathlib import Path

import numpy as np

SEMI = Path(__file__).resolve().parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cost", default="receiver", choices=["receiver", "combined"])
    ap.add_argument("--time-only", action="store_true")
    args = ap.parse_args()
    cg = _load("campaign_gap", SEMI / "campaign_gap.py")
    camp = cg.camp
    tabs, idx = cg.load_tables()
    rec = tabs["qe_hse06"]
    pool = [c for c in sorted(rec) if cg.family(idx[c]["formula"]) != "halide"]
    donor_names = ["qe_pbe", "qe_hse06", *cg.ARCHIVES, "expt_zhuo"]
    donors = {d: tabs[d] for d in donor_names if d != "qe_hse06" and d in tabs
              and sum(c in tabs[d] for c in pool) >= 10}
    X = {c: cg.descriptor(idx[c]["formula"]) for c in pool}
    lo = np.min([X[c] for c in pool], 0)
    hi = np.max([X[c] for c in pool], 0)
    X = {c: (X[c] - lo) / np.where(hi > lo, hi - lo, 1) for c in pool}
    pbe_upfront = 0.0
    rec_query = rec
    if args.cost == "combined":
        rec_query = {c: {**rec[c], "cost": rec[c]["cost"] + tabs["qe_pbe"][c]["cost"]} for c in rec
                     if c in tabs["qe_pbe"]}
        pbe_upfront = sum(tabs["qe_pbe"][c]["cost"] for c in pool)
    total = sum(rec_query[c]["cost"] for c in pool)
    ks, seeds = [1, 4], 20
    names = [d for d in donors if d in ("qe_pbe", "qe_hse06", "mp_gga", "jarvis_mbj", "snumat_hse", "expt_zhuo")]
    out = {}
    t0 = time.time()
    for mode in ("pooled_fixed", "pooled_learned"):
        per_run = {}
        for r_ in range(len(names) + 1):
            for S in itertools.combinations(names, r_):
                vals = []
                for k in ks:
                    for s in range(seeds):
                        pays_pbe = args.cost == "combined" and "qe_pbe" in S
                        r_tab = rec if (args.cost == "receiver" or pays_pbe) else rec_query
                        if not S:
                            res = camp.run_campaign("surrogate", r_tab, {}, pool, X, k, camp.crc(f"surrogate|{k}|{s}"))
                        else:
                            arm = mode if len(S) > 1 else ("fixed:" if mode == "pooled_fixed" else "learned:") + S[0]
                            res = camp.run_campaign(arm, r_tab, {d: donors[d] for d in S}, pool, X, k,
                                                    camp.crc(f"{mode}|{'+'.join(S)}|{k}|{s}"))
                        if pays_pbe:
                            res["curve"] = [{**p, "cost": p["cost"] + pbe_upfront} for p in res["curve"]]
                        vals.append(camp.summarise(res["curve"], total)["early_recall_area"])
                        if args.time_only:
                            print(f"one campaign: {time.time() - t0:.3f} s; "
                                  f"full job = {2 * 2 ** len(names) * len(ks) * seeds} campaigns")
                            return
                per_run["+".join(sorted(S))] = vals
        n = len(names)
        v = {k: float(np.mean(x)) for k, x in per_run.items()}
        phi = {}
        for p in names:
            others = [q for q in names if q != p]
            phi[p] = sum(math.factorial(r_) * math.factorial(n - r_ - 1) / math.factorial(n)
                         * (v["+".join(sorted(S + (p,)))] - v["+".join(sorted(S))])
                         for r_ in range(n) for S in itertools.combinations(others, r_))
        out[mode] = {"players": names, "runs": [f"k{k}|s{s}" for k in ks for s in range(seeds)],
                     "per_run": per_run, "shapley_of_means": phi}
        print(mode, {p: round(x, 4) for p, x in phi.items()}, f"{time.time() - t0:.0f} s")
    tag = "qe_hse06_nohalide" + ("_combined" if args.cost == "combined" else "")
    dest = SEMI / "results" / "campaigns" / tag / "coalitions.json"
    dest.write_text(json.dumps(out, indent=1))
    print("wrote", dest)


if __name__ == "__main__":
    main()
