# Experiment 20: data-valuation estimators on the seven-database game

Receiver: experimental band-gap compilation. Window: early. Games: seed average and 10 per-seed games, 128 measured coalitions each. w(N) = +0.0419.

## Values (seed-averaged game)

| Database | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| JARVIS TBmBJ | -0.0067 | -0.0121 | -0.0095 | +0.0053 | +0.0165 | -0.0139 | -0.0125 |
| JARVIS OptB88vdW | -0.0130 | -0.0193 | -0.0114 | -0.0049 | +0.0070 | -0.0155 | -0.0131 |
| MP GGA | -0.0300 | -0.0356 | -0.0038 | -0.0344 | -0.0319 | -0.0206 | -0.0108 |
| MP GGA (ICSD-provenance subset) | -0.0228 | -0.0278 | -0.0095 | -0.0198 | -0.0136 | -0.0211 | -0.0150 |
| MP r2SCAN | +0.0064 | -0.0007 | +0.0038 | +0.0195 | +0.0333 | -0.0006 | +0.0014 |
| SNUMAT GGA | +0.0540 | +0.0428 | +0.0210 | +0.0888 | +0.1196 | +0.0289 | +0.0228 |
| SNUMAT HSE | +0.0540 | +0.0428 | +0.0210 | +0.0888 | +0.1196 | +0.0289 | +0.0228 |

## Duplicate check

- LOO of the identical SNUMAT pair: +0.0210, +0.0210
- LOO of MP GGA and its ICSD-provenance subset: -0.0038, -0.0095
- second SNUMAT copy alone: +0.0000; with other donors present: mean +0.0405, range +0.0114 to +0.0781, positive in 100% of coalitions

## Consistency across seeds

| Estimator | mean pairwise Spearman | min | mean Spearman to averaged Shapley | seeds with Shapley bottom | seeds with sign flip vs own Shapley |
|---|---|---|---|---|---|
| shapley | 0.733 | 0.257 | 0.855 | 5 | 0 |
| banzhaf | 0.714 | 0.200 | 0.836 | 5 | 7 |
| loo | 0.359 | -0.540 | 0.528 | 1 | 10 |
| beta_4_1 | 0.733 | 0.164 | 0.861 | 6 | 4 |
| beta_16_1 | 0.740 | 0.200 | 0.865 | 6 | 6 |
| beta_1_4 | 0.664 | 0.309 | 0.775 | 3 | 7 |
| beta_1_16 | 0.480 | -0.309 | 0.644 | 2 | 7 |

## Truncated Monte Carlo Shapley

| tolerance / w(N) | permutations | median max error | 90th pct | repeats with sign flip | lookups |
|---|---|---|---|---|---|
| 0.00 | 21 | 0.0093 | 0.0167 | 13/50 | 147 |
| 0.00 | 1000 | 0.0014 | 0.0023 | 0/50 | 7000 |
| 0.01 | 21 | 0.0161 | 0.0247 | 17/50 | 125 |
| 0.01 | 1000 | 0.0078 | 0.0094 | 0/50 | 5921 |
| 0.05 | 21 | 0.0145 | 0.0243 | 13/50 | 120 |
| 0.05 | 1000 | 0.0088 | 0.0102 | 0/50 | 5767 |
| 0.25 | 21 | 0.0221 | 0.0326 | 26/50 | 94 |
| 0.25 | 1000 | 0.0139 | 0.0158 | 0/50 | 4448 |

Truncation at the seed noise of w(N) (tolerance 0.0299): max |bias| 0.0260.
