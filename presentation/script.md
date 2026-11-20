# Agentic Unit Testing · 3:00 script

Read the blockquotes aloud. Use the stage directions to cue the slides and the prerecorded demo. Trim model wait time to keep the demo to 60 seconds.

## 0:00–0:25 · Problem

*Slide 1. Show the prompt and the example Python test file.*

> Our Python batch-import codebase validates inputs, parses records, and looks up counts. A developer asks, “Test the maximum allowed retries.” They'd normally find the validator, confirm the limit, write the test, and run pytest. Give the agent the codebase and that request. It returns a test file and verification results, automating the whole workflow. The agent can also answer follow-up questions and revise the tests.

## 0:25–0:52 · Generation workflows

*Slide 2. Trace the single-shot baseline, then compare the two agents.*

> The single-shot baseline sends the goal, source code, and existing tests in one model call. The evaluator runs those test files later.
>
> ReAct chooses its next action from tool feedback. Plan-and-Execute starts with an ordered plan and can revise it as evidence changes. Both run pytest and measure coverage in a temporary copy.

## 0:52–1:10 · Memory and security

*Slide 3. Point to the Memory System and Security Constraints columns.*

> Agentic RAG finds relevant code on demand. The Streamlit session keeps history for follow-up questions and test revisions. Safety checks restrict where the agent can write, screen the generated code, and require fresh verification.

## 1:10–1:33 · Benchmark and grading

*Slide 4. Show the task counts, then point to the automated checks and model judge.*

> Each method got the same fifty tasks: sixteen each on validation, parsing, and dependency behavior, plus two with missing requirements. Single-shot ran once per task. Each agent ran three times. The shared grader ran pytest on generated test files. A separate model judge checked task rubrics and missing-requirement explanations.

## 1:33–2:00 · Results

*Slide 5. Highlight task accuracy, coverage, and generation cost.*

> Pytest counts show how many generated tests passed. Line coverage shows which statements ran, and branch coverage shows which decision paths ran. Together they measure how well the generated tests exercised the codebase.
>
> ReAct passed fifty-eight percent of tasks versus forty-six percent for single-shot. ReAct averaged sixteen seconds, about eight model turns, and twenty-six thousand tokens. Single-shot averaged five seconds, one turn, and sixteen hundred tokens.

## 2:00–3:00 · Prerecorded demo

### 2:00–2:22 · Generate

*Show the Python codebase and submit **“Test the maximum allowed retries.”** Show the generated test file and **Verification**.*

> I’ll use the same Python codebase from the benchmark. I ask for a test of the maximum retry count. In the generated test file, this assertion checks that passing five returns five. The Verification panel shows whether pytest passed.

### 2:22–2:37 · Ask

*Enter **“Which retry values did the generated tests cover, and did pytest pass?”** Click **Ask** and show the answer.*

> Next I ask which retry values the tests covered and whether pytest passed. Ask uses the earlier results to answer. The verified test files stay active.

### 2:37–3:00 · Revise

*Enter **“Parameterize the accepted cases for 4 and 5 and verify that 6 raises ValueError.”** Click **Revise tests**. Show the updated test file and fresh verification.*

> Finally, I ask for one parameterized test that accepts four and five, plus a test that checks whether six raises a value error. The agent updates the test file and runs pytest again. I can review the revised tests and their verification results before adopting them.
