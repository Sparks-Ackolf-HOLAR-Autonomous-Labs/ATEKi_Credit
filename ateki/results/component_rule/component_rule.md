# Experiment 12: sum vs best-component rule (early window)

w(N) = +0.0419; Kendall-tau gain over the cold campaign.

## Star: hub value under each rule (raw Shapley in brackets)

| hub | raw | hub sum | hub max | hub rank sum | hub rank max |
|---|---:|---:|---:|---:|---:|
| JARVIS TBmBJ | -0.0067 | -0.1058 | -0.0541 | 7 | 7 |
| JARVIS OptB88vdW | -0.0130 | -0.1140 | -0.0588 | 7 | 7 |
| MP GGA | -0.0300 | -0.1487 | -0.0720 | 7 | 7 |
| MP GGA (ICSD-provenance subset) | -0.0228 | -0.1325 | -0.0658 | 7 | 7 |
| MP r2SCAN | +0.0064 | -0.0896 | -0.0459 | 7 | 7 |
| SNUMAT GGA | +0.0540 | -0.0118 | -0.0004 | 5 | 3 |
| SNUMAT HSE | +0.0540 | -0.0118 | -0.0004 | 5 | 3 |

## Structure A

| database | unrestricted | hyper sum | hyper max | clique sum | clique max |
|---|---:|---:|---:|---:|---:|
| SNUMAT GGA | +0.0540 (1) | +0.0770 (1) | +0.0692 (1) | +0.0828 (1) | +0.0780 (1) |
| SNUMAT HSE | +0.0540 (1) | +0.0278 (2) | +0.0354 (2) | +0.0181 (2) | +0.0226 (2) |
| MP r2SCAN | +0.0064 (3) | +0.0002 (4) | -0.0150 (5) | -0.0134 (5) | -0.0233 (7) |
| JARVIS TBmBJ | -0.0067 (4) | -0.0227 (6) | -0.0196 (7) | -0.0151 (6) | -0.0093 (4) |
| JARVIS OptB88vdW | -0.0130 (5) | +0.0055 (3) | +0.0006 (3) | +0.0014 (3) | -0.0015 (3) |
| MP GGA (ICSD-provenance subset) | -0.0228 (6) | -0.0124 (5) | -0.0126 (4) | -0.0114 (4) | -0.0109 (5) |
| MP GGA | -0.0300 (7) | -0.0334 (7) | -0.0161 (6) | -0.0206 (7) | -0.0138 (6) |

## Structure B

| database | unrestricted | hyper sum | hyper max | clique sum | clique max |
|---|---:|---:|---:|---:|---:|
| SNUMAT GGA | +0.0540 (1) | +0.0609 (1) | +0.0531 (2) | +0.0552 (2) | +0.0518 (2) |
| SNUMAT HSE | +0.0540 (1) | +0.0546 (2) | +0.0566 (1) | +0.0583 (1) | +0.0609 (1) |
| MP r2SCAN | +0.0064 (3) | +0.0083 (3) | -0.0056 (3) | +0.0020 (3) | -0.0024 (3) |
| JARVIS TBmBJ | -0.0067 (4) | -0.0086 (4) | -0.0070 (4) | -0.0081 (4) | -0.0073 (4) |
| JARVIS OptB88vdW | -0.0130 (5) | -0.0106 (5) | -0.0155 (6) | -0.0129 (5) | -0.0136 (5) |
| MP GGA (ICSD-provenance subset) | -0.0228 (6) | -0.0132 (6) | -0.0074 (5) | -0.0177 (6) | -0.0153 (6) |
| MP GGA | -0.0300 (7) | -0.0495 (7) | -0.0322 (7) | -0.0350 (7) | -0.0321 (7) |
