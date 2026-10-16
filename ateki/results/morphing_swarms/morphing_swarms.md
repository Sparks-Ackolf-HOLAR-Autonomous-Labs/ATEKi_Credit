# Experiment 17: morphing swarms (merge, nest, split during the campaign)

Value = early-window recall area of the ten most stable compounds; mean [5th, 95th percentile of the
matched-seed mean by bootstrap]. Share mode isolated unless stated. Number of swarms at 25 % of the compute.

Learned thresholds: join 0.049, split 0.800, nest 0.213, delta 0.327, period 3.048
(defaults {'join': 0.6, 'split': 0.2, 'nest': 0.4, 'delta': 0.1, 'period': 2.0}; training value 0.672)

## Receiver qe_pbe

| start | mode | value | swarms at 25% | groups at 25% | nested at 25% |
|---|---|---|---|---|---|
| one_7 | fixed|isolated | 0.699 [0.691, 0.708] | 1.00 | 1.00 | 0.00 |
| one_7 | full_learned|isolated | 0.686 [0.675, 0.696] | 5.33 | 1.69 | 3.64 |
| one_7 | full|isolated | 0.661 [0.649, 0.673] | 5.03 | 1.09 | 3.94 |
| one_7 | split_only|isolated | 0.659 [0.647, 0.672] | 5.10 | 1.60 | 3.50 |
| split_1x7 | fixed|isolated | 0.592 [0.583, 0.600] | 7.00 | 7.00 | 0.00 |
| split_1x7 | fixed|published | 0.678 [0.669, 0.686] | 7.00 | 7.00 | 0.00 |
| split_1x7 | full_learned|isolated | 0.624 [0.616, 0.632] | 5.92 | 3.01 | 2.91 |
| split_1x7 | full|isolated | 0.613 [0.601, 0.624] | 6.81 | 2.43 | 4.38 |
| split_1x7 | full|published | 0.651 [0.642, 0.661] | 6.32 | 1.34 | 4.98 |
| split_1x7 | merge_only|isolated | 0.621 [0.609, 0.632] | 6.81 | 1.91 | 4.90 |
| split_1x7 | no_nest|isolated | 0.589 [0.581, 0.597] | 6.19 | 6.19 | 0.00 |
| split_1x7 | split_only|isolated | 0.592 [0.583, 0.600] | 7.00 | 7.00 | 0.00 |
| split_2_2_3 | fixed|isolated | 0.661 [0.651, 0.670] | 3.00 | 3.00 | 0.00 |
| split_2_2_3 | full_learned|isolated | 0.672 [0.664, 0.680] | 5.47 | 2.31 | 3.16 |
| split_2_2_3 | full|isolated | 0.667 [0.658, 0.678] | 5.51 | 1.46 | 4.05 |
| split_2_2_3 | merge_only|isolated | 0.681 [0.671, 0.692] | 3.00 | 1.12 | 1.88 |
| split_2_2_3 | no_nest|isolated | 0.649 [0.639, 0.659] | 4.83 | 4.83 | 0.00 |
| split_2_2_3 | split_only|isolated | 0.658 [0.648, 0.667] | 5.36 | 3.76 | 1.60 |
| split_2_5w | fixed|isolated | 0.633 [0.623, 0.644] | 2.00 | 2.00 | 0.00 |
| split_2_5w | full_learned|isolated | 0.631 [0.621, 0.643] | 6.06 | 2.19 | 3.87 |
| split_2_5w | full|isolated | 0.600 [0.589, 0.612] | 6.02 | 1.40 | 4.62 |
| split_2_5w | merge_only|isolated | 0.642 [0.631, 0.653] | 2.00 | 1.28 | 0.72 |
| split_2_5w | no_nest|isolated | 0.594 [0.585, 0.605] | 4.51 | 4.51 | 0.00 |
| split_2_5w | split_only|isolated | 0.603 [0.592, 0.613] | 6.04 | 2.70 | 3.34 |
| split_4_3 | fixed|isolated | 0.645 [0.635, 0.656] | 2.00 | 2.00 | 0.00 |
| split_4_3 | fixed|published | 0.660 [0.651, 0.669] | 2.00 | 2.00 | 0.00 |
| split_4_3 | full_learned|isolated | 0.625 [0.617, 0.634] | 5.59 | 2.13 | 3.46 |
| split_4_3 | full|isolated | 0.623 [0.614, 0.633] | 6.45 | 1.44 | 5.01 |
| split_4_3 | full|published | 0.662 [0.651, 0.672] | 5.91 | 1.09 | 4.82 |
| split_4_3 | merge_only|isolated | 0.650 [0.640, 0.661] | 1.84 | 1.16 | 0.68 |
| split_4_3 | no_nest|isolated | 0.609 [0.600, 0.618] | 4.95 | 4.95 | 0.00 |
| split_4_3 | split_only|isolated | 0.618 [0.608, 0.628] | 6.51 | 3.34 | 3.17 |

