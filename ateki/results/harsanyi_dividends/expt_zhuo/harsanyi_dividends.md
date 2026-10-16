# Experiment 09: Harsanyi dividends of the seven-database game

Receiver `expt_zhuo`; characteristic function = the 128 measured coalition values of experiment 08 (early (primary window of exp 08) window; source `ateki/results/database_attribution/expt_zhuo/database_attribution.json`, cross-checked against `ateki/results/database_attribution/coalitions/expt_zhuo`). No new campaigns were run.

d(S) = sum_{T subset S} (-1)^{|S|-|T|} v(T) (Moebius inversion on the subset lattice). v(empty) = +0.6400, v(N) = +0.6819; best coalition: MP r2SCAN + SNUMAT GGA + SNUMAT HSE06, v = +0.7981.

## Checks

- checkpoint_vs_json_max_gap: 0.00e+00
- moebius_fast_vs_brute_max_gap: 0.00e+00
- zeta_roundtrip_max_gap: 0.00e+00
- shapley_from_dividends_vs_committed_max_gap: 1.39e-17
- banzhaf_from_dividends_vs_committed_max_gap: 1.39e-17
- sum_nonempty_dividends_minus_(vN-v0): 0.00e+00
- per_seed_linearity_max_gap: 1.43e-15

## Dividend mass by coalition order

| order | #coalitions | sum d | sum abs d | sum d>0 | sum d<0 | #pos | #neg | sum d, 95% CI over seeds |
|---|---|---|---|---|---|---|---|---|
| 1 | 7 | +0.3181 | 0.3981 | +0.3581 | -0.0400 | 5 | 2 | [-0.0781, +0.8019] |
| 2 | 21 | -0.6229 | 0.7562 | +0.0667 | -0.6895 | 5 | 16 | [-2.3200, +0.7676] |
| 3 | 35 | +0.1010 | 0.9390 | +0.5200 | -0.4190 | 19 | 16 | [-2.7200, +3.4153] |
| 4 | 35 | +1.3352 | 1.5676 | +1.4514 | -0.1162 | 28 | 7 | [-3.0058, +5.2667] |
| 5 | 21 | -2.1543 | 2.1543 | +0.0000 | -2.1543 | 0 | 21 | [-5.9029, +1.4077] |
| 6 | 7 | +1.3867 | 1.3867 | +1.3867 | +0.0000 | 7 | 0 | [-0.4019, +3.4192] |
| 7 | 1 | -0.3219 | 0.3219 | +0.0000 | -0.3219 | 0 | 1 | [-0.7905, +0.0686] |

Total |d| over nonempty coalitions: 7.5238; v(N) - v(empty) = +0.0419; net of orders 2..7 = -0.2762.

Order-2 split: the 11 pairs containing a SNUMAT source sum to -0.6038 (11 of them negative); the remaining pairs sum to -0.0190.

## Best attainable value by coalition size

| size | best v(S) | coalition |
|---|---|---|
| 0 | +0.6400 | (cold campaign) |
| 1 | +0.7790 | SNUMAT GGA |
| 2 | +0.7790 | SNUMAT GGA + SNUMAT HSE06 |
| 3 | +0.7981 | MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 |
| 4 | +0.7695 | JARVIS TBmBJ + JARVIS OptB88vdW + SNUMAT GGA + SNUMAT HSE06 |
| 5 | +0.7371 | JARVIS TBmBJ + JARVIS OptB88vdW + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 |
| 6 | +0.6933 | JARVIS TBmBJ + MP GGA + MP GGA (ICSD-provenance subset) + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 |
| 7 | +0.6819 | JARVIS TBmBJ + JARVIS OptB88vdW + MP GGA + MP GGA (ICSD-provenance subset) + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 |

## Largest positive higher-order dividends (|S| >= 2)

| order | coalition | d(S) | 95% CI over seeds |
|---|---|---|---|
| 6 | JARVIS TBmBJ + JARVIS OptB88vdW + MP GGA + MP GGA (ICSD-provenance subset) + SNUMAT GGA + SNUMAT HSE06 | +0.3010 | [-0.0229, +0.6514] |
| 6 | JARVIS TBmBJ + MP GGA + MP GGA (ICSD-provenance subset) + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 | +0.2400 | [-0.0914, +0.6191] |
| 6 | JARVIS TBmBJ + JARVIS OptB88vdW + MP GGA + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 | +0.1981 | [-0.0800, +0.5048] |
| 6 | JARVIS OptB88vdW + MP GGA + MP GGA (ICSD-provenance subset) + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 | +0.1924 | [-0.0705, +0.5105] |
| 6 | JARVIS TBmBJ + JARVIS OptB88vdW + MP GGA + MP GGA (ICSD-provenance subset) + MP r2SCAN + SNUMAT HSE06 | +0.1829 | [-0.0438, +0.4286] |
| 6 | JARVIS TBmBJ + JARVIS OptB88vdW + MP GGA + MP GGA (ICSD-provenance subset) + MP r2SCAN + SNUMAT GGA | +0.1829 | [-0.0381, +0.4248] |
| 3 | JARVIS OptB88vdW + SNUMAT GGA + SNUMAT HSE06 | +0.1067 | [+0.0210, +0.2133] |
| 4 | JARVIS TBmBJ + JARVIS OptB88vdW + MP GGA + MP GGA (ICSD-provenance subset) | +0.0914 | [-0.0419, +0.2095] |

## Largest negative higher-order dividends (|S| >= 2)

