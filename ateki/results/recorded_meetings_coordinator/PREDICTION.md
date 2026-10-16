# Experiment 13, recorded coordinator-led meetings: registered predictions (5 Oct 2026, before any campaign)

Written after the smoke test of the code path only (no campaign of the
production design has run). Not to be edited once data exist; failed
predictions are reported as failed.

## Design

Script: `ateki/experiments/13_recorded_meetings_coordinator.py` (experiment 11
imported unchanged; changes listed in its docstring). Follows the five
changes proposed in `../recorded_meetings_scale/CREDIT_FIXES.md`.

- Task: five LLM agents rank the 13 anion-element groups of the
  experimental band-gap compilation (groups with at least 30 measured
  compounds) by measured optical gap. Each agent holds one computed
  database's group order. Standalone accuracy of each database's order
  (Kendall tau against the measured order): SNUMAT HSE06 0.90, MP r2SCAN
  0.85, JARVIS TB-mBJ 0.82, JARVIS OptB88vdW 0.79, MP GGA 0.69. All five
  differ, unlike the seven-family task of experiment 11 at larger scale
  (three tied at 0.62).
- Model: Qwen3-4B-Instruct-2507 on an NVIDIA DGX Spark (vLLM),
  temperature 0.7, 12 rounds, 4 groups per query (same as S1 of
  experiment 11 at larger scale).
- Arms: flat team (no coordinator), seeds 0-19; coordinator-led team at
  rotation r = 0..4 (coordinator holds MP GGA, MP r2SCAN, JARVIS
  OptB88vdW, JARVIS TB-mBJ, SNUMAT HSE06 in turn), seeds 0-19 each.
  120 campaigns; 20 pairs per cell.
- Credit rule for separated teams: mean rule primary (a split team is
  worth the member-weighted average of its groups' scores); sum and
  best-group rules reported as secondary.
- Role premium: coordinator share (mean rule, share of team score) minus
  the share of the agent holding the same database in the flat team of
  the same seed.

## Predictions

- **Q1 (role premium, pooled).** Over the 100 coordinator-led campaigns,
  the mean role premium under the mean rule is positive, and its 95 %
  bootstrap interval excludes 0.
- **Q2 (role premium does not depend on the database held).** The role
  premium point estimate is positive in at least 4 of the 5 rotations.
- **Q3 (credit follows source accuracy).** In the flat team and in the
  pooled coordinator-led team (Shapley share summed per database, as a
  share of team score): bootstrap probability that SNUMAT HSE06 is in the
  top two is at least 0.9, and bootstrap probability that MP GGA receives
  the smallest share is at least 0.9.
- **Q4 (effect of having a coordinator).** Paired by seed (each
  coordinator-led campaign against the flat campaign of the same seed,
  100 pairs), the mean difference in team Kendall tau is positive with a
  95 % bootstrap interval that excludes 0.
- **Q5 (which database the coordinator should hold).** Team tau with the
  HSE06 coordinator exceeds team tau with the GGA coordinator: bootstrap
  probability of a positive difference at least 0.9 (20 vs 20 campaigns).
- **Q6 (herding).** The flat team's share of distinct 4-group queries
  (distinct queries over all 60 queries of a campaign) is lower than the
  coordinator-led team's (pooled over rotations), with a 95 % bootstrap
  interval of the difference that excludes 0.

## Grading

`analyze_coordinator.py` (written before collection) computes every quantity
above from the campaign files and writes `summary_coordinator.json` and
`GRADING.md`.
