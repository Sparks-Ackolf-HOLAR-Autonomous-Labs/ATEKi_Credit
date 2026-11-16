# Experiment 10: estimator disagreement, team structure and conference structures on the seven-database game

- Source game: `results/database_attribution/expt_zhuo/database_attribution.json` (receiver expt_zhuo, final window, 128 measured coalitions)
- Zero-normalised game w(S) = v(S) - v(empty); v(empty) = 0.8667, w(N) = -0.0667

## (a) Baseline estimators

| Database | Shapley | rank | Banzhaf | rank | LOO | rank |
|---|---|---|---|---|---|---|
| SNUMAT GGA | +0.0185 | 1 | +0.0204 | 1 | +0.0095 | 1 |
| SNUMAT HSE | +0.0185 | 1 | +0.0204 | 1 | +0.0095 | 1 |
| JARVIS TBmBJ | -0.0113 | 3 | -0.0070 | 3 | +0.0000 | 4 |
| MP GGA (ICSD-provenance subset) | -0.0224 | 4 | -0.0219 | 7 | +0.0000 | 4 |
| JARVIS OptB88vdW | -0.0228 | 5 | -0.0115 | 4 | -0.0190 | 7 |
| MP GGA | -0.0234 | 6 | -0.0147 | 6 | +0.0095 | 1 |
| MP r2SCAN | -0.0237 | 7 | -0.0135 | 5 | -0.0095 | 6 |

- Sign flips vs Shapley: {"banzhaf": [], "loo": ["jarvis_mbj", "mp_gga", "mp_gga_expsynth"]}
- Bottom player: {"shapley": ["mp_r2scan"], "banzhaf": ["mp_gga_expsynth"], "loo": ["jarvis_optb88vdw"]}
- Per-seed disagreement counts (10 seeds): {"loo_bottom_differs": 8, "banzhaf_bottom_differs": 3, "loo_bottom_unique_and_equal": 1, "loo_bottom_excludes_shapley_bottom": 1, "loo_any_sign_flip": 10, "banzhaf_any_sign_flip": 3, "loo_top_differs": 9, "banzhaf_top_differs": 1}

## (b) Star topology, every database as hub

| Hub | raw phi(hub) | degree-weighted hub | Myerson hub | hub rank raw -> Myerson | BC leaves tied | degree keeps leaf order | Myerson keeps leaf order |
|---|---|---|---|---|---|---|---|
| JARVIS TBmBJ | -0.0113 | -0.0389 | +0.1093 | 3 -> 1 | True | True | False |
| JARVIS OptB88vdW | -0.0228 | -0.0742 | +0.0886 | 5 -> 1 | True | True | False |
| MP GGA | -0.0234 | -0.0761 | +0.0701 | 6 -> 1 | True | True | True |
| MP GGA (ICSD-provenance subset) | -0.0224 | -0.0732 | +0.1034 | 4 -> 1 | True | True | False |
| MP r2SCAN | -0.0237 | -0.0771 | +0.0822 | 7 -> 1 | True | True | True |
| SNUMAT GGA | +0.0185 | +0.0531 | +0.1616 | 1 -> 1 | True | True | False |
| SNUMAT HSE | +0.0185 | +0.0531 | +0.1616 | 1 -> 1 | True | True | False |

Headline hub: MP GGA

| Database | raw Shapley | betweenness-weighted | degree-weighted | Myerson (star) |
|---|---|---|---|---|
| SNUMAT GGA | +0.0185 | +0.0139 | +0.0166 | +0.0122 |
| SNUMAT HSE | +0.0185 | +0.0139 | +0.0166 | +0.0122 |
| JARVIS TBmBJ | -0.0113 | +0.0139 | -0.0008 | -0.0282 |
| MP GGA (ICSD-provenance subset) | -0.0224 | +0.0139 | -0.0073 | -0.0336 |
| JARVIS OptB88vdW | -0.0228 | +0.0139 | -0.0075 | -0.0482 |
| MP GGA (hub) | -0.0234 | -0.1499 | -0.0761 | +0.0701 |
| MP r2SCAN | -0.0237 | +0.0139 | -0.0081 | -0.0512 |

