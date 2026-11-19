import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from openai.types.chat import ChatCompletion

import unit_agent
from unit_agent import ModelConfig, run_agent

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures/sample_project"
TASK = next(task for line in (ROOT / "tasks.jsonl").read_text().splitlines()
            if (task := json.loads(line))["id"] == "validation-02")
CANDIDATE = "tests/test_agent_boundary.py"


def snapshot(root):
    return {path.relative_to(root): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in root.rglob("*") if path.is_file()}


def stage(expected):
    return ("stage_tests", {"path": CANDIDATE, "content":
            f"from validation import retries\n\ndef test_upper_boundary():\n    assert retries(5) == {expected}\n"})


def setup_model(monkeypatch, steps):
    responses = iter(steps)
    requests = []

    def create(**kwargs):
        requests.append(kwargs)
        index, step = next(responses)
        if isinstance(step, tuple):
            name, arguments = step
            message = {"role": "assistant", "content": None, "tool_calls": [
                {"id": f"call-{index}", "type": "function",
                 "function": {"name": name, "arguments": json.dumps(arguments)}}
            ]}
        else:
            message = {"role": "assistant", "content": step if isinstance(step, str) else json.dumps(step)}
        return ChatCompletion.model_validate({
            "id": f"response-{index}", "created": 0, "model": "scripted",
            "object": "chat.completion", "choices": [{
                "index": 0, "finish_reason": "tool_calls" if isinstance(step, tuple) else "stop",
                "message": message,
            }],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        })

    class Client:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(completions=SimpleNamespace(create=create))

        def __enter__(self):
            return self

        def __exit__(self, *error):
            pass

    monkeypatch.setattr(unit_agent, "OpenAI", Client)
    return requests


@pytest.mark.parametrize(("final_reply", "issues"), [
    ({"outcome": "ready", "summary": ""}, []),
    ('```json\n{"outcome": "ready", "summary": ""}\n```', []),
    ("Tests passed and coverage was recorded.", ["Model returned an invalid final response."]),
])
def test_validation_task_repairs_and_measures_coverage(monkeypatch, final_reply, issues):
    before = snapshot(FIXTURE)
    setup_model(monkeypatch, enumerate([
        ("list_files", {"pattern": "**/*.py"}),
        ("read_file", {"path": "../outside.py"}),
        ("read_file", {"path": "validation.py"}),
        ("inspect_python", {"path": "validation.py"}),
        stage(6), ("run_tests", {"target": "."}), stage(5),
        ("run_tests", {"target": "."}), ("get_coverage", {"target": "."}),
        final_reply,
    ]))
    result = run_agent(FIXTURE, TASK["question"], ModelConfig("scripted"))
    assert result.outcome == "ready"
    assert result.unresolved_issues == issues
    assert result.repair_count == 1
    assert result.tests["status"] == "passed"
    assert result.coverage["line_percent"] > 0
    assert result.coverage["branch_percent"] > 0
    assert "assert retries(5) == 5" in result.diff
    assert "error" in result.tool_trace[1]["result"]
    assert result.tool_trace[5]["result"]["status"] == "failed"
    assert result.token_usage == {"input_tokens": 100, "output_tokens": 50}
    assert snapshot(FIXTURE) == before


def test_repair_budget(monkeypatch):
    steps = [step for expected in (6, 7, 8, 9)
             for step in (stage(expected), ("run_tests", {"target": "."}))]
    setup_model(monkeypatch, enumerate([*steps, stage(10)]))
    result = run_agent(FIXTURE, TASK["question"], ModelConfig("scripted"))
    assert result.outcome == "budget_exhausted"
    assert result.repair_count == 3
    assert result.tests["status"] == "failed"
    assert "assert retries(5) == 9" in result.diff


def test_missing_evidence_returns_empty_diff(monkeypatch):
    setup_model(monkeypatch, enumerate([
        {"outcome": "unanswerable", "summary": "The service contract is missing."}
    ]))
    result = run_agent(FIXTURE, "Test the required retry delay.", ModelConfig("scripted"))
    assert result.outcome == "unanswerable"
    assert result.diff == ""
    assert result.unresolved_issues == ["The service contract is missing."]
    assert result.model_turns == 1
    assert result.tool_trace == []


