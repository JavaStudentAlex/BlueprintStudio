---
name: backend-contract-check
description: Review BlueprintStudio backend changes for API, SSE, upload, persistence, report pipeline, export, and external-service contract risks. Use before completing backend or cross-stack changes.
---

# Backend Contract Check Skill

Use this skill when a change touches backend routes, schemas, ingestion,
knowledge-base adapters, LangGraph chat, threads, report sessions, report
pipeline, exports, or frontend contracts that consume backend data.

## Checkpoints

Ask whether the change affects any of these contracts:

- API request and response model shapes.
- SSE event type names, payload fields, and stream completion behavior.
- Upload validation: filename, extension, size, content hash, deduplication, and
  storage path.
- Document registry states and failure modes.
- Knowledge-base interface behavior and fake implementation parity.
- LangGraph thread IDs, checkpoint persistence, and history replay.
- Report-session status, stage order, gate lifecycle, validation findings,
  artifacts, logs, and exports.
- Safe file path handling for generated reports and downloads.
- Frontend TypeScript types, API client parsing, and store transitions.
- Default-test isolation from real LLM, Ollama, Postgres, Jules, GitHub, or
  third-party APIs.

## Verification Pattern

1. Find the closest existing tests for the affected contract.
2. Add or update the narrowest deterministic regression test if needed.
3. Run the targeted backend and, for cross-stack changes, frontend tests.
4. Run Ruff, mypy, and relevant frontend checks for touched paths.
5. State any unverified service assumptions explicitly.

## Guardrails

- Do not weaken upload, path, or secret handling to make a test pass.
- Do not hide external-service or pipeline failures behind broad exception
  handling without preserving diagnostic context.
- Do not rely on real external services for the only proof of correctness.
