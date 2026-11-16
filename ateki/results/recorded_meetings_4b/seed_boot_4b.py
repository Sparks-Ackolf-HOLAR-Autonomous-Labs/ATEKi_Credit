"""Seed-level intervals for the finer task (Experiment 13), G3 Fig 8b rows 3-4.

Each seed's flat run is the control for all five coordinator rotations, so the
100 coordinated-minus-flat differences are not independent. This resamples the
20 seeds (with their five rotation pairs each) instead of the 100 pairs.
Pairs and quantities are those of analyze_4b.py (coordinator effect L196-206,
role premium under the "mean" rule L160-175).
B = 20000, numpy default_rng(20261101), percentile 95%.
Usage: python seed_boot_4b.py [out.json]"""
import json, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import analyze_4b as A

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "seed_boot_4b.json"
B, SEED = 20000, 20261101

flat = A.load("flat")
rot = {r: A.load(f"rot{r}") for r in range(5)}
flat_sh = {s: A.rule_shares(g, "mean") for s, g in flat.items()}
eff, prem = {}, {}
for r, v in rot.items():
    db = A.DB_ORDER[r]
    for s, g in v.items():
        if s not in flat:
            continue
        eff.setdefault(s, []).append(A.team_tau(g) - A.team_tau(flat[s]))
        c = A.rule_shares(g, "mean")["agent1"]
        prem.setdefault(s, []).append(c - flat_sh[s][A.agent_of(flat[s], db)])


def seed_boot(by_seed):
    seeds = sorted(by_seed)
    M = np.array([by_seed[s] for s in seeds])          # seeds x rotations
    rng = np.random.default_rng(SEED)
    idx = rng.integers(0, len(seeds), (B, len(seeds)))
    bm = M[idx].mean(axis=(1, 2))
    sm = M.mean(1)
    return {"pooled_mean": round(float(M.mean()), 4),
            "seed_ci95": [round(float(np.percentile(bm, 2.5)), 4),
                          round(float(np.percentile(bm, 97.5)), 4)],
            "n_seeds": len(seeds), "n_pairs": int(M.size),
            "pairs_per_seed": sorted({len(by_seed[s]) for s in seeds}),
            "seeds_with_positive_mean": f"{int((sm > 0).sum())}/{len(seeds)}"}


R = {"method": "resample seeds (each with its five rotation pairs); B=20000, "
               "numpy default_rng(20261101) per quantity, percentile 95%",
     "source": "ateki/results/recorded_meetings_4b (analyze_4b.py pairs)",
     "coordinator_effect": seed_boot(eff),
     "role_premium_mean": seed_boot(prem)}
OUT.write_text(json.dumps(R, indent=1) + "\n")
print(json.dumps(R, indent=1))
