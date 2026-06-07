from app.schemas import (
    ComplianceCondition,
    ComplianceRule,
    ComplianceTargetClass,
    EngineeringGraph,
    GraphEdge,
    GraphMeta,
    GraphNode,
    GraphSpace,
)
from app.services.compliance_runner import run_compliance_rules


def test_compliance_runner_must_exist() -> None:
    graph = EngineeringGraph(
        meta=GraphMeta(diagram_id="bld-1"),
        spaces=[
            GraphSpace(space_id="room-1", category="data_hall"),
        ],
    )

    rules = [
        ComplianceRule(
            target_class=ComplianceTargetClass.ROOM,
            target_type="data_hall",
            condition=ComplianceCondition.MUST_EXIST,
            value="true",
        ),
        ComplianceRule(
            target_class=ComplianceTargetClass.EQUIPMENT,
            target_type="ups",
            condition=ComplianceCondition.MUST_EXIST,
            value="true",
        ),
    ]

    report = run_compliance_rules(graph, rules)

    assert report.checks_run == 2
    assert not report.passed
    assert len(report.violations) == 1
    assert report.violations[0].rule.target_type == "ups"
    assert report.violations[0].expected == "true"


def test_compliance_runner_min_area() -> None:
    graph = EngineeringGraph(
        meta=GraphMeta(diagram_id="bld-1"),
        spaces=[
            GraphSpace(space_id="room-1", category="data_hall", area=100.0),
            GraphSpace(space_id="room-2", category="data_hall", area=40.0),
        ],
    )

    rules = [
        ComplianceRule(
            target_class=ComplianceTargetClass.ROOM,
            target_type="data_hall",
            condition=ComplianceCondition.MIN_AREA,
            value=50.0,
        ),
    ]

    report = run_compliance_rules(graph, rules)

    assert report.checks_run == 2
    assert not report.passed
    assert len(report.violations) == 1
    assert report.violations[0].target_object == "room-2"
    assert report.violations[0].actual == 40.0


def test_compliance_runner_must_connect_to() -> None:
    graph = EngineeringGraph(
        meta=GraphMeta(diagram_id="bld-1"),
        nodes=[
            GraphNode(node_id="rack-1", category="rack"),
            GraphNode(node_id="pdu-1", category="pdu"),
            GraphNode(node_id="rack-2", category="rack"),
        ],
        edges=[
            GraphEdge(edge_id="e1", source_id="rack-1", target_id="pdu-1"),
        ],
    )

    rules = [
        ComplianceRule(
            target_class=ComplianceTargetClass.RACK,
            condition=ComplianceCondition.MUST_CONNECT_TO,
            value="pdu",
        ),
    ]

    report = run_compliance_rules(graph, rules)

    assert report.checks_run == 2
    assert not report.passed
    assert len(report.violations) == 1
    assert report.violations[0].target_object == "rack-2"
    assert report.violations[0].expected == "connected to pdu"


def test_compliance_runner_max_pue() -> None:
    graph = EngineeringGraph(
        meta=GraphMeta(diagram_id="bld-1", properties={"pue": 1.8}),
    )

    rules = [
        ComplianceRule(
            target_class=ComplianceTargetClass.BUILDING,
            condition=ComplianceCondition.MAX_PUE,
            value=1.5,
        ),
    ]

    report = run_compliance_rules(graph, rules)

    assert report.checks_run == 1
    assert not report.passed
    assert len(report.violations) == 1
    assert report.violations[0].target_object == "bld-1"
    assert report.violations[0].actual == 1.8


def test_compliance_runner_passing_all() -> None:
    graph = EngineeringGraph(
        meta=GraphMeta(diagram_id="bld-1", properties={"pue": 1.4}),
        spaces=[
            GraphSpace(space_id="room-1", category="data_hall", area=100.0),
        ],
    )

    rules = [
        ComplianceRule(
            target_class=ComplianceTargetClass.BUILDING,
            condition=ComplianceCondition.MAX_PUE,
            value=1.5,
        ),
        ComplianceRule(
            target_class=ComplianceTargetClass.ROOM,
            target_type="data_hall",
            condition=ComplianceCondition.MIN_AREA,
            value=50.0,
        ),
    ]

    report = run_compliance_rules(graph, rules)

    assert report.checks_run == 2
    assert report.passed
    assert len(report.violations) == 0


def test_compliance_runner_must_not_exist() -> None:
    graph = EngineeringGraph(
        meta=GraphMeta(diagram_id="bld-1"),
        spaces=[
            GraphSpace(space_id="room-1", category="unwanted_room"),
        ],
    )

    rules = [
        ComplianceRule(
            target_class=ComplianceTargetClass.ROOM,
            target_type="unwanted_room",
            condition=ComplianceCondition.MUST_EXIST,
            value="false",
        ),
    ]

    report = run_compliance_rules(graph, rules)

    assert report.checks_run == 1
    assert not report.passed
    assert len(report.violations) == 1
    assert report.violations[0].actual == "true"
    assert report.violations[0].expected == "false"
    assert report.violations[0].target_object == "room-1"
