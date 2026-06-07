"""Validate BlueprintStudio's agent task manifest.

Usage:
    python scripts/validate_agent_tasks.py agent_tasks.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


VALID_STATUSES = {"todo", "in_progress", "blocked", "done"}
VALID_RISKS = {"low", "medium", "high", "critical"}
REQUIRED_TASK_FIELDS = {
    "id",
    "status",
    "area",
    "risk",
    "title",
    "description",
    "allowed_paths",
    "acceptance",
}


def _fail(message: str) -> None:
    raise SystemExit(f"agent_tasks.json invalid: {message}")


def _require_string(task: dict[str, Any], field: str) -> None:
    if not isinstance(task.get(field), str) or not task[field].strip():
        _fail(f"task {task.get('id', '<unknown>')} has invalid {field!r}")


def _require_string_list(task: dict[str, Any], field: str) -> None:
    value = task.get(field)
    if not isinstance(value, list) or not value:
        _fail(f"task {task.get('id', '<unknown>')} has empty {field!r}")
    if not all(isinstance(item, str) and item.strip() for item in value):
        _fail(f"task {task.get('id', '<unknown>')} has non-string {field!r} entry")


def validate_manifest(data: dict[str, Any]) -> None:
    if data.get("schema_version") != 1:
        _fail("schema_version must be 1")
    if data.get("project") != "BlueprintStudio":
        _fail("project must be BlueprintStudio")

    risk_levels = data.get("risk_levels")
    if risk_levels != ["low", "medium", "high", "critical"]:
        _fail("risk_levels must be ['low', 'medium', 'high', 'critical']")

    tasks = data.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        _fail("tasks must be a non-empty list")

    seen_ids: set[str] = set()
    todo_count = 0
    for task in tasks:
        if not isinstance(task, dict):
            _fail("every task must be an object")
        missing = REQUIRED_TASK_FIELDS - set(task)
        if missing:
            _fail(f"task {task.get('id', '<unknown>')} missing fields: {sorted(missing)}")

        for field in ("id", "status", "area", "risk", "title", "description"):
            _require_string(task, field)

        task_id = task["id"]
        if task_id in seen_ids:
            _fail(f"duplicate task id: {task_id}")
        seen_ids.add(task_id)

        if task["status"] not in VALID_STATUSES:
            _fail(f"task {task_id} has unknown status {task['status']!r}")
        if task["risk"] not in VALID_RISKS:
            _fail(f"task {task_id} has unknown risk {task['risk']!r}")

        if task["status"] == "todo":
            todo_count += 1

        _require_string_list(task, "allowed_paths")
        _require_string_list(task, "acceptance")

        if task["risk"] in {"high", "critical"} and not task.get("review_required"):
            _fail(f"task {task_id} is {task['risk']} risk but lacks review_required")

    repl = data.get("replenishment_policy")
    if not isinstance(repl, dict):
        _fail("replenishment_policy must be an object")
    minimum = repl.get("minimum_todo_tasks")
    if not isinstance(minimum, int) or minimum < 0:
        _fail("replenishment_policy.minimum_todo_tasks must be a non-negative integer")
    if todo_count < minimum:
        _fail(f"todo task count {todo_count} is below minimum {minimum}")


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path("agent_tasks.json")
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    validate_manifest(data)
    tasks = data["tasks"]
    counts: dict[str, int] = {}
    for task in tasks:
        counts[task["status"]] = counts.get(task["status"], 0) + 1
    print(f"ok: {path} contains {len(tasks)} tasks; status counts: {counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
