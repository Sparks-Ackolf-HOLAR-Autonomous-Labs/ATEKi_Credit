# Experiment 11 at larger scale: what to change after the P4 and P5 failures (5 Oct 2026)

Exploratory, not registered. Script `credit_fixes.py`, numbers in
`credit_fixes.json`. Computed on the recorded campaigns of S1 to S3; no new
LLM runs. The failed verdicts in `GRADING_FINAL.md` stand unchanged.

## P5 (coordinator credit): the rule and the control were the problem

The coordinator is always agent 1, an MP GGA holder. Two things mixed into
its credit: the valuation rule for a team that falls apart when the
coordinator is removed, and the database the coordinator happens to hold.

Coordinator credit as a share of team score, three rules for a separated
team (sum of groups, best group, member-weighted mean of groups):

| set | sum rule | best-group rule | mean rule | mean rule, positive campaigns |
| --- | ---: | ---: | ---: | ---: |
| S1 (5 agents, Qwen) | -0.83 | +0.05 | +0.19 | 20/20 |
| S2 (5 agents, Nemotron) | -0.87 | +0.11 | +0.20 | 9/10 |
| S3 (10 agents, Qwen) | -2.73 | -0.05 | +0.17 | 8/8 |

The mean rule does not grow with team size: a team split into nine single
agents is worth their average ranking, not their sum.

Role premium: coordinator credit minus a control holding the same database
without the role.

| set | control | mean rule premium (95% interval) | paired effect of having a coordinator on team tau (95% interval) |
| --- | --- | --- | --- |
| S1 | agent 1 in the flat team | +0.04 (-0.02 to +0.10) | +0.07 (+0.02 to +0.13), better in 14/20 pairs |
| S2 | agent 1 in the flat team | -0.05 (-0.17 to +0.09) | +0.04 (-0.12 to +0.20), 4/10 |
| S3 | agent 1 in the flat team | +0.09 (0.00 to +0.17) | +0.03 (-0.05 to +0.09), 4/8 |
| S3 | agent 6 (MP GGA, same team, no role) | +0.10 (+0.01 to +0.19) | |

Under the sum and best-group rules the premium is negative in every set,
so neither rule isolates the role. Under the mean rule most of the
coordinator's credit is what any MP GGA holder receives; the part due to
the role is +0.04 to +0.10, the same size as the measured effect of adding
a coordinator (+0.03 to +0.07), and the intervals of S2 and S3 include zero
because those sets have 8 to 10 pairs.

## P4 (credit by database): the prediction asked for a winner of a tie

Standalone accuracy of each database's seven-family order (Kendall tau
against the measured order): SNUMAT HSE06 0.81; MP r2SCAN, JARVIS
OptB88vdW and JARVIS TB-mBJ 0.62 each; MP GGA 0.52. Three databases give
the same accuracy on this task, so which of them takes second place is not
decided by the data they hold.

Bootstrap probability (over campaigns) that each database is in the top two:

| set, team | SNUMAT HSE06 | MP r2SCAN | TB-mBJ | OptB88vdW | MP GGA |
| --- | ---: | ---: | ---: | ---: | ---: |
| S1 flat | 1.00 | 0.90 | 0.01 | 0.08 | 0.00 |
| S1 coordinator-led | 0.47 | 0.76 | 0.77 | 0.00 | 0.00 |
| S2 flat | 0.97 | 0.00 | 0.14 | 0.14 | 0.75 |
| S2 coordinator-led | 0.99 | 0.70 | 0.13 | 0.15 | 0.03 |
| S3 flat | 1.00 | 0.05 | 0.14 | 0.54 | 0.28 |
| S3 coordinator-led | 1.00 | 0.78 | 0.14 | 0.07 | 0.00 |

The resolvable statement is "the most accurate source (HSE06) is in the top
two": probability 0.97 to 1.00 in five of six cells.

## Changes adopted in experiment 13 (recorded coordinator-led meetings)

1. Report credit for separated teams under the mean rule as primary; keep
   sum and best-group as secondary.
2. Grade a coordinator by its role premium against a same-database control,
   and check it against the paired effect of adding a coordinator.
3. Rotate the coordinator role over the five databases, so role and
   database are not confounded (the coordinator now always holds the least
   accurate database).
4. Make the task able to separate the sources: rank more groups (or
   individual compounds) so the three middle databases no longer tie.
5. Write credit predictions as bootstrap probabilities with a threshold
   (for example "HSE06 in the top two with probability at least 0.9"), and
   size the number of campaigns for the interval widths above (20 pairs per
   cell rather than 8 to 10).
