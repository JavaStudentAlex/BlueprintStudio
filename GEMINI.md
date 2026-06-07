# GEMINI.md

@AGENTS.md

The file above is the repository-local contract for this project. Load it
first.

For code-writing, review, or refactor tasks, also load:

- `.github/instructions/code_writing_behavior.instructions.md`

For backend API, LangGraph, MemoryPalace, ingestion, persistence, report
pipeline, or export work, also load:

- `.github/instructions/backend_app.instructions.md`

For frontend Next.js, React, Zustand, UI, API client, or TypeScript work, also
load:

- `.github/instructions/frontend_app.instructions.md`

For test changes or verification work, also load:

- `.github/instructions/tests.instructions.md`
- `.github/instructions/python_quality_gates.instructions.md` when backend code
  is involved
- `.github/instructions/frontend_quality_gates.instructions.md` when frontend
  code is involved

For read-only analysis or review tasks, also load:

- `.github/instructions/qa_readonly.instructions.md`

## Tooling Rules

- Use `rtk` before shell commands in this environment.
- Use `uv --directory backend run --extra dev ...` for backend checks from the
  repo root.
- Use `npm --prefix frontend ...` for frontend checks from the repo root.
- Prefer targeted tests that match the touched subsystem before running the full
  suites.

## Completion Rule

Before finishing, re-check that:

- the reported verification actually ran in the current session
- any remaining gaps, service assumptions, or blocked gates are named
  explicitly
- docs and agent files stay aligned with the repository's current FastAPI,
  LangGraph, MemoryPalace, and Next.js stack
