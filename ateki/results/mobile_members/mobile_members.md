# Experiment 18: members that move between swarms or sit in two swarms

Value = early-window recall area of the ten most stable compounds; mean [5th, 95th percentile of the
matched-seed mean by bootstrap]. Moves and shared members counted in the early window (25 % of compute).

Learned thresholds: move 0.251, bridge 0.073, cool 1.133
(defaults {'move': 0.2, 'bridge': 0.6, 'cool': 2.0}; training value 0.685)

## Receiver qe_pbe

| start | swarm mode | member rule | value | minus rule none | moves | mean shared members at 25% |
|---|---|---|---|---|---|---|
| one_7 | fixed | move | 0.699 [0.691, 0.708] | +0.000 [+0.000, +0.000] | 0.00 | 0.00 |
| one_7 | fixed | move learned | 0.699 [0.691, 0.708] | +0.000 [+0.000, +0.000] | 0.00 | 0.00 |
| one_7 | fixed | move+share | 0.699 [0.691, 0.708] | +0.000 [+0.000, +0.000] | 0.00 | 0.00 |
| one_7 | fixed | move+share learned | 0.699 [0.691, 0.708] | +0.000 [+0.000, +0.000] | 0.00 | 0.00 |
| one_7 | fixed | none | 0.699 [0.691, 0.708] |  | 0.00 | 0.00 |
| one_7 | fixed | share | 0.699 [0.691, 0.708] | +0.000 [+0.000, +0.000] | 0.00 | 0.00 |
| one_7 | fixed | share learned | 0.699 [0.691, 0.708] | +0.000 [+0.000, +0.000] | 0.00 | 0.00 |
| one_7 | full | move | 0.665 [0.653, 0.677] | +0.004 [+0.000, +0.007] | 1.62 | 0.00 |
| one_7 | full | move+share | 0.671 [0.660, 0.682] | +0.010 [+0.006, +0.014] | 1.57 | 1.05 |
| one_7 | full | none | 0.661 [0.649, 0.673] |  | 0.00 | 0.00 |
| one_7 | full | share | 0.669 [0.657, 0.680] | +0.008 [+0.004, +0.011] | 0.00 | 1.34 |
| split_1x7 | fixed | move | 0.640 [0.630, 0.649] | +0.048 [+0.039, +0.058] | 4.28 | 0.00 |
| split_1x7 | fixed | move learned | 0.640 [0.630, 0.649] | +0.049 [+0.039, +0.058] | 4.08 | 0.00 |
| split_1x7 | fixed | move+share | 0.642 [0.632, 0.652] | +0.050 [+0.040, +0.060] | 4.36 | 1.17 |
| split_1x7 | fixed | move+share learned | 0.659 [0.649, 0.669] | +0.068 [+0.056, +0.079] | 4.17 | 2.66 |
| split_1x7 | fixed | none | 0.592 [0.583, 0.600] |  | 0.00 | 0.00 |
| split_1x7 | fixed | share | 0.596 [0.587, 0.605] | +0.005 [+0.000, +0.009] | 0.00 | 1.40 |
| split_1x7 | fixed | share learned | 0.628 [0.621, 0.635] | +0.037 [+0.029, +0.045] | 0.00 | 2.14 |
| split_1x7 | full | move | 0.634 [0.625, 0.643] | +0.022 [+0.009, +0.034] | 6.64 | 0.00 |
| split_1x7 | full | move+share | 0.633 [0.624, 0.643] | +0.021 [+0.008, +0.033] | 6.62 | 1.31 |
| split_1x7 | full | none | 0.613 [0.601, 0.624] |  | 0.00 | 0.00 |
| split_1x7 | full | share | 0.612 [0.601, 0.624] | -0.000 [-0.002, +0.002] | 0.00 | 2.04 |
| split_1x7 | merge_only | move | 0.642 [0.632, 0.651] | +0.021 [+0.009, +0.034] | 4.52 | 0.00 |
| split_1x7 | merge_only | move+share | 0.642 [0.633, 0.651] | +0.021 [+0.009, +0.034] | 4.53 | 1.69 |
| split_1x7 | merge_only | none | 0.621 [0.609, 0.632] |  | 0.00 | 0.00 |
| split_1x7 | merge_only | share | 0.619 [0.607, 0.631] | -0.001 [-0.003, +0.001] | 0.00 | 2.03 |
| split_2_2_3 | fixed | move | 0.659 [0.650, 0.669] | -0.001 [-0.006, +0.004] | 1.30 | 0.00 |
| split_2_2_3 | fixed | move learned | 0.660 [0.650, 0.669] | -0.001 [-0.006, +0.003] | 0.81 | 0.00 |
| split_2_2_3 | fixed | move+share | 0.660 [0.651, 0.669] | -0.001 [-0.006, +0.004] | 1.30 | 0.51 |
| split_2_2_3 | fixed | move+share learned | 0.702 [0.693, 0.710] | +0.041 [+0.033, +0.050] | 1.44 | 1.51 |
| split_2_2_3 | fixed | none | 0.661 [0.651, 0.670] |  | 0.00 | 0.00 |
| split_2_2_3 | fixed | share | 0.664 [0.655, 0.674] | +0.004 [+0.001, +0.007] | 0.00 | 0.97 |
| split_2_2_3 | fixed | share learned | 0.705 [0.697, 0.714] | +0.045 [+0.036, +0.053] | 0.00 | 2.09 |
| split_2_2_3 | full | move | 0.665 [0.655, 0.675] | -0.002 [-0.006, +0.001] | 2.23 | 0.00 |
| split_2_2_3 | full | move+share | 0.666 [0.657, 0.676] | -0.001 [-0.006, +0.004] | 2.18 | 1.90 |
| split_2_2_3 | full | none | 0.667 [0.658, 0.678] |  | 0.00 | 0.00 |
| split_2_2_3 | full | share | 0.670 [0.660, 0.680] | +0.003 [-0.001, +0.006] | 0.00 | 2.45 |
| split_2_2_3 | merge_only | move | 0.681 [0.671, 0.692] | -0.000 [-0.006, +0.005] | 1.73 | 0.00 |
| split_2_2_3 | merge_only | move+share | 0.679 [0.669, 0.690] | -0.002 [-0.008, +0.004] | 1.72 | 1.86 |
| split_2_2_3 | merge_only | none | 0.681 [0.671, 0.692] |  | 0.00 | 0.00 |
| split_2_2_3 | merge_only | share | 0.684 [0.675, 0.694] | +0.003 [-0.001, +0.007] | 0.00 | 2.43 |
| split_2_5w | fixed | move | 0.644 [0.634, 0.654] | +0.011 [+0.004, +0.017] | 0.88 | 0.00 |
| split_2_5w | fixed | move learned | 0.641 [0.631, 0.651] | +0.009 [+0.003, +0.015] | 0.88 | 0.00 |
| split_2_5w | fixed | move+share | 0.644 [0.634, 0.654] | +0.011 [+0.004, +0.017] | 0.88 | 0.00 |
| split_2_5w | fixed | move+share learned | 0.648 [0.639, 0.657] | +0.015 [+0.007, +0.022] | 0.87 | 0.08 |
| split_2_5w | fixed | none | 0.633 [0.623, 0.644] |  | 0.00 | 0.00 |
| split_2_5w | fixed | share | 0.635 [0.624, 0.645] | +0.002 [-0.001, +0.004] | 0.00 | 0.34 |
| split_2_5w | fixed | share learned | 0.658 [0.648, 0.667] | +0.025 [+0.017, +0.033] | 0.00 | 1.59 |
| split_2_5w | full | move | 0.614 [0.604, 0.625] | +0.014 [+0.007, +0.022] | 3.77 | 0.00 |
| split_2_5w | full | move+share | 0.614 [0.604, 0.625] | +0.014 [+0.007, +0.022] | 3.98 | 1.52 |
| split_2_5w | full | none | 0.600 [0.589, 0.612] |  | 0.00 | 0.00 |
| split_2_5w | full | share | 0.611 [0.600, 0.623] | +0.011 [+0.007, +0.015] | 0.00 | 1.61 |
| split_2_5w | merge_only | move | 0.651 [0.641, 0.661] | +0.009 [+0.002, +0.017] | 0.94 | 0.00 |
| split_2_5w | merge_only | move+share | 0.651 [0.641, 0.661] | +0.009 [+0.002, +0.017] | 0.94 | 0.00 |
| split_2_5w | merge_only | none | 0.642 [0.631, 0.653] |  | 0.00 | 0.00 |
| split_2_5w | merge_only | share | 0.643 [0.632, 0.654] | +0.001 [-0.000, +0.003] | 0.00 | 0.48 |
| split_4_3 | fixed | move | 0.645 [0.634, 0.655] | -0.000 [-0.002, +0.001] | 0.32 | 0.00 |
| split_4_3 | fixed | move learned | 0.644 [0.633, 0.654] | -0.001 [-0.003, -0.000] | 0.16 | 0.00 |
| split_4_3 | fixed | move+share | 0.647 [0.637, 0.658] | +0.002 [-0.001, +0.004] | 0.45 | 0.56 |
| split_4_3 | fixed | move+share learned | 0.657 [0.648, 0.667] | +0.012 [+0.006, +0.017] | 0.47 | 1.74 |
| split_4_3 | fixed | none | 0.645 [0.635, 0.656] |  | 0.00 | 0.00 |
| split_4_3 | fixed | share | 0.648 [0.637, 0.658] | +0.002 [+0.001, +0.004] | 0.00 | 0.97 |
| split_4_3 | fixed | share learned | 0.658 [0.648, 0.667] | +0.012 [+0.007, +0.017] | 0.00 | 2.36 |
| split_4_3 | full | move | 0.619 [0.608, 0.629] | -0.005 [-0.012, +0.002] | 3.77 | 0.00 |
| split_4_3 | full | move+share | 0.626 [0.617, 0.636] | +0.003 [-0.004, +0.010] | 3.89 | 1.43 |
| split_4_3 | full | none | 0.623 [0.614, 0.633] |  | 0.00 | 0.00 |
| split_4_3 | full | share | 0.630 [0.621, 0.640] | +0.007 [+0.004, +0.010] | 0.00 | 1.93 |
| split_4_3 | merge_only | move | 0.649 [0.639, 0.660] | -0.001 [-0.002, +0.001] | 0.53 | 0.00 |
| split_4_3 | merge_only | move+share | 0.652 [0.641, 0.662] | +0.001 [-0.000, +0.004] | 0.58 | 0.57 |
| split_4_3 | merge_only | none | 0.650 [0.640, 0.661] |  | 0.00 | 0.00 |
| split_4_3 | merge_only | share | 0.652 [0.642, 0.663] | +0.002 [+0.000, +0.003] | 0.00 | 1.28 |

