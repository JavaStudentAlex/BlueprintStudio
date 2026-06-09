---
estimated_steps: 18
estimated_files: 5
skills_used: []
---

# T04: Wire frontend ingest stream client and store state

---
skills_used:
  - api-design
  - tdd
  - verify-before-complete
---
Why: The frontend shell needs a typed client and durable store transitions before FileTree and FilePreview can render live processing states.

Do:
- Add TypeScript ingest event, document status, parser warning, and routing override types that mirror backend schemas.
- Add API helpers for opening the ingest SSE stream and requesting manual document reparse without changing existing chat/report stream behavior.
- Extend the Zustand store with per-document ingestion status, stage, progress, warning summaries, error summaries, routing, and actions to apply ingest events idempotently.
- Ensure duplicate or out-of-order events do not regress a terminal indexed, failed, skipped, or Ready (Warnings) state unless a new reparse generation starts.
- Keep EventSource setup testable by accepting injectable constructors or callback seams already consistent with existing stream helpers.

Done when:
- Frontend unit tests prove SSE parsing, stream error handling, store event application, warning preservation, terminal-state idempotency, and manual reparse action dispatch.
- Q4: Frontend state directly supports PARSE-04 and UI-01 surfaces.
- Q5: Stream errors and duplicated events leave visible state deterministic.
- Q7: Negative tests cover malformed event payloads and failed reparse requests.

## Inputs

- `frontend/src/types/index.ts`
- `frontend/src/lib/api.ts`
- `frontend/src/lib/store.ts`
- `frontend/tests/unit/api.test.ts`
- `frontend/tests/unit/store.test.ts`

## Expected Output

- `frontend/src/types/index.ts`
- `frontend/src/lib/api.ts`
- `frontend/src/lib/store.ts`
- `frontend/tests/unit/api.test.ts`
- `frontend/tests/unit/store.test.ts`

## Verification

rtk npm --prefix frontend test -- frontend/tests/unit/api.test.ts frontend/tests/unit/store.test.ts

## Observability Impact

Maintains a client-side per-document observability model for ingestion stage, progress, warnings, and errors.
