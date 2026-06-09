---
analysis_date: 2026-06-07
focus: quality
last_mapped_commit: b7a5fca729d82fd6d25707deb6edc1356f008624
last_mapped_at: 2026-06-07
project: BlueprintStudio
---
# Coding Conventions

## Overview

BlueprintStudio is split between a Python backend under `backend/app` and a
Next.js frontend under `frontend/src`. The codebase favors explicit contracts,
small helpers, and direct imports over framework magic.

## Naming Patterns

### Backend

- Files use `snake_case.py` under `backend/app/**` (`api/chat.py`,
  `services/report_pipeline.py`, `services/document_registry.py`).
- Public classes and Pydantic models use `PascalCase`
  (`AppState`, `ReportSessionRecord`, `ChatRequest`).
- Functions and methods use `snake_case`; private helpers begin with `_`
  (`_prepare_uploads`, `_safe`, `_build_pipeline`).
- Constants use `UPPER_SNAKE_CASE`, with module-private constants often using
  a leading underscore (`_TERMINAL_SESSION_STATUSES`,
  `_MAX_LOG_PAYLOAD_CODES`).
- Durable state is usually represented with `@dataclass(slots=True, frozen=True)`
  records or lightweight wrapper classes.

### Frontend

- Components use `PascalCase.tsx` (`AppShell.tsx`, `ReportView.tsx`,
  `ChatPanel.tsx`, `FileTree.tsx`).
- Shared libraries use `camelCase.ts` (`api.ts`, `store.ts`, `mock.ts`).
- Route files keep the Next.js conventions (`page.tsx`, `layout.tsx`).
- Shared wire types live in `frontend/src/types/index.ts` and use
  `PascalCase` type aliases and union names.

### Tests

- Backend test files use `test_*.py`.
- Vitest files use `*.test.ts` or `*.test.tsx`.
- Playwright files use `*.spec.ts`.
- Private test helpers may use underscore-prefixed module names such as
  `backend/tests/_fakes.py`.

## Code Style

### Python

- `from __future__ import annotations` is standard in application modules.
- Type hints are pervasive; return types are explicit on public helpers and
  route handlers.
- Module docstrings are common, especially in `backend/app/api/**` and
  `backend/app/services/**`.
- Pydantic models own wire contracts and coercion via `field_validator`,
  `model_validate`, and `model_dump_json`.
- Route handlers stay thin and defer business logic to services or stores.
- Optional arguments are commonly keyword-only.
- Backend style is governed by Ruff in `backend/pyproject.toml`:
  line length 100, target Python 3.11, and `E/F/I/B/UP/N/S` selected with
  `S101` ignored.

### TypeScript and React

- Interactive components declare `"use client"` only when browser APIs or
  hooks are required.
- Functional components, hooks, and Zustand state are the dominant patterns.
- Double quotes and semicolons are the prevailing formatting style.
- Tailwind utility classes carry most styling, with brand tokens defined in
  `frontend/src/app/globals.css` and `frontend/tailwind.config.ts`.
- `frontend/.eslintrc.json` extends `next/core-web-vitals`; no repo Prettier
  config was detected.

## Import Organization

### Backend

1. `from __future__ import annotations`
2. Stdlib imports
3. Third-party imports
4. Local `app.*` imports

- Tests import from `app.*` and `tests.*` instead of reaching across the tree
  with relative paths.
- Concrete modules are imported directly; barrel layers are uncommon.

### Frontend

1. External packages
2. `@/` alias imports
3. Nearby relative component imports

- Use `import type` for type-only imports where possible.
- `frontend/tsconfig.json` maps `@/*` to `frontend/src/*`.

## Error Handling

- HTTP boundaries raise `HTTPException` with specific status codes.
  Examples: `backend/app/api/ingest.py`, `backend/app/api/chat.py`,
  `backend/app/api/reports.py`.
- Service and store layers raise `ValueError`, `KeyError`, or `RuntimeError`
  for invalid input or missing durable rows.
- Streaming code keeps failures visible without tearing down the whole stream.
  `backend/app/api/chat.py` emits `error` and `done` chunks, and
  `backend/app/api/health.py` returns degraded readiness instead of failing.
- SQLite-backed stores validate transitions explicitly in
  `backend/app/services/document_registry.py` and
  `backend/app/services/report_sessions.py`.
- Frontend fetch helpers normalize failures in `frontend/src/lib/api.ts` by
  throwing `Error("HTTP ...")` with the status and response text.

## Logging

- The repo uses the standard library `logging` module in a few integration
  boundaries such as `backend/app/kb/memorypalace.py` and
  `backend/app/services/standards_indexer.py`.
- Logging is mostly warning-oriented for optional dependency or reachability
  issues.
- There is no dedicated structured logging package or app-wide logging facade
  in the inspected code.
- Avoid ad hoc `console.log` or unscoped print-based tracing in production
  code.

## Comments

- Backend modules and many tests use module docstrings to explain lifecycle or
  contract behavior.
- Public route and service entry points often have docstrings; tiny helpers can
  stay undocumented when the signature is self-explanatory.
- Inline comments are used to explain why a workaround exists, not to restate
  obvious code.
- Suppression comments should stay narrow and justified
  (`# noqa: BLE001`, `# type: ignore[...]`).
- Test comments are acceptable when they explain environment quirks, payload
  framing, or sanitization rules.

## Function Design

- Keep functions small and composable.
- Prefer guard clauses and early returns over deep nesting.
- Use local helper functions or dataclasses when a route handler would
  otherwise become too large.
- Optional knobs are usually keyword-only.
- Return explicit typed objects rather than loosely shaped ad hoc dicts at
  module boundaries.

## Module Design

- `backend/app/main.py` is the composition root for settings, KB, checkpointer,
  registry, report sessions, and router wiring.
- `backend/app/api/**` contains boundary code only.
- `backend/app/services/**` contains business logic, persistence adapters, and
  transformation helpers.
- `frontend/src/lib/store.ts` centralizes client state.
- `frontend/src/components/**` stays presentation-oriented.
- Shared contracts live in `backend/app/schemas.py` and
  `frontend/src/types/index.ts`; keep them aligned when changing wire shapes.
- Barrel files are rare; import concrete modules unless a re-export materially
  reduces churn.

## Reference Files

- `backend/app/main.py`
- `backend/app/config.py`
- `backend/app/schemas.py`
- `backend/app/api/chat.py`
- `backend/app/api/ingest.py`
- `backend/app/services/ingestion.py`
- `backend/app/services/report_pipeline.py`
- `frontend/src/lib/api.ts`
- `frontend/src/lib/store.ts`
- `frontend/src/components/report/ReportView.tsx`
- `frontend/src/components/chat/ChatPanel.tsx`

*Convention analysis: 2026-06-07*
