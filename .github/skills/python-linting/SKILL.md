---
name: python-linting
description: Run backend Python linting, formatting, and type checks for BlueprintStudio using uv, Ruff, and mypy. Use when editing backend app code, tests, scripts, or tooling.
---

# Python Linting Skill

## Scope

- Backend package code: `backend/app/`
- Backend tests: `backend/tests/`
- Backend Python configuration source of truth: `backend/pyproject.toml`
- CI reference: `.github/workflows/ci.yml`

All commands should go through `rtk` in this environment.

## Quality Gates

```bash
rtk uv --directory backend run --extra dev ruff format --check app tests
rtk uv --directory backend run --extra dev ruff check app tests
rtk uv --directory backend run --extra dev mypy app
```

## Targeted Checks

Use targeted paths when the change is narrow:

```bash
rtk uv --directory backend run --extra dev ruff format --check app/services tests/unit
rtk uv --directory backend run --extra dev ruff check app/api tests/integration
```

## Guardrails

- Do not change runtime behavior solely to satisfy linting unless the lint issue
  exposes a real bug.
- Re-run the relevant check after fixes.
- Pair linting with targeted pytest when the change affects behavior.
