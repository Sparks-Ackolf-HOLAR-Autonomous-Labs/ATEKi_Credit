"""
Report generation for ATEKi attribution results.
Produces JSON-serializable dicts and markdown text summaries.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any

from .shapley import AttributionResult
from .topology import TopologyResult
from .influence import LOOResult, DataValuationResult


def attribution_to_dict(result: AttributionResult) -> dict[str, Any]:
    return {
        "method": result.method,
        "n_samples": result.n_samples,
        "grand_coalition_value": result.grand_coalition_value,
        "scores": result.scores,
        "normalized": result.normalized,
        "rank": result.rank(),
    }


def topology_to_dict(result: TopologyResult) -> dict[str, Any]:
    return {
        "topology_name": result.topology_name,
        "players": result.players,
        "degree_centrality": result.degree_centrality,
        "betweenness_centrality": result.betweenness_centrality,
        "communication_weight": result.communication_weight,
    }


def loo_to_dict(result: LOOResult) -> dict[str, Any]:
    return {
        "method": result.method,
        "grand_value": result.grand_value,
        "scores": result.scores,
        "rank": result.rank(),
    }


def write_json(data: dict, path: str | Path) -> None:
    # Atomic replace so a kill mid-dump cannot truncate a previous good result.
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    tmp.replace(path)


def attribution_report(result: AttributionResult, topology: TopologyResult | None = None) -> str:
    lines: list[str] = []
    lines.append(f"# ATEKi Attribution Report")
    lines.append(f"Method: {result.method}  |  samples: {result.n_samples}")
    lines.append(f"Grand coalition value: {result.grand_coalition_value:.4f}")
    lines.append("")
    lines.append("| Rank | Player | Score | % of Grand |")
    lines.append("|------|--------|-------|------------|")
    for i, (p, v) in enumerate(result.rank(), 1):
        pct = result.normalized.get(p, 0.0) * 100
        lines.append(f"| {i} | {p} | {v:.4f} | {pct:.1f}% |")

    if topology is not None:
        lines.append("")
        lines.append(f"## Topology: {topology.topology_name}")
        lines.append("| Player | Degree | Betweenness | Comm. Weight |")
        lines.append("|--------|--------|-------------|--------------|")
        for p in topology.players:
            dc = topology.degree_centrality.get(p, 0.0)
            bc = topology.betweenness_centrality.get(p, 0.0)
            cw = topology.communication_weight.get(p, 0.0)
            lines.append(f"| {p} | {dc:.3f} | {bc:.3f} | {cw:.3f} |")

    return "\n".join(lines)
