# Experiment 15: several bodies of one kind as separate players

Computed Al-Mg-Si campaign, batches of 4, 200 matched campaigns per coalition; value = early-window recall area of the ten most stable compounds. Shapley values are exact and computed per campaign (mean, 90% bootstrap interval of the mean).

## Receiver qe_pbe

| game | v(empty) | v(all) | credit of all copies | type-level credit | |gap| between two copies | campaigns with gap > 0.01 | pair dividend | batches with different outputs |
|---|---|---|---|---|---|---|---|---|
| scouts_indep_1 | 0.129 | 0.537 | +nan | -0.097 | nan | nan | +nan | nan |
| scouts_indep_2 | 0.129 | 0.477 | -0.131 | -0.138 | 0.067 | 0.86 | +0.012 | nan |
| scouts_clone_2 | 0.129 | 0.471 | -0.136 | -0.143 | 0.000 | 0.00 | +0.004 | nan |
| scouts_indep_3 | 0.129 | 0.421 | -0.160 | -0.172 | 0.063 | 0.93 | +0.012 | nan |
| scouts_clone_3 | 0.129 | 0.417 | -0.158 | -0.174 | 0.000 | 0.00 | +0.004 | nan |
| scouts_indep_4 | 0.129 | 0.383 | -0.178 | -0.204 | 0.057 | 0.91 | +0.012 | nan |
| scouts_clone_4 | 0.129 | 0.377 | -0.173 | -0.201 | 0.000 | 0.00 | +0.004 | nan |
| mace_shared | 0.129 | 0.632 | +0.589 |  | 0.000 | 0.00 | -0.679 | 0.00 |
| mace_separate | 0.129 | 0.597 | +0.578 |  | 0.000 | 0.00 | -0.706 | 0.94 |

Shapley, scouts_indep_3: mace_relax +0.402 [+0.396, +0.408], surrogate +0.050 [+0.045, +0.056], explorer#1 -0.056 [-0.063, -0.049], explorer#2 -0.050 [-0.056, -0.044], explorer#3 -0.053 [-0.060, -0.047]

Shapley, mace_shared: surrogate +0.006 [+0.000, +0.012], explorer -0.093 [-0.100, -0.085], mace_relax#1 +0.295 [+0.291, +0.298], mace_relax#2 +0.295 [+0.291, +0.298]

Shapley, mace_separate: surrogate -0.007 [-0.014, +0.001], explorer -0.104 [-0.111, -0.097], mace_relax#1 +0.289 [+0.285, +0.293], mace_relax#2 +0.289 [+0.285, +0.293]

## Receiver qe_hse06

| game | v(empty) | v(all) | credit of all copies | type-level credit | |gap| between two copies | campaigns with gap > 0.01 | pair dividend | batches with different outputs |
|---|---|---|---|---|---|---|---|---|
| scouts_indep_1 | 0.124 | 0.397 | +nan | -0.068 | nan | nan | +nan | nan |
| scouts_indep_2 | 0.124 | 0.381 | -0.088 | -0.099 | 0.067 | 0.92 | +0.001 | nan |
| scouts_clone_2 | 0.124 | 0.394 | -0.073 | -0.085 | 0.000 | 0.00 | +0.002 | nan |
| scouts_indep_3 | 0.124 | 0.353 | -0.110 | -0.121 | 0.063 | 0.93 | +0.001 | nan |
| scouts_clone_3 | 0.124 | 0.372 | -0.093 | -0.106 | 0.000 | 0.00 | +0.002 | nan |
| scouts_indep_4 | 0.124 | 0.329 | -0.126 | -0.139 | 0.057 | 0.86 | +0.001 | nan |
| scouts_clone_4 | 0.124 | 0.337 | -0.119 | -0.129 | 0.000 | 0.00 | +0.002 | nan |
| mace_shared | 0.124 | 0.453 | +0.475 |  | 0.000 | 0.00 | -0.603 | 0.00 |
| mace_separate | 0.124 | 0.480 | +0.485 |  | 0.000 | 0.00 | -0.716 | 0.90 |

Shapley, scouts_indep_3: mace_relax +0.320 [+0.314, +0.326], surrogate +0.019 [+0.013, +0.026], explorer#1 -0.038 [-0.045, -0.031], explorer#2 -0.039 [-0.046, -0.032], explorer#3 -0.032 [-0.041, -0.025]

Shapley, mace_shared: surrogate -0.070 [-0.078, -0.062], explorer -0.075 [-0.082, -0.067], mace_relax#1 +0.237 [+0.233, +0.241], mace_relax#2 +0.237 [+0.233, +0.242]

Shapley, mace_separate: surrogate -0.057 [-0.066, -0.048], explorer -0.071 [-0.078, -0.064], mace_relax#1 +0.243 [+0.238, +0.247], mace_relax#2 +0.243 [+0.238, +0.247]

## Receiver gpaw_r2scan

| game | v(empty) | v(all) | credit of all copies | type-level credit | |gap| between two copies | campaigns with gap > 0.01 | pair dividend | batches with different outputs |
|---|---|---|---|---|---|---|---|---|
| scouts_indep_1 | 0.113 | 0.454 | +nan | +0.001 | nan | nan | +nan | nan |
| scouts_indep_2 | 0.113 | 0.438 | -0.013 | -0.018 | 0.064 | 0.88 | -0.003 | nan |
| scouts_clone_2 | 0.113 | 0.434 | -0.016 | -0.021 | 0.000 | 0.00 | -0.005 | nan |
| scouts_indep_3 | 0.113 | 0.389 | -0.047 | -0.041 | 0.061 | 0.89 | -0.003 | nan |
| scouts_clone_3 | 0.113 | 0.378 | -0.052 | -0.047 | 0.000 | 0.00 | -0.005 | nan |
| scouts_indep_4 | 0.113 | 0.346 | -0.071 | -0.064 | 0.057 | 0.86 | -0.003 | nan |
| scouts_clone_4 | 0.113 | 0.341 | -0.074 | -0.070 | 0.000 | 0.00 | -0.005 | nan |
| mace_shared | 0.113 | 0.492 | +0.352 |  | 0.000 | 0.00 | -0.335 | 0.00 |
| mace_separate | 0.113 | 0.485 | +0.396 |  | 0.000 | 0.00 | -0.246 | 0.89 |

Shapley, scouts_indep_3: mace_relax +0.295 [+0.288, +0.301], surrogate +0.027 [+0.021, +0.034], explorer#1 -0.010 [-0.016, -0.003], explorer#2 -0.019 [-0.026, -0.012], explorer#3 -0.018 [-0.024, -0.011]

Shapley, mace_shared: surrogate +0.018 [+0.012, +0.024], explorer +0.009 [+0.003, +0.016], mace_relax#1 +0.176 [+0.173, +0.180], mace_relax#2 +0.176 [+0.173, +0.180]

Shapley, mace_separate: surrogate -0.023 [-0.030, -0.016], explorer -0.002 [-0.008, +0.004], mace_relax#1 +0.198 [+0.195, +0.202], mace_relax#2 +0.198 [+0.195, +0.202]

