# Source Migration

**Date:** 2026-06-07  
**Purpose:** Track how the previous Jules/Codex planning files were transferred
into GSD `.planning/` documentation and then removed as active repository
surfaces.

## Source Files

| Legacy source | GSD destination |
|---------------|-----------------|
| `agent_tasks.json` | `.planning/todos/AGENT-TASKS.md`, `.planning/ROADMAP.md`, `.planning/STATE.md` |
| `docs/product_direction.md` | `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/intel/context.md` |
| `docs/flowdraft_integration_research.md` | `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/intel/context.md` |
| `docs/jules_autonomous_loop.md` | `.planning/STATE.md`, `.planning/config.json` |
| `docs/codex_worker_plan.md` | `.planning/STATE.md`, `.planning/todos/AGENT-TASKS.md` |
| `backlog.md` | `.planning/ROADMAP.md`, `.planning/REQUIREMENTS.md`, `.planning/todos/AGENT-TASKS.md` |
| `docs/ideas.md` | `.planning/seeds/SEED-001-team-direction.md`, `.planning/ROADMAP.md` |

## Migration Rules

- Treat `.planning/` as the first planning entry point for future work.
- Do not recreate legacy Jules planning files, task manifests, or validators.
- Retained Jules workflows must behave as GSD-compatible bridges over
  `.planning/`.
- When task status changes, update `.planning/todos/AGENT-TASKS.md` and the
  relevant roadmap/requirements state.
- If a future source contradicts a locked decision in `.planning/PROJECT.md`,
  record the conflict before changing roadmap or requirements.

## Integrity Notes

- The initial migration was additive; the follow-up cleanup removed stale
  legacy Jules/Codex files and converted Jules automation to GSD-compatible
  workflow bridges.
- Application code was not changed.
- No generated runtime data, uploaded documents, report exports, secrets, model
  weights, or external assets were added.

## Automation Bridges

| Legacy behavior | GSD-compatible replacement |
|-----------------|----------------------------|
| Select next task from `agent_tasks.json` | Select next safe task from `.planning/todos/AGENT-TASKS.md` with `scripts/gsd_task_bridge.py` |
| Trigger Jules with legacy planning docs | Trigger Jules with `AGENTS.md`, `.planning/`, and GSD workflow instructions |
| Auto-merge Jules PRs after validation | Retain automerge, adding GSD task queue validation and legacy-surface guardrails |
