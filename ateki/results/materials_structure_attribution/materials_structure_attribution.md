# Experiment 10: estimator disagreement, team structure and conference structures on the seven-database game

- Source game: `results/database_attribution/expt_zhuo/database_attribution.json` (receiver expt_zhuo, early window, 128 measured coalitions)
- Zero-normalised game w(S) = v(S) - v(empty); v(empty) = 0.6949, w(N) = 0.0419

## (a) Baseline estimators

| Database | Shapley | rank | Banzhaf | rank | LOO | rank |
|---|---|---|---|---|---|---|
| SNUMAT GGA | +0.0539 | 1 | +0.0462 | 1 | +0.0286 | 1 |
| SNUMAT HSE | +0.0539 | 1 | +0.0462 | 1 | +0.0286 | 1 |
| MP r2SCAN | +0.0054 | 3 | -0.0023 | 3 | +0.0076 | 3 |
| JARVIS OptB88vdW | -0.0051 | 4 | -0.0076 | 4 | -0.0133 | 6 |
| JARVIS TBmBJ | -0.0134 | 5 | -0.0188 | 5 | -0.0160 | 7 |
| MP GGA (ICSD-provenance subset) | -0.0234 | 6 | -0.0284 | 6 | -0.0103 | 5 |
| MP GGA | -0.0294 | 7 | -0.0357 | 7 | -0.0038 | 4 |

- Sign flips vs Shapley: {"banzhaf": ["mp_r2scan"], "loo": []}
- Bottom player: {"shapley": ["mp_gga"], "banzhaf": ["mp_gga"], "loo": ["jarvis_mbj"]}
- Per-seed disagreement counts (10 seeds): {"loo_bottom_differs": 9, "banzhaf_bottom_differs": 2, "loo_bottom_unique_and_equal": 1, "loo_bottom_excludes_shapley_bottom": 4, "loo_any_sign_flip": 10, "banzhaf_any_sign_flip": 6, "loo_top_differs": 3, "banzhaf_top_differs": 2}

## (b) Star topology, every database as hub

| Hub | raw phi(hub) | degree-weighted hub | Myerson hub | hub rank raw -> Myerson | BC leaves tied | degree keeps leaf order | Myerson keeps leaf order |
|---|---|---|---|---|---|---|---|
| JARVIS TBmBJ | -0.0134 | -0.0389 | -0.0633 | 5 -> 7 | True | True | True |
| JARVIS OptB88vdW | -0.0051 | -0.0131 | -0.0580 | 4 -> 7 | True | True | True |
| MP GGA | -0.0294 | -0.0883 | -0.0933 | 7 -> 7 | True | True | True |
| MP GGA (ICSD-provenance subset) | -0.0234 | -0.0696 | -0.0835 | 6 -> 7 | True | True | True |
| MP r2SCAN | +0.0054 | +0.0192 | -0.0442 | 3 -> 7 | True | True | True |
| SNUMAT GGA | +0.0539 | +0.1687 | +0.0243 | 1 -> 2 | True | True | True |
| SNUMAT HSE | +0.0539 | +0.1687 | +0.0243 | 1 -> 2 | True | True | True |

Headline hub: MP GGA

| Database | raw Shapley | betweenness-weighted | degree-weighted | Myerson (star) |
|---|---|---|---|---|
| SNUMAT GGA | +0.0539 | +0.0354 | +0.0462 | +0.0724 |
| SNUMAT HSE | +0.0539 | +0.0354 | +0.0462 | +0.0724 |
| MP r2SCAN | +0.0054 | +0.0354 | +0.0179 | +0.0142 |
| JARVIS OptB88vdW | -0.0051 | +0.0354 | +0.0118 | +0.0008 |
| JARVIS TBmBJ | -0.0134 | +0.0354 | +0.0069 | -0.0041 |
| MP GGA (ICSD-provenance subset) | -0.0234 | +0.0354 | +0.0011 | -0.0206 |
| MP GGA (hub) | -0.0294 | -0.1707 | -0.0883 | -0.0933 |

## (c) Conference structure: three organisation meetings + beyond-GGA meeting

Hyperedges: [["mp_gga", "mp_gga_expsynth", "mp_r2scan"], ["jarvis_mbj", "jarvis_optb88vdw"], ["snumat_gga", "snumat_hse"], ["jarvis_mbj", "mp_r2scan", "snumat_hse"]]

| Database | none | star (hub SNUMAT GGA) | hypergraph | clique |
|---|---|---|---|---|
| SNUMAT GGA | +0.0539 (1) | +0.0243 (2) | +0.0633 (1) | +0.0682 (1) |
| SNUMAT HSE | +0.0539 (1) | +0.0702 (1) | +0.0277 (2) | +0.0288 (2) |
| MP r2SCAN | +0.0054 (3) | +0.0118 (3) | +0.0006 (4) | -0.0112 (5) |
| JARVIS OptB88vdW | -0.0051 (4) | -0.0024 (4) | +0.0110 (3) | +0.0040 (3) |
| JARVIS TBmBJ | -0.0134 (5) | -0.0090 (5) | -0.0070 (5) | -0.0103 (4) |
| MP GGA (ICSD-provenance subset) | -0.0234 (6) | -0.0228 (6) | -0.0215 (6) | -0.0167 (6) |
| MP GGA | -0.0294 (7) | -0.0301 (7) | -0.0322 (7) | -0.0208 (7) |

- Rank moves hypergraph vs none: {"jarvis_optb88vdw": [4, 3], "mp_r2scan": [3, 4], "snumat_hse": [1, 2]}
- Rank moves hypergraph vs clique: {"jarvis_mbj": [4, 5], "mp_r2scan": [5, 4]}
- k=2 reduction: {"max_abs_dev_values": 0.0, "max_abs_dev_coalitions": 0.0, "tolerance": 1e-09, "passed": true}

## (c) Conference structure: three organisation meetings + beyond-GGA + GGA-level meetings

Hyperedges: [["mp_gga", "mp_gga_expsynth", "mp_r2scan"], ["jarvis_mbj", "jarvis_optb88vdw"], ["snumat_gga", "snumat_hse"], ["jarvis_mbj", "mp_r2scan", "snumat_hse"], ["jarvis_optb88vdw", "mp_gga", "snumat_gga"]]

| Database | none | star (hub SNUMAT GGA) | hypergraph | clique |
|---|---|---|---|---|
| SNUMAT GGA | +0.0539 (1) | +0.0243 (2) | +0.0545 (1) | +0.0521 (2) |
| SNUMAT HSE | +0.0539 (1) | +0.0702 (1) | +0.0482 (2) | +0.0568 (1) |
| MP r2SCAN | +0.0054 (3) | +0.0118 (3) | +0.0045 (3) | +0.0032 (3) |
| JARVIS OptB88vdW | -0.0051 (4) | -0.0024 (4) | +0.0023 (4) | -0.0054 (4) |
| JARVIS TBmBJ | -0.0134 (5) | -0.0090 (5) | -0.0061 (5) | -0.0119 (5) |
| MP GGA (ICSD-provenance subset) | -0.0234 (6) | -0.0228 (6) | -0.0206 (6) | -0.0227 (6) |
| MP GGA | -0.0294 (7) | -0.0301 (7) | -0.0409 (7) | -0.0302 (7) |

- Rank moves hypergraph vs none: {"snumat_hse": [1, 2]}
- Rank moves hypergraph vs clique: {"snumat_gga": [2, 1], "snumat_hse": [1, 2]}
- k=2 reduction: {"max_abs_dev_values": 0.0, "max_abs_dev_coalitions": 0.0, "tolerance": 1e-09, "passed": true}
