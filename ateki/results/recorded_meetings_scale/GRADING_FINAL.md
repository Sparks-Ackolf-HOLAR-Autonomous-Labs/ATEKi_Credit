# Experiment 11 at larger scale: final grading (5 Oct 2026)

Predictions: `PREDICTION.md` (registered 4 Oct about 09:55 UTC, before any
run; not edited since). Numbers: `scale_summary.json` from
`analyze_scale.py`. All three sets are complete: S1 (Qwen3-4B, 5 agents,
20 campaigns per team type), S2 (Nemotron 30B-A3B, 5 agents, 10 per team
type), S3 (Qwen3-4B, 10 agents with two per database, 8 per team type).
S3 finished on an NVIDIA DGX Spark at 17:18 UTC on 4 Oct. An interim
grading was made at 12:35 UTC on 4 Oct, before S3 was complete.

Task: a team of LLM agents ranks the seven families of the experimental
band-gap compilation by measured optical gap. Each agent holds the family
order from one computed database. Team score is Kendall tau against the
measured order.

## Verdicts

| prediction | measured | verdict |
| --- | --- | --- |
| P1 (S1: coordinator-led team ranks better) | tau 0.833 vs 0.761; difference 0.072, 95% interval 0.011 to 0.135; flat distinct trays 10.1% | pass |
| P2 (S2: herding also with the 30B model) | flat distinct trays 5.5% (< 30%); coordinator-led tau 0.806 vs flat 0.767 | pass |
| P3 (S3: doubling the team does not remove herding) | flat distinct trays 6.0% at 10 agents vs 10.1% at 5; coordinator-led tau 0.845 vs flat 0.819 | pass |
| P4 (MP r2SCAN and SNUMAT HSE06 holders take the two largest credit shares everywhere) | holds in 3 of 6 set and team-type cells; fails in S1 coordinator-led (TB-mBJ second), S2 flat (MP GGA second), S3 flat (OptB88vdW second) | fail |
| P5 (coordinator credit negative under the sum rule and positive under the best-group rule, every set) | sum rule: S1 -0.83, S2 -0.87, S3 -2.73 (negative in all 38 campaigns); best-group rule: S1 +0.05, S2 +0.11, **S3 -0.05** | **fail** (S3) |
| P6 (S3 flat: no agent cited more than twice the team median) | 1.18 times the median | pass |

Four of six predictions pass. P4 failed already at the interim stage.
P5 passed at the interim stage and fails on the complete data: the
10-agent coordinator-led campaigns were the last to run.

Random four-family trays at the same evaluation budget give tau 0.867
(5 agents) and 0.848 (10 agents). No team organisation in any set ranks
above random trays; the coordinator brings the team up to random-tray
quality (S3: 0.845 vs 0.848) but not beyond it.

## What the failure of P5 shows (exploratory, not registered)

Script: `coordinator_per_campaign.py`, output
`coordinator_per_campaign.txt`.

1. **The sum-rule penalty grows with team size.** The coordinator's
   credit under Myerson's sum rule is negative in every one of the 38
   coordinator-led campaigns, about -0.8 of the team score at 5 agents and
   -2.0 to -3.2 at 10 agents. Removing the coordinator splits the meeting
   structure into single agents, and the sum rule adds up their separate
   rankings; with nine other agents that sum exceeds the team's single
   ranking by more. The size of this credit is therefore a property of the
   valuation rule and the number of members, not of the coordinator's
   contribution.
2. **Under the best-group rule the coordinator's credit is near zero and
   its sign varies between campaigns.** It is positive in 12 of 20 (S1),
   7 of 10 (S2) and 3 of 8 (S3) campaigns; the set means (+0.05, +0.11,
   -0.05) are small against the campaign-to-campaign spread (-0.23 to
   +0.33).
3. **The sign follows the outcome.** Across all 38 campaigns the
   coordinator's best-group credit rises with the team score (Spearman
   0.47, p = 0.003). The coordinator receives credit in campaigns where
   the team ranked the families well and loses it where the team ranked
   them poorly.

For an audit of a laboratory team (for example a group lead who assigns
XRD trays to four students), this means the lead's credit under the sum
rule says more about how many people report to the lead than about the
lead's contribution, and under the best-group rule a single campaign does
not determine the sign: it needs several campaigns, and it tracks whether
the campaigns succeeded.

## Credit by database (Shapley share of team score, summed over holders)

| set, team type | first | second | third |
| --- | --- | --- | --- |
| S1 flat | SNUMAT HSE06 0.309 | MP r2SCAN 0.218 | OptB88vdW 0.182 |
| S1 coordinator-led | MP r2SCAN 0.270 | TB-mBJ 0.266 | SNUMAT HSE06 0.251 |
| S2 flat | SNUMAT HSE06 0.320 | MP GGA 0.262 | OptB88vdW 0.182 |
| S2 coordinator-led | SNUMAT HSE06 0.252 | MP r2SCAN 0.229 | TB-mBJ 0.188 |
| S3 flat | SNUMAT HSE06 0.314 | OptB88vdW 0.186 | MP r2SCAN 0.174 |
| S3 coordinator-led | SNUMAT HSE06 0.285 | MP r2SCAN 0.242 | TB-mBJ 0.195 |

SNUMAT HSE06 is in the top two in every cell and first in five of six.
The second place moves between MP r2SCAN, TB-mBJ, MP GGA and OptB88vdW,
with small margins. In a coordinator-led team the coordinator holds MP
GGA, and MP GGA ranks last or fourth in those cells, so the coordinator's
own database contributes little even when the coordinator's organisation
helps.
