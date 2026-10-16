# Experiment 19: credit that is not shared equally

Value = early-window recall area of the ten most stable compounds; mean [5th, 95th percentile of the
matched-seed mean by bootstrap].

## Part A, receiver gpaw_r2scan (one swarm of seven)
v(empty) +0.111 [+0.100, +0.124], v(all) +0.467 [+0.455, +0.479], best single gpumd_nep89_md +0.519 [+0.519, +0.519]

| body | compute (s) | solo gain | equal (Shapley) | by compute spent | by inverse compute | by solo gain | by seniority (tiers) | proportional to solo gain |
|---|---|---|---|---|---|---|---|---|
| MACE-MP-0 relaxation | 166 | +0.336 [+0.324, +0.348] | +0.147 [+0.142, +0.152] | +0.075 [+0.067, +0.084] | +0.156 [+0.154, +0.159] | +0.126 [+0.117, +0.135] | +0.105 [+0.091, +0.119] | +0.084 [+0.080, +0.088] |
| NEP89 MD | 1027 | +0.407 [+0.395, +0.419] | +0.084 [+0.082, +0.086] | -0.000 [-0.003, +0.002] | +0.299 [+0.290, +0.307] | +0.025 [+0.022, +0.027] | +0.080 [+0.070, +0.090] | +0.102 [+0.098, +0.106] |
| NEP89 relaxation | 282 | +0.186 [+0.173, +0.197] | +0.034 [+0.031, +0.036] | -0.005 [-0.012, +0.001] | -0.024 [-0.027, -0.022] | +0.052 [+0.045, +0.060] | +0.039 [+0.025, +0.054] | +0.046 [+0.043, +0.049] |
| MEAM MD | 200 | -0.066 [-0.079, -0.055] | -0.055 [-0.059, -0.051] | -0.064 [-0.072, -0.057] | -0.115 [-0.119, -0.112] | -0.019 [-0.029, -0.010] | -0.032 [-0.046, -0.019] | +0.001 [+0.001, +0.002] |
| MP archive | 1 | +0.350 [+0.338, +0.362] | +0.125 [+0.121, +0.129] | +0.312 [+0.302, +0.322] | +0.028 [+0.021, +0.035] | +0.103 [+0.095, +0.112] | +0.082 [+0.068, +0.095] | +0.088 [+0.084, +0.091] |
| Active learner | 1 | +0.080 [+0.055, +0.104] | +0.021 [+0.015, +0.027] | +0.045 [+0.033, +0.057] | +0.004 [-0.001, +0.010] | +0.032 [+0.020, +0.044] | +0.082 [+0.064, +0.099] | +0.025 [+0.021, +0.030] |
| Random scout | 1 | -0.002 [-0.020, +0.017] | -0.000 [-0.006, +0.006] | -0.007 [-0.018, +0.005] | +0.008 [+0.001, +0.014] | +0.037 [+0.024, +0.050] | +0.000 [-0.019, +0.019] | +0.010 [+0.007, +0.012] |

Rank (first to last): equal: MACE-MP-0 relaxation > MP archive > NEP89 MD > NEP89 relaxation > Active learner > Random scout > MEAM MD; compute: MP archive > MACE-MP-0 relaxation > Active learner > NEP89 MD > NEP89 relaxation > Random scout > MEAM MD; inv_compute: NEP89 MD > MACE-MP-0 relaxation > MP archive > Random scout > Active learner > NEP89 relaxation > MEAM MD; solo: MACE-MP-0 relaxation > MP archive > NEP89 relaxation > Random scout > Active learner > NEP89 MD > MEAM MD; seniority: MACE-MP-0 relaxation > Active learner > MP archive > NEP89 MD > NEP89 relaxation > Random scout > MEAM MD; proportional: NEP89 MD > MP archive > MACE-MP-0 relaxation > NEP89 relaxation > Active learner > Random scout > MEAM MD

Joint gains and joint losses (positive and negative dividends) received per rule:

