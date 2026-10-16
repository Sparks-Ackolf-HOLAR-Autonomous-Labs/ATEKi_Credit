# Experiment 16: several swarms in one campaign

Value = early-window recall area of the ten most stable compounds (mean over matched seeds).
Batch of 4 shared by all swarms: every configuration spends the same compute.

## Team values, receiver qe_pbe

| configuration | inner | outer | isolated | published |
|---|---|---|---|---|
| one_7 | flat | equal |  | 0.610 |
| one_7 | emergent | equal |  | 0.702 |
| split_4_3 | flat | equal | 0.614 | 0.606 |
| split_4_3 | flat | size | 0.610 | 0.599 |
| split_4_3 | flat | record | 0.608 | 0.605 |
| split_4_3 | emergent | equal | 0.680 | 0.671 |
| split_4_3 | emergent | size | 0.675 | 0.654 |
| split_4_3 | emergent | record | 0.671 | 0.661 |
| split_2_5s | flat | equal | 0.616 | 0.609 |
| split_2_5s | flat | size | 0.606 | 0.591 |
| split_2_5s | flat | record | 0.630 | 0.616 |
| split_2_5s | emergent | equal | 0.639 | 0.654 |
| split_2_5s | emergent | size | 0.661 | 0.663 |
| split_2_5s | emergent | record | 0.655 | 0.668 |
| split_2_5w | flat | equal | 0.544 | 0.552 |
| split_2_5w | flat | size | 0.587 | 0.601 |
| split_2_5w | flat | record | 0.556 | 0.599 |
| split_2_5w | emergent | equal | 0.571 | 0.604 |
| split_2_5w | emergent | size | 0.643 | 0.657 |
| split_2_5w | emergent | record | 0.590 | 0.694 |
| split_1_6 | flat | equal | 0.670 | 0.694 |
| split_1_6 | flat | size | 0.623 | 0.616 |
| split_1_6 | flat | record | 0.679 | 0.736 |
| split_1_6 | emergent | equal | 0.685 | 0.732 |
| split_1_6 | emergent | size | 0.656 | 0.676 |
| split_1_6 | emergent | record | 0.709 | 0.749 |
| split_2_2_3 | flat | equal | 0.583 | 0.623 |
| split_2_2_3 | flat | size | 0.574 | 0.598 |
| split_2_2_3 | flat | record | 0.561 | 0.664 |
| split_2_2_3 | emergent | equal | 0.620 | 0.623 |
| split_2_2_3 | emergent | size | 0.603 | 0.617 |
| split_2_2_3 | emergent | record | 0.610 | 0.656 |
| split_1x7 | flat | equal | 0.551 | 0.610 |
| split_1x7 | flat | size | 0.551 | 0.610 |
| split_1x7 | flat | record | 0.593 | 0.647 |
| split_1x7 | emergent | equal | 0.544 | 0.597 |
| split_1x7 | emergent | size | 0.544 | 0.597 |
| split_1x7 | emergent | record | 0.579 | 0.645 |
| dup_7_7 | flat | equal | 0.614 | 0.598 |
| dup_7_7 | flat | size | 0.614 | 0.598 |
| dup_7_7 | flat | record | 0.621 | 0.599 |
| dup_7_7 | emergent | equal | 0.678 | 0.683 |
| dup_7_7 | emergent | size | 0.678 | 0.683 |
| dup_7_7 | emergent | record | 0.678 | 0.687 |
| dup_7_7_7 | flat | equal | 0.597 | 0.605 |
| dup_7_7_7 | flat | size | 0.597 | 0.605 |
| dup_7_7_7 | flat | record | 0.609 | 0.606 |
| dup_7_7_7 | emergent | equal | 0.669 | 0.688 |
| dup_7_7_7 | emergent | size | 0.669 | 0.688 |
| dup_7_7_7 | emergent | record | 0.681 | 0.685 |
| dup_7_3 | flat | equal | 0.572 | 0.555 |
| dup_7_3 | flat | size | 0.590 | 0.599 |
| dup_7_3 | flat | record | 0.581 | 0.562 |
| dup_7_3 | emergent | equal | 0.646 | 0.648 |
| dup_7_3 | emergent | size | 0.662 | 0.669 |
| dup_7_3 | emergent | record | 0.645 | 0.639 |

## Team values, receiver qe_hse06

| configuration | inner | outer | isolated | published |
|---|---|---|---|---|
| one_7 | flat | equal |  | 0.384 |
| one_7 | emergent | equal |  | 0.503 |
| split_4_3 | flat | equal | 0.383 | 0.399 |
| split_4_3 | flat | size | 0.399 | 0.398 |
| split_4_3 | flat | record | 0.420 | 0.385 |
| split_4_3 | emergent | equal | 0.494 | 0.494 |
| split_4_3 | emergent | size | 0.496 | 0.472 |
| split_4_3 | emergent | record | 0.502 | 0.463 |
| split_2_5s | flat | equal | 0.407 | 0.371 |
| split_2_5s | flat | size | 0.396 | 0.365 |
| split_2_5s | flat | record | 0.394 | 0.376 |
| split_2_5s | emergent | equal | 0.471 | 0.478 |
| split_2_5s | emergent | size | 0.436 | 0.448 |
| split_2_5s | emergent | record | 0.485 | 0.510 |
| split_2_5w | flat | equal | 0.359 | 0.348 |
| split_2_5w | flat | size | 0.350 | 0.402 |
| split_2_5w | flat | record | 0.334 | 0.330 |
| split_2_5w | emergent | equal | 0.377 | 0.405 |
| split_2_5w | emergent | size | 0.453 | 0.471 |
| split_2_5w | emergent | record | 0.377 | 0.495 |
| split_1_6 | flat | equal | 0.502 | 0.466 |
| split_1_6 | flat | size | 0.447 | 0.379 |
| split_1_6 | flat | record | 0.519 | 0.563 |
| split_1_6 | emergent | equal | 0.534 | 0.551 |
| split_1_6 | emergent | size | 0.487 | 0.469 |
| split_1_6 | emergent | record | 0.547 | 0.600 |
| split_2_2_3 | flat | equal | 0.401 | 0.390 |
| split_2_2_3 | flat | size | 0.421 | 0.333 |
| split_2_2_3 | flat | record | 0.406 | 0.444 |
| split_2_2_3 | emergent | equal | 0.464 | 0.404 |
| split_2_2_3 | emergent | size | 0.451 | 0.392 |
| split_2_2_3 | emergent | record | 0.449 | 0.443 |
| split_1x7 | flat | equal | 0.399 | 0.384 |
| split_1x7 | flat | size | 0.399 | 0.384 |
| split_1x7 | flat | record | 0.427 | 0.397 |
| split_1x7 | emergent | equal | 0.402 | 0.370 |
| split_1x7 | emergent | size | 0.402 | 0.370 |
| split_1x7 | emergent | record | 0.429 | 0.390 |
| dup_7_7 | flat | equal | 0.406 | 0.401 |
| dup_7_7 | flat | size | 0.406 | 0.401 |
| dup_7_7 | flat | record | 0.397 | 0.395 |
| dup_7_7 | emergent | equal | 0.508 | 0.510 |
| dup_7_7 | emergent | size | 0.508 | 0.510 |
| dup_7_7 | emergent | record | 0.523 | 0.507 |
| dup_7_7_7 | flat | equal | 0.399 | 0.384 |
| dup_7_7_7 | flat | size | 0.399 | 0.384 |
| dup_7_7_7 | flat | record | 0.406 | 0.385 |
| dup_7_7_7 | emergent | equal | 0.543 | 0.522 |
| dup_7_7_7 | emergent | size | 0.543 | 0.522 |
| dup_7_7_7 | emergent | record | 0.538 | 0.510 |
| dup_7_3 | flat | equal | 0.399 | 0.412 |
| dup_7_3 | flat | size | 0.399 | 0.417 |
| dup_7_3 | flat | record | 0.402 | 0.422 |
| dup_7_3 | emergent | equal | 0.484 | 0.509 |
| dup_7_3 | emergent | size | 0.498 | 0.487 |
| dup_7_3 | emergent | record | 0.471 | 0.483 |

## Team values, receiver gpaw_r2scan

| configuration | inner | outer | isolated | published |
|---|---|---|---|---|
| one_7 | flat | equal |  | 0.439 |
| one_7 | emergent | equal |  | 0.481 |
| split_4_3 | flat | equal | 0.455 | 0.421 |
| split_4_3 | flat | size | 0.450 | 0.415 |
| split_4_3 | flat | record | 0.447 | 0.411 |
| split_4_3 | emergent | equal | 0.498 | 0.465 |
| split_4_3 | emergent | size | 0.499 | 0.453 |
| split_4_3 | emergent | record | 0.485 | 0.445 |
| split_2_5s | flat | equal | 0.472 | 0.436 |
| split_2_5s | flat | size | 0.428 | 0.413 |
| split_2_5s | flat | record | 0.485 | 0.449 |
| split_2_5s | emergent | equal | 0.490 | 0.470 |
| split_2_5s | emergent | size | 0.438 | 0.451 |
| split_2_5s | emergent | record | 0.514 | 0.473 |
| split_2_5w | flat | equal | 0.418 | 0.426 |
| split_2_5w | flat | size | 0.417 | 0.432 |
| split_2_5w | flat | record | 0.416 | 0.420 |
| split_2_5w | emergent | equal | 0.441 | 0.453 |
| split_2_5w | emergent | size | 0.448 | 0.462 |
| split_2_5w | emergent | record | 0.433 | 0.494 |
| split_1_6 | flat | equal | 0.474 | 0.479 |
| split_1_6 | flat | size | 0.456 | 0.428 |
| split_1_6 | flat | record | 0.478 | 0.498 |
| split_1_6 | emergent | equal | 0.482 | 0.501 |
| split_1_6 | emergent | size | 0.458 | 0.456 |
| split_1_6 | emergent | record | 0.492 | 0.505 |
| split_2_2_3 | flat | equal | 0.469 | 0.428 |
| split_2_2_3 | flat | size | 0.466 | 0.407 |
| split_2_2_3 | flat | record | 0.445 | 0.450 |
| split_2_2_3 | emergent | equal | 0.498 | 0.441 |
| split_2_2_3 | emergent | size | 0.475 | 0.416 |
| split_2_2_3 | emergent | record | 0.481 | 0.459 |
| split_1x7 | flat | equal | 0.441 | 0.439 |
| split_1x7 | flat | size | 0.441 | 0.439 |
| split_1x7 | flat | record | 0.462 | 0.439 |
| split_1x7 | emergent | equal | 0.441 | 0.422 |
| split_1x7 | emergent | size | 0.441 | 0.422 |
| split_1x7 | emergent | record | 0.456 | 0.426 |
| dup_7_7 | flat | equal | 0.446 | 0.413 |
| dup_7_7 | flat | size | 0.446 | 0.413 |
| dup_7_7 | flat | record | 0.447 | 0.413 |
| dup_7_7 | emergent | equal | 0.514 | 0.468 |
| dup_7_7 | emergent | size | 0.514 | 0.468 |
| dup_7_7 | emergent | record | 0.504 | 0.460 |
| dup_7_7_7 | flat | equal | 0.456 | 0.415 |
| dup_7_7_7 | flat | size | 0.456 | 0.415 |
| dup_7_7_7 | flat | record | 0.451 | 0.423 |
| dup_7_7_7 | emergent | equal | 0.526 | 0.462 |
| dup_7_7_7 | emergent | size | 0.526 | 0.462 |
| dup_7_7_7 | emergent | record | 0.520 | 0.465 |
| dup_7_3 | flat | equal | 0.431 | 0.419 |
| dup_7_3 | flat | size | 0.424 | 0.433 |
| dup_7_3 | flat | record | 0.430 | 0.418 |
| dup_7_3 | emergent | equal | 0.472 | 0.448 |
| dup_7_3 | emergent | size | 0.481 | 0.465 |
| dup_7_3 | emergent | record | 0.464 | 0.445 |

