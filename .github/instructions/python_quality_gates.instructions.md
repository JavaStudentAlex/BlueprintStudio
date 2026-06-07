---
applyTo: "backend/**/*.py"
description: "Backend Python linting, formatting, typecheck, and test gate policy for BlueprintStudio."
---

# Python Quality Gates

## Purpose and Scope

This file defines the verification policy for backend Python changes in this
repository.

Applies to:

- `backend/app/**/*.py`
- `backend/tests/**/*.py`
- `scripts/**/*.py` when scripts exercise backend behavior

Does not apply to docs-only or frontend-only changes, although docs changes
should still be checked for path and command accuracy.

## Tooling Rules

- Use `rtk uv --directory backend run --extra dev ...` from the repository root.
- Use `backend/pyproject.toml` and GitHub Actions as the source of truth.
- Use Ruff for formatting and linting.
- Use mypy for backend application type checking.

## Quality Gates

Run from the repository root when backend Python code changes:

```bash
rtk uv --directory backend run --extra dev ruff format --check app tests
rtk uv --directory backend run --extra dev ruff check app tests
rtk uv --directory backend run --extra dev mypy app
rtk uv --directory backend run --extra dev pytest -q
```

## Target Selection Guidance

- `backend/app/api/*` -> `backend/tests/unit` and affected integration tests
- `backend/app/agent/*` -> chat, thread, and checkpointer tests
- `backend/app/kb/*` -> knowledge-base unit tests and skipped integration tests
  when services are unavailable
- `backend/app/services/document*` or ingestion services -> ingestion and
  registry tests
- `backend/app/services/report*` -> report pipeline, report sessions, report
  endpoint, and PDF export tests
- `backend/app/config.py` or `backend/app/main.py` -> health, ready, app
  composition, and settings tests
- Cross-stack schema changes -> backend tests plus relevant frontend API/type
  tests

## Notes

- Report blocked or failed gates explicitly.
- Do not claim verification you did not run.
- If a full suite is too slow or blocked by optional services, run the most
  relevant deterministic subset and state the limitation.
