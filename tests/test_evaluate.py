import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from unit_agent import AgentResult, ModelConfig
from unit_agent.evaluate import evaluate_attempt, judge_attempt, read_tasks, run_evaluation
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


@pytest.mark.parametrize("include_plan_execute", [False, True])
def test_two_task_report(tmp_path, include_plan_execute):
    tasks = read_tasks(ROOT / "tasks.jsonl", ["validation-02", "unanswerable-01"])
    candidate = result(tmp_path / "candidate", "from validation import retries\n"
                       "def test_boundary():\n    assert retries(5) == 5")
    unanswerable = result(tmp_path / "candidate", outcome="unanswerable",
                          issues=["The deployment-specific maximum is missing. Ask for its spec."])
    def snapshot():
        return {path: path.read_bytes() for path in Path(tasks[0]["fixture"]).rglob("*")
                if path.is_file()}

    before = snapshot()
    boundary_judgments = iter((True, True, False, True, True, False, True))

    def generate(repo, goal, config):
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

    output = tmp_path / "eval"
    rows = run_evaluation(tasks, output, CONFIG,
                          lambda *args: judge_attempt(client, CONFIG.model, *args),
                          baseline=generate, react=generate,
                          plan_execute=generate if include_plan_execute else None)
    assert snapshot() == before
    assert len(rows) == (14 if include_plan_execute else 8)
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
    if include_plan_execute:
        assert sum(row["method"] == "plan-execute" for row in rows) == 6
        assert "Plan-and-Execute trial 1" in report
        assert "## Plan-and-Execute consistency" in report
        assert "## Tasks that flipped for Plan-and-Execute" in report
    else:
        assert "Plan-and-Execute" not in report
    logged = [json.loads(line) for line in (output / "attempts.jsonl").read_text().splitlines()]
    assert logged == rows
    assert logged[0]["schema_version"] == 1
    assert logged[0]["model"] == "scripted"
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

    row = evaluate_attempt(task, "baseline", 1, lambda *args: candidate, CONFIG, unexpected_judge)
    assert row["failure_stage"] == stage
    if source == "def test_broken(:":
        assert "test_counts" not in row["execution"]
    if source == "# no tests":
        assert row["execution"]["test_counts"] == {"passed": 0, "generated": 0}
