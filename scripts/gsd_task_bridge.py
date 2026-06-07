#!/usr/bin/env python3
"""Bridge GSD markdown task queues to automation-friendly outputs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


EXPECTED_HEADER = ["id", "phase", "status", "risk", "title", "scope", "acceptance"]
ALLOWED_STATUSES = {"todo", "in-progress", "blocked", "done"}
ALLOWED_RISKS = {"low", "medium", "high", "critical"}
SAFE_AUTONOMOUS_RISKS = {"low", "medium"}


@dataclass(frozen=True)
class Task:
    id: str
    phase: str
    status: str
    risk: str
    title: str
    scope: str
    acceptance: str

    @property
    def safe_for_autonomous_work(self) -> bool:
        return self.status == "todo" and self.risk in SAFE_AUTONOMOUS_RISKS


class TaskQueueError(ValueError):
    """Raised when the task queue cannot be parsed or validated."""


def _split_markdown_row(line: str) -> list[str]:
    row = line.strip()
    if not row.startswith("|"):
        raise TaskQueueError(f"not a markdown table row: {line!r}")
    if row.endswith("|"):
        row = row[1:-1]
    else:
        row = row[1:]

    cells: list[str] = []
    current: list[str] = []
    in_code = False
    escaped = False

    for char in row:
        if char == "`" and not escaped:
            in_code = not in_code
        if char == "|" and not in_code and not escaped:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        escaped = char == "\\" and not escaped

    cells.append("".join(current).strip())
    return cells


def _is_separator(cells: Iterable[str]) -> bool:
    return all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells)


def _clean_cell(value: str) -> str:
    return re.sub(r"<br\s*/?>", "; ", value.strip(), flags=re.IGNORECASE)


def parse_tasks(path: Path) -> list[Task]:
    if not path.exists():
        raise TaskQueueError(f"task queue does not exist: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    header_index: int | None = None

    for index, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            continue
        cells = [_clean_cell(cell).lower() for cell in _split_markdown_row(line)]
        if cells[: len(EXPECTED_HEADER)] == EXPECTED_HEADER:
            header_index = index
            break

    if header_index is None:
        raise TaskQueueError(
            f"could not find expected task table header in {path}: "
            + " | ".join(EXPECTED_HEADER)
        )

    tasks: list[Task] = []

    for line_number, line in enumerate(lines[header_index + 1 :], start=header_index + 2):
        if not line.lstrip().startswith("|"):
            if tasks:
                break
            continue

        cells = [_clean_cell(cell) for cell in _split_markdown_row(line)]
        if _is_separator(cells):
            continue
        if len(cells) < len(EXPECTED_HEADER):
            raise TaskQueueError(f"{path}:{line_number}: expected 7 task columns, got {len(cells)}")

        task = Task(
            id=cells[0],
            phase=cells[1],
            status=cells[2].lower(),
            risk=cells[3].lower(),
            title=cells[4],
            scope=cells[5],
            acceptance=cells[6],
        )
        tasks.append(task)

    validate_tasks(tasks, path)
    return tasks


def validate_tasks(tasks: list[Task], path: Path) -> None:
    if not tasks:
        raise TaskQueueError(f"task queue has no tasks: {path}")

    seen: set[str] = set()
    errors: list[str] = []

    for task in tasks:
        if not task.id:
            errors.append("task has an empty ID")
        elif task.id in seen:
            errors.append(f"duplicate task ID: {task.id}")
        seen.add(task.id)

        if task.status not in ALLOWED_STATUSES:
            errors.append(
                f"{task.id}: invalid status {task.status!r}; "
                f"expected one of {sorted(ALLOWED_STATUSES)}"
            )
        if task.risk not in ALLOWED_RISKS:
            errors.append(
                f"{task.id}: invalid risk {task.risk!r}; expected one of {sorted(ALLOWED_RISKS)}"
            )
        if not task.title:
            errors.append(f"{task.id}: title is required")
        if not task.scope:
            errors.append(f"{task.id}: scope is required")
        if not task.acceptance:
            errors.append(f"{task.id}: acceptance is required")

    if errors:
        raise TaskQueueError("\n".join(errors))


def select_next_task(tasks: Iterable[Task]) -> Task:
    for task in tasks:
        if task.safe_for_autonomous_work:
            return task
    raise TaskQueueError("no todo task with low or medium risk was found")


def render_task_prompt(task: Task) -> str:
    return f"""GSD task selected from .planning/todos/AGENT-TASKS.md