## Swarm games (Shapley over swarms)

### qe_pbe|split_4_3|emergent|equal|isolated|swarm
v(all) 0.680, v(empty) 0.126
- size 4: Shapley +0.261 (per body +0.065), alone 0.636: mace_relax + gpumd_nep89_md + lammps_meam_md + explorer
- size 3: Shapley +0.293 (per body +0.098), alone 0.667: archive_mp + gpumd_nep89_relax + surrogate

### qe_pbe|split_2_5s|emergent|equal|isolated|swarm
v(all) 0.639, v(empty) 0.126
- size 2: Shapley +0.271 (per body +0.136), alone 0.686: mace_relax + surrogate
- size 5: Shapley +0.242 (per body +0.048), alone 0.656: gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + explorer

### qe_pbe|split_2_5w|emergent|equal|isolated|swarm
v(all) 0.571, v(empty) 0.126
- size 2: Shapley +0.128 (per body +0.064), alone 0.529: gpumd_nep89_md + explorer
- size 5: Shapley +0.317 (per body +0.063), alone 0.717: mace_relax + archive_mp + gpumd_nep89_relax + lammps_meam_md + surrogate

### qe_pbe|split_1_6|emergent|equal|isolated|swarm
v(all) 0.685, v(empty) 0.126
- size 1: Shapley +0.380 (per body +0.380), alone 0.808: mace_relax
- size 6: Shapley +0.179 (per body +0.030), alone 0.607: gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer

### qe_pbe|dup_7_3|emergent|equal|isolated|swarm
v(all) 0.646, v(empty) 0.126
- size 7: Shapley +0.306 (per body +0.044), alone 0.702: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 3: Shapley +0.214 (per body +0.071), alone 0.609: mace_relax@1 + surrogate@1 + explorer@1

### qe_pbe|split_2_2_3|emergent|equal|isolated|swarm
v(all) 0.620, v(empty) 0.126
- size 2: Shapley +0.280 (per body +0.140), alone 0.729: mace_relax + archive_mp
- size 2: Shapley +0.158 (per body +0.079), alone 0.547: gpumd_nep89_md + gpumd_nep89_relax
- size 3: Shapley +0.056 (per body +0.019), alone 0.338: lammps_meam_md + surrogate + explorer

### qe_pbe|split_4_3|emergent|size|isolated|swarm
v(all) 0.675, v(empty) 0.126
- size 4: Shapley +0.259 (per body +0.065), alone 0.636: mace_relax + gpumd_nep89_md + lammps_meam_md + explorer
- size 3: Shapley +0.290 (per body +0.097), alone 0.667: archive_mp + gpumd_nep89_relax + surrogate

### qe_pbe|split_2_5s|emergent|size|isolated|swarm
v(all) 0.661, v(empty) 0.126
- size 2: Shapley +0.282 (per body +0.141), alone 0.686: mace_relax + surrogate
- size 5: Shapley +0.252 (per body +0.050), alone 0.656: gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + explorer

### qe_pbe|dup_7_7|emergent|equal|isolated|swarm
v(all) 0.678, v(empty) 0.126
- size 7: Shapley +0.283 (per body +0.040), alone 0.702: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 7: Shapley +0.269 (per body +0.038), alone 0.687: mace_relax@1 + gpumd_nep89_md@1 + gpumd_nep89_relax@1 + lammps_meam_md@1 + archive_mp@1 + surrogate@1 + explorer@1

### qe_pbe|split_2_5w|emergent|size|isolated|swarm
v(all) 0.643, v(empty) 0.126
- size 2: Shapley +0.164 (per body +0.082), alone 0.529: gpumd_nep89_md + explorer
- size 5: Shapley +0.353 (per body +0.071), alone 0.717: mace_relax + archive_mp + gpumd_nep89_relax + lammps_meam_md + surrogate

### qe_pbe|split_1_6|emergent|size|isolated|swarm
v(all) 0.656, v(empty) 0.126
- size 1: Shapley +0.366 (per body +0.366), alone 0.808: mace_relax
- size 6: Shapley +0.164 (per body +0.027), alone 0.607: gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer

### qe_pbe|split_2_2_3|emergent|size|isolated|swarm
v(all) 0.603, v(empty) 0.126
- size 2: Shapley +0.285 (per body +0.143), alone 0.729: mace_relax + archive_mp
- size 2: Shapley +0.142 (per body +0.071), alone 0.547: gpumd_nep89_md + gpumd_nep89_relax
- size 3: Shapley +0.050 (per body +0.017), alone 0.338: lammps_meam_md + surrogate + explorer

### qe_pbe|dup_7_3|emergent|size|isolated|swarm
v(all) 0.662, v(empty) 0.126
- size 7: Shapley +0.314 (per body +0.045), alone 0.702: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 3: Shapley +0.222 (per body +0.074), alone 0.609: mace_relax@1 + surrogate@1 + explorer@1

### qe_pbe|dup_7_7|emergent|size|isolated|swarm
v(all) 0.678, v(empty) 0.126
- size 7: Shapley +0.283 (per body +0.040), alone 0.702: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 7: Shapley +0.269 (per body +0.038), alone 0.687: mace_relax@1 + gpumd_nep89_md@1 + gpumd_nep89_relax@1 + lammps_meam_md@1 + archive_mp@1 + surrogate@1 + explorer@1

### qe_pbe|dup_7_7_7|emergent|equal|isolated|swarm
v(all) 0.669, v(empty) 0.126
- size 7: Shapley +0.184 (per body +0.026), alone 0.702: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 7: Shapley +0.176 (per body +0.025), alone 0.687: mace_relax@1 + gpumd_nep89_md@1 + gpumd_nep89_relax@1 + lammps_meam_md@1 + archive_mp@1 + surrogate@1 + explorer@1
- size 7: Shapley +0.183 (per body +0.026), alone 0.695: mace_relax@2 + gpumd_nep89_md@2 + gpumd_nep89_relax@2 + lammps_meam_md@2 + archive_mp@2 + surrogate@2 + explorer@2

### qe_pbe|dup_7_7_7|emergent|size|isolated|swarm
v(all) 0.669, v(empty) 0.126
- size 7: Shapley +0.184 (per body +0.026), alone 0.702: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 7: Shapley +0.176 (per body +0.025), alone 0.687: mace_relax@1 + gpumd_nep89_md@1 + gpumd_nep89_relax@1 + lammps_meam_md@1 + archive_mp@1 + surrogate@1 + explorer@1
- size 7: Shapley +0.183 (per body +0.026), alone 0.695: mace_relax@2 + gpumd_nep89_md@2 + gpumd_nep89_relax@2 + lammps_meam_md@2 + archive_mp@2 + surrogate@2 + explorer@2

### qe_pbe|split_1x7|emergent|equal|isolated|swarm
v(all) 0.544, v(empty) 0.126
- size 1: Shapley +0.184 (per body +0.184), alone 0.808: mace_relax
- size 1: Shapley +0.075 (per body +0.075), alone 0.620: gpumd_nep89_md
- size 1: Shapley +0.071 (per body +0.071), alone 0.489: gpumd_nep89_relax
- size 1: Shapley +0.020 (per body +0.020), alone 0.411: lammps_meam_md
- size 1: Shapley +0.135 (per body +0.135), alone 0.771: archive_mp
- size 1: Shapley -0.005 (per body -0.005), alone 0.387: surrogate
- size 1: Shapley -0.063 (per body -0.063), alone 0.126: explorer

### qe_pbe|split_4_3|emergent|equal|published|swarm
v(all) 0.671, v(empty) 0.126
- size 4: Shapley +0.257 (per body +0.064), alone 0.636: mace_relax + gpumd_nep89_md + lammps_meam_md + explorer
- size 3: Shapley +0.288 (per body +0.096), alone 0.667: archive_mp + gpumd_nep89_relax + surrogate

### qe_pbe|split_2_5s|emergent|equal|published|swarm
v(all) 0.654, v(empty) 0.126
- size 2: Shapley +0.279 (per body +0.139), alone 0.686: mace_relax + surrogate
- size 5: Shapley +0.249 (per body +0.050), alone 0.656: gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + explorer

### qe_pbe|split_1x7|emergent|size|isolated|swarm
v(all) 0.544, v(empty) 0.126
- size 1: Shapley +0.184 (per body +0.184), alone 0.808: mace_relax
- size 1: Shapley +0.075 (per body +0.075), alone 0.620: gpumd_nep89_md
- size 1: Shapley +0.071 (per body +0.071), alone 0.489: gpumd_nep89_relax
- size 1: Shapley +0.020 (per body +0.020), alone 0.411: lammps_meam_md
- size 1: Shapley +0.135 (per body +0.135), alone 0.771: archive_mp
- size 1: Shapley -0.005 (per body -0.005), alone 0.387: surrogate
- size 1: Shapley -0.063 (per body -0.063), alone 0.126: explorer

### qe_pbe|split_2_5w|emergent|equal|published|swarm
v(all) 0.604, v(empty) 0.126
- size 2: Shapley +0.145 (per body +0.072), alone 0.529: gpumd_nep89_md + explorer
- size 5: Shapley +0.333 (per body +0.067), alone 0.717: mace_relax + archive_mp + gpumd_nep89_relax + lammps_meam_md + surrogate

### qe_pbe|split_1_6|emergent|equal|published|swarm
v(all) 0.732, v(empty) 0.126
- size 1: Shapley +0.403 (per body +0.403), alone 0.808: mace_relax
- size 6: Shapley +0.202 (per body +0.034), alone 0.607: gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer

