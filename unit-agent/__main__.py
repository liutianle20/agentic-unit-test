"""Command-line entry point for the preview agent."""

import argparse
from dataclasses import asdict
import json

from openai import OpenAIError

from . import ModelConfig, run_agent, run_plan_execute
from .baseline import run_baseline


def main():
    parser = argparse.ArgumentParser(description="Preview generated pytest tests.")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--goal", required=True)
    methods = {"react": run_agent, "baseline": run_baseline, "plan-execute": run_plan_execute}
    parser.add_argument("--method", choices=methods, default="react")
    parser.add_argument("--no-memory", action="store_true", help="Send all tool responses to the model.")
    args = parser.parse_args()
    if args.method == "baseline" and args.no_memory:
        parser.error("--no-memory applies only to react and plan-execute")
    run = methods[args.method]
    options = {} if args.method == "baseline" else {"manage_memory": not args.no_memory}
    try:
        result = run(args.repo, args.goal, ModelConfig.from_env(), **options)
    except (OSError, ValueError, OpenAIError) as error:
        parser.exit(2, f"{parser.prog}: {error}\n")
    print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
    return 0 if result.outcome in ("ready", "staged", "unanswerable") else 1


if __name__ == "__main__":
    raise SystemExit(main())