| body | equal (Shapley) gains / losses | by compute spent gains / losses | by inverse compute gains / losses | by solo gain gains / losses | by seniority (tiers) gains / losses |
|---|---|---|---|---|---|
| MACE-MP-0 relaxation | +1.455 / -1.308 | +1.560 / -1.485 | +0.590 / -0.434 | +2.253 / -2.127 | +3.499 / -3.394 |
| NEP89 MD | +1.403 / -1.319 | +3.156 / -3.156 | +0.449 / -0.150 | +2.118 / -2.094 | +0.812 / -0.732 |
| NEP89 relaxation | +1.237 / -1.203 | +1.708 / -1.714 | +0.380 / -0.404 | +1.290 / -1.238 | +0.528 / -0.489 |
| MEAM MD | +1.153 / -1.208 | +1.697 / -1.761 | +0.176 / -0.291 | +0.139 / -0.158 | +0.514 / -0.546 |
| MP archive | +1.380 / -1.255 | +0.358 / -0.046 | +2.735 / -2.707 | +2.024 / -1.920 | +3.141 / -3.059 |
| Active learner | +1.026 / -1.005 | +0.090 / -0.045 | +2.215 / -2.210 | +0.641 / -0.609 | +0.082 / +0.000 |
| Random scout | +0.923 / -0.923 | +0.010 / -0.016 | +2.033 / -2.026 | +0.114 / -0.077 | +0.002 / -0.002 |

Largest joint dividends: MP archive+NEP89 MD+NEP89 relaxation+MACE-MP-0 relaxation -0.412; MP archive+NEP89 MD -0.397; MP archive+NEP89 MD+MACE-MP-0 relaxation +0.387; NEP89 MD+NEP89 relaxation -0.367; MP archive+MACE-MP-0 relaxation -0.351; Random scout+MEAM MD+MACE-MP-0 relaxation+Active learner +0.347
Efficiency gaps: equal 1.1e-14, compute 1.1e-14, inv_compute 1.1e-14, solo 1.1e-14, seniority 1.1e-14, proportional 1.1e-16

## Part A, receiver qe_hse06 (one swarm of seven)
v(empty) +0.123 [+0.108, +0.139], v(all) +0.507 [+0.492, +0.522], best single mace_relax +0.727 [+0.727, +0.727]

| body | compute (s) | solo gain | equal (Shapley) | by compute spent | by inverse compute | by solo gain | by seniority (tiers) | proportional to solo gain |
|---|---|---|---|---|---|---|---|---|
| MACE-MP-0 relaxation | 166 | +0.604 [+0.588, +0.619] | +0.199 [+0.193, +0.204] | +0.117 [+0.108, +0.124] | +0.239 [+0.231, +0.246] | +0.118 [+0.108, +0.128] | +0.092 [+0.077, +0.106] | +0.114 [+0.108, +0.120] |
| NEP89 MD | 1027 | +0.457 [+0.441, +0.472] | +0.055 [+0.053, +0.058] | -0.015 [-0.020, -0.011] | +0.330 [+0.319, +0.340] | -0.001 [-0.005, +0.002] | -0.007 [-0.018, +0.005] | +0.087 [+0.082, +0.091] |
| NEP89 relaxation | 282 | +0.057 [+0.041, +0.073] | +0.001 [-0.002, +0.004] | +0.007 [+0.001, +0.013] | -0.040 [-0.050, -0.029] | +0.075 [+0.065, +0.086] | +0.056 [+0.044, +0.069] | +0.014 [+0.012, +0.016] |
| MEAM MD | 200 | +0.185 [+0.169, +0.200] | -0.033 [-0.038, -0.029] | -0.073 [-0.082, -0.064] | -0.238 [-0.245, -0.231] | +0.029 [+0.021, +0.037] | +0.006 [-0.008, +0.021] | +0.036 [+0.033, +0.039] |
| MP archive | 1 | +0.472 [+0.457, +0.488] | +0.165 [+0.160, +0.170] | +0.326 [+0.315, +0.338] | +0.084 [+0.075, +0.093] | +0.114 [+0.106, +0.123] | +0.080 [+0.064, +0.095] | +0.090 [+0.085, +0.094] |
| Active learner | 1 | +0.158 [+0.126, +0.190] | +0.004 [-0.003, +0.011] | +0.053 [+0.039, +0.066] | -0.001 [-0.010, +0.008] | +0.041 [+0.032, +0.049] | +0.157 [+0.135, +0.179] | +0.034 [+0.029, +0.039] |
| Random scout | 1 | +0.001 [-0.018, +0.020] | -0.008 [-0.017, +0.000] | -0.031 [-0.042, -0.020] | +0.010 [-0.002, +0.021] | +0.007 [-0.009, +0.024] | -0.001 [-0.020, +0.017] | +0.009 [+0.007, +0.011] |

