# Experiment 09: Harsanyi dividends of the seven-database game

Receiver `expt_zhuo`; characteristic function = the 128 measured coalition values of experiment 08 (early (primary window of exp 08) window; source `ateki/results/database_attribution/expt_zhuo/database_attribution.json`, cross-checked against `ateki/results/database_attribution/coalitions/expt_zhuo`). No new campaigns were run.

d(S) = sum_{T subset S} (-1)^{|S|-|T|} v(T) (Moebius inversion on the subset lattice). v(empty) = +0.6949, v(N) = +0.7368; best coalition: MP r2SCAN + SNUMAT GGA + SNUMAT HSE06, v = +0.8514.

## Checks

- checkpoint_vs_json_max_gap: 0.00e+00
- moebius_fast_vs_brute_max_gap: 2.22e-16
- zeta_roundtrip_max_gap: 0.00e+00
- shapley_from_dividends_vs_committed_max_gap: 3.30e-17
- banzhaf_from_dividends_vs_committed_max_gap: 2.08e-17
- sum_nonempty_dividends_minus_(vN-v0): 0.00e+00
- per_seed_linearity_max_gap: 7.77e-16

## Dividend mass by coalition order

| order | #coalitions | sum d | sum abs d | sum d>0 | sum d<0 | #pos | #neg | sum d, 95% CI over seeds |
|---|---|---|---|---|---|---|---|---|
| 1 | 7 | +0.2088 | 0.3063 | +0.2575 | -0.0488 | 5 | 2 | [-0.1093, +0.5543] |
| 2 | 21 | +0.1139 | 0.4423 | +0.2781 | -0.1642 | 16 | 5 | [-1.1357, +1.3055] |
| 3 | 35 | -2.0065 | 2.1390 | +0.0663 | -2.0728 | 3 | 32 | [-4.7144, +0.5543] |
| 4 | 35 | +4.8057 | 4.8057 | +4.8057 | +0.0000 | 35 | 0 | [+0.9161, +9.2267] |
| 5 | 21 | -5.6244 | 5.6244 | +0.0000 | -5.6244 | 0 | 21 | [-10.0988, -1.7600] |
| 6 | 7 | +3.3074 | 3.3074 | +3.3074 | +0.0000 | 7 | 0 | [+1.1409, +5.8808] |
| 7 | 1 | -0.7630 | 0.7630 | +0.0000 | -0.7630 | 0 | 1 | [-1.4004, -0.2304] |

Total |d| over nonempty coalitions: 17.3882; v(N) - v(empty) = +0.0419; net of orders 2..7 = -0.1669.

Order-2 split: the 11 pairs containing a SNUMAT source sum to -0.0385 (3 of them negative); the remaining pairs sum to +0.1524.

## Best attainable value by coalition size

| size | best v(S) | coalition |
|---|---|---|
| 0 | +0.6949 | (cold campaign) |
| 1 | +0.8019 | SNUMAT GGA |
| 2 | +0.8457 | MP r2SCAN + SNUMAT GGA |
| 3 | +0.8514 | MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 |
| 4 | +0.8373 | JARVIS OptB88vdW + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 |
| 5 | +0.8023 | JARVIS OptB88vdW + MP GGA (ICSD-provenance subset) + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 |
| 6 | +0.7528 | JARVIS OptB88vdW + MP GGA + MP GGA (ICSD-provenance subset) + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 |
| 7 | +0.7368 | JARVIS TBmBJ + JARVIS OptB88vdW + MP GGA + MP GGA (ICSD-provenance subset) + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 |

## Largest positive higher-order dividends (|S| >= 2)

| order | coalition | d(S) | 95% CI over seeds |
|---|---|---|---|
| 6 | JARVIS TBmBJ + MP GGA + MP GGA (ICSD-provenance subset) + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 | +0.5836 | [+0.2552, +0.9406] |
| 6 | JARVIS TBmBJ + JARVIS OptB88vdW + MP GGA + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 | +0.5562 | [+0.1924, +1.0038] |
| 6 | JARVIS TBmBJ + JARVIS OptB88vdW + MP GGA + MP GGA (ICSD-provenance subset) + SNUMAT GGA + SNUMAT HSE06 | +0.5562 | [+0.1962, +0.9886] |
| 6 | JARVIS OptB88vdW + MP GGA + MP GGA (ICSD-provenance subset) + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 | +0.4590 | [+0.1580, +0.8190] |
| 6 | JARVIS TBmBJ + JARVIS OptB88vdW + MP GGA + MP GGA (ICSD-provenance subset) + MP r2SCAN + SNUMAT HSE06 | +0.4091 | [+0.0705, +0.8225] |
| 6 | JARVIS TBmBJ + JARVIS OptB88vdW + MP GGA + MP GGA (ICSD-provenance subset) + MP r2SCAN + SNUMAT GGA | +0.4091 | [+0.0648, +0.8126] |
| 6 | JARVIS TBmBJ + JARVIS OptB88vdW + MP GGA (ICSD-provenance subset) + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 | +0.3341 | [+0.1467, +0.5566] |
| 4 | MP GGA + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 | +0.1893 | [+0.0255, +0.3710] |

## Largest negative higher-order dividends (|S| >= 2)

