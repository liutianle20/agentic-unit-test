"""Run generators and save attempts for independent grading."""

import argparse
from dataclasses import asdict
import json
from pathlib import Path
from time import monotonic

from openai import OpenAIError

from . import ModelConfig, run_agent, run_plan_execute
from .baseline import run_baseline
from .eval_records import SCHEMA_VERSION, TRIALS, Progress, describe_tasks, read_tasks, task_keys, write_record
from .security import redact_data


def collect_attempts(tasks, output, config, *, generators=None):
    if generators is None:
        generators = {"baseline": run_baseline, "react": run_agent, "plan-execute": run_plan_execute}
    descriptions = describe_tasks(tasks)
    for description in descriptions:
        safe_fields, _ = redact_data({
            "question": description["question"], "rubric": description["rubric"],
        })
        description.update(safe_fields)
    by_id = {task["id"]: task for task in descriptions}
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "model": config.model,
        "trials": TRIALS,
        "tasks": descriptions,
    }
    output.mkdir(parents=True, exist_ok=False)
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    keys = task_keys(tasks)
    progress = Progress("Collecting", len(keys))
    with (output / "generation.jsonl").open("x", encoding="utf-8") as log:
        for completed, (task_id, method, trial) in enumerate(keys, 1):
            task = by_id[task_id]
            generation = failure = None
            started = monotonic()
            try:
                result = generators[method](task["fixture"], task["question"], config)
            except (OSError, ValueError, OpenAIError) as error:
                failure = f"Generation raised {type(error).__name__}."
            elapsed = monotonic() - started
            if failure is None:
                generation = asdict(result)
            write_record(log, {
                "schema_version": SCHEMA_VERSION,
                "task_id": task_id, "task": task, "method": method, "trial": trial,
                "model": config.model, "generation_seconds": elapsed,
                "generation": generation, "failure_reason": failure,
            }, preserve_task_fixture=True)
            progress.update(completed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tasks", type=Path, default=Path("tasks.jsonl"))
    parser.add_argument("--task", action="append", default=[], help="Task ID, repeat to select several")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = ModelConfig.from_env()
    if not config.model.strip():
        parser.error("Set OPENAI_MODEL")
    try:
        collect_attempts(read_tasks(args.tasks, args.task), args.output, config)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(2, f"{parser.prog}: {error}\n")
    print(args.output / "generation.jsonl")


if __name__ == "__main__":
    main()