## Receiver qe_hse06

| start | mode | value | swarms at 25% | groups at 25% | nested at 25% |
|---|---|---|---|---|---|
| one_7 | fixed|isolated | 0.498 [0.483, 0.513] | 1.00 | 1.00 | 0.00 |
| one_7 | full_learned|isolated | 0.494 [0.479, 0.509] | 4.73 | 1.60 | 3.13 |
| one_7 | full|isolated | 0.468 [0.452, 0.485] | 4.36 | 1.11 | 3.25 |
| one_7 | split_only|isolated | 0.470 [0.453, 0.487] | 4.39 | 1.59 | 2.80 |
| split_1x7 | fixed|isolated | 0.424 [0.412, 0.435] | 7.00 | 7.00 | 0.00 |
| split_1x7 | fixed|published | 0.435 [0.419, 0.450] | 7.00 | 7.00 | 0.00 |
| split_1x7 | full_learned|isolated | 0.435 [0.422, 0.446] | 6.09 | 3.49 | 2.60 |
| split_1x7 | full|isolated | 0.440 [0.424, 0.454] | 6.92 | 3.18 | 3.74 |
| split_1x7 | full|published | 0.420 [0.406, 0.436] | 6.27 | 1.70 | 4.57 |
| split_1x7 | merge_only|isolated | 0.451 [0.434, 0.467] | 6.98 | 2.32 | 4.66 |
| split_1x7 | no_nest|isolated | 0.423 [0.411, 0.433] | 6.71 | 6.71 | 0.00 |
| split_1x7 | split_only|isolated | 0.424 [0.412, 0.435] | 7.00 | 7.00 | 0.00 |
| split_2_2_3 | fixed|isolated | 0.534 [0.520, 0.550] | 3.00 | 3.00 | 0.00 |
| split_2_2_3 | full_learned|isolated | 0.538 [0.524, 0.551] | 5.08 | 2.42 | 2.66 |
| split_2_2_3 | full|isolated | 0.513 [0.496, 0.532] | 4.75 | 1.74 | 3.01 |
| split_2_2_3 | merge_only|isolated | 0.542 [0.526, 0.558] | 2.99 | 1.46 | 1.53 |
| split_2_2_3 | no_nest|isolated | 0.504 [0.487, 0.520] | 4.41 | 4.41 | 0.00 |
| split_2_2_3 | split_only|isolated | 0.506 [0.490, 0.522] | 4.67 | 3.74 | 0.93 |
| split_2_5w | fixed|isolated | 0.475 [0.458, 0.493] | 2.00 | 2.00 | 0.00 |
| split_2_5w | full_learned|isolated | 0.474 [0.455, 0.492] | 5.55 | 2.26 | 3.29 |
| split_2_5w | full|isolated | 0.426 [0.410, 0.443] | 5.44 | 1.69 | 3.75 |
| split_2_5w | merge_only|isolated | 0.493 [0.474, 0.510] | 2.00 | 1.23 | 0.77 |
| split_2_5w | no_nest|isolated | 0.412 [0.398, 0.427] | 4.71 | 4.71 | 0.00 |
| split_2_5w | split_only|isolated | 0.415 [0.402, 0.430] | 5.33 | 2.58 | 2.75 |
| split_4_3 | fixed|isolated | 0.446 [0.428, 0.465] | 2.00 | 2.00 | 0.00 |
| split_4_3 | fixed|published | 0.438 [0.422, 0.453] | 2.00 | 2.00 | 0.00 |
| split_4_3 | full_learned|isolated | 0.429 [0.410, 0.448] | 5.27 | 2.09 | 3.18 |
| split_4_3 | full|isolated | 0.394 [0.377, 0.413] | 5.69 | 1.82 | 3.87 |
| split_4_3 | full|published | 0.448 [0.434, 0.462] | 5.03 | 1.08 | 3.95 |
| split_4_3 | merge_only|isolated | 0.448 [0.430, 0.467] | 1.87 | 1.39 | 0.48 |
| split_4_3 | no_nest|isolated | 0.381 [0.365, 0.397] | 4.67 | 4.67 | 0.00 |
| split_4_3 | split_only|isolated | 0.391 [0.374, 0.410] | 5.74 | 2.73 | 3.01 |

## Receiver gpaw_r2scan