### qe_pbe|split_2_2_3|emergent|equal|published|swarm
v(all) 0.623, v(empty) 0.126
- size 2: Shapley +0.288 (per body +0.144), alone 0.729: mace_relax + archive_mp
- size 2: Shapley +0.170 (per body +0.085), alone 0.547: gpumd_nep89_md + gpumd_nep89_relax
- size 3: Shapley +0.038 (per body +0.013), alone 0.338: lammps_meam_md + surrogate + explorer

### qe_pbe|dup_7_7|emergent|equal|published|swarm
v(all) 0.683, v(empty) 0.126
- size 7: Shapley +0.286 (per body +0.041), alone 0.702: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 7: Shapley +0.271 (per body +0.039), alone 0.687: mace_relax@1 + gpumd_nep89_md@1 + gpumd_nep89_relax@1 + lammps_meam_md@1 + archive_mp@1 + surrogate@1 + explorer@1

### qe_pbe|dup_7_3|emergent|equal|published|swarm
v(all) 0.648, v(empty) 0.126
- size 7: Shapley +0.307 (per body +0.044), alone 0.702: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 3: Shapley +0.215 (per body +0.072), alone 0.609: mace_relax@1 + surrogate@1 + explorer@1

### qe_pbe|dup_7_7_7|emergent|equal|published|swarm
v(all) 0.688, v(empty) 0.126
- size 7: Shapley +0.191 (per body +0.027), alone 0.702: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 7: Shapley +0.181 (per body +0.026), alone 0.687: mace_relax@1 + gpumd_nep89_md@1 + gpumd_nep89_relax@1 + lammps_meam_md@1 + archive_mp@1 + surrogate@1 + explorer@1
- size 7: Shapley +0.190 (per body +0.027), alone 0.695: mace_relax@2 + gpumd_nep89_md@2 + gpumd_nep89_relax@2 + lammps_meam_md@2 + archive_mp@2 + surrogate@2 + explorer@2

### qe_pbe|split_4_3|emergent|size|published|swarm
v(all) 0.654, v(empty) 0.126
- size 4: Shapley +0.249 (per body +0.062), alone 0.636: mace_relax + gpumd_nep89_md + lammps_meam_md + explorer
- size 3: Shapley +0.280 (per body +0.093), alone 0.667: archive_mp + gpumd_nep89_relax + surrogate

### qe_pbe|split_2_5s|emergent|size|published|swarm
v(all) 0.663, v(empty) 0.126
- size 2: Shapley +0.283 (per body +0.142), alone 0.686: mace_relax + surrogate
- size 5: Shapley +0.254 (per body +0.051), alone 0.656: gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + explorer

### qe_pbe|split_2_5w|emergent|size|published|swarm
v(all) 0.657, v(empty) 0.126
- size 2: Shapley +0.171 (per body +0.086), alone 0.529: gpumd_nep89_md + explorer
- size 5: Shapley +0.360 (per body +0.072), alone 0.717: mace_relax + archive_mp + gpumd_nep89_relax + lammps_meam_md + surrogate

### qe_pbe|split_1_6|emergent|size|published|swarm
v(all) 0.676, v(empty) 0.126
- size 1: Shapley +0.376 (per body +0.376), alone 0.808: mace_relax
- size 6: Shapley +0.174 (per body +0.029), alone 0.607: gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer

### qe_pbe|split_2_2_3|emergent|size|published|swarm
v(all) 0.617, v(empty) 0.126
- size 2: Shapley +0.282 (per body +0.141), alone 0.729: mace_relax + archive_mp
- size 2: Shapley +0.177 (per body +0.088), alone 0.547: gpumd_nep89_md + gpumd_nep89_relax
- size 3: Shapley +0.032 (per body +0.011), alone 0.338: lammps_meam_md + surrogate + explorer

### qe_pbe|dup_7_7|emergent|size|published|swarm
v(all) 0.683, v(empty) 0.126
- size 7: Shapley +0.286 (per body +0.041), alone 0.702: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 7: Shapley +0.271 (per body +0.039), alone 0.687: mace_relax@1 + gpumd_nep89_md@1 + gpumd_nep89_relax@1 + lammps_meam_md@1 + archive_mp@1 + surrogate@1 + explorer@1

### qe_pbe|dup_7_3|emergent|size|published|swarm
v(all) 0.669, v(empty) 0.126
- size 7: Shapley +0.318 (per body +0.045), alone 0.702: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 3: Shapley +0.225 (per body +0.075), alone 0.609: mace_relax@1 + surrogate@1 + explorer@1

### qe_pbe|dup_7_7_7|emergent|size|published|swarm
v(all) 0.688, v(empty) 0.126
- size 7: Shapley +0.191 (per body +0.027), alone 0.702: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 7: Shapley +0.181 (per body +0.026), alone 0.687: mace_relax@1 + gpumd_nep89_md@1 + gpumd_nep89_relax@1 + lammps_meam_md@1 + archive_mp@1 + surrogate@1 + explorer@1
- size 7: Shapley +0.190 (per body +0.027), alone 0.695: mace_relax@2 + gpumd_nep89_md@2 + gpumd_nep89_relax@2 + lammps_meam_md@2 + archive_mp@2 + surrogate@2 + explorer@2

### qe_pbe|split_1x7|emergent|equal|published|swarm
v(all) 0.597, v(empty) 0.126
- size 1: Shapley +0.168 (per body +0.168), alone 0.808: mace_relax
- size 1: Shapley +0.084 (per body +0.084), alone 0.620: gpumd_nep89_md
- size 1: Shapley +0.081 (per body +0.081), alone 0.489: gpumd_nep89_relax
- size 1: Shapley +0.041 (per body +0.041), alone 0.411: lammps_meam_md
- size 1: Shapley +0.141 (per body +0.141), alone 0.771: archive_mp
- size 1: Shapley +0.015 (per body +0.015), alone 0.387: surrogate
- size 1: Shapley -0.060 (per body -0.060), alone 0.126: explorer

### qe_hse06|split_4_3|emergent|equal|isolated|swarm
v(all) 0.494, v(empty) 0.109
- size 4: Shapley +0.156 (per body +0.039), alone 0.402: mace_relax + gpumd_nep89_md + lammps_meam_md + explorer
- size 3: Shapley +0.229 (per body +0.076), alone 0.475: archive_mp + gpumd_nep89_relax + surrogate

### qe_hse06|split_2_5s|emergent|equal|isolated|swarm
v(all) 0.471, v(empty) 0.109
- size 2: Shapley +0.259 (per body +0.130), alone 0.598: mace_relax + surrogate
- size 5: Shapley +0.103 (per body +0.021), alone 0.441: gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + explorer

### qe_hse06|split_2_5w|emergent|equal|isolated|swarm
v(all) 0.377, v(empty) 0.109
- size 2: Shapley +0.026 (per body +0.013), alone 0.294: gpumd_nep89_md + explorer
- size 5: Shapley +0.242 (per body +0.048), alone 0.510: mace_relax + archive_mp + gpumd_nep89_relax + lammps_meam_md + surrogate

### qe_hse06|split_1_6|emergent|equal|isolated|swarm
v(all) 0.534, v(empty) 0.109
- size 1: Shapley +0.371 (per body +0.371), alone 0.727: mace_relax
- size 6: Shapley +0.054 (per body +0.009), alone 0.409: gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer

### qe_hse06|split_2_2_3|emergent|equal|isolated|swarm
v(all) 0.464, v(empty) 0.109
- size 2: Shapley +0.285 (per body +0.143), alone 0.644: mace_relax + archive_mp
- size 2: Shapley +0.030 (per body +0.015), alone 0.402: gpumd_nep89_md + gpumd_nep89_relax
- size 3: Shapley +0.040 (per body +0.013), alone 0.329: lammps_meam_md + surrogate + explorer

### qe_pbe|split_1x7|emergent|size|published|swarm
v(all) 0.597, v(empty) 0.126
- size 1: Shapley +0.168 (per body +0.168), alone 0.808: mace_relax
- size 1: Shapley +0.084 (per body +0.084), alone 0.620: gpumd_nep89_md
- size 1: Shapley +0.081 (per body +0.081), alone 0.489: gpumd_nep89_relax
- size 1: Shapley +0.041 (per body +0.041), alone 0.411: lammps_meam_md
- size 1: Shapley +0.141 (per body +0.141), alone 0.771: archive_mp
- size 1: Shapley +0.015 (per body +0.015), alone 0.387: surrogate
- size 1: Shapley -0.060 (per body -0.060), alone 0.126: explorer

### qe_hse06|dup_7_3|emergent|equal|isolated|swarm
v(all) 0.484, v(empty) 0.109
- size 7: Shapley +0.217 (per body +0.031), alone 0.503: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 3: Shapley +0.158 (per body +0.053), alone 0.444: mace_relax@1 + surrogate@1 + explorer@1

### qe_hse06|dup_7_7|emergent|equal|isolated|swarm
v(all) 0.508, v(empty) 0.109
- size 7: Shapley +0.199 (per body +0.028), alone 0.503: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 7: Shapley +0.200 (per body +0.029), alone 0.505: mace_relax@1 + gpumd_nep89_md@1 + gpumd_nep89_relax@1 + lammps_meam_md@1 + archive_mp@1 + surrogate@1 + explorer@1

### qe_hse06|dup_7_7_7|emergent|equal|isolated|swarm
v(all) 0.543, v(empty) 0.109
- size 7: Shapley +0.142 (per body +0.020), alone 0.503: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 7: Shapley +0.147 (per body +0.021), alone 0.505: mace_relax@1 + gpumd_nep89_md@1 + gpumd_nep89_relax@1 + lammps_meam_md@1 + archive_mp@1 + surrogate@1 + explorer@1
- size 7: Shapley +0.145 (per body +0.021), alone 0.510: mace_relax@2 + gpumd_nep89_md@2 + gpumd_nep89_relax@2 + lammps_meam_md@2 + archive_mp@2 + surrogate@2 + explorer@2

### qe_hse06|split_4_3|emergent|size|isolated|swarm
v(all) 0.496, v(empty) 0.109
- size 4: Shapley +0.157 (per body +0.039), alone 0.402: mace_relax + gpumd_nep89_md + lammps_meam_md + explorer
- size 3: Shapley +0.230 (per body +0.077), alone 0.475: archive_mp + gpumd_nep89_relax + surrogate

### qe_hse06|split_2_5s|emergent|size|isolated|swarm
v(all) 0.436, v(empty) 0.109
- size 2: Shapley +0.242 (per body +0.121), alone 0.598: mace_relax + surrogate
- size 5: Shapley +0.085 (per body +0.017), alone 0.441: gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + explorer

