---
estimated_steps: 16
estimated_files: 7
skills_used: []
---

# T06: Run cross-stack contract gates and close slice proof

---
skills_used:
  - verify-before-complete
  - write-docs
---
Why: S03 changes a cross-stack contract across backend schemas, SSE, frontend parsing, registry state, parser warnings, and UI status rendering; the slice needs one final targeted proof pass.

Do:
- Run the targeted backend unit tests for registry warnings, event bus behavior, ingestion instrumentation, and ingest API SSE/background lifecycle.
- Run the targeted frontend unit tests for API stream parsing, store transitions, and FileTree/FilePreview status rendering.
- If a targeted test exposes a contract mismatch, fix it in the owning task files rather than weakening assertions.
- Record any limitations in the task summary, especially the intentionally single-process in-memory SSE bus and any future durable-queue follow-up.

Done when:
- Backend and frontend targeted gates pass in the current session.
- No test reads or writes .gsd, .planning, .audits, backend/data runtime uploads, secrets, or external services.
- Q6: The final proof confirms bounded event behavior is tested and no external broker is required for this milestone.
- Integration closure: S04 can depend on persisted graph artifacts and document warning state rather than frontend-only status.

## Inputs

- `backend/tests/unit/test_document_registry.py`
- `backend/tests/unit/test_ingest_events.py`
- `backend/tests/unit/test_ingestion.py`
- `backend/tests/unit/test_ingest_api.py`
- `frontend/tests/unit/api.test.ts`
- `frontend/tests/unit/store.test.ts`
- `frontend/tests/unit/file-processing-status.test.tsx`

## Expected Output

- Update the implementation and proof artifacts needed for this task.

## Verification

rtk uv --directory backend run --extra dev pytest tests/unit/test_document_registry.py tests/unit/test_ingest_events.py tests/unit/test_ingestion.py tests/unit/test_ingest_api.py && rtk npm --prefix frontend test -- frontend/tests/unit/api.test.ts frontend/tests/unit/store.test.ts frontend/tests/unit/file-processing-status.test.tsx

## Observability Impact

Confirms the cross-stack ingestion observability contract is verifiable without live external services.
