# Experiment 07: attribution over paired campaign arms

Substrate: `../shared/output/bandgap_cluster_run2/paired_campaign_k4/checkpoints` (label: k4_50seed). Value = measured exp 26 tau; no simulation.

## early-window game (exact 4-player Shapley, mean over all donor->receiver cells)

| player | mean Shapley |
|---|---|
| cold_data | +0.5917 |
| donor_prior | +0.0792 |
| adaptive_trust | -0.0082 |
| kway_events | +0.0278 |

donor_prior share positive in 88% of cells.

## final-window game (exact 4-player Shapley, mean over all donor->receiver cells)

| player | mean Shapley |
|---|---|
| cold_data | +0.7049 |
| donor_prior | +0.0228 |
| adaptive_trust | -0.0019 |
| kway_events | +0.0272 |

donor_prior share positive in 61% of cells.

## Pooled-prior game (early window, per receiver)

| receiver | cold_data | pooled_prior | kway_events |
|---|---|---|---|
| expt_zhuo | +0.7157 | +0.0076 | +0.0275 |
| jarvis_mbj | +0.6089 | +0.1030 | +0.0330 |
| jarvis_optb88vdw | +0.5404 | +0.1457 | +0.0174 |
| mp_gga | +0.5085 | +0.0913 | +0.0313 |
| mp_gga_expsynth | +0.6546 | +0.1163 | +0.0331 |
| mp_r2scan | +0.6638 | +0.1667 | +0.0278 |
| snumat_gga | +0.5574 | +0.0713 | +0.0327 |
| snumat_hse | +0.6051 | +0.0529 | +0.0365 |

## Most negative donor_prior cells (early window)

| cell | prior Shapley [95% CI] | adaptive_trust Shapley |
|---|---|---|
| mp_gga->expt_zhuo | -0.0385 [-0.0478, -0.0294] | +0.0235 |
| mp_gga->snumat_hse | -0.0311 [-0.0426, -0.0201] | +0.0095 |
| mp_gga_expsynth->expt_zhuo | -0.0260 [-0.0358, -0.0170] | +0.0221 |
| mp_gga->snumat_gga | -0.0205 [-0.0326, -0.0094] | +0.0044 |
| jarvis_mbj->expt_zhuo | -0.0091 [-0.0181, -0.0002] | +0.0116 |