### qe_hse06|split_2_5w|emergent|size|isolated|swarm
v(all) 0.453, v(empty) 0.109
- size 2: Shapley +0.064 (per body +0.032), alone 0.294: gpumd_nep89_md + explorer
- size 5: Shapley +0.280 (per body +0.056), alone 0.510: mace_relax + archive_mp + gpumd_nep89_relax + lammps_meam_md + surrogate

### qe_hse06|split_1_6|emergent|size|isolated|swarm
v(all) 0.487, v(empty) 0.109
- size 1: Shapley +0.348 (per body +0.348), alone 0.727: mace_relax
- size 6: Shapley +0.030 (per body +0.005), alone 0.409: gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer

### qe_hse06|split_1x7|emergent|equal|isolated|swarm
v(all) 0.402, v(empty) 0.109
- size 1: Shapley +0.195 (per body +0.195), alone 0.727: mace_relax
- size 1: Shapley +0.038 (per body +0.038), alone 0.580: gpumd_nep89_md
- size 1: Shapley +0.007 (per body +0.007), alone 0.180: gpumd_nep89_relax
- size 1: Shapley -0.013 (per body -0.013), alone 0.308: lammps_meam_md
- size 1: Shapley +0.110 (per body +0.110), alone 0.596: archive_mp
- size 1: Shapley -0.017 (per body -0.017), alone 0.286: surrogate
- size 1: Shapley -0.026 (per body -0.026), alone 0.116: explorer

### qe_hse06|split_2_2_3|emergent|size|isolated|swarm
v(all) 0.451, v(empty) 0.109
- size 2: Shapley +0.266 (per body +0.133), alone 0.644: mace_relax + archive_mp
- size 2: Shapley +0.037 (per body +0.019), alone 0.402: gpumd_nep89_md + gpumd_nep89_relax
- size 3: Shapley +0.039 (per body +0.013), alone 0.329: lammps_meam_md + surrogate + explorer

### qe_hse06|dup_7_7|emergent|size|isolated|swarm
v(all) 0.508, v(empty) 0.109
- size 7: Shapley +0.199 (per body +0.028), alone 0.503: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 7: Shapley +0.200 (per body +0.029), alone 0.505: mace_relax@1 + gpumd_nep89_md@1 + gpumd_nep89_relax@1 + lammps_meam_md@1 + archive_mp@1 + surrogate@1 + explorer@1

### qe_hse06|dup_7_3|emergent|size|isolated|swarm
v(all) 0.498, v(empty) 0.109
- size 7: Shapley +0.224 (per body +0.032), alone 0.503: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 3: Shapley +0.165 (per body +0.055), alone 0.444: mace_relax@1 + surrogate@1 + explorer@1

### qe_hse06|dup_7_7_7|emergent|size|isolated|swarm
v(all) 0.543, v(empty) 0.109
- size 7: Shapley +0.142 (per body +0.020), alone 0.503: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 7: Shapley +0.147 (per body +0.021), alone 0.505: mace_relax@1 + gpumd_nep89_md@1 + gpumd_nep89_relax@1 + lammps_meam_md@1 + archive_mp@1 + surrogate@1 + explorer@1
- size 7: Shapley +0.145 (per body +0.021), alone 0.510: mace_relax@2 + gpumd_nep89_md@2 + gpumd_nep89_relax@2 + lammps_meam_md@2 + archive_mp@2 + surrogate@2 + explorer@2

### qe_hse06|split_4_3|emergent|equal|published|swarm
v(all) 0.494, v(empty) 0.109
- size 4: Shapley +0.156 (per body +0.039), alone 0.402: mace_relax + gpumd_nep89_md + lammps_meam_md + explorer
- size 3: Shapley +0.229 (per body +0.076), alone 0.475: archive_mp + gpumd_nep89_relax + surrogate

### qe_hse06|split_2_5s|emergent|equal|published|swarm
v(all) 0.478, v(empty) 0.109
- size 2: Shapley +0.263 (per body +0.131), alone 0.598: mace_relax + surrogate
- size 5: Shapley +0.106 (per body +0.021), alone 0.441: gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + explorer

### qe_hse06|split_2_5w|emergent|equal|published|swarm
v(all) 0.405, v(empty) 0.109
- size 2: Shapley +0.040 (per body +0.020), alone 0.294: gpumd_nep89_md + explorer
- size 5: Shapley +0.256 (per body +0.051), alone 0.510: mace_relax + archive_mp + gpumd_nep89_relax + lammps_meam_md + surrogate

### qe_hse06|split_1_6|emergent|equal|published|swarm
v(all) 0.551, v(empty) 0.109
- size 1: Shapley +0.380 (per body +0.380), alone 0.727: mace_relax
- size 6: Shapley +0.062 (per body +0.010), alone 0.409: gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer

### qe_hse06|split_2_2_3|emergent|equal|published|swarm
v(all) 0.404, v(empty) 0.109
- size 2: Shapley +0.200 (per body +0.100), alone 0.644: mace_relax + archive_mp
- size 2: Shapley +0.063 (per body +0.032), alone 0.402: gpumd_nep89_md + gpumd_nep89_relax
- size 3: Shapley +0.031 (per body +0.010), alone 0.329: lammps_meam_md + surrogate + explorer

### qe_hse06|dup_7_7|emergent|equal|published|swarm
v(all) 0.510, v(empty) 0.109
- size 7: Shapley +0.200 (per body +0.029), alone 0.503: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 7: Shapley +0.201 (per body +0.029), alone 0.505: mace_relax@1 + gpumd_nep89_md@1 + gpumd_nep89_relax@1 + lammps_meam_md@1 + archive_mp@1 + surrogate@1 + explorer@1

### qe_hse06|split_1x7|emergent|size|isolated|swarm
v(all) 0.402, v(empty) 0.109
- size 1: Shapley +0.195 (per body +0.195), alone 0.727: mace_relax
- size 1: Shapley +0.038 (per body +0.038), alone 0.580: gpumd_nep89_md
- size 1: Shapley +0.007 (per body +0.007), alone 0.180: gpumd_nep89_relax
- size 1: Shapley -0.013 (per body -0.013), alone 0.308: lammps_meam_md
- size 1: Shapley +0.110 (per body +0.110), alone 0.596: archive_mp
- size 1: Shapley -0.017 (per body -0.017), alone 0.286: surrogate
- size 1: Shapley -0.026 (per body -0.026), alone 0.116: explorer

### qe_hse06|dup_7_3|emergent|equal|published|swarm
v(all) 0.509, v(empty) 0.109
- size 7: Shapley +0.229 (per body +0.033), alone 0.503: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 3: Shapley +0.170 (per body +0.057), alone 0.444: mace_relax@1 + surrogate@1 + explorer@1

### qe_hse06|dup_7_7_7|emergent|equal|published|swarm
v(all) 0.522, v(empty) 0.109
- size 7: Shapley +0.139 (per body +0.020), alone 0.503: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 7: Shapley +0.133 (per body +0.019), alone 0.505: mace_relax@1 + gpumd_nep89_md@1 + gpumd_nep89_relax@1 + lammps_meam_md@1 + archive_mp@1 + surrogate@1 + explorer@1
- size 7: Shapley +0.140 (per body +0.020), alone 0.510: mace_relax@2 + gpumd_nep89_md@2 + gpumd_nep89_relax@2 + lammps_meam_md@2 + archive_mp@2 + surrogate@2 + explorer@2

### qe_hse06|split_4_3|emergent|size|published|swarm
v(all) 0.472, v(empty) 0.109
- size 4: Shapley +0.145 (per body +0.036), alone 0.402: mace_relax + gpumd_nep89_md + lammps_meam_md + explorer
- size 3: Shapley +0.218 (per body +0.073), alone 0.475: archive_mp + gpumd_nep89_relax + surrogate

### qe_hse06|split_2_5s|emergent|size|published|swarm
v(all) 0.448, v(empty) 0.109
- size 2: Shapley +0.247 (per body +0.124), alone 0.598: mace_relax + surrogate
- size 5: Shapley +0.091 (per body +0.018), alone 0.441: gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + explorer

### qe_hse06|split_2_5w|emergent|size|published|swarm
v(all) 0.471, v(empty) 0.109
- size 2: Shapley +0.073 (per body +0.037), alone 0.294: gpumd_nep89_md + explorer
- size 5: Shapley +0.289 (per body +0.058), alone 0.510: mace_relax + archive_mp + gpumd_nep89_relax + lammps_meam_md + surrogate

### qe_hse06|split_1_6|emergent|size|published|swarm
v(all) 0.469, v(empty) 0.109
- size 1: Shapley +0.338 (per body +0.338), alone 0.727: mace_relax
- size 6: Shapley +0.021 (per body +0.003), alone 0.409: gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer

### qe_hse06|split_2_2_3|emergent|size|published|swarm
v(all) 0.392, v(empty) 0.109
- size 2: Shapley +0.194 (per body +0.097), alone 0.644: mace_relax + archive_mp
- size 2: Shapley +0.067 (per body +0.033), alone 0.402: gpumd_nep89_md + gpumd_nep89_relax
- size 3: Shapley +0.022 (per body +0.007), alone 0.329: lammps_meam_md + surrogate + explorer

### qe_hse06|dup_7_7|emergent|size|published|swarm
v(all) 0.510, v(empty) 0.109
- size 7: Shapley +0.200 (per body +0.029), alone 0.503: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 7: Shapley +0.201 (per body +0.029), alone 0.505: mace_relax@1 + gpumd_nep89_md@1 + gpumd_nep89_relax@1 + lammps_meam_md@1 + archive_mp@1 + surrogate@1 + explorer@1

### qe_hse06|dup_7_3|emergent|size|published|swarm
v(all) 0.487, v(empty) 0.109
- size 7: Shapley +0.218 (per body +0.031), alone 0.503: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 3: Shapley +0.159 (per body +0.053), alone 0.444: mace_relax@1 + surrogate@1 + explorer@1

### qe_hse06|dup_7_7_7|emergent|size|published|swarm
v(all) 0.522, v(empty) 0.109
- size 7: Shapley +0.139 (per body +0.020), alone 0.503: mace_relax + gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- size 7: Shapley +0.133 (per body +0.019), alone 0.505: mace_relax@1 + gpumd_nep89_md@1 + gpumd_nep89_relax@1 + lammps_meam_md@1 + archive_mp@1 + surrogate@1 + explorer@1
- size 7: Shapley +0.140 (per body +0.020), alone 0.510: mace_relax@2 + gpumd_nep89_md@2 + gpumd_nep89_relax@2 + lammps_meam_md@2 + archive_mp@2 + surrogate@2 + explorer@2

