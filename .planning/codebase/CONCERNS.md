---
title: CONCERNS
last_mapped_commit: b7a5fca729d82fd6d25707deb6edc1356f008624
mapped_on: 2026-06-07
scope: full repo
---

# Concerns

Current-state risks and debt discovered from code inspection. The biggest structural hotspots are `backend/app/services/report_pipeline.py` (1,413 lines), `backend/app/services/report_sessions.py` (1,244 lines), `frontend/src/lib/store.ts` (781 lines), and `backend/app/services/engineering_converters.py` (857 lines).

## 1. The primary shell is still mock-driven, while the live chat path is effectively dead
- `frontend/src/app/page.tsx:7` mounts `AppShell`, not `ChatShell`.
- `frontend/src/components/chat/ChatPanel.tsx:92` sends every message through `sendMockChat`, which appends a canned assistant reply from `frontend/src/lib/mock.ts:1`.
- `frontend/src/components/ChatShell.tsx:46` contains the live `streamChat` path, but nothing imports it, so it is dead code in the current app.
- `frontend/src/lib/mock.ts:1` and `frontend/src/lib/mock.ts:93` still seed the shell with `bob-*` placeholder files, graph nodes, and replies.

Impact: the default UX can look interactive while never touching the backend chat route, and the repository now carries two parallel chat implementations.

## 2. Frontend components still bind to mock-layer types instead of the shared graph contract
- Shared graph types already exist in `frontend/src/types/index.ts:256`.
- Core views still import `ProjectFile`, `GraphNode`, `GraphEdge`, `Snapshot`, `SnapshotReason`, `Guideline`, and `TemplateSection` from `frontend/src/lib/mock.ts:7`, `frontend/src/components/graph/GraphView.tsx:6`, `frontend/src/components/files/FileTree.tsx:6`, `frontend/src/components/dock/BottomDock.tsx:5`, and `frontend/src/components/settings/SettingsModal.tsx:7`.

Impact: the UI is not actually wired to the canonical graph contract, so backend schema changes and mock schema changes can drift independently.

## 3. `New bob-project` does not fully reset persisted state
- `frontend/src/components/shell/TopBar.tsx:32` calls `useChatStore.getState().reset()`.
- `frontend/src/lib/store.ts:474` resets in-memory state only.
- The same store persists and rehydrates `THREAD_STORAGE_KEY` and `REPORT_STORAGE_KEY` at `frontend/src/lib/store.ts:478`, `frontend/src/lib/store.ts:486`, `frontend/src/lib/store.ts:508`, and `frontend/src/lib/store.ts:588`.

Impact: a "new project" can still resurrect the previous thread or report after refresh, which is a real user-facing bug and makes the reset action misleading.

## 4. The backend is using synchronous SQLite and filesystem work inside async request handlers
- `backend/app/api/ingest.py:55` writes uploads and drives the registry pipeline inline.
- `backend/app/api/reports.py:63` and `backend/app/api/threads.py:31` read from the SQLite-backed session and checkpoint stores directly in request handlers.
- `backend/app/services/document_registry.py:73`, `backend/app/services/graph_artifacts.py:1`, and `backend/app/services/report_sessions.py:104` all use direct `sqlite3` connections and RLocks instead of an async driver or a threadpool boundary.

Impact: request latency will scale poorly under load, and multi-worker deployment will be fragile because the app relies on several local SQLite files as first-class state stores.

## 5. Error handling is too broad in the orchestration layer
- `backend/app/services/report_pipeline.py:188`, `backend/app/services/report_pipeline.py:272`, `backend/app/services/report_pipeline.py:346`, `backend/app/services/report_pipeline.py:547`, and `backend/app/services/report_pipeline.py:643` catch `Exception` broadly and reclassify every failure into a report-session failure path.
- `backend/app/api/chat.py:72` and `backend/app/api/chat.py:105` also catch every exception and surface only the exception string.

Impact: real programming errors get flattened into generic failure states, which makes diagnosis harder and can leak raw exception text to clients instead of failing fast with structured errors.

## 6. Graph and thread rendering paths are not scaled for larger datasets
- `frontend/src/components/graph/GraphView.tsx:87` updates the store on every mousemove, with no throttling or batching.
- `frontend/src/components/graph/GraphView.tsx:216` resolves every edge with `nodes.find(...)`, which makes render cost grow with the product of edges and nodes.
- `backend/app/api/threads.py:31` walks every checkpoint to build `/api/threads`, and `backend/app/api/reports.py:229` polls the report event queue every 250ms when idle.

Impact: the current implementation is fine for demo-sized data, but it will feel sluggish or wasteful as histories and graphs grow.

## 7. Demo routes are brittle outside the repo root, and the overlay path buffers entire uploads in memory
- `backend/app/api/ingest.py:149`, `backend/app/api/ingest.py:156`, and `backend/app/api/ingest.py:163` open fixture JSON with relative `tests/fixtures/...` paths, so the demo endpoints depend on the process working directory.
- `backend/app/api/ingest.py:176` reads the full overlay image into memory before validation and rendering.

Impact: the demo endpoints are easy to break when the app is launched from a different cwd, and the overlay route has a clear memory and CPU DoS surface for large images.

## 8. Security hardening is minimal on the default server settings
- `backend/app/main.py:164` allows every origin, method, and header via CORS.
- `backend/pyproject.toml:14`, `backend/pyproject.toml:18`, `backend/pyproject.toml:29`, and `backend/pyproject.toml:31` bring OpenAI, Ollama, and Postgres clients into the base backend install, even though the repo also supports fake and local paths.

Impact: acceptable for a local-first demo, but this is not production-hardened by default and the default install footprint is larger than it needs to be.
