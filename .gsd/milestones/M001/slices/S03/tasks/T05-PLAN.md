---
estimated_steps: 16
estimated_files: 4
skills_used: []
---

# T05: Render processing and warning states in FileTree and FilePreview

---
skills_used:
  - tdd
  - verify-before-complete
---
Why: Users must see long-running conversion status, partial-warning readiness, failures, and manual override controls in the IDE-style shell without blocking interaction.

Do:
- Extend ProjectFile-compatible UI data with ingestion status, progress, warning count or summary, error summary, and current routing where needed.
- Update FileTree rows to render Processing, Ready, Ready (Warnings), Failed, and Skipped states with accessible labels and stable test selectors.
- Update FilePreview to show current pipeline stage, warning details for partial parses, failure/skipped reasons, and a manual drawing type override control that triggers the reparse action from the store.
- Ensure existing warningRange behavior and non-ingestion mock demo behavior remain unchanged for files without ingestion metadata.
- Add React tests for processing spinner, progress text, Ready (Warnings) badge, failure rendering, and manual override action invocation.

Done when:
- UI tests prove status badges and preview details update from store state without requiring a backend server.
- Q4: UI-01 and GRAPH-07 supporting behavior is visible to users.
- Q7: Negative tests cover files with no ingestion metadata and failed/skipped documents.

## Inputs

- `frontend/src/lib/mock.ts`
- `frontend/src/components/files/FileTree.tsx`
- `frontend/src/components/preview/FilePreview.tsx`
- `frontend/src/lib/store.ts`

## Expected Output

- `frontend/src/lib/mock.ts`
- `frontend/src/components/files/FileTree.tsx`
- `frontend/src/components/preview/FilePreview.tsx`
- `frontend/tests/unit/file-processing-status.test.tsx`

## Verification

rtk npm --prefix frontend test -- frontend/tests/unit/file-processing-status.test.tsx

## Observability Impact

Makes ingestion observability visible in the primary file navigation and preview surfaces.