- one_7|full|move: most frequent moves mace_relax -> lammps_meam_md 0.10; mace_relax -> surrogate 0.09; mace_relax -> gpumd_nep89_md 0.09; gpumd_nep89_relax -> gpumd_nep89_md 0.08
- one_7|full|move+share: most frequent moves archive_mp -> gpumd_nep89_relax 0.12; archive_mp -> surrogate 0.09; gpumd_nep89_relax -> surrogate 0.09; archive_mp -> lammps_meam_md 0.09
- split_1x7|fixed|move: most frequent moves gpumd_nep89_md -> gpumd_nep89_relax 0.78; mace_relax -> lammps_meam_md 0.76; surrogate -> archive_mp 0.43; archive_mp -> surrogate 0.28
- split_1x7|fixed|move learned: most frequent moves gpumd_nep89_md -> gpumd_nep89_relax 0.77; mace_relax -> lammps_meam_md 0.76; surrogate -> archive_mp 0.44; archive_mp -> surrogate 0.29
- split_1x7|fixed|move+share: most frequent moves gpumd_nep89_md -> gpumd_nep89_relax 0.78; mace_relax -> lammps_meam_md 0.76; surrogate -> archive_mp 0.43; archive_mp -> surrogate 0.28
- split_1x7|fixed|move+share learned: most frequent moves mace_relax -> lammps_meam_md 0.76; gpumd_nep89_md -> gpumd_nep89_relax 0.71; surrogate -> archive_mp 0.37; archive_mp -> surrogate 0.28
- split_1x7|full|move: most frequent moves mace_relax -> lammps_meam_md 1.04; gpumd_nep89_md -> gpumd_nep89_relax 0.78; surrogate -> archive_mp 0.62; archive_mp -> surrogate 0.38
- split_1x7|full|move+share: most frequent moves mace_relax -> lammps_meam_md 1.07; gpumd_nep89_md -> gpumd_nep89_relax 0.78; surrogate -> archive_mp 0.64; archive_mp -> surrogate 0.40
- split_1x7|merge_only|move: most frequent moves mace_relax -> lammps_meam_md 0.76; gpumd_nep89_md -> gpumd_nep89_relax 0.73; surrogate -> archive_mp 0.38; archive_mp -> surrogate 0.27
- split_1x7|merge_only|move+share: most frequent moves mace_relax -> lammps_meam_md 0.77; gpumd_nep89_md -> gpumd_nep89_relax 0.73; surrogate -> archive_mp 0.38; archive_mp -> surrogate 0.28
- split_2_2_3|fixed|move: most frequent moves surrogate -> archive_mp+mace_relax 0.25; lammps_meam_md -> archive_mp+mace_relax 0.24; surrogate -> archive_mp+lammps_meam_md+mace_relax 0.23; lammps_meam_md -> archive_mp+mace_relax+surrogate 0.18
- split_2_2_3|fixed|move learned: most frequent moves surrogate -> archive_mp+mace_relax 0.23; lammps_meam_md -> archive_mp+mace_relax 0.13; lammps_meam_md -> archive_mp+mace_relax+surrogate 0.12; surrogate -> archive_mp+lammps_meam_md+mace_relax 0.12
- split_2_2_3|fixed|move+share: most frequent moves surrogate -> archive_mp+mace_relax 0.25; lammps_meam_md -> archive_mp+mace_relax 0.22; surrogate -> archive_mp+lammps_meam_md+mace_relax 0.20; lammps_meam_md -> archive_mp+mace_relax+surrogate 0.18
- split_2_2_3|fixed|move+share learned: most frequent moves lammps_meam_md -> archive_mp+mace_relax 0.27; surrogate -> archive_mp+mace_relax 0.27; lammps_meam_md -> archive_mp+mace_relax+surrogate 0.23; surrogate -> archive_mp+lammps_meam_md+mace_relax 0.18
- split_2_2_3|full|move: most frequent moves mace_relax -> archive_mp 0.83; lammps_meam_md -> surrogate 0.27; gpumd_nep89_md -> gpumd_nep89_relax 0.16; surrogate -> lammps_meam_md 0.11
- split_2_2_3|full|move+share: most frequent moves mace_relax -> archive_mp 0.69; lammps_meam_md -> surrogate 0.28; gpumd_nep89_md -> gpumd_nep89_relax 0.13; surrogate -> lammps_meam_md 0.10
- split_2_2_3|merge_only|move: most frequent moves lammps_meam_md -> archive_mp+mace_relax 0.28; surrogate -> archive_mp+lammps_meam_md+mace_relax 0.21; surrogate -> archive_mp+mace_relax 0.17; lammps_meam_md -> archive_mp+mace_relax+surrogate 0.12
- split_2_2_3|merge_only|move+share: most frequent moves lammps_meam_md -> archive_mp+mace_relax 0.27; surrogate -> archive_mp+mace_relax 0.20; surrogate -> archive_mp+lammps_meam_md+mace_relax 0.19; lammps_meam_md -> archive_mp+mace_relax+surrogate 0.16
- split_2_5w|fixed|move: most frequent moves gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.86; explorer -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.02
- split_2_5w|fixed|move learned: most frequent moves gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.87; explorer -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.01
- split_2_5w|fixed|move+share: most frequent moves gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.86; explorer -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.02
- split_2_5w|fixed|move+share learned: most frequent moves gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.86; explorer -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.01
- split_2_5w|full|move: most frequent moves archive_mp -> gpumd_nep89_relax 0.37; mace_relax -> lammps_meam_md 0.24; surrogate -> lammps_meam_md 0.21; archive_mp -> surrogate 0.20
- split_2_5w|full|move+share: most frequent moves archive_mp -> gpumd_nep89_relax 0.36; archive_mp -> surrogate 0.28; surrogate -> lammps_meam_md 0.25; mace_relax -> lammps_meam_md 0.23
- split_2_5w|merge_only|move: most frequent moves gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.92; explorer -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.02
- split_2_5w|merge_only|move+share: most frequent moves gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.92; explorer -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.02
- split_4_3|fixed|move: most frequent moves mace_relax -> archive_mp+gpumd_nep89_relax+surrogate 0.12; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+surrogate 0.04; explorer -> archive_mp+gpumd_nep89_relax+surrogate 0.02; lammps_meam_md -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+surrogate 0.02
- split_4_3|fixed|move learned: most frequent moves mace_relax -> archive_mp+gpumd_nep89_relax+surrogate 0.09; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+surrogate 0.02; lammps_meam_md -> archive_mp+gpumd_nep89_relax+mace_relax+surrogate 0.01; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.01
- split_4_3|fixed|move+share: most frequent moves mace_relax -> archive_mp+gpumd_nep89_relax+surrogate 0.14; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+surrogate 0.05; lammps_meam_md -> archive_mp+gpumd_nep89_relax+surrogate 0.05; mace_relax -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+surrogate 0.04
- split_4_3|fixed|move+share learned: most frequent moves mace_relax -> archive_mp+gpumd_nep89_relax+surrogate 0.16; lammps_meam_md -> archive_mp+gpumd_nep89_relax+surrogate 0.06; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.06; mace_relax -> archive_mp+gpumd_nep89_relax+lammps_meam_md+surrogate 0.04
- split_4_3|full|move: most frequent moves mace_relax -> gpumd_nep89_md 0.73; mace_relax -> lammps_meam_md 0.39; gpumd_nep89_md -> lammps_meam_md 0.31; archive_mp -> surrogate 0.29
- split_4_3|full|move+share: most frequent moves mace_relax -> gpumd_nep89_md 0.72; mace_relax -> lammps_meam_md 0.43; archive_mp -> surrogate 0.34; gpumd_nep89_md -> lammps_meam_md 0.30
- split_4_3|merge_only|move: most frequent moves mace_relax -> archive_mp+gpumd_nep89_relax+surrogate 0.21; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+surrogate 0.05; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.04; lammps_meam_md -> archive_mp+gpumd_nep89_relax+surrogate 0.03
- split_4_3|merge_only|move+share: most frequent moves mace_relax -> archive_mp+gpumd_nep89_relax+surrogate 0.19; lammps_meam_md -> archive_mp+gpumd_nep89_relax+surrogate 0.06; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.05; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+surrogate 0.04

## Receiver qe_hse06

