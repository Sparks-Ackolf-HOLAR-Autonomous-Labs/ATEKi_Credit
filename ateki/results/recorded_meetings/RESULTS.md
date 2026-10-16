# Recorded meetings with LLM agents (ATEKi experiment 11): results

Script `ateki/experiments/11_recorded_meetings.py`; campaign logs
`campaigns/*.json` (every query, notebook entry and message); summary
`meetings_summary.json`; figure `fig_meetings.png`; sum-versus-max check
`max_variant.json`.

## Set-up

Five LLM agents (Qwen3-4B-Instruct-2507, served by vLLM on an NVIDIA DGX Spark,
temperature 0.7) rank the seven families of the experimental band-gap
compilation by measured gap. Each agent holds one computed database as
private knowledge (its family order only, no values): MP GGA, MP r2SCAN,
JARVIS OptB88vdW, JARVIS TB-mBJ, SNUMAT HSE06. Each round every agent
submits one four-family query and the archive returns the measured order
of one archived compound per family. 12 rounds, 240 evaluations per
campaign, 5 seeds per team type, 0 parse fallbacks in 660 calls.

- **No coordinator:** agents act at the same time on a shared notebook,
  may message any agent, and cite the entries they build on.
- **Coordinator-led:** the MP GGA agent assigns every agent a query each
  round; the others may change it and may message only the coordinator.

The recorded conference structure is built from the logs (a message from
i to a set T is the meeting {i} plus T; a query citing entries of other
agents is the meeting of its author and those agents; meetings seen at
least twice are kept). Coalition values are measured by replay: the
queries of the coalition's members, refitted with their databases'
orders as a learned-trust prior, scored by Kendall tau against the
measured ranking.

## What happened

| | no coordinator | coordinator-led | random queries, no agents |
| --- | ---: | ---: | ---: |
| team tau (mean of 5) | 0.783 | 0.867 | 0.867 (no prior), 0.819 (pooled prior) |
| distinct trays among 60 queries | 9 % | 12 % | about 100 % |
| messages per campaign | 0.2 | 62 | |
| recorded meetings kept per campaign | 5 | 9 | |

1. **Without a coordinator the agents herd.** In one campaign 53 of 60
   queries were the same tray (boride, halide, oxide, pnictide). Agents
   read the same notebook, write claims and summaries (about 6 and 5 per
   agent), but almost never message each other, and a claim does not stop
   the next agent from loading the same tray. The team ranks the families
   worse than random four-family trays with the same budget (0.78 vs
   0.87). This is the duplicated-work failure of the parallel-width
   experiment, now produced by LLM decision makers.
2. **A coordinator spreads the work** (four trays used about 11 times each
   instead of one tray 53 times) and matches random trays (0.87; two of
   five campaigns reach the full measured order).
3. **The recorded structure of the coordinator-led team is the declared
   star.** Every worker query cites the coordinator, so the conferences
   read from the logs give exactly the same Myerson value as the declared
   star. Without a coordinator, the recorded structure differs from the
   provenance-declared one (rank correlation with Shapley 0.58 vs 0.46),
   and it changes who gets the credit.
4. **Which database the credit follows.** In the flat team the SNUMAT
   HSE06 agent receives the largest share (Shapley 0.32); in the
   coordinator-led team the MP r2SCAN agent does (0.32) and SNUMAT HSE06
   is second (0.25). In both teams and under every rule these two agents
   hold the two largest shares, and they are the two of the five
   databases with positive credit in the seven-database game without
   agents.
5. **Coordinator credit depends on how a split team is valued.** With
   ATEKi's sum-of-components rule the coordinator receives a negative
   share (-0.75): removing the hub splits the team into four separate
   rankings whose Kendall taus are added, and that sum exceeds what the
   joined team reaches. If a split team is valued by its best component
   (the team reports one ranking), the coordinator receives +0.06 and the
   workers keep their order (`max_variant.json`). For bounded quality
   scores such as Kendall tau, the max rule is the one that matches the
   campaign.
6. **Roles.** The coordinator is cited by others about 48 times per
   campaign against 13 to 20 for workers; in the flat team all five agents
   are cited about equally (36 to 39), so no reviewer or integrator role
   appears at five agents.

## Limits

One model (4 B parameters) at one temperature; five agents and 12
rounds; 5 campaigns per team type, so team-tau differences of 0.08 are
within campaign-to-campaign spread (standard deviation of the random
reference 0.13). In Agensh (Zhan et al., 2026, arXiv:2609.26781,
doi:10.48550/arXiv.2609.26781) roles appeared at 32 to 1,024 agents; five
agents test only the smallest end of that range.
