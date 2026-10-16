# Experiment 10: estimator disagreement, team structure and conference structures on the seven-database game

- Source game: `results/database_attribution/expt_zhuo/database_attribution.json` (receiver expt_zhuo, early window, 128 measured coalitions)
- Zero-normalised game w(S) = v(S) - v(empty); v(empty) = 0.6400, w(N) = 0.0419

## (a) Baseline estimators

| Database | Shapley | rank | Banzhaf | rank | LOO | rank |
|---|---|---|---|---|---|---|
| SNUMAT GGA | +0.0540 | 1 | +0.0428 | 1 | +0.0210 | 1 |
| SNUMAT HSE | +0.0540 | 1 | +0.0428 | 1 | +0.0210 | 1 |
| MP r2SCAN | +0.0064 | 3 | -0.0007 | 3 | +0.0038 | 3 |
| JARVIS TBmBJ | -0.0067 | 4 | -0.0121 | 4 | -0.0095 | 5 |
| JARVIS OptB88vdW | -0.0130 | 5 | -0.0193 | 5 | -0.0114 | 7 |
| MP GGA (ICSD-provenance subset) | -0.0228 | 6 | -0.0278 | 6 | -0.0095 | 5 |
| MP GGA | -0.0300 | 7 | -0.0356 | 7 | -0.0038 | 4 |

- Sign flips vs Shapley: {"banzhaf": ["mp_r2scan"], "loo": []}
- Bottom player: {"shapley": ["mp_gga"], "banzhaf": ["mp_gga"], "loo": ["jarvis_optb88vdw"]}
- Per-seed disagreement counts (10 seeds): {"loo_bottom_differs": 9, "banzhaf_bottom_differs": 0, "loo_bottom_unique_and_equal": 1, "loo_bottom_excludes_shapley_bottom": 2, "loo_any_sign_flip": 10, "banzhaf_any_sign_flip": 7, "loo_top_differs": 5, "banzhaf_top_differs": 0}

## (b) Star topology, every database as hub

| Hub | raw phi(hub) | degree-weighted hub | Myerson hub | hub rank raw -> Myerson | BC leaves tied | degree keeps leaf order | Myerson keeps leaf order |
|---|---|---|---|---|---|---|---|
| JARVIS TBmBJ | -0.0067 | -0.0183 | -0.1058 | 4 -> 7 | True | True | True |
| JARVIS OptB88vdW | -0.0130 | -0.0375 | -0.1140 | 5 -> 7 | True | True | True |
| MP GGA | -0.0300 | -0.0899 | -0.1487 | 7 -> 7 | True | True | True |
| MP GGA (ICSD-provenance subset) | -0.0228 | -0.0678 | -0.1325 | 6 -> 7 | True | True | True |
| MP r2SCAN | +0.0064 | +0.0221 | -0.0896 | 3 -> 7 | True | True | True |
| SNUMAT GGA | +0.0540 | +0.1690 | -0.0118 | 1 -> 5 | True | True | True |
| SNUMAT HSE | +0.0540 | +0.1690 | -0.0118 | 1 -> 5 | True | True | True |

Headline hub: MP GGA

| Database | raw Shapley | betweenness-weighted | degree-weighted | Myerson (star) |
|---|---|---|---|---|
| SNUMAT GGA | +0.0540 | +0.0359 | +0.0465 | +0.0862 |
| SNUMAT HSE | +0.0540 | +0.0359 | +0.0465 | +0.0862 |
| MP r2SCAN | +0.0064 | +0.0359 | +0.0187 | +0.0228 |
| JARVIS TBmBJ | -0.0067 | +0.0359 | +0.0110 | +0.0079 |
| JARVIS OptB88vdW | -0.0130 | +0.0359 | +0.0074 | +0.0014 |
| MP GGA (ICSD-provenance subset) | -0.0228 | +0.0359 | +0.0017 | -0.0139 |
| MP GGA (hub) | -0.0300 | -0.1737 | -0.0899 | -0.1487 |