| start | swarm mode | member rule | value | minus rule none | moves | mean shared members at 25% |
|---|---|---|---|---|---|---|
| one_7 | fixed | move | 0.498 [0.483, 0.513] | +0.000 [+0.000, +0.000] | 0.00 | 0.00 |
| one_7 | fixed | move learned | 0.498 [0.483, 0.513] | +0.000 [+0.000, +0.000] | 0.00 | 0.00 |
| one_7 | fixed | move+share | 0.498 [0.483, 0.513] | +0.000 [+0.000, +0.000] | 0.00 | 0.00 |
| one_7 | fixed | move+share learned | 0.498 [0.483, 0.513] | +0.000 [+0.000, +0.000] | 0.00 | 0.00 |
| one_7 | fixed | none | 0.498 [0.483, 0.513] |  | 0.00 | 0.00 |
| one_7 | fixed | share | 0.498 [0.483, 0.513] | +0.000 [+0.000, +0.000] | 0.00 | 0.00 |
| one_7 | fixed | share learned | 0.498 [0.483, 0.513] | +0.000 [+0.000, +0.000] | 0.00 | 0.00 |
| one_7 | full | move | 0.470 [0.453, 0.486] | +0.001 [-0.001, +0.004] | 0.71 | 0.00 |
| one_7 | full | move+share | 0.474 [0.458, 0.490] | +0.006 [+0.001, +0.010] | 0.70 | 1.45 |
| one_7 | full | none | 0.468 [0.452, 0.485] |  | 0.00 | 0.00 |
| one_7 | full | share | 0.472 [0.456, 0.488] | +0.004 [-0.001, +0.009] | 0.00 | 1.83 |
| split_1x7 | fixed | move | 0.494 [0.481, 0.509] | +0.071 [+0.054, +0.088] | 3.90 | 0.00 |
| split_1x7 | fixed | move learned | 0.496 [0.483, 0.509] | +0.072 [+0.055, +0.090] | 3.67 | 0.00 |
| split_1x7 | fixed | move+share | 0.494 [0.481, 0.508] | +0.071 [+0.054, +0.088] | 3.87 | 0.82 |
| split_1x7 | fixed | move+share learned | 0.509 [0.495, 0.524] | +0.086 [+0.066, +0.105] | 3.92 | 2.83 |
| split_1x7 | fixed | none | 0.424 [0.412, 0.435] |  | 0.00 | 0.00 |
| split_1x7 | fixed | share | 0.431 [0.418, 0.443] | +0.007 [+0.002, +0.013] | 0.00 | 0.78 |
| split_1x7 | fixed | share learned | 0.448 [0.433, 0.462] | +0.024 [+0.014, +0.033] | 0.00 | 2.15 |
| split_1x7 | full | move | 0.480 [0.464, 0.495] | +0.040 [+0.021, +0.059] | 4.86 | 0.00 |
| split_1x7 | full | move+share | 0.480 [0.464, 0.495] | +0.040 [+0.021, +0.059] | 4.88 | 0.76 |
| split_1x7 | full | none | 0.440 [0.424, 0.454] |  | 0.00 | 0.00 |
| split_1x7 | full | share | 0.442 [0.426, 0.457] | +0.002 [-0.000, +0.005] | 0.00 | 0.97 |
| split_1x7 | merge_only | move | 0.478 [0.461, 0.494] | +0.027 [+0.007, +0.047] | 3.94 | 0.00 |
| split_1x7 | merge_only | move+share | 0.478 [0.461, 0.494] | +0.027 [+0.008, +0.048] | 3.95 | 0.85 |
| split_1x7 | merge_only | none | 0.451 [0.434, 0.467] |  | 0.00 | 0.00 |
| split_1x7 | merge_only | share | 0.450 [0.434, 0.466] | -0.001 [-0.005, +0.003] | 0.00 | 1.21 |
| split_2_2_3 | fixed | move | 0.536 [0.521, 0.552] | +0.002 [-0.004, +0.008] | 0.73 | 0.00 |
| split_2_2_3 | fixed | move learned | 0.533 [0.519, 0.549] | -0.001 [-0.005, +0.004] | 0.43 | 0.00 |
| split_2_2_3 | fixed | move+share | 0.537 [0.522, 0.553] | +0.002 [-0.003, +0.009] | 0.75 | 0.16 |
| split_2_2_3 | fixed | move+share learned | 0.575 [0.560, 0.590] | +0.041 [+0.028, +0.053] | 1.05 | 1.88 |
| split_2_2_3 | fixed | none | 0.534 [0.520, 0.550] |  | 0.00 | 0.00 |
| split_2_2_3 | fixed | share | 0.539 [0.524, 0.554] | +0.004 [+0.001, +0.008] | 0.00 | 0.37 |
| split_2_2_3 | fixed | share learned | 0.573 [0.559, 0.587] | +0.038 [+0.026, +0.050] | 0.00 | 2.29 |
| split_2_2_3 | full | move | 0.513 [0.495, 0.532] | -0.001 [-0.004, +0.003] | 0.89 | 0.00 |
| split_2_2_3 | full | move+share | 0.516 [0.497, 0.534] | +0.002 [-0.003, +0.008] | 0.93 | 1.84 |
| split_2_2_3 | full | none | 0.513 [0.496, 0.532] |  | 0.00 | 0.00 |
| split_2_2_3 | full | share | 0.516 [0.498, 0.535] | +0.002 [-0.002, +0.007] | 0.00 | 2.26 |
| split_2_2_3 | merge_only | move | 0.541 [0.525, 0.558] | -0.001 [-0.007, +0.005] | 1.24 | 0.00 |
| split_2_2_3 | merge_only | move+share | 0.542 [0.526, 0.559] | +0.000 [-0.006, +0.006] | 1.22 | 1.72 |
| split_2_2_3 | merge_only | none | 0.542 [0.526, 0.558] |  | 0.00 | 0.00 |
| split_2_2_3 | merge_only | share | 0.546 [0.530, 0.562] | +0.004 [+0.001, +0.008] | 0.00 | 2.12 |
| split_2_5w | fixed | move | 0.482 [0.465, 0.499] | +0.006 [-0.002, +0.015] | 0.75 | 0.00 |
| split_2_5w | fixed | move learned | 0.481 [0.465, 0.498] | +0.006 [-0.002, +0.014] | 0.69 | 0.00 |
| split_2_5w | fixed | move+share | 0.482 [0.465, 0.499] | +0.006 [-0.002, +0.015] | 0.75 | 0.00 |
| split_2_5w | fixed | move+share learned | 0.493 [0.475, 0.510] | +0.017 [+0.008, +0.026] | 0.81 | 0.13 |
| split_2_5w | fixed | none | 0.475 [0.458, 0.493] |  | 0.00 | 0.00 |
| split_2_5w | fixed | share | 0.476 [0.459, 0.493] | +0.001 [-0.000, +0.002] | 0.00 | 0.14 |
| split_2_5w | fixed | share learned | 0.499 [0.480, 0.517] | +0.023 [+0.015, +0.031] | 0.00 | 2.03 |
| split_2_5w | full | move | 0.438 [0.423, 0.454] | +0.012 [+0.000, +0.025] | 2.26 | 0.00 |
| split_2_5w | full | move+share | 0.438 [0.422, 0.454] | +0.012 [-0.001, +0.025] | 2.17 | 1.53 |
| split_2_5w | full | none | 0.426 [0.410, 0.443] |  | 0.00 | 0.00 |
| split_2_5w | full | share | 0.429 [0.412, 0.445] | +0.003 [-0.001, +0.007] | 0.00 | 2.22 |
| split_2_5w | merge_only | move | 0.493 [0.476, 0.510] | +0.000 [-0.008, +0.009] | 0.84 | 0.00 |
| split_2_5w | merge_only | move+share | 0.493 [0.476, 0.510] | +0.000 [-0.008, +0.009] | 0.84 | 0.00 |
| split_2_5w | merge_only | none | 0.493 [0.474, 0.510] |  | 0.00 | 0.00 |
| split_2_5w | merge_only | share | 0.493 [0.475, 0.511] | +0.001 [-0.000, +0.002] | 0.00 | 0.51 |
| split_4_3 | fixed | move | 0.447 [0.428, 0.466] | +0.001 [-0.001, +0.003] | 0.23 | 0.00 |
| split_4_3 | fixed | move learned | 0.447 [0.428, 0.466] | +0.001 [-0.001, +0.004] | 0.11 | 0.00 |
| split_4_3 | fixed | move+share | 0.449 [0.431, 0.468] | +0.003 [+0.000, +0.007] | 0.30 | 0.72 |
| split_4_3 | fixed | move+share learned | 0.458 [0.440, 0.477] | +0.012 [+0.004, +0.019] | 0.40 | 1.89 |
| split_4_3 | fixed | none | 0.446 [0.428, 0.465] |  | 0.00 | 0.00 |
| split_4_3 | fixed | share | 0.449 [0.431, 0.468] | +0.003 [+0.001, +0.006] | 0.00 | 0.97 |
| split_4_3 | fixed | share learned | 0.457 [0.439, 0.477] | +0.011 [+0.004, +0.019] | 0.00 | 2.45 |
| split_4_3 | full | move | 0.404 [0.386, 0.423] | +0.009 [+0.003, +0.016] | 2.01 | 0.00 |
| split_4_3 | full | move+share | 0.405 [0.387, 0.424] | +0.011 [+0.005, +0.017] | 2.07 | 1.71 |
| split_4_3 | full | none | 0.394 [0.377, 0.413] |  | 0.00 | 0.00 |
| split_4_3 | full | share | 0.398 [0.381, 0.416] | +0.004 [+0.001, +0.006] | 0.00 | 2.12 |
| split_4_3 | merge_only | move | 0.449 [0.431, 0.468] | +0.001 [-0.001, +0.004] | 0.33 | 0.00 |
| split_4_3 | merge_only | move+share | 0.450 [0.432, 0.469] | +0.002 [-0.001, +0.005] | 0.33 | 0.93 |
| split_4_3 | merge_only | none | 0.448 [0.430, 0.467] |  | 0.00 | 0.00 |
| split_4_3 | merge_only | share | 0.449 [0.431, 0.468] | +0.001 [-0.000, +0.003] | 0.00 | 1.34 |

