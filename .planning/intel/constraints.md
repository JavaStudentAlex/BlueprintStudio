# Constraint Intel

## Security And Sensitive Data

- Do not expose, print, commit, or transform secret values.
- Do not commit uploaded construction documents, generated reports, SQLite
  runtime state, report exports, Playwright artifacts, local caches, or secrets.
- Do not commit large YOLO weights, customer drawings, generated overlay images,
  or external raw source drawings without explicit approval.

## Testing

- Backend tests should use `FakeKB`, `ScriptedChatModel`, in-memory SQLite,
  mocks, fixtures, or fakes.
- Default tests must not call real LLMs, Ollama, Postgres, paid APIs,
  standards sites, government sites, or third-party services.
- Behavior changes require targeted deterministic checks for the touched
  subsystem.

## API And Persistence

- Preserve backend schemas, frontend type contracts, SSE event handling, thread
  IDs, checkpointer behavior, and history replay unless updated together.
- Keep ingestion validation explicit: filename, extension, size, hash,
  classification, deduplication, and safe storage path.
- Keep report export paths rooted under configured export directories and
  validate download paths before returning files.

## Product And Compliance

- Do not use LLM output as the compliance source of truth.
- Compliance rules require source provenance, human-reviewed normalization, and
  deterministic execution.
- Candidate fixes require evidence, confidence, provenance, and human approval
  before write-back.

## Autonomous Work

- One task ID per PR.
- Bounded allowed paths.
- No opportunistic refactors.
- No workflow, secret, deployment, auto-merge, publish, or external-service
  changes without explicit user approval.
- High and critical risk tasks require human review before implementation.

