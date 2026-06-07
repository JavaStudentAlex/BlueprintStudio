---
description: "Read-only review overlay for analysis, QA, and code review tasks."
---

# Read-Only QA Instructions

## Purpose

Use this when the task is to inspect, review, audit, or explain without making
changes.

## Rules

- Do not edit files unless the user explicitly changes the task to
  implementation.
- Ground findings in repository evidence: files, tests, commands, and observed
  behavior.
- Distinguish confirmed issues from hypotheses.
- Prioritize findings by severity and likelihood.
- Call out missing verification and untested behavior explicitly.
- For backend concerns, name the affected contract: API schema, SSE payload,
  upload validation, persistence, report pipeline, export path, checkpointer, or
  knowledge-base adapter.
- For frontend concerns, name the affected contract: API parsing, state
  transition, UI flow, accessibility, responsive layout, or test hook.
- Avoid broad style commentary unless it creates a maintainability or
  correctness risk.

## Output Shape

Prefer:

1. Findings ordered by severity.
2. Evidence and affected path for each finding.
3. Suggested fix or next verification step.
4. Open questions or limitations.

If no issues are found, state what was reviewed and what verification was or
was not performed.
