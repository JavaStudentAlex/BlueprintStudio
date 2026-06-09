---
estimated_steps: 18
estimated_files: 3
skills_used: []
---

# T03: Add background ingest API, SSE stream, and reparse override

---
skills_used:
  - api-design
  - tdd
  - verify-before-complete
---
Why: Uploads must stop blocking the UI, and users need a post-upload manual route override when AUTO drawing detection is wrong or ambiguous.

Do:
- Add ingest event bus and background task tracking to FastAPI app state in app composition.
- Refactor POST /ingest so it validates and stores uploads, registers document rows, emits queued/processing events, starts background ingestion work with asyncio task management, and returns promptly with document identifiers and pending or processing status.
- Add GET /ingest/stream using the existing EventSourceResponse pattern from reports, including heartbeats and subscriber cleanup on disconnect.
- Add a document reparse endpoint that validates document_id and drawing routing, rejects missing or unsafe records, updates the routing override, and starts a reparse against the stored file path.
- Ensure background task exceptions are caught, logged through registry error state, and emitted as failed events rather than becoming zombie tasks.

Done when:
- API tests prove immediate upload response, SSE event formatting, heartbeat behavior, disconnect cleanup, task failure reporting, and manual override reparse.
- Q3: Reparse validates document IDs and never accepts client-provided filesystem paths.
- Q5: Task exceptions and client disconnects have deterministic outcomes.
- Q7: Negative tests cover bad routing, unknown document_id, missing stored file, and malformed uploads.

## Inputs

- `backend/app/main.py`
- `backend/app/api/ingest.py`
- `backend/app/api/reports.py`
- `backend/app/services/ingestion.py`
- `backend/app/services/ingest_events.py`
- `backend/app/services/document_registry.py`

## Expected Output

- `backend/app/main.py`
- `backend/app/api/ingest.py`
- `backend/tests/unit/test_ingest_api.py`

## Verification

rtk uv --directory backend run --extra dev pytest tests/unit/test_ingest_api.py tests/unit/test_ingestion.py

## Observability Impact

Exposes ingestion progress as a live SSE stream and records background task failures in both registry state and emitted events.
