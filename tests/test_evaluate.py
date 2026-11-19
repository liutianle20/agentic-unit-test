from dataclasses import asdict
from io import StringIO
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from unit_agent import AgentResult, ModelConfig
from unit_agent.collect import collect_attempts
from unit_agent.eval_records import Progress, TRIALS, read_tasks
from unit_agent.evaluate import evaluate_attempt, judge_attempt, load_collection, run_evaluation
from unit_agent.workspace import Workspace

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ModelConfig("scripted")
BOUNDARY = "Test the maximum allowed retries."


def result(tmp_path, source=None, outcome="staged", issues=None):
    tmp_path.mkdir(exist_ok=True)
    workspace = Workspace(tmp_path)
    if source is not None:
        workspace.stage_tests("tests/test_agent_case.py", source)
    return AgentResult(outcome, workspace.diff(), None, None, issues or [],
                       1, {"input_tokens": 10, "output_tokens": 5}, 0.1, 0, [])


def test_two_task_report(tmp_path, capsys):
    tasks = read_tasks(ROOT / "tasks.jsonl", ["validation-02", "unanswerable-01"])
    candidate = result(tmp_path / "candidate", "from validation import retries\n"
                       "def test_boundary():\n    assert retries(5) == 5")
    unanswerable = result(tmp_path / "candidate", outcome="unanswerable",
                          issues=["The deployment-specific maximum is missing. Ask for its spec."])
    candidate.tool_trace.append({"event": "step_complete", "step": {"action": "Test boundary"}})

    def snapshot():
        return {path: path.read_bytes() for path in Path(tasks[0]["fixture"]).rglob("*")
                if path.is_file()}

    before = snapshot()
    generation_calls = []
    boundary_judgments = iter((True, True, False, True, True, False, True) * 2)

    def generate(repo, goal, config):
        generation_calls.append(goal)
        return candidate if goal == BOUNDARY else unanswerable

    def complete(**request):
        assert "tools" not in request
        evidence = json.loads(request["messages"][1]["content"])
        verdict = next(boundary_judgments) if evidence["question"] == BOUNDARY else True
        assert (evidence["pytest"] is not None) == (evidence["question"] == BOUNDARY)
        checks = [{"passed": verdict or index < 4,
                   "reason": "Evidence checked." if verdict or index < 4 else "Scripted rubric failure."}
                  for index, _ in enumerate(evidence["criteria"])]
        return SimpleNamespace(choices=[SimpleNamespace(
            message=SimpleNamespace(content=json.dumps({"checks": checks})))])
    client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=complete)))

    collection = tmp_path / "collection"
    collect_attempts(tasks, collection, CONFIG, generators=dict.fromkeys(TRIALS, generate))
    assert len(generation_calls) == 14
    judge_config = ModelConfig("scripted-judge")

    def judge(*args):
        return judge_attempt(client, judge_config.model, *args)

    output = tmp_path / "eval"
    rows = run_evaluation(collection, output, judge_config, judge)
    regraded = run_evaluation(collection, tmp_path / "regrade", judge_config, judge)
    assert [(row["passed"], row["metrics"]) for row in regraded] == [
        (row["passed"], row["metrics"]) for row in rows
    ]
    assert len(generation_calls) == 14
    progress = capsys.readouterr().err
    assert "Collecting 0/14" in progress and "Collecting 14/14" in progress
    assert progress.count("Grading 14/14") == 2
    assert rows[0]["generation"]["tool_trace"] == candidate.tool_trace
    assert snapshot() == before
    assert len(rows) == 14
    assert sum(row["method"] == "baseline" for row in rows) == 2
    assert sum(row["method"] == "react" for row in rows) == 6
    assert rows[2]["failure_stage"] == "rubric"
    assert rows[2]["execution"]["status"] == "passed"
    assert rows[0]["execution"]["test_counts"] == {"passed": 1, "generated": 1}
    assert rows[0]["mutation"]["detected"] is True
    assert rows[-1]["execution"] is None and rows[-1]["passed"]
    report = (output / "results.md").read_text()
    for label in ("Accuracy", "Average model turns", "Average latency", "p95 latency",
                  "Average tokens", "Generated tests passed / generated", "Failure trace"):
        assert label in report
    assert "pass@3: 2/2" in report and "pass^3: 1/2" in report
    assert "validation-02: pass, fail, pass" in report
    assert sum(row["method"] == "plan-execute" for row in rows) == 6
    assert "Plan-and-Execute trial 1" in report
    assert "## Plan-and-Execute consistency" in report
    assert "## Tasks that flipped for Plan-and-Execute" in report
    logged = [json.loads(line) for line in (output / "attempts.jsonl").read_text().splitlines()]
    assert logged == rows
    assert logged[0]["schema_version"] == 1
    assert logged[0]["model"] == "scripted"
    assert logged[0]["judge_model"] == "scripted-judge"
    assert logged[0]["task"]["rubric"] == ["Assert retries(5) == 5."]
    assert logged[0]["metrics"]["total_tokens"] == 15
    assert logged[0]["metrics"]["generated_tests_passed"] == 1
    assert logged[0]["metrics"]["generated_tests_collected"] == 1
    assert logged[0]["failure_stage"] is None
    assert logged[2]["failure_stage"] == "rubric"
    assert logged[-1]["metrics"]["generated_tests_collected"] is None


