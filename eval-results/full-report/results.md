# Evaluation results for 50 tasks

| Metric | Single-shot | ReAct trial 1 | Plan-and-Execute trial 1 |
| --- | ---: | ---: | ---: |
| Accuracy | 46.0% | 58.0% | 56.0% |
| Average model turns | 1.00 (50/50) | 7.54 (50/50) | 10.12 (50/50) |
| Average latency (s) | 5.26 | 16.14 | 30.35 |
| p95 latency (s) | 13.01 | 29.78 | 50.40 |
| Average tokens | 1622.30 (50/50) | 25750.98 (50/50) | 35398.80 (49/50) |
| Generated tests passed / generated | 134/134 (48/50 attempts) | 442/442 (48/50 attempts) | 446/446 (46/50 attempts) |
| Average production line coverage (%) | 37.22 | 48.54 | 48.48 |
| Average production branch coverage (%) | 21.70 | 34.20 | 34.96 |

## ReAct consistency

- pass@3: 32/50 (64.0%)
- pass^3: 22/50 (44.0%)

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

## Plan-and-Execute consistency

- pass@3: 34/50 (68.0%)
- pass^3: 22/50 (44.0%)

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

## Per-task verdicts

| Task | Single-shot | ReAct 1 | ReAct 2 | ReAct 3 | Plan-and-Execute 1 | Plan-and-Execute 2 | Plan-and-Execute 3 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| validation-01 | Pass · 2/2 | Pass · 6/6 | Pass · 5/5 | Pass · 8/8 | Pass · 7/7 | Pass · 15/15 | Pass · 7/7 |
| validation-02 | Pass · 2/2 | Pass · 11/11 | Pass · 2/2 | Pass · 10/10 | Pass · 19/19 | Pass · 19/19 | Pass · 14/14 |
| validation-03 | Pass · 1/1 | Pass · 5/5 | Pass · 2/2 | Pass · 12/12 | Pass · 5/5 | Pass · 6/6 | Pass · 3/3 |
| validation-04 | Pass · 1/1 | Pass · 2/2 | Pass · 1/1 | Pass · 3/3 | Pass · 4/4 | Pass · 1/1 | Pass · 2/2 |
| validation-05 | Pass · 4/4 | Pass · 4/4 | Pass · 21/21 | Pass · 8/8 | Pass · 13/13 | Pass · 12/12 | Pass · 12/12 |
| validation-06 | Pass · 2/2 | Pass · 6/6 | Pass · 4/4 | Pass · 2/2 | Pass · 7/7 | Pass · 5/5 | Pass · 7/7 |
| validation-07 | Fail (rubric) · 5/5 | Pass · 16/16 | Pass · 10/10 | Fail (rubric) · 10/10 | Pass · 20/20 | Pass · 47/47 | Pass · 2/2 |
| validation-08 | Fail (rubric) · 1/1 | Pass · 5/5 | Pass · 4/4 | Fail (rubric) · 8/8 | Fail (rubric) · 8/8 | Fail (rubric) · 24/24 | Pass · 11/11 |
| validation-09 | Pass · 1/1 | Pass · 8/8 | Pass · 4/4 | Pass · 7/7 | Pass · 15/15 | Pass · 4/4 | Pass · 14/14 |
| validation-10 | Fail (rubric) · 1/1 | Fail (rubric) · 6/6 | Fail (judge) · 7/7 | Fail (rubric) · 5/5 | Fail (rubric) · 7/7 | Pass · 5/5 | Pass · 7/7 |
| validation-11 | Fail (rubric) · 6/6 | Fail (rubric) · 7/7 | Fail (rubric) · 6/6 | Fail (rubric) · 14/14 | Fail (rubric) · 2/2 | Fail (rubric) · 8/8 | Fail (rubric) · 7/7 |
| validation-12 | Pass · 9/9 | Pass · 7/7 | Pass · 6/6 | Pass · 3/3 | Pass · 15/15 | Pass · 15/15 | Pass · 10/10 |
| validation-13 | Fail (rubric) · 6/6 | Fail (rubric) · 9/9 | Fail (judge) · 17/17 | Fail (rubric) · 11/11 | Fail (rubric) · 9/9 | Fail (rubric) · 11/11 | Fail (rubric) · 37/37 |
| validation-14 | Pass · 3/3 | Pass · 3/3 | Pass · 6/6 | Pass · 11/11 | Pass · 7/7 | Pass · 10/10 | Pass · 5/5 |
| validation-15 | Fail (rubric) · 6/6 | Fail (rubric) · 18/18 | Fail (rubric) · 17/17 | Fail (rubric) · 13/13 | Fail (rubric) · 14/14 | Fail (rubric) · 8/8 | Fail (rubric) · 11/11 |
| validation-16 | Fail (rubric) · 5/5 | Fail (rubric) · 19/19 | Fail (rubric) · 15/15 | Fail (rubric) · 14/14 | Pass · 10/10 | Fail (rubric) · 9/9 | Fail (judge) · 34/34 |
| parsing-01 | Pass · 1/1 | Pass · 12/12 | Pass · 6/6 | Pass · 10/10 | Pass · 5/5 | Pass · 8/8 | Pass · 7/7 |
| parsing-02 | Pass · 1/1 | Pass · 6/6 | Pass · 8/8 | Pass · 6/6 | Pass · 14/14 | Pass · 9/9 | Pass · 3/3 |
| parsing-03 | Pass · 1/1 | Pass · 10/10 | Pass · 2/2 | Pass · 5/5 | Pass · 5/5 | Pass · 6/6 | Pass · 3/3 |
| parsing-04 | Fail (rubric) · 4/4 | Fail (rubric) · 4/4 | Fail (rubric) · 10/10 | Fail (rubric) · 8/8 | Fail (generation) | Fail (rubric) · 13/13 | Fail (rubric) · 6/6 |
| parsing-05 | Fail (rubric) · 3/3 | Fail (rubric) · 5/5 | Fail (rubric) · 4/4 | Fail (rubric) · 16/16 | Fail (rubric) · 4/4 | Fail (rubric) · 9/9 | Fail (rubric) · 41/41 |
| parsing-06 | Fail (rubric) · 1/1 | Fail (rubric) · 1/1 | Fail (rubric) · 7/7 | Fail (rubric) · 7/7 | Fail (rubric) · 6/6 | Fail (rubric) · 10/10 | Fail (rubric) · 6/6 |
| parsing-07 | Pass · 1/1 | Pass · 2/2 | Pass · 4/4 | Pass · 3/3 | Pass · 1/1 | Pass · 2/2 | Pass · 2/2 |
| parsing-08 | Pass · 3/3 | Fail (rubric) · 10/10 | Pass · 19/19 | Fail (rubric) · 2/2 | Pass · 4/4 | Pass · 8/8 | Fail (rubric) · 12/12 |
| parsing-09 | Fail (rubric) · 4/4 | Fail (rubric) · 3/3 | Fail (rubric) · 5/5 | Fail (rubric) · 7/7 | Fail (rubric) · 3/3 | Fail (rubric) · 1/1 | Pass · 8/8 |
| parsing-10 | Fail (rubric) · 3/3 | Pass · 9/9 | Pass · 9/9 | Pass · 10/10 | Fail (rubric) · 13/13 | Pass · 14/14 | Fail (rubric) · 8/8 |
| parsing-11 | Fail (rubric) · 5/5 | Fail (rubric) · 10/10 | Fail (rubric) · 16/16 | Fail (rubric) · 10/10 | Fail (rubric) · 33/33 | Fail (judge) · 31/31 | Fail (rubric) · 12/12 |
| parsing-12 | Pass · 3/3 | Fail (rubric) · 3/3 | Fail (generation) | Pass · 12/12 | Pass · 8/8 | Pass · 16/16 | Pass · 11/11 |
| parsing-13 | Fail (rubric) · 1/1 | Fail (rubric) · 7/7 | Fail (rubric) · 5/5 | Fail (rubric) · 5/5 | Fail (rubric) · 8/8 | Fail (rubric) · 4/4 | Fail (rubric) · 8/8 |
| parsing-14 | Pass · 3/3 | Pass · 19/19 | Pass · 9/9 | Pass · 8/8 | Pass · 10/10 | Pass · 10/10 | Pass · 7/7 |
| parsing-15 | Fail (rubric) · 3/3 | Fail (rubric) · 14/14 | Fail (rubric) · 5/5 | Fail (rubric) · 8/8 | Fail (rubric) · 7/7 | Fail (rubric) · 10/10 | Fail (rubric) · 10/10 |
| parsing-16 | Fail (rubric) · 1/1 | Fail (rubric) · 15/15 | Fail (rubric) · 8/8 | Fail (rubric) · 7/7 | Fail (rubric) · 11/11 | Fail (rubric) · 12/12 | Fail (rubric) · 9/9 |
| dependency-01 | Fail (rubric) · 1/1 | Pass · 5/5 | Pass · 11/11 | Pass · 22/22 | Pass · 5/5 | Fail (rubric) · 7/7 | Pass · 11/11 |
| dependency-02 | Pass · 1/1 | Fail (rubric) · 2/2 | Fail (rubric) · 9/9 | Fail (rubric) · 4/4 | Fail (rubric) · 8/8 | Pass · 8/8 | Fail (rubric) · 4/4 |
| dependency-03 | Pass · 1/1 | Pass · 2/2 | Pass · 11/11 | Pass · 5/5 | Pass · 7/7 | Pass · 7/7 | Pass · 6/6 |
| dependency-04 | Pass · 1/1 | Pass · 5/5 | Pass · 3/3 | Pass · 2/2 | Pass · 1/1 | Pass · 4/4 | Pass · 1/1 |
| dependency-05 | Pass · 1/1 | Pass · 3/3 | Fail (generation) | Pass · 8/8 | Fail (generation) | Fail (judge) · 10/10 | Fail (generation) |
| dependency-06 | Fail (rubric) · 1/1 | Pass · 12/12 | Fail (generation) | Pass · 6/6 | Pass · 6/6 | Fail (generation) | Fail (generation) |
| dependency-07 | Pass · 5/5 | Pass · 45/45 | Pass · 8/8 | Pass · 32/32 | Pass · 16/16 | Pass · 16/16 | Pass · 19/19 |
| dependency-08 | Pass · 4/4 | Pass · 4/4 | Pass · 4/4 | Pass · 20/20 | Pass · 32/32 | Pass · 31/31 | Pass · 38/38 |
| dependency-09 | Pass · 7/7 | Pass · 43/43 | Pass · 52/52 | Pass · 16/16 | Pass · 11/11 | Pass · 19/19 | Pass · 35/35 |
| dependency-10 | Fail (rubric) · 2/2 | Pass · 8/8 | Pass · 9/9 | Fail (rubric) · 7/7 | Pass · 10/10 | Pass · 3/3 | Pass · 4/4 |
| dependency-11 | Fail (rubric) · 3/3 | Fail (rubric) · 9/9 | Fail (rubric) · 3/3 | Fail (rubric) · 8/8 | Fail (rubric) · 11/11 | Fail (rubric) · 13/13 | Fail (rubric) · 5/5 |
| dependency-12 | Fail (rubric) · 6/6 | Fail (rubric) · 6/6 | Fail (rubric) · 12/12 | Fail (rubric) · 8/8 | Fail (rubric) · 10/10 | Fail (rubric) · 7/7 | Fail (rubric) · 9/9 |
| dependency-13 | Fail (rubric) · 4/4 | Fail (rubric) · 14/14 | Fail (rubric) · 29/29 | Fail (rubric) · 11/11 | Fail (rubric) · 24/24 | Fail (rubric) · 9/9 | Fail (rubric) · 22/22 |
| dependency-14 | Fail (rubric) · 1/1 | Pass · 1/1 | Fail (rubric) · 1/1 | Fail (rubric) · 4/4 | Fail (rubric) · 4/4 | Fail (rubric) · 4/4 | Fail (rubric) · 4/4 |
| dependency-15 | Fail (rubric) · 2/2 | Pass · 12/12 | Pass · 9/9 | Pass · 6/6 | Fail (rubric) · 2/2 | Fail (rubric) · 7/7 | Pass · 8/8 |
| dependency-16 | Fail (rubric) · 1/1 | Fail (rubric) · 9/9 | Fail (rubric) · 6/6 | Fail (rubric) · 1/1 | Fail (rubric) · 5/5 | Fail (rubric) · 7/7 | Fail (rubric) · 11/11 |
| unanswerable-01 | Fail (rubric) | Pass | Pass | Fail (rubric) | Pass | Pass | Fail (generation) |
| unanswerable-02 | Fail (rubric) | Fail (rubric) | Pass | Fail (rubric) | Pass | Fail (rubric) | Fail (generation) |

