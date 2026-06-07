---
applyTo: "frontend/**/*.{ts,tsx,js,jsx,css}"
description: "Frontend conventions, Next.js contracts, and UI boundaries for BlueprintStudio."
---

# Frontend App Instructions

## Scope

This covers:

- `frontend/src/app/**/*`
- `frontend/src/components/**/*`
- `frontend/src/lib/**/*`
- `frontend/src/types/**/*`
- `frontend/tests/**/*` when tests exercise frontend behavior

## Tooling Rules

- Use `rtk npm --prefix frontend ...` from the repository root.
- Use `frontend/package.json`, `frontend/package-lock.json`, and GitHub Actions
  as the source of truth for frontend tools.
- Use existing Next.js, TypeScript, Tailwind, Zustand, Vitest, RTL, MSW, and
  Playwright patterns.
- Do not introduce another package manager or UI framework without updating
  configuration, lockfiles, CI, and tests.

## Architecture Rules

- Keep route entry points under `frontend/src/app`.
- Keep reusable UI under `frontend/src/components`, grouped by domain surface.
- Keep API client behavior in `frontend/src/lib/api.ts`.
- Keep global client state in `frontend/src/lib/store.ts`.
- Keep shared TypeScript contracts in `frontend/src/types`.
- Keep mock-only behavior in `frontend/src/lib/mock.ts` and tests.
- Keep UI components focused; move complex parsing, normalization, or state
  transitions into helpers that are easy to test.

## Domain Rules

- Preserve API and SSE payload handling with backend schema changes.
- Keep report stream, gate, stage, artifact, export, and error states
  deterministic.
- Keep upload, chat, graph-highlight, onboarding, settings, and report view
  flows covered when behavior changes.
- Avoid UI text or state that assumes real external services are always
  available.
- Do not leak uploaded document contents or generated report data into logs,
  mock snapshots, or committed files.
- Preserve accessibility-friendly controls and stable `data-testid` hooks used
  by tests unless tests are updated in the same change.
- Keep layout changes responsive and avoid overlapping text or controls.

## Verification

- For frontend changes, run the gates from
  `.github/instructions/frontend_quality_gates.instructions.md`.
- For behavior changes, run targeted Vitest or Playwright tests matching the
  touched user flow.
- For backend contract changes, update `frontend/src/types`, API parsing, and
  tests together.