| start | mode | value | swarms at 25% | groups at 25% | nested at 25% |
|---|---|---|---|---|---|
| one_7 | fixed|isolated | 0.468 [0.455, 0.479] | 1.00 | 1.00 | 0.00 |
| one_7 | full_learned|isolated | 0.467 [0.454, 0.478] | 4.06 | 1.32 | 2.74 |
| one_7 | full|isolated | 0.454 [0.441, 0.465] | 3.79 | 1.19 | 2.60 |
| one_7 | split_only|isolated | 0.454 [0.442, 0.466] | 3.81 | 1.49 | 2.32 |
| split_1x7 | fixed|isolated | 0.459 [0.453, 0.467] | 7.00 | 7.00 | 0.00 |
| split_1x7 | fixed|published | 0.472 [0.461, 0.483] | 7.00 | 7.00 | 0.00 |
| split_1x7 | full_learned|isolated | 0.462 [0.455, 0.469] | 5.74 | 3.59 | 2.15 |
| split_1x7 | full|isolated | 0.478 [0.470, 0.485] | 6.83 | 3.42 | 3.41 |
| split_1x7 | full|published | 0.462 [0.452, 0.473] | 6.14 | 2.29 | 3.85 |
| split_1x7 | merge_only|isolated | 0.477 [0.470, 0.484] | 6.93 | 2.61 | 4.32 |
| split_1x7 | no_nest|isolated | 0.459 [0.452, 0.466] | 6.60 | 6.60 | 0.00 |
| split_1x7 | split_only|isolated | 0.459 [0.453, 0.467] | 7.00 | 7.00 | 0.00 |
| split_2_2_3 | fixed|isolated | 0.534 [0.522, 0.546] | 3.00 | 3.00 | 0.00 |
| split_2_2_3 | full_learned|isolated | 0.541 [0.529, 0.553] | 5.20 | 2.56 | 2.64 |
| split_2_2_3 | full|isolated | 0.540 [0.527, 0.553] | 4.87 | 1.90 | 2.97 |
| split_2_2_3 | merge_only|isolated | 0.551 [0.540, 0.563] | 2.97 | 1.48 | 1.49 |
| split_2_2_3 | no_nest|isolated | 0.526 [0.512, 0.540] | 4.61 | 4.61 | 0.00 |
| split_2_2_3 | split_only|isolated | 0.527 [0.513, 0.541] | 4.84 | 3.67 | 1.17 |
| split_2_5w | fixed|isolated | 0.487 [0.473, 0.500] | 2.00 | 2.00 | 0.00 |
| split_2_5w | full_learned|isolated | 0.491 [0.477, 0.505] | 5.23 | 2.36 | 2.87 |
| split_2_5w | full|isolated | 0.462 [0.449, 0.474] | 5.55 | 1.76 | 3.79 |
| split_2_5w | merge_only|isolated | 0.491 [0.478, 0.505] | 2.00 | 1.40 | 0.60 |
| split_2_5w | no_nest|isolated | 0.457 [0.446, 0.467] | 4.71 | 4.71 | 0.00 |
| split_2_5w | split_only|isolated | 0.465 [0.453, 0.477] | 5.53 | 2.51 | 3.02 |
| split_4_3 | fixed|isolated | 0.464 [0.452, 0.476] | 2.00 | 2.00 | 0.00 |
| split_4_3 | fixed|published | 0.428 [0.417, 0.438] | 2.00 | 2.00 | 0.00 |
| split_4_3 | full_learned|isolated | 0.455 [0.443, 0.468] | 5.17 | 2.13 | 3.04 |
| split_4_3 | full|isolated | 0.454 [0.444, 0.465] | 5.92 | 2.03 | 3.89 |
| split_4_3 | full|published | 0.440 [0.430, 0.450] | 5.15 | 1.26 | 3.89 |
| split_4_3 | merge_only|isolated | 0.472 [0.460, 0.484] | 1.90 | 1.41 | 0.49 |
| split_4_3 | no_nest|isolated | 0.455 [0.444, 0.465] | 4.96 | 4.96 | 0.00 |
| split_4_3 | split_only|isolated | 0.452 [0.441, 0.462] | 5.93 | 2.96 | 2.97 |

## Credit with a changing structure

### qe_hse06|split_1x7|merge_only|default
v(all) 0.443, v(empty) 0.120, efficiency gap 5.1e-15
| body | Shapley | Owen (start structure) | time-averaged level value | difference to Shapley [5, 95] |
|---|---|---|---|---|
| mace_relax | +0.213 | +0.213 | +0.237 | +0.024 [-0.019, +0.062] |
| gpumd_nep89_md | +0.058 | +0.058 | +0.043 | -0.015 [-0.032, +0.005] |
| gpumd_nep89_relax | -0.005 | -0.005 | -0.009 | -0.004 [-0.026, +0.013] |
| lammps_meam_md | -0.021 | -0.021 | -0.017 | +0.004 [-0.022, +0.035] |
| archive_mp | +0.136 | +0.136 | +0.130 | -0.006 [-0.031, +0.029] |
| surrogate | -0.017 | -0.017 | -0.020 | -0.004 [-0.031, +0.026] |
| explorer | -0.042 | -0.042 | -0.041 | +0.001 [-0.017, +0.023] |

