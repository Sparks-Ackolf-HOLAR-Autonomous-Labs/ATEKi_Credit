# Experiment 06: the physics prior as a Shapley player

Players: kway_events, pair_events, physics_prior. Exact 3-player Shapley, lambda = 4.0, 10 seeds x 8 channels.

| budget | phi(physics_prior) | phi(pair_events) | phi(kway_events) | v(grand) | physics share |
|---|---|---|---|---|---|
| 16 | +0.4092 | +0.1151 | +0.1668 | +0.6911 | 59.2% |
| 48 | +0.3828 | +0.1066 | +0.1755 | +0.6649 | 57.6% |
| 96 | +0.2856 | +0.1792 | +0.2079 | +0.6726 | 42.5% |
| 192 | +0.2727 | +0.2096 | +0.2513 | +0.7336 | 37.2% |

Prior-only value (tau of the donor ordering alone): +0.6458.
Evaluations-equivalent of the prior: 192 evaluations (budget at which data alone matches the prior).

Efficiency holds exactly (sum phi = v(grand)); see --self-test.
Same frozen-universe retrospective querying as TENKi exps 24/25.