Rank (first to last): equal: MACE-MP-0 relaxation > MP archive > NEP89 MD > Active learner > NEP89 relaxation > Random scout > MEAM MD; compute: MP archive > MACE-MP-0 relaxation > Active learner > NEP89 relaxation > NEP89 MD > Random scout > MEAM MD; inv_compute: NEP89 MD > MACE-MP-0 relaxation > MP archive > Random scout > Active learner > NEP89 relaxation > MEAM MD; solo: MACE-MP-0 relaxation > MP archive > NEP89 relaxation > Active learner > MEAM MD > Random scout > NEP89 MD; seniority: Active learner > MACE-MP-0 relaxation > MP archive > NEP89 relaxation > MEAM MD > Random scout > NEP89 MD; proportional: MACE-MP-0 relaxation > MP archive > NEP89 MD > MEAM MD > Active learner > NEP89 relaxation > Random scout

Joint gains and joint losses (positive and negative dividends) received per rule:

| body | equal (Shapley) gains / losses | by compute spent gains / losses | by inverse compute gains / losses | by solo gain gains / losses | by seniority (tiers) gains / losses |
|---|---|---|---|---|---|
| MACE-MP-0 relaxation | +2.783 / -2.584 | +2.546 / -2.429 | +1.475 / -1.236 | +4.457 / -4.339 | +6.524 / -6.433 |
| NEP89 MD | +2.688 / -2.632 | +6.476 / -6.491 | +0.603 / -0.273 | +3.734 / -3.735 | +1.297 / -1.303 |
| NEP89 relaxation | +1.688 / -1.687 | +2.069 / -2.062 | +0.534 / -0.574 | +0.454 / -0.379 | +0.476 / -0.420 |
| MEAM MD | +1.896 / -1.930 | +1.823 / -1.896 | +0.770 / -1.008 | +1.335 / -1.305 | +0.784 / -0.778 |
| MP archive | +2.040 / -1.875 | +0.493 / -0.166 | +4.340 / -4.256 | +2.665 / -2.551 | +4.359 / -4.280 |
| Active learner | +1.431 / -1.427 | +0.176 / -0.124 | +3.280 / -3.281 | +0.900 / -0.860 | +0.158 / -0.002 |
| Random scout | +1.073 / -1.081 | +0.017 / -0.048 | +2.598 / -2.588 | +0.055 / -0.047 | +0.001 / -0.002 |

Largest joint dividends: NEP89 MD+NEP89 relaxation+MACE-MP-0 relaxation +0.666; NEP89 MD+MEAM MD -0.607; NEP89 MD+NEP89 relaxation+MEAM MD+MACE-MP-0 relaxation -0.602; MP archive+NEP89 MD+NEP89 relaxation+MACE-MP-0 relaxation -0.578; MP archive+MACE-MP-0 relaxation -0.547; NEP89 MD+MEAM MD+MACE-MP-0 relaxation +0.546
Efficiency gaps: equal 1.1e-14, compute 1.3e-14, inv_compute 1.2e-14, solo 1.1e-14, seniority 1.2e-14, proportional 1.1e-16

## Part A, receiver qe_pbe (one swarm of seven)
v(empty) +0.123 [+0.109, +0.136], v(all) +0.692 [+0.682, +0.701], best single mace_relax +0.808 [+0.808, +0.808]

