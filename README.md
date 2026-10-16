# ATEKi

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23413476.svg)](https://doi.org/10.5281/zenodo.23413476)

**Paper.** Fairly Dividing a Discovery Campaign's Outcome Among Its Members, Meetings, and Borrowed Knowledge (submitted to Transactions on Machine Learning Research).

This repository holds the code and data behind the paper: the scripts that draw its figures, the result files they read, the code that produced those results, and the archived or computed inputs that code reads. The manuscript itself is not part of the repository. Every script runs unchanged from the repository root.

**Authors.** Kinston Ackölf, Taylor D. Sparks, Materials Science and Engineering, The University of Utah.

**Citation.** `CITATION.cff` (software citation) and `.zenodo.json` (archive metadata).

## Layout

- `shared/`, `compute/`, `ateki/`, `campaign_protocols/`: result files and the code that produced them.
- `writings/papers_2026/regen_figs/` and `paper_fig_style.py`: figure scripts (each reads only committed result files and draws at print size into `writings/papers_2026/<paper>/figures/`).

## Running

Figures: run a script from the folder root, for example `python writings/papers_2026/regen_figs/<script>.py` (environment: `writings/papers_2026/regen_figs/requirements.txt`). `REPRODUCE.md` gives the full procedure: software versions, the rebuild of the band-gap archive, the commands that regenerate every result file, and the DFT, MD and potential calculations behind the computed records.

## Figure scripts

| Figure | Script | Files read |
|---|---|---|
| `06_physics_prior_attribution.png` | `writings/papers_2026/regen_figs/ateki_physics_prior.py` | `ateki/results/physics_attribution/06_physics_prior_attribution.json`, `ateki/results/physics_attribution/06_physics_prior_attribution_per_run.json` |
| `07_campaign_attribution.png` | `writings/papers_2026/regen_figs/ateki_campaign_attribution.py` | `ateki/results/campaign_attribution/k4_50seed/07_campaign_attribution.json` |
| `worked_example_ateki.png` | `writings/papers_2026/regen_figs/worked_example_ateki.py` | `ateki/results/database_attribution/coalitions/expt_zhuo/0.json`, `ateki/results/database_attribution/coalitions/expt_zhuo/1.json`, `ateki/results/database_attribution/coalitions/expt_zhuo/10.json`, `ateki/results/database_attribution/coalitions/expt_zhuo/100.json` and 125 more |
| `database_attribution.png` | `writings/papers_2026/regen_figs/ateki_database_attribution.py` | `ateki/results/database_attribution/expt_zhuo/database_attribution.json` |
| `recorded_meetings.pdf` | `writings/papers_2026/regen_figs/ateki_recorded_meetings.py` | `ateki/results/recorded_meetings/campaigns/flat_s0.json`, `ateki/results/recorded_meetings/campaigns/flat_s1.json`, `ateki/results/recorded_meetings/campaigns/flat_s2.json`, `ateki/results/recorded_meetings/campaigns/flat_s3.json` and 8 more |
| `live_attribution.png` | `writings/papers_2026/regen_figs/live_almgsi_figs.py` | `compute/almgsi_campaign/candidates_index.json`, `compute/almgsi_campaign/results/analysis/source_agreement.json`, `compute/almgsi_campaign/results/campaigns/qe_hse06_all/summary.json`, `compute/almgsi_campaign/results/campaigns/qe_pbe_all/summary.json` and 11 more |
| `harsanyi_dividends.png` | `writings/papers_2026/regen_figs/ateki_harsanyi_dividends.py` | `ateki/results/harsanyi_dividends/expt_zhuo/harsanyi_dividends.json` |
| `compute_credit.png` | `writings/papers_2026/regen_figs/ateki_compute_credit.py` | `compute/almgsi_campaign/results/campaigns/qe_hse06_shapley_coalitions/coalitions.json`, `compute/almgsi_campaign/results/campaigns/qe_hse06_shapley_combined/coalitions.json`, `compute/almgsi_campaign/results/campaigns/qe_pbe_shapley_coalitions/coalitions.json`, `compute/semiconductor_campaign/results/campaigns/qe_hse06_nohalide/coalitions.json` and 3 more |
| `emergent_swarm.pdf` | `writings/papers_2026/regen_figs/ateki_emergent_swarm.py` | `ateki/results/emergent_swarm/shapley.json`, `ateki/results/emergent_swarm/team_values.json` |
| `emergent_swarm_dynamics.pdf` | `writings/papers_2026/regen_figs/ateki_emergent_swarm.py` | `ateki/results/emergent_swarm/shapley.json`, `ateki/results/emergent_swarm/team_values.json` |
| `shared_member_credit.pdf` | `writings/papers_2026/regen_figs/ateki_unequal_credit.py` | `ateki/results/unequal_credit/part_a.json`, `ateki/results/unequal_credit/part_b.json` |
| `replicated_bodies.pdf` | `writings/papers_2026/regen_figs/ateki_replicated_bodies.py` | `ateki/results/replicated_bodies/replicated_bodies.json` |
| `multiple_swarms.pdf` | `writings/papers_2026/regen_figs/ateki_multiple_swarms.py` | `ateki/results/multiple_swarms/games.json`, `ateki/results/multiple_swarms/team_values.json` |
| `morphing_swarms.pdf` | `writings/papers_2026/regen_figs/ateki_morphing_swarms.py` | `ateki/results/morphing_swarms/games.json`, `ateki/results/morphing_swarms/team_values.json` |
| `mobile_members.pdf` | `writings/papers_2026/regen_figs/ateki_mobile_members.py` | `ateki/results/mobile_members/games.json`, `ateki/results/mobile_members/team_values.json`, `ateki/results/morphing_swarms/team_values.json` |
| `unequal_credit.pdf` | `writings/papers_2026/regen_figs/ateki_unequal_credit.py` | `ateki/results/unequal_credit/part_a.json`, `ateki/results/unequal_credit/part_b.json` |

## Producing code

The result files above were written by these scripts (local modules they import are included as well):

- `ateki/experiments/06_physics_prior_attribution.py`
- `ateki/experiments/07_campaign_attribution.py`
- `ateki/experiments/08_database_attribution.py`
- `ateki/experiments/09_harsanyi_dividends.py`
- `ateki/experiments/10_materials_structure_attribution.py`
- `ateki/experiments/11_recorded_meetings.py`
- `ateki/experiments/12_component_rule.py`
- `ateki/results/recorded_meetings/analyze_meetings.py`
- `ateki/experiments/13_recorded_meetings_coordinator.py`
- `ateki/results/recorded_meetings_scale/analyze_scale.py`
- `ateki/results/recorded_meetings_coordinator/analyze_coordinator.py`
- `campaign_protocols/code/experiments/26_paired_campaign.py`
- `campaign_protocols/code/experiments/25_physics_informed_budget.py`
- `compute/bandgap_archive/build_inventory.py`
- `compute/almgsi_campaign/generate_candidates.py`
- `compute/almgsi_campaign/add_observed_phases.py`
- `compute/almgsi_campaign/dgx_sources.py`
- `compute/almgsi_campaign/aggregate_sources.py`
- `compute/almgsi_campaign/analyze_live.py`
- `compute/almgsi_campaign/campaign.py`
- `compute/almgsi_campaign/live_campaign.py`
- `compute/almgsi_campaign/compare_live_replay.py`
- `compute/almgsi_campaign/temperature_study.py`
- `compute/almgsi_campaign/dft_receiver_study.py`
- `compute/semiconductor_campaign/generate_pool.py`
- `compute/semiconductor_campaign/archive_donors.py`
- `compute/semiconductor_campaign/campaign_gap.py`
- `compute/semiconductor_campaign/summarise.py`
- `compute/semiconductor_campaign/shapley_per_run.py`
- `ateki/experiments/14_emergent_swarm.py`
- `ateki/experiments/15_replicated_bodies.py`
- `ateki/experiments/16_multiple_swarms.py`
- `ateki/experiments/17_morphing_swarms.py`
- `ateki/experiments/18_mobile_members.py`
- `ateki/experiments/19_unequal_credit.py`
- `ateki/experiments/20_data_valuation_estimators.py`
- `campaign_protocols/code/experiments/24_hyperedge_budget.py`
- `compute/almgsi_campaign/rerun_md_noise.py`
- `compute/almgsi_campaign/temperature_coalitions.py`
- `compute/almgsi_campaign/shard_cids.py`

## Carried-over code and data

Some results in the paper come from campaign protocols and analyses that also serve other projects of the group. The scripts and the result files they need are copied here, so this repository depends on no other repository. Their files are marked `(carried over)` in `CONTENTS.tsv`. Folders:

- `campaign_protocols/code/`
- `campaign_protocols/results/`

## Notes on inputs

- The version-locked band-gap archive (`shared/output/bandgap_archive_build/bandgap_universe.jsonl`, 261,053 records) is not stored in git; rebuild it from the included source caches with `python compute/bandgap_archive/build_inventory.py` and check it against the manifest hash in `build_stats.json`.
- Computed Al-Mg-Si records (DFT, MACE-MP-0, MD) are under `compute/almgsi_campaign/results*`; the HSE06 values with the half q grid, set aside after the convergence test, are left out.

## Contents by role

- code: 135 files
- environment: 6 files
- figure data: 5432 files
- input data: 2199 files
- result named in paper: 24 files
- code (carried over): 4 files
- input data (carried over): 6 files

`FILES.sha256` lists every file with its SHA-256 checksum; `CONTENTS.tsv` gives the role of each file.

## Provenance

The folder was assembled from the `singular_obj/` project of the Sparks group repository by `build_paper_repos.py`, which keeps the project's relative layout and gives working folders their public names.

## Licence

Code (Python, shell and SLURM scripts) is released under the MIT License (LICENSE). Data, result files and figures are released under the Creative Commons Attribution 4.0 International licence (LICENSE-CC-BY-4.0.txt). The archived third-party datasets (Materials Project, JARVIS-DFT, SNUMAT, the Zhuo et al. experimental compilation) keep their own terms; their sources are cited in the paper.

## Acknowledgements

Taylor D. Sparks acknowledges support from the Army Research Office Materials Design, under Contract No. W911NF-23-1-0333.