Most occupied structures (share of early-window compute):
- 0.27: archive_mp || explorer || gpumd_nep89_md || gpumd_nep89_relax || lammps_meam_md || mace_relax || surrogate
- 0.11: archive_mp > explorer > gpumd_nep89_md > surrogate || gpumd_nep89_relax || lammps_meam_md || mace_relax
- 0.08: archive_mp > explorer > gpumd_nep89_md > gpumd_nep89_relax > lammps_meam_md > mace_relax > surrogate
- 0.05: archive_mp > gpumd_nep89_md > surrogate || explorer || gpumd_nep89_relax || lammps_meam_md || mace_relax
- 0.03: archive_mp > explorer > gpumd_nep89_md || gpumd_nep89_relax || lammps_meam_md || mace_relax || surrogate
- 0.03: archive_mp > gpumd_nep89_md || explorer || gpumd_nep89_relax || lammps_meam_md || mace_relax || surrogate
- 0.03: archive_mp > explorer > gpumd_nep89_md > gpumd_nep89_relax > surrogate || lammps_meam_md || mace_relax
- 0.02: archive_mp > explorer > gpumd_nep89_md > gpumd_nep89_relax > surrogate || lammps_meam_md > mace_relax

### qe_pbe|split_2_2_3|fixed|default
v(all) 0.648, v(empty) 0.107, efficiency gap 5.6e-16
| body | Shapley | Owen (start structure) | time-averaged level value | difference to Shapley [5, 95] |
|---|---|---|---|---|
| mace_relax | +0.159 | +0.165 | +0.165 | +0.006 [-0.017, +0.030] |
| archive_mp | +0.177 | +0.159 | +0.159 | -0.019 [-0.035, -0.002] |
| gpumd_nep89_md | +0.082 | +0.106 | +0.106 | +0.024 [+0.002, +0.052] |
| gpumd_nep89_relax | +0.067 | +0.061 | +0.061 | -0.006 [-0.028, +0.020] |
| lammps_meam_md | +0.059 | +0.064 | +0.064 | +0.006 [-0.026, +0.029] |
| surrogate | +0.019 | +0.021 | +0.021 | +0.002 [-0.023, +0.025] |
| explorer | -0.022 | -0.034 | -0.034 | -0.013 [-0.039, +0.015] |

Most occupied structures (share of early-window compute):
- 1.00: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax

### qe_pbe|split_4_3|merge_only|default
v(all) 0.639, v(empty) 0.107, efficiency gap 3.8e-15
| body | Shapley | Owen (start structure) | time-averaged level value | difference to Shapley [5, 95] |
|---|---|---|---|---|
| mace_relax | +0.215 | +0.219 | +0.219 | +0.003 [-0.020, +0.030] |
| gpumd_nep89_md | +0.086 | +0.068 | +0.069 | -0.017 [-0.037, +0.007] |
| lammps_meam_md | +0.030 | +0.009 | +0.009 | -0.021 [-0.042, +0.005] |
| explorer | -0.056 | -0.055 | -0.055 | +0.000 [-0.019, +0.024] |
| archive_mp | +0.184 | +0.205 | +0.204 | +0.021 [-0.013, +0.050] |
| gpumd_nep89_relax | +0.055 | +0.066 | +0.066 | +0.011 [-0.020, +0.045] |
| surrogate | +0.017 | +0.020 | +0.020 | +0.003 [-0.030, +0.026] |

Most occupied structures (share of early-window compute):
- 0.55: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.41: archive_mp+gpumd_nep89_relax+surrogate > explorer+gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.04: archive_mp+explorer+gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate

### qe_pbe|split_2_2_3|merge_only|default
v(all) 0.666, v(empty) 0.107, efficiency gap 1.1e-15
| body | Shapley | Owen (start structure) | time-averaged level value | difference to Shapley [5, 95] |
|---|---|---|---|---|
| mace_relax | +0.165 | +0.161 | +0.160 | -0.005 [-0.034, +0.015] |
| archive_mp | +0.186 | +0.168 | +0.164 | -0.022 [-0.041, -0.003] |
| gpumd_nep89_md | +0.093 | +0.113 | +0.110 | +0.018 [-0.010, +0.043] |
| gpumd_nep89_relax | +0.064 | +0.059 | +0.058 | -0.006 [-0.024, +0.018] |
| lammps_meam_md | +0.052 | +0.061 | +0.065 | +0.013 [-0.020, +0.050] |
| surrogate | +0.016 | +0.021 | +0.026 | +0.010 [-0.011, +0.043] |
| explorer | -0.016 | -0.024 | -0.024 | -0.008 [-0.044, +0.026] |

