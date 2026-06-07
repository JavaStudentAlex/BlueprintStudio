---
applyTo: "backend/**/*.py"
description: "Backend conventions, FastAPI/LangGraph contracts, and service boundaries for BlueprintStudio."
---

# Backend App Instructions

## Scope

This covers:

- `backend/app/**/*.py`
- `backend/tests/**/*.py` when tests exercise backend behavior
- `scripts/**/*.py` when scripts exercise backend services or smoke checks

## Tooling Rules

- Use `rtk uv --directory backend run --extra dev ...` from the repository root.
- Use `backend/pyproject.toml` and GitHub Actions as the source of truth for
  backend tools.
- Use Ruff for formatting and linting and mypy for backend type checking.
- Do not introduce another formatter, linter, or package manager without
  updating project configuration and CI.

## Architecture Rules

- Keep FastAPI route modules thin. Route handlers should validate request
  shape, call services, map errors, and return schemas.
- Keep reusable business logic in `backend/app/services`.
- Keep LLM selection, LangGraph checkpointing, and agent-specific wiring in
  `backend/app/agent`.
- Keep knowledge-base behavior behind `backend/app/kb/base.py`.
- Keep MemoryPalace-specific details in `backend/app/kb/memorypalace.py`.
- Keep tests independent from real LLM, Ollama, Postgres, or network calls
  unless an integration test is explicitly marked and skipped when unavailable.
- Prefer explicit dataclasses, pydantic models, typed dicts, or value objects
  when data shape matters.
- Avoid global mutable state except for existing settings caches that provide a
  test reset path.

## Domain Rules

- Preserve API schemas and status fields consumed by `frontend/src/lib/api.ts`
  and `frontend/src/types`.
- Preserve SSE event types and payload semantics for chat and report streams.
- Keep uploaded-file validation explicit: filename, extension, size, content
  hash, deduplication, classification, and storage path.
- Keep document and report output paths rooted under configured directories.
  Validate paths before reads, writes, and downloads.
- Keep report pipeline gates explicit and durable. Do not skip or auto-answer
  human-in-the-loop gates unless the product contract changes.
- Preserve report-session status transitions, stage IDs, artifact records,
  validation findings, export records, and log semantics.
- Keep fallback and fake modes deterministic for tests.
- Do not hide external-service failures behind broad exception handling without
  preserving diagnostic context.

## Verification

- For Python changes, run the gates from
  `.github/instructions/python_quality_gates.instructions.md`.
- For behavior changes, run targeted backend tests matching the changed
  subsystem.
- For cross-stack changes, run relevant frontend tests after updating frontend
  types and API parsing.
