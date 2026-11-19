# Evaluation results

DeepSeek Flash generated and judged the attempts. We evaluated 50 tasks, including seven edge cases and two unanswerable tasks. The baseline ran once per task, and each agent ran three times per task, for 350 attempts total.

| Metric | Single-shot | ReAct | Plan-and-Execute |
| --- | ---: | ---: | ---: |
| Accuracy | 46.0% | 58.0% | 56.0% |
| Average model turns | 1.00 (50/50) | 7.54 (50/50) | 10.12 (50/50) |
| Average latency (s) | 5.26 | 16.14 | 30.35 |
| p95 latency (s) | 13.01 | 29.78 | 50.40 |
| Average tokens | 1622.30 (50/50) | 25750.98 (50/50) | 35398.80 (49/50) |
| pass@3 | N/A | 32/50 (64.0%) | 34/50 (68.0%) |
| pass^3 | N/A | 22/50 (44.0%) | 22/50 (44.0%) |

Accuracy and generation cost use the baseline attempt and each agent’s first trial. Latency and token counts exclude independent grading. One Plan-and-Execute first trial had no token count. Consistency metrics use all three agent trials.

## Tasks that flipped for ReAct

- validation-07: pass, pass, fail
- validation-08: pass, pass, fail
- parsing-08: fail, pass, fail
- parsing-12: fail, fail, pass
- dependency-05: pass, fail, pass
- dependency-06: pass, fail, pass
- dependency-10: pass, pass, fail
- dependency-14: pass, fail, fail
- unanswerable-01: pass, pass, fail
- unanswerable-02: fail, pass, fail

## Tasks that flipped for Plan-and-Execute

- validation-08: fail, fail, pass
- validation-10: fail, pass, pass
- validation-16: pass, fail, fail
- parsing-08: pass, pass, fail
- parsing-09: fail, fail, pass
- parsing-10: fail, pass, fail
- dependency-01: pass, fail, pass
- dependency-02: fail, pass, fail
- dependency-06: pass, fail, fail
- dependency-15: fail, fail, pass
- unanswerable-01: pass, pass, fail
- unanswerable-02: pass, fail, fail

## Failure analysis

On `validation-07`, the single-shot baseline chose the inputs `"0"`, `"1"`, `"5"`, `"03"`, and `" 4 "` for its generated test. All five parameterized cases passed in pytest. The rubric required an assertion that `retries("3")` raises `TypeError`. The baseline omitted that exact input during test generation, so the grader failed the attempt on completeness.