Most occupied structures (share of early-window compute):
- 0.43: archive_mp+mace_relax > explorer+lammps_meam_md+surrogate > gpumd_nep89_md+gpumd_nep89_relax
- 0.29: archive_mp+mace_relax > gpumd_nep89_md+gpumd_nep89_relax || explorer+lammps_meam_md+surrogate
- 0.23: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.06: archive_mp+mace_relax > explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax

### qe_pbe|split_1x7|merge_only|default
v(all) 0.612, v(empty) 0.107, efficiency gap 8.0e-15
| body | Shapley | Owen (start structure) | time-averaged level value | difference to Shapley [5, 95] |
|---|---|---|---|---|
| mace_relax | +0.204 | +0.204 | +0.211 | +0.007 [-0.033, +0.059] |
| gpumd_nep89_md | +0.086 | +0.086 | +0.071 | -0.015 [-0.038, +0.016] |
| gpumd_nep89_relax | +0.045 | +0.045 | +0.064 | +0.019 [-0.028, +0.058] |
| lammps_meam_md | +0.031 | +0.031 | +0.045 | +0.014 [-0.015, +0.065] |
| archive_mp | +0.168 | +0.168 | +0.156 | -0.012 [-0.041, +0.025] |
| surrogate | +0.007 | +0.007 | -0.007 | -0.014 [-0.035, +0.006] |
| explorer | -0.037 | -0.037 | -0.036 | +0.000 [-0.016, +0.016] |

Most occupied structures (share of early-window compute):
- 0.15: archive_mp || explorer || gpumd_nep89_md || gpumd_nep89_relax || lammps_meam_md || mace_relax || surrogate
- 0.10: archive_mp > explorer > gpumd_nep89_md > gpumd_nep89_relax > lammps_meam_md > mace_relax > surrogate
- 0.07: archive_mp > explorer > gpumd_nep89_md > mace_relax > surrogate || gpumd_nep89_relax || lammps_meam_md
- 0.05: archive_mp > surrogate || explorer || gpumd_nep89_md > mace_relax || gpumd_nep89_relax || lammps_meam_md
- 0.05: archive_mp > explorer > gpumd_nep89_md > surrogate || gpumd_nep89_relax || lammps_meam_md || mace_relax
- 0.04: archive_mp || explorer > mace_relax > surrogate || gpumd_nep89_md || gpumd_nep89_relax || lammps_meam_md
- 0.04: archive_mp > explorer > gpumd_nep89_md > lammps_meam_md > mace_relax > surrogate || gpumd_nep89_relax
- 0.03: archive_mp > explorer > gpumd_nep89_md > gpumd_nep89_relax > surrogate || lammps_meam_md || mace_relax

### qe_pbe|split_1x7|full|learned
v(all) 0.613, v(empty) 0.107, efficiency gap 4.2e-15
| body | Shapley | Owen (start structure) | time-averaged level value | difference to Shapley [5, 95] |
|---|---|---|---|---|
| mace_relax | +0.201 | +0.201 | +0.218 | +0.017 [-0.010, +0.041] |
| gpumd_nep89_md | +0.084 | +0.084 | +0.081 | -0.002 [-0.021, +0.022] |
| gpumd_nep89_relax | +0.051 | +0.051 | +0.047 | -0.005 [-0.024, +0.010] |
| lammps_meam_md | +0.032 | +0.032 | +0.031 | -0.001 [-0.021, +0.014] |
| archive_mp | +0.165 | +0.165 | +0.161 | -0.004 [-0.022, +0.028] |
| surrogate | +0.009 | +0.009 | +0.000 | -0.009 [-0.029, +0.017] |
| explorer | -0.037 | -0.037 | -0.033 | +0.004 [-0.011, +0.020] |

Most occupied structures (share of early-window compute):
- 0.27: archive_mp || explorer || gpumd_nep89_md || gpumd_nep89_relax || lammps_meam_md || mace_relax || surrogate
- 0.03: archive_mp+surrogate || explorer || gpumd_nep89_md+gpumd_nep89_relax || lammps_meam_md+mace_relax
- 0.03: archive_mp > surrogate || explorer || gpumd_nep89_md+gpumd_nep89_relax || lammps_meam_md+mace_relax
- 0.02: archive_mp+mace_relax || explorer > lammps_meam_md || gpumd_nep89_md > gpumd_nep89_relax > surrogate
- 0.02: archive_mp > surrogate || explorer || gpumd_nep89_md > gpumd_nep89_relax || lammps_meam_md+mace_relax
- 0.02: archive_mp+surrogate || explorer > lammps_meam_md || gpumd_nep89_md+gpumd_nep89_relax || mace_relax
- 0.02: archive_mp > gpumd_nep89_md || explorer || gpumd_nep89_relax+surrogate || lammps_meam_md+mace_relax
- 0.01: archive_mp > gpumd_nep89_md > gpumd_nep89_relax > surrogate || explorer || lammps_meam_md+mace_relax

