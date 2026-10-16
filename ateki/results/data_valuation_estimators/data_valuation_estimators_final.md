# Experiment 20: data-valuation estimators on the seven-database game

Receiver: experimental band-gap compilation. Window: final. Games: seed average and 10 per-seed games, 128 measured coalitions each. w(N) = +0.0667.

## Values (seed-averaged game)

| Database | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| JARVIS TBmBJ | +0.0015 | -0.0021 | -0.0190 | +0.0136 | +0.0271 | -0.0077 | -0.0134 |
| JARVIS OptB88vdW | +0.0224 | +0.0185 | +0.0000 | +0.0386 | +0.0543 | +0.0099 | +0.0042 |
| MP GGA | -0.0052 | -0.0077 | -0.0095 | -0.0026 | +0.0037 | -0.0058 | -0.0070 |
| MP GGA (ICSD-provenance subset) | -0.0049 | -0.0080 | -0.0190 | +0.0061 | +0.0183 | -0.0128 | -0.0162 |
| MP r2SCAN | +0.0249 | +0.0125 | +0.0000 | +0.0549 | +0.0843 | +0.0054 | +0.0022 |
| SNUMAT GGA | +0.0140 | +0.0077 | -0.0190 | +0.0384 | +0.0603 | -0.0050 | -0.0132 |
| SNUMAT HSE | +0.0140 | +0.0077 | -0.0190 | +0.0384 | +0.0603 | -0.0050 | -0.0132 |

## Duplicate check

- LOO of the identical SNUMAT pair: -0.0190, -0.0190
- LOO of MP GGA and its ICSD-provenance subset: -0.0095, -0.0190
- second SNUMAT copy alone: +0.0000; with other donors present: mean -0.0037, range -0.0190 to +0.0095, positive in 23% of coalitions

## Consistency across seeds

| Estimator | mean pairwise Spearman | min | mean Spearman to averaged Shapley | seeds with Shapley bottom | seeds with sign flip vs own Shapley |
|---|---|---|---|---|---|
| shapley | 0.120 | -0.741 | 0.384 | 2 | 0 |
| banzhaf | 0.146 | -0.769 | 0.386 | 2 | 3 |
| loo | -0.029 | -0.730 | 0.243 | 0 | 10 |
| beta_4_1 | 0.213 | -0.745 | 0.457 | 4 | 3 |
| beta_16_1 | 0.212 | -0.745 | 0.453 | 3 | 3 |
| beta_1_4 | 0.092 | -0.697 | 0.343 | 2 | 4 |
| beta_1_16 | 0.074 | -0.667 | 0.327 | 2 | 6 |

## Truncated Monte Carlo Shapley

| tolerance / w(N) | permutations | median max error | 90th pct | repeats with sign flip | lookups |
|---|---|---|---|---|---|
| 0.00 | 21 | 0.0086 | 0.0155 | 23/50 | 147 |
| 0.00 | 1000 | 0.0014 | 0.0021 | 1/50 | 7000 |
| 0.01 | 21 | 0.0096 | 0.0164 | 25/50 | 86 |
| 0.01 | 1000 | 0.0053 | 0.0064 | 1/50 | 4155 |
| 0.05 | 21 | 0.0102 | 0.0142 | 22/50 | 88 |
| 0.05 | 1000 | 0.0050 | 0.0059 | 0/50 | 4164 |
| 0.25 | 21 | 0.0114 | 0.0163 | 44/50 | 44 |
| 0.25 | 1000 | 0.0079 | 0.0087 | 50/50 | 2007 |

Truncation at the seed noise of w(N) (tolerance 0.0248): max |bias| 0.0085.