| body | compute (s) | solo gain | equal (Shapley) | by compute spent | by inverse compute | by solo gain | by seniority (tiers) | proportional to solo gain |
|---|---|---|---|---|---|---|---|---|
| MACE-MP-0 relaxation | 166 | +0.685 [+0.672, +0.699] | +0.213 [+0.209, +0.217] | +0.089 [+0.083, +0.096] | +0.210 [+0.205, +0.213] | +0.161 [+0.155, +0.169] | +0.122 [+0.109, +0.136] | +0.139 [+0.135, +0.142] |
| NEP89 MD | 1027 | +0.497 [+0.484, +0.511] | +0.085 [+0.082, +0.087] | -0.005 [-0.009, -0.002] | +0.348 [+0.339, +0.358] | +0.069 [+0.066, +0.073] | +0.088 [+0.079, +0.097] | +0.101 [+0.098, +0.104] |
| NEP89 relaxation | 282 | +0.366 [+0.352, +0.380] | +0.071 [+0.068, +0.074] | +0.015 [+0.009, +0.020] | +0.041 [+0.039, +0.044] | +0.104 [+0.099, +0.109] | +0.069 [+0.054, +0.084] | +0.074 [+0.071, +0.077] |
| MEAM MD | 200 | +0.288 [+0.275, +0.302] | +0.028 [+0.025, +0.031] | -0.014 [-0.018, -0.009] | -0.044 [-0.047, -0.041] | +0.057 [+0.050, +0.064] | -0.008 [-0.021, +0.005] | +0.058 [+0.055, +0.061] |
| MP archive | 1 | +0.648 [+0.635, +0.662] | +0.176 [+0.172, +0.179] | +0.441 [+0.430, +0.452] | +0.042 [+0.036, +0.048] | +0.138 [+0.133, +0.144] | +0.098 [+0.086, +0.109] | +0.131 [+0.128, +0.134] |
| Active learner | 1 | +0.285 [+0.262, +0.308] | +0.025 [+0.019, +0.031] | +0.088 [+0.075, +0.099] | -0.016 [-0.023, -0.009] | +0.045 [+0.037, +0.053] | +0.244 [+0.227, +0.261] | +0.057 [+0.052, +0.061] |
| Random scout | 1 | -0.004 [-0.024, +0.018] | -0.028 [-0.035, -0.021] | -0.044 [-0.056, -0.033] | -0.012 [-0.020, -0.005] | -0.006 [-0.026, +0.014] | -0.044 [-0.061, -0.027] | +0.010 [+0.008, +0.012] |

Rank (first to last): equal: MACE-MP-0 relaxation > MP archive > NEP89 MD > NEP89 relaxation > MEAM MD > Active learner > Random scout; compute: MP archive > MACE-MP-0 relaxation > Active learner > NEP89 relaxation > NEP89 MD > MEAM MD > Random scout; inv_compute: NEP89 MD > MACE-MP-0 relaxation > MP archive > NEP89 relaxation > Random scout > Active learner > MEAM MD; solo: MACE-MP-0 relaxation > MP archive > NEP89 relaxation > NEP89 MD > MEAM MD > Active learner > Random scout; seniority: Active learner > MACE-MP-0 relaxation > MP archive > NEP89 MD > NEP89 relaxation > MEAM MD > Random scout; proportional: MACE-MP-0 relaxation > MP archive > NEP89 MD > NEP89 relaxation > MEAM MD > Active learner > Random scout

Joint gains and joint losses (positive and negative dividends) received per rule:

| body | equal (Shapley) gains / losses | by compute spent gains / losses | by inverse compute gains / losses | by solo gain gains / losses | by seniority (tiers) gains / losses |
|---|---|---|---|---|---|
| MACE-MP-0 relaxation | +3.025 / -2.812 | +3.145 / -3.056 | +1.252 / -1.042 | +4.032 / -3.870 | +6.308 / -6.186 |
| NEP89 MD | +3.094 / -3.009 | +7.944 / -7.949 | +0.602 / -0.254 | +3.475 / -3.406 | +1.214 / -1.126 |
| NEP89 relaxation | +2.529 / -2.458 | +3.348 / -3.333 | +0.715 / -0.674 | +2.209 / -2.105 | +0.826 / -0.757 |
| MEAM MD | +2.389 / -2.362 | +2.592 / -2.605 | +0.701 / -0.745 | +1.778 / -1.721 | +0.831 / -0.839 |
| MP archive | +3.618 / -3.442 | +0.715 / -0.274 | +7.746 / -7.705 | +4.865 / -4.726 | +8.681 / -8.583 |
| Active learner | +2.383 / -2.358 | +0.347 / -0.259 | +4.893 / -4.908 | +1.755 / -1.710 | +0.285 / -0.040 |
| Random scout | +1.108 / -1.136 | +0.055 / -0.099 | +2.237 / -2.249 | +0.032 / -0.038 | +0.000 / -0.044 |

Largest joint dividends: MP archive+MACE-MP-0 relaxation -0.725; MP archive+NEP89 MD+MACE-MP-0 relaxation +0.667; MP archive+NEP89 MD+NEP89 relaxation+MACE-MP-0 relaxation -0.666; MP archive+NEP89 MD+NEP89 relaxation +0.647; MP archive+NEP89 MD -0.644; MP archive+NEP89 relaxation+MACE-MP-0 relaxation +0.595
Efficiency gaps: equal 1.7e-14, compute 1.7e-14, inv_compute 1.8e-14, solo 1.7e-14, seniority 1.8e-14, proportional 2.2e-16

## Part B, qe_hse06|split_4_3 (move+share, learned thresholds, fixed structure)
mean shared members in the early window +1.380 [+1.198, +1.564]

| body | Shapley | h = 0.0 | h = 0.25 | h = 0.5 | h = 0.75 | h = 1.0 | h = 1 minus h = 0 |
|---|---|---|---|---|---|---|---|
| MACE-MP-0 relaxation | +0.188 [+0.183, +0.194] | +0.192 [+0.186, +0.198] | +0.190 [+0.185, +0.195] | +0.188 [+0.183, +0.193] | +0.188 [+0.182, +0.193] | +0.188 [+0.183, +0.194] | -0.003 |
| NEP89 MD | +0.056 [+0.051, +0.060] | +0.045 [+0.039, +0.051] | +0.048 [+0.042, +0.053] | +0.048 [+0.043, +0.053] | +0.046 [+0.041, +0.051] | +0.042 [+0.036, +0.048] | -0.003 |
| NEP89 relaxation | -0.009 [-0.013, -0.004] | -0.000 [-0.006, +0.006] | -0.000 [-0.006, +0.006] | -0.000 [-0.006, +0.006] | +0.001 [-0.005, +0.008] | +0.004 [-0.003, +0.011] | +0.004 |
| MEAM MD | -0.028 [-0.033, -0.023] | -0.056 [-0.062, -0.051] | -0.052 [-0.058, -0.047] | -0.053 [-0.058, -0.047] | -0.058 [-0.063, -0.052] | -0.067 [-0.073, -0.062] | -0.011 |
| MP archive | +0.186 [+0.181, +0.191] | +0.206 [+0.200, +0.213] | +0.203 [+0.197, +0.209] | +0.204 [+0.198, +0.210] | +0.209 [+0.202, +0.215] | +0.218 [+0.211, +0.225] | +0.012 |
| Active learner | -0.009 [-0.016, -0.001] | -0.008 [-0.015, -0.000] | -0.009 [-0.017, -0.001] | -0.010 [-0.018, -0.001] | -0.010 [-0.019, -0.002] | -0.013 [-0.021, -0.004] | -0.005 |
| Random scout | -0.039 [-0.046, -0.032] | -0.032 [-0.040, -0.025] | -0.033 [-0.040, -0.026] | -0.032 [-0.039, -0.025] | -0.029 [-0.037, -0.023] | -0.027 [-0.034, -0.019] | +0.006 |

