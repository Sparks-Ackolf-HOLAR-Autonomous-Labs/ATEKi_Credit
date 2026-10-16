# Experiment 10: estimator disagreement, team structure and conference structures on the seven-database game

- Source game: `results/database_attribution/expt_zhuo/database_attribution.json` (receiver expt_zhuo, final window, 128 measured coalitions)
- Zero-normalised game w(S) = v(S) - v(empty); v(empty) = 0.7143, w(N) = 0.0667

## (a) Baseline estimators

| Database | Shapley | rank | Banzhaf | rank | LOO | rank |
|---|---|---|---|---|---|---|
| MP r2SCAN | +0.0249 | 1 | +0.0125 | 2 | +0.0000 | 1 |
| JARVIS OptB88vdW | +0.0224 | 2 | +0.0185 | 1 | +0.0000 | 1 |
| SNUMAT GGA | +0.0140 | 3 | +0.0077 | 3 | -0.0190 | 4 |
| SNUMAT HSE | +0.0140 | 3 | +0.0077 | 3 | -0.0190 | 4 |
| JARVIS TBmBJ | +0.0015 | 5 | -0.0021 | 5 | -0.0190 | 4 |
| MP GGA (ICSD-provenance subset) | -0.0049 | 6 | -0.0080 | 7 | -0.0190 | 4 |
| MP GGA | -0.0052 | 7 | -0.0077 | 6 | -0.0095 | 3 |

- Sign flips vs Shapley: {"banzhaf": ["jarvis_mbj"], "loo": ["jarvis_mbj", "jarvis_optb88vdw", "mp_r2scan", "snumat_gga", "snumat_hse"]}
- Bottom player: {"shapley": ["mp_gga"], "banzhaf": ["mp_gga_expsynth"], "loo": ["jarvis_mbj", "mp_gga_expsynth", "snumat_gga", "snumat_hse"]}
- Per-seed disagreement counts (10 seeds): {"loo_bottom_differs": 7, "banzhaf_bottom_differs": 0, "loo_bottom_unique_and_equal": 0, "loo_bottom_excludes_shapley_bottom": 0, "loo_any_sign_flip": 10, "banzhaf_any_sign_flip": 3, "loo_top_differs": 8, "banzhaf_top_differs": 2}

## (b) Star topology, every database as hub

| Hub | raw phi(hub) | degree-weighted hub | Myerson hub | hub rank raw -> Myerson | BC leaves tied | degree keeps leaf order | Myerson keeps leaf order |
|---|---|---|---|---|---|---|---|
| JARVIS TBmBJ | +0.0015 | +0.0084 | -0.1156 | 5 -> 7 | True | True | True |
| JARVIS OptB88vdW | +0.0224 | +0.0730 | -0.0898 | 2 -> 7 | True | True | True |
| MP GGA | -0.0052 | -0.0121 | -0.1357 | 7 -> 7 | True | True | True |
| MP GGA (ICSD-provenance subset) | -0.0049 | -0.0111 | -0.1238 | 6 -> 7 | True | True | True |
| MP r2SCAN | +0.0249 | +0.0809 | -0.0666 | 1 -> 7 | True | True | True |
| SNUMAT GGA | +0.0140 | +0.0471 | -0.0872 | 3 -> 7 | True | True | True |
| SNUMAT HSE | +0.0140 | +0.0471 | -0.0872 | 3 -> 7 | True | True | True |

Headline hub: MP GGA

| Database | raw Shapley | betweenness-weighted | degree-weighted | Myerson (star) |
|---|---|---|---|---|
| MP r2SCAN | +0.0249 | +0.0147 | +0.0207 | +0.0570 |
| JARVIS OptB88vdW | +0.0224 | +0.0147 | +0.0192 | +0.0407 |
| SNUMAT GGA | +0.0140 | +0.0147 | +0.0143 | +0.0395 |
| SNUMAT HSE | +0.0140 | +0.0147 | +0.0143 | +0.0395 |
| JARVIS TBmBJ | +0.0015 | +0.0147 | +0.0070 | +0.0168 |
| MP GGA (ICSD-provenance subset) | -0.0049 | +0.0147 | +0.0033 | +0.0088 |
| MP GGA (hub) | -0.0052 | -0.0218 | -0.0121 | -0.1357 |