Task ID: {task.id}
Phase: {task.phase}
Risk: {task.risk}
Title: {task.title}
Scope: {task.scope}
Acceptance: {task.acceptance}

Mandatory workflow:
1. Read AGENTS.md first.
2. Read .planning/STATE.md, .planning/PROJECT.md, .planning/REQUIREMENTS.md,
   .planning/ROADMAP.md, and .planning/todos/AGENT-TASKS.md.
3. Prefer native GSD workflow commands if available; otherwise follow the
   equivalent Discuss -> Plan -> Execute -> Verify -> Ship lifecycle manually.
4. Work on exactly this task ID unless it is already complete or genuinely
   blocked on current main.
5. Stay inside the listed scope unless the GSD phase plan explicitly expands it.
6. Update .planning/STATE.md, .planning/todos/AGENT-TASKS.md, and verification
   notes affected by the work.
7. Do not recreate agent_tasks.json or legacy Jules planning files.
8. When opening a pull request, use .github/PULL_REQUEST_TEMPLATE.md as the main
   PR description template and fill its sections with the implementation,
   testing, planning updates, commands run, and limitations.
"""


def write_github_output(path: Path, values: dict[str, str]) -> None:
    with path.open("a", encoding="utf-8") as output:
        for key, value in values.items():
            if "\n" not in value:
                output.write(f"{key}={value}\n")
                continue

            delimiter = f"EOF_{key.upper()}"
            while delimiter in value:
                delimiter = f"{delimiter}_X"
            output.write(f"{key}<<{delimiter}\n{value}\n{delimiter}\n")


def command_validate(args: argparse.Namespace) -> int:
    tasks = parse_tasks(args.queue)
    print(f"Validated {len(tasks)} tasks from {args.queue}")
    return 0


def command_summary(args: argparse.Namespace) -> int:
    tasks = parse_tasks(args.queue)
    status_counts = {status: 0 for status in sorted(ALLOWED_STATUSES)}
    risk_counts = {risk: 0 for risk in sorted(ALLOWED_RISKS)}

    for task in tasks:
        status_counts[task.status] += 1
        risk_counts[task.risk] += 1

    try:
        next_safe_task = select_next_task(tasks).id
    except TaskQueueError:
        next_safe_task = None

    summary = {
        "queue": str(args.queue),
        "total": len(tasks),
        "statuses": status_counts,
        "risks": risk_counts,
        "next_safe_task": next_safe_task,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def command_next(args: argparse.Namespace) -> int:
    tasks = parse_tasks(args.queue)
    task = select_next_task(tasks)
    task_json = json.dumps(asdict(task), separators=(",", ":"), sort_keys=True)
    task_prompt = render_task_prompt(task)

    if args.github_output:
        write_github_output(
            args.github_output,
            {
                "task_id": task.id,
                "task_json": task_json,
                "task_prompt": task_prompt,
            },
        )

    print(task_json)
    return 0


def command_prompt(args: argparse.Namespace) -> int:
    tasks = parse_tasks(args.queue)
    task = next((candidate for candidate in tasks if candidate.id == args.task_id), None)
    if task is None:
        raise TaskQueueError(f"task ID not found: {args.task_id}")
    print(render_task_prompt(task))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate, summarize, select, and render GSD task queue entries."
    )
    subparsers = parser.add_subparsers(dest="command")

    validate_parser = subparsers.add_parser("validate", help="Validate the GSD task queue.")
    validate_parser.add_argument("queue", type=Path)
    validate_parser.set_defaults(func=command_validate)

    summary_parser = subparsers.add_parser("summary", help="Print task queue summary JSON.")
    summary_parser.add_argument("queue", type=Path)
    summary_parser.set_defaults(func=command_summary)

    next_parser = subparsers.add_parser("next", help="Print the next safe task as JSON.")
    next_parser.add_argument("queue", type=Path)
    next_parser.add_argument(
        "--github-output",
        type=Path,
        help="Append task_id, task_json, and task_prompt to a GitHub Actions output file.",
    )
    next_parser.set_defaults(func=command_next)

    prompt_parser = subparsers.add_parser("prompt", help="Render a focused GSD task prompt.")
    prompt_parser.add_argument("queue", type=Path)
    prompt_parser.add_argument("task_id", help="Task ID to render.")
    prompt_parser.set_defaults(func=command_prompt)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "func"):
        parser.print_help()
        return 2

    try:
        return args.func(args)
    except TaskQueueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
