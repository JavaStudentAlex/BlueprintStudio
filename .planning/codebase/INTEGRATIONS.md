---
analysis_date: 2026-06-07
last_mapped_commit: b7a5fca729d82fd6d25707deb6edc1356f008624
---

# External Integrations

**Analysis Date:** 2026-06-07

## APIs & External Services

- `OpenAI API` - Used for the chat LLM when `LLM_PROVIDER=openai` in `backend/app/agent/llm.py`, and for optional visual document enrichment when `document_analysis_enabled=true` in `backend/app/services/document_analysis.py`; SDKs: `langchain-openai` `ChatOpenAI` plus the direct `openai` SDK import; auth via `OPENAI_API_KEY` for chat and `DOCUMENT_ANALYSIS_API_KEY` for enrichment; the enrichment path uses `chat.completions.parse(...)` with a strict output schema.
- `Ollama` - Used as the alternate chat LLM provider and as the embedding/LLM backend for MemoryPalace; SDKs: `langchain-ollama` `ChatOllama` plus `httpx` health probes in `backend/app/kb/memorypalace.py` and `backend/app/api/health.py`; auth is none; key env vars are `OLLAMA_HOST`, `OLLAMA_MODEL`, `MEMORY_PALACE_LLM_MODEL`, and `MEMORY_PALACE_EMBEDDING_MODEL`; the runtime target is the local `ollama/ollama` container in `docker-compose.yml`.
- `MemoryPalace` - Used as the long-term knowledge-base layer for recall and remember operations; client: the `memory_palace` Python package installed from `git+https://github.com/jeffpierce/memory-palace.git@main` in `backend/Dockerfile` and imported in `backend/app/kb/memorypalace.py`; connection/config comes from `MEMORY_PALACE_DATABASE_URL`, `OLLAMA_HOST`, and `MEMORY_PALACE_INSTANCE_ID`; the adapter calls `remember()` and `recall()` and bootstraps the schema on startup.

## Data Storage

- `PostgreSQL 16 + pgvector` - Primary external database for MemoryPalace; container image: `pgvector/pgvector:pg16` in `docker-compose.yml`; clients: `asyncpg`, `psycopg2-binary`, `psycopg[binary]`, and `pgvector`; connection env var: `MEMORY_PALACE_DATABASE_URL`; `make pg-index` creates the HNSW index on `memories.embedding`.
- `SQLite` - Local durable stores owned by the app; `CHECKPOINT_DB_PATH` in `backend/app/agent/checkpointer.py`, `REGISTRY_DB_PATH` in `backend/app/services/document_registry.py`, `REPORT_SESSIONS_DB_PATH` in `backend/app/services/report_sessions.py`, and `GRAPH_ARTIFACTS_DB_PATH` in `backend/app/services/graph_artifacts.py` all use stdlib `sqlite3`, while LangGraph uses `langgraph-checkpoint-sqlite`.
- `Local file storage` - Uploaded docs, exports, and converter outputs live under ignored paths such as `backend/data/documents`, `backend/data/exports`, and `backend/data/conversions`; these are configured by `DOCUMENTS_DIR`, `REPORT_EXPORTS_DIR`, and `ENGINEERING_CONVERTER_OUTPUT_DIR`.

## Authentication & Identity

- No auth provider, OAuth, JWT, or SSO integration was found in the current repo scan.
- Service credentials are limited to API keys in env vars such as `OPENAI_API_KEY` and `DOCUMENT_ANALYSIS_API_KEY`; there is no end-user auth flow or token storage code in the current state.

## Monitoring & Observability

- Health checks are implemented in `backend/app/api/health.py` and exposed to the browser through `frontend/src/app/api/health/route.ts`; Docker healthchecks are also defined in `backend/Dockerfile`, `frontend/Dockerfile`, and `docker-compose.yml`.
- No dedicated external error-tracking or analytics service was found in the current repo scan.

## CI/CD & Deployment

- `Docker Compose` - Full-stack local orchestration with `postgres`, `ollama`, `backend`, and `frontend` services in `docker-compose.yml`.
- `GitHub Actions` - The repository keeps `.github/workflows/ci.yml` for CI and `.github/workflows/jules_next_task.yml` plus `.github/workflows/jules_automerge.yml` for Jules automation. The Jules workflows are GSD-compatible bridges over `.planning/`, not product-runtime dependencies.

## Environment Configuration

- Development uses `.env.example`, `backend/.env.example`, and `frontend/.env.example`; the key knobs are `LLM_PROVIDER`, `OPENAI_API_KEY`, `DOCUMENT_ANALYSIS_ENABLED`, `OLLAMA_HOST`, `MEMORY_PALACE_DATABASE_URL`, `KB_BACKEND`, and `NEXT_PUBLIC_BACKEND_URL`.
- `KB_BACKEND=fake` is the deterministic no-external-services mode for tests and local smoke runs.
- No separate cloud secret manager or hosted deployment target is configured in repo.

## Webhooks & Callbacks

- Incoming webhooks: none found in the current repo scan.
- Outgoing webhooks: none found in the current repo scan.

## Reference-Only External Sources

- `backend/tests/fixtures/flowdraft/PROVENANCE.md` and `frontend/tests/fixtures/flowdraft/PROVENANCE.md` point at FlowDraft source URLs, but the runtime does not call FlowDraft or CrashPine services.
- `backend/app/services/property_valuation.py` uses an in-repo Hong Kong demo dataset, not a live market API.
- `backend/app/services/standards_catalog.py` embeds official standard URLs as catalog metadata, but there is no live standards scraper or standards API path in the current runtime.

*Integration audit: 2026-06-07*
*Update when adding/removing external services*
