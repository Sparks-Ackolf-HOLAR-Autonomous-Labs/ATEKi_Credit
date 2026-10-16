# Experiment 20, second part: data-valuation estimators on the computed Al-Mg-Si games

Early recall area (share of the 10 most stable compounds found early). Games: run average and 40 per-run games (k = 1 and 4, 20 seeds), every coalition measured by compute/almgsi_campaign/campaign.py.

## Receiver QE PBE, fixed trust (w(N) = +0.0680)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| MACE-MP-0 relaxation | +0.2258 | +0.1930 | +0.2244 | +0.2737 | +0.3261 | +0.2042 | +0.2157 |
| NEP89 MD | -0.1966 | -0.2141 | -0.1590 | -0.1967 | -0.1788 | -0.1825 | -0.1663 |
| MEAM MD | -0.1094 | -0.1093 | +0.0368 | -0.2027 | -0.2425 | -0.0161 | +0.0236 |
| MP archive | +0.1481 | +0.1472 | +0.1459 | +0.1454 | +0.1489 | +0.1516 | +0.1498 |

| Estimator | mean pairwise Spearman (780 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 1.000 | 0/40 |
| banzhaf | 1.000 | 0/40 |
| loo | 1.000 | 40/40 |
| beta_4_1 | 0.914 | 3/40 |
| beta_16_1 | 1.000 | 9/40 |
| beta_1_4 | 1.000 | 1/40 |
| beta_1_16 | 1.000 | 39/40 |

TMC at 12 permutations (3n): sign flips in 0, 0, 0, 0 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0333.

## Receiver QE PBE, learned trust (w(N) = +0.2858)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| MACE-MP-0 relaxation | +0.1049 | +0.0712 | +0.0721 | +0.1712 | +0.2343 | +0.0656 | +0.0681 |
| NEP89 MD | +0.0434 | +0.0170 | +0.0219 | +0.0912 | +0.1399 | +0.0167 | +0.0194 |
| MEAM MD | +0.0239 | -0.0035 | +0.0470 | +0.0465 | +0.0841 | +0.0232 | +0.0388 |
| MP archive | +0.1136 | +0.0911 | +0.0158 | +0.2009 | +0.2651 | +0.0443 | +0.0238 |

| Estimator | mean pairwise Spearman (780 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 0.162 | 0/40 |
| banzhaf | 0.195 | 14/40 |
| loo | 0.373 | 34/40 |
| beta_4_1 | 0.653 | 7/40 |
| beta_16_1 | 0.685 | 14/40 |
| beta_1_4 | -0.005 | 21/40 |
| beta_1_16 | 0.169 | 34/40 |

TMC at 12 permutations (3n): sign flips in 7, 6, 6, 3 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0091.

## Receiver QE HSE06, fixed trust (w(N) = +0.1644)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| MACE-MP-0 relaxation | +0.1673 | +0.1303 | +0.1052 | +0.2578 | +0.3434 | +0.1082 | +0.1030 |
| NEP89 MD | -0.2092 | -0.2371 | -0.1781 | -0.1904 | -0.1446 | -0.2037 | -0.1867 |
| MEAM MD | -0.0845 | -0.0881 | -0.0085 | -0.1279 | -0.1333 | -0.0363 | -0.0155 |
| MP archive | +0.1199 | +0.1072 | +0.1224 | +0.1380 | +0.1667 | +0.1140 | +0.1185 |
| QE PBE | +0.1709 | +0.1315 | +0.1193 | +0.2574 | +0.3441 | +0.1178 | +0.1161 |

| Estimator | mean pairwise Spearman (780 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 0.982 | 0/40 |
| banzhaf | 0.962 | 0/40 |
| loo | 0.902 | 7/40 |
| beta_4_1 | 0.953 | 5/40 |
| beta_16_1 | 0.919 | 11/40 |
| beta_1_4 | 0.896 | 0/40 |
| beta_1_16 | 0.914 | 2/40 |

QE PBE and MACE-MP-0 relaxation: LOO +0.1193, +0.1052; second of the pair alone +0.0171; with other donors mean +0.0941 (range +0.0080 to +0.1685).

TMC at 15 permutations (3n): sign flips in 0, 0, 0, 0 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0483.

## Receiver QE HSE06, learned trust (w(N) = +0.2573)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| MACE-MP-0 relaxation | +0.1012 | +0.0690 | +0.0248 | +0.1906 | +0.2671 | +0.0382 | +0.0272 |
| NEP89 MD | -0.0509 | -0.0842 | -0.0911 | +0.0149 | +0.0840 | -0.0894 | -0.0908 |
| MEAM MD | -0.0021 | +0.0013 | +0.0403 | -0.0353 | -0.0487 | +0.0289 | +0.0385 |
| MP archive | +0.0644 | +0.0343 | -0.0058 | +0.1421 | +0.2151 | +0.0116 | +0.0001 |
| QE PBE | +0.1447 | +0.1175 | +0.0090 | +0.2588 | +0.3451 | +0.0530 | +0.0224 |

| Estimator | mean pairwise Spearman (780 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 0.840 | 0/40 |
| banzhaf | 0.871 | 17/40 |
| loo | 0.281 | 37/40 |
| beta_4_1 | 0.898 | 12/40 |
| beta_16_1 | 0.897 | 22/40 |
| beta_1_4 | 0.475 | 29/40 |
| beta_1_16 | 0.276 | 37/40 |

QE PBE and MACE-MP-0 relaxation: LOO +0.0090, +0.0248; second of the pair alone +0.0100; with other donors mean +0.0183 (range -0.0013 to +0.0402).

TMC at 15 permutations (3n): sign flips in 26, 18, 23, 30 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0257.

