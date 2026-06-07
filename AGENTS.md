@/home/jovyan/.codex/RTK.md

# AGENTS.md

## Purpose: Repository Contract and LLM Guidance for BlueprintStudio

This file is the repository-local instruction surface for agent-based work in
this project. It complements the runtime contract and focuses on the parts that
are specific to BlueprintStudio.

## Task Direction Source Priority

Before selecting or implementing development work, read these files in order:

1. `agent_tasks.json`
2. `docs/product_direction.md`
3. `docs/jules_autonomous_loop.md`
4. `docs/flowdraft_integration_research.md`
5. `docs/codex_worker_plan.md`
6. `backlog.md`
7. `docs/ideas.md`

Use `agent_tasks.json` as the machine-readable source of truth for autonomous
Jules/Codex work. Markdown backlog and idea files are human-readable planning
surfaces and should be converted into explicit task entries before
implementation.

## Project Overview

BlueprintStudio is a construction-analysis application pairing an IDE-style
Next.js shell with a LangGraph-powered FastAPI backend. Uploaded construction
documents flow through an ingestion pipeline into a knowledge-base abstraction
backed by MemoryPalace, PostgreSQL, pgvector, and Ollama in production-like
local runs. SQLite-backed registries and LangGraph checkpoints keep uploads,
reports, and conversations durable.

The project includes:

- document upload, validation, classification, parsing, and registry storage
- MemoryPalace and fake knowledge-base adapters
- LangGraph chat orchestration, streaming SSE responses, and SQLite thread
  checkpointing
- report-session orchestration with inventory, planning, retrieval, drafting,
  validation gates, and PDF export
- a Next.js App Router frontend with onboarding, file tree, graph, preview,
  chat, report, profile, and settings surfaces
- backend pytest suites, frontend Vitest/RTL/MSW suites, Playwright e2e tests,
  and curl-based smoke checks

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, FastAPI, LangGraph, LangChain, pydantic-settings, sse-starlette |
| Knowledge base | MemoryPalace with PostgreSQL 16, pgvector, and Ollama; FakeKB under tests |
| Persistence | SQLite document registry, LangGraph checkpointer, report-session store |
| Frontend | Next.js 14 App Router, React 18, TypeScript, Tailwind, Zustand, Framer Motion |
| Testing | pytest, httpx, respx, Vitest, React Testing Library, MSW, Playwright |
| Linting and formatting | Ruff, mypy, Next lint, TypeScript |
| CI | GitHub Actions for backend and frontend lint, typecheck, tests, and build |

## CLI Guidance

- Use `rtk` before shell commands in this environment.
- Backend commands run from `backend` or use `uv --directory backend ...`.
- Frontend commands run from `frontend` or use `npm --prefix frontend ...`.
- Use the existing package managers: `uv` for backend and `npm` for frontend.
- Do not introduce alternate formatters, linters, or package managers unless the
  repository explicitly changes.
- Do not commit generated document data, SQLite runtime state, uploaded files,
  report exports, Playwright artifacts, local caches, or secrets.

Common local checks:

```bash
rtk uv --directory backend run --extra dev ruff format --check app tests
rtk uv --directory backend run --extra dev ruff check app tests
rtk uv --directory backend run --extra dev mypy app
rtk uv --directory backend run --extra dev pytest -q
rtk npm --prefix frontend run lint
rtk npm --prefix frontend exec -- tsc --noEmit
rtk npm --prefix frontend test
rtk npm --prefix frontend run build
```

## Project Structure and Boundaries

- Keep backend application code under `backend/app`.
- Keep backend tests under `backend/tests`, grouped into `unit`,
  `integration`, and `e2e`.
- Keep frontend application code under `frontend/src`.
- Keep frontend tests under `frontend/tests`, grouped into `unit` and `e2e`.
- Keep operational scripts under `scripts` and Makefile targets at the repo
  root.
- Keep generated data under ignored paths such as `backend/data/`.

Backend boundaries:

- `backend/app/api`: FastAPI route modules for chat, health, ingest, reports,
  and threads.
- `backend/app/agent`: LLM selection and LangGraph checkpoint wiring.
- `backend/app/kb`: knowledge-base interface, fake implementation, and
  MemoryPalace adapter.
- `backend/app/services`: ingestion, registry, report sessions, report
  pipeline, drafting, validation, and export services.
- `backend/app/schemas.py`: shared API payload contracts used by backend and
  frontend clients.

Frontend boundaries:

- `frontend/src/app`: Next.js App Router entry points and API proxy routes.
- `frontend/src/components`: domain UI for shell, chat, reports, files, graph,
  preview, onboarding, profile, and settings.