## (c) Conference structure: three organisation meetings + beyond-GGA meeting

Hyperedges: [["mp_gga", "mp_gga_expsynth", "mp_r2scan"], ["jarvis_mbj", "jarvis_optb88vdw"], ["snumat_gga", "snumat_hse"], ["jarvis_mbj", "mp_r2scan", "snumat_hse"]]

| Database | none | star (hub JARVIS OptB88vdW) | hypergraph | clique |
|---|---|---|---|---|
| MP r2SCAN | +0.0249 (1) | +0.0556 (1) | +0.0240 (3) | +0.0147 (3) |
| JARVIS OptB88vdW | +0.0224 (2) | -0.0898 (7) | +0.0478 (1) | +0.0423 (1) |
| SNUMAT GGA | +0.0140 (3) | +0.0367 (2) | +0.0343 (2) | +0.0340 (2) |
| SNUMAT HSE | +0.0140 (3) | +0.0367 (2) | -0.0109 (5) | -0.0077 (6) |
| JARVIS TBmBJ | +0.0015 (5) | +0.0166 (4) | -0.0204 (7) | -0.0152 (7) |
| MP GGA (ICSD-provenance subset) | -0.0049 (6) | +0.0090 (5) | +0.0054 (4) | +0.0036 (4) |
| MP GGA | -0.0052 (7) | +0.0018 (6) | -0.0136 (6) | -0.0050 (5) |

- Rank moves hypergraph vs none: {"jarvis_mbj": [5, 7], "jarvis_optb88vdw": [2, 1], "mp_gga": [7, 6], "mp_gga_expsynth": [6, 4], "mp_r2scan": [1, 3], "snumat_gga": [3, 2], "snumat_hse": [3, 5]}
- Rank moves hypergraph vs clique: {"mp_gga": [5, 6], "snumat_hse": [6, 5]}
- k=2 reduction: {"max_abs_dev_values": 0.0, "max_abs_dev_coalitions": 0.0, "tolerance": 1e-09, "passed": true}

## (c) Conference structure: three organisation meetings + beyond-GGA + GGA-level meetings

Hyperedges: [["mp_gga", "mp_gga_expsynth", "mp_r2scan"], ["jarvis_mbj", "jarvis_optb88vdw"], ["snumat_gga", "snumat_hse"], ["jarvis_mbj", "mp_r2scan", "snumat_hse"], ["jarvis_optb88vdw", "mp_gga", "snumat_gga"]]

| Database | none | star (hub JARVIS OptB88vdW) | hypergraph | clique |
|---|---|---|---|---|
| MP r2SCAN | +0.0249 (1) | +0.0556 (1) | +0.0360 (1) | +0.0238 (2) |
| JARVIS OptB88vdW | +0.0224 (2) | -0.0898 (7) | +0.0322 (2) | +0.0249 (1) |
| SNUMAT GGA | +0.0140 (3) | +0.0367 (2) | +0.0187 (3) | +0.0170 (3) |
| SNUMAT HSE | +0.0140 (3) | +0.0367 (2) | +0.0085 (4) | +0.0135 (4) |
| JARVIS TBmBJ | +0.0015 (5) | +0.0166 (4) | -0.0042 (6) | +0.0003 (6) |
| MP GGA (ICSD-provenance subset) | -0.0049 (6) | +0.0090 (5) | +0.0047 (5) | +0.0013 (5) |
| MP GGA | -0.0052 (7) | +0.0018 (6) | -0.0293 (7) | -0.0143 (7) |

- Rank moves hypergraph vs none: {"jarvis_mbj": [5, 6], "mp_gga_expsynth": [6, 5], "snumat_hse": [3, 4]}
- Rank moves hypergraph vs clique: {"jarvis_optb88vdw": [1, 2], "mp_r2scan": [2, 1]}
- k=2 reduction: {"max_abs_dev_values": 0.0, "max_abs_dev_coalitions": 0.0, "tolerance": 1e-09, "passed": true}
