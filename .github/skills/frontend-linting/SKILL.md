---
name: frontend-linting
description: Run frontend linting, TypeScript checks, and build checks for BlueprintStudio using npm. Use when editing frontend source, tests, or configuration.
---

# Frontend Linting Skill

## Scope

- Frontend source: `frontend/src/`
- Frontend tests: `frontend/tests/`
- Frontend configuration source of truth: `frontend/package.json`
- CI reference: `.github/workflows/ci.yml`

All commands should go through `rtk` in this environment.

## Quality Gates

```bash
rtk npm --prefix frontend run lint
rtk npm --prefix frontend exec -- tsc --noEmit
rtk npm --prefix frontend run build
```

## Guardrails

- Do not change user-facing behavior solely to satisfy linting unless the issue
  exposes a real bug.
- Re-run the relevant check after fixes.
- Pair linting and type checks with targeted tests when behavior changes.
