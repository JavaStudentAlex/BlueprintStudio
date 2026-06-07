# State: BlueprintStudio

**Initialized:** 2026-06-07  
**Last updated:** 2026-06-07 after Jules API key cleanup  
**Project reference:** `.planning/PROJECT.md`

## Current Status

BlueprintStudio now has a GSD `.planning/` structure that replaces the prior
Jules/Codex planning files. Jules next-task and automerge workflows remain
available as GSD-compatible automation bridges.

Agent PR creation guidance now requires `.github/PULL_REQUEST_TEMPLATE.md` to
be used as the main pull request description template.

Jules task creation now uses `JULES_API_KEY` as the only supported API key
secret name; the previous secondary-key fallback has been removed from the
workflow.

The migration retained the substance of:

- product direction
- FlowDraft and CrashPine research
- autonomous worker policy
- GSD-compatible Jules automation policy
- human backlog
- raw ideas
- task queue details

## Current Focus

Primary planning surface cleanup is complete. The next implementation work
should be selected from `.planning/todos/AGENT-TASKS.md`.

Following the GSD task queue, the first safe pending task is:

- `flowdraft-golden-demo-frontend` - Add frontend golden demo workflow.

If the user wants strict GSD phase execution instead of manifest-order task
selection, run:

```text
$gsd-plan-phase 8
```

Phase 8 contains the current golden-demo packaging work.

## Worker Policy

Use this selection policy for autonomous work:

1. Read `AGENTS.md`.
2. Read `.planning/STATE.md`, `.planning/PROJECT.md`,
   `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, and
   `.planning/todos/AGENT-TASKS.md`.
3. Select the first `todo` task that is not blocked by high or critical risk.
4. If the first task is too large, keep it pending and create smaller
   prerequisites.
5. Implement one focused change.
6. Run the lightest deterministic checks that prove the change.
7. Update the GSD planning files and task state when relevant.
8. Do not commit, push, publish, merge, or trigger external services unless the
   user explicitly asks and confirms.

## Replenishment Policy

- Maintain at least 5 todo tasks.
- Add tasks only when the todo pool drops below the minimum.
- Add batches of 5 when replenishing.
- Generated tasks may be low or medium risk by default.
- Prefer stabilization, graph contracts, validation, fixtures, and tests before
  large parser/editor features.

## Risk Policy

| Risk | Handling |
|------|----------|
| Low | Safe for autonomous implementation with relevant checks. |
| Medium | Safe for autonomous implementation with relevant checks and review. |
| High | Human review required before implementation. |
| Critical | Manual-only. |

## Safety Gates

Ask the user before:

- High-risk or critical-risk changes.
- Secrets, credentials, paid services, or live external service access.
- Workflow, auto-merge, deployment, publish, or CI policy changes.
- Destructive operations.
- Ambiguous product direction.

## Verification Memory

No application code was changed during this migration. Verification for the
migration should check:

- `.planning/` exists.
- Root GSD files exist.
- GSD task index exists.
- Legacy Jules planning files and task manifests are absent.
- Jules workflows exist only as GSD-compatible bridges.
- `AGENTS.md` points future agents only to `.planning/`.

## Source Of Truth

Primary GSD files:

- `.planning/PROJECT.md`
- `.planning/REQUIREMENTS.md`
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.planning/todos/AGENT-TASKS.md`

Removed legacy sources:

- `agent_tasks.json`
- `backlog.md`
- `docs/product_direction.md`
- `docs/flowdraft_integration_research.md`
- `docs/jules_autonomous_loop.md`
- `docs/codex_worker_plan.md`
- `docs/ideas.md`
- `scripts/validate_agent_tasks.py`

Retained GSD-compatible automation bridges:

- `.github/workflows/jules_automerge.yml`
- `.github/workflows/jules_next_task.yml`
- `scripts/gsd_task_bridge.py`