## (c) Conference structure: three organisation meetings + beyond-GGA meeting

Hyperedges: [["mp_gga", "mp_gga_expsynth", "mp_r2scan"], ["jarvis_mbj", "jarvis_optb88vdw"], ["snumat_gga", "snumat_hse"], ["jarvis_mbj", "mp_r2scan", "snumat_hse"]]

| Database | none | star (hub SNUMAT GGA) | hypergraph | clique |
|---|---|---|---|---|
| SNUMAT GGA | +0.0540 (1) | -0.0118 (5) | +0.0770 (1) | +0.0828 (1) |
| SNUMAT HSE | +0.0540 (1) | +0.0847 (1) | +0.0278 (2) | +0.0181 (2) |
| MP r2SCAN | +0.0064 (3) | +0.0185 (2) | +0.0002 (4) | -0.0134 (5) |
| JARVIS TBmBJ | -0.0067 (4) | +0.0021 (3) | -0.0227 (6) | -0.0151 (6) |
| JARVIS OptB88vdW | -0.0130 (5) | -0.0030 (4) | +0.0055 (3) | +0.0014 (3) |
| MP GGA (ICSD-provenance subset) | -0.0228 (6) | -0.0182 (6) | -0.0124 (5) | -0.0114 (4) |
| MP GGA | -0.0300 (7) | -0.0304 (7) | -0.0334 (7) | -0.0206 (7) |

- Rank moves hypergraph vs none: {"jarvis_mbj": [4, 6], "jarvis_optb88vdw": [5, 3], "mp_gga_expsynth": [6, 5], "mp_r2scan": [3, 4], "snumat_hse": [1, 2]}
- Rank moves hypergraph vs clique: {"mp_gga_expsynth": [4, 5], "mp_r2scan": [5, 4]}
- k=2 reduction: {"max_abs_dev_values": 0.0, "max_abs_dev_coalitions": 0.0, "tolerance": 1e-09, "passed": true}

## (c) Conference structure: three organisation meetings + beyond-GGA + GGA-level meetings

Hyperedges: [["mp_gga", "mp_gga_expsynth", "mp_r2scan"], ["jarvis_mbj", "jarvis_optb88vdw"], ["snumat_gga", "snumat_hse"], ["jarvis_mbj", "mp_r2scan", "snumat_hse"], ["jarvis_optb88vdw", "mp_gga", "snumat_gga"]]

| Database | none | star (hub SNUMAT GGA) | hypergraph | clique |
|---|---|---|---|---|
| SNUMAT GGA | +0.0540 (1) | -0.0118 (5) | +0.0609 (1) | +0.0552 (2) |
| SNUMAT HSE | +0.0540 (1) | +0.0847 (1) | +0.0546 (2) | +0.0583 (1) |
| MP r2SCAN | +0.0064 (3) | +0.0185 (2) | +0.0083 (3) | +0.0020 (3) |
| JARVIS TBmBJ | -0.0067 (4) | +0.0021 (3) | -0.0086 (4) | -0.0081 (4) |
| JARVIS OptB88vdW | -0.0130 (5) | -0.0030 (4) | -0.0106 (5) | -0.0129 (5) |
| MP GGA (ICSD-provenance subset) | -0.0228 (6) | -0.0182 (6) | -0.0132 (6) | -0.0177 (6) |
| MP GGA | -0.0300 (7) | -0.0304 (7) | -0.0495 (7) | -0.0350 (7) |

- Rank moves hypergraph vs none: {"snumat_hse": [1, 2]}
- Rank moves hypergraph vs clique: {"snumat_gga": [2, 1], "snumat_hse": [1, 2]}
- k=2 reduction: {"max_abs_dev_values": 0.0, "max_abs_dev_coalitions": 0.0, "tolerance": 1e-09, "passed": true}
