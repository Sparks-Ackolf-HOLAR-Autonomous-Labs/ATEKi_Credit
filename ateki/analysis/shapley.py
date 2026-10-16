"""
Shapley value and Banzhaf power index computation for non-egalitarian attribution.

Both estimators measure individual marginal contribution to the group value v(S).
Use Monte Carlo sampling for tractability when |players| > ~15.

References:
  Shapley (1953): A Value for n-Person Games. Contributions to the Theory of Games.
  Banzhaf (1965): Weighted Voting Doesn't Work. Rutgers Law Review.
  Castro et al. (2009): Polynomial calculation of the Shapley value based on sampling.
"""

from __future__ import annotations
import math
import random
from dataclasses import dataclass, field
from typing import Callable

import numpy as np


Coalition = frozenset[str]
ValueFn = Callable[[Coalition], float]


@dataclass
class AttributionResult:
    """Attribution scores for each player, normalized to sum to v(grand_coalition)."""
    players: list[str]
    scores: dict[str, float]          # player -> attribution value
    method: str                        # "shapley" or "banzhaf"
    n_samples: int                     # MC samples used (exact if -1)
    grand_coalition_value: float
    # Sign-preserving share of |v(grand)|: dividing by a *negative* grand value
    # (routine for negated colour-distance objectives) would invert every sign,
    # reporting the best players as negative shares and vice versa.
    normalized: dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        gv = self.grand_coalition_value
        if abs(gv) > 1e-12:
            self.normalized = {p: v / abs(gv) for p, v in self.scores.items()}
        else:
            self.normalized = {p: 0.0 for p in self.players}

    def rank(self) -> list[tuple[str, float]]:
        """Return players sorted by attribution descending."""
        return sorted(self.scores.items(), key=lambda x: x[1], reverse=True)


class GraphRestrictedValue:
    """Myerson (1977) restriction of a coalition value to a communication graph.

    v_G(S) = sum of v(C) over the connected components C of the subgraph of G
    induced by S: members of S cooperate only if they can communicate within
    S. ShapleyEngine over v_G yields the Myerson value -- the principled
    implementation of "topology as a constraint on admissible coalitions"
    (unlike post-hoc reweighting of unconstrained Shapley values). For a
    connected G, v_G(N) = v(N), so efficiency is preserved.
    """

    def __init__(self, players: list[str], value_fn: ValueFn, adjacency):
        self.players = list(players)
        self.value_fn = value_fn
        self._index = {p: i for i, p in enumerate(self.players)}
        self.adjacency = adjacency

    def _components(self, S: frozenset) -> list[frozenset]:
        remaining = set(S)
        comps = []
        while remaining:
            seed = remaining.pop()
            comp = {seed}
            frontier = [seed]
            while frontier:
                u_i = self._index[frontier.pop()]
                linked = [q for q in remaining
                          if self.adjacency[u_i][self._index[q]] > 0]
                for q in linked:
                    remaining.remove(q)
                    comp.add(q)
                    frontier.append(q)
            comps.append(frozenset(comp))
        return comps

    def __call__(self, S) -> float:
        S = frozenset(S)
        if not S:
            return float(self.value_fn(S))
        return float(sum(self.value_fn(c) for c in self._components(S)))


