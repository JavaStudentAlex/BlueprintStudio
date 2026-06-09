---
estimated_steps: 18
estimated_files: 5
skills_used: []
---

# T01: Define ingest event and warning contracts

---
skills_used:
  - api-design
  - design-an-interface
  - verify-before-complete
---
Why: S03 needs a single backend contract for progress, warnings, partial success, and downstream frontend parsing before background work or UI wiring can be reliable.

Do:
- Add typed ingestion event payloads to backend schemas, including stage, status, document_id, safe filename, optional routing, progress percentage, warnings, and error summary fields.
- Extend the shared chunk/event type surface with an ingestion progress type while preserving existing chat and report stream compatibility.
- Add a small ingest event bus module with bounded subscriber queues, heartbeat-friendly event serialization, disconnect cleanup, and tests for fan-out and queue cleanup.
- Extend DocumentRegistry warning metadata in a backward-compatible SQLite migration so parser warnings can be persisted independently of terminal failure errors.
- Keep the event payload data-minimized: no document body, raw extracted content, absolute local paths, or secrets.

Done when:
- Unit tests prove event fan-out, late subscriber behavior, cleanup, warning persistence, and existing registry rows remain readable after migration.
- Q3: Event payloads are explicitly path/content safe.
- Q4: PARSE-04 has a typed graph and document status contract to build on.
- Q6: Queue bounds and cleanup behavior are covered by tests.

## Inputs

- `backend/app/schemas.py`
- `backend/app/services/document_registry.py`
- `backend/tests/unit/test_document_registry.py`
- `backend/app/api/reports.py`

## Expected Output

- `backend/app/schemas.py`
- `backend/app/services/document_registry.py`
- `backend/app/services/ingest_events.py`
- `backend/tests/unit/test_document_registry.py`
- `backend/tests/unit/test_ingest_events.py`

## Verification

rtk uv --directory backend run --extra dev pytest tests/unit/test_document_registry.py tests/unit/test_ingest_events.py

## Observability Impact

Creates the canonical observability payload and event distribution seam for all later ingestion progress surfaces.