Efficiency gaps: h=0.0 6.7e-15, h=0.25 2.3e-15, h=0.5 1.3e-15, h=0.75 1.6e-15, h=1.0 2.2e-15

## Part B, qe_hse06|split_2_2_3 (move+share, learned thresholds, fixed structure)
mean shared members in the early window +1.519 [+1.365, +1.675]

| body | Shapley | h = 0.0 | h = 0.25 | h = 0.5 | h = 0.75 | h = 1.0 | h = 1 minus h = 0 |
|---|---|---|---|---|---|---|---|
| MACE-MP-0 relaxation | +0.192 [+0.187, +0.197] | +0.168 [+0.163, +0.173] | +0.168 [+0.163, +0.173] | +0.168 [+0.163, +0.172] | +0.167 [+0.162, +0.172] | +0.167 [+0.161, +0.172] | -0.002 |
| NEP89 MD | +0.077 [+0.074, +0.081] | +0.093 [+0.086, +0.100] | +0.096 [+0.089, +0.102] | +0.099 [+0.092, +0.105] | +0.102 [+0.095, +0.109] | +0.106 [+0.098, +0.115] | +0.013 |
| NEP89 relaxation | +0.010 [+0.006, +0.014] | -0.013 [-0.020, -0.006] | -0.012 [-0.019, -0.006] | -0.014 [-0.021, -0.007] | -0.017 [-0.025, -0.010] | -0.022 [-0.030, -0.015] | -0.009 |
| MEAM MD | +0.033 [+0.028, +0.037] | +0.057 [+0.052, +0.062] | +0.057 [+0.051, +0.062] | +0.057 [+0.052, +0.062] | +0.059 [+0.053, +0.064] | +0.061 [+0.055, +0.066] | +0.004 |
| MP archive | +0.166 [+0.160, +0.171] | +0.139 [+0.133, +0.146] | +0.139 [+0.132, +0.145] | +0.137 [+0.131, +0.143] | +0.135 [+0.128, +0.141] | +0.131 [+0.124, +0.137] | -0.009 |
| Active learner | -0.017 [-0.023, -0.011] | -0.003 [-0.009, +0.004] | -0.003 [-0.010, +0.003] | -0.003 [-0.010, +0.003] | -0.003 [-0.009, +0.003] | -0.003 [-0.009, +0.004] | -0.000 |
| Random scout | -0.008 [-0.015, -0.002] | +0.010 [+0.002, +0.018] | +0.009 [+0.001, +0.017] | +0.009 [+0.001, +0.017] | +0.010 [+0.002, +0.019] | +0.013 [+0.004, +0.022] | +0.003 |

Efficiency gaps: h=0.0 3.8e-15, h=0.25 1.3e-15, h=0.5 1.2e-15, h=0.75 1.2e-15, h=1.0 1.2e-15

## Part B, qe_pbe|split_4_3 (move+share, learned thresholds, fixed structure)
mean shared members in the early window +1.559 [+1.365, +1.769]

