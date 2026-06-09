# Requirements Intel

This file captures the synthesized requirement categories extracted from the
legacy planning files. The checkable canonical version is
`.planning/REQUIREMENTS.md`.

## Governance

- GSD `.planning/` should be the first planning surface.
- Existing autonomous task details must be preserved.
- Source priority, risk gates, selection rules, and replenishment policy must be
  explicit.
- Work must stay one task ID per PR with bounded paths and reported checks.

## Product Capabilities

- Multi-discipline engineering understanding for architecture, electrical,
  plumbing, HVAC, ventilation, data-centres, and other MEP systems.
- Standards and compliance checking with source evidence.
- Property, real-estate, cost, and ROI reasoning.
- Agent-generated reports with warnings, evidence, candidate fixes, and
  approval gates.
- 2D editing for architecture and electrical layouts.

## Technical Capabilities

- Canonical engineering graph schema.
- Parser adapter contracts and optional parser engines.
- Deterministic validation for graph, compliance, loads, PUE, BEC, cost, and
  ROI behavior.
- Hybrid retrieval with vector/text lookup and graph topology reasoning.
- Frontend inspection and review views.

## Demo Capabilities

- Offline golden demo based on committed fixtures.
- No API keys, model weights, file upload, or external network calls.
- Rooms, valuation, compliance, and overlay behavior in the existing Next.js
  shell.
- Honest capability disclosure and deterministic runbook after the demo is
  stable.

## Backlog Sources

The following source pools were transferred into GSD and the legacy files were
removed:

- task manifest -> `.planning/todos/AGENT-TASKS.md`
- backlog -> `.planning/ROADMAP.md`
- raw ideas -> `.planning/seeds/SEED-001-team-direction.md`