### qe_pbe|split_2_2_3|full|learned
v(all) 0.664, v(empty) 0.107, efficiency gap 1.1e-15
| body | Shapley | Owen (start structure) | time-averaged level value | difference to Shapley [5, 95] |
|---|---|---|---|---|
| mace_relax | +0.165 | +0.171 | +0.164 | -0.001 [-0.024, +0.021] |
| archive_mp | +0.180 | +0.160 | +0.168 | -0.013 [-0.039, +0.020] |
| gpumd_nep89_md | +0.088 | +0.106 | +0.091 | +0.003 [-0.021, +0.028] |
| gpumd_nep89_relax | +0.065 | +0.057 | +0.051 | -0.014 [-0.030, +0.011] |
| lammps_meam_md | +0.060 | +0.068 | +0.073 | +0.014 [-0.011, +0.038] |
| surrogate | +0.022 | +0.025 | +0.028 | +0.006 [-0.025, +0.032] |
| explorer | -0.023 | -0.030 | -0.018 | +0.004 [-0.022, +0.038] |

Most occupied structures (share of early-window compute):
- 0.20: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.10: archive_mp+mace_relax || explorer > lammps_meam_md > surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.04: archive_mp > explorer > gpumd_nep89_md+gpumd_nep89_relax > lammps_meam_md > mace_relax > surrogate
- 0.04: archive_mp+mace_relax || explorer > gpumd_nep89_md+gpumd_nep89_relax > lammps_meam_md > surrogate
- 0.04: archive_mp+mace_relax+surrogate || explorer > gpumd_nep89_md+gpumd_nep89_relax > lammps_meam_md
- 0.03: archive_mp+mace_relax || explorer || gpumd_nep89_md+gpumd_nep89_relax > lammps_meam_md > surrogate
- 0.03: archive_mp+mace_relax+surrogate || explorer > lammps_meam_md || gpumd_nep89_md+gpumd_nep89_relax
- 0.02: archive_mp+mace_relax > explorer > gpumd_nep89_md+gpumd_nep89_relax > lammps_meam_md > surrogate

### qe_pbe|split_4_3|full|learned
v(all) 0.616, v(empty) 0.107, efficiency gap 1.9e-15
| body | Shapley | Owen (start structure) | time-averaged level value | difference to Shapley [5, 95] |
|---|---|---|---|---|
| mace_relax | +0.205 | +0.207 | +0.220 | +0.016 [-0.024, +0.069] |
| gpumd_nep89_md | +0.087 | +0.069 | +0.075 | -0.012 [-0.041, +0.019] |
| lammps_meam_md | +0.025 | +0.004 | +0.009 | -0.016 [-0.044, +0.009] |
| explorer | -0.051 | -0.057 | -0.050 | +0.001 [-0.027, +0.038] |
| archive_mp | +0.173 | +0.197 | +0.182 | +0.008 [-0.020, +0.036] |
| gpumd_nep89_relax | +0.055 | +0.069 | +0.060 | +0.005 [-0.012, +0.038] |
| surrogate | +0.016 | +0.019 | +0.014 | -0.002 [-0.031, +0.020] |

Most occupied structures (share of early-window compute):
- 0.28: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.04: archive_mp > gpumd_nep89_relax > surrogate || explorer > gpumd_nep89_md+lammps_meam_md > mace_relax
- 0.04: archive_mp > explorer > gpumd_nep89_relax > surrogate || gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.03: archive_mp > explorer > gpumd_nep89_md+lammps_meam_md > gpumd_nep89_relax > mace_relax > surrogate
- 0.03: archive_mp > gpumd_nep89_relax > surrogate || explorer > gpumd_nep89_md > lammps_meam_md+mace_relax
- 0.02: archive_mp+gpumd_nep89_relax+surrogate || explorer || gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.02: archive_mp > gpumd_nep89_relax > surrogate || explorer > gpumd_nep89_md > lammps_meam_md > mace_relax
- 0.02: archive_mp > gpumd_nep89_md > gpumd_nep89_relax > lammps_meam_md > mace_relax > surrogate || explorer

### qe_hse06|split_1x7|full|learned
v(all) 0.438, v(empty) 0.120, efficiency gap 6.8e-15
| body | Shapley | Owen (start structure) | time-averaged level value | difference to Shapley [5, 95] |
|---|---|---|---|---|
| mace_relax | +0.207 | +0.207 | +0.199 | -0.008 [-0.023, +0.006] |
| gpumd_nep89_md | +0.053 | +0.053 | +0.055 | +0.002 [-0.013, +0.026] |
| gpumd_nep89_relax | -0.007 | -0.007 | -0.011 | -0.004 [-0.026, +0.016] |
| lammps_meam_md | -0.013 | -0.013 | -0.015 | -0.003 [-0.025, +0.015] |
| archive_mp | +0.125 | +0.125 | +0.125 | +0.000 [-0.013, +0.020] |
| surrogate | -0.014 | -0.014 | -0.011 | +0.004 [-0.023, +0.044] |
| explorer | -0.032 | -0.032 | -0.024 | +0.008 [-0.009, +0.033] |

