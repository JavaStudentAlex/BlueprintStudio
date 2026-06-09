# S03: Parser And Conversion Pipeline

**Goal:** Provide a robust background ingestion pipeline that converts CAD documents into engineering graphs with live SSE progress tracking, accepts partial parser results with user-visible warnings, and supports AUTO drawing detection with manual reparse overrides.
**Demo:** unit tests prove Parser And Conversion Pipeline works

## Must-Haves

- Uploading supported CAD or document files returns promptly after registry persistence while conversion, parsing, graph artifact storage, and KB indexing continue in a tracked background task.
- Backend emits typed ingestion SSE events for queued, processing, conversion, parsing, indexing, indexed, warning, skipped, and failed transitions, with heartbeats and cleanup when clients disconnect.
- Parser warnings and skipped unsupported entities are persisted as document warning metadata; documents with usable partial graphs end in an indexed state that the frontend can render as Ready (Warnings), not failed.
- Manual drawing type override after AUTO detection validates routing, reuses the stored upload path, triggers a safe reparse, and streams the resulting status updates.
- Frontend API, store, FileTree, and FilePreview consume the event contract and render Processing, Ready, Ready (Warnings), Failed, and Skipped states deterministically.
- Requirement coverage: owns PARSE-04; supports PARSE-02, PARSE-03, GRAPH-07, UI-01, and downstream compliance/reporting slices by producing persisted graph artifacts tied to source documents.
- Quality gates: Q3 threat surface covers SSE data minimization, document ID validation, and path-safe reparse; Q4 requirement impact is documented in task plans; Q5 failure modes include parser/converter failures and client disconnects; Q6 load profile uses bounded in-memory queues with cleanup; Q7 negative tests cover malformed routing, partial warnings, duplicate uploads, and failed conversions.

## Proof Level

- This slice proves: Contract and integration proof. Backend unit tests must exercise the event bus, document warning metadata, background task lifecycle, parser partial-warning handling, and manual reparse routing. Frontend unit tests must exercise SSE parsing, store state transitions, FileTree badges, FilePreview warning details, and manual override actions. Final verification must run the targeted backend and frontend test sets from the repository root using existing rtk, uv, npm, pytest, and vitest commands.

## Integration Closure

S03 closes when backend ingestion state, graph artifact persistence, SSE events, frontend client streaming, global store updates, and visible file status surfaces all use the same typed contract. The implementation must preserve existing EngineeringConverter and DrawingParserAdapter protocols, keep existing ingest_directory behavior working, avoid committing runtime data under backend/data, and leave S04 able to consume graph artifacts without depending on frontend-only state.

## Verification

- Adds ingestion progress observability through a typed backend event bus, SSE stream events, registry warnings/errors, frontend per-document progress state, and visible user-facing status badges. Events must include stage, status, document_id, safe filename, optional progress percentage, and warning summaries, but must not include raw document content or secrets.

## Tasks

- [ ] **T01: Define ingest event and warning contracts** `est:1 day`
  ---
  skills_used:
    - api-design
    - design-an-interface
    - verify-before-complete
  ---
  Why: S03 needs a single backend contract for progress, warnings, partial success, and downstream frontend parsing before background work or UI wiring can be reliable.
  - Files: `backend/app/schemas.py`, `backend/app/services/document_registry.py`, `backend/app/services/ingest_events.py`, `backend/tests/unit/test_document_registry.py`, `backend/tests/unit/test_ingest_events.py`
  - Verify: rtk uv --directory backend run --extra dev pytest tests/unit/test_document_registry.py tests/unit/test_ingest_events.py

- [ ] **T02: Instrument conversion and parser pipeline** `est:1.5 days`
  ---
  skills_used:
    - tdd
    - verify-before-complete
  ---
  Why: The existing ingestion service performs conversion, parser, graph artifact, and KB indexing work synchronously without fine-grained progress or partial-warning semantics.
  - Files: `backend/app/services/ingestion.py`, `backend/tests/unit/test_ingestion.py`
  - Verify: rtk uv --directory backend run --extra dev pytest tests/unit/test_ingestion.py tests/unit/test_ingest_events.py

- [ ] **T03: Add background ingest API, SSE stream, and reparse override** `est:1.5 days`
  ---
  skills_used:
    - api-design
    - tdd
    - verify-before-complete
  ---
  Why: Uploads must stop blocking the UI, and users need a post-upload manual route override when AUTO drawing detection is wrong or ambiguous.
  - Files: `backend/app/main.py`, `backend/app/api/ingest.py`, `backend/tests/unit/test_ingest_api.py`
  - Verify: rtk uv --directory backend run --extra dev pytest tests/unit/test_ingest_api.py tests/unit/test_ingestion.py

- [ ] **T04: Wire frontend ingest stream client and store state** `est:1 day`
  ---
  skills_used:
    - api-design
    - tdd
    - verify-before-complete
  ---
  Why: The frontend shell needs a typed client and durable store transitions before FileTree and FilePreview can render live processing states.
  - Files: `frontend/src/types/index.ts`, `frontend/src/lib/api.ts`, `frontend/src/lib/store.ts`, `frontend/tests/unit/api.test.ts`, `frontend/tests/unit/store.test.ts`
  - Verify: rtk npm --prefix frontend test -- frontend/tests/unit/api.test.ts frontend/tests/unit/store.test.ts

- [ ] **T05: Render processing and warning states in FileTree and FilePreview** `est:1 day`
  ---
  skills_used:
    - tdd
    - verify-before-complete
  ---
  Why: Users must see long-running conversion status, partial-warning readiness, failures, and manual override controls in the IDE-style shell without blocking interaction.
  - Files: `frontend/src/lib/mock.ts`, `frontend/src/components/files/FileTree.tsx`, `frontend/src/components/preview/FilePreview.tsx`, `frontend/tests/unit/file-processing-status.test.tsx`
  - Verify: rtk npm --prefix frontend test -- frontend/tests/unit/file-processing-status.test.tsx

- [ ] **T06: Run cross-stack contract gates and close slice proof** `est:0.5 day`
  ---
  skills_used:
    - verify-before-complete
    - write-docs
  ---
  Why: S03 changes a cross-stack contract across backend schemas, SSE, frontend parsing, registry state, parser warnings, and UI status rendering; the slice needs one final targeted proof pass.
  - Verify: rtk uv --directory backend run --extra dev pytest tests/unit/test_document_registry.py tests/unit/test_ingest_events.py tests/unit/test_ingestion.py tests/unit/test_ingest_api.py && rtk npm --prefix frontend test -- frontend/tests/unit/api.test.ts frontend/tests/unit/store.test.ts frontend/tests/unit/file-processing-status.test.tsx

## Files Likely Touched

- backend/app/schemas.py
- backend/app/services/document_registry.py
- backend/app/services/ingest_events.py
- backend/tests/unit/test_document_registry.py
- backend/tests/unit/test_ingest_events.py
- backend/app/services/ingestion.py
- backend/tests/unit/test_ingestion.py
- backend/app/main.py
- backend/app/api/ingest.py
- backend/tests/unit/test_ingest_api.py
- frontend/src/types/index.ts
- frontend/src/lib/api.ts
- frontend/src/lib/store.ts
- frontend/tests/unit/api.test.ts
- frontend/tests/unit/store.test.ts
- frontend/src/lib/mock.ts
- frontend/src/components/files/FileTree.tsx
- frontend/src/components/preview/FilePreview.tsx
- frontend/tests/unit/file-processing-status.test.tsx
