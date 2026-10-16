"""
Bridge between ATEKi attribution engines and PEGKi database outputs.

Mirrors TENKi/analysis/adapters.py in structure but reorients data for
coalition game theory: each policy's per-experiment scores become the
individual player's history; v(S) is computed from the joint performance
of subset S.
"""

from __future__ import annotations
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable


@dataclass
class PolicyScores:
    """Per-policy per-experiment scores loaded from a PEGKi database."""
    name: str
    db_path: str
    policy_scores: dict[str, list[float]]   # policy_id -> [score_per_experiment]
    n_experiments: int                       # min experiments across all policies
    objective: str = "best_color_distance_mean"


def load_policy_scores(db_path: str, objective: str = "best_color_distance_mean") -> PolicyScores:
    """
    Load per-policy per-experiment scores from a PEGKi database directory.

    Reads experiment_*/summary.json -> policy_stats[policy][objective].
    Lower is better for color_distance objectives.

    Args:
        db_path: Path to PEGKi database root (contains policies/ subdirectory).
        objective: Key in policy_stats summary to use as the score.

    Returns:
        PolicyScores with policy -> [score per experiment] mapping.
    """
    db = Path(db_path)
    policies_dir = db / "policies"
    if not policies_dir.exists():
        raise FileNotFoundError(f"No policies/ directory found in {db_path}")

    policy_scores: dict[str, list[float]] = {}

    for policy_dir in sorted(policies_dir.iterdir()):
        if not policy_dir.is_dir():
            continue
        policy_id = policy_dir.name
        scores: list[float] = []

        for exp_dir in sorted(policy_dir.glob("experiment_*")):
            summary_file = exp_dir / "summary.json"
            if not summary_file.exists():
                continue
            with open(summary_file, "r", encoding="utf-8") as f:
                summary = json.load(f)
            val = summary.get("policy_stats", {}).get(objective)
            if val is not None:
                scores.append(float(val))

        if scores:
            policy_scores[policy_id] = scores

    n_experiments = min(len(v) for v in policy_scores.values()) if policy_scores else 0
    return PolicyScores(
        name=db.name,
        db_path=str(db),
        policy_scores=policy_scores,
        n_experiments=n_experiments,
        objective=objective,
    )


class CoalitionValueFunction:
    """
    Defines v(S) for a coalition S of policies using PEGKi scores.

    Three aggregation semantics:
    - "best"   : v(S) = max_score_in_S  (best member wins; lower color_distance = better, so MIN)
    - "mean"   : v(S) = mean_score_in_S (ensemble average)
    - "oracle" : v(S) = min per-target (best policy per experiment, lower-is-better)

    Value convention: higher v(S) = better (we negate color_distance internally).
    """

    def __init__(
        self,
        policy_scores: PolicyScores,
        mode: str = "best",
        n_experiments: int | None = None,
    ):
        self.policy_scores = policy_scores
        self.mode = mode
        n = n_experiments or policy_scores.n_experiments
        # Normalize: take mean over first n experiments per policy
        self.means: dict[str, float] = {
            pid: -float(sum(scores[:n]) / len(scores[:n]))  # negate: lower dist = higher value
            for pid, scores in policy_scores.policy_scores.items()
            if len(scores) >= 1
        }
        self.policies = list(self.means.keys())
        self._cache: dict[frozenset, float] = {}

    def __call__(self, coalition: frozenset[str]) -> float:
        """Return v(S) for the given coalition (higher = better)."""
        if not coalition:
            return 0.0
        key = frozenset(coalition)
        if key in self._cache:
            return self._cache[key]

        members = [p for p in coalition if p in self.means]
        if not members:
            return 0.0

        if self.mode == "best":
            val = max(self.means[p] for p in members)
        elif self.mode == "mean":
            val = sum(self.means[p] for p in members) / len(members)
        else:
            raise ValueError(f"Unknown mode: {self.mode}")

        self._cache[key] = val
        return val
