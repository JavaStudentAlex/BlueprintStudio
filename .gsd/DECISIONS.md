# Decisions Register

<!-- Append-only. Never edit or remove existing rows.
     To reverse a decision, add a new row that supersedes it.
     Read this file at the start of any planning or research phase. -->

| # | When | Scope | Decision | Choice | Rationale | Revisable? | Made By |
|---|------|-------|----------|--------|-----------|------------|---------|
| D001 | M001/S03 plan-slice | architecture | How S03 ingestion progress should be surfaced during long-running parser and conversion work | Use a single-process in-memory IngestEventBus attached to FastAPI app state, emit typed ingest progress events from the ingestion pipeline, and expose those events through a backend SSE endpoint while background tasks update the SQLite document registry. | The current local development and test architecture already assumes a single backend process with SQLite registry state, and the report pipeline has an established SSE pattern that can be reused without introducing external brokers. This keeps S03 small while preserving a clear seam for a future durable queue if multi-process deployment becomes necessary. | Yes, when deployment requires multiple backend workers or durable cross-process event delivery. | agent |
