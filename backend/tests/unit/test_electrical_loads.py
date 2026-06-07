from app.schemas import EngineeringGraph, GraphEdge, GraphNode
from app.services.electrical_loads import (
    analyze_electrical_loads,
    downstream_load_kW,
)


def test_downstream_load_kW_ok():  # noqa: N802
    node1 = GraphNode(
        node_id="n1", category="breaker", properties={"rated_power_kW": 10, "ampacity_A": 200}
    )
    node2 = GraphNode(node_id="n2", category="equipment", properties={"rated_power_kW": 20})
    node3 = GraphNode(node_id="n3", category="equipment", properties={"power_kW": 30})

    edge1 = GraphEdge(edge_id="e1", source_id="n1", target_id="n2")
    edge2 = GraphEdge(edge_id="e2", source_id="n1", target_id="n3")

    graph = EngineeringGraph(nodes=[node1, node2, node3], edges=[edge1, edge2])

    load = downstream_load_kW(graph, "n1")
    assert load == 60.0  # 10 + 20 + 30

    analysis = analyze_electrical_loads(graph)
    assert len(analysis.breakers) == 1
    breaker = analysis.breakers[0]
    assert breaker.node_id == "n1"
    assert breaker.status == "OK"  # With ampacity=200, 200*0.8=160 > 101.3, so it is OK.


def test_breaker_overloaded():
    node1 = GraphNode(
        node_id="n1", category="breaker", properties={"rated_power_kW": 10, "ampacity_A": 100}
    )
    node2 = GraphNode(node_id="n2", category="equipment", properties={"rated_power_kW": 20})
    node3 = GraphNode(node_id="n3", category="equipment", properties={"power_kW": 30})

    edge1 = GraphEdge(edge_id="e1", source_id="n1", target_id="n2")
    edge2 = GraphEdge(edge_id="e2", source_id="n1", target_id="n3")

    graph = EngineeringGraph(nodes=[node1, node2, node3], edges=[edge1, edge2])

    analysis = analyze_electrical_loads(graph)
    assert len(analysis.breakers) == 1
    breaker = analysis.breakers[0]
    assert breaker.node_id == "n1"
    assert breaker.status == "OVERLOAD"
    assert breaker.computed_amps > 80.0


def test_breaker_ok():
    node1 = GraphNode(
        node_id="n1", category="breaker", properties={"rated_power_kW": 10, "ampacity_A": 200}
    )
    node2 = GraphNode(node_id="n2", category="equipment", properties={"rated_power_kW": 20})

    edge1 = GraphEdge(edge_id="e1", source_id="n1", target_id="n2")

    graph = EngineeringGraph(nodes=[node1, node2], edges=[edge1])

    analysis = analyze_electrical_loads(graph)
    assert len(analysis.breakers) == 1
    breaker = analysis.breakers[0]
    assert breaker.node_id == "n1"
    assert breaker.status == "OK"
    assert breaker.computed_amps < 200 * 0.8


def test_breaker_no_rating():
    node1 = GraphNode(node_id="n1", category="breaker", properties={"rated_power_kW": 10})
    graph = EngineeringGraph(nodes=[node1], edges=[])

    analysis = analyze_electrical_loads(graph)
    assert len(analysis.breakers) == 1
    breaker = analysis.breakers[0]
    assert breaker.node_id == "n1"
    assert breaker.status == "NO_RATING"


def test_downstream_load_cycle_safe():
    node1 = GraphNode(
        node_id="n1", category="breaker", properties={"rated_power_kW": 10, "ampacity_A": 200}
    )
    node2 = GraphNode(node_id="n2", category="equipment", properties={"rated_power_kW": 20})

    edge1 = GraphEdge(edge_id="e1", source_id="n1", target_id="n2")
    edge2 = GraphEdge(edge_id="e2", source_id="n2", target_id="n1")  # cycle

    graph = EngineeringGraph(nodes=[node1, node2], edges=[edge1, edge2])

    load = downstream_load_kW(graph, "n1")
    assert load == 30.0  # should not loop infinitely
