import math
from typing import Any, Literal

from app.schemas import (
    BreakerAnalysisResult,
    ElectricalLoadAnalysis,
    EngineeringGraph,
)


def _build_adjacency(graph: EngineeringGraph) -> dict[str, list[str]]:
    adj: dict[str, list[str]] = {}
    for edge in graph.edges:
        adj.setdefault(edge.source_id, []).append(edge.target_id)
    return adj


def _node_index(graph: EngineeringGraph) -> dict[str, Any]:
    return {n.node_id: n for n in graph.nodes}


def downstream_load_kW(graph: EngineeringGraph, node_id: str) -> float:  # noqa: N802
    """Sum rated_power_kW of a node and everything downstream of it (DFS, cycle-safe)."""
    adj = _build_adjacency(graph)
    nodes = _node_index(graph)
    seen: set[str] = set()

    def _rated(nid: str) -> float:
        node = nodes.get(nid)
        if not node:
            return 0.0
        attrs = node.properties
        return float(attrs.get("rated_power_kW") or attrs.get("power_kW") or 0.0)

    stack = [node_id]
    total = 0.0
    while stack:
        nid = stack.pop()
        if nid in seen:
            continue
        seen.add(nid)
        total += _rated(nid)
        stack.extend(adj.get(nid, []))
    return round(total, 2)


def breaker_overloaded(
    graph: EngineeringGraph,
    node_id: str,
    pf: float = 0.9,
    voltage_V: float = 380.0,  # noqa: N803
    threshold: float = 0.8,
) -> BreakerAnalysisResult:
    """3-phase: I = P / (sqrt(3) * V * pf). Overloaded if I > threshold * ampacity."""
    nodes = _node_index(graph)
    node = nodes.get(node_id)

    if not node:
        return BreakerAnalysisResult(
            node_id=node_id,
            downstream_load_kW=0.0,
            computed_amps=0.0,
            threshold=threshold,
            status="UNKNOWN",
            reason="node not found",
        )

    load_kW = downstream_load_kW(graph, node_id)  # noqa: N806
    attrs = node.properties
    v = float(attrs.get("voltage_V") or voltage_V)
    amps = (load_kW * 1000.0) / (math.sqrt(3) * v * pf) if v > 0 else 0.0

    ampacity = attrs.get("ampacity_A")
    if ampacity is None:
        ampacity = attrs.get("current_A")

    tag = attrs.get("tag") or attrs.get("name")
    if tag is not None:
        tag = str(tag)

    if ampacity is not None:
        ampacity = float(ampacity)
        status = "OVERLOAD" if amps > threshold * ampacity else "OK"
    else:
        status = "NO_RATING"

    status_literal: Literal["OK", "OVERLOAD", "NO_RATING", "UNKNOWN"] = "UNKNOWN"
    if status == "OK":
        status_literal = "OK"
    elif status == "OVERLOAD":
        status_literal = "OVERLOAD"
    elif status == "NO_RATING":
        status_literal = "NO_RATING"

    return BreakerAnalysisResult(
        node_id=node_id,
        tag=tag,
        downstream_load_kW=load_kW,
        computed_amps=round(amps, 1),
        ampacity_A=ampacity,
        threshold=threshold,
        status=status_literal,
    )


def analyze_electrical_loads(graph: EngineeringGraph) -> ElectricalLoadAnalysis:
    """One-shot electrical report for the API."""
    breakers = []
    for node in graph.nodes:
        # Check if the node is a breaker based on category or having ampacity properties
        category = node.category or ""
        # From loads.py trace, filter by type (mapped to category here) or if it has current rating
        if (
            category in ("breaker", "distribution_panel", "busway", "transformer")
            or node.properties.get("ampacity_A") is not None
            or node.properties.get("current_A") is not None
        ):
            breakers.append(breaker_overloaded(graph, node.node_id))

    return ElectricalLoadAnalysis(breakers=breakers)