- one_7|full|move: most frequent moves archive_mp -> surrogate 0.06; surrogate -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+mace_relax 0.06; archive_mp -> gpumd_nep89_relax 0.05; archive_mp -> gpumd_nep89_md 0.05
- one_7|full|move+share: most frequent moves archive_mp -> gpumd_nep89_md 0.07; gpumd_nep89_relax -> gpumd_nep89_md 0.05; archive_mp -> surrogate 0.05; surrogate -> gpumd_nep89_relax 0.04
- split_1x7|fixed|move: most frequent moves mace_relax -> lammps_meam_md 0.90; gpumd_nep89_md -> gpumd_nep89_relax 0.63; surrogate -> archive_mp 0.51; gpumd_nep89_md -> archive_mp 0.24
- split_1x7|fixed|move learned: most frequent moves mace_relax -> lammps_meam_md 0.90; gpumd_nep89_md -> gpumd_nep89_relax 0.63; surrogate -> archive_mp 0.53; gpumd_nep89_md -> archive_mp 0.24
- split_1x7|fixed|move+share: most frequent moves mace_relax -> lammps_meam_md 0.90; gpumd_nep89_md -> gpumd_nep89_relax 0.63; surrogate -> archive_mp 0.51; gpumd_nep89_md -> archive_mp 0.24
- split_1x7|fixed|move+share learned: most frequent moves mace_relax -> lammps_meam_md 0.91; gpumd_nep89_md -> gpumd_nep89_relax 0.64; surrogate -> archive_mp 0.49; gpumd_nep89_md -> archive_mp 0.21
- split_1x7|full|move: most frequent moves mace_relax -> lammps_meam_md 1.15; surrogate -> archive_mp 0.59; gpumd_nep89_md -> gpumd_nep89_relax 0.59; gpumd_nep89_relax -> gpumd_nep89_md 0.27
- split_1x7|full|move+share: most frequent moves mace_relax -> lammps_meam_md 1.15; surrogate -> archive_mp 0.59; gpumd_nep89_md -> gpumd_nep89_relax 0.59; archive_mp -> surrogate 0.28
- split_1x7|merge_only|move: most frequent moves mace_relax -> lammps_meam_md 0.90; gpumd_nep89_md -> gpumd_nep89_relax 0.57; surrogate -> archive_mp 0.50; gpumd_nep89_md -> archive_mp 0.21
- split_1x7|merge_only|move+share: most frequent moves mace_relax -> lammps_meam_md 0.90; gpumd_nep89_md -> gpumd_nep89_relax 0.57; surrogate -> archive_mp 0.50; gpumd_nep89_md -> archive_mp 0.21
- split_2_2_3|fixed|move: most frequent moves lammps_meam_md -> archive_mp+mace_relax 0.15; surrogate -> archive_mp+lammps_meam_md+mace_relax 0.13; surrogate -> archive_mp+mace_relax 0.12; explorer -> gpumd_nep89_md+gpumd_nep89_relax 0.06
- split_2_2_3|fixed|move learned: most frequent moves surrogate -> archive_mp+mace_relax 0.13; lammps_meam_md -> archive_mp+mace_relax 0.07; surrogate -> archive_mp+lammps_meam_md+mace_relax 0.06; surrogate -> gpumd_nep89_md+gpumd_nep89_relax 0.05
- split_2_2_3|fixed|move+share: most frequent moves lammps_meam_md -> archive_mp+mace_relax 0.16; surrogate -> archive_mp+lammps_meam_md+mace_relax 0.14; surrogate -> archive_mp+mace_relax 0.12; explorer -> gpumd_nep89_md+gpumd_nep89_relax 0.06
- split_2_2_3|fixed|move+share learned: most frequent moves surrogate -> archive_mp+mace_relax 0.28; lammps_meam_md -> archive_mp+mace_relax+surrogate 0.20; lammps_meam_md -> archive_mp+mace_relax 0.14; surrogate -> archive_mp+lammps_meam_md+mace_relax 0.08
- split_2_2_3|full|move: most frequent moves mace_relax -> archive_mp 0.36; lammps_meam_md -> surrogate 0.15; surrogate -> lammps_meam_md 0.05; explorer -> archive_mp+mace_relax 0.04
- split_2_2_3|full|move+share: most frequent moves mace_relax -> archive_mp 0.36; lammps_meam_md -> surrogate 0.16; surrogate -> lammps_meam_md 0.05; explorer -> archive_mp+mace_relax 0.04
- split_2_2_3|merge_only|move: most frequent moves lammps_meam_md -> archive_mp+mace_relax 0.18; surrogate -> archive_mp+lammps_meam_md+mace_relax 0.16; surrogate -> archive_mp+mace_relax 0.15; surrogate -> gpumd_nep89_md+gpumd_nep89_relax 0.09
- split_2_2_3|merge_only|move+share: most frequent moves lammps_meam_md -> archive_mp+mace_relax 0.18; surrogate -> archive_mp+lammps_meam_md+mace_relax 0.16; surrogate -> archive_mp+mace_relax 0.15; surrogate -> gpumd_nep89_md+gpumd_nep89_relax 0.10
- split_2_5w|fixed|move: most frequent moves gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.71; explorer -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.04
- split_2_5w|fixed|move learned: most frequent moves gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.66; explorer -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.03
- split_2_5w|fixed|move+share: most frequent moves gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.71; explorer -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.04
- split_2_5w|fixed|move+share learned: most frequent moves gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.78; explorer -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.03
- split_2_5w|full|move: most frequent moves mace_relax -> lammps_meam_md 0.25; gpumd_nep89_md -> lammps_meam_md 0.16; surrogate -> archive_mp 0.15; lammps_meam_md -> archive_mp+mace_relax+surrogate 0.13
- split_2_5w|full|move+share: most frequent moves mace_relax -> lammps_meam_md 0.22; gpumd_nep89_md -> lammps_meam_md 0.17; surrogate -> archive_mp 0.15; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.12
- split_2_5w|merge_only|move: most frequent moves gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.83; explorer -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.01
- split_2_5w|merge_only|move+share: most frequent moves gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.83; explorer -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.01
- split_4_3|fixed|move: most frequent moves mace_relax -> archive_mp+gpumd_nep89_relax+surrogate 0.07; lammps_meam_md -> archive_mp+gpumd_nep89_relax+surrogate 0.04; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+surrogate 0.04; mace_relax -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+surrogate 0.03
- split_4_3|fixed|move learned: most frequent moves mace_relax -> archive_mp+gpumd_nep89_relax+surrogate 0.06; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+surrogate 0.02; lammps_meam_md -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+surrogate 0.01; explorer -> archive_mp+gpumd_nep89_relax+surrogate 0.01
- split_4_3|fixed|move+share: most frequent moves mace_relax -> archive_mp+gpumd_nep89_relax+surrogate 0.11; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+surrogate 0.03; lammps_meam_md -> archive_mp+gpumd_nep89_relax+surrogate 0.03; mace_relax -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+surrogate 0.03
- split_4_3|fixed|move+share learned: most frequent moves mace_relax -> archive_mp+gpumd_nep89_relax+surrogate 0.12; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+surrogate 0.07; mace_relax -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+surrogate 0.05; mace_relax -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+surrogate 0.03
- split_4_3|full|move: most frequent moves mace_relax -> gpumd_nep89_md 0.38; archive_mp -> surrogate 0.35; mace_relax -> lammps_meam_md 0.21; lammps_meam_md -> gpumd_nep89_md 0.18
- split_4_3|full|move+share: most frequent moves mace_relax -> gpumd_nep89_md 0.37; archive_mp -> surrogate 0.37; mace_relax -> lammps_meam_md 0.23; lammps_meam_md -> gpumd_nep89_md 0.21
- split_4_3|merge_only|move: most frequent moves gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+surrogate 0.09; mace_relax -> archive_mp+gpumd_nep89_relax+surrogate 0.08; lammps_meam_md -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+mace_relax+surrogate 0.03; lammps_meam_md -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+surrogate 0.03
- split_4_3|merge_only|move+share: most frequent moves mace_relax -> archive_mp+gpumd_nep89_relax+surrogate 0.09; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+surrogate 0.08; lammps_meam_md -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+surrogate 0.04; mace_relax -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+surrogate 0.03

## Receiver gpaw_r2scan

| start | swarm mode | member rule | value | minus rule none | moves | mean shared members at 25% |
|---|---|---|---|---|---|---|
| one_7 | fixed | move | 0.468 [0.455, 0.479] | +0.000 [+0.000, +0.000] | 0.00 | 0.00 |
| one_7 | fixed | move learned | 0.468 [0.455, 0.479] | +0.000 [+0.000, +0.000] | 0.00 | 0.00 |
| one_7 | fixed | move+share | 0.468 [0.455, 0.479] | +0.000 [+0.000, +0.000] | 0.00 | 0.00 |
| one_7 | fixed | move+share learned | 0.468 [0.455, 0.479] | +0.000 [+0.000, +0.000] | 0.00 | 0.00 |
| one_7 | fixed | none | 0.468 [0.455, 0.479] |  | 0.00 | 0.00 |
| one_7 | fixed | share | 0.468 [0.455, 0.479] | +0.000 [+0.000, +0.000] | 0.00 | 0.00 |
| one_7 | fixed | share learned | 0.468 [0.455, 0.479] | +0.000 [+0.000, +0.000] | 0.00 | 0.00 |
| one_7 | full | move | 0.453 [0.441, 0.465] | -0.000 [-0.002, +0.001] | 0.40 | 0.00 |
| one_7 | full | move+share | 0.456 [0.443, 0.467] | +0.002 [+0.000, +0.005] | 0.45 | 1.43 |
| one_7 | full | none | 0.454 [0.441, 0.465] |  | 0.00 | 0.00 |
| one_7 | full | share | 0.456 [0.444, 0.467] | +0.002 [+0.000, +0.004] | 0.00 | 1.86 |
| split_1x7 | fixed | move | 0.485 [0.477, 0.494] | +0.026 [+0.015, +0.036] | 3.80 | 0.00 |
| split_1x7 | fixed | move learned | 0.487 [0.478, 0.496] | +0.027 [+0.017, +0.038] | 3.62 | 0.00 |
| split_1x7 | fixed | move+share | 0.487 [0.478, 0.496] | +0.028 [+0.017, +0.038] | 3.77 | 0.43 |
| split_1x7 | fixed | move+share learned | 0.489 [0.480, 0.498] | +0.029 [+0.019, +0.040] | 3.88 | 2.49 |
| split_1x7 | fixed | none | 0.459 [0.453, 0.467] |  | 0.00 | 0.00 |
| split_1x7 | fixed | share | 0.462 [0.455, 0.469] | +0.003 [-0.001, +0.006] | 0.00 | 0.89 |
| split_1x7 | fixed | share learned | 0.478 [0.471, 0.486] | +0.019 [+0.013, +0.025] | 0.00 | 2.42 |
| split_1x7 | full | move | 0.490 [0.480, 0.501] | +0.013 [+0.001, +0.025] | 4.44 | 0.00 |
| split_1x7 | full | move+share | 0.492 [0.482, 0.502] | +0.014 [+0.002, +0.027] | 4.46 | 0.49 |
| split_1x7 | full | none | 0.478 [0.470, 0.485] |  | 0.00 | 0.00 |
| split_1x7 | full | share | 0.478 [0.471, 0.486] | +0.001 [-0.000, +0.002] | 0.00 | 0.94 |
| split_1x7 | merge_only | move | 0.481 [0.472, 0.491] | +0.004 [-0.007, +0.016] | 3.90 | 0.00 |
| split_1x7 | merge_only | move+share | 0.483 [0.474, 0.493] | +0.006 [-0.005, +0.018] | 3.89 | 0.59 |
| split_1x7 | merge_only | none | 0.477 [0.470, 0.484] |  | 0.00 | 0.00 |
| split_1x7 | merge_only | share | 0.477 [0.469, 0.484] | -0.000 [-0.001, +0.000] | 0.00 | 1.12 |
| split_2_2_3 | fixed | move | 0.537 [0.525, 0.549] | +0.003 [-0.003, +0.008] | 0.75 | 0.00 |
| split_2_2_3 | fixed | move learned | 0.536 [0.524, 0.549] | +0.002 [-0.002, +0.007] | 0.46 | 0.00 |
| split_2_2_3 | fixed | move+share | 0.536 [0.524, 0.549] | +0.002 [-0.003, +0.008] | 0.79 | 0.15 |
| split_2_2_3 | fixed | move+share learned | 0.557 [0.546, 0.568] | +0.023 [+0.012, +0.033] | 0.75 | 2.02 |
| split_2_2_3 | fixed | none | 0.534 [0.522, 0.546] |  | 0.00 | 0.00 |
| split_2_2_3 | fixed | share | 0.535 [0.522, 0.548] | +0.001 [-0.003, +0.005] | 0.00 | 0.35 |
| split_2_2_3 | fixed | share learned | 0.558 [0.548, 0.569] | +0.024 [+0.013, +0.035] | 0.00 | 2.43 |
| split_2_2_3 | full | move | 0.542 [0.529, 0.554] | +0.001 [-0.001, +0.003] | 0.76 | 0.00 |
| split_2_2_3 | full | move+share | 0.542 [0.529, 0.555] | +0.002 [-0.002, +0.006] | 0.80 | 1.23 |
| split_2_2_3 | full | none | 0.540 [0.527, 0.553] |  | 0.00 | 0.00 |
| split_2_2_3 | full | share | 0.542 [0.528, 0.554] | +0.001 [-0.003, +0.005] | 0.00 | 1.66 |
| split_2_2_3 | merge_only | move | 0.550 [0.539, 0.561] | -0.001 [-0.007, +0.005] | 0.83 | 0.00 |
| split_2_2_3 | merge_only | move+share | 0.549 [0.538, 0.560] | -0.002 [-0.008, +0.004] | 0.83 | 0.64 |
| split_2_2_3 | merge_only | none | 0.551 [0.540, 0.563] |  | 0.00 | 0.00 |
| split_2_2_3 | merge_only | share | 0.553 [0.542, 0.565] | +0.002 [-0.004, +0.008] | 0.00 | 0.98 |
| split_2_5w | fixed | move | 0.486 [0.473, 0.499] | -0.001 [-0.005, +0.003] | 0.75 | 0.00 |
| split_2_5w | fixed | move learned | 0.484 [0.471, 0.497] | -0.003 [-0.006, +0.000] | 0.67 | 0.00 |
| split_2_5w | fixed | move+share | 0.486 [0.473, 0.499] | -0.001 [-0.005, +0.003] | 0.75 | 0.00 |
| split_2_5w | fixed | move+share learned | 0.489 [0.476, 0.502] | +0.002 [-0.003, +0.007] | 0.67 | 0.44 |
| split_2_5w | fixed | none | 0.487 [0.473, 0.500] |  | 0.00 | 0.00 |
| split_2_5w | fixed | share | 0.487 [0.473, 0.500] | -0.000 [-0.001, +0.001] | 0.00 | 0.18 |
| split_2_5w | fixed | share learned | 0.492 [0.479, 0.506] | +0.005 [+0.001, +0.009] | 0.00 | 1.88 |
| split_2_5w | full | move | 0.467 [0.454, 0.479] | +0.005 [-0.001, +0.011] | 2.09 | 0.00 |
| split_2_5w | full | move+share | 0.467 [0.454, 0.479] | +0.005 [-0.001, +0.011] | 2.06 | 1.41 |
| split_2_5w | full | none | 0.462 [0.449, 0.474] |  | 0.00 | 0.00 |
| split_2_5w | full | share | 0.461 [0.449, 0.473] | -0.001 [-0.003, +0.002] | 0.00 | 1.97 |
| split_2_5w | merge_only | move | 0.489 [0.476, 0.503] | -0.002 [-0.007, +0.002] | 0.82 | 0.00 |
| split_2_5w | merge_only | move+share | 0.489 [0.476, 0.503] | -0.002 [-0.007, +0.002] | 0.82 | 0.00 |
| split_2_5w | merge_only | none | 0.491 [0.478, 0.505] |  | 0.00 | 0.00 |
| split_2_5w | merge_only | share | 0.491 [0.477, 0.505] | -0.000 [-0.001, +0.001] | 0.00 | 0.26 |
| split_4_3 | fixed | move | 0.464 [0.452, 0.477] | +0.001 [-0.000, +0.002] | 0.11 | 0.00 |
| split_4_3 | fixed | move learned | 0.464 [0.452, 0.476] | -0.000 [-0.001, +0.001] | 0.08 | 0.00 |
| split_4_3 | fixed | move+share | 0.464 [0.452, 0.477] | +0.000 [-0.002, +0.003] | 0.11 | 0.35 |
| split_4_3 | fixed | move+share learned | 0.469 [0.457, 0.482] | +0.006 [-0.000, +0.011] | 0.10 | 1.62 |
| split_4_3 | fixed | none | 0.464 [0.452, 0.476] |  | 0.00 | 0.00 |
| split_4_3 | fixed | share | 0.464 [0.452, 0.477] | +0.000 [-0.002, +0.002] | 0.00 | 0.45 |
| split_4_3 | fixed | share learned | 0.471 [0.459, 0.483] | +0.007 [+0.001, +0.013] | 0.00 | 1.71 |
| split_4_3 | full | move | 0.449 [0.439, 0.459] | -0.005 [-0.011, -0.000] | 2.07 | 0.00 |
| split_4_3 | full | move+share | 0.455 [0.444, 0.466] | +0.001 [-0.006, +0.007] | 2.12 | 1.44 |
| split_4_3 | full | none | 0.454 [0.444, 0.465] |  | 0.00 | 0.00 |
| split_4_3 | full | share | 0.456 [0.445, 0.467] | +0.001 [-0.003, +0.005] | 0.00 | 1.76 |
| split_4_3 | merge_only | move | 0.472 [0.460, 0.485] | +0.000 [-0.001, +0.001] | 0.17 | 0.00 |
| split_4_3 | merge_only | move+share | 0.472 [0.460, 0.484] | +0.000 [-0.002, +0.002] | 0.20 | 0.33 |
| split_4_3 | merge_only | none | 0.472 [0.460, 0.484] |  | 0.00 | 0.00 |
| split_4_3 | merge_only | share | 0.472 [0.460, 0.485] | +0.000 [-0.002, +0.002] | 0.00 | 0.72 |

