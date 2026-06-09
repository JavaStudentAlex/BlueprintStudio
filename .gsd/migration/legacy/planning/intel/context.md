# Context Intel

## Product Context

BlueprintStudio is a construction-analysis application with a FastAPI backend,
LangGraph chat/report orchestration, MemoryPalace-backed document recall in
production-like runs, SQLite-backed registries/checkpoints, and a Next.js
App Router frontend.

The intended product is a multi-discipline building-engineering agent covering
architecture, electrical systems, plumbing, HVAC, ventilation, data-centre
analysis where useful for demos, standards/compliance checking, real-estate and
cost data, 2D editing, and evidence-backed reports.

## Architecture Context

The target architecture is hybrid:

- controlled parsers and extractors
- authoritative engineering graph
- deterministic validation and rule engines
- vector/text retrieval for direct source lookup
- graph retrieval for topology and multi-hop reasoning
- LLM explanation and candidate-fix generation
- human approval for physical or compliance-impacting changes

MemoryPalace is useful for agent memory and document recall, but it is not the
authoritative engineering graph.

## FlowDraft Context

FlowDraft contributes useful contracts and prototype behavior:

- unified graph schema for floor plans, P&ID, SLD, and fused graphs
- parser routing for floor plans, P&ID, SLD, fused graphs, data-centre diagrams,
  cooling P&ID, and AUTO mode
- point-in-polygon fusion of MEP nodes into architectural spaces
- deterministic PUE, BEC, electrical load, breaker headroom, property value,
  and ROI calculations
- fixture-backed offline demo behavior with rooms, valuation, compliance, and
  overlay views

BlueprintStudio should absorb the stable contracts and engines behind its
existing backend/frontend surfaces. It should not copy FlowDraft as a separate
app or import large weights, raw drawings, generated overlays, or secret files.

## CrashPine Context

CrashPine upstream contains a standalone FlowDraft demo replacement tree,
honesty docs, Docker/juror packaging, a graph-to-3D twin page, and a capability
roadmap page. The replacement tree is not safe to merge because it removes this
repo's backend, frontend, tests, and planning surfaces.

Useful ideas should be translated into BlueprintStudio-native docs, runbooks,
routes, and frontend views.

## Autonomous Work Context

The previous autonomous loop selected the first safe `todo` task, replenished
the task pool when low, limited each PR to one task ID, and avoided high-risk or
destructive work without human review.

This behavior is now represented in `.planning/STATE.md` and
`.planning/todos/AGENT-TASKS.md`.