### qe_hse06|split_1x7|emergent|equal|published|swarm
v(all) 0.370, v(empty) 0.109
- size 1: Shapley +0.137 (per body +0.137), alone 0.727: mace_relax
- size 1: Shapley +0.030 (per body +0.030), alone 0.580: gpumd_nep89_md
- size 1: Shapley +0.010 (per body +0.010), alone 0.180: gpumd_nep89_relax
- size 1: Shapley +0.008 (per body +0.008), alone 0.308: lammps_meam_md
- size 1: Shapley +0.086 (per body +0.086), alone 0.596: archive_mp
- size 1: Shapley +0.004 (per body +0.004), alone 0.286: surrogate
- size 1: Shapley -0.013 (per body -0.013), alone 0.116: explorer

### qe_hse06|split_1x7|emergent|size|published|swarm
v(all) 0.370, v(empty) 0.109
- size 1: Shapley +0.137 (per body +0.137), alone 0.727: mace_relax
- size 1: Shapley +0.030 (per body +0.030), alone 0.580: gpumd_nep89_md
- size 1: Shapley +0.010 (per body +0.010), alone 0.180: gpumd_nep89_relax
- size 1: Shapley +0.008 (per body +0.008), alone 0.308: lammps_meam_md
- size 1: Shapley +0.086 (per body +0.086), alone 0.596: archive_mp
- size 1: Shapley +0.004 (per body +0.004), alone 0.286: surrogate
- size 1: Shapley -0.013 (per body -0.013), alone 0.116: explorer

## Body games (Owen value with swarms as unions, minus Shapley)

### qe_pbe|split_2_2_3|emergent|equal|isolated|body
unions: mace_relax + archive_mp | gpumd_nep89_md + gpumd_nep89_relax | lammps_meam_md + surrogate + explorer
- mace_relax: Shapley +0.178, Owen +0.172, Owen - Shapley -0.007 [-0.033, +0.020]
- archive_mp: Shapley +0.111, Owen +0.108, Owen - Shapley -0.003 [-0.032, +0.027]
- gpumd_nep89_md: Shapley +0.082, Owen +0.090, Owen - Shapley +0.008 [-0.018, +0.035]
- gpumd_nep89_relax: Shapley +0.077, Owen +0.068, Owen - Shapley -0.010 [-0.037, +0.022]
- lammps_meam_md: Shapley +0.055, Owen +0.062, Owen - Shapley +0.007 [-0.023, +0.035]
- surrogate: Shapley +0.025, Owen +0.035, Owen - Shapley +0.010 [-0.016, +0.042]
- explorer: Shapley -0.034, Owen -0.041, Owen - Shapley -0.006 [-0.042, +0.028]

### qe_pbe|split_4_3|emergent|equal|isolated|body
unions: mace_relax + gpumd_nep89_md + lammps_meam_md + explorer | archive_mp + gpumd_nep89_relax + surrogate
- mace_relax: Shapley +0.216, Owen +0.221, Owen - Shapley +0.005 [-0.017, +0.036]
- gpumd_nep89_md: Shapley +0.084, Owen +0.075, Owen - Shapley -0.010 [-0.031, +0.012]
- lammps_meam_md: Shapley +0.034, Owen +0.004, Owen - Shapley -0.030 [-0.051, -0.006]
- explorer: Shapley -0.030, Owen -0.039, Owen - Shapley -0.009 [-0.030, +0.012]
- archive_mp: Shapley +0.165, Owen +0.205, Owen - Shapley +0.040 [+0.012, +0.066]
- gpumd_nep89_relax: Shapley +0.073, Owen +0.072, Owen - Shapley -0.001 [-0.029, +0.026]
- surrogate: Shapley +0.011, Owen +0.016, Owen - Shapley +0.005 [-0.025, +0.037]

### qe_pbe|split_1_6|emergent|equal|isolated|body
unions: mace_relax | gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- mace_relax: Shapley +0.189, Owen +0.380, Owen - Shapley +0.191 [+0.131, +0.253]
- gpumd_nep89_md: Shapley +0.074, Owen +0.029, Owen - Shapley -0.045 [-0.055, -0.037]
- gpumd_nep89_relax: Shapley +0.088, Owen +0.060, Owen - Shapley -0.028 [-0.040, -0.013]
- lammps_meam_md: Shapley +0.036, Owen +0.003, Owen - Shapley -0.033 [-0.046, -0.019]
- archive_mp: Shapley +0.177, Owen +0.139, Owen - Shapley -0.037 [-0.054, -0.011]
- surrogate: Shapley +0.023, Owen -0.010, Owen - Shapley -0.033 [-0.047, -0.019]
- explorer: Shapley -0.028, Owen -0.043, Owen - Shapley -0.015 [-0.032, -0.001]

### qe_pbe|split_4_3|emergent|size|isolated|body
unions: mace_relax + gpumd_nep89_md + lammps_meam_md + explorer | archive_mp + gpumd_nep89_relax + surrogate
- mace_relax: Shapley +0.222, Owen +0.213, Owen - Shapley -0.008 [-0.031, +0.016]
- gpumd_nep89_md: Shapley +0.079, Owen +0.063, Owen - Shapley -0.016 [-0.036, +0.006]
- lammps_meam_md: Shapley +0.031, Owen +0.009, Owen - Shapley -0.022 [-0.045, +0.002]
- explorer: Shapley -0.030, Owen -0.026, Owen - Shapley +0.004 [-0.016, +0.026]
- archive_mp: Shapley +0.159, Owen +0.187, Owen - Shapley +0.029 [+0.002, +0.057]
- gpumd_nep89_relax: Shapley +0.073, Owen +0.078, Owen - Shapley +0.005 [-0.018, +0.028]
- surrogate: Shapley +0.017, Owen +0.025, Owen - Shapley +0.008 [-0.017, +0.034]

### qe_pbe|split_2_5w|emergent|size|isolated|body
unions: gpumd_nep89_md + explorer | mace_relax + archive_mp + gpumd_nep89_relax + lammps_meam_md + surrogate
- gpumd_nep89_md: Shapley +0.057, Owen +0.198, Owen - Shapley +0.141 [+0.101, +0.181]
- explorer: Shapley -0.047, Owen -0.033, Owen - Shapley +0.014 [-0.021, +0.044]
- mace_relax: Shapley +0.195, Owen +0.152, Owen - Shapley -0.044 [-0.061, -0.027]
- archive_mp: Shapley +0.161, Owen +0.118, Owen - Shapley -0.043 [-0.063, -0.028]
- gpumd_nep89_relax: Shapley +0.078, Owen +0.047, Owen - Shapley -0.031 [-0.047, -0.013]
- lammps_meam_md: Shapley +0.039, Owen +0.026, Owen - Shapley -0.013 [-0.028, -0.000]
- surrogate: Shapley +0.034, Owen +0.010, Owen - Shapley -0.024 [-0.043, +0.000]

### qe_pbe|split_2_5s|emergent|size|isolated|body
unions: mace_relax + surrogate | gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + explorer
- mace_relax: Shapley +0.206, Owen +0.281, Owen - Shapley +0.075 [+0.024, +0.129]
- surrogate: Shapley -0.010, Owen +0.001, Owen - Shapley +0.011 [-0.033, +0.057]
- gpumd_nep89_md: Shapley +0.082, Owen +0.047, Owen - Shapley -0.034 [-0.049, -0.021]
- gpumd_nep89_relax: Shapley +0.073, Owen +0.055, Owen - Shapley -0.018 [-0.032, -0.003]
- lammps_meam_md: Shapley +0.026, Owen +0.017, Owen - Shapley -0.009 [-0.027, +0.011]
- archive_mp: Shapley +0.197, Owen +0.172, Owen - Shapley -0.025 [-0.046, +0.001]
- explorer: Shapley -0.039, Owen -0.040, Owen - Shapley -0.000 [-0.022, +0.026]

### qe_pbe|split_2_2_3|emergent|size|isolated|body
unions: mace_relax + archive_mp | gpumd_nep89_md + gpumd_nep89_relax | lammps_meam_md + surrogate + explorer
- mace_relax: Shapley +0.174, Owen +0.159, Owen - Shapley -0.015 [-0.051, +0.014]
- archive_mp: Shapley +0.134, Owen +0.126, Owen - Shapley -0.008 [-0.039, +0.024]
- gpumd_nep89_md: Shapley +0.072, Owen +0.084, Owen - Shapley +0.011 [-0.019, +0.040]
- gpumd_nep89_relax: Shapley +0.076, Owen +0.058, Owen - Shapley -0.017 [-0.047, +0.015]
- lammps_meam_md: Shapley +0.049, Owen +0.063, Owen - Shapley +0.015 [-0.011, +0.042]
- surrogate: Shapley +0.015, Owen +0.025, Owen - Shapley +0.010 [-0.022, +0.039]
- explorer: Shapley -0.042, Owen -0.038, Owen - Shapley +0.004 [-0.025, +0.033]

### qe_pbe|split_1_6|emergent|size|isolated|body
unions: mace_relax | gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- mace_relax: Shapley +0.176, Owen +0.366, Owen - Shapley +0.189 [+0.120, +0.245]
- gpumd_nep89_md: Shapley +0.079, Owen +0.034, Owen - Shapley -0.045 [-0.055, -0.035]
- gpumd_nep89_relax: Shapley +0.076, Owen +0.049, Owen - Shapley -0.027 [-0.043, -0.011]
- lammps_meam_md: Shapley +0.017, Owen -0.012, Owen - Shapley -0.030 [-0.043, -0.015]
- archive_mp: Shapley +0.214, Owen +0.169, Owen - Shapley -0.045 [-0.062, -0.026]
- surrogate: Shapley +0.011, Owen -0.020, Owen - Shapley -0.031 [-0.045, -0.015]
- explorer: Shapley -0.044, Owen -0.056, Owen - Shapley -0.012 [-0.028, +0.007]

### qe_pbe|split_2_5w|emergent|equal|isolated|body
unions: gpumd_nep89_md + explorer | mace_relax + archive_mp + gpumd_nep89_relax + lammps_meam_md + surrogate
- gpumd_nep89_md: Shapley +0.088, Owen +0.210, Owen - Shapley +0.123 [+0.078, +0.162]
- explorer: Shapley -0.083, Owen -0.082, Owen - Shapley +0.001 [-0.036, +0.037]
- mace_relax: Shapley +0.167, Owen +0.135, Owen - Shapley -0.032 [-0.051, -0.011]
- archive_mp: Shapley +0.139, Owen +0.111, Owen - Shapley -0.028 [-0.046, -0.012]
- gpumd_nep89_relax: Shapley +0.077, Owen +0.052, Owen - Shapley -0.025 [-0.043, -0.005]
- lammps_meam_md: Shapley +0.036, Owen +0.014, Owen - Shapley -0.022 [-0.037, -0.008]
- surrogate: Shapley +0.022, Owen +0.005, Owen - Shapley -0.017 [-0.035, +0.001]

