# Experiment 13, recorded coordinator-led meetings: final grading (5 Oct 2026)

Predictions: `PREDICTION.md` (registered before any campaign, not edited).
Numbers: `summary_coordinator.json` from `analyze_coordinator.py`; figure `fig_coordinator.png`.
All 120 campaigns finished (05:40 to 08:35 UTC on an NVIDIA DGX Spark), 8,438 LLM
calls, 23 unparseable replies replaced by the fallback rule (0.3 %).

Task: five Qwen3-4B agents rank the 13 anion-element groups of the
experimental band-gap compilation (fluorides to antimonides) by measured
optical gap. Each agent holds one computed database's group order. Team
score is Kendall tau against the measured order.

## Verdicts

| prediction | measured | verdict |
| --- | --- | --- |
| Q1 role premium > 0, pooled, interval excludes 0 | +0.021 (-0.010 to +0.054), 100 pairs | fail |
| Q2 role premium positive in at least 4 of 5 rotations | 4 of 5 (GGA +0.045, r2SCAN +0.030, OptB88vdW +0.041, TB-mBJ +0.036, HSE06 -0.048) | pass |
| Q3 HSE06 top two with p >= 0.9 and GGA last with p >= 0.9, in both team types | coordinator-led: 0.997 and 0.972; flat: 0.996 and 0.705 | fail (flat GGA-last at 0.705) |
| Q4 coordinator raises team tau, paired, interval excludes 0 | +0.035 (+0.011 to +0.058), better in 62 of 100 pairs | pass |
| Q5 HSE06 coordinator outranks GGA coordinator with p >= 0.9 | difference -0.013, p = 0.29 | fail |
| Q6 flat team issues fewer distinct queries than coordinator-led | 0.128 vs 0.144, difference -0.017 (-0.033 to -0.001) | pass |

## Findings

1. **Credit follows source accuracy once the task separates the sources.**
   On the 13-group task the order of database credit in the flat team is
   the order of the databases' standalone accuracy (Spearman 1.0: HSE06
   0.27, r2SCAN 0.21, TB-mBJ 0.19, OptB88vdW 0.18, GGA 0.15 of team
   score); in the coordinator-led team it is 0.9. On the seven-family task
   of experiment 11 at larger scale three databases tied and the second place was not
   decided by the data. The failure of Q3 is on one cell only: in the flat
   team GGA is last in 71 % of bootstrap draws (OptB88vdW last in the
   rest), below the 0.9 threshold.
2. **A coordinator improves the team by a small, resolved amount.** With
   100 pairs, the coordinator-led team ranks better than the flat team of
   the same seed by +0.035 in Kendall tau (62 of 100 pairs better). This
   is the size measured in experiment 11 at larger scale (+0.03 to +0.07), now with an
   interval that excludes zero.
3. **The coordinator's own credit is mostly the credit of its database.**
   Under the mean rule the coordinator receives 0.22 of team score on
   average; the agent holding the same database in the flat team receives
   0.20. The role premium of +0.02 is not distinguishable from zero, while
   the team-level effect of having a coordinator (finding 2) is. The
   gain from the role appears in the team score but not in the
   coordinator's own share; a likely reading is that assignments change
   what every worker measures, so the gain is spread across the workers'
   shares (not tested separately here).
4. **The database the coordinator holds does not change the team score.**
   Team tau ranges 0.80 to 0.84 over the five coordinator databases with
   overlapping intervals; the HSE06-led team is not better than the
   GGA-led team (Q5 fails). The only rotation with a negative role premium
   is the HSE06 holder (-0.048, interval -0.109 to +0.014, includes
   zero); whether the most accurate source loses credit when its holder
   assigns queries is not resolved by 20 pairs.
5. **Herding without a coordinator persists on the finer task.** The flat
   team repeats queries more (12.8 % distinct trays vs 14.4 %; 715
   possible 4-group trays). The difference is small and its interval only
   just excludes zero.
6. **Rule choice.** The sum rule gives the coordinator a negative share in
   every rotation (-0.84 to -0.99) and the best-group rule gives a
   negative premium (-0.07 to -0.14); the mean rule is the only one of the
   three whose coordinator credit is near the paired team effect, as
   proposed in `../recorded_meetings_scale/CREDIT_FIXES.md`.

## Implications

Findings 1 to 3 answer the two failures of experiment 11 at larger scale
(P4 and P5 in `../recorded_meetings_scale/GRADING_FINAL.md`): the
tie was a property of the seven-family task, and the coordinator credit
was a property of the valuation rule and of the database it held. A
coordinator role is best graded at the team level (paired effect), not by
its Shapley share.
