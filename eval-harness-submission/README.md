# Evaluation harness submission

## Team members

- Tianle Liu (`tianlliu`)
- Jade Guo (`xiguo`)

## Folder structure

```text
eval-harness-submission/
├── README.md
├── tasks.jsonl                  # 50 tasks and their grading rubrics
├── run_evaluation.sh           # Collect and grade all attempts in one command
├── results.md                  # Submitted metrics, flipped tasks, and failure analysis
├── unit-agent/
│   ├── collect.py              # Run the baseline, ReAct, and Plan-and-Execute
│   ├── evaluate.py             # Grade saved attempts and generate the report
│   └── …                       # Agent, baseline, workspace, and record code
├── fixtures/
│   └── sample_project/         # Python code under test and reference tests
├── pyproject.toml              # Python requirements and dependencies
└── uv.lock                     # Locked dependency versions
```

## Setup

Install Python 3.11 or newer and `uv`. From the directory containing the submission folder, run the commands below. Replace the placeholders with your model ID and API key. The generation model must support function tool calls.

`uv run` installs the source from `unit-agent/` as the Python package `unit_agent`. Use `unit_agent` in commands that run Python modules with `-m`.

```sh
cd eval-harness-submission
export OPENAI_MODEL='<model-id>'
export OPENAI_API_KEY='<your-api-key>'
```

The client uses OpenAI's default endpoint unless you set `OPENAI_BASE_URL`. For a different OpenAI-compatible provider, set it to that provider's API base URL.

```sh
export OPENAI_BASE_URL='<provider-api-base-url>'
```

## Run the full evaluation

Run from the submission folder. Choose two output paths that do not exist yet. The script runs one baseline attempt and three trials per agent on each of the 50 tasks, then grades all 350 attempts. Both stages print progress to stderr.

```sh
sh ./run_evaluation.sh eval-results/generation eval-results/report
```

```text
eval-results/
├── generation/
│   ├── manifest.json          # Selected tasks, model, and expected trial counts
│   └── generation.jsonl       # Candidates, traces, and generation metrics
└── report/
    ├── attempts.jsonl         # Verdicts and grading evidence for each attempt
    └── results.md             # Summary of this run
```

## Run a smoke evaluation

Collect and grade seven attempts for one task. Use fresh output paths for repeat runs.

```sh
uv run python -m unit_agent.collect --tasks tasks.jsonl --task validation-02 --output eval-results/smoke-generation
uv run python -m unit_agent.evaluate --input eval-results/smoke-generation --output eval-results/smoke-report
```

## Regrade saved attempts

Keep the collection complete and its original fixture paths and contents available. With judge credentials configured, pass the existing collection directory and a new report path. The evaluator runs pytest and rubric checks on the saved candidates without rerunning the baseline or agents.

```sh
uv run python -m unit_agent.evaluate --input eval-results/generation --output eval-results/regraded
```
