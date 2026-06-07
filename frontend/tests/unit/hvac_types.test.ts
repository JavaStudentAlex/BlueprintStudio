import { describe, expect, it } from "vitest";
import type { HVACEquipmentRule, PUEAnalysisResult } from "@/types";

describe("HVAC Analysis Types", () => {
  it("should type-check a valid PUEAnalysisResult payload", () => {
    const mockRule: HVACEquipmentRule = {
      equipment_id: "chiller-1",
      rule_name: "Chiller Minimum COP",
      expected: ">= 3.0",
      actual: "3.5",
      passed: true,
    };

    const mockPayload: PUEAnalysisResult = {
      total_facility_power_kW: 20.0,
      total_it_power_kW: 15.0,
      pue: 1.33,
      equipment_rules_passed: 1,
      equipment_rules_failed: 0,
      equipment_rules: [mockRule],
    };

    expect(mockPayload.pue).toBe(1.33);
    expect(mockPayload.equipment_rules[0].passed).toBe(true);
  });
});
