# Experiment 20, third part: data-valuation estimators on the higher-temperature MD games (sem)

Early recall area (share of the 10 most stable candidates found in the early quarter of the receiver's MD budget). Games: run average and 20 per-run games (k = 4, 20 runs), 64 coalitions each, every coalition run by compute/almgsi_campaign/temperature_coalitions.py. Each run draws every MD value (receiver and donors) from a normal distribution with the measured standard error of its time average (temperature_coalitions.py --resample-sem); 0 K sources are fixed. This is the run-to-run noise from MD sampling.

## Receiver MEAM MD 453 K, learned trust (w(N) = +0.0239, run s.e. 0.0152, 20 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| MEAM MD 300 K | +0.2058 | +0.1765 | +0.0392 | +0.3547 | +0.4452 | +0.0802 | +0.0463 |
| NEP89 MD 453 K | -0.0593 | -0.0619 | -0.0685 | -0.0511 | -0.0520 | -0.0669 | -0.0674 |
| MACE-MP-0 MD 453 K | -0.0155 | -0.0266 | +0.0042 | -0.0100 | +0.0036 | -0.0117 | -0.0015 |
| MACE-MP-0 relaxation | -0.0261 | -0.0434 | +0.0042 | -0.0182 | +0.0008 | -0.0200 | -0.0044 |
| QE PBE | -0.0298 | -0.0293 | -0.0019 | -0.0446 | -0.0564 | -0.0158 | -0.0066 |
| QE HSE06 | -0.0512 | -0.0703 | -0.0186 | -0.0454 | -0.0292 | -0.0426 | -0.0260 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 0.846 | 0/20 |
| banzhaf | 0.834 | 2/20 |
| loo | 0.302 | 16/20 |
| beta_4_1 | 0.817 | 6/20 |
| beta_16_1 | 0.875 | 10/20 |
| beta_1_4 | 0.768 | 6/20 |
| beta_1_16 | 0.618 | 12/20 |

QE PBE and QE HSE06: LOO -0.0019, -0.0186; second of the pair alone +0.0000; with other donors mean -0.0742 (range -0.2741 to +0.0000).

TMC at 18 permutations (3n): sign flips in 3, 5, 5, 9 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0576.

## Receiver MEAM MD 453 K, fixed trust (w(N) = +0.0732, run s.e. 0.0152, 20 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| MEAM MD 300 K | +0.2223 | +0.1792 | +0.0893 | +0.3598 | +0.4827 | +0.1225 | +0.0977 |
| NEP89 MD 453 K | -0.1057 | -0.0889 | +0.0119 | -0.2031 | -0.2480 | -0.0188 | +0.0061 |
| MACE-MP-0 MD 453 K | +0.0023 | +0.0129 | +0.0014 | -0.0086 | -0.0121 | +0.0077 | +0.0032 |
| MACE-MP-0 relaxation | +0.0027 | +0.0124 | +0.0001 | -0.0076 | -0.0088 | +0.0080 | +0.0029 |
| QE PBE | -0.0005 | +0.0122 | +0.0071 | -0.0209 | -0.0301 | +0.0126 | +0.0094 |
| QE HSE06 | -0.0478 | -0.0377 | -0.0065 | -0.0850 | -0.1014 | -0.0163 | -0.0088 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 0.905 | 0/20 |
| banzhaf | 0.880 | 11/20 |
| loo | 0.701 | 20/20 |
| beta_4_1 | 0.970 | 6/20 |
| beta_16_1 | 0.970 | 7/20 |
| beta_1_4 | 0.888 | 11/20 |
| beta_1_16 | 0.755 | 19/20 |

QE PBE and QE HSE06: LOO +0.0071, -0.0065; second of the pair alone -0.0458; with other donors mean -0.0249 (range -0.1203 to +0.0720).

TMC at 18 permutations (3n): sign flips in 43, 41, 42, 36 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0029.

## Receiver MEAM MD 803 K, learned trust (w(N) = +0.0442, run s.e. 0.0206, 20 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| MEAM MD 300 K | +0.2339 | +0.2130 | +0.0744 | +0.3625 | +0.4519 | +0.1244 | +0.0862 |
| NEP89 MD 803 K | -0.0933 | -0.0954 | -0.1341 | -0.0554 | -0.0330 | -0.1274 | -0.1366 |
| MACE-MP-0 MD 803 K | -0.0126 | -0.0130 | +0.0056 | -0.0174 | -0.0138 | -0.0056 | +0.0000 |
| MACE-MP-0 relaxation | -0.0091 | -0.0142 | +0.0036 | -0.0007 | +0.0145 | -0.0107 | -0.0046 |
| QE PBE | -0.0319 | -0.0289 | -0.0241 | -0.0335 | -0.0334 | -0.0307 | -0.0288 |
| QE HSE06 | -0.0428 | -0.0678 | -0.0087 | -0.0176 | +0.0222 | -0.0455 | -0.0257 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 0.852 | 0/20 |
| banzhaf | 0.885 | 7/20 |
| loo | 0.637 | 15/20 |
| beta_4_1 | 0.652 | 11/20 |
| beta_16_1 | 0.620 | 16/20 |
| beta_1_4 | 0.848 | 10/20 |
| beta_1_16 | 0.724 | 13/20 |

QE PBE and QE HSE06: LOO -0.0241, -0.0087; second of the pair alone -0.0329; with other donors mean -0.0618 (range -0.1769 to +0.0000).

TMC at 18 permutations (3n): sign flips in 10, 23, 13, 23 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0688.

## Receiver MEAM MD 803 K, fixed trust (w(N) = +0.1896, run s.e. 0.0175, 20 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| MEAM MD 300 K | +0.2193 | +0.1747 | +0.0600 | +0.3760 | +0.5126 | +0.1026 | +0.0709 |
| NEP89 MD 803 K | -0.0921 | -0.0765 | +0.0204 | -0.1857 | -0.2220 | -0.0070 | +0.0162 |
| MACE-MP-0 MD 803 K | +0.0309 | +0.0333 | -0.0025 | +0.0507 | +0.0715 | +0.0126 | +0.0017 |
| MACE-MP-0 relaxation | +0.0418 | +0.0397 | -0.0033 | +0.0730 | +0.1070 | +0.0162 | +0.0027 |
| QE PBE | +0.0139 | +0.0195 | -0.0023 | +0.0195 | +0.0304 | +0.0072 | +0.0002 |
| QE HSE06 | -0.0242 | -0.0265 | -0.0101 | -0.0276 | -0.0129 | -0.0158 | -0.0119 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 0.971 | 0/20 |
| banzhaf | 0.953 | 4/20 |
| loo | 0.607 | 20/20 |
| beta_4_1 | 0.977 | 6/20 |
| beta_16_1 | 0.989 | 11/20 |
| beta_1_4 | 0.754 | 12/20 |
| beta_1_16 | 0.662 | 19/20 |

QE PBE and QE HSE06: LOO -0.0023, -0.0101; second of the pair alone -0.0177; with other donors mean -0.0266 (range -0.1191 to +0.0738).

TMC at 18 permutations (3n): sign flips in 22, 16, 17, 11 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0031.

## Receiver NEP89 MD 453 K, learned trust (w(N) = +0.2796, run s.e. 0.0265, 20 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| NEP89 MD 300 K | +0.2164 | +0.1829 | +0.0389 | +0.3653 | +0.4778 | +0.0958 | +0.0554 |
| MEAM MD 453 K | -0.0514 | -0.0826 | -0.0045 | -0.0410 | -0.0011 | -0.0365 | -0.0138 |
| MACE-MP-0 MD 453 K | +0.0087 | -0.0154 | -0.0214 | +0.0531 | +0.1068 | -0.0155 | -0.0180 |
| MACE-MP-0 relaxation | +0.0199 | -0.0012 | -0.0128 | +0.0651 | +0.1152 | -0.0071 | -0.0107 |
| QE PBE | +0.0508 | +0.0279 | -0.0122 | +0.1084 | +0.1691 | +0.0121 | -0.0013 |
| QE HSE06 | +0.0353 | +0.0123 | -0.0164 | +0.0805 | +0.1355 | +0.0082 | -0.0030 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 0.932 | 0/20 |
| banzhaf | 0.945 | 12/20 |
| loo | 0.419 | 20/20 |
| beta_4_1 | 0.908 | 8/20 |
| beta_16_1 | 0.855 | 13/20 |
| beta_1_4 | 0.893 | 15/20 |
| beta_1_16 | 0.601 | 18/20 |

QE PBE and QE HSE06: LOO -0.0122, -0.0164; second of the pair alone +0.0023; with other donors mean +0.0191 (range -0.0663 to +0.1696).

TMC at 18 permutations (3n): sign flips in 27, 25, 23, 10 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0035.

## Receiver NEP89 MD 453 K, fixed trust (w(N) = +0.1534, run s.e. 0.0247, 20 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| NEP89 MD 300 K | +0.3065 | +0.2404 | +0.2127 | +0.4499 | +0.5730 | +0.2137 | +0.2097 |
| MEAM MD 453 K | -0.1551 | -0.1726 | -0.0099 | -0.2310 | -0.2374 | -0.0647 | -0.0221 |
| MACE-MP-0 MD 453 K | +0.0012 | -0.0249 | +0.0044 | +0.0257 | +0.0684 | -0.0027 | +0.0042 |
| MACE-MP-0 relaxation | +0.0020 | -0.0232 | +0.0002 | +0.0280 | +0.0694 | -0.0044 | +0.0007 |
| QE PBE | +0.0079 | -0.0259 | -0.0031 | +0.0495 | +0.1065 | -0.0074 | -0.0022 |
| QE HSE06 | -0.0090 | -0.0317 | -0.0044 | +0.0067 | +0.0429 | -0.0072 | -0.0019 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 0.910 | 0/20 |
| banzhaf | 0.868 | 15/20 |
| loo | 0.769 | 15/20 |
| beta_4_1 | 0.944 | 7/20 |
| beta_16_1 | 0.935 | 9/20 |
| beta_1_4 | 0.726 | 13/20 |
| beta_1_16 | 0.710 | 18/20 |

QE PBE and QE HSE06: LOO -0.0031, -0.0044; second of the pair alone -0.0302; with other donors mean -0.0102 (range -0.2992 to +0.0635).

TMC at 18 permutations (3n): sign flips in 44, 45, 43, 46 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0464.

## Receiver NEP89 MD 803 K, learned trust (w(N) = +0.1687, run s.e. 0.0308, 20 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| NEP89 MD 300 K | +0.1343 | +0.0876 | +0.0016 | +0.2499 | +0.3645 | +0.0549 | +0.0265 |
| MEAM MD 803 K | -0.0653 | -0.0954 | -0.0076 | -0.0738 | -0.0434 | -0.0339 | -0.0107 |
| MACE-MP-0 MD 803 K | +0.0295 | +0.0061 | -0.0047 | +0.0632 | +0.1136 | +0.0141 | +0.0076 |
| MACE-MP-0 relaxation | +0.0179 | -0.0151 | -0.0074 | +0.0625 | +0.1257 | -0.0005 | -0.0005 |
| QE PBE | +0.0299 | +0.0004 | +0.0024 | +0.0707 | +0.1287 | +0.0124 | +0.0106 |
| QE HSE06 | +0.0225 | -0.0049 | +0.0132 | +0.0495 | +0.0987 | +0.0170 | +0.0197 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 0.760 | 0/20 |
| banzhaf | 0.820 | 17/20 |
| loo | 0.040 | 20/20 |
| beta_4_1 | 0.718 | 3/20 |
| beta_16_1 | 0.706 | 9/20 |
| beta_1_4 | 0.650 | 13/20 |
| beta_1_16 | 0.139 | 18/20 |

QE PBE and QE HSE06: LOO +0.0024, +0.0132; second of the pair alone +0.0044; with other donors mean +0.0086 (range -0.0776 to +0.1422).

TMC at 18 permutations (3n): sign flips in 20, 16, 20, 18 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0468.

## Receiver NEP89 MD 803 K, fixed trust (w(N) = +0.1162, run s.e. 0.0269, 20 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| NEP89 MD 300 K | +0.2835 | +0.2285 | +0.1856 | +0.4157 | +0.5219 | +0.1932 | +0.1845 |
| MEAM MD 803 K | -0.1492 | -0.1677 | -0.0206 | -0.2126 | -0.2111 | -0.0702 | -0.0320 |
| MACE-MP-0 MD 803 K | -0.0148 | -0.0313 | +0.0044 | -0.0133 | +0.0075 | -0.0039 | +0.0042 |
| MACE-MP-0 relaxation | +0.0001 | -0.0189 | +0.0077 | +0.0122 | +0.0410 | +0.0026 | +0.0083 |
| QE PBE | +0.0084 | -0.0200 | +0.0154 | +0.0325 | +0.0754 | +0.0062 | +0.0147 |
| QE HSE06 | -0.0118 | -0.0285 | +0.0092 | -0.0122 | +0.0089 | +0.0012 | +0.0096 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 0.977 | 0/20 |
| banzhaf | 0.934 | 11/20 |
| loo | 0.628 | 12/20 |
| beta_4_1 | 0.973 | 4/20 |
| beta_16_1 | 0.973 | 8/20 |
| beta_1_4 | 0.887 | 10/20 |
| beta_1_16 | 0.680 | 11/20 |

QE PBE and QE HSE06: LOO +0.0154, +0.0092; second of the pair alone -0.0314; with other donors mean -0.0038 (range -0.2985 to +0.0786).

TMC at 18 permutations (3n): sign flips in 42, 38, 36, 42 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0386.

## Receiver MACE-MP-0 MD 453 K, learned trust (w(N) = +0.3062, run s.e. 0.0176, 20 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| MACE-MP-0 MD 300 K | +0.1468 | +0.1077 | +0.0219 | +0.2677 | +0.3794 | +0.0595 | +0.0341 |
| MEAM MD 453 K | -0.0195 | -0.0418 | -0.0198 | +0.0005 | +0.0478 | -0.0200 | -0.0165 |
| NEP89 MD 453 K | +0.0100 | -0.0022 | -0.0640 | +0.0632 | +0.1179 | -0.0310 | -0.0514 |
| MACE-MP-0 relaxation | +0.1198 | +0.0839 | +0.0197 | +0.2231 | +0.3210 | +0.0473 | +0.0284 |
| QE PBE | +0.0360 | -0.0032 | -0.0247 | +0.1175 | +0.2143 | -0.0112 | -0.0190 |
| QE HSE06 | +0.0132 | -0.0081 | -0.0351 | +0.0619 | +0.1207 | -0.0168 | -0.0268 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 0.897 | 0/20 |
| banzhaf | 0.820 | 17/20 |
| loo | 0.534 | 20/20 |
| beta_4_1 | 0.944 | 12/20 |
| beta_16_1 | 0.936 | 17/20 |
| beta_1_4 | 0.634 | 20/20 |
| beta_1_16 | 0.595 | 20/20 |

QE PBE and QE HSE06: LOO -0.0247, -0.0351; second of the pair alone -0.0287; with other donors mean +0.0146 (range -0.0981 to +0.1659).

MACE-MP-0 relaxation and MACE-MP-0 MD 300 K: LOO +0.0197, +0.0219; second of the pair alone +0.0422; with other donors mean +0.0787 (range -0.0029 to +0.1654).

TMC at 18 permutations (3n): sign flips in 34, 31, 25, 35 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0086.

## Receiver MACE-MP-0 MD 453 K, fixed trust (w(N) = +0.4737, run s.e. 0.0167, 20 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| MACE-MP-0 MD 300 K | +0.1807 | +0.1299 | +0.0631 | +0.3213 | +0.4644 | +0.0867 | +0.0687 |
| MEAM MD 453 K | -0.0651 | -0.0737 | -0.0340 | -0.0746 | -0.0406 | -0.0427 | -0.0340 |
| NEP89 MD 453 K | +0.0615 | +0.0612 | +0.1276 | +0.0190 | +0.0379 | +0.1118 | +0.1264 |
| MACE-MP-0 relaxation | +0.1575 | +0.1164 | +0.0390 | +0.2857 | +0.4128 | +0.0680 | +0.0466 |
| QE PBE | +0.0699 | +0.0438 | -0.0260 | +0.1638 | +0.2579 | +0.0022 | -0.0177 |
| QE HSE06 | +0.0694 | +0.0462 | -0.0274 | +0.1596 | +0.2503 | +0.0033 | -0.0180 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 0.884 | 0/20 |
| banzhaf | 0.899 | 0/20 |
| loo | 0.882 | 20/20 |
| beta_4_1 | 0.970 | 6/20 |
| beta_16_1 | 0.970 | 10/20 |
| beta_1_4 | 0.953 | 14/20 |
| beta_1_16 | 0.958 | 20/20 |

QE PBE and QE HSE06: LOO -0.0260, -0.0274; second of the pair alone +0.0197; with other donors mean +0.0156 (range -0.0440 to +0.1379).

MACE-MP-0 relaxation and MACE-MP-0 MD 300 K: LOO +0.0390, +0.0631; second of the pair alone +0.0376; with other donors mean +0.0864 (range +0.0230 to +0.2479).

TMC at 18 permutations (3n): sign flips in 2, 3, 4, 13 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0098.

## Receiver MACE-MP-0 MD 803 K, learned trust (w(N) = +0.3357, run s.e. 0.0164, 20 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| MACE-MP-0 MD 300 K | +0.1365 | +0.0928 | +0.0244 | +0.2503 | +0.3568 | +0.0579 | +0.0375 |
| MEAM MD 803 K | -0.0891 | -0.1214 | -0.0192 | -0.0993 | -0.0630 | -0.0529 | -0.0256 |
| NEP89 MD 803 K | +0.0840 | +0.0642 | +0.0766 | +0.0912 | +0.1259 | +0.0914 | +0.0902 |
| MACE-MP-0 relaxation | +0.1208 | +0.0790 | +0.0103 | +0.2316 | +0.3368 | +0.0441 | +0.0235 |
| QE PBE | +0.0418 | +0.0055 | -0.0384 | +0.1270 | +0.2166 | -0.0132 | -0.0274 |
| QE HSE06 | +0.0417 | +0.0302 | -0.0205 | +0.0853 | +0.1241 | +0.0073 | -0.0088 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 0.902 | 0/20 |
| banzhaf | 0.888 | 7/20 |
| loo | 0.609 | 19/20 |
| beta_4_1 | 0.945 | 2/20 |
| beta_16_1 | 0.936 | 6/20 |
| beta_1_4 | 0.921 | 15/20 |
| beta_1_16 | 0.789 | 18/20 |

QE PBE and QE HSE06: LOO -0.0384, -0.0205; second of the pair alone +0.0202; with other donors mean +0.0243 (range -0.0404 to +0.1936).

MACE-MP-0 relaxation and MACE-MP-0 MD 300 K: LOO +0.0103, +0.0244; second of the pair alone +0.0123; with other donors mean +0.0588 (range -0.0351 to +0.1713).

TMC at 18 permutations (3n): sign flips in 5, 3, 4, 0 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0215.

## Receiver MACE-MP-0 MD 803 K, fixed trust (w(N) = +0.3523, run s.e. 0.0222, 20 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| MACE-MP-0 MD 300 K | +0.1650 | +0.1193 | +0.0704 | +0.2799 | +0.4014 | +0.0909 | +0.0769 |
| MEAM MD 803 K | -0.1149 | -0.1155 | -0.0472 | -0.1618 | -0.1562 | -0.0629 | -0.0475 |
| NEP89 MD 803 K | +0.0196 | +0.0159 | +0.0771 | -0.0142 | -0.0005 | +0.0612 | +0.0754 |
| MACE-MP-0 relaxation | +0.1326 | +0.0969 | +0.0481 | +0.2308 | +0.3327 | +0.0672 | +0.0534 |
| QE PBE | +0.0710 | +0.0457 | -0.0068 | +0.1506 | +0.2325 | +0.0156 | +0.0003 |
| QE HSE06 | +0.0790 | +0.0561 | -0.0108 | +0.1618 | +0.2441 | +0.0187 | -0.0011 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 0.973 | 0/20 |
| banzhaf | 0.927 | 1/20 |
| loo | 0.915 | 19/20 |
| beta_4_1 | 0.973 | 9/20 |
| beta_16_1 | 0.973 | 10/20 |
| beta_1_4 | 0.886 | 6/20 |
| beta_1_16 | 0.901 | 17/20 |

QE PBE and QE HSE06: LOO -0.0068, -0.0108; second of the pair alone +0.0181; with other donors mean +0.0326 (range -0.0174 to +0.1566).

MACE-MP-0 relaxation and MACE-MP-0 MD 300 K: LOO +0.0481, +0.0704; second of the pair alone +0.0473; with other donors mean +0.0886 (range +0.0248 to +0.1557).

TMC at 18 permutations (3n): sign flips in 13, 10, 8, 8 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0216.

## Summary over the 12 games

Mean pairwise Spearman over all 12 games: shapley 0.901, banzhaf 0.888, loo 0.587, beta_4_1 0.899, beta_16_1 0.895, beta_1_4 0.817, beta_1_16 0.678.

| Receiver | trust | w(N) | top (Shapley) | top (LOO) | bottom (Shapley) | bottom (LOO) | LOO/Shapley sign disagreements | Spearman Shapley | Spearman Banzhaf | Spearman Beta(16,1) | TMC 3n flips (tol 0) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MEAM MD 453 K | learned | +0.024 | MEAM MD 300 K | MEAM MD 300 K | NEP89 MD 453 K | NEP89 MD 453 K | 2 | 0.846 | 0.834 | 0.875 | 3/50 |
| MEAM MD 453 K | fixed | +0.073 | MEAM MD 300 K | MEAM MD 300 K | NEP89 MD 453 K | QE HSE06 | 2 | 0.905 | 0.880 | 0.970 | 43/50 |
| MEAM MD 803 K | learned | +0.044 | MEAM MD 300 K | MEAM MD 300 K | NEP89 MD 803 K | NEP89 MD 803 K | 2 | 0.852 | 0.885 | 0.620 | 10/50 |
| MEAM MD 803 K | fixed | +0.190 | MEAM MD 300 K | MEAM MD 300 K | NEP89 MD 803 K | QE HSE06 | 4 | 0.971 | 0.953 | 0.989 | 22/50 |
| NEP89 MD 453 K | learned | +0.280 | NEP89 MD 300 K | NEP89 MD 300 K | MEAM MD 453 K | MACE-MP-0 MD 453 K | 4 | 0.932 | 0.945 | 0.855 | 27/50 |
| NEP89 MD 453 K | fixed | +0.153 | NEP89 MD 300 K | NEP89 MD 300 K | MEAM MD 453 K | MEAM MD 453 K | 1 | 0.910 | 0.868 | 0.935 | 44/50 |
| NEP89 MD 803 K | learned | +0.169 | NEP89 MD 300 K | QE HSE06 | MEAM MD 803 K | MEAM MD 803 K | 2 | 0.760 | 0.820 | 0.706 | 20/50 |
| NEP89 MD 803 K | fixed | +0.116 | NEP89 MD 300 K | NEP89 MD 300 K | MEAM MD 803 K | MEAM MD 803 K | 2 | 0.977 | 0.934 | 0.973 | 42/50 |
| MACE-MP-0 MD 453 K | learned | +0.306 | MACE-MP-0 MD 300 K | MACE-MP-0 MD 300 K | MEAM MD 453 K | NEP89 MD 453 K | 3 | 0.897 | 0.820 | 0.936 | 34/50 |
| MACE-MP-0 MD 453 K | fixed | +0.474 | MACE-MP-0 MD 300 K | NEP89 MD 453 K | MEAM MD 453 K | MEAM MD 453 K | 2 | 0.884 | 0.899 | 0.970 | 2/50 |
| MACE-MP-0 MD 803 K | learned | +0.336 | MACE-MP-0 MD 300 K | NEP89 MD 803 K | MEAM MD 803 K | QE PBE | 2 | 0.902 | 0.888 | 0.936 | 5/50 |
| MACE-MP-0 MD 803 K | fixed | +0.352 | MACE-MP-0 MD 300 K | NEP89 MD 803 K | MEAM MD 803 K | MEAM MD 803 K | 2 | 0.973 | 0.927 | 0.973 | 13/50 |