class HypergraphRestrictedValue:
    """Conference-structure restriction of a coalition value to a hypergraph.

    Generalizes GraphRestrictedValue from pairwise communication links to
    multi-party "conferences": each hyperedge is a set of >= 2 players that
    can only communicate when ALL of its members are present in the
    coalition. For a coalition S, the hyperedges fully contained in S
    partition the players of S into components (players covered by no
    contained hyperedge are singletons), and

        v_H(S) = sum of value_fn(C) over the components C of S.

    Passing this callable to ShapleyEngine yields the hypergraph Myerson
    value. Semantics differ from a graph in an essential way: a size-3
    hyperedge {a, b, c} enables cooperation only when all three are present,
    whereas its clique expansion (edges ab, ac, bc) lets any two of them
    cooperate on their own.

    Reduction property: when every hyperedge has exactly 2 players, this
    reduces EXACTLY (not just approximately) to GraphRestrictedValue on the
    corresponding graph -- contained pairs are precisely the present edges,
    so the component partition and hence v_H(S) coincide for every S. See
    check_pairwise_reduction() below for an executable demonstration.

    References:
      - Myerson, R. B. (1977). Graphs and cooperation in games. Mathematics
        of Operations Research 2(3), 225-229. doi:10.1287/moor.2.3.225
      - Myerson, R. B. (1980). Conference structures and fair allocation
        rules. International Journal of Game Theory 9(3), 169-182.
        doi:10.1007/BF01781371
      - van den Nouweland, A., Borm, P., Tijs, S. (1992). Allocation rules
        for hypergraph communication situations. International Journal of
        Game Theory 20(3), 255-268. doi:10.1007/BF01253780
    """

    def __init__(self, players: list[str], value_fn: ValueFn, hyperedges):
        self.players = list(players)
        self.value_fn = value_fn
        player_set = set(self.players)
        self.hyperedges: list[frozenset[str]] = []
        for e in hyperedges:
            fe = frozenset(e)
            if len(fe) < 2:
                raise ValueError(f"Hyperedge {sorted(fe)} has < 2 players")
            unknown = fe - player_set
            if unknown:
                raise ValueError(f"Hyperedge {sorted(fe)} contains unknown players {sorted(unknown)}")
            self.hyperedges.append(fe)

    def _components(self, S: frozenset) -> list[frozenset]:
        """Partition S by the union of hyperedges fully contained in S."""
        parent: dict[str, str] = {p: p for p in S}

        def find(x: str) -> str:
            while parent[x] != x:
                parent[x] = parent[parent[x]]  # path halving
                x = parent[x]
            return x

        for e in self.hyperedges:
            if e <= S:
                it = iter(e)
                root = find(next(it))
                for q in it:
                    rq = find(q)
                    if rq != root:
                        parent[rq] = root
        groups: dict[str, set[str]] = {}
        for p in S:
            groups.setdefault(find(p), set()).add(p)
        return [frozenset(g) for g in groups.values()]

    def __call__(self, S) -> float:
        S = frozenset(S)
        if not S:
            return float(self.value_fn(S))
        return float(sum(self.value_fn(c) for c in self._components(S)))


def check_pairwise_reduction(tol: float = 1e-9) -> bool:
    """Self-check: a hypergraph of only 2-player hyperedges equals the
    graph restriction on the corresponding graph, coalition by coalition.

    Uses a small superadditive game (squared sum) on 4 players with a path
    a-b-c so the component partition actually matters, and compares
    HypergraphRestrictedValue against GraphRestrictedValue on every one of
    the 2^4 coalitions. Raises AssertionError on any mismatch > tol.
    """
    players = ["a", "b", "c", "d"]
    base = {"a": 1.0, "b": 2.0, "c": 4.0, "d": 8.0}

    def v(S: frozenset) -> float:
        return sum(base[p] for p in S) ** 2 if S else 0.0

    pairs = [("a", "b"), ("b", "c")]
    adj = [[0.0] * 4 for _ in range(4)]
    idx = {p: i for i, p in enumerate(players)}
    for (x, y) in pairs:
        adj[idx[x]][idx[y]] = 1.0
        adj[idx[y]][idx[x]] = 1.0

    v_h = HypergraphRestrictedValue(players, v, pairs)
    v_g = GraphRestrictedValue(players, v, adj)
    for mask in range(1 << len(players)):
        S = frozenset(players[j] for j in range(len(players)) if mask & (1 << j))
        dh, dg = v_h(S), v_g(S)
        assert abs(dh - dg) <= tol, (
            f"Pairwise-hypergraph reduction failed on S={sorted(S)}: {dh} vs {dg}")
    return True