### qe_pbe|split_4_3|emergent|equal|published|body
unions: mace_relax + gpumd_nep89_md + lammps_meam_md + explorer | archive_mp + gpumd_nep89_relax + surrogate
- mace_relax: Shapley +0.217, Owen +0.226, Owen - Shapley +0.010 [-0.018, +0.037]
- gpumd_nep89_md: Shapley +0.084, Owen +0.070, Owen - Shapley -0.014 [-0.036, +0.003]
- lammps_meam_md: Shapley +0.030, Owen +0.005, Owen - Shapley -0.025 [-0.049, -0.002]
- explorer: Shapley -0.037, Owen -0.044, Owen - Shapley -0.008 [-0.032, +0.016]
- archive_mp: Shapley +0.160, Owen +0.193, Owen - Shapley +0.033 [+0.001, +0.063]
- gpumd_nep89_relax: Shapley +0.083, Owen +0.083, Owen - Shapley -0.000 [-0.024, +0.024]
- surrogate: Shapley +0.008, Owen +0.012, Owen - Shapley +0.005 [-0.021, +0.036]

### qe_pbe|split_2_5s|emergent|equal|published|body
unions: mace_relax + surrogate | gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + explorer
- mace_relax: Shapley +0.216, Owen +0.293, Owen - Shapley +0.077 [+0.029, +0.120]
- surrogate: Shapley -0.016, Owen -0.014, Owen - Shapley +0.002 [-0.043, +0.046]
- gpumd_nep89_md: Shapley +0.084, Owen +0.057, Owen - Shapley -0.027 [-0.041, -0.012]
- gpumd_nep89_relax: Shapley +0.082, Owen +0.061, Owen - Shapley -0.021 [-0.040, -0.002]
- lammps_meam_md: Shapley +0.028, Owen +0.013, Owen - Shapley -0.016 [-0.036, +0.002]
- archive_mp: Shapley +0.172, Owen +0.168, Owen - Shapley -0.004 [-0.031, +0.035]
- explorer: Shapley -0.038, Owen -0.049, Owen - Shapley -0.011 [-0.032, +0.011]

### qe_pbe|split_2_2_3|emergent|equal|published|body
unions: mace_relax + archive_mp | gpumd_nep89_md + gpumd_nep89_relax | lammps_meam_md + surrogate + explorer
- mace_relax: Shapley +0.166, Owen +0.169, Owen - Shapley +0.003 [-0.020, +0.025]
- archive_mp: Shapley +0.117, Owen +0.119, Owen - Shapley +0.003 [-0.022, +0.027]
- gpumd_nep89_md: Shapley +0.090, Owen +0.101, Owen - Shapley +0.011 [-0.018, +0.038]
- gpumd_nep89_relax: Shapley +0.078, Owen +0.069, Owen - Shapley -0.010 [-0.035, +0.017]
- lammps_meam_md: Shapley +0.056, Owen +0.063, Owen - Shapley +0.007 [-0.020, +0.038]
- surrogate: Shapley +0.026, Owen +0.029, Owen - Shapley +0.003 [-0.026, +0.036]
- explorer: Shapley -0.035, Owen -0.054, Owen - Shapley -0.018 [-0.052, +0.012]

### qe_pbe|split_1_6|emergent|equal|published|body
unions: mace_relax | gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- mace_relax: Shapley +0.227, Owen +0.403, Owen - Shapley +0.177 [+0.132, +0.227]
- gpumd_nep89_md: Shapley +0.084, Owen +0.041, Owen - Shapley -0.043 [-0.052, -0.035]
- gpumd_nep89_relax: Shapley +0.079, Owen +0.053, Owen - Shapley -0.026 [-0.036, -0.015]
- lammps_meam_md: Shapley +0.031, Owen +0.005, Owen - Shapley -0.025 [-0.037, -0.015]
- archive_mp: Shapley +0.185, Owen +0.144, Owen - Shapley -0.041 [-0.057, -0.019]
- surrogate: Shapley +0.022, Owen -0.008, Owen - Shapley -0.031 [-0.044, -0.017]
- explorer: Shapley -0.022, Owen -0.033, Owen - Shapley -0.011 [-0.025, +0.004]

### qe_pbe|split_4_3|emergent|size|published|body
unions: mace_relax + gpumd_nep89_md + lammps_meam_md + explorer | archive_mp + gpumd_nep89_relax + surrogate
- mace_relax: Shapley +0.218, Owen +0.217, Owen - Shapley -0.001 [-0.028, +0.026]
- gpumd_nep89_md: Shapley +0.082, Owen +0.060, Owen - Shapley -0.021 [-0.040, -0.002]
- lammps_meam_md: Shapley +0.026, Owen +0.002, Owen - Shapley -0.025 [-0.050, -0.001]
- explorer: Shapley -0.034, Owen -0.030, Owen - Shapley +0.004 [-0.014, +0.024]
- archive_mp: Shapley +0.151, Owen +0.185, Owen - Shapley +0.033 [-0.003, +0.060]
- gpumd_nep89_relax: Shapley +0.075, Owen +0.073, Owen - Shapley -0.002 [-0.028, +0.023]
- surrogate: Shapley +0.011, Owen +0.022, Owen - Shapley +0.011 [-0.017, +0.035]

### qe_pbe|split_2_5s|emergent|size|published|body
unions: mace_relax + surrogate | gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + explorer
- mace_relax: Shapley +0.197, Owen +0.278, Owen - Shapley +0.081 [+0.034, +0.129]
- surrogate: Shapley +0.009, Owen +0.005, Owen - Shapley -0.003 [-0.042, +0.039]
- gpumd_nep89_md: Shapley +0.081, Owen +0.054, Owen - Shapley -0.027 [-0.040, -0.013]
- gpumd_nep89_relax: Shapley +0.084, Owen +0.062, Owen - Shapley -0.022 [-0.037, -0.005]
- lammps_meam_md: Shapley +0.030, Owen +0.010, Owen - Shapley -0.020 [-0.036, -0.000]
- archive_mp: Shapley +0.173, Owen +0.167, Owen - Shapley -0.006 [-0.031, +0.027]
- explorer: Shapley -0.036, Owen -0.039, Owen - Shapley -0.003 [-0.026, +0.024]

### qe_pbe|split_2_5w|emergent|size|published|body
unions: gpumd_nep89_md + explorer | mace_relax + archive_mp + gpumd_nep89_relax + lammps_meam_md + surrogate
- gpumd_nep89_md: Shapley +0.073, Owen +0.210, Owen - Shapley +0.136 [+0.093, +0.175]
- explorer: Shapley -0.050, Owen -0.039, Owen - Shapley +0.011 [-0.033, +0.054]
- mace_relax: Shapley +0.200, Owen +0.152, Owen - Shapley -0.048 [-0.067, -0.027]
- archive_mp: Shapley +0.153, Owen +0.113, Owen - Shapley -0.040 [-0.056, -0.023]
- gpumd_nep89_relax: Shapley +0.084, Owen +0.055, Owen - Shapley -0.030 [-0.049, -0.012]
- lammps_meam_md: Shapley +0.044, Owen +0.023, Owen - Shapley -0.021 [-0.038, -0.003]
- surrogate: Shapley +0.026, Owen +0.017, Owen - Shapley -0.009 [-0.029, +0.012]

### qe_pbe|split_2_5s|emergent|equal|isolated|body
unions: mace_relax + surrogate | gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + explorer
- mace_relax: Shapley +0.206, Owen +0.282, Owen - Shapley +0.076 [+0.028, +0.126]
- surrogate: Shapley -0.021, Owen -0.011, Owen - Shapley +0.010 [-0.026, +0.049]
- gpumd_nep89_md: Shapley +0.076, Owen +0.050, Owen - Shapley -0.025 [-0.039, -0.013]
- gpumd_nep89_relax: Shapley +0.078, Owen +0.052, Owen - Shapley -0.026 [-0.045, -0.007]
- lammps_meam_md: Shapley +0.032, Owen +0.010, Owen - Shapley -0.022 [-0.039, -0.003]
- archive_mp: Shapley +0.180, Owen +0.171, Owen - Shapley -0.009 [-0.038, +0.023]
- explorer: Shapley -0.037, Owen -0.041, Owen - Shapley -0.004 [-0.028, +0.018]

### qe_hse06|split_4_3|emergent|equal|isolated|body
unions: mace_relax + gpumd_nep89_md + lammps_meam_md + explorer | archive_mp + gpumd_nep89_relax + surrogate
- mace_relax: Shapley +0.199, Owen +0.188, Owen - Shapley -0.012 [-0.059, +0.029]
- gpumd_nep89_md: Shapley +0.040, Owen +0.016, Owen - Shapley -0.024 [-0.073, +0.022]
- lammps_meam_md: Shapley +0.005, Owen -0.044, Owen - Shapley -0.049 [-0.089, -0.002]
- explorer: Shapley -0.004, Owen -0.003, Owen - Shapley +0.001 [-0.044, +0.044]
- archive_mp: Shapley +0.151, Owen +0.226, Owen - Shapley +0.075 [+0.017, +0.132]
- gpumd_nep89_relax: Shapley -0.007, Owen +0.005, Owen - Shapley +0.013 [-0.040, +0.068]
- surrogate: Shapley +0.002, Owen -0.002, Owen - Shapley -0.004 [-0.058, +0.046]

### qe_hse06|split_2_5s|emergent|equal|isolated|body
unions: mace_relax + surrogate | gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + explorer
- mace_relax: Shapley +0.204, Owen +0.287, Owen - Shapley +0.084 [-0.004, +0.168]
- surrogate: Shapley -0.029, Owen -0.028, Owen - Shapley +0.001 [-0.058, +0.063]
- gpumd_nep89_md: Shapley +0.042, Owen +0.017, Owen - Shapley -0.024 [-0.046, -0.004]
- gpumd_nep89_relax: Shapley +0.022, Owen +0.002, Owen - Shapley -0.020 [-0.049, +0.010]
- lammps_meam_md: Shapley -0.003, Owen -0.037, Owen - Shapley -0.034 [-0.060, -0.005]
- archive_mp: Shapley +0.139, Owen +0.128, Owen - Shapley -0.011 [-0.039, +0.023]
- explorer: Shapley -0.013, Owen -0.008, Owen - Shapley +0.005 [-0.031, +0.034]

