# Experiment 08: which database earns the credit?

Receiver `expt_zhuo` advised by 7 donor databases on the frozen band-gap archive universe. v(S) = mean over 10 matched seeds of the early-window mean tau of an exp-26-style campaign whose pooled prior uses ONLY the donors in S (arm: pair, budget 240). v(empty) = cold campaign. Every value below comes from the 128 measured coalition campaigns; nothing is simulated beyond retrospective queries into archived records.

## Credit ranking (exact 7-player Shapley, early window)

| rank | database | Shapley [95% CI over seeds] | Banzhaf | LOO |
|---|---|---|---|---|
| 1 | SNUMAT GGA | +0.0540 [+0.0348, +0.0725] | +0.0428 | +0.0210 |
| 2 | SNUMAT HSE | +0.0540 [+0.0361, +0.0730] | +0.0428 | +0.0210 |
| 3 | MP r2SCAN | +0.0064 [-0.0070, +0.0223] | -0.0007 | +0.0038 |
| 4 | JARVIS TBmBJ | -0.0067 [-0.0194, +0.0054] | -0.0121 | -0.0095 |
| 5 | JARVIS OptB88vdW | -0.0130 [-0.0207, -0.0058] | -0.0193 | -0.0114 |
| 6 | MP GGA (ICSD-provenance subset) | -0.0228 [-0.0410, -0.0061] | -0.0278 | -0.0095 |
| 7 | MP GGA | -0.0300 [-0.0470, -0.0162] | -0.0356 | -0.0038 |

## The materials story

The measured-band-gap campaign should thank **SNUMAT GGA** first: it holds 47% of the positive credit in this run.

Credit is **spread**: the effective number of contributing databases (inverse Herfindahl over positive Shapley shares) is 2.23 of 7.

Negative-credit donors (their pooled-prior contribution lowered the early-window tau in this run): JARVIS TBmBJ, JARVIS OptB88vdW, MP GGA (ICSD-provenance subset), MP GGA. A donor whose class ordering misranks against the measured gaps prices at about zero or below.

## Feasibility and axioms

- 128 coalition campaigns; campaign wall time 4543.0 s total (35.49 s per coalition mean, 4 workers); exact Shapley+Banzhaf+LOO from the cached values took 0.001 s.
- Efficiency axiom: |sum(phi) - (v(N) - v(empty))| = 1.39e-17 (machine precision; asserted).
- v(N) = +0.6819, v(empty) = +0.6400; final-window Shapley reported in the JSON as a no-long-run-harm cross-check.

## Monte-Carlo validation (from cached values only)

| permutations m | median max-error | rank exact (frac of 20 reps) | distinct coalitions touched |
|---|---|---|---|
| 10 | 0.0175 | 0.00 | 47.0 |
| 30 | 0.0087 | 0.00 | 89.8 |
| 100 | 0.0043 | 0.00 | 124.2 |
| 300 | 0.0028 | 0.00 | 128.0 |
| 1000 | 0.0015 | 0.00 | 128.0 |
| 3000 | 0.0008 | 0.00 | 128.0 |

Player ranking did NOT stabilise within the tested permutation budgets (max m = 3000); reported honestly.

Mechanism: the smallest exact Shapley gap between adjacent players is 0.00e+00, at or below the m = 3000 median value error (7.79e-04), so exact rank agreement is unattainable by sampling REGARDLESS of m -- two players are measurably (inter)changeable. When two donors carry the same class-level ordering they are symmetric players and the symmetry axiom forces equal Shapley values; the VALUE estimates themselves converge fast (see the max-error column), which is what the sampling path needs.
