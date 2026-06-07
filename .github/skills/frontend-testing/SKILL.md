---
name: frontend-testing
description: Run frontend Vitest, React Testing Library, MSW, and Playwright checks for BlueprintStudio. Use when changing frontend behavior or API contracts.
---

# Frontend Testing Skill

Use this skill to run and inspect frontend tests for this repository.

## Scope

- Test directory: `frontend/tests/`
- Preferred execution wrapper: `rtk npm --prefix frontend ...`
- CI reference: `.github/workflows/ci.yml`

## Running Tests

```bash
rtk npm --prefix frontend test
rtk npm --prefix frontend run e2e
```

## Target Selection

- API client, SSE parsing, or shared types -> `frontend/tests/unit/api.test.ts`
  and affected flow tests.
- Store behavior -> store-focused unit tests and affected flow tests.
- Chat or report UI -> chat/report component and flow tests.
- Onboarding, profile, settings, graph, files, or preview UI -> matching
  component or flow tests.
- Browser-level behavior -> Playwright e2e when the stack is available.

## Pass Criteria

- The selected test command exits with code `0`.
- All collected tests pass.
- Any blocked browser or service checks are named explicitly.

## Troubleshooting

If dependencies are missing:

```bash
rtk npm --prefix frontend ci
```
