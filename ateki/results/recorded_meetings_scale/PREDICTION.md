# Experiment 11 at larger scale: predictions (written before any run)

Registered 2026-10-04 about 09:55 UTC, before any campaign
of this extension was started. Script: `ateki/experiments/11_recorded_meetings.py`
(now takes `--team-size`; team size 5 reproduces the original campaigns
exactly, checked on `flat_s0`: same coalition values and Shapley shares).

The task is unchanged: a team of LLM agents ranks the seven families of
the experimental band-gap compilation (wide-gap semiconductor screening)
by measured optical gap. Each agent holds one computed database's family
order (MP GGA, MP r2SCAN, JARVIS OptB88vdW, JARVIS TB-mBJ, SNUMAT HSE06).
12 rounds, one four-family query per agent per round.

## Runs

| set | model | agents | campaigns per team type |
| --- | --- | ---: | ---: |
| S1 | Qwen3-4B-Instruct-2507 | 5 | 20 (seeds 0-4 from 4 Oct, 5-19 new) |
| S2 | NVIDIA Nemotron 3.5 Lightning 30B-A3B (NVFP4) | 5 | 10 |
| S3 | Qwen3-4B-Instruct-2507 | 10 (two per database) | 8 |

Team types: no coordinator (flat) and coordinator-led (agent 1, an MP GGA
holder, assigns queries).

## Predictions

- **P1 (S1).** With 20 campaigns per team type the coordinator-led team
  ranks better than the flat team: mean team Kendall tau difference > 0,
  with a 95 % bootstrap interval that excludes 0. The flat team's share
  of distinct trays stays below 20 %.
- **P2 (S2).** Herding without a coordinator is not specific to the 4B
  model: the flat team's share of distinct trays is below 30 % with the
  30B model, and the coordinator-led team ranks at least as well as the
  flat team.
- **P3 (S3).** Doubling the team does not remove herding: the flat team's
  share of distinct trays at 10 agents is no higher than at 5 agents.
  The coordinator-led team ranks at least as well as the flat team.
- **P4 (credit).** Summed over agents holding the same database, the
  MP r2SCAN and SNUMAT HSE06 holders receive the two largest Shapley
  shares in every set and team type.
- **P5 (coordinator credit).** In every coordinator-led set the
  coordinator's share is negative under the sum rule and positive under
  the best-group rule.
- **P6 (roles).** In the flat team at 10 agents, no agent is cited by
  others more than twice the team median (no hub forms without a
  declared coordinator at this size).

Any prediction that fails is reported as failed; none is edited after
data exist.
