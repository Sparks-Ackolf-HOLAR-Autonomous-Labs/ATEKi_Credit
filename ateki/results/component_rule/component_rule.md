# Experiment 12: sum vs best-component rule (early window)

w(N) = +0.0419; Kendall-tau gain over the cold campaign.

## Star: hub value under each rule (raw Shapley in brackets)

| hub | raw | hub sum | hub max | hub rank sum | hub rank max |
|---|---:|---:|---:|---:|---:|
| JARVIS TBmBJ | -0.0134 | -0.0633 | -0.0349 | 7 | 7 |
| JARVIS OptB88vdW | -0.0051 | -0.0580 | -0.0314 | 7 | 7 |
| MP GGA | -0.0294 | -0.0933 | -0.0479 | 7 | 7 |
| MP GGA (ICSD-provenance subset) | -0.0234 | -0.0835 | -0.0432 | 7 | 7 |
| MP r2SCAN | +0.0054 | -0.0442 | -0.0244 | 7 | 7 |
| SNUMAT GGA | +0.0539 | +0.0243 | +0.0174 | 2 | 2 |
| SNUMAT HSE | +0.0539 | +0.0243 | +0.0174 | 2 | 2 |

## Structure A

| database | unrestricted | hyper sum | hyper max | clique sum | clique max |
|---|---:|---:|---:|---:|---:|
| SNUMAT GGA | +0.0539 (1) | +0.0633 (1) | +0.0579 (1) | +0.0682 (1) | +0.0658 (1) |
| SNUMAT HSE | +0.0539 (1) | +0.0277 (2) | +0.0322 (2) | +0.0288 (2) | +0.0314 (2) |
| MP r2SCAN | +0.0054 (3) | +0.0006 (4) | -0.0081 (4) | -0.0112 (5) | -0.0221 (7) |
| JARVIS OptB88vdW | -0.0051 (4) | +0.0110 (3) | +0.0032 (3) | +0.0040 (3) | +0.0012 (3) |
| JARVIS TBmBJ | -0.0134 (5) | -0.0070 (5) | -0.0108 (5) | -0.0103 (4) | -0.0069 (4) |
| MP GGA (ICSD-provenance subset) | -0.0234 (6) | -0.0215 (6) | -0.0153 (6) | -0.0167 (6) | -0.0132 (5) |
| MP GGA | -0.0294 (7) | -0.0322 (7) | -0.0171 (7) | -0.0208 (7) | -0.0143 (6) |

## Structure B

| database | unrestricted | hyper sum | hyper max | clique sum | clique max |
|---|---:|---:|---:|---:|---:|
| SNUMAT GGA | +0.0539 (1) | +0.0545 (1) | +0.0482 (2) | +0.0521 (2) | +0.0501 (2) |
| SNUMAT HSE | +0.0539 (1) | +0.0482 (2) | +0.0491 (1) | +0.0568 (1) | +0.0589 (1) |
| MP r2SCAN | +0.0054 (3) | +0.0045 (3) | -0.0065 (4) | +0.0032 (3) | -0.0023 (3) |
| JARVIS OptB88vdW | -0.0051 (4) | +0.0023 (4) | -0.0065 (4) | -0.0054 (4) | -0.0064 (4) |
| JARVIS TBmBJ | -0.0134 (5) | -0.0061 (5) | -0.0058 (3) | -0.0119 (5) | -0.0104 (5) |
| MP GGA (ICSD-provenance subset) | -0.0234 (6) | -0.0206 (6) | -0.0098 (6) | -0.0227 (6) | -0.0186 (6) |
| MP GGA | -0.0294 (7) | -0.0409 (7) | -0.0268 (7) | -0.0302 (7) | -0.0294 (7) |