## (c) Conference structure: three organisation meetings + beyond-GGA meeting

Hyperedges: [["mp_gga", "mp_gga_expsynth", "mp_r2scan"], ["jarvis_mbj", "jarvis_optb88vdw"], ["snumat_gga", "snumat_hse"], ["jarvis_mbj", "mp_r2scan", "snumat_hse"]]

| Database | none | star (hub MP GGA) | hypergraph | clique |
|---|---|---|---|---|
| SNUMAT GGA | +0.0185 (1) | +0.0122 (2) | +0.0079 (2) | +0.0133 (3) |
| SNUMAT HSE | +0.0185 (1) | +0.0122 (2) | +0.0255 (1) | +0.0135 (2) |
| JARVIS TBmBJ | -0.0113 (3) | -0.0282 (4) | +0.0064 (3) | +0.0166 (1) |
| MP GGA (ICSD-provenance subset) | -0.0224 (4) | -0.0336 (5) | +0.0023 (4) | -0.0162 (5) |
| JARVIS OptB88vdW | -0.0228 (5) | -0.0482 (6) | -0.0493 (6) | -0.0488 (7) |
| MP GGA | -0.0234 (6) | +0.0701 (1) | -0.0548 (7) | -0.0386 (6) |
| MP r2SCAN | -0.0237 (7) | -0.0512 (7) | -0.0047 (5) | -0.0065 (4) |

- Rank moves hypergraph vs none: {"jarvis_optb88vdw": [5, 6], "mp_gga": [6, 7], "mp_r2scan": [7, 5], "snumat_gga": [1, 2]}
- Rank moves hypergraph vs clique: {"jarvis_mbj": [1, 3], "jarvis_optb88vdw": [7, 6], "mp_gga": [6, 7], "mp_gga_expsynth": [5, 4], "mp_r2scan": [4, 5], "snumat_gga": [3, 2], "snumat_hse": [2, 1]}
- k=2 reduction: {"max_abs_dev_values": 0.0, "max_abs_dev_coalitions": 0.0, "tolerance": 1e-09, "passed": true}

## (c) Conference structure: three organisation meetings + beyond-GGA + GGA-level meetings

Hyperedges: [["mp_gga", "mp_gga_expsynth", "mp_r2scan"], ["jarvis_mbj", "jarvis_optb88vdw"], ["snumat_gga", "snumat_hse"], ["jarvis_mbj", "mp_r2scan", "snumat_hse"], ["jarvis_optb88vdw", "mp_gga", "snumat_gga"]]

| Database | none | star (hub MP GGA) | hypergraph | clique |
|---|---|---|---|---|
| SNUMAT GGA | +0.0185 (1) | +0.0122 (2) | +0.0277 (1) | +0.0222 (1) |
| SNUMAT HSE | +0.0185 (1) | +0.0122 (2) | +0.0229 (2) | +0.0187 (2) |
| JARVIS TBmBJ | -0.0113 (3) | -0.0282 (4) | -0.0065 (3) | -0.0118 (3) |
| MP GGA (ICSD-provenance subset) | -0.0224 (4) | -0.0336 (5) | -0.0180 (4) | -0.0248 (6) |
| JARVIS OptB88vdW | -0.0228 (5) | -0.0482 (6) | -0.0295 (6) | -0.0272 (7) |
| MP GGA | -0.0234 (6) | +0.0701 (1) | -0.0350 (7) | -0.0210 (4) |
| MP r2SCAN | -0.0237 (7) | -0.0512 (7) | -0.0282 (5) | -0.0227 (5) |

- Rank moves hypergraph vs none: {"jarvis_optb88vdw": [5, 6], "mp_gga": [6, 7], "mp_r2scan": [7, 5], "snumat_hse": [1, 2]}
- Rank moves hypergraph vs clique: {"jarvis_optb88vdw": [7, 6], "mp_gga": [4, 7], "mp_gga_expsynth": [6, 4]}
- k=2 reduction: {"max_abs_dev_values": 0.0, "max_abs_dev_coalitions": 0.0, "tolerance": 1e-09, "passed": true}