@pytest.mark.parametrize(("repair_reply", "outcome", "repair_outcome"), [
    ({"outcome": "unanswerable", "summary": "No cap is specified. What limit applies?"},
     "unanswerable", "succeeded"),
    ("Still invalid.", "error", "failed"),
    ({"outcome": "unanswerable", "summary": " "}, "error", "failed"),
])
def test_unanswerable_final_retry(monkeypatch, repair_reply, outcome, repair_outcome):
    malformed = "The fixture does not specify the production count limit."
    requests = setup_model(monkeypatch, enumerate([
        ("read_file", {"path": "parsing.py"}), malformed, repair_reply,
    ]))
    result = run_agent(FIXTURE, "Test the production count limit.", ModelConfig("scripted"))

    assert result.outcome == outcome
    assert result.diff == ""
    assert len(requests) == result.model_turns == 3
    assert "tools" not in requests[-1]
    assert json.loads(requests[-1]["messages"][-1]["content"]) == {"reply": malformed}
    assert result.token_usage == {"input_tokens": 30, "output_tokens": 15}
    event = result.tool_trace[-1]
    assert event["event"] == "final_response_parse_failure"
    assert event["category"] == "JSONDecodeError"
    assert event["repair_attempted"] is True
    assert event["repair_outcome"] == repair_outcome


def test_pytest_timeout_and_missing_dependency_are_structured(monkeypatch, tmp_path):
    import subprocess

    from unit_agent.workspace import Workspace

    workspace = Workspace(tmp_path)
    workspace.stage_tests(**stage(5)[1])

    def timeout(command, **kwargs):
        raise subprocess.TimeoutExpired(command, kwargs["timeout"])

    monkeypatch.setattr(subprocess, "run", timeout)
    assert workspace.pytest(".", timeout=1)["status"] == "timeout"

    def no_pytest(command, **kwargs):
        return subprocess.CompletedProcess(command, 1, "python: No module named pytest")

    monkeypatch.setattr(subprocess, "run", no_pytest)
    result = workspace.pytest(".", timeout=1)
    assert result["status"] == "error"
    assert "No module named pytest" in result["output"]


def test_invalid_final_reply_after_candidate_edit_stays_error(monkeypatch):
    setup_model(monkeypatch, enumerate([
        stage(5), ("get_coverage", {"target": "."}), stage(6), "Done.",
    ]))
    result = run_agent(FIXTURE, TASK["question"], ModelConfig("scripted"))
    assert result.outcome == "error"
    assert result.tests is None
    assert result.coverage is None


def test_single_shot_stages_without_tools_or_execution(monkeypatch):
    from unit_agent import baseline
    from unit_agent.workspace import Workspace

    before = snapshot(FIXTURE)
    candidate = stage(5)[1]["content"]
    setup_model(monkeypatch, enumerate([{"outcome": "staged", "content": candidate}]))
    requests = []
    scripted_client = unit_agent.OpenAI

    def client(**kwargs):
        instance = scripted_client(**kwargs)
        create = instance.chat.completions.create

        def record(**request):
            requests.append(request)
            return create(**request)

        instance.chat.completions.create = record
        return instance

    def unexpected_pytest(*args, **kwargs):
        pytest.fail("The baseline must not execute pytest")

    monkeypatch.setattr(baseline, "OpenAI", client)
    monkeypatch.setattr(Workspace, "pytest", unexpected_pytest)

    result = baseline.run_baseline(FIXTURE, TASK["question"], ModelConfig("scripted"))

    assert len(requests) == result.model_turns == 1
    assert "tools" not in requests[0]
    context = json.loads(requests[0]["messages"][1]["content"])
    assert context["goal"] == TASK["question"]
    assert "validation.py" in context["python_files"]
    assert "tests/test_reference.py" in context["python_files"]
    assert result.outcome == "staged"
    assert "assert retries(5) == 5" in result.diff
    assert result.tests is result.coverage is None
    assert result.tool_trace == []
    assert snapshot(FIXTURE) == before


def plan_steps(*actions):
    return {"steps": [{"action": action, "done_when": f"Evidence confirms: {action}"}
                      for action in actions]}


