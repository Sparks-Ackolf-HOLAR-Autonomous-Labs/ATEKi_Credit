"""
Group topology definitions for ATEKi non-egalitarian attribution.

A topology defines HOW players communicate/coordinate when forming coalitions.
The same Shapley/Banzhaf values can be reweighted by topology-induced communication
weights, yielding topology-conditional attribution.

Four canonical topologies (plus custom):
  Network (flat/peer-to-peer): all pairs connected equally; uniform graph Shapley
  Supervisor: one hub coordinates all others (star graph)
  Hierarchical: tree with chain-of-command; depth determines discount factor
  Custom: arbitrary adjacency matrix (any DAG or undirected graph)

Topology-weighted Shapley: phi_i^G = phi_i * w_i(G)
where w_i(G) is the centrality-derived weight for player i under graph G.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import numpy as np


@dataclass
class TopologyResult:
    """Communication weights and centrality measures for one topology."""
    topology_name: str
    players: list[str]
    adjacency: np.ndarray               # n x n, symmetric for undirected
    degree_centrality: dict[str, float]
    betweenness_centrality: dict[str, float]
    # Normalized weights summing to 1.0; used to rescale attribution
    communication_weight: dict[str, float]


def _degree_centrality(adj: np.ndarray, players: list[str]) -> dict[str, float]:
    n = len(players)
    if n <= 1:
        return {p: 1.0 for p in players}
    degree = adj.sum(axis=1)
    max_deg = float(n - 1)
    return {p: float(degree[i]) / max_deg for i, p in enumerate(players)}


def _betweenness_approx(adj: np.ndarray, players: list[str]) -> dict[str, float]:
    """Approximate betweenness via BFS shortest-path counts (unweighted)."""
    n = len(players)
    bc = np.zeros(n)
    for s in range(n):
        # BFS
        visited = [-1] * n
        visited[s] = 0
        queue = [s]
        order = []
        pred: list[list[int]] = [[] for _ in range(n)]
        sigma = np.zeros(n)
        sigma[s] = 1.0
        dist = np.full(n, -1)
        dist[s] = 0
        qi = 0
        while qi < len(queue):
            v = queue[qi]; qi += 1
            order.append(v)
            for w in range(n):
                if adj[v, w] > 0:
                    if dist[w] < 0:
                        dist[w] = dist[v] + 1
                        queue.append(w)
                    if dist[w] == dist[v] + 1:
                        sigma[w] += sigma[v]
                        pred[w].append(v)
        delta = np.zeros(n)
        for w in reversed(order):
            for v in pred[w]:
                if sigma[w] > 0:
                    delta[v] += (sigma[v] / sigma[w]) * (1.0 + delta[w])
            if w != s:
                bc[w] += delta[w]

    norm = (n - 1) * (n - 2) if n > 2 else 1.0
    bc = bc / norm
    return {p: float(bc[i]) for i, p in enumerate(players)}


def _communication_weights(centrality: dict[str, float]) -> dict[str, float]:
    total = sum(centrality.values())
    if total < 1e-12:
        n = len(centrality)
        return {p: 1.0 / n for p in centrality}
    return {p: v / total for p, v in centrality.items()}


class NetworkTopology:
    """
    Flat peer-to-peer: all players connected to all others (complete graph).
    All degrees equal => uniform communication weights.
    """

    def __init__(self, players: list[str]):
        self.players = players

    def build(self) -> TopologyResult:
        n = len(self.players)
        adj = np.ones((n, n)) - np.eye(n)
        dc = _degree_centrality(adj, self.players)
        bc = _betweenness_approx(adj, self.players)
        return TopologyResult(
            topology_name="network",
            players=self.players,
            adjacency=adj,
            degree_centrality=dc,
            betweenness_centrality=bc,
            communication_weight=_communication_weights(dc),
        )


class SupervisorTopology:
    """
    Star graph: one supervisor hub connected to all others, others not connected to each other.
    Supervisor has maximum degree centrality; others have degree 1.

    Args:
        players: All player ids.
        supervisor_id: Which player is the hub. Defaults to first in list.
    """

    def __init__(self, players: list[str], supervisor_id: Optional[str] = None):
        self.players = players
        self.supervisor_id = supervisor_id or players[0]

    def build(self) -> TopologyResult:
        n = len(self.players)
        adj = np.zeros((n, n))
        hub = self.players.index(self.supervisor_id)
        for i in range(n):
            if i != hub:
                adj[hub, i] = 1.0
                adj[i, hub] = 1.0
        dc = _degree_centrality(adj, self.players)
        bc = _betweenness_approx(adj, self.players)
        # Weight driver is DEGREE, not betweenness: on a star every leaf has
        # betweenness exactly 0 (a degree-1 vertex is never interior to a
        # shortest path) and the hub exactly 1, so BC weights are winner-
        # takes-all and the supervisor column carries no leaf information.
        # Degree gives hub = (n-1)/2(n-1) = half the mass and leaves the
        # rest -- "hub dominates but not exclusively", which is what the
        # supervisor topology is documented to mean. BC is still reported.
        return TopologyResult(
            topology_name="supervisor",
            players=self.players,
            adjacency=adj,
            degree_centrality=dc,
            betweenness_centrality=bc,
            communication_weight=_communication_weights(dc),
        )


class HierarchicalTopology:
    """
    Balanced k-ary tree (default k=2, binary tree).
    Players are assigned levels root->leaf. Root has highest centrality.
    Depth discount: players at depth d have weight proportional to 1/(d+1).

    Args:
        players: All player ids; first player becomes root.
        branching: Number of children per node (k in k-ary tree).
    """

    def __init__(self, players: list[str], branching: int = 2):
        self.players = players
        self.branching = branching

    def _tree_adjacency(self) -> tuple[np.ndarray, dict[str, int]]:
        n = len(self.players)
        adj = np.zeros((n, n))
        depth: dict[str, int] = {}
        depth[self.players[0]] = 0
        for i in range(n):
            for c in range(1, self.branching + 1):
                child_idx = self.branching * i + c
                if child_idx < n:
                    adj[i, child_idx] = 1.0
                    adj[child_idx, i] = 1.0
                    depth[self.players[child_idx]] = depth[self.players[i]] + 1
        return adj, depth

    def build(self) -> TopologyResult:
        adj, depth = self._tree_adjacency()
        dc = _degree_centrality(adj, self.players)
        bc = _betweenness_approx(adj, self.players)
        # Depth-discounted weight: root (depth 0) gets full weight
        depth_weight = {p: 1.0 / (depth.get(p, 0) + 1) for p in self.players}
        comm_w = _communication_weights(depth_weight)
        return TopologyResult(
            topology_name="hierarchical",
            players=self.players,
            adjacency=adj,
            degree_centrality=dc,
            betweenness_centrality=bc,
            communication_weight=comm_w,
        )


class CustomTopology:
    """
    Arbitrary topology defined by an adjacency matrix or edge list.

    Args:
        players: Player ids in order matching adjacency rows/cols.
        adjacency: n x n numpy array. Symmetric for undirected.
        weight_by: "degree" | "betweenness" — which centrality drives comm weights.
    """

    def __init__(
        self,
        players: list[str],
        adjacency: np.ndarray,
        weight_by: str = "betweenness",
        name: str = "custom",
    ):
        self.players = players
        self.adjacency = adjacency
        self.weight_by = weight_by
        self.name = name

    def build(self) -> TopologyResult:
        dc = _degree_centrality(self.adjacency, self.players)
        bc = _betweenness_approx(self.adjacency, self.players)
        source = dc if self.weight_by == "degree" else bc
        return TopologyResult(
            topology_name=self.name,
            players=self.players,
            adjacency=self.adjacency.copy(),
            degree_centrality=dc,
            betweenness_centrality=bc,
            communication_weight=_communication_weights(source),
        )
