# Experiment 20: data-valuation estimators on the seven-database game

Receiver: experimental band-gap compilation. Window: early. Games: seed average and 10 per-seed games, 128 measured coalitions each. w(N) = +0.0419.

## Values (seed-averaged game)

| Database | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| JARVIS TBmBJ | -0.0134 | -0.0188 | -0.0160 | -0.0008 | +0.0068 | -0.0219 | -0.0199 |
| JARVIS OptB88vdW | -0.0051 | -0.0076 | -0.0133 | +0.0037 | +0.0096 | -0.0119 | -0.0133 |
| MP GGA | -0.0294 | -0.0357 | -0.0038 | -0.0301 | -0.0277 | -0.0235 | -0.0129 |
| MP GGA (ICSD-provenance subset) | -0.0234 | -0.0284 | -0.0103 | -0.0196 | -0.0168 | -0.0231 | -0.0165 |
| MP r2SCAN | +0.0054 | -0.0023 | +0.0076 | +0.0174 | +0.0261 | -0.0008 | +0.0033 |
| SNUMAT GGA | +0.0539 | +0.0462 | +0.0286 | +0.0810 | +0.0999 | +0.0330 | +0.0286 |
| SNUMAT HSE | +0.0539 | +0.0462 | +0.0286 | +0.0810 | +0.0999 | +0.0330 | +0.0286 |

## Duplicate check

- LOO of the identical SNUMAT pair: +0.0286, +0.0286
- LOO of MP GGA and its ICSD-provenance subset: -0.0038, -0.0103
- second SNUMAT copy alone: +0.0000; with other donors present: mean +0.0425, range -0.0099 to +0.1013, positive in 97% of coalitions

## Consistency across seeds

| Estimator | mean pairwise Spearman | min | mean Spearman to averaged Shapley | seeds with Shapley bottom | seeds with sign flip vs own Shapley |
|---|---|---|---|---|---|
| shapley | 0.678 | -0.164 | 0.836 | 5 | 0 |
| banzhaf | 0.794 | 0.330 | 0.889 | 5 | 6 |
| loo | 0.379 | -0.971 | 0.551 | 1 | 10 |
| beta_4_1 | 0.578 | -0.382 | 0.782 | 6 | 7 |
| beta_16_1 | 0.480 | -0.673 | 0.720 | 5 | 8 |
| beta_1_4 | 0.523 | -0.855 | 0.737 | 3 | 6 |
| beta_1_16 | 0.398 | -0.855 | 0.611 | 1 | 7 |

## Truncated Monte Carlo Shapley

| tolerance / w(N) | permutations | median max error | 90th pct | repeats with sign flip | lookups |
|---|---|---|---|---|---|
| 0.00 | 21 | 0.0099 | 0.0139 | 16/50 | 147 |
| 0.00 | 1000 | 0.0014 | 0.0025 | 0/50 | 7000 |
| 0.01 | 21 | 0.0126 | 0.0183 | 23/50 | 135 |
| 0.01 | 1000 | 0.0039 | 0.0052 | 0/50 | 6425 |
| 0.05 | 21 | 0.0120 | 0.0190 | 17/50 | 131 |
| 0.05 | 1000 | 0.0048 | 0.0066 | 0/50 | 6283 |
| 0.25 | 21 | 0.0156 | 0.0236 | 18/50 | 113 |
| 0.25 | 1000 | 0.0089 | 0.0101 | 0/50 | 5323 |

Truncation at the seed noise of w(N) (tolerance 0.0216): max |bias| 0.0190.