### qe_hse06|split_2_5w|emergent|equal|isolated|body
unions: gpumd_nep89_md + explorer | mace_relax + archive_mp + gpumd_nep89_relax + lammps_meam_md + surrogate
- gpumd_nep89_md: Shapley +0.005, Owen +0.116, Owen - Shapley +0.112 [+0.049, +0.172]
- explorer: Shapley -0.050, Owen -0.090, Owen - Shapley -0.040 [-0.098, +0.015]
- mace_relax: Shapley +0.167, Owen +0.143, Owen - Shapley -0.023 [-0.053, +0.012]
- archive_mp: Shapley +0.134, Owen +0.122, Owen - Shapley -0.011 [-0.036, +0.018]
- gpumd_nep89_relax: Shapley -0.004, Owen -0.002, Owen - Shapley +0.002 [-0.021, +0.027]
- lammps_meam_md: Shapley -0.002, Owen -0.029, Owen - Shapley -0.027 [-0.057, -0.002]
- surrogate: Shapley +0.019, Owen +0.007, Owen - Shapley -0.012 [-0.039, +0.013]

### qe_hse06|split_2_2_3|emergent|equal|isolated|body
unions: mace_relax + archive_mp | gpumd_nep89_md + gpumd_nep89_relax | lammps_meam_md + surrogate + explorer
- mace_relax: Shapley +0.183, Owen +0.188, Owen - Shapley +0.005 [-0.047, +0.049]
- archive_mp: Shapley +0.094, Owen +0.097, Owen - Shapley +0.003 [-0.034, +0.051]
- gpumd_nep89_md: Shapley +0.050, Owen +0.081, Owen - Shapley +0.031 [-0.027, +0.091]
- gpumd_nep89_relax: Shapley -0.009, Owen -0.051, Owen - Shapley -0.042 [-0.104, +0.015]
- lammps_meam_md: Shapley +0.028, Owen +0.036, Owen - Shapley +0.008 [-0.038, +0.051]
- surrogate: Shapley +0.017, Owen +0.015, Owen - Shapley -0.002 [-0.053, +0.034]
- explorer: Shapley -0.009, Owen -0.011, Owen - Shapley -0.002 [-0.048, +0.040]

### qe_hse06|split_1_6|emergent|equal|isolated|body
unions: mace_relax | gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- mace_relax: Shapley +0.197, Owen +0.371, Owen - Shapley +0.175 [+0.096, +0.243]
- gpumd_nep89_md: Shapley +0.044, Owen -0.007, Owen - Shapley -0.052 [-0.064, -0.037]
- gpumd_nep89_relax: Shapley +0.016, Owen -0.001, Owen - Shapley -0.017 [-0.034, +0.001]
- lammps_meam_md: Shapley +0.008, Owen -0.032, Owen - Shapley -0.039 [-0.060, -0.020]
- archive_mp: Shapley +0.138, Owen +0.104, Owen - Shapley -0.033 [-0.050, -0.013]
- surrogate: Shapley +0.026, Owen +0.001, Owen - Shapley -0.025 [-0.049, +0.004]
- explorer: Shapley -0.004, Owen -0.012, Owen - Shapley -0.008 [-0.024, +0.014]

### qe_pbe|split_1_6|emergent|size|published|body
unions: mace_relax | gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- mace_relax: Shapley +0.189, Owen +0.376, Owen - Shapley +0.187 [+0.132, +0.240]
- gpumd_nep89_md: Shapley +0.077, Owen +0.033, Owen - Shapley -0.044 [-0.053, -0.035]
- gpumd_nep89_relax: Shapley +0.080, Owen +0.051, Owen - Shapley -0.029 [-0.040, -0.016]
- lammps_meam_md: Shapley +0.027, Owen +0.001, Owen - Shapley -0.026 [-0.037, -0.015]
- archive_mp: Shapley +0.198, Owen +0.153, Owen - Shapley -0.045 [-0.065, -0.021]
- surrogate: Shapley +0.014, Owen -0.018, Owen - Shapley -0.032 [-0.044, -0.013]
- explorer: Shapley -0.034, Owen -0.046, Owen - Shapley -0.012 [-0.027, +0.002]

### qe_pbe|split_2_2_3|emergent|size|published|body
unions: mace_relax + archive_mp | gpumd_nep89_md + gpumd_nep89_relax | lammps_meam_md + surrogate + explorer
- mace_relax: Shapley +0.165, Owen +0.152, Owen - Shapley -0.014 [-0.037, +0.008]
- archive_mp: Shapley +0.134, Owen +0.130, Owen - Shapley -0.004 [-0.031, +0.022]
- gpumd_nep89_md: Shapley +0.084, Owen +0.099, Owen - Shapley +0.015 [-0.011, +0.049]
- gpumd_nep89_relax: Shapley +0.084, Owen +0.078, Owen - Shapley -0.007 [-0.034, +0.014]
- lammps_meam_md: Shapley +0.045, Owen +0.048, Owen - Shapley +0.003 [-0.024, +0.033]
- surrogate: Shapley +0.019, Owen +0.028, Owen - Shapley +0.009 [-0.021, +0.037]
- explorer: Shapley -0.041, Owen -0.044, Owen - Shapley -0.003 [-0.031, +0.024]

### qe_pbe|split_2_5w|emergent|equal|published|body
unions: gpumd_nep89_md + explorer | mace_relax + archive_mp + gpumd_nep89_relax + lammps_meam_md + surrogate
- gpumd_nep89_md: Shapley +0.112, Owen +0.215, Owen - Shapley +0.104 [+0.068, +0.149]
- explorer: Shapley -0.078, Owen -0.071, Owen - Shapley +0.008 [-0.033, +0.048]
- mace_relax: Shapley +0.184, Owen +0.153, Owen - Shapley -0.031 [-0.051, -0.013]
- archive_mp: Shapley +0.138, Owen +0.107, Owen - Shapley -0.031 [-0.047, -0.014]
- gpumd_nep89_relax: Shapley +0.071, Owen +0.050, Owen - Shapley -0.022 [-0.039, -0.003]
- lammps_meam_md: Shapley +0.033, Owen +0.016, Owen - Shapley -0.017 [-0.040, +0.003]
- surrogate: Shapley +0.017, Owen +0.007, Owen - Shapley -0.010 [-0.036, +0.016]

### qe_hse06|split_4_3|emergent|size|isolated|body
unions: mace_relax + gpumd_nep89_md + lammps_meam_md + explorer | archive_mp + gpumd_nep89_relax + surrogate
- mace_relax: Shapley +0.198, Owen +0.180, Owen - Shapley -0.018 [-0.062, +0.027]
- gpumd_nep89_md: Shapley +0.034, Owen +0.012, Owen - Shapley -0.022 [-0.067, +0.013]
- lammps_meam_md: Shapley -0.002, Owen -0.030, Owen - Shapley -0.028 [-0.072, +0.016]
- explorer: Shapley -0.011, Owen -0.005, Owen - Shapley +0.006 [-0.028, +0.041]
- archive_mp: Shapley +0.157, Owen +0.208, Owen - Shapley +0.051 [+0.003, +0.104]
- gpumd_nep89_relax: Shapley +0.006, Owen +0.018, Owen - Shapley +0.012 [-0.043, +0.067]
- surrogate: Shapley +0.005, Owen +0.005, Owen - Shapley -0.001 [-0.051, +0.051]

### qe_hse06|split_2_5w|emergent|size|isolated|body
unions: gpumd_nep89_md + explorer | mace_relax + archive_mp + gpumd_nep89_relax + lammps_meam_md + surrogate
- gpumd_nep89_md: Shapley +0.015, Owen +0.139, Owen - Shapley +0.124 [+0.058, +0.194]
- explorer: Shapley -0.031, Owen -0.075, Owen - Shapley -0.044 [-0.104, +0.012]
- mace_relax: Shapley +0.185, Owen +0.163, Owen - Shapley -0.022 [-0.050, +0.001]
- archive_mp: Shapley +0.165, Owen +0.139, Owen - Shapley -0.026 [-0.056, +0.001]
- gpumd_nep89_relax: Shapley -0.005, Owen -0.003, Owen - Shapley +0.002 [-0.025, +0.030]
- lammps_meam_md: Shapley -0.004, Owen -0.020, Owen - Shapley -0.016 [-0.045, +0.008]
- surrogate: Shapley +0.019, Owen +0.002, Owen - Shapley -0.017 [-0.052, +0.016]

### qe_hse06|split_2_2_3|emergent|size|isolated|body
unions: mace_relax + archive_mp | gpumd_nep89_md + gpumd_nep89_relax | lammps_meam_md + surrogate + explorer
- mace_relax: Shapley +0.174, Owen +0.174, Owen - Shapley -0.001 [-0.048, +0.052]
- archive_mp: Shapley +0.100, Owen +0.092, Owen - Shapley -0.007 [-0.051, +0.051]
- gpumd_nep89_md: Shapley +0.026, Owen +0.075, Owen - Shapley +0.050 [-0.012, +0.109]
- gpumd_nep89_relax: Shapley -0.007, Owen -0.038, Owen - Shapley -0.031 [-0.090, +0.022]
- lammps_meam_md: Shapley +0.040, Owen +0.052, Owen - Shapley +0.012 [-0.031, +0.052]
- surrogate: Shapley +0.017, Owen -0.002, Owen - Shapley -0.019 [-0.070, +0.037]
- explorer: Shapley -0.007, Owen -0.011, Owen - Shapley -0.004 [-0.044, +0.028]

### qe_hse06|split_1_6|emergent|size|isolated|body
unions: mace_relax | gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- mace_relax: Shapley +0.182, Owen +0.348, Owen - Shapley +0.166 [+0.081, +0.244]
- gpumd_nep89_md: Shapley +0.044, Owen -0.006, Owen - Shapley -0.050 [-0.064, -0.036]
- gpumd_nep89_relax: Shapley +0.002, Owen -0.014, Owen - Shapley -0.016 [-0.033, -0.000]
- lammps_meam_md: Shapley -0.007, Owen -0.042, Owen - Shapley -0.035 [-0.054, -0.015]
- archive_mp: Shapley +0.146, Owen +0.115, Owen - Shapley -0.031 [-0.048, -0.010]
- surrogate: Shapley +0.020, Owen -0.005, Owen - Shapley -0.025 [-0.050, +0.002]
- explorer: Shapley -0.009, Owen -0.017, Owen - Shapley -0.009 [-0.029, +0.009]

### qe_hse06|split_4_3|emergent|equal|published|body
unions: mace_relax + gpumd_nep89_md + lammps_meam_md + explorer | archive_mp + gpumd_nep89_relax + surrogate
- mace_relax: Shapley +0.211, Owen +0.211, Owen - Shapley -0.000 [-0.043, +0.051]
- gpumd_nep89_md: Shapley +0.042, Owen +0.025, Owen - Shapley -0.017 [-0.065, +0.027]
- lammps_meam_md: Shapley -0.024, Owen -0.068, Owen - Shapley -0.043 [-0.087, -0.004]
- explorer: Shapley -0.009, Owen -0.012, Owen - Shapley -0.003 [-0.047, +0.032]
- archive_mp: Shapley +0.156, Owen +0.224, Owen - Shapley +0.069 [+0.010, +0.126]
- gpumd_nep89_relax: Shapley +0.010, Owen +0.008, Owen - Shapley -0.002 [-0.063, +0.052]
- surrogate: Shapley -0.000, Owen -0.003, Owen - Shapley -0.003 [-0.059, +0.057]

