"""Shared task loading and disk format for collection and grading."""

from hashlib import sha256
import json
import os
import sys
from pathlib import Path

from .security import redact_data
from .workspace import ignore_files

SCHEMA_VERSION = 1
TRIALS = {"baseline": 1, "react": 3, "plan-execute": 3}
TASK_FIELDS = ("id", "type", "question", "fixture", "tags", "rubric")


def read_tasks(path, selected):
    tasks = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    by_id = {task["id"]: task for task in tasks}
    if len(by_id) != len(tasks):
        raise ValueError("Task IDs must be unique")
    for task in tasks:
        if (task["type"] not in ("rubric", "unanswerable")
                or not isinstance(task["question"], str) or not task["question"].strip()
                or not isinstance(task["rubric"], list) or not task["rubric"]
                or any(not isinstance(item, str) or not item.strip() for item in task["rubric"])):
            raise ValueError(f"Invalid task: {task['id']}")
        task["fixture"] = str((path.parent / task["fixture"]).resolve(strict=True))
    if selected:
        unknown = set(selected) - by_id.keys()
        if unknown:
            raise ValueError(f"Unknown task IDs: {', '.join(sorted(unknown))}")
        return [task for task in tasks if task["id"] in selected]
    if (len(tasks) != 50 or sum("edge-case" in task["tags"] for task in tasks) < 3
            or sum(task["type"] == "unanswerable" for task in tasks) < 2):
        raise ValueError("Full eval requires 50 tasks, at least 3 edge cases, and 2 unanswerable tasks")
    return tasks


def task_keys(tasks):
    return [
        (task["id"], method, trial)
        for task in tasks
        for method, count in TRIALS.items()
        for trial in range(1, count + 1)
    ]


def fixture_fingerprint(path):
    root = Path(path)
    if not root.is_dir():
        raise ValueError(f"Fixture directory unavailable: {root}")
    files = {}
    for directory, subdirs, names in os.walk(root):
        ignored = ignore_files(directory, subdirs + names)
        subdirs[:] = [name for name in subdirs if name not in ignored]
        for name in names:
            if name not in ignored:
                file = Path(directory) / name
                files[file.relative_to(root).as_posix()] = sha256(file.read_bytes()).hexdigest()
    return sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()


def describe_tasks(tasks):
    fingerprints = {
        path: fixture_fingerprint(path) for path in {task["fixture"] for task in tasks}
    }
    return [
        {**{key: task[key] for key in TASK_FIELDS},
         "fixture_fingerprint": fingerprints[task["fixture"]]}
        for task in tasks
    ]


def write_record(log, row, *, preserve_task_fixture=False):
    safe_row, _ = redact_data(row)
    if preserve_task_fixture:
        for key in ("schema_version", "task_id", "method", "trial", "model",
                    "generation_seconds"):
            if key in row:
                safe_row[key] = row[key]
        if isinstance(row.get("task"), dict) and isinstance(safe_row.get("task"), dict):
            for key in ("id", "type", "fixture", "tags", "fixture_fingerprint"):
                if key in row["task"]:
                    safe_row["task"][key] = row["task"][key]
    log.write(json.dumps(safe_row, ensure_ascii=False) + "\n")
    log.flush()


class Progress:
    def __init__(self, label, total, stream=None):
        self.label = label
        self.total = total
        self.stream = sys.stderr if stream is None else stream
        self.terminal = self.stream.isatty()
        self.update(0)

    def update(self, completed):
        if self.terminal:
            filled = 24 * completed // self.total
            bar = "#" * filled + "-" * (24 - filled)
            end = "\n" if completed == self.total else ""
            print(f"\r{self.label} [{bar}] {completed}/{self.total}",
                  end=end, file=self.stream, flush=True)
        elif completed % 25 == 0 or completed == self.total:
            print(f"{self.label} {completed}/{self.total}", file=self.stream, flush=True)