def test_plan_execute_orders_steps_and_replans_on_failure(monkeypatch):
    completed = {"action": "step_complete", "summary": "Step verified."}
    requests = setup_model(monkeypatch, enumerate([
        plan_steps("Inspect validation", "Stage and verify the retry test"),
        ("read_file", {"path": "validation.py"}), completed,
        stage(6), ("run_tests", {"target": "."}),
        plan_steps("Correct the assertion and verify coverage"),
        stage(5), ("get_coverage", {"target": "."}), completed,
    ]))

    result = unit_agent.run_plan_execute(FIXTURE, TASK["question"], ModelConfig("scripted"))

    assert result.outcome == "ready"
    assert result.repair_count == 1
    assert result.tests["status"] == "passed" and result.coverage is not None
    assert result.model_turns == 9
    assert result.token_usage == {"input_tokens": 90, "output_tokens": 45}
    assert all("tools" not in requests[index] for index in (0, 5))
    assert "Inspect validation" in requests[1]["messages"][-1]["content"]
    assert "Stage and verify the retry test" in requests[3]["messages"][-1]["content"]
    events = [item for item in result.tool_trace if "event" in item]
    assert [item["event"] for item in events] == ["plan", "step_complete", "replan", "step_complete"]
    assert events[2]["reason"] == "run_tests returned failed."
    assert "Step verified." in requests[5]["messages"][-1]["content"]


def test_plan_execute_replan_budget(monkeypatch):
    steps = [
        step for _ in range(4) for step in (
            plan_steps("Inspect the fixture"),
            {"action": "replan", "summary": "Current plan cannot be completed."},
        )
    ]
    setup_model(monkeypatch, enumerate(steps))

    result = unit_agent.run_plan_execute(FIXTURE, TASK["question"], ModelConfig("scripted"))

    assert result.outcome == "budget_exhausted"
    assert result.model_turns == 8
    assert sum(item.get("event") == "replan" for item in result.tool_trace) == 3
    assert not result.diff


def test_plan_execute_unanswerable(monkeypatch):
    setup_model(monkeypatch, enumerate([
        plan_steps("Check production importer limits"),
        ("read_file", {"path": "parsing.py"}),
        {"outcome": "unanswerable", "summary": "No production limit is specified. Can you share it?"},
    ]))

    result = unit_agent.run_plan_execute(FIXTURE, "Test the production importer limit.",
                                         ModelConfig("scripted"))

    assert result.outcome == "unanswerable"
    assert not result.diff


def test_plan_execute_repairs_step_prose_and_continues(monkeypatch):
    inspected = "Inspection complete. validation.retries accepts 5 and rejects 6."
    tested = "The staged boundary test passed and coverage was recorded."
    plan = plan_steps("Inspect retry validation", "Generate and verify the boundary test")
    requests = setup_model(monkeypatch, enumerate([
        plan, ("read_file", {"path": "validation.py"}), inspected,
        {"action": "step_complete", "summary": inspected},
        stage(5), ("get_coverage", {"target": "."}), tested,
        {"action": "step_complete", "summary": tested},
    ]))

    result = unit_agent.run_plan_execute(FIXTURE, TASK["question"], ModelConfig("scripted"))

    assert result.outcome == "ready"
    assert "assert retries(5) == 5" in result.diff
    assert result.tests["status"] == "passed"
    assert result.coverage is not None
    assert result.model_turns == 8
    for index, step, reply in ((3, 0, inspected), (7, 1, tested)):
        assert "tools" not in requests[index]
        assert json.loads(requests[index]["messages"][-1]["content"]) == {
            "reply": reply, "active_step": plan["steps"][step],
        }
    repairs = [event for event in result.tool_trace if event.get("event") == "final_response_parse_failure"]
    assert [event["repair_outcome"] for event in repairs] == ["succeeded", "succeeded"]



def test_plan_execute_finalizes_on_last_allowed_model_turn(monkeypatch):
    reads = [("read_file", {"path": "validation.py"})] * 16
    requests = setup_model(monkeypatch, enumerate([
        plan_steps("Generate and verify the boundary test"),
        *reads, stage(5), ("get_coverage", {"target": "."}),
        {"action": "step_complete", "summary": "Boundary test passed with coverage."},
    ]))

    result = unit_agent.run_plan_execute(FIXTURE, TASK["question"], ModelConfig("scripted"))

    assert result.outcome == "ready"
    assert result.tests["status"] == "passed"
    assert len(requests) == result.model_turns == 20


