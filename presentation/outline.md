# Agentic Unit Testing - 3 minutes

## Problem: What problem are you solving, and why does it matter?

The Agent generate pytest tests from plain-language goals for an existing Python repository. The hard part is translating a request like “test the maximum allowed retries” into the whole sequence of steps needed to implement the test, including understanding the codebase, identifying the relevant functions and classes, and writing the test code, run the generated tests, and revise them. The agent must also be able to verify that the generated tests are correct and safe to run. Storytelling should focus on the automation of the complete workflow.

Explain what the agent is given and what it produces

## Agent design and baseline: Why does this problem benefit from an agent, and how does your design provide the capabilities needed to solve it compared with a non-agentic baseline?

### Why one-shot prompting is insufficient

- One-shot cannot understand the codebase correctly, and it cannot verify that the generated tests are correct and safe to run.
- It cannot run the actual tests, and it cannot revise the generated tests based on the results of running them.

### How baseline is designed - refer to /unit-agent code

### How Our agent is designed - refer to /unit-agent code

- Make sure to include the design flowchart
- Demonstrate agent's ability(refer to tools and agent loop)
- Memory system
  - Agentic RAG is used to retrieve relevant code snippets from the codebase and store them in memory for future reference.
  - Chat session management is used to keep track of the conversation history and the state of the agent's reasoning process, so that follow-up questions and revisions can be handled.
- Safety layer - refer to the commit add security

## Evaluation and results: How do your benchmark tasks and metrics test those capabilities? What do the results tell you about your agent’s strengths, limitations, and tradeoffs?

- Explain the evaluation task types
- Explain how each metric is calculated or measured in one sentence and what it means in one sentence.
- Display the full report and make comparisons. 

## Live demo screen recording - 1 minute

0. Explain the fixture codebase in a few words.
1. Initial prompt task: Test the maximum allowed retries.
2. "Ask" feature, be able to ask follow-up questions to the agent.
3. "Revise tests" feature, be able to make follow-up revisions to the generated tests.