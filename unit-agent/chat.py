"""State owned by one interactive agent chat."""

from dataclasses import dataclass, field
from pathlib import Path

from . import AgentResult, ModelConfig, run_chat_turn


@dataclass
class AgentChat:
    repository: Path
    plan_execute: bool = False
    turns: list[tuple[str, str, AgentResult]] = field(default_factory=list, init=False)
    candidate: dict[str, str] = field(default_factory=dict, init=False)

    def send(self, question: str, config: ModelConfig, *, ask=False, manage_memory=True):
        question = question.strip()
        if ask and not self.turns:
            raise ValueError("Generate tests before asking a follow-up.")
        result, staged = run_chat_turn(
            self.repository, question, config, plan_execute=self.plan_execute,
            manage_memory=manage_memory, turns=self.turns, candidate=self.candidate, ask=ask,
        )
        if not ask and result.outcome == "ready":
            self.candidate = staged
        if result.outcome == "answered":
            answer = result.unresolved_issues[0]
        else:
            answer = f"Outcome: {result.outcome}."
            if result.unresolved_issues:
                answer += " " + " ".join(result.unresolved_issues)
        self.turns.append((question, answer, result))
        return result
