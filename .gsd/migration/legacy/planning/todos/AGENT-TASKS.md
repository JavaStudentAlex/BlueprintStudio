# GSD Task Queue: BlueprintStudio

**Status:** Active  
**Updated:** 2026-06-07 after legacy planning cleanup  
**Source of truth:** This file, with phase context in `.planning/ROADMAP.md`
and requirements in `.planning/REQUIREMENTS.md`.

Legacy task-manifest files were removed after migration. Do not recreate the
old JSON queue. Jules automation, when enabled, must read this GSD task queue
and follow the repository GSD workflow.

## Selection Policy

1. Select the first `todo` task that is not high or critical risk.
2. Keep each change to one task ID.
3. Stay inside the listed scope unless the phase plan expands it explicitly.
4. Run the lightest deterministic verification that proves the change.
5. Update this file, `.planning/ROADMAP.md`, and `.planning/STATE.md` when task
   state changes.

## Current Queue

| ID | Phase | Status | Risk | Title | Scope | Acceptance |
|----|-------|--------|------|-------|-------|------------|
| flowdraft-golden-demo-frontend | 8 | done | medium | Add frontend golden demo workflow | `frontend/src/**`, `frontend/tests/**`, `.planning/**` | `Load demo` works without upload/API keys/network; rooms, valuation, and compliance views render deterministic fixture data; frontend tests cover the path. |
| flowdraft-demo-e2e-smoke | 8 | done | medium | Add offline golden demo smoke test | `backend/tests/e2e/**`, `frontend/tests/e2e/**`, `scripts/**`, `.planning/**` | Smoke starts from committed fixtures only and proves API/UI demo path without external services. |
| crashpine-upstream-recheck-log | 8 | todo | low | Add CrashPine upstream recheck log | `docs/**`, `.planning/**` | Latest reviewed CrashPine branch/commit SHAs are recorded with merge safety notes. |
| demo-capability-honesty-disclosure | 8 | todo | low | Add demo capability honesty disclosure | `docs/**`, `.planning/**` | Disclosure separates live, beta, mocked, hardcoded, external-service, and roadmap behavior. |
| demo-docker-jury-packaging | 8 | todo | medium | Add deterministic demo Docker runbook | `docs/**`, `scripts/**`, `docker-compose.yml`, `.planning/**` | Runbook documents offline demo startup, health checks, fallback build, and no-secret assumptions. |
| graph-3d-twin-frontend | 6 | todo | medium | Add graph-to-3D twin frontend view | `frontend/src/**`, `frontend/tests/**`, `.planning/**` | View consumes canonical graph fixtures and renders spaces, fixtures, MEP nodes/edges, labels, and fallback state. |
| capability-roadmap-frontend | 6 | todo | low | Add capability roadmap view | `frontend/src/**`, `frontend/tests/**`, `.planning/**` | UI labels live, beta, mocked, and roadmap capabilities without overstating implementation status. |
| yolo-conversion-spike | 2 | todo | high | Plan YOLO-based drawing conversion integration | `docs/**`, `.planning/**` | Spike plan defines optional-engine boundaries, fixtures, model-weight policy, and no-default-network tests. |
| gost-ingestion-plan | 3 | todo | high | Plan GOST-oriented standards ingestion | `docs/**`, `.planning/**` | Plan covers source catalog, clause extraction, human review, deterministic rule normalization, and approval gates. |
| ventilation-graph-taxonomy | 5 | todo | low | Define ventilation graph taxonomy | `docs/**`, `backend/app/**`, `backend/tests/**`, `.planning/**` | Taxonomy defines fans, AHUs, ducts, dampers, diffusers, zones, airflow edges, provenance, and validation cases. |
| real-estate-dataset-catalog | 4 | todo | medium | Create real-estate dataset catalog | `backend/app/**`, `backend/tests/**`, `docs/**`, `.planning/**` | Catalog records source, license, geography, update cadence, fields, and suitability for RAG/cost use. |
| property-price-rag-fixture | 4 | todo | medium | Add property price RAG fixture workflow | `backend/app/**`, `backend/tests/**`, `docs/**`, `.planning/**` | Curated fixture data indexes deterministically with source metadata and test coverage. |
| approximate-cost-estimation-service | 7 | todo | medium | Implement approximate cost estimation service | `backend/app/**`, `backend/tests/**`, `docs/**`, `.planning/**` | Service computes deterministic cost estimates before LLM explanation and exposes assumptions/provenance. |
| roi-scenario-service | 7 | todo | medium | Add ROI and scenario calculation service | `backend/app/**`, `backend/tests/**`, `docs/**`, `.planning/**` | Service computes scenario ROI from explicit inputs and records assumptions/provenance. |
| graph-inspection-frontend | 6 | todo | medium | Add frontend graph inspection view | `frontend/src/**`, `frontend/tests/**`, `.planning/**` | Users can inspect graph objects, relationships, provenance, confidence, and validation warnings. |
| compliance-report-ui | 6 | todo | medium | Add compliance results UI | `frontend/src/**`, `frontend/tests/**`, `.planning/**` | UI renders deterministic violations with rule, object, actual, expected, source, confidence, and candidate fixes. |
| architecture-2d-editor-design | 6 | todo | medium | Design architecture 2D editor state model | `docs/**`, `.planning/**`, `frontend/src/**` | Design covers walls, rooms, openings, labels, dimensions, areas, layers, validation, and graph write-back. |
| architecture-2d-editor-mvp | 6 | todo | medium | Build architecture 2D editor MVP | `frontend/src/**`, `frontend/tests/**`, `.planning/**` | MVP supports graph-backed architecture edits and deterministic tests for core interactions. |
| electrical-2d-editor-design | 6 | todo | medium | Design electrical 2D editor state model | `docs/**`, `.planning/**`, `frontend/src/**` | Design covers panels, circuits, switches, outlets, fixtures, cable paths, schedules, and validation. |
| electrical-2d-editor-mvp | 6 | todo | medium | Build electrical 2D editor MVP | `frontend/src/**`, `frontend/tests/**`, `.planning/**` | MVP supports graph-backed electrical edits and deterministic tests for core interactions. |
| agent-warning-fix-workflow | 5 | todo | medium | Add agent warning and candidate fix workflow | `backend/app/**`, `backend/tests/**`, `docs/**`, `.planning/**` | Agent emits warning, evidence, violated condition, confidence, provenance, ranked fixes, and human-approval gate. |
| report-pipeline-compliance-extension | 7 | todo | medium | Extend report pipeline with compliance evidence | `backend/app/**`, `backend/tests/**`, `frontend/src/**`, `frontend/tests/**`, `.planning/**` | Reports include compliance evidence while preserving report-session validation gates and export safety. |
| agent-task-bridge-cli | 0 | done | low | Add GSD task helper CLI | `scripts/**`, `.planning/**`, `docs/**` | CLI can validate the GSD task queue, show queue status, print next safe task, and render a focused implementation prompt. |
| graph-ontology-mapping-doc | 1 | todo | low | Map graph concepts to BOT, IFC, Brick, and SHACL | `docs/**`, `.planning/**` | Mapping documents concept alignment, gaps, and non-goals for interoperability. |
| ifc-ingestion-spike-plan | 2 | todo | high | Plan IFC ingestion spike | `docs/**`, `.planning/**` | Spike defines IFC scope, fixtures, graph output, risks, and implementation boundaries. |
| external-source-access-policy | 3 | todo | high | Define external source access policy | `docs/**`, `.planning/**`, `.github/instructions/**` | Policy defines approval gates for standards sites, government sources, scraping, paid APIs, and live external calls. |

## Completed Work Summary

Completed work is summarized in `.planning/PROJECT.md` under `Validated` and in
`.planning/ROADMAP.md` phase details. Do not recreate old manifest records for
completed tasks.

- `agent-task-bridge-cli` completed on 2026-06-07 with
  `scripts/gsd_task_bridge.py` and Jules workflow integration.