| body | Shapley | h = 0.0 | h = 0.25 | h = 0.5 | h = 0.75 | h = 1.0 | h = 1 minus h = 0 |
|---|---|---|---|---|---|---|---|
| MACE-MP-0 relaxation | +0.213 [+0.209, +0.216] | +0.215 [+0.210, +0.221] | +0.213 [+0.209, +0.217] | +0.212 [+0.208, +0.216] | +0.213 [+0.209, +0.217] | +0.216 [+0.212, +0.220] | +0.001 |
| NEP89 MD | +0.085 [+0.082, +0.089] | +0.076 [+0.072, +0.079] | +0.078 [+0.075, +0.081] | +0.079 [+0.075, +0.082] | +0.078 [+0.074, +0.082] | +0.076 [+0.072, +0.081] | +0.001 |
| NEP89 relaxation | +0.058 [+0.054, +0.061] | +0.066 [+0.061, +0.071] | +0.067 [+0.062, +0.071] | +0.068 [+0.063, +0.072] | +0.068 [+0.064, +0.072] | +0.068 [+0.064, +0.073] | +0.002 |
| MEAM MD | +0.029 [+0.026, +0.032] | +0.017 [+0.013, +0.021] | +0.018 [+0.015, +0.022] | +0.018 [+0.015, +0.022] | +0.016 [+0.012, +0.020] | +0.012 [+0.008, +0.016] | -0.005 |
| MP archive | +0.178 [+0.175, +0.182] | +0.190 [+0.185, +0.195] | +0.187 [+0.182, +0.191] | +0.186 [+0.182, +0.191] | +0.188 [+0.184, +0.193] | +0.192 [+0.187, +0.197] | +0.002 |
| Active learner | +0.018 [+0.013, +0.023] | +0.019 [+0.013, +0.025] | +0.018 [+0.012, +0.025] | +0.018 [+0.012, +0.025] | +0.018 [+0.012, +0.025] | +0.018 [+0.012, +0.025] | -0.001 |
| Random scout | -0.044 [-0.050, -0.038] | -0.045 [-0.052, -0.039] | -0.044 [-0.051, -0.038] | -0.044 [-0.051, -0.038] | -0.045 [-0.051, -0.038] | -0.045 [-0.052, -0.039] | -0.000 |

Efficiency gaps: h=0.0 1.7e-14, h=0.25 5.4e-15, h=0.5 1.6e-15, h=0.75 1.4e-15, h=1.0 1.2e-15

## Part B, qe_pbe|split_2_2_3 (move+share, learned thresholds, fixed structure)
mean shared members in the early window +1.727 [+1.581, +1.876]

| body | Shapley | h = 0.0 | h = 0.25 | h = 0.5 | h = 0.75 | h = 1.0 | h = 1 minus h = 0 |
|---|---|---|---|---|---|---|---|
| MACE-MP-0 relaxation | +0.172 [+0.168, +0.175] | +0.163 [+0.159, +0.167] | +0.162 [+0.159, +0.166] | +0.162 [+0.158, +0.165] | +0.162 [+0.159, +0.166] | +0.163 [+0.159, +0.167] | -0.001 |
| NEP89 MD | +0.096 [+0.093, +0.099] | +0.106 [+0.101, +0.110] | +0.109 [+0.105, +0.113] | +0.112 [+0.108, +0.116] | +0.115 [+0.111, +0.119] | +0.118 [+0.114, +0.123] | +0.013 |
| NEP89 relaxation | +0.070 [+0.067, +0.074] | +0.072 [+0.067, +0.077] | +0.073 [+0.068, +0.078] | +0.073 [+0.068, +0.077] | +0.071 [+0.067, +0.075] | +0.068 [+0.063, +0.072] | -0.004 |
| MEAM MD | +0.064 [+0.061, +0.068] | +0.067 [+0.062, +0.072] | +0.066 [+0.062, +0.070] | +0.065 [+0.061, +0.070] | +0.066 [+0.061, +0.070] | +0.066 [+0.062, +0.071] | -0.000 |
| MP archive | +0.180 [+0.177, +0.183] | +0.168 [+0.163, +0.172] | +0.168 [+0.164, +0.172] | +0.168 [+0.165, +0.172] | +0.168 [+0.165, +0.172] | +0.168 [+0.164, +0.172] | +0.000 |
| Active learner | +0.015 [+0.011, +0.020] | +0.021 [+0.016, +0.027] | +0.019 [+0.014, +0.025] | +0.018 [+0.013, +0.023] | +0.017 [+0.012, +0.022] | +0.016 [+0.011, +0.022] | -0.005 |
| Random scout | -0.023 [-0.027, -0.018] | -0.021 [-0.028, -0.014] | -0.022 [-0.028, -0.015] | -0.022 [-0.029, -0.016] | -0.023 [-0.030, -0.016] | -0.023 [-0.030, -0.017] | -0.003 |

Efficiency gaps: h=0.0 2.2e-15, h=0.25 1.4e-15, h=0.5 7.8e-16, h=0.75 8.9e-16, h=1.0 1.0e-15

