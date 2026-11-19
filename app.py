"""Local Streamlit preview for the unit test agent."""

from pathlib import Path

from openai import OpenAIError
import streamlit as st

from unit_agent import ModelConfig
from unit_agent.baseline import run_baseline
from unit_agent.chat import AgentChat


METHODS = ("ReAct", "Plan-and-Execute", "Single-shot baseline")
DEFAULT_REPO = Path(__file__).resolve().parent / "fixtures" / "sample_project"


def show_result(result):
    st.subheader(f"Outcome: {result.outcome}")
    for issue in result.unresolved_issues:
        st.text(issue)

    turns, tokens, elapsed, repairs = st.columns(4)
    turns.metric("Model turns", result.model_turns)
    usage = result.token_usage
    tokens.metric("Tokens", f"{sum(usage.values()):,}" if usage is not None else "Unavailable")
    elapsed.metric("Seconds", f"{result.elapsed_seconds:.2f}")
    repairs.metric("Repairs", result.repair_count)

    st.subheader("Generated diff")
    if result.diff:
        st.code(result.diff, language="diff")
    else:
        st.caption("This run produced no diff.")

    st.subheader("Verification")
    tests, coverage = st.columns(2)
    for column, label, data in (
        (tests, "Tests", result.tests),
        (coverage, "Coverage", result.coverage),
    ):
        with column:
            st.markdown(f"**{label}**")
            if data is None:
                st.caption("Unavailable for this run.")
            else:
                st.json(data)

    show_trace(result)


def show_trace(result):
    with st.expander(f"Trace ({len(result.tool_trace)} steps)"):
        for entry in result.tool_trace:
            st.json(entry)


def main():
    st.set_page_config(page_title="Unit test agent", layout="wide")
    st.title("Unit test agent")
    defaults = ModelConfig.from_env()

    chat = st.session_state.get("agent_chat")
    with st.sidebar:
        if st.button("New chat"):
            st.session_state.pop("agent_chat", None)
            st.session_state.pop("baseline_result", None)
            st.rerun()
        repo = st.text_input("Repository path", value=str(DEFAULT_REPO), disabled=chat is not None)
        method = st.selectbox("Method", METHODS, disabled=chat is not None)
        model = st.text_input("Model", value=defaults.model, placeholder="Enter your provider's model ID")
        manage_memory = st.checkbox("Clear old tool results", value=True,
                                    disabled=method == "Single-shot baseline")
        if not defaults.api_key:
            st.info("Set OPENAI_API_KEY in the environment and restart Streamlit.")
        st.caption("Use trusted repositories. Verification executes generated Python locally.")

    ask = False
    if chat is None:
        with st.form("preview"):
            goal = st.text_area("Test goal", value="Test the maximum allowed retries.")
            submitted = st.form_submit_button("Run preview", type="primary")
    else:
        with st.form("follow_up", clear_on_submit=True):
            goal = st.text_area("Follow-up")
            ask = st.form_submit_button("Ask", type="primary")
            revise = st.form_submit_button("Revise tests")
            submitted = ask or revise

    error = None
    if submitted:
        try:
            if not repo.strip():
                raise ValueError("Enter a repository path.")
            if not goal.strip():
                raise ValueError("Enter a test goal.")
            if not model.strip():
                raise ValueError("Enter a model ID in the Model field or set OPENAI_MODEL before starting Streamlit.")
            if not defaults.api_key:
                raise ValueError("Set OPENAI_API_KEY before starting Streamlit.")
            config = ModelConfig(model.strip(), defaults.base_url, defaults.api_key)
            repository = chat.repository if chat else Path(repo.strip()).expanduser().resolve(strict=True)
            with st.spinner("Working…"):
                if method == "Single-shot baseline" and chat is None:
                    result = run_baseline(repository, goal.strip(), config)
                    st.session_state["baseline_result"] = (repository, goal.strip(), config.model, result)
                else:
                    current = chat or AgentChat(repository, plan_execute=method == "Plan-and-Execute")
                    result = current.send(goal, config, ask=ask, manage_memory=manage_memory)
                    st.session_state["agent_chat"] = current
                    if chat is None:
                        st.session_state.pop("baseline_result", None)
                        st.rerun()
                    if not ask and result.outcome != "ready" and current.candidate:
                        st.info("The previous verified candidate is still active.")
        except (OSError, ValueError, OpenAIError) as failure:
            error = str(failure)

    if error:
        st.error(error)
    if chat:
        st.text(f"{method} · {chat.repository}")
        for question, answer, result in chat.turns:
            with st.chat_message("user"):
                st.text(question)
            with st.chat_message("assistant"):
                if result.outcome == "answered":
                    st.text(answer)
                    show_trace(result)
                else:
                    show_result(result)
    elif "baseline_result" in st.session_state:
        repository, question, used_model, result = st.session_state["baseline_result"]
        st.text(f"Single-shot baseline · {used_model}\n{repository}\n{question}")
        show_result(result)


if __name__ == "__main__":
    main()