Fractions in verdict cells show generated pytest cases passed / collected.
Accuracy compares single-shot with trial 1 for each agent. Consistency uses all three trials.
Generation latency and tokens exclude shared grading and judge calls.

## Retry boundary mutation

- baseline trial 1: detected
- react trial 1: detected
- react trial 2: detected
- react trial 3: detected
- plan-execute trial 1: detected
- plan-execute trial 2: detected
- plan-execute trial 3: detected

## Failure trace

validation-07 (baseline, trial 1) failed at the rubric step. Complete — It tests several numeric strings but does not include the explicitly requested retries('3') case, so the requested specific behavior is not fully covered. See attempts.jsonl for the recorded evidence.

### Failed attempts

- **validation-07 · baseline 1** (rubric) — Complete — It tests several numeric strings but does not include the explicitly requested retries('3') case, so the requested specific behavior is not fully covered.
- **validation-07 · react 3** (rubric) — Assert retries('3') raises TypeError. — The parametrized cases include ' 3 ' but do not assert retries('3') specifically; there is no exact call to retries('3').
- **validation-08 · baseline 1** (rubric) — Correct — The submission tests retries(2.0), not the specified retries(3.0), so it does not match the required assertion.
- **validation-08 · react 3** (rubric) — Assert retries(3.0) raises TypeError. — The candidate does not assert retries(3.0) raises TypeError; it uses other integral float values such as 2.0, 1.0, 0.0, 5.0, and 9.0.
- **validation-08 · plan-execute 1** (rubric) — Complete — The tests cover integral floats generally but omit the explicitly requested exact case retries(3.0), so the requested behavior is not fully verified.
- **validation-08 · plan-execute 2** (rubric) — Complete — The requested exact behavior is not covered: no test asserts retries(3.0); the suite uses 2.0 and other floats instead.
- **validation-10 · baseline 1** (rubric) — Correct — The candidate test uses a different whitespace pattern than the specified label with two leading spaces and a trailing tab, so it does not match the reference assertion exactly.
- **validation-10 · react 1** (rubric) — Correct — Candidate tests pass, but they do not match the requested exact assertion for label with two leading spaces, 'blue', and a trailing tab.
- **validation-10 · react 2** (judge) — Judge request or response failed (APITimeoutError).
- **validation-10 · react 3** (rubric) — Assert label(' blue\t') returns 'blue'. — No test asserts label(' blue\t') == 'blue' exactly; the closest assertion is label(' \tblue\t ') == 'blue'.
- **validation-10 · plan-execute 1** (rubric) — Assert label(' blue\t') returns 'blue'. — No exact assertion for the requested two-leading-space label literal; candidate uses label(" blue\t") with one leading space and other whitespace cases.
- **validation-11 · baseline 1** (rubric) — Assert label(' blue team ') returns 'blue team'. — The submission does not assert label(' blue team ') == 'blue team'; it only tests equivalent blue/green cases.
- **validation-11 · react 1** (rubric) — Assert label(' blue team ') returns 'blue team'. — No assertion for label(' blue team ') == 'blue team'; the closest test uses ' North America ' instead.
- **validation-11 · react 2** (rubric) — Assert label(' blue team ') returns 'blue team'. — No test asserts label(' blue team ') == 'blue team'; the candidate uses other examples such as 'blue sky', 'red green', and 'a b'.
- **validation-11 · react 3** (rubric) — Assert label(' blue team ') returns 'blue team'. — The exact assertion label(' blue team ') == 'blue team' is not present; the tests use analogous values such as ' big blue ' instead.
- **validation-11 · plan-execute 1** (rubric) — Complete — The submission tests a single interior space in 'blue green' but does not cover the specified multiple-space case 'blue team', so it does not fully verify that multiple internal spaces survive normalization.
- **validation-11 · plan-execute 2** (rubric) — Complete — The tests broadly cover internal spaces but omit the explicitly requested assertion for label(' blue team ').
- **validation-11 · plan-execute 3** (rubric) — Assert label(' blue team ') returns 'blue team'. — No test asserts label(' blue team ') == 'blue team'; the closest tests use strings like ' two words ' and 'a b'.
- **validation-13 · baseline 1** (rubric) — Assert label(' \t\n') raises ValueError. — The parametrization does not include the exact requested input label(' \t\n'); it uses ' \t\n\r ' instead, so the exact assertion is not present.
- **validation-13 · react 1** (rubric) — Complete — The tests cover several whitespace-only labels and integration paths, but they do not include the specifically requested exact assertion for label(' \t\n').
- **validation-13 · react 2** (judge) — Judge request or response failed (APITimeoutError).
- **validation-13 · react 3** (rubric) — Assert label(' \t\n') raises ValueError. — No exact assertion for the specified space-tab-newline input; the parametrization includes a similar whitespace-only value with a trailing space plus separate tab/newline cases, but not the exact requested input.
- **validation-13 · plan-execute 1** (rubric) — Assert label(' \t\n') raises ValueError. — The parametrized cases include whitespace combinations but not the exact requested call label(' \t\n'); the closest case has an extra trailing space.
- **validation-13 · plan-execute 2** (rubric) — Assert label(' \t\n') raises ValueError. — No test directly asserts label with the exact space-tab-newline string; the closest batch_size case has an extra trailing space.
- **validation-13 · plan-execute 3** (rubric) — Assert label(' \t\n') raises ValueError. — No test calls label with the exact literal ' \t\n'; the closest parametrized value is ' \t\n ' with an extra trailing space, so the specific requested assertion is not present.
- **validation-15 · baseline 1** (rubric) — Assert label(' BlueTeam ') returns 'BlueTeam'. — No test asserts label(' BlueTeam ') == 'BlueTeam'; the closest is label(' MiXeD Case ') == 'MiXeD Case'.
- **validation-15 · react 1** (rubric) — Assert label(' BlueTeam ') returns 'BlueTeam'. — No test asserts label(' BlueTeam ') == 'BlueTeam'; the closest cases use ' Blue ', 'Blue', and 'MixedCaseName', so the specific requested assertion is missing.
- **validation-15 · react 2** (rubric) — Assert label(' BlueTeam ') returns 'BlueTeam'. — No assertion checks label(' BlueTeam ') == 'BlueTeam'; the closest cases use 'Blue' and 'BlueThing', not the requested ' BlueTeam ' input.
- **validation-15 · react 3** (rubric) — Complete — Broad case-preservation coverage exists, but the explicitly requested assertion for label(' BlueTeam ') == 'BlueTeam' is absent.
- **validation-15 · plan-execute 1** (rubric) — Complete — The suite broadly covers case preservation but does not include the specifically requested assertion for label(' BlueTeam ') returning 'BlueTeam'.
- **validation-15 · plan-execute 2** (rubric) — Complete — The suite broadly covers case preservation but does not verify the specifically requested case label(' BlueTeam ') returning 'BlueTeam'.
- **validation-15 · plan-execute 3** (rubric) — Assert label(' BlueTeam ') returns 'BlueTeam'. — There is no assertion for label(' BlueTeam ') == 'BlueTeam'; tests use other strings such as ' Blue ', ' Blue Lagoon ', and 'BigBlue' instead.
- **validation-16 · baseline 1** (rubric) — Assert label(' café ') returns 'café'. — The required exact assertion label(' café ') == 'café' is not present; the test uses label(' café ') with two leading and trailing spaces instead.
- **validation-16 · react 1** (rubric) — Assert label(' café ') returns 'café'. — No exact assertion label(' café ') == 'café'; the closest test uses two spaces on each side, e.g. label(' café ') == 'café', not the requested single-space call.
- **validation-16 · react 2** (rubric) — Assert label(' café ') returns 'café'. — There is no exact assertion for label(' café ') == 'café'; the tests use two surrounding spaces instead of the requested single leading/trailing space.
- **validation-16 · react 3** (rubric) — Assert label(' café ') returns 'café'. — No direct assertion label(' café ') == 'café'; tests use two spaces plus tabs or indirect parse/service variants instead.
- **validation-16 · plan-execute 2** (rubric) — Complete — Covers Unicode preservation broadly but omits the explicitly requested label(' café ') case with ASCII surrounding spaces.
- **validation-16 · plan-execute 3** (judge) — Judge request or response failed (APITimeoutError).
- **parsing-04 · baseline 1** (rubric) — Assert parse_record(':2') raises ValueError. — The submission does not assert parse_record(':2') raises ValueError; it uses ':3', ':0', and whitespace variants instead.
- **parsing-04 · react 1** (rubric) — Assert parse_record(':2') raises ValueError. — No assertion calls parse_record(':2'); the candidate uses parse_record(':3') and parse_record(' :3') instead.
- **parsing-04 · react 2** (rubric) — Assert parse_record(':2') raises ValueError. — No test asserts parse_record(':2') raises ValueError; the added tests use ':3', ':0', ' :7', '\t:1', and other cases, but never ':2'.
- **parsing-04 · react 3** (rubric) — In policy — No forbidden source edits, but the explanation claims 72.7% line coverage while supplied coverage is 60.0%; that is an unsupported factual claim.
- **parsing-04 · plan-execute 1** (generation) — No test candidate was produced. Model request failed (APIConnectionError).
- **parsing-04 · plan-execute 2** (rubric) — Assert parse_record(':2') raises ValueError. — No test asserts parse_record(':2') raises ValueError; the empty-name cases use ':3', ' :3', ' :3', '\t:3', ' :0', ':abc', and ':not-a-count'.
- **parsing-04 · plan-execute 3** (rubric) — Assert parse_record(':2') raises ValueError. — No test calls parse_record(':2'); the empty-name parse_record tests use ':3' instead.
- **parsing-05 · baseline 1** (rubric) — Assert parse_record(' :2') raises ValueError. — No assertion calls parse_record(' :2'); the parametrized cases use different whitespace-only inputs.
- **parsing-05 · react 1** (rubric) — Assert parse_record(' :2') raises ValueError. — No assertion calls parse_record(' :2'); the candidate uses other whitespace-only inputs such as three spaces with count 3 and a tab/newline case.
- **parsing-05 · react 2** (rubric) — Assert parse_record(' :2') raises ValueError. — No test calls parse_record(' :2'); the closest cases are ' :3', '\t:3', and ' :0'.
- **parsing-05 · react 3** (rubric) — Assert parse_record(' :2') raises ValueError. — No test asserts the exact requested input parse_record(' :2'); the parametrized parse_record cases use ':3', and other cases use ' :0' or ' :not-a-number'.
- **parsing-05 · plan-execute 1** (rubric) — Assert parse_record(' :2') raises ValueError. — No test asserts parse_record(' :2') specifically; it uses ' :3' and '\t\n :0' instead.
- **parsing-05 · plan-execute 2** (rubric) — Assert parse_record(' :2') raises ValueError. — No test asserts parse_record(' :2') raises ValueError; the submission uses parse_record(' :3') and parse_record(' :not-a-number') instead, so the specifically requested assertion is missing.
- **parsing-05 · plan-execute 3** (rubric) — Assert parse_record(' :2') raises ValueError. — No test asserts exactly parse_record(' :2') raises ValueError; the parametrized cases use other whitespace names/counts, such as ' :3', not the requested two-space name with count 2.
- **parsing-06 · baseline 1** (rubric) — Assert parse_record('blue:2:3') raises ValueError. — It asserts parse_record('blue:3:4') raises ValueError, not the specifically requested parse_record('blue:2:3').
- **parsing-06 · react 1** (rubric) — Assert parse_record('blue:2:3') raises ValueError. — The test uses parse_record('blue:3:4'), not the required parse_record('blue:2:3').
- **parsing-06 · react 2** (rubric) — Complete — The suite tests several two-separator inputs but omits the explicitly requested parse_record('blue:2:3') case, so it does not fully address the specified assertion.
- **parsing-06 · react 3** (rubric) — Complete — The submission covers several two-separator examples but does not include the specifically requested `parse_record('blue:2:3')` case.
- **parsing-06 · plan-execute 1** (rubric) — Assert parse_record('blue:2:3') raises ValueError. — No test asserts parse_record('blue:2:3') raises ValueError; the two-separator test uses 'blue:3:4' instead.
- **parsing-06 · plan-execute 2** (rubric) — Assert parse_record('blue:2:3') raises ValueError. — No assertion calls parse_record('blue:2:3'); the tests use other two-separator inputs such as 'blue:3:4'.
- **parsing-06 · plan-execute 3** (rubric) — Assert parse_record('blue:2:3') raises ValueError. — No test asserts parse_record('blue:2:3') raises ValueError; it uses 'blue:3:4' and other two-separator variants instead.
- **parsing-08 · react 1** (rubric) — Complete — The suite covers several fractional inputs but omits the specifically requested 'blue:1.5' case, so it does not fully verify every requested behavior.
- **parsing-08 · react 3** (rubric) — Complete — It tests parse_record('blue:2.5'), not the requested parse_record('blue:1.5'), so the exact requested assertion is missing.
- **parsing-08 · plan-execute 3** (rubric) — Assert parse_record('blue:1.5') raises ValueError. — No test asserts parse_record('blue:1.5') raises ValueError; the fractional inputs used are 'blue:2.5', 'blue:0.5', 'blue:1.0', 'blue:3.75', and separately 'blue:2.9'.
- **parsing-09 · baseline 1** (rubric) — Assert parse_record('blue:many') raises ValueError. — The test does not explicitly assert parse_record('blue:many') raises ValueError; it parametrizes other alphabetic counts instead.
- **parsing-09 · react 1** (rubric) — Complete — The submission covers alphabetic-count rejection generally but omits the specifically requested assertion for parse_record('blue:many').
- **parsing-09 · react 2** (rubric) — Assert parse_record('blue:many') raises ValueError. — No test asserts parse_record('blue:many') raises ValueError; the parametrized cases are 'blue:abc', 'blue:x', ' :abc', and 'blue:1a'.
- **parsing-09 · react 3** (rubric) — Assert parse_record('blue:many') raises ValueError. — No test asserts parse_record('blue:many') raises ValueError; the closest cases use 'blue:abc', 'blue:x', and 'blue:3a'.
- **parsing-09 · plan-execute 1** (rubric) — Assert parse_record('blue:many') raises ValueError. — The test uses parse_record('blue:abc'), not the required parse_record('blue:many').
- **parsing-09 · plan-execute 2** (rubric) — Assert parse_record('blue:many') raises ValueError. — It asserts parse_record('blue:abc') rather than the specifically requested parse_record('blue:many').
- **parsing-10 · baseline 1** (rubric) — Assert parse_record('blue:12abc') raises ValueError. — The exact assertion parse_record('blue:12abc') raising ValueError is absent; the test uses 'blue:123abc' and other variants instead.
- **parsing-10 · plan-execute 1** (rubric) — Complete — The goal is covered broadly, but the explicit required assertion for parse_record('blue:12abc') is omitted, so coverage is not complete.
- **parsing-10 · plan-execute 3** (rubric) — Complete — The suite covers multiple digit-leading, letter-trailing counts but does not include the explicitly requested exact case parse_record('blue:12abc'), so the requested behavior is not fully addressed.
- **parsing-11 · baseline 1** (rubric) — Assert parse_record(' blue : 12 ') returns ('blue', 12). — No assertion uses parse_record(' blue : 12 '); candidate instead asserts parse_record(' blue : 3 ') and tab variants.
- **parsing-11 · react 1** (rubric) — Assert parse_record(' blue : 12 ') returns ('blue', 12). — No test asserts parse_record(' blue : 12 ') == ('blue', 12); the closest test uses parse_record(' blue : 3 ') and different spacing/count.
- **parsing-11 · react 2** (rubric) — Complete — The required exact assertion parse_record(' blue : 12 ') == ('blue', 12) is missing; tests use other names and counts such as blue:3 and a:0.
- **parsing-11 · react 3** (rubric) — Assert parse_record(' blue : 12 ') returns ('blue', 12). — No test asserts parse_record(' blue : 12 ') == ('blue', 12); the closest cases use 'blue :3' and an 'order batch : 12' variant.
- **parsing-11 · plan-execute 1** (rubric) — Assert parse_record(' blue : 12 ') returns ('blue', 12). — No test calls parse_record(' blue : 12 ') or asserts that it returns ('blue', 12); the parameterized cases use count 3 instead.
- **parsing-11 · plan-execute 2** (judge) — Judge request or response failed (APITimeoutError).
- **parsing-11 · plan-execute 3** (rubric) — Assert parse_record(' blue : 12 ') returns ('blue', 12). — The exact assertion parse_record(' blue : 12 ') == ('blue', 12) is absent; the suite uses other whitespace/count examples such as ' blue : 3 '.
- **parsing-12 · react 1** (rubric) — Assert parse_record('blue:007') returns ('blue', 7). — The added tests assert parse_record('blue:003') == ('blue', 3), but they do not assert parse_record('blue:007') == ('blue', 7) as explicitly requested.
- **parsing-12 · react 2** (generation) — No test candidate was produced. No test was staged (diff intentionally empty). The only count parsing in the fixture is parsing.parse_record, whose docstring says merely 'Return (stripped name, count). Count must be a nonnegative integer.' It defines no lexical rule for leading zeros: the impleme...
- **parsing-13 · baseline 1** (rubric) — Correct — Candidate asserts parse_record('blue:+3') == ('blue', 3), not the reference expectation parse_record('blue:+7') == ('blue', 7).
- **parsing-13 · react 1** (rubric) — Assert parse_record('blue:+7') returns ('blue', 7). — It does not assert parse_record('blue:+7') == ('blue', 7); it tests +3 exactly and +7 only with surrounding whitespace.
- **parsing-13 · react 2** (rubric) — Assert parse_record('blue:+7') returns ('blue', 7). — No test asserts parse_record('blue:+7') == ('blue', 7); the file tests +3, +12, and +0 instead.
- **parsing-13 · react 3** (rubric) — Assert parse_record('blue:+7') returns ('blue', 7). — No assertion for parse_record('blue:+7') == ('blue', 7); the tests use '+3', '+0', and '+120' instead.
- **parsing-13 · plan-execute 1** (rubric) — Assert parse_record('blue:+7') returns ('blue', 7). — It does not include the exact required assertion parse_record('blue:+7') == ('blue', 7); the closest is parse_record(' blue : +7 ') == ('blue', 7).
- **parsing-13 · plan-execute 2** (rubric) — Assert parse_record('blue:+7') returns ('blue', 7). — The required assertion parse_record('blue:+7') == ('blue', 7) is absent; the tests use +3, +0, and +12 instead.
- **parsing-13 · plan-execute 3** (rubric) — Assert parse_record('blue:+7') returns ('blue', 7). — No test asserts parse_record('blue:+7') == ('blue', 7); the plus-sign positive tests use +3, +0, and +12 instead.
- **parsing-15 · baseline 1** (rubric) — Assert parse_record('blue team:2') returns ('blue team', 2). — No test calls parse_record('blue team:2') or asserts it returns ('blue team', 2); the added cases use names like 'blue jeans' with count 3.
- **parsing-15 · react 1** (rubric) — Assert parse_record('blue team:2') returns ('blue team', 2). — No test asserts parse_record('blue team:2') == ('blue team', 2); the exact requested assertion is absent, though similar interior-space cases are tested.
- **parsing-15 · react 2** (rubric) — Assert parse_record('blue team:2') returns ('blue team', 2). — No test asserts parse_record('blue team:2') == ('blue team', 2); the added cases use 'blue green' variants instead.
- **parsing-15 · react 3** (rubric) — Assert parse_record('blue team:2') returns ('blue team', 2). — No assertion uses parse_record('blue team:2') or expects ('blue team', 2); the closest tests use different names and counts.
- **parsing-15 · plan-execute 1** (rubric) — Assert parse_record('blue team:2') returns ('blue team', 2). — No test asserts parse_record('blue team:2') == ('blue team', 2); the added tests use other names such as 'light blue' and 'a b'.
- **parsing-15 · plan-execute 2** (rubric) — Assert parse_record('blue team:2') returns ('blue team', 2). — The candidate diff does not include the exact required assertion parse_record('blue team:2') == ('blue team', 2); it tests analogous names such as 'light blue' and 'a b c' instead.
- **parsing-15 · plan-execute 3** (rubric) — Assert parse_record('blue team:2') returns ('blue team', 2). — There is no assertion for parse_record('blue team:2') == ('blue team', 2); the candidate uses names such as 'blue green' instead.
- **parsing-16 · baseline 1** (rubric) — Complete — The test covers consecutive records generally but omits the specifically requested assertions for parse_record('blue:4') and parse_record('red:9').
- **parsing-16 · react 1** (rubric) — Complete — The suite broadly covers consecutive records, but it omits the specifically required parse_record('red:9') assertion.
- **parsing-16 · react 2** (rubric) — Assert parse_record('blue:4') and parse_record('red:9') return their respective pairs. — The exact assertion is absent: the test uses parse_record('blue:3') and parse_record('red:9'), not parse_record('blue:4').
- **parsing-16 · react 3** (rubric) — Complete — It covers consecutive records broadly but does not verify the explicitly requested parse_record('blue:4') and parse_record('red:9') pair, so not all requested behavior is covered.
- **parsing-16 · plan-execute 1** (rubric) — Assert parse_record('blue:4') and parse_record('red:9') return their respective pairs. — The diff does not assert parse_record('blue:4') and parse_record('red:9'); it has blue:4/red:4 and blue:3/red:7 instead, so the exact requested assertion is missing.
- **parsing-16 · plan-execute 2** (rubric) — Assert parse_record('blue:4') and parse_record('red:9') return their respective pairs. — No test asserts parse_record('blue:4') and parse_record('red:9') specifically; parse_record is tested with blue:3/red:10, while blue:4/red:9 appear only for batch_size.
- **parsing-16 · plan-execute 3** (rubric) — Complete — The suite broadly covers consecutive records, but it omits the requested explicit red:9 parse_record case and provides no explanation for the omission.
- **dependency-01 · baseline 1** (rubric) — Assert one fetch_count('blue') call for input ' blue '. — It asserts fetch_count was called once with 'blue', but the input passed to batch_size is ' blue ', not the specified ' blue '.
- **dependency-01 · plan-execute 2** (rubric) — Assert one fetch_count('blue') call for input ' blue '. — It asserts fetch_count once with 'blue', but for input ' blue ', not the specified input ' blue '.
- **dependency-02 · react 1** (rubric) — Stub fetch_count to return 11. — The fake client returns 7 and 42, not 11; fetch_count is not stubbed to return 11.
- **dependency-02 · react 2** (rubric) — Stub fetch_count to return 11. — No test stubs fetch_count with return value 11; parametrized values are 0, 1, 3, 7, 42, and 10**6.
- **dependency-02 · react 3** (rubric) — Stub fetch_count to return 11. — No test stubs client.fetch_count.return_value = 11; tests use 3, a sentinel object, 0, and 7.
- **dependency-02 · plan-execute 1** (rubric) — Complete — The submission does not address the specific requested value 11; it tests successful lookups with 3, 42, 0, 1, 7, and 250 instead.
- **dependency-02 · plan-execute 3** (rubric) — Stub fetch_count to return 11. — No test stubs client.fetch_count.return_value = 11; the stubbed values are 7, 42, 0, and 3.
- **dependency-05 · react 2** (generation) — No test candidate was produced. The request asks to 'test propagation of a client timeout', but the fixture defines no timeout concept to assert against, so any test would have to invent the missing fact. Evidence: README.md states 'The client is an injected dependency. The fixture contains no ex...
- **dependency-05 · plan-execute 1** (generation) — No test candidate was produced. Planner returned no usable plan.
- **dependency-05 · plan-execute 2** (judge) — Judge request or response failed (APITimeoutError).
- **dependency-05 · plan-execute 3** (generation) — No test candidate was produced. Inspection complete but the step premise is not supported by repository evidence, so no tests were staged and the diff is empty. The whole repository is: README.md, parsing.py, service.py, validation.py, tests/test_reference.py (no conftest, packaging, config, or o...
- **dependency-06 · baseline 1** (rubric) — Correct — The test verifies preservation of a client exception, but it uses a custom ClientError rather than the required RuntimeError, so it does not fully match the requested test.
- **dependency-06 · react 2** (generation) — No test candidate was produced. Missing evidence: no requirement in the repository specifies "preservation of the original client exception object" for service.batch_size (or any other module). service.batch_size's docstring states the contract as "Return client.fetch_count for a normalized name,...
- **dependency-06 · plan-execute 2** (generation) — No test candidate was produced. No client-exception-preservation behavior exists in the repository to test, so no test files were staged (diff is empty). Evidence: the only injected-client call site is service.batch_size(name, client), whose docstring states 'Return client.fetch_count for a norma...
- **dependency-06 · plan-execute 3** (generation) — No test candidate was produced. No repository evidence supports the requirement 'preservation of the original client exception object', so no test can be written for it without inventing behavior. Repository contents are only README.md, service.py, parsing.py, validation.py, and tests/test_refere...
- **dependency-10 · baseline 1** (rubric) — Complete — The submission covers zero-count parsing and batch_size return, but it does not address all requested behavior because it omits the required fetch_count call-count assertion.
- **dependency-10 · react 3** (rubric) — Complete — Covers the zero-count goal but omits the required assertion that fetch_count was called exactly once.
- **dependency-11 · baseline 1** (rubric) — Complete — The tests cover case preservation with 'Blue', but do not cover the explicitly requested input ' BlueTeam '.
- **dependency-11 · react 1** (rubric) — Complete — The submission covers case preservation broadly but omits the specifically requested BlueTeam-with-spaces case.
- **dependency-11 · react 2** (rubric) — In policy — The explanation claims overall coverage of 54% line / 17% branch, but pytest reports 43.33% line / 16.67% branch; this is an unsupported/incorrect factual claim.
- **dependency-11 · react 3** (rubric) — Complete — The submission covers case preservation broadly but does not address the explicitly requested ' BlueTeam ' example.
- **dependency-11 · plan-execute 1** (rubric) — Verify fetch_count receives 'BlueTeam' for input ' BlueTeam '. — No test uses input ' BlueTeam ' or asserts fetch_count was called with 'BlueTeam'; the closest whitespace case uses ' CaSeD Name ' -> 'CaSeD Name'.
- **dependency-11 · plan-execute 2** (rubric) — Verify fetch_count receives 'BlueTeam' for input ' BlueTeam '. — No test calls batch_size with the exact input ' BlueTeam '; the whitespace case uses ' TrimmedCase ' and 'BlueTeam' is tested without surrounding spaces, so fetch_count is not asserted to receive 'BlueTeam' for that exact input.
- **dependency-11 · plan-execute 3** (rubric) — Complete — Tests cover case preservation generally but omit the specifically requested batch_size(' BlueTeam ', ...) scenario and assertion that fetch_count receives 'BlueTeam'.
- **dependency-12 · baseline 1** (rubric) — Verify fetch_count receives 'blue team' for input ' blue team '. — No test uses input ' blue team ' and asserts fetch_count is called with 'blue team'; the parametrized cases use different names.
- **dependency-12 · react 1** (rubric) — Verify fetch_count receives 'blue team' for input ' blue team '. — No test uses input ' blue team ' or asserts fetch_count receives 'blue team'; the Mock test uses ' a b ' and asserts fetch_count called with 'a b'.
- **dependency-12 · react 2** (rubric) — Verify fetch_count receives 'blue team' for input ' blue team '. — No test uses input ' blue team ' or asserts that fetch_count receives 'blue team'; analogous cases exist, but the specifically requested case is absent.
- **dependency-12 · react 3** (rubric) — Verify fetch_count receives 'blue team' for input ' blue team '. — No test uses the exact input ' blue team ' or asserts fetch_count receives 'blue team'. The closest checks use ' blue green red ' and parametrized names such as 'x y', so the requested exact case is not verified.
- **dependency-12 · plan-execute 1** (rubric) — Verify fetch_count receives 'blue team' for input ' blue team '. — No test calls batch_size(' blue team ') and asserts fetch_count receives 'blue team'; the closest cases use 'blue green' with edge spaces or 'blue green' without edge spaces.
- **dependency-12 · plan-execute 2** (rubric) — Complete — The tests do not cover the exact required case batch_size(' blue team ') verifying fetch_count receives 'blue team'; they only include analogous spacing cases.
- **dependency-12 · plan-execute 3** (rubric) — Complete — The tests cover internal-space preservation broadly but omit the specifically requested lookup case for input ' blue team ' with expected fetch_count argument 'blue team'.
- **dependency-13 · baseline 1** (rubric) — Verify fetch_count receives 'café' for input ' café '. — No test calls batch_size with the exact input ' café ' (single spaces each side); the café case uses ' café ' with two spaces, so it does not directly verify fetch_count receives 'café' for the specified input.
- **dependency-13 · react 1** (rubric) — Complete — Although the suite broadly covers Unicode lookup, it does not verify the requested exact case of batch_size(' café ', client) causing fetch_count to receive 'café'; café stripping and Unicode pass-through are tested separately, and the stripped lookup case uses Japanese.
- **dependency-13 · react 2** (rubric) — Verify fetch_count receives 'café' for input ' café '. — The exact requested input `' café '` is not tested. The whitespace case uses `' café '` with two spaces, so it does not verify `fetch_count` receives `'café'` for the specified single-space input.
- **dependency-13 · react 3** (rubric) — Complete — Although Unicode preservation is broadly covered, the suite lacks a direct end-to-end test using the exact input " café " and asserting fetch_count receives "café".
- **dependency-13 · plan-execute 1** (rubric) — Complete — Unicode preservation is broadly covered, but the specified integrated case for input ' café ' through batch_size to fetch_count is not directly asserted.
- **dependency-13 · plan-execute 2** (rubric) — Complete — The suite covers many Unicode cases but omits the required scenario with ASCII spaces around 'café'.
- **dependency-13 · plan-execute 3** (rubric) — Verify fetch_count receives 'café' for input ' café '. — No test calls batch_size(' café ', client) and asserts fetch_count was called with 'café'; the NBSP and inner-space cases use different inputs.
- **dependency-14 · baseline 1** (rubric) — Correct — Expected the changed client values to be 3 then 8 for 'blue', but the submitted test uses 2 then 5.
- **dependency-14 · react 2** (rubric) — Correct — Candidate uses side_effect [3, 7] and asserts 3 then 7, not the required 3 then 8.
- **dependency-14 · react 3** (rubric) — Correct — The added tests exercise repeated batch_size calls, but the 'blue' case uses side_effect [3, 7], not the required [3, 8], so it does not match the specified reference behavior.
- **dependency-14 · plan-execute 1** (rubric) — Correct — The main two-lookup test uses 3 then 7, not the required 3 then 8 for 'blue'.
- **dependency-14 · plan-execute 2** (rubric) — Correct — The repeat test uses side_effect [3, 7] and asserts (3, 7), so it does not match the required 3-then-8 behavior for 'blue'.
- **dependency-14 · plan-execute 3** (rubric) — Correct — The core test uses side_effect [3, 5], not [3, 8], so it does not match the required reference behavior.
- **dependency-15 · baseline 1** (rubric) — Correct — Pytest passes, but the added tests do not verify the requested same-name independence: the first test uses 'blue' vs 'green', and the second uses KeyError vs a count for 'blue'.
- **dependency-15 · plan-execute 1** (rubric) — Configure two clients to return different counts for the same name. — It configures clients with different return values 3 and 7 but calls them with different names ('blue' and 'green'); the same-name case uses KeyError rather than two different returned counts.
- **dependency-15 · plan-execute 2** (rubric) — In policy — The docstring cites an absent README.md claim that 'The client is an injected dependency,' introducing an unverified fact not present in the provided fixture evidence.
- **dependency-16 · baseline 1** (rubric) — Correct — The test verifies recovery but uses 7 as the later value, not the requested 6, so it does not match the exact expected behavior.
- **dependency-16 · react 1** (rubric) — Arrange KeyError then 6 for repeated lookups. — No test arranges KeyError then 6 for repeated lookups; the main recovery test uses side_effect [KeyError('blue'), 7].
- **dependency-16 · react 2** (rubric) — Correct — Recovery test uses a KeyError followed by 3, not the expected 6, so it does not match the specified reference scenario.
- **dependency-16 · react 3** (rubric) — Correct — The test uses a KeyError then 4 and asserts 0 then 4, so it does not match the expected KeyError then 6 and 0 then 6 reference behavior.
- **dependency-16 · plan-execute 1** (rubric) — Correct — The recovery tests use later returns of 4, 2, and 9, not the required 6, so the submission does not match the specified reference scenario.
- **dependency-16 · plan-execute 2** (rubric) — Arrange KeyError then 6 for repeated lookups. — The recovery tests arrange KeyError then 4, 7, or 2, not KeyError then 6.
- **dependency-16 · plan-execute 3** (rubric) — Correct — The submission exercises recovery, but it does not match the requested reference scenario of arranging a KeyError followed by 6.
- **unanswerable-01 · baseline 1** (rubric) — Complete — The explanation identifies the missing maximum but does not request the importer limit or authoritative specification needed to resolve it.
- **unanswerable-01 · react 3** (rubric) — Grounded — Most code observations are supported, but the explanation asserts that a README states there is no external service contract or deployment configuration; no README is included in the fixture evidence.
- **unanswerable-01 · plan-execute 3** (generation) — Expected an explanation and an empty diff. Model staged tests before reporting missing evidence.
- **unanswerable-02 · baseline 1** (rubric) — Ask for the service contract. — Does not ask for the service contract or explicitly request the missing rate-limit/retry-delay specification.
- **unanswerable-02 · react 1** (rubric) — Grounded — The core conclusion is supported by service.py and validation.py, but the explanation cites an unprovided README.md and says it inspected five files, while the fixture contains only four listed sources and no README.
- **unanswerable-02 · react 3** (rubric) — Grounded — The core absence claim is supported by service.py and validation.py, but it also asserts a README statement not present in the supplied fixture evidence.
- **unanswerable-02 · plan-execute 2** (rubric) — Grounded — Core findings from service.py and validation.py are supported, but the explanation claims README.md content not present in the supplied sources, making part of the grounding unsupported.
- **unanswerable-02 · plan-execute 3** (generation) — Expected an explanation and an empty diff. Model returned an invalid final response.

Generation model: deepseek-flash

Judge model: deepseek-flash