Most occupied structures (share of early-window compute):
- 0.51: archive_mp || explorer || gpumd_nep89_md || gpumd_nep89_relax || lammps_meam_md || mace_relax || surrogate
- 0.03: archive_mp > gpumd_nep89_md > gpumd_nep89_relax || explorer || lammps_meam_md > mace_relax || surrogate
- 0.03: archive_mp+surrogate || explorer || gpumd_nep89_md > gpumd_nep89_relax || lammps_meam_md+mace_relax
- 0.02: archive_mp > gpumd_nep89_md || explorer || gpumd_nep89_relax || lammps_meam_md > mace_relax || surrogate
- 0.01: archive_mp+surrogate || explorer || gpumd_nep89_md+gpumd_nep89_relax || lammps_meam_md+mace_relax
- 0.01: archive_mp || explorer || gpumd_nep89_md+gpumd_nep89_relax || lammps_meam_md+mace_relax || surrogate
- 0.01: archive_mp > surrogate || explorer || gpumd_nep89_md+gpumd_nep89_relax || lammps_meam_md+mace_relax
- 0.01: archive_mp > surrogate || explorer || gpumd_nep89_md > gpumd_nep89_relax || lammps_meam_md+mace_relax

### qe_hse06|split_2_2_3|merge_only|default
v(all) 0.548, v(empty) 0.120, efficiency gap 1.1e-15
| body | Shapley | Owen (start structure) | time-averaged level value | difference to Shapley [5, 95] |
|---|---|---|---|---|
| mace_relax | +0.180 | +0.164 | +0.160 | -0.019 [-0.072, +0.050] |
| archive_mp | +0.174 | +0.147 | +0.148 | -0.026 [-0.078, +0.045] |
| gpumd_nep89_md | +0.075 | +0.109 | +0.112 | +0.037 [-0.026, +0.093] |
| gpumd_nep89_relax | +0.003 | -0.035 | -0.033 | -0.035 [-0.099, +0.027] |
| lammps_meam_md | +0.021 | +0.057 | +0.057 | +0.037 [-0.008, +0.090] |
| surrogate | -0.014 | -0.010 | -0.011 | +0.003 [-0.062, +0.054] |
| explorer | -0.010 | -0.003 | -0.007 | +0.003 [-0.057, +0.052] |

Most occupied structures (share of early-window compute):
- 0.45: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.25: archive_mp+mace_relax > explorer+lammps_meam_md+surrogate > gpumd_nep89_md+gpumd_nep89_relax
- 0.18: archive_mp+mace_relax > gpumd_nep89_md+gpumd_nep89_relax || explorer+lammps_meam_md+surrogate
- 0.11: archive_mp+mace_relax > explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax

### qe_hse06|split_2_2_3|fixed|default
v(all) 0.537, v(empty) 0.120, efficiency gap 1.1e-15
| body | Shapley | Owen (start structure) | time-averaged level value | difference to Shapley [5, 95] |
|---|---|---|---|---|
| mace_relax | +0.182 | +0.166 | +0.166 | -0.016 [-0.059, +0.045] |
| archive_mp | +0.148 | +0.123 | +0.123 | -0.024 [-0.072, +0.040] |
| gpumd_nep89_md | +0.070 | +0.098 | +0.098 | +0.027 [-0.028, +0.080] |
| gpumd_nep89_relax | +0.000 | -0.044 | -0.044 | -0.044 [-0.098, +0.008] |
| lammps_meam_md | +0.025 | +0.056 | +0.056 | +0.032 [-0.029, +0.086] |
| surrogate | -0.003 | +0.009 | +0.009 | +0.012 [-0.044, +0.061] |
| explorer | -0.005 | +0.008 | +0.008 | +0.013 [-0.040, +0.073] |

Most occupied structures (share of early-window compute):
- 1.00: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax

