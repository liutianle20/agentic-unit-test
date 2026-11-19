"""Local Streamlit preview for the unit test agent."""

from pathlib import Path

from openai import OpenAIError
import streamlit as st

from unit_agent import ModelConfig, run_agent, run_plan_execute
from unit_agent.baseline import run_baseline
from unit_agent.security import redact_sensitive_text


METHODS = {
    "ReAct": run_agent,
    "Plan-and-Execute": run_plan_execute,
    "Single-shot baseline": run_baseline,
}
DEFAULT_REPO = Path(__file__).resolve().parent / "fixtures" / "sample_project"


def show_result(method, repo, goal, model, result):
    st.subheader(f"Outcome: {result.outcome}")
    st.text(f"{method} · {model}\nRepository: {repo}\nGoal: {goal}")
    for issue in result.unresolved_issues:
        st.warning(issue)

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

    with st.expander(f"Trace ({len(result.tool_trace)} steps)", expanded=True):
        for entry in result.tool_trace:
            st.json(entry)


def main():
    st.set_page_config(page_title="Unit test agent", layout="wide")
    st.title("Unit test agent")
    defaults = ModelConfig.from_env()

    with st.sidebar.form("preview"):
        repo = st.text_input("Repository path", value=str(DEFAULT_REPO))
        goal = st.text_area("Test goal", value="Test the maximum allowed retries.")
        method = st.selectbox("Method", list(METHODS))
        model = st.text_input("Model", value=defaults.model, placeholder="Enter your provider's model ID")
        if not defaults.api_key:
            st.info("Set OPENAI_API_KEY in the environment and restart Streamlit.")
        st.caption("Use trusted repositories. Verification executes generated Python locally.")
        st.caption("Safety checks are educational defense in depth, not an OS sandbox.")
        submitted = st.form_submit_button("Run preview", type="primary")

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
            repo = str(Path(repo.strip()).expanduser().resolve(strict=True))
            with st.spinner("Running preview…"):
                result = METHODS[method](repo, goal.strip(), config)
        except (OSError, ValueError, OpenAIError) as error:
            st.session_state["preview_error"] = str(error)
        else:
            display_goal, _ = redact_sensitive_text(goal.strip())
            st.session_state["preview_result"] = (method, repo, display_goal, config.model, result)
            st.session_state.pop("preview_error", None)

    error = st.session_state.get("preview_error")
    previous = st.session_state.get("preview_result")
    if error:
        st.error(error)
        if previous:
            st.caption("Showing the previous run.")
    if previous:
        show_result(*previous)


if __name__ == "__main__":
    main()
