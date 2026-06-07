---
name: python-testing
description: Run backend pytest for BlueprintStudio using uv with subsystem-aware target selection. Use when changing backend code, tests, scripts, or debugging failures.
---

# Python Testing Skill

Use this skill to run and inspect backend Python tests for this repository.

## Scope

- Test directory: `backend/tests/`
- Preferred execution wrapper: `rtk uv --directory backend run --extra dev ...`
- CI reference: `.github/workflows/ci.yml`

## Running Tests

```bash
rtk uv --directory backend run --extra dev pytest tests/unit -q
rtk uv --directory backend run --extra dev pytest tests/integration -q
rtk uv --directory backend run --extra dev pytest tests/e2e -q
rtk uv --directory backend run --extra dev pytest -q
```

## Target Selection

- API route changes -> endpoint-focused unit or integration tests.
- Ingestion or registry changes -> ingestion, document, and registry tests.
- Knowledge-base changes -> fake and MemoryPalace adapter tests, with external
  service tests skipped when unavailable.
- Chat, thread, or checkpointer changes -> chat and thread tests.
- Report services or routes -> report pipeline, report session, report endpoint,
  and export tests.
- Settings or app composition changes -> health, ready, main, and config tests.

## Pass Criteria

- The selected test command exits with code `0`.
- All collected tests pass.
- Any skipped or blocked external-service checks are named explicitly.

## Troubleshooting

If dev dependencies are missing:

```bash
rtk uv --directory backend sync --extra dev
```
