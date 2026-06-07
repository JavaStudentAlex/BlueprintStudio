---
description: "Workflow for keeping repository agent instructions aligned with the current codebase."
---

# Agent Maintenance Workflow

## Purpose

Use this when editing `AGENTS.md`, model wrappers, `.github/instructions`,
`.github/agents`, `.github/skills`, or project-local `.agents/skills`.

## Maintenance Rules

- Keep `AGENTS.md` as the shared source of truth.
- Keep `CLAUDE.md` and `GEMINI.md` thin wrappers that point to `AGENTS.md` and
  the relevant scoped instruction files.
- Keep instruction files task-scoped and repository-specific.
- Remove stale stack references immediately when the repository changes.
- Do not copy instruction files from another repository without adapting the
  stack, commands, domain contracts, and verification gates.
- Keep verification commands aligned with `backend/pyproject.toml`,
  `frontend/package.json`, and GitHub Actions.
- Keep custom agents aligned with the instruction map and current subsystem
  boundaries.

## Review Checklist

Before finishing an agent-instruction change, verify:

- Root wrappers point to existing files.
- Every file referenced in `AGENTS.md` exists.
- Commands match the repository's actual package managers and CI.
- Subsystem descriptions match current directories.
- Guardrails do not contradict higher-priority runtime or user instructions.
- The change is docs-only unless the task explicitly asked for behavior changes.
