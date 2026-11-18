# ReAct pytest preview

Set `OPENAI_MODEL` and `OPENAI_API_KEY`. Set `OPENAI_BASE_URL` if using a different OpenAI-compatible chat completions endpoint. The endpoint and model must support function tool calls.

```sh
uv run unit-agent --repo fixtures/sample_project --goal "Test the maximum allowed retries."
```

The CLI prints a JSON preview, including the staged diff and verification results. For Python callers, import `ModelConfig` and `run_agent` from `unit_agent`. Credentials can be read from the environment with `ModelConfig.from_env()`.

Use trusted repositories. Pytest executes generated Python in a temporary copy with a timeout and a limited environment. The subprocess still runs with the current user's OS permissions.

Run the scripted acceptance checks with `uv run python -m pytest -q tests`.

## Single-shot baseline

Run one model call with the goal, Python source, and existing tests:

```sh
uv run unit-agent --method baseline --repo fixtures/sample_project \
  --goal "Test the maximum allowed retries."
```

The baseline returns `staged` and a diff when it receives a candidate. It leaves
`tests` and `coverage` empty for the evaluator to fill. Python callers can import
`run_baseline` from `unit_agent.baseline`.

## Shared evaluator

Run the two-task smoke evaluation from the repository root with the model and
API credentials configured. Choose a new output directory for each run.

```sh
uv run --env-file .env.deepseek python -m unit_agent.evaluate \
  --tasks tasks.jsonl --task validation-02 --task unanswerable-01 \
  --output eval-results/smoke
```

The evaluator runs one single-shot attempt and three ReAct attempts per selected
task. It grades the candidates independently with pytest and model rubric checks.
The report compares single-shot with ReAct trial one. ReAct consistency uses all
three trials. See `results.md` for the report. Each line of `attempts.jsonl`
contains one versioned attempt with task details, model, method, trial, verdict,
normalized metrics, and generation, pytest, judge, and mutation evidence.
Unavailable metrics are JSON `null`.
Omit the task flags when ready to run the full 50-task submission evaluation.

## Plan-and-Execute

Plan-and-Execute produces an ordered plan, executes one step at a time, and
replans when tests fail or repository evidence invalidates a step. It uses the
same tools and workspace as ReAct.

```sh
uv run --env-file .env.deepseek unit-agent --method plan-execute \
  --repo fixtures/sample_project --goal "Test the maximum allowed retries."
```

Add `--include-plan-execute` to the shared evaluator to add three trials per
task and a separate consistency section for Plan-and-Execute.
