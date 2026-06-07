from app.schemas import EngineeringGraph, GraphMeta, GraphNode
from app.services.hvac_analysis import analyze_hvac


def test_analyze_hvac_pue_and_rules() -> None:
    # Build a simple datacentre/HVAC graph fixture
    graph = EngineeringGraph(
        meta=GraphMeta(diagram_id="dc-demo"),
        nodes=[
            # IT Equipment (Rack)
            GraphNode(node_id="rack-1", category="rack", properties={"power_kW": 10.0}),
            # IT Equipment (Server)
            GraphNode(node_id="srv-1", category="server", properties={"power_kW": 5.0}),
            # Facility Equipment (Chiller - passing rule)
            GraphNode(
                node_id="chiller-1", category="chiller", properties={"power_kW": 2.0, "cop": 3.5}
            ),
            # Facility Equipment (Chiller - failing rule)
            GraphNode(
                node_id="chiller-2", category="chiller", properties={"power_kW": 2.0, "cop": 2.8}
            ),
            # Facility Equipment (CRAC - passing rule)
            GraphNode(
                node_id="crac-1",
                category="crac",
                properties={"power_kW": 1.0, "cooling_capacity_kW": 20.0},
            ),
        ],
    )

    result = analyze_hvac(graph)

    # IT power should be 10.0 + 5.0 = 15.0
    assert result.total_it_power_kW == 15.0

    # Facility power should be IT (15.0) + Chiller1 (2.0) + Chiller2 (2.0) + CRAC (1.0) = 20.0
    assert result.total_facility_power_kW == 20.0

    # PUE = 20.0 / 15.0 = 1.33
    assert result.pue == 1.33

    # Rules
    # We expect 3 rules to be evaluated (2 chillers, 1 crac)
    assert len(result.equipment_rules) == 3

    # Check passes and fails
    assert result.equipment_rules_passed == 2  # chiller-1, crac-1
    assert result.equipment_rules_failed == 1  # chiller-2

    # Verify specific rules
    chiller2_rule = next(r for r in result.equipment_rules if r.equipment_id == "chiller-2")
    assert not chiller2_rule.passed
    assert chiller2_rule.actual == "2.8"

    chiller1_rule = next(r for r in result.equipment_rules if r.equipment_id == "chiller-1")
    assert chiller1_rule.passed
    assert chiller1_rule.actual == "3.5"

    crac1_rule = next(r for r in result.equipment_rules if r.equipment_id == "crac-1")
    assert crac1_rule.passed
    assert crac1_rule.actual == "20.0"


def test_analyze_hvac_no_it_power() -> None:
    graph = EngineeringGraph(
        meta=GraphMeta(diagram_id="dc-empty"),
        nodes=[
            GraphNode(
                node_id="chiller-1", category="chiller", properties={"power_kW": 2.0, "cop": 3.5}
            )
        ],
    )
    result = analyze_hvac(graph)
    assert result.total_it_power_kW == 0.0
    assert result.total_facility_power_kW == 2.0
    assert result.pue == 0.0  # Avoid division by zero
    assert result.equipment_rules_passed == 1
    assert result.equipment_rules_failed == 0
