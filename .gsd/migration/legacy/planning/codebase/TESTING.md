---
analysis_date: 2026-06-07
focus: quality
last_mapped_commit: b7a5fca729d82fd6d25707deb6edc1356f008624
last_mapped_at: 2026-06-07
project: BlueprintStudio
---
# Testing Patterns

## Overview

BlueprintStudio uses deterministic backend fixtures and frontend mocks to keep
default tests hermetic. The backend is exercised with `pytest`; the frontend
uses `Vitest`, React Testing Library, MSW, and Playwright.

## Test Framework

### Backend

- Runner: `pytest 8.3.x` from `backend/pyproject.toml`.
- Async support: `pytest-asyncio` with `asyncio_mode = auto`.
- Extra tooling: `pytest-cov` is available, but no backend coverage threshold
  is configured.
- Markers: `integration` and `e2e`, enforced with `--strict-markers`.
- Primary command: `rtk uv --directory backend run --extra dev pytest -q`.
- Useful focused runs:
  - `rtk uv --directory backend run --extra dev pytest -q backend/tests/unit/test_fusion.py`
  - `rtk uv --directory backend run --extra dev pytest -q backend/tests/integration/test_chat_endpoint.py`

### Frontend

- Runner: `Vitest` in `frontend/vitest.config.ts`.
- Assertion library: Vitest `expect` plus React Testing Library assertions from
  `@testing-library/jest-dom/vitest`.
- DOM environment: `jsdom`.
- E2E runner: Playwright in `frontend/playwright.config.ts`.
- Primary commands:
  - `rtk npm --prefix frontend run test`
  - `rtk npm --prefix frontend run e2e`
  - `rtk npm --prefix frontend exec -- tsc --noEmit`

## Test File Organization

- Backend unit tests live in `backend/tests/unit`.
- Backend integration tests live in `backend/tests/integration`.
- Backend e2e scaffolding lives in `backend/tests/e2e`.
- Shared backend fixtures live in `backend/tests/fixtures/graphs` and
  `backend/tests/fixtures/flowdraft`.
- Frontend unit tests live in `frontend/tests/unit`.
- Frontend E2E tests live in `frontend/tests/e2e`.
- Frontend fixtures live in `frontend/tests/fixtures/graphs` and
  `frontend/tests/fixtures/flowdraft`.
- Shared backend fakes live in `backend/tests/_fakes.py`; frontend setup lives
  in `frontend/tests/setup.ts`.
- Representative layout:

```text
backend/tests/
  unit/
    test_schemas.py
    test_ingestion.py
    test_report_pipeline.py
  integration/
    test_chat_endpoint.py
    test_ingest_endpoint.py
  fixtures/
    graphs/
      architecture_only.json
      fused_graph.json
frontend/tests/
  unit/
    ReportView.test.tsx
    api.test.ts
    store.test.ts
  e2e/
    pipeline.spec.ts
    report.spec.ts
  fixtures/
    graphs/
      architecture_only.json
      fused_graph.json
```

## Test Structure

- Backend tests use both plain functions and `class Test...` groupings.
- Small service suites tend to be function-based, while larger schema or
  endpoint suites use classes for grouping (`backend/tests/unit/test_schemas.py`,
  `backend/tests/integration/test_chat_endpoint.py`).
- `pytest.fixture` and `pytest_asyncio.fixture` are used heavily for reusable
  app wiring and async resource setup.
- `backend/tests/conftest.py` builds an injected FastAPI app around
  in-memory SQLite, `FakeKB`, and a scripted LLM for most tests.
- Frontend tests use `describe`/`it` blocks with `beforeEach` cleanup and
  explicit expectations around rendered output.
- Complex tests keep an implicit arrange/act/assert flow, even when the
  assertions span multiple related fields in a single payload.

## Mocking

- Backend external boundaries are replaced with `FakeKB`,
  `ScriptedChatModel`, `make_fake_chat_model`, monkeypatching, and in-memory
  lifespan managers.
- `backend/tests/unit/test_chat_endpoint.py` scripts LLM responses so SSE and
  sync outputs stay deterministic.
- `backend/tests/unit/test_report_pipeline.py` uses fake chat payloads and
  temporary export directories to exercise the state machine.
- Frontend network calls are mocked with MSW via `setupServer`,
  `http.*` handlers, and `HttpResponse.json`.
- `frontend/tests/setup.ts` clears `window.localStorage`, resets the Zustand
  store, and restores timers after each test.
- Mock external services and network boundaries; keep pure parsing and state
  logic real.

## Fixtures and Factories

- Graph fixtures are JSON files under `backend/tests/fixtures/graphs` and
  `frontend/tests/fixtures/graphs`.
- FlowDraft demo fixtures are mirrored under `backend/tests/fixtures/flowdraft`
  and `frontend/tests/fixtures/flowdraft`.
- Helper factories are usually defined next to the tests that need them
  (`makeInspection` in `frontend/tests/unit/store.test.ts`,
  `_pipeline_context` in `backend/tests/unit/test_report_pipeline.py`).
- Keep fixtures small, deterministic, and provenance-backed when they model
  external behavior.

## Coverage

- No repo-wide coverage threshold or frontend coverage script is configured in
  the inspected files.
- `pytest-cov` is available on the backend, but coverage reporting is opt-in.
- Coverage emphasis is on critical paths rather than blanket line percentage:
  graph validation, ingestion dedupe, chat SSE framing, report pipeline
  transitions, store hydration, and fixture validity.
- Add coverage around the touched behavior when changing a boundary or shared
  contract.

## Test Types

- Unit tests cover pure functions, validators, serializers, and isolated UI
  components.
- Integration tests cover route handlers and multi-module flows with injected
  state.
- E2E tests cover browser-level user flows with Playwright.
- Current references for browser-style coverage are
  `frontend/tests/e2e/pipeline.spec.ts` and `frontend/tests/e2e/report.spec.ts`.
- Backend `tests/e2e` exists as a package, but the visible browser flow still
  lives in the frontend tree.

## Common Patterns

- Assert explicit HTTP status codes and JSON payloads in route tests.
- Assert SSE framing and event names when testing streamed endpoints.
- Use `pytest.raises` for validation failures and `await expect(...).rejects`
  for async JavaScript failures.
- Use MSW and route handlers to keep fetch-based tests hermetic.
- Avoid snapshot testing for these flows; the current codebase prefers explicit
  assertions on text, attributes, classes, and encoded URLs.
- Test names are descriptive and behavior-driven rather than implementation
  centered.

## Reference Files

- `backend/pyproject.toml`
- `backend/tests/conftest.py`
- `backend/tests/_fakes.py`
- `backend/tests/unit/test_schemas.py`
- `backend/tests/unit/test_ingestion.py`
- `backend/tests/unit/test_report_pipeline.py`
- `backend/tests/integration/test_chat_endpoint.py`
- `backend/tests/integration/test_ingest_endpoint.py`
- `frontend/vitest.config.ts`
- `frontend/playwright.config.ts`
- `frontend/tests/setup.ts`
- `frontend/tests/unit/api.test.ts`
- `frontend/tests/unit/store.test.ts`
- `frontend/tests/unit/ReportView.test.tsx`
- `frontend/tests/e2e/pipeline.spec.ts`
- `frontend/tests/e2e/report.spec.ts`

*Testing analysis: 2026-06-07*