@pytest.mark.parametrize("manage_memory", [True, False])
def test_retrieval_and_tool_response_window(monkeypatch, manage_memory):
    from unit_agent.retrieval import CLEARED

    requests = setup_model(monkeypatch, enumerate([
        ("search_repo", {"query": "retries"}),
        ("read_lines", {"path": "validation.py", "start": 1, "end": 20}),
        ("read_lines", {"path": "../outside.py", "start": 1, "end": 2}),
        ("inspect_python", {"path": "validation.py"}),
        stage(5), ("get_coverage", {"target": "."}),
        {"outcome": "ready", "summary": ""},
    ]))
    result = run_agent(FIXTURE, TASK["question"], ModelConfig("scripted"),
                       manage_memory=manage_memory)
    assert result.outcome == "ready" and result.coverage
    trace = result.tool_trace
    assert "validation.py" in {hit["path"] for hit in trace[0]["result"]["results"]}
    assert "def retries" in trace[1]["result"]["text"]
    assert "workspace-relative" in trace[2]["result"]["error"]
    tools = [item for item in requests[-1]["messages"] if item["role"] == "tool"]
    assert [item["tool_call_id"] for item in tools] == [f"call-{i}" for i in range(6)]
    assert [item["content"] == CLEARED for item in tools] == [manage_memory] * 2 + [False] * 4
    assert all(item["role"] != "tool" for item in requests[0]["messages"])


def test_chat_recalls_older_results_and_keeps_verified_candidate(monkeypatch):
    from unit_agent.chat import AgentChat

    ready = {"outcome": "ready", "summary": "Verified retry boundary."}
    requests = setup_model(monkeypatch, enumerate([
        ("read_file", {"path": "validation.py"}),
        stage(5), ("get_coverage", {"target": "."}), ready,
        "The first test checks the upper limit.",
        "The test was verified with coverage.",
        ("search_history", {"query": "def retries"}),
        ("read_history", {"entry_id": "turn-1-tool-1:0"}),
        stage(6),
        ("run_tests", {"target": "."}),
        "The earlier validation.py read showed the retry definition.",
        ("read_file", {"path": CANDIDATE}),
        stage(6), ("get_coverage", {"target": "."}),
        {"outcome": "blocked", "summary": "The revision failed."},
        ("read_file", {"path": CANDIDATE}),
        stage(5), ("get_coverage", {"target": "."}), ready,
    ]))
    config = ModelConfig("scripted")
    chat = AgentChat(FIXTURE)
    assert chat.send("Generate the retry test", config).outcome == "ready"
    original = chat.candidate.copy()
    chat.send("What does it cover?", config, ask=True)
    chat.send("Did you collect coverage?", config, ask=True)
    answer = chat.send("What did the first source read show?", config, ask=True)
    assert answer.outcome == "answered"
    assert "validation.py" in answer.unresolved_issues[0]
    assert "Generate the retry test" not in str(requests[6]["messages"])
    hits = answer.tool_trace[0]["result"]["results"]
    assert any(hit["entry_id"] == "turn-1-tool-1:0" for hit in hits)
    assert "def retries" in answer.tool_trace[1]["result"]["text"]
    assert all("Unknown tool" in entry["result"]["error"] for entry in answer.tool_trace[2:])
    names = {tool["function"]["name"] for tool in requests[6]["tools"]}
    assert not names & {"stage_tests", "run_tests", "get_coverage"}
    assert chat.candidate == original
    failed = chat.send("Try a bad assertion", config)
    assert failed.outcome == "blocked" and chat.candidate == original
    assert failed.tool_trace[0]["result"]["text"] == original[CANDIDATE]
    revised = chat.send("Restore the valid assertion", config)
    assert revised.outcome == "ready" and revised.coverage
    assert revised.tool_trace[0]["result"]["text"] == original[CANDIDATE]
    assert not AgentChat(FIXTURE).turns


def test_replan_receives_only_four_full_tool_responses(monkeypatch):
    from unit_agent.retrieval import CLEARED

    reads = [("read_file", {"path": "validation.py"})] * 5
    requests = setup_model(monkeypatch, enumerate([
        plan_steps("Inspect retry code"), *reads,
        {"action": "replan", "summary": "The original test criterion needs review."},
        plan_steps("Check what evidence is missing"),
        {"outcome": "unanswerable", "summary": "Please provide the deployment requirement."},
    ]))
    result = unit_agent.run_plan_execute(FIXTURE, TASK["question"], ModelConfig("scripted"))
    assert result.outcome == "unanswerable"
    planner = requests[-2]
    assert "tools" not in planner
    responses = [message for message in planner["messages"] if message["role"] == "tool"]
    assert [message["content"] == CLEARED for message in responses] == [True, False, False, False, False]
    assert all("def retries" in item["result"]["text"]
               for item in result.tool_trace if item.get("tool") == "read_file")
