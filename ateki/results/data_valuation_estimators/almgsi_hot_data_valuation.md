# Experiment 20, third part: data-valuation estimators on the higher-temperature MD games (seeds)

Early recall area (share of the 10 most stable candidates found in the early quarter of the receiver's MD budget). Games: run average and 20 per-run games (k = 4, 20 runs), 64 coalitions each, every coalition run by compute/almgsi_campaign/temperature_coalitions.py. Runs differ only in the campaign seed, which breaks exact ties; with a donor present every run makes the same choices, so the per-run games differ only in v(empty) and the consistency columns are not a noise test.

## Receiver MEAM MD 453 K, learned trust (w(N) = +0.0231, run s.e. 0.0137, 1 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| MEAM MD 300 K | +0.1953 | +0.1745 | -0.0184 | +0.3614 | +0.4489 | +0.0451 | -0.0052 |
| NEP89 MD 453 K | -0.0509 | -0.0413 | -0.0765 | -0.0516 | -0.0657 | -0.0593 | -0.0699 |
| MACE-MP-0 MD 453 K | -0.0165 | -0.0237 | +0.0041 | -0.0070 | +0.0045 | -0.0185 | -0.0081 |
| MACE-MP-0 relaxation | -0.0321 | -0.0500 | +0.0041 | -0.0216 | -0.0011 | -0.0276 | -0.0097 |
| QE PBE | -0.0247 | -0.0207 | +0.0041 | -0.0433 | -0.0586 | -0.0093 | -0.0016 |
| QE HSE06 | -0.0479 | -0.0642 | +0.0041 | -0.0463 | -0.0377 | -0.0365 | -0.0135 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 1.000 | 0/20 |
| banzhaf | 1.000 | 1/20 |
| loo | 1.000 | 20/20 |
| beta_4_1 | 1.000 | 7/20 |
| beta_16_1 | 1.000 | 10/20 |
| beta_1_4 | 1.000 | 1/20 |
| beta_1_16 | 1.000 | 20/20 |

QE PBE and QE HSE06: LOO +0.0041, +0.0041; second of the pair alone +0.0000; with other donors mean -0.0730 (range -0.3196 to +0.0533).

TMC at 18 permutations (3n): sign flips in 7, 11, 10, 12 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0438.

## Receiver MEAM MD 453 K, fixed trust (w(N) = +0.0836, run s.e. 0.0137, 16 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| MEAM MD 300 K | +0.2248 | +0.1797 | +0.1093 | +0.3583 | +0.4804 | +0.1310 | +0.1127 |
| NEP89 MD 453 K | -0.1031 | -0.0871 | +0.0273 | -0.2049 | -0.2518 | -0.0110 | +0.0183 |
| MACE-MP-0 MD 453 K | +0.0055 | +0.0152 | +0.0129 | -0.0067 | -0.0104 | +0.0131 | +0.0118 |
| MACE-MP-0 relaxation | +0.0051 | +0.0125 | +0.0222 | -0.0098 | -0.0127 | +0.0173 | +0.0195 |
| QE PBE | -0.0021 | +0.0109 | +0.0096 | -0.0234 | -0.0339 | +0.0119 | +0.0101 |
| QE HSE06 | -0.0466 | -0.0364 | +0.0038 | -0.0868 | -0.1052 | -0.0119 | -0.0014 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 1.000 | 0/20 |
| banzhaf | 1.000 | 12/20 |
| loo | 1.000 | 20/20 |
| beta_4_1 | 1.000 | 10/20 |
| beta_16_1 | 1.000 | 11/20 |
| beta_1_4 | 1.000 | 12/20 |
| beta_1_16 | 1.000 | 20/20 |

QE PBE and QE HSE06: LOO +0.0096, +0.0038; second of the pair alone -0.0458; with other donors mean -0.0239 (range -0.1131 to +0.0748).

TMC at 18 permutations (3n): sign flips in 42, 40, 42, 34 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0024.

## Receiver MEAM MD 803 K, learned trust (w(N) = -0.0110, run s.e. 0.0160, 1 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| MEAM MD 300 K | +0.2306 | +0.2141 | +0.0574 | +0.3568 | +0.4466 | +0.1205 | +0.0757 |
| NEP89 MD 803 K | -0.1314 | -0.1158 | -0.2639 | -0.0691 | -0.0425 | -0.2029 | -0.2462 |
| MACE-MP-0 MD 803 K | +0.0081 | +0.0049 | +0.0032 | +0.0175 | +0.0373 | +0.0042 | +0.0030 |
| MACE-MP-0 relaxation | -0.0179 | -0.0343 | +0.0032 | +0.0000 | +0.0316 | -0.0200 | -0.0076 |
| QE PBE | -0.0343 | -0.0227 | -0.0209 | -0.0555 | -0.0681 | -0.0202 | -0.0207 |
| QE HSE06 | -0.0660 | -0.0913 | -0.0209 | -0.0507 | -0.0098 | -0.0580 | -0.0360 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 1.000 | 0/20 |
| banzhaf | 1.000 | 9/20 |
| loo | 1.000 | 18/20 |
| beta_4_1 | 1.000 | 12/20 |
| beta_16_1 | 1.000 | 13/20 |
| beta_1_4 | 1.000 | 9/20 |
| beta_1_16 | 1.000 | 9/20 |

QE PBE and QE HSE06: LOO -0.0209, -0.0209; second of the pair alone -0.0350; with other donors mean -0.0739 (range -0.2415 to +0.0000).

TMC at 18 permutations (3n): sign flips in 20, 28, 14, 16 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.2306.

## Receiver MEAM MD 803 K, fixed trust (w(N) = +0.1573, run s.e. 0.0160, 20 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| MEAM MD 300 K | +0.2101 | +0.1677 | +0.0441 | +0.3665 | +0.5005 | +0.0915 | +0.0570 |
| NEP89 MD 803 K | -0.0874 | -0.0647 | +0.0242 | -0.1893 | -0.2370 | +0.0003 | +0.0211 |
| MACE-MP-0 MD 803 K | +0.0351 | +0.0384 | +0.0136 | +0.0484 | +0.0630 | +0.0223 | +0.0150 |
| MACE-MP-0 relaxation | +0.0231 | +0.0249 | -0.0046 | +0.0403 | +0.0605 | +0.0079 | -0.0013 |
| QE PBE | +0.0094 | +0.0167 | +0.0055 | +0.0068 | +0.0098 | +0.0093 | +0.0056 |
| QE HSE06 | -0.0329 | -0.0297 | -0.0133 | -0.0462 | -0.0427 | -0.0191 | -0.0153 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 1.000 | 0/20 |
| banzhaf | 1.000 | 4/20 |
| loo | 1.000 | 20/20 |
| beta_4_1 | 1.000 | 7/20 |
| beta_16_1 | 1.000 | 10/20 |
| beta_1_4 | 1.000 | 17/20 |
| beta_1_16 | 1.000 | 20/20 |

QE PBE and QE HSE06: LOO +0.0055, -0.0133; second of the pair alone -0.0208; with other donors mean -0.0278 (range -0.1148 to +0.0719).

TMC at 18 permutations (3n): sign flips in 29, 19, 19, 17 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0033.

## Receiver NEP89 MD 453 K, learned trust (w(N) = +0.2998, run s.e. 0.0271, 1 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| NEP89 MD 300 K | +0.2265 | +0.1923 | +0.0084 | +0.3961 | +0.5198 | +0.0852 | +0.0326 |
| MEAM MD 453 K | -0.0439 | -0.0801 | -0.0041 | -0.0242 | +0.0260 | -0.0343 | -0.0125 |
| MACE-MP-0 MD 453 K | +0.0040 | -0.0154 | -0.0404 | +0.0450 | +0.0924 | -0.0212 | -0.0305 |
| MACE-MP-0 relaxation | +0.0298 | +0.0026 | -0.0404 | +0.0973 | +0.1653 | -0.0156 | -0.0295 |
| QE PBE | +0.0547 | +0.0334 | -0.0404 | +0.1240 | +0.1905 | +0.0027 | -0.0216 |
| QE HSE06 | +0.0287 | +0.0131 | -0.0404 | +0.0633 | +0.1096 | +0.0053 | -0.0159 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 1.000 | 0/20 |
| banzhaf | 1.000 | 19/20 |
| loo | 1.000 | 20/20 |
| beta_4_1 | 1.000 | 13/20 |
| beta_16_1 | 1.000 | 18/20 |
| beta_1_4 | 1.000 | 20/20 |
| beta_1_16 | 1.000 | 20/20 |

QE PBE and QE HSE06: LOO -0.0404, -0.0404; second of the pair alone -0.0001; with other donors mean +0.0279 (range -0.0812 to +0.1981).

TMC at 18 permutations (3n): sign flips in 30, 29, 24, 16 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0034.

## Receiver NEP89 MD 453 K, fixed trust (w(N) = +0.1475, run s.e. 0.0271, 14 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| NEP89 MD 300 K | +0.3128 | +0.2458 | +0.2115 | +0.4617 | +0.5864 | +0.2149 | +0.2092 |
| MEAM MD 453 K | -0.1486 | -0.1661 | -0.0040 | -0.2246 | -0.2325 | -0.0584 | -0.0160 |
| MACE-MP-0 MD 453 K | -0.0082 | -0.0299 | +0.0000 | +0.0073 | +0.0396 | -0.0070 | -0.0001 |
| MACE-MP-0 relaxation | -0.0006 | -0.0262 | -0.0006 | +0.0250 | +0.0649 | -0.0067 | -0.0006 |
| QE PBE | +0.0044 | -0.0309 | -0.0008 | +0.0442 | +0.1006 | -0.0083 | -0.0008 |
| QE HSE06 | -0.0122 | -0.0368 | -0.0001 | +0.0006 | +0.0365 | -0.0063 | +0.0017 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 1.000 | 0/20 |
| banzhaf | 1.000 | 12/20 |
| loo | 1.000 | 20/20 |
| beta_4_1 | 1.000 | 5/20 |
| beta_16_1 | 1.000 | 8/20 |
| beta_1_4 | 1.000 | 12/20 |
| beta_1_16 | 1.000 | 20/20 |

QE PBE and QE HSE06: LOO -0.0008, -0.0001; second of the pair alone -0.0302; with other donors mean -0.0105 (range -0.2904 to +0.0664).

TMC at 18 permutations (3n): sign flips in 46, 44, 39, 48 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0438.

## Receiver NEP89 MD 803 K, learned trust (w(N) = +0.1438, run s.e. 0.0228, 1 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| NEP89 MD 300 K | +0.0912 | +0.0441 | -0.0558 | +0.2003 | +0.3217 | +0.0183 | -0.0179 |
| MEAM MD 803 K | -0.0749 | -0.1061 | -0.0293 | -0.0810 | -0.0451 | -0.0451 | -0.0263 |
| MACE-MP-0 MD 803 K | +0.0434 | +0.0203 | -0.0261 | +0.0888 | +0.1541 | +0.0166 | -0.0026 |
| MACE-MP-0 relaxation | +0.0277 | -0.0123 | +0.0142 | +0.0647 | +0.1363 | +0.0221 | +0.0256 |
| QE PBE | +0.0405 | +0.0082 | +0.0140 | +0.0796 | +0.1425 | +0.0270 | +0.0253 |
| QE HSE06 | +0.0159 | -0.0103 | +0.0140 | +0.0385 | +0.0871 | +0.0147 | +0.0192 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 1.000 | 0/20 |
| banzhaf | 1.000 | 19/20 |
| loo | 1.000 | 20/20 |
| beta_4_1 | 1.000 | 2/20 |
| beta_16_1 | 1.000 | 10/20 |
| beta_1_4 | 1.000 | 5/20 |
| beta_1_16 | 1.000 | 20/20 |

QE PBE and QE HSE06: LOO +0.0140, +0.0140; second of the pair alone +0.0068; with other donors mean -0.0045 (range -0.1652 to +0.0813).

TMC at 18 permutations (3n): sign flips in 24, 20, 20, 22 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0219.

## Receiver NEP89 MD 803 K, fixed trust (w(N) = +0.0853, run s.e. 0.0228, 20 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| NEP89 MD 300 K | +0.2206 | +0.1637 | +0.1305 | +0.3551 | +0.4651 | +0.1303 | +0.1251 |
| MEAM MD 803 K | -0.1726 | -0.1836 | -0.0415 | -0.2467 | -0.2545 | -0.0880 | -0.0519 |
| MACE-MP-0 MD 803 K | -0.0002 | -0.0196 | +0.0319 | +0.0007 | +0.0245 | +0.0143 | +0.0275 |
| MACE-MP-0 relaxation | +0.0145 | -0.0074 | +0.0397 | +0.0249 | +0.0560 | +0.0219 | +0.0344 |
| QE PBE | +0.0233 | -0.0061 | +0.0450 | +0.0452 | +0.0894 | +0.0252 | +0.0391 |
| QE HSE06 | -0.0003 | -0.0162 | +0.0226 | +0.0003 | +0.0229 | +0.0120 | +0.0210 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 0.975 | 0/20 |
| banzhaf | 1.000 | 18/20 |
| loo | 1.000 | 9/20 |
| beta_4_1 | 1.000 | 3/20 |
| beta_16_1 | 1.000 | 2/20 |
| beta_1_4 | 1.000 | 9/20 |
| beta_1_16 | 1.000 | 9/20 |

QE PBE and QE HSE06: LOO +0.0450, +0.0226; second of the pair alone -0.0314; with other donors mean +0.0065 (range -0.2780 to +0.1068).

TMC at 18 permutations (3n): sign flips in 42, 39, 45, 41 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0616.

## Receiver MACE-MP-0 MD 453 K, learned trust (w(N) = +0.2305, run s.e. 0.0161, 1 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| MACE-MP-0 MD 300 K | +0.1304 | +0.1043 | -0.0514 | +0.2573 | +0.3618 | +0.0257 | -0.0225 |
| MEAM MD 453 K | -0.0214 | -0.0138 | -0.0964 | +0.0012 | +0.0235 | -0.0480 | -0.0764 |
| NEP89 MD 453 K | -0.0159 | -0.0151 | -0.1516 | +0.0500 | +0.1026 | -0.0801 | -0.1242 |
| MACE-MP-0 relaxation | +0.0947 | +0.0724 | -0.0688 | +0.2060 | +0.2982 | +0.0024 | -0.0417 |
| QE PBE | +0.0325 | -0.0159 | -0.0187 | +0.1255 | +0.2342 | -0.0187 | -0.0196 |
| QE HSE06 | +0.0102 | -0.0139 | -0.0289 | +0.0645 | +0.1206 | -0.0236 | -0.0278 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 1.000 | 0/20 |
| banzhaf | 1.000 | 20/20 |
| loo | 1.000 | 20/20 |
| beta_4_1 | 1.000 | 19/20 |
| beta_16_1 | 1.000 | 19/20 |
| beta_1_4 | 1.000 | 20/20 |
| beta_1_16 | 1.000 | 20/20 |

QE PBE and QE HSE06: LOO -0.0187, -0.0289; second of the pair alone +0.0093; with other donors mean +0.0060 (range -0.1169 to +0.2955).

MACE-MP-0 relaxation and MACE-MP-0 MD 300 K: LOO -0.0688, -0.0514; second of the pair alone +0.0625; with other donors mean +0.0799 (range -0.0514 to +0.1522).

TMC at 18 permutations (3n): sign flips in 33, 30, 37, 40 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0097.

## Receiver MACE-MP-0 MD 453 K, fixed trust (w(N) = +0.4725, run s.e. 0.0161, 12 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| MACE-MP-0 MD 300 K | +0.1804 | +0.1302 | +0.0625 | +0.3195 | +0.4616 | +0.0874 | +0.0688 |
| MEAM MD 453 K | -0.0570 | -0.0686 | -0.0173 | -0.0697 | -0.0317 | -0.0288 | -0.0174 |
| NEP89 MD 453 K | +0.0463 | +0.0442 | +0.1284 | -0.0031 | +0.0126 | +0.1047 | +0.1246 |
| MACE-MP-0 relaxation | +0.1566 | +0.1149 | +0.0446 | +0.2826 | +0.4088 | +0.0700 | +0.0508 |
| QE PBE | +0.0686 | +0.0426 | -0.0273 | +0.1626 | +0.2565 | +0.0007 | -0.0192 |
| QE HSE06 | +0.0776 | +0.0523 | -0.0188 | +0.1702 | +0.2643 | +0.0109 | -0.0098 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 1.000 | 0/20 |
| banzhaf | 1.000 | 0/20 |
| loo | 1.000 | 20/20 |
| beta_4_1 | 1.000 | 11/20 |
| beta_16_1 | 1.000 | 11/20 |
| beta_1_4 | 1.000 | 2/20 |
| beta_1_16 | 1.000 | 20/20 |

QE PBE and QE HSE06: LOO -0.0273, -0.0188; second of the pair alone +0.0269; with other donors mean +0.0201 (range -0.0465 to +0.1085).

MACE-MP-0 relaxation and MACE-MP-0 MD 300 K: LOO +0.0446, +0.0625; second of the pair alone +0.0364; with other donors mean +0.0853 (range +0.0186 to +0.2158).

TMC at 18 permutations (3n): sign flips in 3, 7, 8, 20 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0082.

## Receiver MACE-MP-0 MD 803 K, learned trust (w(N) = +0.3215, run s.e. 0.0197, 1 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| MACE-MP-0 MD 300 K | +0.1440 | +0.1037 | +0.0029 | +0.2734 | +0.3829 | +0.0474 | +0.0185 |
| MEAM MD 803 K | -0.0800 | -0.0911 | -0.0076 | -0.1168 | -0.1180 | -0.0345 | -0.0121 |
| NEP89 MD 803 K | +0.0655 | +0.0469 | +0.0046 | +0.1036 | +0.1481 | +0.0403 | +0.0244 |
| MACE-MP-0 relaxation | +0.1160 | +0.0696 | -0.0227 | +0.2459 | +0.3651 | +0.0236 | -0.0041 |
| QE PBE | +0.0332 | -0.0006 | -0.0745 | +0.1302 | +0.2268 | -0.0350 | -0.0584 |
| QE HSE06 | +0.0428 | +0.0296 | -0.0284 | +0.0950 | +0.1384 | +0.0011 | -0.0165 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 1.000 | 0/20 |
| banzhaf | 1.000 | 10/20 |
| loo | 1.000 | 20/20 |
| beta_4_1 | 1.000 | 1/20 |
| beta_16_1 | 1.000 | 1/20 |
| beta_1_4 | 1.000 | 20/20 |
| beta_1_16 | 1.000 | 20/20 |

QE PBE and QE HSE06: LOO -0.0745, -0.0284; second of the pair alone +0.0010; with other donors mean +0.0165 (range -0.0810 to +0.3164).

MACE-MP-0 relaxation and MACE-MP-0 MD 300 K: LOO -0.0227, +0.0029; second of the pair alone -0.0082; with other donors mean +0.0645 (range +0.0029 to +0.1564).

TMC at 18 permutations (3n): sign flips in 9, 8, 5, 3 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0126.

## Receiver MACE-MP-0 MD 803 K, fixed trust (w(N) = +0.3485, run s.e. 0.0197, 11 distinct per-run games)

| Donor | shapley | banzhaf | loo | beta_4_1 | beta_16_1 | beta_1_4 | beta_1_16 |
|---|---|---|---|---|---|---|---|
| MACE-MP-0 MD 300 K | +0.1702 | +0.1217 | +0.0811 | +0.2862 | +0.4107 | +0.0973 | +0.0859 |
| MEAM MD 803 K | -0.1296 | -0.1257 | -0.0632 | -0.1852 | -0.1875 | -0.0728 | -0.0601 |
| NEP89 MD 803 K | +0.0093 | +0.0019 | +0.0647 | -0.0166 | +0.0039 | +0.0460 | +0.0612 |
| MACE-MP-0 relaxation | +0.1372 | +0.0984 | +0.0634 | +0.2344 | +0.3382 | +0.0755 | +0.0660 |
| QE PBE | +0.0765 | +0.0486 | +0.0084 | +0.1538 | +0.2367 | +0.0253 | +0.0137 |
| QE HSE06 | +0.0849 | +0.0613 | -0.0008 | +0.1682 | +0.2509 | +0.0249 | +0.0069 |

| Estimator | mean pairwise Spearman (190 run pairs) | runs with sign flip vs own Shapley |
|---|---|---|
| shapley | 1.000 | 0/20 |
| banzhaf | 1.000 | 1/20 |
| loo | 1.000 | 20/20 |
| beta_4_1 | 1.000 | 8/20 |
| beta_16_1 | 1.000 | 4/20 |
| beta_1_4 | 1.000 | 5/20 |
| beta_1_16 | 1.000 | 5/20 |

QE PBE and QE HSE06: LOO +0.0084, -0.0008; second of the pair alone +0.0254; with other donors mean +0.0376 (range -0.0199 to +0.1763).

MACE-MP-0 relaxation and MACE-MP-0 MD 300 K: LOO +0.0634, +0.0811; second of the pair alone +0.0483; with other donors mean +0.0908 (range +0.0280 to +0.1521).

TMC at 18 permutations (3n): sign flips in 22, 15, 15, 9 of 50 repeats at tolerance 0, 0.01, 0.05, 0.25 w(N); truncation at the run noise of w(N) biases by at most 0.0148.

## Summary over the 12 games

Mean pairwise Spearman over all 12 games: shapley 0.998, banzhaf 1.000, loo 1.000, beta_4_1 1.000, beta_16_1 1.000, beta_1_4 1.000, beta_1_16 1.000.

| Receiver | trust | w(N) | top (Shapley) | top (LOO) | bottom (Shapley) | bottom (LOO) | LOO/Shapley sign disagreements | Spearman Shapley | Spearman Banzhaf | Spearman Beta(16,1) | TMC 3n flips (tol 0) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MEAM MD 453 K | learned | +0.023 | MEAM MD 300 K | MACE-MP-0 MD 453 K | NEP89 MD 453 K | NEP89 MD 453 K | 5 | 1.000 | 1.000 | 1.000 | 7/50 |
| MEAM MD 453 K | fixed | +0.084 | MEAM MD 300 K | MEAM MD 300 K | NEP89 MD 453 K | QE HSE06 | 3 | 1.000 | 1.000 | 1.000 | 42/50 |
| MEAM MD 803 K | learned | -0.011 | MEAM MD 300 K | MEAM MD 300 K | NEP89 MD 803 K | NEP89 MD 803 K | 1 | 1.000 | 1.000 | 1.000 | 20/50 |
| MEAM MD 803 K | fixed | +0.157 | MEAM MD 300 K | MEAM MD 300 K | NEP89 MD 803 K | QE HSE06 | 2 | 1.000 | 1.000 | 1.000 | 29/50 |
| NEP89 MD 453 K | learned | +0.300 | NEP89 MD 300 K | NEP89 MD 300 K | MEAM MD 453 K | MACE-MP-0 MD 453 K | 4 | 1.000 | 1.000 | 1.000 | 30/50 |
| NEP89 MD 453 K | fixed | +0.148 | NEP89 MD 300 K | NEP89 MD 300 K | MEAM MD 453 K | MEAM MD 453 K | 2 | 1.000 | 1.000 | 1.000 | 46/50 |
| NEP89 MD 803 K | learned | +0.144 | NEP89 MD 300 K | MACE-MP-0 relaxation | MEAM MD 803 K | NEP89 MD 300 K | 2 | 1.000 | 1.000 | 1.000 | 24/50 |
| NEP89 MD 803 K | fixed | +0.085 | NEP89 MD 300 K | NEP89 MD 300 K | MEAM MD 803 K | MEAM MD 803 K | 2 | 0.975 | 1.000 | 1.000 | 42/50 |
| MACE-MP-0 MD 453 K | learned | +0.231 | MACE-MP-0 MD 300 K | QE PBE | MEAM MD 453 K | NEP89 MD 453 K | 4 | 1.000 | 1.000 | 1.000 | 33/50 |
| MACE-MP-0 MD 453 K | fixed | +0.472 | MACE-MP-0 MD 300 K | NEP89 MD 453 K | MEAM MD 453 K | QE PBE | 2 | 1.000 | 1.000 | 1.000 | 3/50 |
| MACE-MP-0 MD 803 K | learned | +0.321 | MACE-MP-0 MD 300 K | NEP89 MD 803 K | MEAM MD 803 K | QE PBE | 3 | 1.000 | 1.000 | 1.000 | 9/50 |
| MACE-MP-0 MD 803 K | fixed | +0.348 | MACE-MP-0 MD 300 K | MACE-MP-0 MD 300 K | MEAM MD 803 K | MEAM MD 803 K | 1 | 1.000 | 1.000 | 1.000 | 22/50 |