@pytest.mark.parametrize(("source", "invalid_diff", "stage"), [
    ("def test_broken(:", False, "pytest"),
    ("def test_candidate():\n    assert True", True, "diff"),
    ("# no tests", False, "pytest"),
])
def test_bad_candidates_skip_judge(tmp_path, source, invalid_diff, stage):
    task, = read_tasks(ROOT / "tasks.jsonl", ["validation-02"])
    candidate = result(tmp_path, source)
    if invalid_diff:
        candidate.diff = candidate.diff.replace("tests/test_agent_case.py", "../validation.py")

    def unexpected_judge(*args):
        pytest.fail("Invalid candidate reached judge")

    saved = {"method": "baseline", "trial": 1, "generation": asdict(candidate),
             "generation_seconds": 0.1, "failure_reason": None}
    row = evaluate_attempt(task, saved, CONFIG, unexpected_judge)
    assert row["failure_stage"] == stage
    if source == "def test_broken(:":
        assert "test_counts" not in row["execution"]
    if source == "# no tests":
        assert row["execution"]["test_counts"] == {"passed": 0, "generated": 0}


def test_collection_failures_and_validation(tmp_path):
    fixture = tmp_path / "fixture"
    fixture.mkdir()
    source = fixture / "sample.py"
    source.write_text("answer = 1")
    task, = read_tasks(ROOT / "tasks.jsonl", ["validation-02"])
    task["fixture"] = str(fixture)

    def failed_generation(*args):
        raise ValueError("Provider error")

    def unexpected_judge(*args):
        pytest.fail("Generation failure reached judge")

    collection = tmp_path / "collection"
    collect_attempts([task], collection, CONFIG,
                     generators=dict.fromkeys(TRIALS, failed_generation))
    rows = run_evaluation(collection, tmp_path / "report", CONFIG, unexpected_judge)
    assert len(rows) == 7
    assert all(row["failure_stage"] == "generation" and not row["passed"] for row in rows)

    source.write_text("answer = 2")
    with pytest.raises(ValueError, match="Fixture changed"):
        load_collection(collection)

    source.write_text("answer = 1")
    log = collection / "generation.jsonl"
    lines = log.read_text().splitlines(keepends=True)
    log.write_text("".join(lines + lines[:1]))
    with pytest.raises(ValueError, match="Duplicate attempt"):
        load_collection(collection)

    log.write_text("".join(lines[:-1]))
    with pytest.raises(ValueError, match="Missing 1 of 7 attempts"):
        load_collection(collection)


def test_progress_for_full_run():
    stream = StringIO()
    progress = Progress("Collecting", 350, stream)
    for completed in range(1, 351):
        progress.update(completed)
    assert stream.getvalue().splitlines() == [
        f"Collecting {completed}/350" for completed in range(0, 351, 25)
    ]
