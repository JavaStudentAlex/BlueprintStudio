---
applyTo: "**/tests/**/*"
description: "Test conventions, organization, and verification patterns for BlueprintStudio."
---

# Test Instructions

## Scope

This covers backend pytest tests, frontend Vitest/RTL/MSW tests, Playwright e2e
tests, and deterministic script or CLI verification used to prove repository
behavior.

## Tooling Rules

- Use `rtk uv --directory backend run --extra dev pytest ...` for backend tests.
- Use `rtk npm --prefix frontend test` for frontend unit and flow tests.
- Use `rtk npm --prefix frontend run e2e` or `make e2e` for Playwright when the
  required stack is available.
- Prefer targeted test paths first; run broader tests when touched behavior
  crosses subsystem boundaries.

## Behavioral Overlay

For test changes, also apply:

- `.github/instructions/code_writing_behavior.instructions.md`
- `.github/instructions/backend_app.instructions.md` when backend behavior is
  involved
- `.github/instructions/frontend_app.instructions.md` when frontend behavior is
  involved
- the relevant quality-gate instruction file

## Test Organization

- Keep backend shared fixtures in `backend/tests/conftest.py` or explicit
  subsystem helpers.
- Keep frontend shared setup in existing Vitest and test helper files.
- Use deterministic fakes for knowledge base, chat models, external APIs,
  filesystem state, and time-sensitive flows.
- Use `tmp_path` for backend filesystem behavior.
- Use MSW or local mocks for frontend network behavior.
- Avoid tests that require real external services unless they are clearly
  marked and skipped when unavailable.

## Test Conventions

- Assert on contract boundaries: API shape, status transitions, SSE payloads,
  persisted records, report gate behavior, export paths, and frontend state.
- Keep tests small and focused on one behavior.
- Include explicit failure assertions for invalid uploads, missing records,
  closed gates, unavailable exports, malformed SSE data, and service failures.
- For regressions, add the narrowest test that would have failed before the fix.
- Never call real LLMs, Ollama, Postgres, GitHub, or other third-party APIs
  from default tests.

## Repository-Specific Priorities

- Cover ingestion validation, registry status, and knowledge-base writes.
- Cover chat streaming, sync chat, thread history, and checkpoint behavior.
- Cover report launch, stage progression, gates, validation findings, export
  records, and safe downloads.
- Cover frontend API parsing, store transitions, chat/report UI, onboarding,
  settings, and profile/export flows.
- Cover cross-stack schema changes from backend models through frontend types.

## Running Tests

Examples from the repository root:

```bash
rtk uv --directory backend run --extra dev pytest tests/unit -q
rtk uv --directory backend run --extra dev pytest tests/integration -q
rtk uv --directory backend run --extra dev pytest -q
rtk npm --prefix frontend test
rtk npm --prefix frontend run e2e
```
