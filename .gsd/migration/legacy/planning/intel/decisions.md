# Decision Intel

| Decision | Source | Rationale |
|----------|--------|-----------|
| Use GSD `.planning/` as the primary planning surface | User request on 2026-06-07 | The user prefers gsd-core structure over Jules-first planning files. |
| Replace legacy source planning files with GSD and keep Jules automation as GSD bridges | User correction on 2026-06-07 | The old planning surfaces must not compete with `.planning/`, but Jules next-task and automerge functionality must remain available. |
| Keep active work in `.planning/todos/AGENT-TASKS.md` | GSD migration cleanup | The GSD task queue replaces the removed JSON task manifest. |
| Keep MemoryPalace optional and not authoritative for engineering state | Product direction | Engineering graph state needs schema, provenance, validation, and deterministic rules. |
| Use deterministic rule engines for compliance | Product direction and compliance guardrails | LLMs may explain results, but should not decide pass/fail. |
| Absorb FlowDraft contracts behind existing services | FlowDraft research | BlueprintStudio already has a FastAPI backend and Next.js frontend. |
| Do not merge external tree-replacement branches | FlowDraft/CrashPine research | Replacements delete existing product structure and tests. |
| Keep parser engines optional and fixture-backed in tests | Parser direction | Default tests must not depend on model weights, paid APIs, or external services. |
| Require human approval for graph write-back | Agent direction | Physical and compliance-impacting changes need evidence and visible approval. |
| Do not commit docs automatically from this migration | Repository guardrail | The user did not ask for commits, and agent sessions must not commit unless explicitly requested. |
