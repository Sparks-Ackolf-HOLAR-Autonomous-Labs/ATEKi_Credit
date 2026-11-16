# Experiment 20: data-valuation estimators on the seven-database game

Receiver: experimental band-gap compilation. Window: final. Games: seed average and 10 per-seed games, 128 measured coalitions each. w(N) = -0.0667.

## Values (seed-averaged game)

| Database | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| JARVIS TBmBJ | -0.0113 | -0.0070 | +0.0000 | -0.0227 | -0.0400 | -0.0049 | -0.0022 |
| JARVIS OptB88vdW | -0.0228 | -0.0115 | -0.0190 | -0.0394 | -0.0640 | -0.0164 | -0.0188 |
| MP GGA | -0.0234 | -0.0147 | +0.0095 | -0.0535 | -0.0861 | -0.0022 | +0.0051 |
| MP GGA (ICSD-provenance subset) | -0.0224 | -0.0219 | +0.0000 | -0.0331 | -0.0453 | -0.0131 | -0.0056 |
| MP r2SCAN | -0.0237 | -0.0135 | -0.0095 | -0.0442 | -0.0715 | -0.0127 | -0.0113 |
| SNUMAT GGA | +0.0185 | +0.0204 | +0.0095 | +0.0232 | +0.0185 | +0.0115 | +0.0088 |
| SNUMAT HSE | +0.0185 | +0.0204 | +0.0095 | +0.0232 | +0.0185 | +0.0115 | +0.0088 |

## Duplicate check

- LOO of the identical SNUMAT pair: +0.0095, +0.0095
- LOO of MP GGA and its ICSD-provenance subset: +0.0095, +0.0000
- second SNUMAT copy alone: +0.0000; with other donors present: mean +0.0273, range -0.0095 to +0.0667, positive in 81% of coalitions

## Consistency across seeds

| Estimator | mean pairwise Spearman | min | mean Spearman to averaged Shapley | seeds with Shapley bottom | seeds with sign flip vs own Shapley |
|---|---|---|---|---|---|
| shapley | 0.194 | -0.925 | 0.444 | 1 | 0 |
| banzhaf | 0.188 | -0.925 | 0.414 | 0 | 3 |
| loo | -0.104 | -1.000 | 0.153 | 0 | 10 |
| beta_4_1 | 0.162 | -0.818 | 0.434 | 1 | 5 |
| beta_16_1 | 0.141 | -0.927 | 0.408 | 0 | 5 |
| beta_1_4 | 0.105 | -0.964 | 0.389 | 1 | 4 |
| beta_1_16 | 0.113 | -0.964 | 0.371 | 0 | 6 |

## Truncated Monte Carlo Shapley

| tolerance / w(N) | permutations | median max error | 90th pct | repeats with sign flip | lookups |
|---|---|---|---|---|---|
| 0.00 | 21 | 0.0117 | 0.0170 | 5/50 | 147 |
| 0.00 | 1000 | 0.0016 | 0.0024 | 0/50 | 7000 |
| 0.01 | 21 | 0.0107 | 0.0170 | 1/50 | 102 |
| 0.01 | 1000 | 0.0044 | 0.0053 | 0/50 | 4840 |
| 0.05 | 21 | 0.0105 | 0.0159 | 1/50 | 101 |
| 0.05 | 1000 | 0.0043 | 0.0052 | 0/50 | 4848 |
| 0.25 | 21 | 0.0143 | 0.0181 | 2/50 | 58 |
| 0.25 | 1000 | 0.0100 | 0.0107 | 0/50 | 2719 |

Truncation at the seed noise of w(N) (tolerance 0.0319): max |bias| 0.0147.