| order | coalition | d(S) | 95% CI over seeds |
|---|---|---|---|
| 7 | JARVIS TBmBJ + JARVIS OptB88vdW + MP GGA + MP GGA (ICSD-provenance subset) + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 | -0.3219 | [-0.7943, +0.0743] |
| 5 | JARVIS TBmBJ + JARVIS OptB88vdW + MP GGA + MP GGA (ICSD-provenance subset) + SNUMAT GGA | -0.1657 | [-0.3600, +0.0381] |
| 5 | JARVIS TBmBJ + JARVIS OptB88vdW + MP GGA + MP GGA (ICSD-provenance subset) + SNUMAT HSE06 | -0.1657 | [-0.3543, +0.0343] |
| 5 | MP GGA + MP GGA (ICSD-provenance subset) + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 | -0.1524 | [-0.4324, +0.0914] |
| 5 | JARVIS TBmBJ + JARVIS OptB88vdW + MP GGA + SNUMAT GGA + SNUMAT HSE06 | -0.1467 | [-0.3696, +0.1105] |
| 2 | SNUMAT GGA + SNUMAT HSE06 | -0.1390 | [-0.2171, -0.0743] |
| 5 | JARVIS TBmBJ + MP GGA + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 | -0.1352 | [-0.3848, +0.1029] |
| 5 | JARVIS TBmBJ + MP GGA + MP GGA (ICSD-provenance subset) + SNUMAT GGA + SNUMAT HSE06 | -0.1314 | [-0.3733, +0.0933] |

## Singleton dividends d({i}) = v({i}) - v(empty)

- SNUMAT GGA: +0.1390
- SNUMAT HSE06: +0.1390
- MP r2SCAN: +0.0419
- JARVIS TBmBJ: +0.0229
- JARVIS OptB88vdW: +0.0152
- MP GGA (ICSD-provenance subset): -0.0095
- MP GGA: -0.0305

## All pairwise dividends (sorted)

| pair | d(S) | 95% CI over seeds |
|---|---|---|
| SNUMAT GGA + SNUMAT HSE06 | -0.1390 | [-0.2171, -0.0743] |
| JARVIS OptB88vdW + SNUMAT GGA | -0.0705 | [-0.1543, +0.0000] |
| JARVIS OptB88vdW + SNUMAT HSE06 | -0.0705 | [-0.1543, +0.0019] |
| MP r2SCAN + SNUMAT GGA | -0.0457 | [-0.1238, +0.0248] |
| MP r2SCAN + SNUMAT HSE06 | -0.0457 | [-0.1219, +0.0229] |
| JARVIS TBmBJ + SNUMAT GGA | -0.0438 | [-0.1371, +0.0324] |
| JARVIS TBmBJ + SNUMAT HSE06 | -0.0438 | [-0.1352, +0.0324] |
| MP GGA + SNUMAT GGA | -0.0362 | [-0.1467, +0.0457] |
| MP GGA + SNUMAT HSE06 | -0.0362 | [-0.1467, +0.0457] |
| MP GGA (ICSD-provenance subset) + SNUMAT GGA | -0.0362 | [-0.1162, +0.0381] |
| MP GGA (ICSD-provenance subset) + SNUMAT HSE06 | -0.0362 | [-0.1219, +0.0381] |
| JARVIS TBmBJ + MP r2SCAN | -0.0324 | [-0.1143, +0.0324] |
| MP GGA (ICSD-provenance subset) + MP r2SCAN | -0.0229 | [-0.0990, +0.0381] |
| JARVIS OptB88vdW + MP r2SCAN | -0.0152 | [-0.0838, +0.0457] |
| JARVIS TBmBJ + JARVIS OptB88vdW | -0.0076 | [-0.0971, +0.0590] |
| JARVIS OptB88vdW + MP GGA (ICSD-provenance subset) | -0.0076 | [-0.0895, +0.0552] |
| MP GGA + MP r2SCAN | +0.0019 | [-0.0686, +0.0629] |
| JARVIS TBmBJ + MP GGA (ICSD-provenance subset) | +0.0038 | [-0.0743, +0.0724] |
| JARVIS OptB88vdW + MP GGA | +0.0152 | [-0.0552, +0.0743] |
| JARVIS TBmBJ + MP GGA | +0.0152 | [-0.0571, +0.0781] |
| MP GGA + MP GGA (ICSD-provenance subset) | +0.0305 | [-0.0476, +0.0990] |

## SNUMAT GGA / SNUMAT HSE06 pair

- v(empty) = +0.6400, v(SNUMAT GGA) = +0.7790, v(SNUMAT HSE06) = +0.7790, v(both) = +0.7790
- pairwise dividend d = -0.1390 (95% CI over seeds [-0.2171, -0.0743]); rank 1 of 21 pairwise dividends (1 = most negative); |d| is 1.00 x the largest singleton dividend
- marginal value of adding the second SNUMAT source to a coalition already holding the first, over all 32 contexts: mean +0.0392, min +0.0000, max +0.0781
- max |v(S + SNUMAT GGA) - v(S + SNUMAT HSE06)| over contexts: 0.00e+00 (interchangeable players)

## Seven lose to four: inclusion-exclusion decomposition

v(N) - v(S*) = sum of d(T) over every T with a member outside S*, for each best four-donor coalition S*.

- S* = JARVIS TBmBJ + JARVIS OptB88vdW + SNUMAT GGA + SNUMAT HSE06 (v = +0.7695; excluded: MP GGA, MP GGA (ICSD-provenance subset), MP r2SCAN): v(N) - v(S*) = -0.0876; by order of T: 1: +0.0019, 2: -0.2476, 3: -0.0762, 4: +1.3238, 5: -2.1543, 6: +1.3867, 7: -0.3219; identity gap 0.0e+00

