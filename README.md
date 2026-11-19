# Agentic Unit Test Generator

Generate pytest tests for Python code from a plain-language goal. The evaluation harness compares ReAct and Plan-and-Execute with a single-shot baseline.

## Project structure

```text
.
├── unit-agent/                     # Agent and baseline source
│   ├── collect.py                  # Run methods and save attempts
│   └── evaluate.py                 # Grade saved attempts and report metrics
├── fixtures/
│   └── sample_project/             # Code under test and reference tests
├── tests/                          # Agent and evaluator tests
├── tasks.jsonl                     # 50 evaluation tasks and rubrics
├── eval-results/
│   └── full-report/
│       ├── attempts.jsonl          # Per-attempt verdicts and evidence
│       └── results.md              # Full evaluation report
├── eval-harness-submission/        # Standalone submission package
├── pyproject.toml                  # Package configuration and dependencies
└── uv.lock                         # Locked dependency versions
```

## Quick start

Install Python 3.11 or newer and `uv`. On macOS with Homebrew, run:

```bash
brew install python uv
python3 --version
uv --version
```

From the repository root, set your model ID and API key in Bash. Use a model and endpoint that support function tool calls.

```bash
export OPENAI_MODEL='<model-id>'

export OPENAI_API_KEY='<your-api-key>'
```

For a different OpenAI-compatible endpoint, also set its API base URL:

```bash
export OPENAI_BASE_URL='<provider-api-base-url>'
```

The source folder is `unit-agent/`. The installed Python package is `unit_agent`, and the CLI command is `unit-agent`. Use `uv run` to install the package and run the commands below.

```sh
uv run unit-agent --repo fixtures/sample_project --goal "Test the maximum allowed retries."
```

The CLI prints a JSON preview, including the staged diff and verification results. For Python callers, import `ModelConfig` and `run_agent` from `unit_agent`. Credentials can be read from the environment with `ModelConfig.from_env()`.

Use trusted repositories. Pytest executes generated Python in a temporary copy with a timeout and a limited environment. The subprocess still runs with the current user's OS permissions.

Run the scripted acceptance checks with `uv run python -m pytest -q tests`.

## Streamlit preview

With the model environment variables set as above, start the local app from the repository root.

```sh
uv run --extra ui streamlit run app.py --server.address 127.0.0.1
```

If your provider settings are in an env file, pass it at launch. For a local
DeepSeek configuration saved in `.env.deepseek`, use:

```sh
uv run --env-file .env.deepseek --extra ui streamlit run app.py --server.address 127.0.0.1
```

Choose a repository, goal, and method to see the generated diff, verification
results, run metrics, and tool trace. Use trusted repositories because verification
runs generated pytest code with your OS permissions.

ReAct and Plan-and-Execute keep a chat in the current Streamlit session. After
the first preview, use **Ask** for read-only follow-ups or **Revise tests** to
edit and reverify the current candidate. A failed revision leaves the previous
verified candidate active. **New chat** clears the conversation and candidate.

## Repository search and memory

ReAct and Plan-and-Execute can search Python, Markdown, and `pyproject.toml`
in the preview workspace. Search returns excerpts with source paths and line
ranges. The agent can read the exact lines before using them as evidence.
Streamlit follow-ups can also search previous questions, answers, diffs, and
full tool results from that chat. The CLI and Python preview functions run
one goal at a time.

By default, model requests carry the newest four tool responses in full.
Older responses become placeholders while the full trace remains available.
Turn this off with **Clear old tool results** in Streamlit, `--no-memory` in
the CLI, or `manage_memory=False` in Python. Historical evaluation runs used
the earlier full-transcript behavior and did not have repository search.

Search uses TF-IDF by default. To enable hybrid repository ranking, run
`uv sync --extra ui`, then `uv pip install sentence-transformers` and make
`sentence-transformers/all-MiniLM-L6-v2` available in the local Hugging Face
cache. Use `uv run --no-sync --extra ui streamlit run app.py --server.address 127.0.0.1`
to keep that optional dependency installed. Preview runs never download the
model and fall back to keyword search if embeddings are unavailable.

## Single-shot baseline

Run one model call with the goal, Python source, and existing tests:

```sh
uv run unit-agent --method baseline --repo fixtures/sample_project \
  --goal "Test the maximum allowed retries."
```

The baseline returns `staged` and a diff when it receives a candidate. It leaves
`tests` and `coverage` empty for the evaluator to fill. Python callers can import
`run_baseline` from `unit_agent.baseline`.

## Collect and grade attempts

From the repository root, choose new output directories. The collector runs one
single-shot baseline attempt and three trials each for ReAct and Plan-and-Execute
on every selected task. A full run collects 350 records across all 50 tasks.

```sh
run_id=$(date +%Y%m%d-%H%M%S)
uv run python -m unit_agent.collect \
  --tasks tasks.jsonl --output "eval-results/full-generation-$run_id"

uv run python -m unit_agent.evaluate \
  --input "eval-results/full-generation-$run_id" \
  --output "eval-results/full-report-$run_id"
```

If you store credentials in a local environment file, add `--env-file <path>` after `uv run`.

For a smoke run, add `--task validation-02` to the collection command and use
separate output directories. Repeat `--task` to select more tasks.

The collector writes `manifest.json` and `generation.jsonl` with the candidate
diffs, traces, and generation statistics. The grader reads those files and needs
the same fixture paths and contents. It uses pytest and a configured model judge
to grade saved candidates. You can grade the same collection again with a fresh
report directory.

Both commands show record counts on stderr. The grader writes `attempts.jsonl`
with per-attempt evidence and `results.md` with side-by-side metrics, consistency
across three agent trials, and a failure trace when an attempt fails. Unavailable
metrics are JSON `null`.

## Plan-and-Execute

Plan-and-Execute produces an ordered plan, executes one step at a time, and
replans when tests fail or repository evidence invalidates a step. It uses the
same tools and workspace as ReAct.

```sh
uv run unit-agent --method plan-execute \
  --repo fixtures/sample_project --goal "Test the maximum allowed retries."
```