| order | coalition | d(S) | 95% CI over seeds |
|---|---|---|---|
| 7 | JARVIS TBmBJ + JARVIS OptB88vdW + MP GGA + MP GGA (ICSD-provenance subset) + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 | -0.7630 | [-1.4072, -0.2381] |
| 5 | JARVIS TBmBJ + MP GGA + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 | -0.3943 | [-0.6686, -0.1486] |
| 5 | MP GGA + MP GGA (ICSD-provenance subset) + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 | -0.3451 | [-0.5893, -0.1257] |
| 5 | JARVIS TBmBJ + JARVIS OptB88vdW + MP GGA + SNUMAT GGA + SNUMAT HSE06 | -0.3383 | [-0.6251, -0.0933] |
| 5 | JARVIS TBmBJ + MP GGA + MP GGA (ICSD-provenance subset) + SNUMAT GGA + SNUMAT HSE06 | -0.3280 | [-0.5524, -0.1318] |
| 5 | JARVIS OptB88vdW + MP GGA + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 | -0.2964 | [-0.4949, -0.1200] |
| 5 | JARVIS TBmBJ + JARVIS OptB88vdW + MP GGA + MP GGA (ICSD-provenance subset) + SNUMAT GGA | -0.2853 | [-0.5798, -0.0400] |
| 5 | JARVIS TBmBJ + JARVIS OptB88vdW + MP GGA + MP GGA (ICSD-provenance subset) + SNUMAT HSE06 | -0.2853 | [-0.5646, -0.0419] |

## Singleton dividends d({i}) = v({i}) - v(empty)

- SNUMAT GGA: +0.1070
- SNUMAT HSE06: +0.1070
- MP r2SCAN: +0.0267
- JARVIS OptB88vdW: +0.0103
- JARVIS TBmBJ: +0.0065
- MP GGA (ICSD-provenance subset): -0.0190
- MP GGA: -0.0297

## All pairwise dividends (sorted)

| pair | d(S) | 95% CI over seeds |
|---|---|---|
| SNUMAT GGA + SNUMAT HSE06 | -0.1070 | [-0.1867, -0.0343] |
| JARVIS OptB88vdW + SNUMAT GGA | -0.0244 | [-0.0949, +0.0400] |
| JARVIS OptB88vdW + SNUMAT HSE06 | -0.0244 | [-0.0930, +0.0408] |
| JARVIS TBmBJ + MP r2SCAN | -0.0065 | [-0.0571, +0.0491] |
| MP GGA (ICSD-provenance subset) + MP r2SCAN | -0.0019 | [-0.0495, +0.0552] |
| JARVIS TBmBJ + MP GGA (ICSD-provenance subset) | +0.0107 | [-0.0343, +0.0560] |
| MP GGA + MP r2SCAN | +0.0107 | [-0.0389, +0.0678] |
| JARVIS OptB88vdW + MP GGA | +0.0114 | [-0.0495, +0.0724] |
| MP GGA + SNUMAT GGA | +0.0130 | [-0.0857, +0.1029] |
| MP GGA + SNUMAT HSE06 | +0.0130 | [-0.0857, +0.1048] |
| JARVIS TBmBJ + SNUMAT GGA | +0.0130 | [-0.0651, +0.0792] |
| JARVIS TBmBJ + SNUMAT HSE06 | +0.0130 | [-0.0648, +0.0792] |
| MP GGA (ICSD-provenance subset) + SNUMAT GGA | +0.0156 | [-0.0381, +0.0655] |
| MP GGA (ICSD-provenance subset) + SNUMAT HSE06 | +0.0156 | [-0.0381, +0.0659] |
| MP r2SCAN + SNUMAT GGA | +0.0171 | [-0.0438, +0.0762] |
| MP r2SCAN + SNUMAT HSE06 | +0.0171 | [-0.0457, +0.0762] |
| JARVIS TBmBJ + MP GGA | +0.0202 | [-0.0248, +0.0629] |
| JARVIS OptB88vdW + MP r2SCAN | +0.0210 | [-0.0324, +0.0819] |
| JARVIS TBmBJ + JARVIS OptB88vdW | +0.0248 | [-0.0495, +0.0971] |
| JARVIS OptB88vdW + MP GGA (ICSD-provenance subset) | +0.0286 | [-0.0305, +0.0952] |
| MP GGA + MP GGA (ICSD-provenance subset) | +0.0335 | [-0.0114, +0.0853] |

## SNUMAT GGA / SNUMAT HSE06 pair

- v(empty) = +0.6949, v(SNUMAT GGA) = +0.8019, v(SNUMAT HSE06) = +0.8019, v(both) = +0.8019
- pairwise dividend d = -0.1070 (95% CI over seeds [-0.1874, -0.0343]); rank 1 of 21 pairwise dividends (1 = most negative); |d| is 1.00 x the largest singleton dividend
- marginal value of adding the second SNUMAT source to a coalition already holding the first, over all 32 contexts: mean +0.0412, min -0.0099, max +0.1013
- max |v(S + SNUMAT GGA) - v(S + SNUMAT HSE06)| over contexts: 0.00e+00 (interchangeable players)

## Seven lose to four: inclusion-exclusion decomposition

v(N) - v(S*) = sum of d(T) over every T with a member outside S*, for each best four-donor coalition S*.

- S* = JARVIS OptB88vdW + MP r2SCAN + SNUMAT GGA + SNUMAT HSE06 (v = +0.8373; excluded: JARVIS TBmBJ, MP GGA, MP GGA (ICSD-provenance subset)): v(N) - v(S*) = -0.1006; by order of T: 1: -0.0423, 2: +0.2145, 3: -1.9310, 4: +4.7383, 5: -5.6244, 6: +3.3074, 7: -0.7630; identity gap 0.0e+00