- `frontend/src/lib`: API client, store, mock data, and frontend utilities.
- `frontend/src/types`: TypeScript contracts that mirror backend API payloads.

## Domain Contracts

- Treat uploaded document content, generated reports, and SQLite state as
  sensitive local runtime data. Do not expose or commit it.
- Preserve API schemas shared across backend routes, frontend client parsing,
  SSE event handling, and tests.
- Keep chat and report SSE payloads backward-compatible unless the frontend and
  tests are updated in the same change.
- Keep LangGraph thread IDs, checkpointer behavior, and history replay stable.
- Keep ingestion validation explicit: filename, extension, size, content hash,
  classification, deduplication, and safe storage path.
- Keep MemoryPalace optional at test time. Tests should use `FakeKB`,
  `ScriptedChatModel`, in-memory SQLite, mocks, or fakes instead of real LLM,
  Ollama, Postgres, or third-party calls.
- Keep report pipeline gates explicit. Do not skip human-in-the-loop template or
  validation gates unless the product contract intentionally changes.
- Keep export paths rooted under configured export directories and validate
  download paths before returning files.
- Keep frontend state transitions deterministic and covered when changing
  upload, chat, graph, report, settings, or onboarding behavior.

## Verification and Quality Gates

- Prefer the lightest verification that proves the change.
- For backend Python changes, run the gates from
  `.github/instructions/python_quality_gates.instructions.md`.
- For frontend TypeScript or UI changes, run the gates from
  `.github/instructions/frontend_quality_gates.instructions.md`.
- For behavior changes, run targeted tests for the touched subsystem.
- For cross-stack API changes, update backend schemas/routes, frontend types/API
  parsing, and tests together.
- Do not claim verification that did not run in the current session.
- If a full gate is blocked by missing services or optional dependencies, report
  the block explicitly and run the closest deterministic checks available.

## Instruction Map

- Behavioral overlay: `.github/instructions/code_writing_behavior.instructions.md`
- Backend conventions: `.github/instructions/backend_app.instructions.md`
- Frontend conventions: `.github/instructions/frontend_app.instructions.md`
- Test conventions: `.github/instructions/tests.instructions.md`
- Backend quality gates: `.github/instructions/python_quality_gates.instructions.md`
- Frontend quality gates: `.github/instructions/frontend_quality_gates.instructions.md`
- Delegation policy: `.github/instructions/delegation_policy.instructions.md`
- Agent maintenance workflow: `.github/instructions/agent_maintenance_workflow.instructions.md`
- Read-only QA overlay: `.github/instructions/qa_readonly.instructions.md`

## Custom Agents

- Backend engineering: `.github/agents/backend-engineer.agent.md`
- Frontend engineering: `.github/agents/frontend-engineer.agent.md`
- Report pipeline engineering: `.github/agents/report-pipeline-engineer.agent.md`
- Testing and verification: `.github/agents/test-engineer.agent.md`
- Code review: `.github/agents/code-reviewer.agent.md`
- Documentation maintenance: `.github/agents/docs-maintainer.agent.md`

## Project Skills

- Backend contract checks: `.github/skills/backend-contract-check/SKILL.md`
- Python linting: `.github/skills/python-linting/SKILL.md`
- Python testing: `.github/skills/python-testing/SKILL.md`
- Frontend linting: `.github/skills/frontend-linting/SKILL.md`
- Frontend testing: `.github/skills/frontend-testing/SKILL.md`
- Reusable imported skills: `.agents/skills/`

## Planning Surfaces

- Machine-readable task queue: `agent_tasks.json`
- Human-readable backlog: `backlog.md`
- Product and architecture direction: `docs/product_direction.md`
- FlowDraft integration research: `docs/flowdraft_integration_research.md`
- Autonomous Jules loop: `docs/jules_autonomous_loop.md`
- Codex/Jules worker plan: `docs/codex_worker_plan.md`
- Raw idea intake: `docs/ideas.md`

## Mandatory Guardrails

1. Treat `AGENTS.md` as the base repository contract for this project.
2. Load the relevant `.github/instructions/*.instructions.md` files for the
   task scope before making changes.
3. Preserve backend, frontend, API, SSE, persistence, and sensitive-data
   contracts with tests when behavior changes.
4. Never expose, print, commit, or transform secret values. Workflows may
   reference secret names only.
5. Never commit, push, publish, trigger external service actions, or merge from
   an agent session unless the user explicitly asks and confirms.
6. Double-check that the final report matches the actual edits, verification,
   and remaining risks.
