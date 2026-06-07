from typing import Any

from app.schemas import (
    ComplianceCondition,
    ComplianceRule,
    ComplianceTargetClass,
    ComplianceValidationReport,
    ComplianceViolation,
    EngineeringGraph,
)


def _get_objects_by_class(
    graph: EngineeringGraph, target_class: ComplianceTargetClass, target_type: str | None = None
) -> list[tuple[str, Any]]:
    objects: list[tuple[str, Any]] = []

    if target_class in (ComplianceTargetClass.ROOM, ComplianceTargetClass.ANY):
        for space in graph.spaces:
            if target_type and space.category != target_type:
                continue
            objects.append((space.space_id, space))

    if target_class in (
        ComplianceTargetClass.EQUIPMENT,
        ComplianceTargetClass.RACK,
        ComplianceTargetClass.ANY,
    ):
        # We assume RACK and EQUIPMENT are both stored as nodes
        # If the target_class is strictly RACK, we might want to check the node category
        for node in graph.nodes:
            if target_class == ComplianceTargetClass.RACK and node.category != "rack":
                continue
            if target_type and node.category != target_type:
                continue
            objects.append((node.node_id, node))

    if target_class in (ComplianceTargetClass.BUILDING, ComplianceTargetClass.ANY):
        objects.append((graph.meta.diagram_id or "building", graph.meta))

    return objects


def run_compliance_rules(
    graph: EngineeringGraph, rules: list[ComplianceRule]
) -> ComplianceValidationReport:
    violations: list[ComplianceViolation] = []
    checks_run = 0

    for rule in rules:
        objects = _get_objects_by_class(graph, rule.target_class, rule.target_type)

        if rule.condition == ComplianceCondition.MUST_EXIST:
            checks_run += 1
            expected = rule.value if isinstance(rule.value, str) else "true"
            is_expected_true = expected.lower() in ("true", "1", "yes")

            if is_expected_true and not objects:
                violations.append(
                    ComplianceViolation(
                        rule=rule,
                        target_object=None,
                        actual="false",
                        expected="true",
                        message=(
                            f"Missing required object: {rule.target_class} "
                            f"of type {rule.target_type}"
                        ),
                        severity="error",
                        source=rule.source,
                    )
                )
            elif not is_expected_true and objects:
                violations.append(
                    ComplianceViolation(
                        rule=rule,
                        target_object=objects[0][0],
                        actual="true",
                        expected="false",
                        message=(
                            f"Object should not exist: {rule.target_class} "
                            f"of type {rule.target_type}"
                        ),
                        severity="error",
                        source=rule.source,
                    )
                )
            continue

        for obj_id, obj in objects:
            checks_run += 1

            if rule.condition == ComplianceCondition.MUST_CONNECT_TO:
                expected_type = str(rule.value)
                connected = False
                for edge in graph.edges:
                    if edge.source_id == obj_id or edge.target_id == obj_id:
                        other_id = edge.target_id if edge.source_id == obj_id else edge.source_id
                        # find type of other_id
                        other_type = None
                        for n in graph.nodes:
                            if n.node_id == other_id:
                                other_type = n.category
                                break
                        if other_type == expected_type:
                            connected = True
                            break
                if not connected:
                    violations.append(
                        ComplianceViolation(
                            rule=rule,
                            target_object=obj_id,
                            actual="not connected",
                            expected=f"connected to {expected_type}",
                            message=f"Object {obj_id} is not connected to {expected_type}",
                            severity="error",
                            source=rule.source,
                        )
                    )

            elif rule.condition == ComplianceCondition.MIN_AREA:
                area = getattr(obj, "area", None)
                if area is None and hasattr(obj, "properties"):
                    area = obj.properties.get("area")

                if area is not None:
                    try:
                        area_val = float(area)
                        expected_val = float(rule.value)
                        if area_val < expected_val:
                            violations.append(
                                ComplianceViolation(
                                    rule=rule,
                                    target_object=obj_id,
                                    actual=area_val,
                                    expected=expected_val,
                                    message=f"Area {area_val} is less than minimum {expected_val}",
                                    severity="error",
                                    source=rule.source,
                                )
                            )
                    except (ValueError, TypeError):
                        pass

            elif rule.condition == ComplianceCondition.MAX_PUE:
                pue = getattr(obj, "properties", {}).get("pue")
                if pue is not None:
                    try:
                        pue_val = float(pue)
                        expected_val = float(rule.value)
                        if pue_val > expected_val:
                            violations.append(
                                ComplianceViolation(
                                    rule=rule,
                                    target_object=obj_id,
                                    actual=pue_val,
                                    expected=expected_val,
                                    message=f"PUE {pue_val} is greater than maximum {expected_val}",
                                    severity="error",
                                    source=rule.source,
                                )
                            )
                    except (ValueError, TypeError):
                        pass

            elif rule.condition == ComplianceCondition.MIN_CLEARANCE:
                clearance = getattr(obj, "properties", {}).get("clearance")
                if clearance is not None:
                    try:
                        c_val = float(clearance)
                        e_val = float(rule.value)
                        if c_val < e_val:
                            violations.append(
                                ComplianceViolation(
                                    rule=rule,
                                    target_object=obj_id,
                                    actual=c_val,
                                    expected=e_val,
                                    message=f"Clearance {c_val} is less than minimum {e_val}",
                                    severity="error",
                                    source=rule.source,
                                )
                            )
                    except (ValueError, TypeError):
                        pass
            elif rule.condition == ComplianceCondition.MIN_POWER:
                power = getattr(obj, "properties", {}).get("power")
                if power is not None:
                    try:
                        p_val = float(power)
                        e_val = float(rule.value)
                        if p_val < e_val:
                            violations.append(
                                ComplianceViolation(
                                    rule=rule,
                                    target_object=obj_id,
                                    actual=p_val,
                                    expected=e_val,
                                    message=f"Power {p_val} is less than minimum {e_val}",
                                    severity="error",
                                    source=rule.source,
                                )
                            )
                    except (ValueError, TypeError):
                        pass
            elif rule.condition == ComplianceCondition.MIN_WIDTH:
                width = getattr(obj, "properties", {}).get("width")
                if width is not None:
                    try:
                        w_val = float(width)
                        e_val = float(rule.value)
                        if w_val < e_val:
                            violations.append(
                                ComplianceViolation(
                                    rule=rule,
                                    target_object=obj_id,
                                    actual=w_val,
                                    expected=e_val,
                                    message=f"Width {w_val} is less than minimum {e_val}",
                                    severity="error",
                                    source=rule.source,
                                )
                            )
                    except (ValueError, TypeError):
                        pass
            elif rule.condition == ComplianceCondition.MAX_WIDTH:
                width = getattr(obj, "properties", {}).get("width")
                if width is not None:
                    try:
                        w_val = float(width)
                        e_val = float(rule.value)
                        if w_val > e_val:
                            violations.append(
                                ComplianceViolation(
                                    rule=rule,
                                    target_object=obj_id,
                                    actual=w_val,
                                    expected=e_val,
                                    message=f"Width {w_val} is greater than maximum {e_val}",
                                    severity="error",
                                    source=rule.source,
                                )
                            )
                    except (ValueError, TypeError):
                        pass

    return ComplianceValidationReport(violations=violations, checks_run=checks_run)
