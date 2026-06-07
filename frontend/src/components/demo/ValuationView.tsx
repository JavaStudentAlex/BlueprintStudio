"use client";

// There isn't a corresponding JSON file in fixtures for Valuation demo data,
// but the acceptance criteria asks for "valuation... render deterministic fixture data".
// We will mock the deterministic data locally here.

const valuationData = {
  propertyValue: "$2,450,000",
  confidence: "High",
  factors: [
    {
      name: "Location",
      impact: "+15%",
      description: "Prime district location",
    },
    {
      name: "Compliance",
      impact: "-2%",
      description: "Minor compliance issues detected",
    },
    { name: "Condition", impact: "+5%", description: "Recently renovated" },
  ],
  estimatedROI: "8.5%",
};

export function ValuationView() {
  return (
    <div className="flex min-w-0 flex-1 flex-col overflow-auto bg-brand-surface p-6">
      <h2 className="mb-6 text-2xl font-semibold text-brand-navy">
        Property Valuation
      </h2>

      <div className="mb-6 flex items-center gap-6">
        <div className="rounded-2xl border border-brand-line bg-white p-6 shadow-sm">
          <div className="text-sm font-medium uppercase text-brand-subtle">
            Estimated Value
          </div>
          <div className="mt-2 text-4xl font-bold text-brand-blue">
            {valuationData.propertyValue}
          </div>
        </div>
        <div className="rounded-2xl border border-brand-line bg-white p-6 shadow-sm">
          <div className="text-sm font-medium uppercase text-brand-subtle">
            Estimated ROI
          </div>
          <div className="mt-2 text-4xl font-bold text-brand-orange">
            {valuationData.estimatedROI}
          </div>
        </div>
        <div className="rounded-2xl border border-brand-line bg-white p-6 shadow-sm">
          <div className="text-sm font-medium uppercase text-brand-subtle">
            Confidence
          </div>
          <div className="mt-2 text-4xl font-bold text-emerald-600">
            {valuationData.confidence}
          </div>
        </div>
      </div>

      <h3 className="mb-4 text-lg font-medium text-brand-navy">
        Valuation Factors
      </h3>
      <div className="flex flex-col gap-3">
        {valuationData.factors.map((factor, idx) => {
          const isPositive = factor.impact.startsWith("+");
          return (
            <div
              key={idx}
              className="flex items-center justify-between rounded-xl border border-brand-line bg-white p-4"
            >
              <div>
                <div className="font-semibold text-brand-ink">
                  {factor.name}
                </div>
                <div className="text-sm text-brand-subtle">
                  {factor.description}
                </div>
              </div>
              <div
                className={`text-lg font-bold ${isPositive ? "text-emerald-600" : "text-red-600"}`}
              >
                {factor.impact}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
