---
project: BlueprintStudio
document: structure
last_mapped_commit: b7a5fca729d82fd6d25707deb6edc1356f008624
mapped_at: 2026-06-07
scope: full repo
---

# BlueprintStudio Structure

## Root Layout

- `README.md` is the main integration guide for the current stack.
- `AGENTS.md` is the repository contract; `.planning/` is the primary planning
  surface after the migration.
- `Makefile` and `docker-compose.yml` are the primary local orchestration
  entry points.
- `deep-research-report.md` remains at the root as a research reference.
- `patch_hvac.py` is a root-level helper script and does not sit in a package
  directory.

## Planning And Docs

- `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`,
  `.planning/ROADMAP.md`, and `.planning/STATE.md` are the active GSD planning
  documents.
- `.planning/todos/AGENT-TASKS.md` is the active GSD task queue.
- `docs/` still contains older design and decision notes such as
  `graph_artifact_persistence.md`, `graph_database_decision_record.md`,
  `plumbing_graph_taxonomy.md`, and `standards_scraping_rules.md`.

## Backend Tree

- `backend/app/main.py` is the bootstrap file; `backend/app/config.py`,
  `backend/app/schemas.py`, `backend/app/agent/`, `backend/app/api/`,
  `backend/app/kb/`, and `backend/app/services/` are the main subpackages.
- `backend/app/api/` groups route modules by capability: `chat.py`,
  `finance.py`, `fusion.py`, `health.py`, `ingest.py`, `reports.py`, and
  `threads.py`.
- `backend/app/agent/` contains `graph.py`, `llm.py`, `checkpointer.py`, and
  `tools.py`.
- `backend/app/kb/` contains `base.py`, `fake.py`, and `memorypalace.py`.
- `backend/app/services/` is the largest package. It includes ingestion,
  parser, registry, graph, retrieval, compliance, report, valuation, and
  engineering-analysis helpers such as `ingestion.py`, `document_registry.py`,
  `graph_validator.py`, `graph_artifacts.py`, `report_pipeline.py`,
  `report_sessions.py`, `property_valuation.py`, `electrical_loads.py`, and
  `hvac_analysis.py`.
- `backend/tests/` is grouped into `unit/`, `integration/`, and `e2e/`, with
  fixtures under `backend/tests/fixtures/graphs/` and
  `backend/tests/fixtures/flowdraft/`.
- `backend/backend/data/` currently holds local SQLite smoke artifacts such as
  `smoke-checkpoints.sqlite`, `smoke-registry.sqlite`, and
  `smoke-report-sessions.sqlite`.
- `backend/pyproject.toml`, `backend/uv.lock`, `backend/Dockerfile`, and
  `backend/.env.example` are the backend package/config files.

## Frontend Tree

- `frontend/src/app/` contains the App Router entry points: `layout.tsx`,
  `page.tsx`, `globals.css`, and `api/health/route.ts`.
- `frontend/src/components/` is split into two styles of code: older
  top-level chat primitives (`ChatShell.tsx`, `Composer.tsx`,
  `Message.tsx`, `MessageList.tsx`, `ThreadList.tsx`, `TypingIndicator.tsx`,
  `ConnectionBadge.tsx`) and the current feature folders under `chat/`,
  `dock/`, `files/`, `graph/`, `onboarding/`, `preview/`, `profile/`,
  `report/`, `settings/`, and `shell/`.
- `frontend/src/components/shell/AppShell.tsx` is the current visual root for
  the IDE-style interface.
- `frontend/src/lib/` contains the shared client logic in `api.ts`, state in
  `store.ts`, demo/mocked data in `mock.ts`, and motion tokens in
  `animations.ts`.
- `frontend/src/types/index.ts` mirrors the backend payloads and graph shapes.
- `frontend/tests/` is split into `unit/`, `unit/flows/`, `e2e/`, and
  fixtures under `frontend/tests/fixtures/graphs/` and
  `frontend/tests/fixtures/flowdraft/`.
- `frontend/package.json`, `frontend/package-lock.json`,
  `frontend/next.config.mjs`, `frontend/tailwind.config.ts`,
  `frontend/vitest.config.ts`, and `frontend/playwright.config.ts` define the
  frontend build and test setup.
- `frontend/.next/` and `frontend/node_modules/` are present locally as build
  and dependency output directories.

## Reference And Sample Trees

- `dc_compliance_checker/` is a separate prototype reference tree with
  `database/`, `engine/`, `parsers/`, `data/`, and `main.py`.
- `dataSamples/` contains sample images and schema material, including
  `dataSamples/raw_diagrams/`, `dataSamples/raw_floorplans/`, and
  `dataSamples/schema.json`.
- `scripts/` contains operational helpers such as `smoke.sh` and
  `smoke_cad_converter.py`.

## Naming Conventions

- Backend Python modules are snake_case and package by concern. Route modules
  use singular capability names such as `chat.py`, `reports.py`, and
  `threads.py`.
- Frontend components use PascalCase filenames, while feature folders are
  lower-case nouns such as `chat`, `graph`, `report`, `shell`, and `settings`.
- Python tests use `test_*.py`; frontend tests use `*.test.tsx` or
  `*.spec.ts`. Numbered flow tests live under
  `frontend/tests/unit/flows/NN-*.test.tsx`.
- Fixture directories are domain-based: `graphs`, `flowdraft`, and the sample
  data directories under `dataSamples/`.
- App Router files follow Next conventions: `layout.tsx`, `page.tsx`, and
  `route.ts`.
- Generated or local-only directories are kept separate from source code, but
  they are still visible in the current working tree and should be treated as
  disposable runtime state.
