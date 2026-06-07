---
description: "Policy for delegating work to specialized agents while preserving repository contracts."
---

# Delegation Policy

## Purpose

Use this when splitting work across specialized LLM agents or reviewing work
produced by another agent.

## Rules

- Every delegated agent must treat `AGENTS.md` as the base repository contract.
- Delegate self-contained work with clear inputs, expected outputs, and
  verification requirements.
- Do not ask one agent to make assumptions that another agent must later guess.
- Keep backend-heavy work with backend-aware agents, frontend-heavy work with
  frontend-aware agents, and review-heavy work with read-only reviewers.
- Parallelize independent exploration, review, and test-design tasks when the
  harness supports it.
- Synthesize delegated results before editing; do not blindly apply patches.
- Verify merged or adopted work in the current session before claiming it works.

## Good Delegation Targets

- Mapping an unfamiliar subsystem.
- Reviewing a risky diff for API, security, persistence, UI, or test
  regressions.
- Designing deterministic tests for a known behavior.
- Checking docs against actual commands and project layout.

## Poor Delegation Targets

- Tasks that require hidden user intent.
- Broad refactors without a narrow contract.
- External service actions, publishing, or secret management steps.
- Anything that would make an agent invent access to services, data, or secrets
  it does not have.