### qe_hse06|split_4_3|merge_only|default
v(all) 0.469, v(empty) 0.120, efficiency gap 7.8e-15
| body | Shapley | Owen (start structure) | time-averaged level value | difference to Shapley [5, 95] |
|---|---|---|---|---|
| mace_relax | +0.189 | +0.191 | +0.191 | +0.001 [-0.046, +0.043] |
| gpumd_nep89_md | +0.063 | +0.036 | +0.037 | -0.025 [-0.069, +0.019] |
| lammps_meam_md | -0.037 | -0.067 | -0.066 | -0.029 [-0.068, +0.006] |
| explorer | -0.044 | -0.031 | -0.032 | +0.013 [-0.031, +0.050] |
| archive_mp | +0.188 | +0.222 | +0.222 | +0.034 [-0.029, +0.103] |
| gpumd_nep89_relax | -0.011 | -0.007 | -0.007 | +0.004 [-0.040, +0.058] |
| surrogate | +0.001 | +0.004 | +0.003 | +0.002 [-0.069, +0.056] |

Most occupied structures (share of early-window compute):
- 0.64: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.33: archive_mp+gpumd_nep89_relax+surrogate > explorer+gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.03: archive_mp+explorer+gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate

### qe_hse06|split_2_2_3|full|learned
v(all) 0.564, v(empty) 0.120, efficiency gap 7.8e-16
| body | Shapley | Owen (start structure) | time-averaged level value | difference to Shapley [5, 95] |
|---|---|---|---|---|
| mace_relax | +0.187 | +0.171 | +0.157 | -0.030 [-0.072, +0.024] |
| archive_mp | +0.165 | +0.129 | +0.138 | -0.027 [-0.077, +0.022] |
| gpumd_nep89_md | +0.077 | +0.102 | +0.093 | +0.015 [-0.039, +0.072] |
| gpumd_nep89_relax | +0.006 | -0.037 | -0.032 | -0.038 [-0.079, +0.014] |
| lammps_meam_md | +0.029 | +0.064 | +0.072 | +0.043 [-0.006, +0.084] |
| surrogate | -0.012 | +0.004 | +0.002 | +0.014 [-0.040, +0.066] |
| explorer | -0.009 | +0.011 | +0.015 | +0.024 [-0.021, +0.069] |

Most occupied structures (share of early-window compute):
- 0.35: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.11: archive_mp+mace_relax || explorer > lammps_meam_md > surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.04: archive_mp+mace_relax || explorer > gpumd_nep89_md+gpumd_nep89_relax > lammps_meam_md > surrogate
- 0.04: archive_mp+mace_relax+surrogate || explorer > lammps_meam_md || gpumd_nep89_md+gpumd_nep89_relax
- 0.03: archive_mp+mace_relax > explorer > lammps_meam_md > surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.03: archive_mp+mace_relax || explorer > lammps_meam_md || gpumd_nep89_md+gpumd_nep89_relax > surrogate
- 0.03: archive_mp > explorer > lammps_meam_md > mace_relax > surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.02: archive_mp > lammps_meam_md > mace_relax > surrogate || explorer || gpumd_nep89_md+gpumd_nep89_relax

### qe_hse06|split_4_3|full|learned
v(all) 0.421, v(empty) 0.120, efficiency gap 3.2e-15
| body | Shapley | Owen (start structure) | time-averaged level value | difference to Shapley [5, 95] |
|---|---|---|---|---|
| mace_relax | +0.180 | +0.180 | +0.189 | +0.009 [-0.034, +0.054] |
| gpumd_nep89_md | +0.051 | +0.024 | +0.031 | -0.021 [-0.063, +0.016] |
| lammps_meam_md | -0.038 | -0.071 | -0.072 | -0.034 [-0.071, +0.010] |
| explorer | -0.052 | -0.034 | -0.036 | +0.016 [-0.019, +0.047] |
| archive_mp | +0.176 | +0.209 | +0.198 | +0.022 [-0.013, +0.061] |
| gpumd_nep89_relax | -0.017 | -0.010 | -0.008 | +0.009 [-0.028, +0.051] |
| surrogate | -0.000 | +0.003 | -0.002 | -0.002 [-0.057, +0.041] |

Most occupied structures (share of early-window compute):
- 0.40: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.03: archive_mp+gpumd_nep89_relax > explorer > gpumd_nep89_md > lammps_meam_md > mace_relax > surrogate
- 0.03: archive_mp > gpumd_nep89_md > gpumd_nep89_relax > lammps_meam_md > mace_relax > surrogate || explorer
- 0.03: archive_mp+gpumd_nep89_relax > surrogate || explorer > gpumd_nep89_md > lammps_meam_md > mace_relax
- 0.03: archive_mp+gpumd_nep89_relax+surrogate || explorer > gpumd_nep89_md+lammps_meam_md > mace_relax
- 0.03: archive_mp+gpumd_nep89_relax+surrogate || explorer || gpumd_nep89_md+lammps_meam_md || mace_relax
- 0.03: archive_mp+surrogate > explorer > gpumd_nep89_md > gpumd_nep89_relax > lammps_meam_md > mace_relax
- 0.02: archive_mp+gpumd_nep89_relax+surrogate || explorer > gpumd_nep89_md > lammps_meam_md > mace_relax

