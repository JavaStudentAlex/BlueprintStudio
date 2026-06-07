from app.schemas import (
    ComplianceCondition,
    ComplianceGeometryObject,
    ComplianceRule,
    ComplianceTargetClass,
    ComplianceValidationReport,
    ComplianceViolation,
)


def test_compliance_rule_numeric_coercion() -> None:
    # Test numeric coercion for a min_area condition
    rule = ComplianceRule(
        target_class=ComplianceTargetClass.ROOM,
        condition=ComplianceCondition.MIN_AREA,
        value=" 15.5 ",  # String should be coerced to float
        unit="sqm",
        description="Minimum area check",
    )
    assert rule.value == 15.5
    assert rule.unit == "sqm"

    # Test int coercion for max_pue
    rule2 = ComplianceRule(
        target_class=ComplianceTargetClass.BUILDING,
        condition=ComplianceCondition.MAX_PUE,
        value=2,
    )
    assert rule2.value == 2.0


def test_compliance_rule_string_value_topology() -> None:
    # Test must_connect_to where value is a string identifier
    rule = ComplianceRule(
        target_class=ComplianceTargetClass.EQUIPMENT,
        condition=ComplianceCondition.MUST_CONNECT_TO,
        value="distribution_panel",
    )
    assert rule.value == "distribution_panel"


def test_compliance_rule_existence() -> None:
    # Test must_exist rule
    rule = ComplianceRule(
        target_class=ComplianceTargetClass.ROOM,
        target_type="data_hall",
        condition=ComplianceCondition.MUST_EXIST,
        value="true",
    )
    assert rule.target_type == "data_hall"
    assert rule.condition == "must_exist"


def test_compliance_geometry_object_alias() -> None:
    # Test population by name / alias 'class'
    obj = ComplianceGeometryObject(
        id="room-1",
        **{"class": ComplianceTargetClass.ROOM},
        type="data_hall",
        calculated_metrics={"area": 20.5},
        links=["equip-1"],
    )
    assert obj.id == "room-1"
    assert obj.cls == "Room"
    assert obj.calculated_metrics["area"] == 20.5
    assert obj.links == ["equip-1"]


def test_compliance_violation_and_report() -> None:
    rule = ComplianceRule(
        target_class=ComplianceTargetClass.BUILDING,
        condition=ComplianceCondition.MAX_PUE,
        value=1.5,
    )

    violation = ComplianceViolation(
        rule=rule,
        target_object="bld-01",
        actual=1.8,
        expected=1.5,
        message="PUE is too high",
        severity="error",
        source="Green Standard 2024",
    )

    assert violation.target_object == "bld-01"
    assert violation.actual == 1.8
    assert violation.expected == 1.5
    assert violation.message == "PUE is too high"
    assert violation.severity == "error"
    assert violation.source == "Green Standard 2024"

    report = ComplianceValidationReport(violations=[violation], checks_run=1)

    assert report.checks_run == 1
    assert not report.passed
    assert len(report.violations) == 1
