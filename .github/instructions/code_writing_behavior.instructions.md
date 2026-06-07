---
description: "Behavioral overlay for code writing, review, and refactor tasks."
---

# Code Writing Behavior

## Purpose

This file defines the expected engineering behavior for day-to-day work in this
repository.

Use it when a task involves:

- writing or editing code
- reviewing code
- refactoring or cleanup work
- changing API contracts, UI behavior, tests, docs, or tooling

## Core Behavior

- Make assumptions explicit when product behavior, API schemas, persistence,
  security, or external-service availability affects the result.
- Prefer the smallest correct change. Do not add speculative abstractions.
- Keep edits surgical and grounded in the current repo layout.
- Match local style and existing patterns unless a scoped instruction says
  otherwise.
- If you notice unrelated issues, call them out separately instead of widening
  the change set.
- Preserve backend route contracts, frontend type contracts, and SSE event
  shapes unless a task explicitly requires a coordinated breaking change.
- Keep deterministic domain logic separate from route handlers, filesystem
  writes, network calls, and UI rendering concerns where practical.

## Execution Pattern

Before implementing:

- state working assumptions when they materially affect the solution
- identify the simplest viable approach
- define what will verify success

During implementation:

- touch only the files and code paths needed for the task
- remove imports, helpers, and dependencies made unused by your own changes
- preserve test seams and deterministic fixtures
- keep ad hoc debugging separate from reusable logic
- avoid hardcoded local paths, service URLs, credentials, or machine-specific
  settings

Before completion:

- verify the claimed outcome with the lightest sufficient evidence
- report open questions, constraints, service assumptions, or blocked gates
  explicitly
- keep the final summary aligned with the files actually changed

## Stack-Specific Work

- For backend API, LangGraph, MemoryPalace, ingestion, persistence, report
  pipeline, or export changes, load
  `.github/instructions/backend_app.instructions.md`.
- For frontend Next.js, React, Zustand, UI, API client, or TypeScript changes,
  load `.github/instructions/frontend_app.instructions.md`.
- For tests or verification work, load `.github/instructions/tests.instructions.md`
  and the relevant quality-gate instruction file.
