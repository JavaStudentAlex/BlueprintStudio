---
analysis_date: 2026-06-07
last_mapped_commit: b7a5fca729d82fd6d25707deb6edc1356f008624
---

# Technology Stack

**Analysis Date:** 2026-06-07

## Languages

**Primary:**
- Python 3.12 for the backend runtime in `backend/app/*`; `backend/Dockerfile` pins `python:3.12-slim`, and `backend/pyproject.toml` allows `>=3.11,<3.13`.
- TypeScript 5.6.x for the frontend app in `frontend/src/*`, the test suite in `frontend/tests/*`, and shared contracts in `frontend/src/types/index.ts`.

**Secondary:**
- Bash/Shell for orchestration and smoke tooling in `Makefile`, `scripts/smoke.sh`, and `scripts/smoke_cad_converter.py`.
- JSON, YAML, and Markdown for config, fixtures, and planning docs in `docker-compose.yml`, `.env.example`, `backend/.env.example`, `frontend/.env.example`, and `.planning/*`.

## Runtime

**Environment:**
- Backend runs as a Python container from `backend/Dockerfile`; local development and checks use `uv --directory backend ...` and `rtk uv --directory backend ...`.
- Frontend runs as a Node.js 20 container from `frontend/Dockerfile`; local development uses `npm --prefix frontend ...`.
- Docker Compose is the default full-stack runtime in `docker-compose.yml`, with `Makefile` targets such as `make up`, `make test`, `make smoke`, and `make e2e`.

**Package Manager:**
- Python dependency resolution uses `uv` with `backend/uv.lock`.
- Frontend dependency resolution uses `npm` with `frontend/package-lock.json`.

## Frameworks

**Core:**
- FastAPI - HTTP API server and router composition in `backend/app/main.py` and `backend/app/api/*`.
- LangGraph - agent graph, tool loop, and checkpoint wiring in `backend/app/agent/graph.py` and `backend/app/agent/checkpointer.py`.
- LangChain - chat model abstraction and tool binding in `backend/app/agent/llm.py` and `backend/app/agent/tools.py`.
- Next.js 14.2.35 - App Router frontend in `frontend/src/app/*` plus the local health route in `frontend/src/app/api/health/route.ts`.
- React 18.3.1 - UI components in `frontend/src/components/*`.
- Tailwind CSS 3.4.x - styling configured in `frontend/tailwind.config.ts` and `frontend/src/app/globals.css`.
- Zustand - client state in `frontend/src/lib/store.ts`.
- Framer Motion - animated UI surfaces in `frontend/src/components/*`.
- sse-starlette - SSE chat and report streams in `backend/app/api/chat.py` and `backend/app/api/reports.py`.

**Testing:**
- pytest, pytest-asyncio, respx, and httpx for backend unit and integration tests in `backend/tests/*`.
- Vitest, React Testing Library, MSW, and jsdom for frontend unit tests in `frontend/tests/unit/*`.
- Playwright for browser E2E in `frontend/tests/e2e/*`.

**Build/Dev:**
- Uvicorn serves the backend app from `backend/app/main.py`.
- `next build`, `next lint`, and the TypeScript compiler drive the frontend build and typecheck path.
- Ruff and mypy are the Python lint and type gates from `backend/pyproject.toml`.
- ReportLab, `pypdf`, `python-docx`, `openpyxl`, and Pillow support document parsing, PDF export, and overlay utilities in `backend/app/services/*` and `backend/app/api/ingest.py`.

## Key Dependencies

**Critical:**
- `fastapi` - backend HTTP surface and router composition.
- `langgraph` and `langgraph-checkpoint-sqlite` - agent execution and persistent thread history.
- `langchain-openai` and `langchain-ollama` - chat provider adapters selected in `backend/app/agent/llm.py`.
- `memory_palace` - long-term KB layer installed from GitHub in `backend/Dockerfile` and used in `backend/app/kb/memorypalace.py`.
- `pgvector`, `asyncpg`, `psycopg2-binary`, and `psycopg[binary]` - MemoryPalace database access and readiness probes.
- `reportlab` and `Pillow` - PDF export and image overlay rendering.
- `pypdf`, `python-docx`, and `openpyxl` - document ingestion and extraction.
- `react`, `next`, `zustand`, and `framer-motion` - frontend shell, state, and motion.

**Infrastructure:**
- `pydantic` and `pydantic-settings` - schemas and env-driven configuration.
- `httpx` - Ollama and health probes.
- `markdown-it-py`, `react-markdown`, and `remark-gfm` - markdown rendering and document parsing support.
- `python-multipart` - file upload handling for `backend/app/api/ingest.py`.
- `msw`, `@testing-library/*`, `vitest`, and `@playwright/test` - test harnesses.

## Configuration

**Environment:**
- Backend config is env-driven via `backend/app/config.py`, `.env.example`, and `backend/.env.example`.
- Core backend env vars: `LLM_PROVIDER`, `OPENAI_API_KEY`, `OPENAI_MODEL`, `DOCUMENT_ANALYSIS_ENABLED`, `DOCUMENT_ANALYSIS_API_KEY`, `OLLAMA_HOST`, `OLLAMA_MODEL`, `MEMORY_PALACE_DATABASE_URL`, `MEMORY_PALACE_EMBEDDING_MODEL`, `MEMORY_PALACE_LLM_MODEL`, `MEMORY_PALACE_INSTANCE_ID`, `CHECKPOINT_DB_PATH`, `REGISTRY_DB_PATH`, `REPORT_SESSIONS_DB_PATH`, `REPORT_EXPORTS_DIR`, `GRAPH_ARTIFACTS_DB_PATH`, `DOCUMENTS_DIR`, `ENGINEERING_CONVERTER_COMMAND_TEMPLATE`, `ENGINEERING_CONVERTER_TIMEOUT_SECONDS`, `ENGINEERING_CONVERTER_OUTPUT_DIR`, `ENGINEERING_CONVERTER_OUTPUT_EXTENSION`, `ENGINEERING_CONVERTER_SMOKE_INPUT_PATH`, and `KB_BACKEND`.
- Frontend config is primarily `NEXT_PUBLIC_BACKEND_URL` from `frontend/.env.example` and `docker-compose.yml`.
- `Makefile` is the canonical local command surface for `up`, `test`, `smoke`, `smoke-cad`, and `e2e`.

**Build:**
- Backend build and lock state live in `backend/pyproject.toml` and `backend/uv.lock`.
- Frontend build and lock state live in `frontend/package.json` and `frontend/package-lock.json`.
- Container and toolchain config lives in `backend/Dockerfile`, `frontend/Dockerfile`, `docker-compose.yml`, `frontend/next.config.mjs`, `frontend/tsconfig.json`, `frontend/vitest.config.ts`, `frontend/playwright.config.ts`, and `frontend/tailwind.config.ts`.

## Platform Requirements

**Development:**
- Docker and Docker Compose are required for the full stack.
- Python 3.12 and Node.js 20 are the native host runtimes if you run outside containers.
- `uv` and `npm` are the supported package managers.

**Production:**
- The repo currently targets containerized deployment: backend, frontend, Postgres, and Ollama in `docker-compose.yml`.
- No alternate cloud hosting target is configured in-repo.

*Stack analysis: 2026-06-07*
*Update after major dependency changes*
