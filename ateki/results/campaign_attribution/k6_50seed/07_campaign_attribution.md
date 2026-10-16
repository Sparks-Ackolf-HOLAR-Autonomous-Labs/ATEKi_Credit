# Experiment 07: attribution over paired campaign arms

Substrate: `../shared/output/bandgap_cluster_run2/paired_campaign_k6/checkpoints` (label: k6_50seed). Value = measured exp 26 tau; no simulation.

## early-window game (exact 4-player Shapley, mean over all donor->receiver cells)

| player | mean Shapley |
|---|---|
| cold_data | +0.5824 |
| donor_prior | +0.0658 |
| adaptive_trust | -0.0163 |
| kway_events | +0.0185 |

donor_prior share positive in 88% of cells.

## final-window game (exact 4-player Shapley, mean over all donor->receiver cells)

| player | mean Shapley |
|---|---|
| cold_data | +0.7043 |
| donor_prior | +0.0217 |
| adaptive_trust | -0.0016 |
| kway_events | +0.0266 |

donor_prior share positive in 61% of cells.

## Pooled-prior game (early window, per receiver)

| receiver | cold_data | pooled_prior | kway_events |
|---|---|---|---|
| expt_zhuo | +0.7051 | +0.0021 | +0.0170 |
| jarvis_mbj | +0.5993 | +0.0847 | +0.0234 |
| jarvis_optb88vdw | +0.5187 | +0.1111 | -0.0044 |
| mp_gga | +0.4939 | +0.0757 | +0.0168 |
| mp_gga_expsynth | +0.6264 | +0.0967 | +0.0050 |
| mp_r2scan | +0.6340 | +0.1313 | -0.0021 |
| snumat_gga | +0.5461 | +0.0514 | +0.0213 |
| snumat_hse | +0.6001 | +0.0375 | +0.0315 |

## Most negative donor_prior cells (early window)

| cell | prior Shapley [95% CI] | adaptive_trust Shapley |
|---|---|---|
| mp_gga->expt_zhuo | -0.0362 [-0.0439, -0.0281] | +0.0258 |
| mp_gga->snumat_hse | -0.0339 [-0.0444, -0.0233] | +0.0098 |
| mp_gga_expsynth->expt_zhuo | -0.0268 [-0.0345, -0.0187] | +0.0210 |
| mp_gga->snumat_gga | -0.0194 [-0.0323, -0.0059] | +0.0057 |
| jarvis_optb88vdw->expt_zhuo | -0.0093 [-0.0174, -0.0013] | +0.0013 |