class ShapleyEngine:
    """
    Computes Shapley values phi_i = E_{pi}[v(S_pi + i) - v(S_pi)]
    where expectation is over random permutations.

    Exact (O(2^n * n)) or Monte Carlo (O(n_samples * n)).
    """

    def __init__(self, players: list[str], value_fn: ValueFn):
        self.players = players
        self.value_fn = value_fn
        self.n = len(players)

    def exact(self) -> AttributionResult:
        """Exact Shapley via all 2^n subsets. Feasible for n <= 20."""
        if self.n > 20:
            raise ValueError(f"Exact Shapley infeasible for n={self.n}; use monte_carlo()")

        phi: dict[str, float] = {p: 0.0 for p in self.players}
        player_set = self.players

        for i, player in enumerate(player_set):
            others = [p for p in player_set if p != player]
            n_others = len(others)
            for mask in range(1 << n_others):
                S = frozenset(others[j] for j in range(n_others) if mask & (1 << j))
                s = len(S)
                weight = math.factorial(s) * math.factorial(self.n - s - 1) / math.factorial(self.n)
                marginal = self.value_fn(S | {player}) - self.value_fn(S)
                phi[player] += weight * marginal

        grand = self.value_fn(frozenset(self.players))
        return AttributionResult(
            players=self.players,
            scores=phi,
            method="shapley_exact",
            n_samples=-1,
            grand_coalition_value=grand,
        )

    def monte_carlo(self, n_samples: int = 2000, seed: int = 42) -> AttributionResult:
        """
        Monte Carlo Shapley (permutation sampling).
        Each sample draws a random permutation; each player's marginal in that order
        is accumulated. Unbiased estimator converges as 1/sqrt(n_samples).
        """
        rng = random.Random(seed)
        phi: dict[str, float] = {p: 0.0 for p in self.players}

        for _ in range(n_samples):
            perm = self.players[:]
            rng.shuffle(perm)
            S: frozenset[str] = frozenset()
            v_S = self.value_fn(S)
            for player in perm:
                S_new = S | {player}
                v_S_new = self.value_fn(S_new)
                phi[player] += v_S_new - v_S
                S = S_new
                v_S = v_S_new

        for p in phi:
            phi[p] /= n_samples

        grand = self.value_fn(frozenset(self.players))
        return AttributionResult(
            players=self.players,
            scores=phi,
            method="shapley_mc",
            n_samples=n_samples,
            grand_coalition_value=grand,
        )


class BanzhafEngine:
    """
    Computes Banzhaf power index eta_i = E_{S uniform}[v(S + i) - v(S | i not in S)]

    Unlike Shapley, all subsets have equal weight (no factorial weighting).
    More robust to extreme coalition sizes; does NOT sum to v(grand) in general.
    Use monte_carlo for n > 15.
    """

    def __init__(self, players: list[str], value_fn: ValueFn):
        self.players = players
        self.value_fn = value_fn
        self.n = len(players)

    def exact(self) -> AttributionResult:
        """Exact Banzhaf via all 2^(n-1) subsets per player."""
        if self.n > 20:
            raise ValueError(f"Exact Banzhaf infeasible for n={self.n}; use monte_carlo()")

        eta: dict[str, float] = {p: 0.0 for p in self.players}

        for i, player in enumerate(self.players):
            others = [p for p in self.players if p != player]
            n_others = len(others)
            total = 0.0
            count = 1 << n_others
            for mask in range(count):
                S = frozenset(others[j] for j in range(n_others) if mask & (1 << j))
                total += self.value_fn(S | {player}) - self.value_fn(S)
            eta[player] = total / count

        grand = self.value_fn(frozenset(self.players))
        return AttributionResult(
            players=self.players,
            scores=eta,
            method="banzhaf_exact",
            n_samples=-1,
            grand_coalition_value=grand,
        )

    def monte_carlo(self, n_samples: int = 2000, seed: int = 42) -> AttributionResult:
        """
        Monte Carlo Banzhaf: for each sample, draw S uniformly (each player
        included with probability 0.5), then compute marginal for each player.
        """
        rng = np.random.default_rng(seed)
        eta: dict[str, float] = {p: 0.0 for p in self.players}
        counts: dict[str, int] = {p: 0 for p in self.players}

        for _ in range(n_samples):
            included = rng.random(self.n) < 0.5
            S_base = frozenset(p for p, inc in zip(self.players, included) if inc)
            for i, player in enumerate(self.players):
                S_without = S_base - {player}
                S_with = S_without | {player}
                eta[player] += self.value_fn(S_with) - self.value_fn(S_without)
                counts[player] += 1

        for p in eta:
            eta[p] /= counts[p]

        grand = self.value_fn(frozenset(self.players))
        return AttributionResult(
            players=self.players,
            scores=eta,
            method="banzhaf_mc",
            n_samples=n_samples,
            grand_coalition_value=grand,
        )