### qe_hse06|split_2_5s|emergent|equal|published|body
unions: mace_relax + surrogate | gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + explorer
- mace_relax: Shapley +0.204, Owen +0.295, Owen - Shapley +0.091 [+0.011, +0.179]
- surrogate: Shapley -0.029, Owen -0.032, Owen - Shapley -0.004 [-0.051, +0.052]
- gpumd_nep89_md: Shapley +0.050, Owen +0.010, Owen - Shapley -0.040 [-0.063, -0.017]
- gpumd_nep89_relax: Shapley +0.010, Owen -0.009, Owen - Shapley -0.018 [-0.048, +0.015]
- lammps_meam_md: Shapley -0.022, Owen -0.052, Owen - Shapley -0.031 [-0.060, +0.003]
- archive_mp: Shapley +0.172, Owen +0.171, Owen - Shapley -0.001 [-0.042, +0.035]
- explorer: Shapley -0.017, Owen -0.014, Owen - Shapley +0.003 [-0.030, +0.034]

### qe_hse06|split_2_5w|emergent|equal|published|body
unions: gpumd_nep89_md + explorer | mace_relax + archive_mp + gpumd_nep89_relax + lammps_meam_md + surrogate
- gpumd_nep89_md: Shapley +0.017, Owen +0.122, Owen - Shapley +0.105 [+0.038, +0.175]
- explorer: Shapley -0.026, Owen -0.082, Owen - Shapley -0.056 [-0.127, +0.009]
- mace_relax: Shapley +0.153, Owen +0.148, Owen - Shapley -0.005 [-0.041, +0.029]
- archive_mp: Shapley +0.122, Owen +0.117, Owen - Shapley -0.005 [-0.033, +0.027]
- gpumd_nep89_relax: Shapley +0.008, Owen +0.006, Owen - Shapley -0.002 [-0.041, +0.032]
- lammps_meam_md: Shapley +0.005, Owen -0.021, Owen - Shapley -0.026 [-0.056, -0.001]
- surrogate: Shapley +0.018, Owen +0.006, Owen - Shapley -0.011 [-0.051, +0.026]

### qe_hse06|split_1_6|emergent|equal|published|body
unions: mace_relax | gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- mace_relax: Shapley +0.209, Owen +0.380, Owen - Shapley +0.170 [+0.086, +0.240]
- gpumd_nep89_md: Shapley +0.053, Owen +0.004, Owen - Shapley -0.049 [-0.059, -0.036]
- gpumd_nep89_relax: Shapley +0.009, Owen -0.003, Owen - Shapley -0.012 [-0.024, +0.000]
- lammps_meam_md: Shapley -0.018, Owen -0.052, Owen - Shapley -0.034 [-0.053, -0.015]
- archive_mp: Shapley +0.186, Owen +0.151, Owen - Shapley -0.035 [-0.055, -0.008]
- surrogate: Shapley +0.011, Owen -0.018, Owen - Shapley -0.029 [-0.057, +0.002]
- explorer: Shapley -0.009, Owen -0.019, Owen - Shapley -0.010 [-0.029, +0.010]

### qe_hse06|split_2_5s|emergent|size|isolated|body
unions: mace_relax + surrogate | gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + explorer
- mace_relax: Shapley +0.202, Owen +0.259, Owen - Shapley +0.058 [-0.028, +0.137]
- surrogate: Shapley -0.025, Owen -0.018, Owen - Shapley +0.007 [-0.050, +0.060]
- gpumd_nep89_md: Shapley +0.039, Owen +0.010, Owen - Shapley -0.029 [-0.052, -0.003]
- gpumd_nep89_relax: Shapley -0.002, Owen -0.012, Owen - Shapley -0.009 [-0.035, +0.018]
- lammps_meam_md: Shapley -0.015, Owen -0.028, Owen - Shapley -0.013 [-0.036, +0.013]
- archive_mp: Shapley +0.148, Owen +0.130, Owen - Shapley -0.019 [-0.050, +0.020]
- explorer: Shapley -0.020, Owen -0.015, Owen - Shapley +0.005 [-0.024, +0.036]

### qe_hse06|split_2_2_3|emergent|equal|published|body
unions: mace_relax + archive_mp | gpumd_nep89_md + gpumd_nep89_relax | lammps_meam_md + surrogate + explorer
- mace_relax: Shapley +0.131, Owen +0.148, Owen - Shapley +0.016 [-0.032, +0.061]
- archive_mp: Shapley +0.061, Owen +0.052, Owen - Shapley -0.009 [-0.064, +0.038]
- gpumd_nep89_md: Shapley +0.054, Owen +0.086, Owen - Shapley +0.032 [-0.035, +0.092]
- gpumd_nep89_relax: Shapley +0.025, Owen -0.023, Owen - Shapley -0.048 [-0.120, +0.010]
- lammps_meam_md: Shapley +0.022, Owen +0.039, Owen - Shapley +0.018 [-0.034, +0.061]
- surrogate: Shapley +0.006, Owen +0.008, Owen - Shapley +0.002 [-0.045, +0.047]
- explorer: Shapley -0.004, Owen -0.016, Owen - Shapley -0.012 [-0.067, +0.037]

### qe_hse06|split_2_5s|emergent|size|published|body
unions: mace_relax + surrogate | gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + explorer
- mace_relax: Shapley +0.179, Owen +0.261, Owen - Shapley +0.083 [+0.006, +0.169]
- surrogate: Shapley -0.005, Owen -0.014, Owen - Shapley -0.009 [-0.054, +0.039]
- gpumd_nep89_md: Shapley +0.043, Owen +0.003, Owen - Shapley -0.041 [-0.061, -0.014]
- gpumd_nep89_relax: Shapley +0.009, Owen -0.007, Owen - Shapley -0.015 [-0.038, +0.014]
- lammps_meam_md: Shapley -0.030, Owen -0.058, Owen - Shapley -0.027 [-0.056, -0.001]
- archive_mp: Shapley +0.165, Owen +0.166, Owen - Shapley +0.001 [-0.037, +0.032]
- explorer: Shapley -0.022, Owen -0.013, Owen - Shapley +0.009 [-0.022, +0.041]

### qe_hse06|split_4_3|emergent|size|published|body
unions: mace_relax + gpumd_nep89_md + lammps_meam_md + explorer | archive_mp + gpumd_nep89_relax + surrogate
- mace_relax: Shapley +0.207, Owen +0.203, Owen - Shapley -0.004 [-0.049, +0.038]
- gpumd_nep89_md: Shapley +0.035, Owen +0.016, Owen - Shapley -0.019 [-0.060, +0.020]
- lammps_meam_md: Shapley -0.027, Owen -0.067, Owen - Shapley -0.040 [-0.080, +0.001]
- explorer: Shapley -0.010, Owen -0.006, Owen - Shapley +0.004 [-0.033, +0.045]
- archive_mp: Shapley +0.152, Owen +0.218, Owen - Shapley +0.066 [+0.014, +0.121]
- gpumd_nep89_relax: Shapley +0.004, Owen +0.004, Owen - Shapley -0.000 [-0.053, +0.051]
- surrogate: Shapley +0.002, Owen -0.004, Owen - Shapley -0.006 [-0.062, +0.044]

### qe_hse06|split_2_2_3|emergent|size|published|body
unions: mace_relax + archive_mp | gpumd_nep89_md + gpumd_nep89_relax | lammps_meam_md + surrogate + explorer
- mace_relax: Shapley +0.126, Owen +0.122, Owen - Shapley -0.004 [-0.051, +0.042]
- archive_mp: Shapley +0.079, Owen +0.072, Owen - Shapley -0.007 [-0.055, +0.042]
- gpumd_nep89_md: Shapley +0.042, Owen +0.070, Owen - Shapley +0.028 [-0.044, +0.092]
- gpumd_nep89_relax: Shapley +0.031, Owen -0.004, Owen - Shapley -0.035 [-0.097, +0.027]
- lammps_meam_md: Shapley +0.010, Owen +0.020, Owen - Shapley +0.010 [-0.031, +0.051]
- surrogate: Shapley +0.001, Owen +0.008, Owen - Shapley +0.007 [-0.042, +0.049]
- explorer: Shapley -0.007, Owen -0.006, Owen - Shapley +0.001 [-0.050, +0.048]

### qe_hse06|split_2_5w|emergent|size|published|body
unions: gpumd_nep89_md + explorer | mace_relax + archive_mp + gpumd_nep89_relax + lammps_meam_md + surrogate
- gpumd_nep89_md: Shapley +0.008, Owen +0.156, Owen - Shapley +0.148 [+0.082, +0.213]
- explorer: Shapley -0.015, Owen -0.083, Owen - Shapley -0.068 [-0.130, +0.009]
- mace_relax: Shapley +0.173, Owen +0.149, Owen - Shapley -0.024 [-0.055, +0.012]
- archive_mp: Shapley +0.135, Owen +0.121, Owen - Shapley -0.015 [-0.050, +0.016]
- gpumd_nep89_relax: Shapley +0.019, Owen +0.014, Owen - Shapley -0.005 [-0.032, +0.021]
- lammps_meam_md: Shapley +0.009, Owen -0.016, Owen - Shapley -0.025 [-0.052, +0.003]
- surrogate: Shapley +0.033, Owen +0.022, Owen - Shapley -0.011 [-0.048, +0.019]

### qe_hse06|split_1_6|emergent|size|published|body
unions: mace_relax | gpumd_nep89_md + gpumd_nep89_relax + lammps_meam_md + archive_mp + surrogate + explorer
- mace_relax: Shapley +0.164, Owen +0.338, Owen - Shapley +0.174 [+0.096, +0.241]
- gpumd_nep89_md: Shapley +0.044, Owen -0.006, Owen - Shapley -0.050 [-0.061, -0.037]
- gpumd_nep89_relax: Shapley +0.010, Owen -0.006, Owen - Shapley -0.015 [-0.028, +0.000]
- lammps_meam_md: Shapley -0.030, Owen -0.064, Owen - Shapley -0.034 [-0.049, -0.017]
- archive_mp: Shapley +0.189, Owen +0.153, Owen - Shapley -0.036 [-0.056, -0.017]
- surrogate: Shapley +0.003, Owen -0.026, Owen - Shapley -0.029 [-0.053, +0.006]
- explorer: Shapley -0.021, Owen -0.030, Owen - Shapley -0.009 [-0.027, +0.008]

