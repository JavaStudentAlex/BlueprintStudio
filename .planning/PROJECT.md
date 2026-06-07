# BlueprintStudio

## What This Is

BlueprintStudio is a construction-analysis application that pairs an IDE-style
Next.js shell with a LangGraph-powered FastAPI backend for uploaded
construction documents, graph-backed engineering understanding, chat, reports,
and deterministic analysis.

The product direction is to evolve beyond architectural-document chat into a
multi-discipline building-engineering agent for drawings, standards, compliance,
real-estate data, cost reasoning, 2D editing, and evidence-backed reports.

## Core Value

BlueprintStudio must convert construction and engineering document context into
traceable, testable engineering evidence before an agent explains, reports, or
proposes changes.

## Requirements

### Validated

- ✓ Repository agent guidance and GSD planning documents exist.
- ✓ Legacy task-manifest planning was migrated into the GSD task queue.
- ✓ Legacy Jules planning files, validator script, and source snapshots were
  removed after migration.
- ✓ Jules next-task and automerge workflows are retained as GSD-compatible
  automation bridges that read `.planning/`.
- ✓ BlueprintStudio engineering graph schema v1 exists.
- ✓ FlowDraft graph fixtures are imported as deterministic test data.
- ✓ Backend graph validation service exists.
- ✓ Graph artifact persistence design and graph database decision records exist.
- ✓ FlowDraft-style fusion service exists in the backend.
- ✓ Parser adapter contract exists for drawing conversion.
- ✓ FlowDraft golden-demo fixtures and demo API surfaces exist.
- ✓ Graph-derived property valuation demo service exists.
- ✓ `dc_compliance_checker` rule model concepts are ported.
- ✓ Deterministic compliance validation runner exists.
- ✓ Standards source catalog exists.
- ✓ Reviewed standards can be indexed into vector RAG.
- ✓ Hybrid graph and text retriever interface exists.
- ✓ Deterministic electrical load analysis exists.
- ✓ PUE and BEC service exists.
- ✓ Plumbing graph taxonomy exists.

### Active

- [ ] Ship the offline FlowDraft-inspired demo workflow in the existing Next.js
      shell.
- [ ] Add deterministic e2e smoke coverage for the offline demo path.
- [ ] Add governance docs for CrashPine upstream tracking, capability honesty,
      and external-source access.
- [ ] Add deterministic demo Docker/juror runbook support after the offline demo
      path is stable.
- [ ] Add graph inspection, compliance evidence, graph-to-3D twin, and
      capability roadmap frontend views.
- [ ] Plan YOLO and IFC ingestion without introducing live external calls into
      default tests.
- [ ] Complete GOST-oriented standards ingestion planning.
- [ ] Add ventilation taxonomy and broader MEP graph primitives.
- [ ] Add real-estate, property price, cost, ROI, and scenario calculation
      services with provenance.
- [ ] Build architecture and electrical 2D editor designs and MVPs.
- [ ] Add agent warning-to-evidence-to-fix workflow with human approval before
      graph write-back.
- [ ] Extend report generation with compliance evidence.

### Out of Scope

- LLM-only compliance decisions - deterministic rules and source evidence must
  decide pass/fail.
- Silent engineering graph write-back - physical or compliance-impacting
  changes require visible evidence and human approval.
- Live external LLMs, standards sites, government sites, or paid APIs in default
  tests - fixtures and fakes are required.
- Committing customer drawings, uploaded documents, generated reports, local
  SQLite state, large model weights, or generated overlay assets without an
  explicit human request.
- Merging external tree-replacement branches into this repository - external
  projects are implementation references, not replacement trees.
- Treating hackathon-specific FlowDraft or CrashPine assumptions as global
  product defaults.
- Workflow, secret, deployment, auto-merge, or publishing changes as normal
  autonomous work.

## Context

BlueprintStudio currently contains:

- A Python 3.12 FastAPI backend with LangGraph, LangChain, pydantic-settings,
  SSE, SQLite registries/checkpoints, MemoryPalace integration, and fake
  adapters for tests.
- A Next.js 14 App Router frontend using React 18, TypeScript, Tailwind,
  Zustand, Framer Motion, and domain components for shell, chat, reports, files,
  graph, preview, onboarding, profile, and settings.
- Pytest, Vitest/RTL/MSW, Playwright, Ruff, mypy, TypeScript, Next lint, and
  GitHub Actions gates.
- Existing planning sources migrated into GSD-native project, requirements,
  roadmap, state, intel, seed, and task documents.
- A GSD-native task queue at `.planning/todos/AGENT-TASKS.md`.

The target architecture is a hybrid analysis stack:

```text
uploaded sources
  -> controlled parsers and extractors
  -> authoritative engineering graph
  -> deterministic validation and rule engines
  -> vector/text retrieval for direct clause lookup
  -> graph retrieval for topology and multi-hop reasoning
  -> LLM explanation and candidate-fix generation
  -> human approval for physical or compliance-impacting changes
```

## Constraints

- **Source of truth**: MemoryPalace remains useful for agent memory and document
  recall, but authoritative engineering state belongs in explicit graph models
  with provenance.
- **Sensitive data**: Uploaded documents, generated reports, SQLite state,
  runtime data, and secrets stay out of git.
- **Tests**: Default tests must not require real LLMs, Ollama, Postgres,
  third-party APIs, standards sites, or model weights.
- **API contracts**: Backend schemas, frontend types, SSE events, thread IDs,
  checkpointer behavior, and report download path validation must remain stable
  unless updated together with tests.
- **External references**: FlowDraft and CrashPine must be rechecked before
  implementation work that depends on their latest state.
- **Task scope**: Autonomous work is one task ID per PR with bounded paths and
  exact validation evidence.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use GSD `.planning/` as the primary planning surface | The user requested migration from Jules-style planning files into gsd-core documentation. | Good |
| Replace legacy Jules planning surfaces with GSD-compatible automation bridges | The GSD files now carry active planning state, while Jules next-task and automerge functionality must remain available. | Good |
| Keep tasks in `.planning/todos/AGENT-TASKS.md` | The GSD task queue replaces the removed JSON task manifest and retains active work selection. | Good |
| Use an explicit engineering graph as authoritative state | Compliance, topology, cost, and editing require typed provenance and deterministic validation. | Good |
| Keep MemoryPalace optional at test time | Tests need deterministic fakes and should not depend on production-like local services. | Good |
| Absorb FlowDraft contracts, not its standalone app | BlueprintStudio already has a backend/frontend architecture that should remain the product base. | Good |
| Treat CrashPine tree replacement as an external reference only | The upstream replacement deletes this repo's backend, frontend, tests, and planning surfaces. | Good |
| Gate compliance through deterministic rules and human review | LLMs can explain and draft, but must not be the compliance source of truth. | Good |

## Evolution

After each GSD phase:

1. Move validated requirements from Active to Validated.
2. Move invalidated or intentionally deferred items to Out of Scope with
   rationale.
3. Update `ROADMAP.md` progress and `STATE.md` current focus.
4. Add new decisions to this file when they constrain future work.
5. Keep `.planning/todos/AGENT-TASKS.md` aligned with any task-queue changes.

---
*Last updated: 2026-06-07 after migration cleanup from legacy planning files to GSD.*
