---
project: BlueprintStudio
document: architecture
last_mapped_commit: b7a5fca729d82fd6d25707deb6edc1356f008624
mapped_at: 2026-06-07
scope: full repo
---

# BlueprintStudio Architecture

## System Shape

- BlueprintStudio is a two-app monorepo: `backend/` is a FastAPI + LangGraph
  service and `frontend/` is a Next.js App Router shell.
- The current runtime path is browser UI -> REST/SSE API -> service layer ->
  SQLite, MemoryPalace, deterministic analyzers, or report generation.
- The repo also keeps reference and planning material in `.planning/`,
  `docs/`, `dc_compliance_checker/`, and `dataSamples/`.

## Backend Layers

- `backend/app/main.py` is the composition root. It builds `AppState`, wires
  the production lifespan, and registers the live routers.
- The registered backend routes are `backend/app/api/health.py`,
  `backend/app/api/chat.py`, `backend/app/api/threads.py`,
  `backend/app/api/ingest.py`, `backend/app/api/reports.py`, and
  `backend/app/api/finance.py`.
- `backend/app/api/fusion.py` exists as a router module, but `main.py` does not
  currently include it in the live app.
- `backend/app/agent/graph.py` defines the LangGraph loop with one agent node
  and one tool node. The only first-class tools today are the KB recall/remember
  tools built from `backend/app/agent/tools.py`.
- `backend/app/kb/base.py` defines the `KnowledgeBase` protocol. The
  production-like adapter is `backend/app/kb/memorypalace.py`; tests and
  offline runs use `backend/app/kb/fake.py`.
- `backend/app/services/document_registry.py`,
  `backend/app/services/report_sessions.py`, and
  `backend/app/services/graph_artifacts.py` are the SQLite-backed durability
  layers.
- `backend/app/schemas.py` is the shared wire contract. Route payloads,
  frontend types, report artifacts, graph payloads, and validation results all
  mirror these models.

## Backend Data Flow

- Upload flow: `backend/app/api/ingest.py` validates file size/name/hash,
  deduplicates through `DocumentRegistry`, classifies by extension via
  `backend/app/services/engineering_files.py`, then routes to parsers or the
  optional converter layer.
- Parsing flow: `backend/app/services/parsers.py` dispatches to PDF, DOCX,
  XLSX, Markdown, and text extractors; `backend/app/services/document_analysis.py`
  can enrich visual elements when `document_analysis_enabled` is on.
- Memory flow: chunked document elements are stored through the KB interface;
  the default test path stays hermetic with `FakeKB`, while
  `MemoryPalaceKB` bridges the external library with `asyncio.to_thread`.
- Chat flow: `backend/app/api/chat.py` emits SSE `ChatChunk` frames, injects
  a stable system prompt, and checkpoints thread state in SQLite so
  `backend/app/api/threads.py` can replay history.
- Report flow: `backend/app/api/reports.py` launches and streams a session
  through `backend/app/services/report_pipeline.py`, which runs inventory ->
  section planning -> retrieval -> drafting -> validation -> PDF export.
- Deterministic domain analysis lives in
  `backend/app/services/compliance_runner.py`,
  `backend/app/services/electrical_loads.py`,
  `backend/app/services/hvac_analysis.py`, and
  `backend/app/services/property_valuation.py`.

## Abstractions

- `AppState` in `backend/app/main.py` is the container for runtime services,
  settings, and compiled graph state.
- `KnowledgeBase` is the main swap point for MemoryPalace vs. fake memory.
- `ReportSessionStore`, `ReportPipelineRegistry`, and `DocumentRegistry`
  isolate durable state from API routes.
- `EngineeringGraph`, `ReportProjection`, `ConversionResult`, and the report
  schema models are the main typed boundaries between parser, service, and UI
  code.
- `backend/app/services/hybrid_retriever.py` and
  `backend/app/services/graph_artifacts.py` already provide graph/text
  retrieval and graph artifact storage, but they are not yet mounted as a
  first-class API surface in `main.py`.

## Frontend Layers

- `frontend/src/app/page.tsx` is the main client entry point. It shows
  `OnboardingWizard` until the store reaches `ready`, then mounts
  `frontend/src/components/shell/AppShell.tsx`.
- `frontend/src/lib/store.ts` is the frontend orchestrator. It owns UI state,
  localStorage persistence, report-session side effects, graph state, and
  mock/demo interactions.
- `frontend/src/lib/api.ts` is the only direct network layer. It handles
  health checks, readiness, threads, ingestion, fusion, report sessions, SSE
  chat, and SSE report streaming.
- `frontend/src/types/index.ts` mirrors the backend schemas so the browser and
  backend stay aligned on graph, report, and response contracts.
- The main visible shell is split into `frontend/src/components/shell/*`,
  `frontend/src/components/chat/*`, `frontend/src/components/graph/*`,
  `frontend/src/components/files/*`, `frontend/src/components/report/*`, and
  the overlay panels in `profile`, `settings`, `dock`, and `preview`.
- `frontend/src/components/ChatShell.tsx` is still present as an older
  standalone chat surface, but `frontend/src/app/page.tsx` does not mount it.

## Frontend Data Flow

- The app shell is state-driven: `frontend/src/lib/store.ts` hydrates from
  storage, fetches backend inspection data, and updates the graph/report views.
- `frontend/src/components/graph/GraphView.tsx` renders and mutates the mock
  graph state with drag, pan, and zoom interactions.
- `frontend/src/components/chat/ChatPanel.tsx` is the report/chat control
  surface in the current shell. It launches report sessions, renders report
  cards, and hosts the gate-answer form.
- `frontend/src/components/report/ReportView.tsx` consumes the report-session
  inspection payload and shows stages, artifacts, validation findings, and PDF
  export links.
- `frontend/src/components/files/FileTree.tsx`,
  `frontend/src/components/preview/FilePreview.tsx`, and
  `frontend/src/components/dock/BottomDock.tsx` keep the graph/file snapshot
  context visible while the user works.

## Styling And Motion

- `frontend/tailwind.config.ts` defines the brand palette, fonts, and motion
  tokens.
- `frontend/src/app/globals.css` adds the background gradients, graph grid,
  and scrollbar styling used by the shell.
- Framer Motion variants in `frontend/src/lib/animations.ts` and the shell
  components provide the main animated transitions.

## Current Wiring Notes

- `backend/app/api/fusion.py` is implemented but not registered by
  `backend/app/main.py`, so the module is present before the route is fully
  surfaced.
- `frontend/src/components/ConnectionBadge.tsx` still polls `fetchHealth()` and
  `fetchReadiness()`, but it is only used by the older `ChatShell` surface.
- The live app is therefore a mixed state: the newer IDE-style shell is the
  active entry point, while the older chat shell and some supporting modules
  remain in the tree as reusable or transitional code.