- one_7|full|move: most frequent moves surrogate -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+mace_relax 0.07; gpumd_nep89_md -> gpumd_nep89_relax 0.05; gpumd_nep89_relax -> gpumd_nep89_md 0.03; lammps_meam_md -> gpumd_nep89_md 0.02
- one_7|full|move+share: most frequent moves gpumd_nep89_md -> gpumd_nep89_relax 0.05; gpumd_nep89_relax -> gpumd_nep89_md 0.05; surrogate -> lammps_meam_md 0.04; surrogate -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+mace_relax 0.04
- split_1x7|fixed|move: most frequent moves mace_relax -> lammps_meam_md 0.90; gpumd_nep89_md -> gpumd_nep89_relax 0.78; surrogate -> archive_mp 0.49; archive_mp -> surrogate 0.28
- split_1x7|fixed|move learned: most frequent moves mace_relax -> lammps_meam_md 0.90; gpumd_nep89_md -> gpumd_nep89_relax 0.78; surrogate -> archive_mp 0.49; archive_mp -> surrogate 0.28
- split_1x7|fixed|move+share: most frequent moves mace_relax -> lammps_meam_md 0.90; gpumd_nep89_md -> gpumd_nep89_relax 0.78; surrogate -> archive_mp 0.49; archive_mp -> surrogate 0.28
- split_1x7|fixed|move+share learned: most frequent moves mace_relax -> lammps_meam_md 0.90; gpumd_nep89_md -> gpumd_nep89_relax 0.79; surrogate -> archive_mp 0.45; archive_mp -> surrogate 0.27
- split_1x7|full|move: most frequent moves mace_relax -> lammps_meam_md 1.06; gpumd_nep89_md -> gpumd_nep89_relax 0.72; surrogate -> archive_mp 0.52; archive_mp -> surrogate 0.35
- split_1x7|full|move+share: most frequent moves mace_relax -> lammps_meam_md 1.05; gpumd_nep89_md -> gpumd_nep89_relax 0.72; surrogate -> archive_mp 0.52; archive_mp -> surrogate 0.35
- split_1x7|merge_only|move: most frequent moves mace_relax -> lammps_meam_md 0.90; gpumd_nep89_md -> gpumd_nep89_relax 0.73; surrogate -> archive_mp 0.46; archive_mp -> surrogate 0.28
- split_1x7|merge_only|move+share: most frequent moves mace_relax -> lammps_meam_md 0.91; gpumd_nep89_md -> gpumd_nep89_relax 0.73; surrogate -> archive_mp 0.46; archive_mp -> surrogate 0.28
- split_2_2_3|fixed|move: most frequent moves surrogate -> archive_mp+mace_relax 0.14; surrogate -> gpumd_nep89_md+gpumd_nep89_relax 0.11; lammps_meam_md -> archive_mp+mace_relax 0.11; surrogate -> archive_mp+lammps_meam_md+mace_relax 0.10
- split_2_2_3|fixed|move learned: most frequent moves surrogate -> archive_mp+mace_relax 0.11; surrogate -> gpumd_nep89_md+gpumd_nep89_relax 0.07; lammps_meam_md -> archive_mp+mace_relax 0.07; surrogate -> archive_mp+lammps_meam_md+mace_relax 0.07
- split_2_2_3|fixed|move+share: most frequent moves surrogate -> archive_mp+mace_relax 0.15; lammps_meam_md -> archive_mp+mace_relax 0.12; surrogate -> gpumd_nep89_md+gpumd_nep89_relax 0.11; surrogate -> archive_mp+lammps_meam_md+mace_relax 0.11
- split_2_2_3|fixed|move+share learned: most frequent moves lammps_meam_md -> archive_mp+mace_relax 0.21; surrogate -> archive_mp+mace_relax 0.12; surrogate -> gpumd_nep89_md+gpumd_nep89_relax 0.10; surrogate -> archive_mp+lammps_meam_md+mace_relax 0.10
- split_2_2_3|full|move: most frequent moves mace_relax -> archive_mp 0.32; surrogate -> lammps_meam_md 0.12; lammps_meam_md -> surrogate 0.05; explorer -> lammps_meam_md+surrogate 0.04
- split_2_2_3|full|move+share: most frequent moves mace_relax -> archive_mp 0.29; surrogate -> lammps_meam_md 0.13; lammps_meam_md -> surrogate 0.06; surrogate -> archive_mp+mace_relax 0.05
- split_2_2_3|merge_only|move: most frequent moves surrogate -> archive_mp+mace_relax 0.15; lammps_meam_md -> archive_mp+mace_relax 0.12; surrogate -> archive_mp+lammps_meam_md+mace_relax 0.10; lammps_meam_md -> archive_mp+mace_relax+surrogate 0.10
- split_2_2_3|merge_only|move+share: most frequent moves surrogate -> archive_mp+mace_relax 0.15; lammps_meam_md -> archive_mp+mace_relax 0.13; surrogate -> archive_mp+lammps_meam_md+mace_relax 0.11; lammps_meam_md -> archive_mp+mace_relax+surrogate 0.08
- split_2_5w|fixed|move: most frequent moves gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.67; explorer -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.03; mace_relax -> gpumd_nep89_md 0.02; gpumd_nep89_md -> archive_mp+explorer+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.01
- split_2_5w|fixed|move learned: most frequent moves gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.67
- split_2_5w|fixed|move+share: most frequent moves gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.67; explorer -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.03; mace_relax -> gpumd_nep89_md 0.02; gpumd_nep89_md -> archive_mp+explorer+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.01
- split_2_5w|fixed|move+share learned: most frequent moves gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.65; archive_mp -> explorer+gpumd_nep89_md 0.01; gpumd_nep89_relax -> archive_mp+explorer+gpumd_nep89_md 0.01
- split_2_5w|full|move: most frequent moves archive_mp -> gpumd_nep89_relax 0.29; mace_relax -> lammps_meam_md 0.22; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.17; surrogate -> archive_mp 0.11
- split_2_5w|full|move+share: most frequent moves archive_mp -> gpumd_nep89_relax 0.32; mace_relax -> lammps_meam_md 0.24; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.17; surrogate -> archive_mp 0.12
- split_2_5w|merge_only|move: most frequent moves gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.72; explorer -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.03; mace_relax -> gpumd_nep89_md 0.02; mace_relax -> explorer+gpumd_nep89_md 0.01
- split_2_5w|merge_only|move+share: most frequent moves gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.72; explorer -> archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate 0.03; mace_relax -> gpumd_nep89_md 0.02; mace_relax -> explorer+gpumd_nep89_md 0.01
- split_4_3|fixed|move: most frequent moves mace_relax -> archive_mp+gpumd_nep89_relax+surrogate 0.05; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+surrogate 0.01; lammps_meam_md -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+surrogate 0.01; mace_relax -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+surrogate 0.01
- split_4_3|fixed|move learned: most frequent moves mace_relax -> archive_mp+gpumd_nep89_relax+surrogate 0.05; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+surrogate 0.01; lammps_meam_md -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+surrogate 0.01; mace_relax -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+surrogate 0.01
- split_4_3|fixed|move+share: most frequent moves mace_relax -> archive_mp+gpumd_nep89_relax+surrogate 0.06; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+surrogate 0.01; lammps_meam_md -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+surrogate 0.01; explorer -> archive_mp+gpumd_nep89_relax+surrogate 0.01
- split_4_3|fixed|move+share learned: most frequent moves mace_relax -> archive_mp+gpumd_nep89_relax+surrogate 0.03; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+surrogate 0.02; mace_relax -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+surrogate 0.01; lammps_meam_md -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+mace_relax+surrogate 0.01
- split_4_3|full|move: most frequent moves mace_relax -> gpumd_nep89_md 0.41; archive_mp -> surrogate 0.24; mace_relax -> lammps_meam_md 0.22; lammps_meam_md -> gpumd_nep89_md 0.19
- split_4_3|full|move+share: most frequent moves mace_relax -> gpumd_nep89_md 0.42; archive_mp -> surrogate 0.26; mace_relax -> lammps_meam_md 0.23; lammps_meam_md -> gpumd_nep89_md 0.20
- split_4_3|merge_only|move: most frequent moves mace_relax -> archive_mp+gpumd_nep89_relax+surrogate 0.10; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+surrogate 0.02; lammps_meam_md -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+surrogate 0.02; lammps_meam_md -> archive_mp+gpumd_nep89_relax+surrogate 0.01
- split_4_3|merge_only|move+share: most frequent moves mace_relax -> archive_mp+gpumd_nep89_relax+surrogate 0.11; gpumd_nep89_md -> archive_mp+gpumd_nep89_relax+surrogate 0.03; lammps_meam_md -> archive_mp+gpumd_nep89_md+gpumd_nep89_relax+surrogate 0.03; lammps_meam_md -> archive_mp+gpumd_nep89_relax+surrogate 0.01

