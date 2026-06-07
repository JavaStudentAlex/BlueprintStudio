"use client";

import demoComplianceReport from "../../../tests/fixtures/flowdraft/demo_compliance_report.json";

export function ComplianceView() {
  const violations = demoComplianceReport.violations || [];
  const checksRun = demoComplianceReport.checks_run;
  const passed = demoComplianceReport.passed;

  return (
    <div className="flex min-w-0 flex-1 flex-col overflow-auto bg-brand-surface p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-brand-navy">
          Compliance View
        </h2>
        <div className="mt-2 flex items-center gap-3">
          <span className="rounded-full bg-brand-surface-soft px-3 py-1 text-sm font-medium text-brand-ink">
            Checks run: {checksRun}
          </span>
          <span
            className={`rounded-full px-3 py-1 text-sm font-medium ${
              passed
                ? "bg-emerald-100 text-emerald-800"
                : "bg-red-100 text-red-800"
            }`}
          >
            {passed ? "Passed" : "Failed"}
          </span>
        </div>
      </div>

      <div className="flex flex-col gap-4">
        {violations.map((violation: any, idx: number) => (
          <div
            key={idx}
            className="rounded-xl border border-red-200 bg-red-50 p-4"
          >
            <div className="flex items-start justify-between">
              <div>
                <h3 className="font-semibold text-red-900">
                  Violation{" "}
                  {violation.geometry_id ? `in ${violation.geometry_id}` : ""}
                </h3>
                <p className="mt-1 text-sm text-red-800">{violation.message}</p>
              </div>
            </div>
            {violation.rule && (
              <div className="mt-3 rounded-lg border border-red-100 bg-white p-3 text-sm">
                <div className="font-medium text-brand-ink">Rule context</div>
                <div className="mt-1 text-brand-subtle">
                  {violation.rule.description}
                </div>
              </div>
            )}
          </div>
        ))}
        {violations.length === 0 && (
          <div className="text-sm text-brand-subtle">No violations found.</div>
        )}
      </div>
    </div>
  );
}
