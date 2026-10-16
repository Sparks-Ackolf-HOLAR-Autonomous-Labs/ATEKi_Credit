r"""
Leave-one-out (LOO) and data valuation for ATEKi non-egalitarian attribution.

LOO attribution: phi_i^LOO = v(all) - v(all \ {i})
  - Computationally cheap (n evals total)
  - Does not satisfy efficiency axiom (phi sum != v(all) in general)
  - Good for outlier detection: large LOO gap => high-influence entity

Data Banzhaf / Data Shapley: marginal contribution of individual experiments
  (data points) rather than policies or agents.
  Here "data" = one experiment run (a row in the PEGKi DB).

References:
  Koh & Liang (2017): Understanding Black-box Predictions via Influence Functions.
  Kwon & Zou (2022): Beta Shapley: a Unified and Noise-reduced Data Valuation Framework.
  Zhang et al. (2023): Towards Efficient Data Valuation Based on the Shapley Value.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable

import numpy as np

Coalition = frozenset[str]
ValueFn = Callable[[Coalition], float]


@dataclass
class LOOResult:
    """Leave-one-out attribution scores."""
    players: list[str]
    scores: dict[str, float]       # player -> LOO gap (positive = beneficial)
    grand_value: float
    method: str = "loo"

    def rank(self) -> list[tuple[str, float]]:
        return sorted(self.scores.items(), key=lambda x: x[1], reverse=True)


class LOOAttributor:
    r"""
    Leave-one-out: estimate influence of removing each player from the grand coalition.

    phi_i^LOO = v(N) - v(N \ {i})

    Positive value: removing i hurts the group (i is beneficial).
    Negative value: removing i helps the group (i is harmful/redundant).
    """

    def __init__(self, players: list[str], value_fn: ValueFn):
        self.players = players
        self.value_fn = value_fn
        self.grand = frozenset(players)

    def compute(self) -> LOOResult:
        grand_val = self.value_fn(self.grand)
        scores: dict[str, float] = {}
        for player in self.players:
            without = self.grand - {player}
            scores[player] = grand_val - self.value_fn(without)
        return LOOResult(
            players=self.players,
            scores=scores,
            grand_value=grand_val,
        )


@dataclass
class DataValuationResult:
    """Per-data-point (per-experiment) attribution scores."""
    entity_id: str           # policy or agent whose experiments are being valued
    experiment_scores: list[float]   # raw scores per experiment
    loo_values: list[float]          # LOO contribution of each experiment
    banzhaf_approx: list[float]      # MC Banzhaf approximation per experiment
    n_experiments: int


class DataValuator:
    """
    Value individual experiments (data points) for a single policy/agent.

    Each experiment contributes independently to the policy's mean score.
    LOO value of experiment k = mean_all - mean_excluding_k.
    Banzhaf approximation: marginal improvement when experiment k joins a random subset.

    Args:
        entity_id: Name of the policy or agent.
        scores: Per-experiment raw scores (lower = better for color_distance;
                pass negated scores if you want higher = better convention).
        n_mc: Monte Carlo samples for Banzhaf approximation.
    """

    def __init__(self, entity_id: str, scores: list[float], n_mc: int = 500, seed: int = 42):
        self.entity_id = entity_id
        self.scores = scores
        self.n = len(scores)
        self.n_mc = n_mc
        self.rng = np.random.default_rng(seed)

    def _subset_mean(self, indices: list[int]) -> float:
        if not indices:
            return 0.0
        return float(np.mean([self.scores[i] for i in indices]))

    def compute(self) -> DataValuationResult:
        arr = np.array(self.scores, dtype=float)
        grand_mean = float(arr.mean())

        # LOO
        loo: list[float] = []
        for k in range(self.n):
            without = np.delete(arr, k)
            loo.append(grand_mean - (float(without.mean()) if len(without) > 0 else 0.0))

        # MC Banzhaf: for each data point k, draw random subsets not containing k,
        # measure marginal of adding k
        banzhaf: list[float] = []
        for k in range(self.n):
            others = [i for i in range(self.n) if i != k]
            marginals: list[float] = []
            for _ in range(self.n_mc):
                mask = self.rng.random(len(others)) < 0.5
                subset = [others[j] for j, m in enumerate(mask) if m]
                v_without = self._subset_mean(subset)
                v_with = self._subset_mean(subset + [k])
                marginals.append(v_with - v_without)
            banzhaf.append(float(np.mean(marginals)))

        return DataValuationResult(
            entity_id=self.entity_id,
            experiment_scores=self.scores,
            loo_values=loo,
            banzhaf_approx=banzhaf,
            n_experiments=self.n,
        )
