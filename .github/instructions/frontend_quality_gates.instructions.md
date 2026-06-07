---
applyTo: "frontend/**/*.{ts,tsx,js,jsx,css,json}"
description: "Frontend linting, typecheck, test, and build gate policy for BlueprintStudio."
---

# Frontend Quality Gates

## Purpose and Scope

This file defines the verification policy for frontend TypeScript, React, and
UI changes in this repository.

Applies to:

- `frontend/src/**/*`
- `frontend/tests/**/*`
- `frontend/package.json`
- `frontend/package-lock.json`
- frontend config files

Does not apply to docs-only or backend-only changes, although docs changes
should still be checked for path and command accuracy.

## Tooling Rules

- Use `rtk npm --prefix frontend ...` from the repository root.
- Use `frontend/package.json`, `frontend/package-lock.json`, and GitHub Actions
  as the source of truth.
- Use Next lint, TypeScript, Vitest, and the existing build command.

## Quality Gates

Run from the repository root when frontend code changes:

```bash
rtk npm --prefix frontend run lint
rtk npm --prefix frontend exec -- tsc --noEmit
rtk npm --prefix frontend test
rtk npm --prefix frontend run build
```

## Target Selection Guidance

- API client, SSE parsing, or shared types -> `frontend/tests/unit/api.test.ts`
  and affected flow tests
- Zustand store behavior -> store-focused unit tests and affected flow tests
- Chat or report UI -> chat/report component and flow tests
- Onboarding, profile, settings, graph, files, or preview UI -> matching
  component or flow tests
- Visual or route-level browser behavior -> Playwright e2e when practical and
  the app stack is available

## Notes

- Report blocked or failed gates explicitly.
- Do not claim verification you did not run.
- If browser e2e is blocked by missing services, run deterministic Vitest tests
  and state the limitation.