## Credit with moving or shared members

### qe_pbe|split_2_2_3|fixed|share
v(all) 0.650, v(empty) 0.107, efficiency gap 7.8e-16
| body | Shapley | averaged level value | difference [5, 95] |
|---|---|---|---|
| mace_relax | +0.159 | +0.163 | +0.004 [-0.019, +0.027] |
| archive_mp | +0.177 | +0.160 | -0.017 [-0.037, +0.004] |
| gpumd_nep89_md | +0.082 | +0.105 | +0.023 [+0.001, +0.043] |
| gpumd_nep89_relax | +0.067 | +0.060 | -0.007 [-0.026, +0.015] |
| lammps_meam_md | +0.058 | +0.064 | +0.006 [-0.026, +0.027] |
| surrogate | +0.020 | +0.023 | +0.003 [-0.020, +0.026] |
| explorer | -0.021 | -0.032 | -0.011 [-0.035, +0.015] |

Most occupied structures (share of early-window compute; second memberships after //):
- 0.82: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.04: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax // lammps_meam_md also in archive_mp+mace_relax; surrogate also in archive_mp+mace_relax
- 0.03: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax // lammps_meam_md also in archive_mp+mace_relax
- 0.03: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax // surrogate also in archive_mp+mace_relax
- 0.02: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax // lammps_meam_md also in archive_mp+mace_relax; mace_relax also in explorer+lammps_meam_md+surrogate; surrogate also in archive_mp+mace_relax
- 0.01: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax // archive_mp also in explorer+lammps_meam_md+surrogate; lammps_meam_md also in archive_mp+mace_relax; mace_relax also in explorer+lammps_meam_md+surrogate; surrogate also in archive_mp+mace_relax
- 0.01: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax // lammps_meam_md also in gpumd_nep89_md+gpumd_nep89_relax; surrogate also in gpumd_nep89_md+gpumd_nep89_relax
- 0.01: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax // surrogate also in gpumd_nep89_md+gpumd_nep89_relax

### qe_pbe|split_4_3|fixed|share
v(all) 0.637, v(empty) 0.107, efficiency gap 1.6e-15
| body | Shapley | averaged level value | difference [5, 95] |
|---|---|---|---|
| mace_relax | +0.216 | +0.219 | +0.003 [-0.028, +0.030] |
| gpumd_nep89_md | +0.084 | +0.068 | -0.016 [-0.042, +0.006] |
| lammps_meam_md | +0.031 | +0.013 | -0.017 [-0.041, +0.009] |
| explorer | -0.051 | -0.054 | -0.002 [-0.022, +0.021] |
| archive_mp | +0.181 | +0.199 | +0.019 [-0.010, +0.046] |
| gpumd_nep89_relax | +0.051 | +0.065 | +0.014 [-0.013, +0.047] |
| surrogate | +0.020 | +0.019 | -0.001 [-0.036, +0.023] |

Most occupied structures (share of early-window compute; second memberships after //):
- 0.81: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.06: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // mace_relax also in archive_mp+gpumd_nep89_relax+surrogate
- 0.02: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // archive_mp also in explorer+gpumd_nep89_md+lammps_meam_md+mace_relax; mace_relax also in archive_mp+gpumd_nep89_relax+surrogate
- 0.02: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // gpumd_nep89_md also in archive_mp+gpumd_nep89_relax+surrogate; lammps_meam_md also in archive_mp+gpumd_nep89_relax+surrogate; mace_relax also in archive_mp+gpumd_nep89_relax+surrogate
- 0.01: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // gpumd_nep89_md also in archive_mp+gpumd_nep89_relax+surrogate
- 0.01: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // mace_relax also in archive_mp+gpumd_nep89_relax+surrogate; surrogate also in explorer+gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.01: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // archive_mp also in explorer+gpumd_nep89_md+lammps_meam_md+mace_relax; gpumd_nep89_md also in archive_mp+gpumd_nep89_relax+surrogate; lammps_meam_md also in archive_mp+gpumd_nep89_relax+surrogate; mace_relax also in archive_mp+gpumd_nep89_relax+surrogate
- 0.01: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // gpumd_nep89_md also in archive_mp+gpumd_nep89_relax+surrogate; lammps_meam_md also in archive_mp+gpumd_nep89_relax+surrogate

### qe_pbe|split_4_3|fixed|move
v(all) 0.633, v(empty) 0.107, efficiency gap 1.6e-15
| body | Shapley | averaged level value | difference [5, 95] |
|---|---|---|---|
| mace_relax | +0.216 | +0.216 | -0.000 [-0.025, +0.027] |
| gpumd_nep89_md | +0.085 | +0.076 | -0.009 [-0.033, +0.019] |
| lammps_meam_md | +0.029 | +0.009 | -0.020 [-0.046, +0.006] |
| explorer | -0.053 | -0.057 | -0.003 [-0.023, +0.020] |
| archive_mp | +0.179 | +0.198 | +0.018 [-0.016, +0.047] |
| gpumd_nep89_relax | +0.053 | +0.067 | +0.014 [-0.015, +0.051] |
| surrogate | +0.018 | +0.018 | +0.000 [-0.036, +0.035] |

Most occupied structures (share of early-window compute; second memberships after //):
- 0.93: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.05: archive_mp+gpumd_nep89_relax+mace_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md
- 0.01: archive_mp+gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate || explorer
- 0.01: archive_mp+gpumd_nep89_md+gpumd_nep89_relax+mace_relax+surrogate || explorer+lammps_meam_md
- 0.00: archive_mp+gpumd_nep89_relax+lammps_meam_md+surrogate || explorer+gpumd_nep89_md+mace_relax
- 0.00: archive_mp+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate || explorer+gpumd_nep89_md
- 0.00: archive_mp+gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+surrogate || explorer+mace_relax

### qe_pbe|split_2_2_3|fixed|move
v(all) 0.638, v(empty) 0.107, efficiency gap 8.9e-16
| body | Shapley | averaged level value | difference [5, 95] |
|---|---|---|---|
| mace_relax | +0.163 | +0.154 | -0.009 [-0.037, +0.012] |
| archive_mp | +0.173 | +0.158 | -0.015 [-0.032, +0.003] |
| gpumd_nep89_md | +0.087 | +0.107 | +0.020 [-0.013, +0.051] |
| gpumd_nep89_relax | +0.062 | +0.060 | -0.002 [-0.021, +0.024] |
| lammps_meam_md | +0.060 | +0.071 | +0.011 [-0.023, +0.038] |
| surrogate | +0.016 | +0.014 | -0.001 [-0.029, +0.018] |
| explorer | -0.031 | -0.033 | -0.003 [-0.027, +0.026] |

Most occupied structures (share of early-window compute; second memberships after //):
- 0.56: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.20: archive_mp+lammps_meam_md+mace_relax+surrogate || explorer || gpumd_nep89_md+gpumd_nep89_relax
- 0.10: archive_mp+mace_relax+surrogate || explorer+lammps_meam_md || gpumd_nep89_md+gpumd_nep89_relax
- 0.05: archive_mp+explorer+mace_relax || gpumd_nep89_md+gpumd_nep89_relax || lammps_meam_md+surrogate
- 0.03: archive_mp+mace_relax || explorer+lammps_meam_md || gpumd_nep89_md+gpumd_nep89_relax+surrogate
- 0.02: archive_mp+mace_relax || explorer || gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+surrogate
- 0.02: archive_mp+mace_relax || explorer+gpumd_nep89_md+gpumd_nep89_relax || lammps_meam_md+surrogate
- 0.01: archive_mp+mace_relax+surrogate || explorer || gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md

### qe_pbe|split_4_3|fixed|move+share
v(all) 0.636, v(empty) 0.107, efficiency gap 1.6e-15
| body | Shapley | averaged level value | difference [5, 95] |
|---|---|---|---|
| mace_relax | +0.217 | +0.216 | -0.001 [-0.025, +0.024] |
| gpumd_nep89_md | +0.085 | +0.079 | -0.006 [-0.032, +0.031] |
| lammps_meam_md | +0.029 | +0.012 | -0.017 [-0.045, +0.007] |
| explorer | -0.054 | -0.056 | -0.002 [-0.023, +0.023] |
| archive_mp | +0.180 | +0.195 | +0.015 [-0.017, +0.046] |
| gpumd_nep89_relax | +0.053 | +0.065 | +0.012 [-0.015, +0.048] |
| surrogate | +0.019 | +0.017 | -0.001 [-0.034, +0.034] |

Most occupied structures (share of early-window compute; second memberships after //):
- 0.78: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.04: archive_mp+gpumd_nep89_relax+mace_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md
- 0.03: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // mace_relax also in archive_mp+gpumd_nep89_relax+surrogate
- 0.02: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // archive_mp also in explorer+gpumd_nep89_md+lammps_meam_md+mace_relax; mace_relax also in archive_mp+gpumd_nep89_relax+surrogate
- 0.02: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // gpumd_nep89_md also in archive_mp+gpumd_nep89_relax+surrogate; lammps_meam_md also in archive_mp+gpumd_nep89_relax+surrogate; mace_relax also in archive_mp+gpumd_nep89_relax+surrogate
- 0.01: archive_mp+gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate || explorer
- 0.01: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // gpumd_nep89_md also in archive_mp+gpumd_nep89_relax+surrogate
- 0.01: archive_mp+gpumd_nep89_md+gpumd_nep89_relax+mace_relax+surrogate || explorer+lammps_meam_md

### qe_pbe|split_2_2_3|fixed|move+share
v(all) 0.639, v(empty) 0.107, efficiency gap 8.9e-16
| body | Shapley | averaged level value | difference [5, 95] |
|---|---|---|---|
| mace_relax | +0.163 | +0.153 | -0.010 [-0.037, +0.012] |
| archive_mp | +0.173 | +0.158 | -0.015 [-0.031, +0.006] |
| gpumd_nep89_md | +0.087 | +0.106 | +0.019 [-0.013, +0.051] |
| gpumd_nep89_relax | +0.063 | +0.061 | -0.002 [-0.020, +0.020] |
| lammps_meam_md | +0.060 | +0.072 | +0.011 [-0.023, +0.035] |
| surrogate | +0.016 | +0.015 | -0.002 [-0.029, +0.019] |
| explorer | -0.031 | -0.034 | -0.003 [-0.027, +0.026] |

Most occupied structures (share of early-window compute; second memberships after //):
- 0.56: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.18: archive_mp+lammps_meam_md+mace_relax+surrogate || explorer || gpumd_nep89_md+gpumd_nep89_relax
- 0.10: archive_mp+mace_relax+surrogate || explorer+lammps_meam_md || gpumd_nep89_md+gpumd_nep89_relax
- 0.05: archive_mp+explorer+mace_relax || gpumd_nep89_md+gpumd_nep89_relax || lammps_meam_md+surrogate
- 0.02: archive_mp+mace_relax || explorer+gpumd_nep89_md+gpumd_nep89_relax || lammps_meam_md+surrogate
- 0.02: archive_mp+mace_relax || explorer+lammps_meam_md || gpumd_nep89_md+gpumd_nep89_relax+surrogate
- 0.02: archive_mp+mace_relax || explorer || gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+surrogate
- 0.01: archive_mp+mace_relax || explorer || gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+surrogate // lammps_meam_md also in archive_mp+mace_relax; mace_relax also in gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+surrogate; surrogate also in archive_mp+mace_relax

### qe_pbe|split_4_3|merge_only|move+share
v(all) 0.637, v(empty) 0.107, efficiency gap 3.2e-15
| body | Shapley | averaged level value | difference [5, 95] |
|---|---|---|---|
| mace_relax | +0.216 | +0.217 | +0.001 [-0.028, +0.025] |
| gpumd_nep89_md | +0.087 | +0.079 | -0.008 [-0.026, +0.030] |
| lammps_meam_md | +0.030 | +0.011 | -0.020 [-0.040, +0.003] |
| explorer | -0.056 | -0.054 | +0.003 [-0.018, +0.030] |
| archive_mp | +0.182 | +0.195 | +0.013 [-0.021, +0.042] |
| gpumd_nep89_relax | +0.055 | +0.065 | +0.010 [-0.014, +0.042] |
| surrogate | +0.016 | +0.017 | +0.001 [-0.029, +0.029] |

Most occupied structures (share of early-window compute; second memberships after //):
- 0.50: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.22: archive_mp+gpumd_nep89_relax+surrogate > explorer+gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.04: archive_mp+gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate > explorer
- 0.04: archive_mp+explorer+gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate
- 0.03: archive_mp+gpumd_nep89_relax+mace_relax+surrogate > explorer+gpumd_nep89_md+lammps_meam_md
- 0.02: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // mace_relax also in archive_mp+gpumd_nep89_relax+surrogate
- 0.01: archive_mp+gpumd_nep89_relax+surrogate > explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // archive_mp also in explorer+gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.01: archive_mp+gpumd_nep89_relax+surrogate > explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // archive_mp also in explorer+gpumd_nep89_md+lammps_meam_md+mace_relax; gpumd_nep89_relax also in explorer+gpumd_nep89_md+lammps_meam_md+mace_relax

### qe_pbe|split_2_2_3|merge_only|move+share
v(all) 0.666, v(empty) 0.107, efficiency gap 5.6e-16
| body | Shapley | averaged level value | difference [5, 95] |
|---|---|---|---|
| mace_relax | +0.170 | +0.159 | -0.011 [-0.033, +0.007] |
| archive_mp | +0.180 | +0.162 | -0.018 [-0.043, -0.001] |
| gpumd_nep89_md | +0.098 | +0.111 | +0.014 [-0.011, +0.034] |
| gpumd_nep89_relax | +0.066 | +0.062 | -0.004 [-0.025, +0.017] |
| lammps_meam_md | +0.056 | +0.066 | +0.009 [-0.013, +0.032] |
| surrogate | +0.013 | +0.021 | +0.008 [-0.017, +0.044] |
| explorer | -0.024 | -0.022 | +0.001 [-0.028, +0.029] |

Most occupied structures (share of early-window compute; second memberships after //):
- 0.21: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.17: archive_mp+mace_relax > gpumd_nep89_md+gpumd_nep89_relax || explorer+lammps_meam_md+surrogate
- 0.13: archive_mp+mace_relax > explorer+lammps_meam_md+surrogate > gpumd_nep89_md+gpumd_nep89_relax
- 0.04: archive_mp+mace_relax > explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.03: archive_mp+lammps_meam_md+mace_relax+surrogate > explorer > gpumd_nep89_md+gpumd_nep89_relax
- 0.03: archive_mp+lammps_meam_md+mace_relax+surrogate > explorer > gpumd_nep89_md+gpumd_nep89_relax // archive_mp also in gpumd_nep89_md+gpumd_nep89_relax; gpumd_nep89_md also in archive_mp+lammps_meam_md+mace_relax+surrogate; gpumd_nep89_relax also in archive_mp+lammps_meam_md+mace_relax+surrogate; lammps_meam_md also in gpumd_nep89_md+gpumd_nep89_relax; mace_relax also in gpumd_nep89_md+gpumd_nep89_relax; surrogate also in gpumd_nep89_md+gpumd_nep89_relax
- 0.02: archive_mp+lammps_meam_md+mace_relax+surrogate > explorer > gpumd_nep89_md+gpumd_nep89_relax // gpumd_nep89_md also in archive_mp+lammps_meam_md+mace_relax+surrogate; gpumd_nep89_relax also in archive_mp+lammps_meam_md+mace_relax+surrogate
- 0.02: archive_mp+mace_relax > explorer+lammps_meam_md+surrogate > gpumd_nep89_md+gpumd_nep89_relax // gpumd_nep89_md also in archive_mp+mace_relax; gpumd_nep89_relax also in archive_mp+mace_relax

### qe_hse06|split_2_2_3|fixed|share
v(all) 0.537, v(empty) 0.120, efficiency gap 1.1e-15
| body | Shapley | averaged level value | difference [5, 95] |
|---|---|---|---|
| mace_relax | +0.182 | +0.164 | -0.018 [-0.059, +0.046] |
| archive_mp | +0.146 | +0.122 | -0.024 [-0.070, +0.040] |
| gpumd_nep89_md | +0.071 | +0.098 | +0.027 [-0.035, +0.081] |
| gpumd_nep89_relax | +0.001 | -0.042 | -0.043 [-0.097, +0.006] |
| lammps_meam_md | +0.024 | +0.056 | +0.032 [-0.029, +0.084] |
| surrogate | -0.002 | +0.011 | +0.013 [-0.044, +0.061] |
| explorer | -0.006 | +0.007 | +0.013 [-0.041, +0.060] |

Most occupied structures (share of early-window compute; second memberships after //):
- 0.93: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.03: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax // lammps_meam_md also in archive_mp+mace_relax
- 0.02: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax // surrogate also in archive_mp+mace_relax
- 0.01: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax // lammps_meam_md also in archive_mp+mace_relax; mace_relax also in explorer+lammps_meam_md+surrogate
- 0.01: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax // lammps_meam_md also in archive_mp+mace_relax; surrogate also in archive_mp+mace_relax
- 0.01: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax // lammps_meam_md also in gpumd_nep89_md+gpumd_nep89_relax; surrogate also in gpumd_nep89_md+gpumd_nep89_relax
- 0.00: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax // archive_mp also in explorer+lammps_meam_md+surrogate; lammps_meam_md also in archive_mp+mace_relax; mace_relax also in explorer+lammps_meam_md+surrogate; surrogate also in archive_mp+mace_relax
- 0.00: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax // lammps_meam_md also in archive_mp+mace_relax; mace_relax also in explorer+lammps_meam_md+surrogate; surrogate also in archive_mp+mace_relax

### qe_hse06|split_2_2_3|fixed|move
v(all) 0.528, v(empty) 0.120, efficiency gap 6.7e-16
| body | Shapley | averaged level value | difference [5, 95] |
|---|---|---|---|
| mace_relax | +0.180 | +0.151 | -0.029 [-0.077, +0.025] |
| archive_mp | +0.161 | +0.130 | -0.031 [-0.087, +0.028] |
| gpumd_nep89_md | +0.071 | +0.099 | +0.028 [-0.027, +0.083] |
| gpumd_nep89_relax | +0.002 | -0.034 | -0.036 [-0.096, +0.016] |
| lammps_meam_md | +0.029 | +0.062 | +0.033 [-0.020, +0.085] |
| surrogate | -0.015 | -0.001 | +0.014 [-0.045, +0.075] |
| explorer | -0.021 | +0.002 | +0.022 [-0.031, +0.070] |

Most occupied structures (share of early-window compute; second memberships after //):
- 0.79: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.06: archive_mp+mace_relax+surrogate || explorer+lammps_meam_md || gpumd_nep89_md+gpumd_nep89_relax
- 0.06: archive_mp+lammps_meam_md+mace_relax+surrogate || explorer || gpumd_nep89_md+gpumd_nep89_relax
- 0.04: archive_mp+lammps_meam_md+mace_relax || explorer+surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.03: archive_mp+mace_relax || explorer || gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+surrogate
- 0.03: archive_mp+mace_relax || explorer+gpumd_nep89_md+gpumd_nep89_relax || lammps_meam_md+surrogate
- 0.01: archive_mp+mace_relax+surrogate || explorer+gpumd_nep89_md+gpumd_nep89_relax || lammps_meam_md
- 0.00: archive_mp+gpumd_nep89_md+gpumd_nep89_relax+mace_relax || explorer || lammps_meam_md+surrogate

### qe_hse06|split_4_3|fixed|share
v(all) 0.458, v(empty) 0.120, efficiency gap 1.3e-15
| body | Shapley | averaged level value | difference [5, 95] |
|---|---|---|---|
| mace_relax | +0.187 | +0.191 | +0.004 [-0.044, +0.044] |
| gpumd_nep89_md | +0.054 | +0.032 | -0.022 [-0.060, +0.021] |
| lammps_meam_md | -0.034 | -0.068 | -0.034 [-0.072, -0.004] |
| explorer | -0.040 | -0.026 | +0.015 [-0.035, +0.052] |
| archive_mp | +0.183 | +0.213 | +0.031 [-0.029, +0.084] |
| gpumd_nep89_relax | -0.015 | -0.007 | +0.009 [-0.032, +0.067] |
| surrogate | +0.003 | +0.001 | -0.002 [-0.070, +0.049] |

Most occupied structures (share of early-window compute; second memberships after //):
- 0.90: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.02: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // gpumd_nep89_md also in archive_mp+gpumd_nep89_relax+surrogate; lammps_meam_md also in archive_mp+gpumd_nep89_relax+surrogate; mace_relax also in archive_mp+gpumd_nep89_relax+surrogate
- 0.02: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // gpumd_nep89_md also in archive_mp+gpumd_nep89_relax+surrogate; mace_relax also in archive_mp+gpumd_nep89_relax+surrogate
- 0.02: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // mace_relax also in archive_mp+gpumd_nep89_relax+surrogate
- 0.01: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // gpumd_nep89_md also in archive_mp+gpumd_nep89_relax+surrogate; lammps_meam_md also in archive_mp+gpumd_nep89_relax+surrogate
- 0.01: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // archive_mp also in explorer+gpumd_nep89_md+lammps_meam_md+mace_relax; mace_relax also in archive_mp+gpumd_nep89_relax+surrogate
- 0.01: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // archive_mp also in explorer+gpumd_nep89_md+lammps_meam_md+mace_relax; gpumd_nep89_md also in archive_mp+gpumd_nep89_relax+surrogate; lammps_meam_md also in archive_mp+gpumd_nep89_relax+surrogate
- 0.01: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // archive_mp also in explorer+gpumd_nep89_md+lammps_meam_md+mace_relax; gpumd_nep89_md also in archive_mp+gpumd_nep89_relax+surrogate; lammps_meam_md also in archive_mp+gpumd_nep89_relax+surrogate; mace_relax also in archive_mp+gpumd_nep89_relax+surrogate; surrogate also in explorer+gpumd_nep89_md+lammps_meam_md+mace_relax

### qe_hse06|split_2_2_3|fixed|move+share
v(all) 0.528, v(empty) 0.120, efficiency gap 1.3e-15
| body | Shapley | averaged level value | difference [5, 95] |
|---|---|---|---|
| mace_relax | +0.180 | +0.151 | -0.029 [-0.079, +0.025] |
| archive_mp | +0.161 | +0.130 | -0.031 [-0.087, +0.028] |
| gpumd_nep89_md | +0.071 | +0.099 | +0.028 [-0.028, +0.083] |
| gpumd_nep89_relax | +0.002 | -0.034 | -0.036 [-0.097, +0.016] |
| lammps_meam_md | +0.029 | +0.063 | +0.033 [-0.020, +0.085] |
| surrogate | -0.015 | -0.001 | +0.014 [-0.045, +0.077] |
| explorer | -0.021 | +0.000 | +0.021 [-0.031, +0.071] |

Most occupied structures (share of early-window compute; second memberships after //):
- 0.78: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.06: archive_mp+mace_relax+surrogate || explorer+lammps_meam_md || gpumd_nep89_md+gpumd_nep89_relax
- 0.06: archive_mp+lammps_meam_md+mace_relax+surrogate || explorer || gpumd_nep89_md+gpumd_nep89_relax
- 0.04: archive_mp+lammps_meam_md+mace_relax || explorer+surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.03: archive_mp+mace_relax || explorer || gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+surrogate
- 0.03: archive_mp+mace_relax || explorer+gpumd_nep89_md+gpumd_nep89_relax || lammps_meam_md+surrogate
- 0.01: archive_mp+mace_relax+surrogate || explorer+gpumd_nep89_md+gpumd_nep89_relax || lammps_meam_md
- 0.00: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax // lammps_meam_md also in archive_mp+mace_relax; surrogate also in archive_mp+mace_relax

### qe_hse06|split_4_3|fixed|move
v(all) 0.461, v(empty) 0.120, efficiency gap 2.1e-15
| body | Shapley | averaged level value | difference [5, 95] |
|---|---|---|---|
| mace_relax | +0.189 | +0.192 | +0.003 [-0.035, +0.045] |
| gpumd_nep89_md | +0.053 | +0.034 | -0.019 [-0.059, +0.032] |
| lammps_meam_md | -0.034 | -0.068 | -0.035 [-0.092, -0.006] |
| explorer | -0.039 | -0.024 | +0.014 [-0.025, +0.050] |
| archive_mp | +0.183 | +0.209 | +0.027 [-0.032, +0.075] |
| gpumd_nep89_relax | -0.015 | -0.003 | +0.012 [-0.031, +0.068] |
| surrogate | +0.003 | +0.000 | -0.003 [-0.071, +0.049] |

Most occupied structures (share of early-window compute; second memberships after //):
- 0.92: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.06: archive_mp+gpumd_nep89_relax+mace_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md
- 0.02: archive_mp+explorer+gpumd_nep89_relax+surrogate || gpumd_nep89_md+lammps_meam_md+mace_relax

### qe_hse06|split_2_2_3|merge_only|move+share
v(all) 0.543, v(empty) 0.120, efficiency gap 5.6e-16
| body | Shapley | averaged level value | difference [5, 95] |
|---|---|---|---|
| mace_relax | +0.183 | +0.155 | -0.028 [-0.075, +0.029] |
| archive_mp | +0.173 | +0.150 | -0.023 [-0.088, +0.029] |
| gpumd_nep89_md | +0.075 | +0.105 | +0.031 [-0.023, +0.102] |
| gpumd_nep89_relax | +0.008 | -0.023 | -0.032 [-0.106, +0.019] |
| lammps_meam_md | +0.025 | +0.058 | +0.033 [-0.015, +0.085] |
| surrogate | -0.023 | -0.016 | +0.008 [-0.049, +0.073] |
| explorer | -0.019 | -0.008 | +0.012 [-0.045, +0.062] |

Most occupied structures (share of early-window compute; second memberships after //):
- 0.40: archive_mp+mace_relax || explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.13: archive_mp+mace_relax > gpumd_nep89_md+gpumd_nep89_relax || explorer+lammps_meam_md+surrogate
- 0.07: archive_mp+mace_relax > explorer+lammps_meam_md+surrogate > gpumd_nep89_md+gpumd_nep89_relax
- 0.06: archive_mp+mace_relax > explorer+lammps_meam_md+surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.04: archive_mp+mace_relax+surrogate > explorer+lammps_meam_md > gpumd_nep89_md+gpumd_nep89_relax
- 0.03: archive_mp+lammps_meam_md+mace_relax || explorer+surrogate || gpumd_nep89_md+gpumd_nep89_relax
- 0.02: archive_mp+lammps_meam_md+mace_relax+surrogate > explorer > gpumd_nep89_md+gpumd_nep89_relax
- 0.02: archive_mp+lammps_meam_md+mace_relax+surrogate > gpumd_nep89_md+gpumd_nep89_relax || explorer

### qe_hse06|split_4_3|fixed|move+share
v(all) 0.457, v(empty) 0.120, efficiency gap 1.5e-15
| body | Shapley | averaged level value | difference [5, 95] |
|---|---|---|---|
| mace_relax | +0.188 | +0.192 | +0.004 [-0.034, +0.045] |
| gpumd_nep89_md | +0.053 | +0.036 | -0.016 [-0.059, +0.031] |
| lammps_meam_md | -0.034 | -0.066 | -0.032 [-0.085, -0.000] |
| explorer | -0.040 | -0.026 | +0.014 [-0.024, +0.047] |
| archive_mp | +0.182 | +0.206 | +0.024 [-0.032, +0.071] |
| gpumd_nep89_relax | -0.015 | -0.004 | +0.011 [-0.030, +0.067] |
| surrogate | +0.003 | -0.001 | -0.004 [-0.072, +0.048] |

Most occupied structures (share of early-window compute; second memberships after //):
- 0.83: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.06: archive_mp+gpumd_nep89_relax+mace_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md
- 0.02: archive_mp+explorer+gpumd_nep89_relax+surrogate || gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.02: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // gpumd_nep89_md also in archive_mp+gpumd_nep89_relax+surrogate; mace_relax also in archive_mp+gpumd_nep89_relax+surrogate
- 0.01: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // gpumd_nep89_md also in archive_mp+gpumd_nep89_relax+surrogate; lammps_meam_md also in archive_mp+gpumd_nep89_relax+surrogate; mace_relax also in archive_mp+gpumd_nep89_relax+surrogate
- 0.01: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // mace_relax also in archive_mp+gpumd_nep89_relax+surrogate
- 0.01: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // gpumd_nep89_md also in archive_mp+gpumd_nep89_relax+surrogate; lammps_meam_md also in archive_mp+gpumd_nep89_relax+surrogate
- 0.01: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // archive_mp also in explorer+gpumd_nep89_md+lammps_meam_md+mace_relax; mace_relax also in archive_mp+gpumd_nep89_relax+surrogate

### qe_hse06|split_4_3|merge_only|move+share
v(all) 0.465, v(empty) 0.120, efficiency gap 3.9e-15
| body | Shapley | averaged level value | difference [5, 95] |
|---|---|---|---|
| mace_relax | +0.189 | +0.194 | +0.005 [-0.030, +0.051] |
| gpumd_nep89_md | +0.060 | +0.042 | -0.018 [-0.057, +0.039] |
| lammps_meam_md | -0.037 | -0.059 | -0.023 [-0.068, +0.005] |
| explorer | -0.044 | -0.032 | +0.012 [-0.023, +0.044] |
| archive_mp | +0.187 | +0.208 | +0.021 [-0.027, +0.082] |
| gpumd_nep89_relax | -0.011 | -0.006 | +0.006 [-0.032, +0.062] |
| surrogate | +0.001 | -0.002 | -0.003 [-0.063, +0.042] |

Most occupied structures (share of early-window compute; second memberships after //):
- 0.58: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.18: archive_mp+gpumd_nep89_relax+surrogate > explorer+gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.04: archive_mp+gpumd_nep89_relax+mace_relax+surrogate > explorer+gpumd_nep89_md+lammps_meam_md
- 0.03: archive_mp+gpumd_nep89_relax+mace_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md
- 0.03: archive_mp+explorer+gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate
- 0.02: archive_mp+gpumd_nep89_relax+surrogate > explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // archive_mp also in explorer+gpumd_nep89_md+lammps_meam_md+mace_relax; gpumd_nep89_relax also in explorer+gpumd_nep89_md+lammps_meam_md+mace_relax; mace_relax also in archive_mp+gpumd_nep89_relax+surrogate; surrogate also in explorer+gpumd_nep89_md+lammps_meam_md+mace_relax
- 0.02: archive_mp+gpumd_nep89_md+gpumd_nep89_relax+lammps_meam_md+mace_relax+surrogate > explorer
- 0.02: archive_mp+gpumd_nep89_relax+surrogate || explorer+gpumd_nep89_md+lammps_meam_md+mace_relax // gpumd_nep89_md also in archive_mp+gpumd_nep89_relax+surrogate; mace_relax also in archive_mp+gpumd_nep89_relax+surrogate

