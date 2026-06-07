# Jules Autonomous Improvement Loop

## Goal

Jules should continuously improve BlueprintStudio without asking for the next
task when safe work is available.

```text
read AGENTS.md
  -> inspect agent_tasks.json
  -> replenish task queue when low
  -> select one safe task
  -> implement one focused change
  -> run relevant checks
  -> update task status
  -> open one PR
  -> wait for CI and merge
  -> continue with next task
```

## Task Sources

Priority:

1. `agent_tasks.json`
2. `AGENTS.md`
3. CI failures
4. `docs/product_direction.md`
5. `docs/flowdraft_integration_research.md`
6. `docs/codex_worker_plan.md`
7. `backlog.md`
8. `docs/ideas.md`
9. TODO/FIXME comments
10. recurring errors from previous PRs

## Main Rule

Do not ask the user what to do next while safe low-risk or medium-risk tasks can
be selected or generated from:

- the task manifest
- product direction docs
- FlowDraft integration gaps
- failing tests or CI
- explicit TODO comments
- repeated errors
- narrow missing test coverage

Ask the user only for:

- high-risk or critical-risk changes
- secrets, credentials, or paid service access
- workflow, auto-merge, or deployment changes
- ambiguous product direction
- destructive operations

## Replenishment Policy

Maintain at least `minimum_todo_tasks` tasks in `agent_tasks.json`.

When the todo pool is low:

1. Do not start random refactoring.
2. Scan existing done and blocked tasks.
3. Scan product direction and research docs.
4. Add a small batch of low-risk or medium-risk tasks.
5. Every task must include:
   - stable `id`
   - `status`
   - `area`
   - `risk`
   - `title`
   - `description`
   - `allowed_paths`
   - `acceptance`
6. Do not recreate already implemented work.
7. Prefer stabilization, graph contracts, validation, fixtures, and tests before
   large parser or editor features.

## Selection Rule

Pick the first `todo` task that is not blocked by high or critical risk.

Before implementation, verify:

- the task is small enough for one PR
- the `allowed_paths` are narrow
- acceptance criteria are testable
- no active claim from another worker exists
- the change does not require secrets or live external services

If the first task is too large:

1. Leave it as `todo` or mark it `blocked` with a reason.
2. Create smaller prerequisite tasks before it.
3. Select the first safe prerequisite.

## Risk Gates

Autonomous work is allowed for:

- docs and planning surfaces
- task manifest updates
- validators and fixtures
- pure backend services with tests
- frontend components with deterministic tests
- compliance rule models and fake data
- parser adapters that do not call external services in tests

Human review is required for:

- `.github/workflows/**`
- secrets and env handling
- deployment files
- dependency manifest changes
- sandbox or code execution policy
- external scraping against real sites
- live external LLM/provider integration
- auto-merge behavior
- destructive file operations

## Stabilization First

Before large model/parser/editor work, stabilize:

- task manifest validation
- graph schema and fixtures
- parser output contracts
- provenance model
- deterministic compliance runner
- test fakes for all external systems
- frontend graph inspection flow

## Failure Loop

If CI or local checks fail:

1. Do not start a new feature.
2. Create or select a fix task for the failure.
3. Keep the diff limited to the failure area.
4. Add a regression test if the failure exposed missing coverage.
5. Add a lesson or guardrail when the same failure recurs.

## PR Shape

Each PR should have:

- one task ID
- bounded file scope
- no opportunistic refactors
- no unrelated backlog churn
- tests or explicit docs-only rationale
- exact validation commands in the PR body

## Done Criteria

A task is done only when:

- implementation stays within `allowed_paths`
- acceptance criteria are met or explicitly updated
- relevant checks ran or blockers are documented
- task status is updated
- new discovered work is added as a task or backlog item
