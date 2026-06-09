# S03: Parser And Conversion Pipeline — Research

**Date:** 2026-06-09

## Summary

The current ingestion pipeline is synchronous and blocking, which prevents the UI from providing real-time feedback during long-running CAD-to-graph conversions. This slice will refactor the ingestion process into a background task architecture and introduce an SSE-based status stream.

We will leverage the existing `DocumentRegistry` (SQLite-backed) to track lifecycle states and the `EventSourceResponse` pattern already established in the report pipeline. The `ingest` endpoint will transition to returning immediate document IDs, while the actual conversion and parsing happen in the background, emitting progress events for each stage (Conversion, Parsing, Indexing).

## Recommendation

Implement an `IngestEventBus` within the backend app state to manage per-client or global ingestion event queues. Refactor the `ingest` API endpoint to use `asyncio.create_task` (or `BackgroundTasks` if appropriate for simple persistence) and return immediately. Update the ingestion service to yield or emit events during critical steps. On the frontend, introduce a persistent SSE listener for ingestion updates that updates the global store, allowing `FileTree` and `FilePreview` to render live "Processing" or "Ready (Warnings)" states.

## Implementation Landscape

### Key Files

- `backend/app/api/ingest.py` — Refactor `ingest` endpoint to launch background tasks and add a new `/api/ingest/stream` SSE endpoint.
- `backend/app/services/ingestion.py` — Update `ingest_registered_files` to accept an event callback or emit to a registry to surface progress.
- `backend/app/schemas.py` — Add `ingest_progress` to `ChunkType` and define `IngestEvent` payload.
- `backend/app/services/document_registry.py` — Ensure `DocumentStatus` adequately represents the "Ready (Warnings)" state (e.g., via a metadata field for warnings).
- `frontend/src/lib/api.ts` — Implement `streamIngest` to consume the new SSE endpoint.
- `frontend/src/lib/store.ts` — Add state for tracking ingestion progress per document.

### Build Order

1. **Schema and Bus**: Add `ingest_progress` to `ChunkType` and implement a simple `IngestEventBus` in `backend/app/services/ingestion.py`.
2. **Background Refactor**: Modify `backend/app/api/ingest.py` to trigger ingestion in a task and return `IngestResponse` with pending status.
3. **SSE Endpoint**: Add the streaming endpoint to `backend/app/api/ingest.py`.
4. **Instrumentation**: Add event emission to `ingest_registered_files` and `_ingest_converted_drawing_path`.
5. **Frontend Integration**: Hook up the SSE stream in the frontend store and update `FileTree` components.

### Verification Approach

- **Backend Logic**: `pytest` for the `IngestEventBus` and background task lifecycle.
- **Integration**: Use `curl --no-buffer` to hit the SSE stream while performing an upload.
- **E2E**: Playwright test confirming the "Processing" spinner appears and disappears in the `FileTree` during a mocked slow upload.

## Constraints

- **Single Process**: Since we are using local SQLite and in-memory event queues, this design assumes a single backend process (standard for the current local-dev/Ollama setup).
- **Graceful Partial Failure**: The pipeline must not crash if one file fails; it must mark that document as `failed` and continue with others.

## Common Pitfalls

- **Queue Bloat** — Ensure event queues are cleaned up if a client disconnects or after a timeout.
- **Zombie Tasks** — Use `asyncio.create_task` carefully and ensure they are tracked or awaited at shutdown to avoid data corruption in the registry.

## Open Risks

- **SSE Connection Stability** — Browser-side SSE can be flaky with long-running tasks if timeouts aren't handled; we should include heartbeat events.
- **Duplicate Processing** — If a user re-uploads while a background task is still running, the registry needs to handle locking or immediate "already processing" returns.

## Skills Discovered

| Technology | Skill | Status |
|------------|-------|--------|
| FastAPI | `api-design` | available |
| SSE | `observability` | available |
| Planning | `decompose-into-slices` | available |
