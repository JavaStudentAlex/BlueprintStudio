# Codex Worker Plan

## Purpose

Codex should work as a disciplined coding worker for BlueprintStudio. It should
use `AGENTS.md`, `agent_tasks.json`, and the project docs to select narrow work,
implement it, verify it, and report honestly.

## Surfaces

### 1. Repository Instructions

`AGENTS.md` is the base contract. Codex must load it first.

### 2. Task Manifest

`agent_tasks.json` is the machine-readable queue. It defines:

- source priority
- risk levels
- replenishment policy
- autonomous loop policy
- task status
- allowed paths
- acceptance criteria

### 3. Validation Command

Use the stdlib validator:

```bash
rtk python scripts/validate_agent_tasks.py agent_tasks.json
```

### 4. Planning Docs

Use these for context and task generation:

- `docs/product_direction.md`
- `docs/flowdraft_integration_research.md`
- `docs/jules_autonomous_loop.md`
- `backlog.md`
- `docs/ideas.md`

## Operating Rules

- Pick one task ID per change.
- Stay within `allowed_paths`.
- Add or update tests when behavior changes.
- Never call real external LLMs, standards sites, government sites, or paid APIs
  from tests.
- Use fixtures and fakes for parser, compliance, graph, and RAG behavior.
- Do not change workflows, secrets, auto-merge, or deployment files unless the
  selected task explicitly allows it.
- Report commands that actually ran.

## Recommended Worker Flow

```text
validate manifest
  -> inspect next todo task
  -> read relevant docs
  -> inspect current code
  -> implement narrow change
  -> run targeted checks
  -> update task manifest
  -> summarize changed files and verification
```

## Future CLI

A future task should add a local bridge like:

```bash
rtk python -m backend.app.agent_tasks validate
rtk python -m backend.app.agent_tasks status
rtk python -m backend.app.agent_tasks next-task
rtk python -m backend.app.agent_tasks render-prompt
```

Until then, use `scripts/validate_agent_tasks.py` and inspect
`agent_tasks.json` directly.
