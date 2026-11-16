# Experiment 08: which database earns the credit?

Receiver `expt_zhuo` advised by 7 donor databases on the frozen band-gap archive universe. v(S) = mean over 10 matched seeds of the early-window mean tau of an exp-26-style campaign whose pooled prior uses ONLY the donors in S (arm: pair, budget 240). v(empty) = cold campaign. Every value below comes from the 128 measured coalition campaigns; nothing is simulated beyond retrospective queries into archived records.

## Credit ranking (exact 7-player Shapley, early window)

| rank | database | Shapley [95% CI over seeds] | Banzhaf | LOO |
|---|---|---|---|---|
| 1 | SNUMAT GGA | +0.0539 [+0.0343, +0.0740] | +0.0462 | +0.0286 |
| 2 | SNUMAT HSE | +0.0539 [+0.0338, +0.0735] | +0.0462 | +0.0286 |
| 3 | MP r2SCAN | +0.0054 [-0.0063, +0.0157] | -0.0023 | +0.0076 |
| 4 | JARVIS OptB88vdW | -0.0051 [-0.0159, +0.0066] | -0.0076 | -0.0133 |
| 5 | JARVIS TBmBJ | -0.0134 [-0.0237, -0.0054] | -0.0188 | -0.0160 |
| 6 | MP GGA (ICSD-provenance subset) | -0.0234 [-0.0420, -0.0075] | -0.0284 | -0.0103 |
| 7 | MP GGA | -0.0294 [-0.0418, -0.0180] | -0.0357 | -0.0038 |

## The materials story

The measured-band-gap campaign should thank **SNUMAT GGA** first: it holds 48% of the positive credit in this run.

Credit is **spread**: the effective number of contributing databases (inverse Herfindahl over positive Shapley shares) is 2.19 of 7.

Negative-credit donors (their pooled-prior contribution lowered the early-window tau in this run): JARVIS OptB88vdW, JARVIS TBmBJ, MP GGA (ICSD-provenance subset), MP GGA. A donor whose class ordering misranks against the measured gaps prices at about zero or below.

## Feasibility and axioms

- 128 coalition campaigns; campaign wall time 5198.3 s total (40.61 s per coalition mean, 6 workers); exact Shapley+Banzhaf+LOO from the cached values took 0.002 s.
- Efficiency axiom: |sum(phi) - (v(N) - v(empty))| = 2.08e-17 (machine precision; asserted).
- v(N) = +0.7368, v(empty) = +0.6949; final-window Shapley reported in the JSON as a no-long-run-harm cross-check.

## Monte-Carlo validation (from cached values only)

| permutations m | median max-error | rank exact (frac of 20 reps) | distinct coalitions touched |
|---|---|---|---|
| 10 | 0.0172 | 0.00 | 47.0 |
| 30 | 0.0107 | 0.00 | 89.8 |
| 100 | 0.0045 | 0.00 | 124.2 |
| 300 | 0.0029 | 0.00 | 128.0 |
| 1000 | 0.0014 | 0.00 | 128.0 |
| 3000 | 0.0009 | 0.00 | 128.0 |

Player ranking did NOT stabilise within the tested permutation budgets (max m = 3000); reported honestly.

Mechanism: the smallest exact Shapley gap between adjacent players is 0.00e+00, at or below the m = 3000 median value error (8.57e-04), so exact rank agreement is unattainable by sampling REGARDLESS of m -- two players are measurably (inter)changeable. When two donors carry the same class-level ordering they are symmetric players and the symmetry axiom forces equal Shapley values; the VALUE estimates themselves converge fast (see the max-error column), which is what the sampling path needs.
