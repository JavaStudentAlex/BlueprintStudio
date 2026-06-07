from app.schemas import EngineeringGraph, HVACEquipmentRule, PUEAnalysisResult


def analyze_hvac(graph: EngineeringGraph) -> PUEAnalysisResult:
    total_facility_power_kw = 0.0
    total_it_power_kw = 0.0

    equipment_rules = []

    # Simple rule-table checks based on FlowDraft context
    # - Chillers must have COP > 3.0 (efficiency > 3.0, COP, etc.)
    # - Racks should have power_kW
    # - CRAC should have cooling_capacity_kW

    # Iterate over all nodes in the graph
    for node in graph.nodes:
        # Summing powers for PUE
        power_kw = float(
            node.properties.get("power_kW") or node.properties.get("rated_power_kW") or 0.0
        )

        # IT equipment vs Facility equipment
        # Typical IT: rack, server
        category = node.category or ""
        category_lower = category.lower()

        if "rack" in category_lower or "server" in category_lower:
            total_it_power_kw += power_kw
            total_facility_power_kw += power_kw  # IT power is part of total facility power
        elif category_lower in (
            "chiller",
            "crac",
            "crah",
            "cooling_tower",
            "pdu",
            "ups",
            "hvac",
            "pump",
            "fan",
        ):
            total_facility_power_kw += power_kw

            # Simple rule check: Chiller must have COP >= 3.0
            if category_lower == "chiller":
                try:
                    cop = float(node.properties.get("cop") or 0.0)
                except (ValueError, TypeError):
                    cop = 0.0
                passed = cop >= 3.0
                equipment_rules.append(
                    HVACEquipmentRule(
                        equipment_id=node.node_id,
                        rule_name="Chiller Minimum COP",
                        expected=">= 3.0",
                        actual=str(cop),
                        passed=passed,
                    )
                )
            # Simple rule check: CRAC must have cooling_capacity_kW > 0
            elif category_lower == "crac":
                try:
                    cooling = float(node.properties.get("cooling_capacity_kW") or 0.0)
                except (ValueError, TypeError):
                    cooling = 0.0
                passed = cooling > 0
                equipment_rules.append(
                    HVACEquipmentRule(
                        equipment_id=node.node_id,
                        rule_name="CRAC Minimum Cooling Capacity",
                        expected="> 0.0",
                        actual=str(cooling),
                        passed=passed,
                    )
                )

    # Calculate PUE = Total Facility Power / Total IT Power
    pue = 0.0
    if total_it_power_kw > 0:
        pue = round(total_facility_power_kw / total_it_power_kw, 2)

    passed_rules = sum(1 for r in equipment_rules if r.passed)
    failed_rules = sum(1 for r in equipment_rules if not r.passed)

    return PUEAnalysisResult(
        total_facility_power_kW=round(total_facility_power_kw, 2),
        total_it_power_kW=round(total_it_power_kw, 2),
        pue=pue,
        equipment_rules_passed=passed_rules,
        equipment_rules_failed=failed_rules,
        equipment_rules=equipment_rules,
    )
