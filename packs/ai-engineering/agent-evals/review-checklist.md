# Review Checklist — Agent Evals Pack

Binary checks, ordered by severity. Each unchecked box is a finding at the listed severity. Checks marked ★ are safety-floor items — a suite that reports something false about the system it measures — and block in every reasoning profile.

Reviewing an eval suite means reading the cases, the harness, the threshold config, and the git history of the baseline — not the pass rate. Several checks require the history or a run report rather than the current state; those say so.

## Critical (blocks in every profile)

- [ ] ★ **History check:** no baseline was updated in the same commit or the same command as a run that failed against it. (AEE54)
- [ ] ★ The harness offers no flag, script, or target that re-records a baseline as a side effect of running the suite. (AEE55)
- [ ] ★ Every case has been verified by deliberately breaking the behavior it tests and observing it go red; any case never seen red is marked unverified. (AEE70)
- [ ] ★ No grader is the same model instance, in the same context, that produced the output under test. (AEE24)
- [ ] ★ Every LLM-as-judge grader that gates anything has been calibrated against human-labeled cases, with the agreement rate recorded, at its current model version. (AEE22, AEE23)
- [ ] ★ Eval cases run against a clean context — no carried session state, no memory files, no leakage from an earlier case in the same run. (AEE64)
- [ ] ★ Case fixtures contain no real secrets, real customer data, or copied production records. (AEE8)

## High

- [ ] The pass bar — floor, maximum permitted drop, gated metrics — is declared in a committed config file, and predates the change under test. (AEE51)
- [ ] The regression threshold sits outside the suite's measured run-to-run variance, and that variance figure is recorded. (AEE52)
- [ ] The baseline records version, corpus revision, grader version, and run count — not the number alone. (AEE53)
- [ ] Every comparison held corpus, grader, and run count fixed; any difference that could not be held is stated. (AEE58)
- [ ] Every reported metric ships with the corpus it was computed over, in the same output. (AEE9, AEE72)
- [ ] Every baseline comparison reports quality, cost, latency, and tool-call efficiency together. (AEE41)
- [ ] Task completion is defined in externally checkable terms and is the headline metric of the end-to-end suite. (AEE35, AEE36)
- [ ] No completion check is satisfied by the agent's own claim of having completed. (AEE38)
- [ ] Groundedness is scored and reported separately from correctness. (AEE29)
- [ ] The suite contains failure-injection cases and reports a recovery rate. (AEE46, AEE47)
- [ ] The suite contains negative cases where the correct behavior is not to act, not to flag, or not to call the tool. (AEE6, AEE13)
- [ ] A held-out portion of the dataset exists, is never used for iteration, and its score is reported next to the iterated set's. (AEE7, AEE67)
- [ ] Per-case pass rate across runs is tracked, and flakiness is flagged automatically rather than from memory. (AEE60)
- [ ] No case identified as flaky remains in the gating suite; each was fixed, re-scoped, or removed with the removal recorded. (AEE61)
- [ ] CI fails the build on a threshold breach; if the suite is advisory only, it is documented as advisory. (AEE57)
- [ ] The dataset lives under version control and changes only through a reviewed commit. (AEE1)
- [ ] Fabricated specifics — invented citations, non-existent functions or endpoints, made-up figures — are graded as full failures, not partial credit. (AEE32)

## Medium

- [ ] Every case declares its altitude (unit / tool-call / trajectory / end-to-end) as a field. (AEE10)
- [ ] Every user-facing task the agent is expected to complete has at least one end-to-end case. (AEE11)
- [ ] Any altitude with no cases is recorded as a stated gap rather than left for the aggregate to imply. (AEE15)
- [ ] Each case names its grader type. (AEE17)
- [ ] No judged grader decides something a schema check, regex, test run, or numeric tolerance could have decided. (AEE18)
- [ ] Exact-match grading is applied only to outputs with a canonical form, never to free prose. (AEE19)
- [ ] Rubric graders enumerate named criteria with behavioral anchors, and report per-criterion results. (AEE20, AEE21)
- [ ] Pairwise comparisons randomize order and report the position-bias check. (AEE26)
- [ ] No pairwise win rate has been converted into an absolute quality score. (AEE27)
- [ ] Tool-call cases assert the tool selected *and* the arguments passed. (AEE12)
- [ ] Trajectory cases assert a property of the path, not only that it terminated. (AEE14)
- [ ] The suite includes cases where the answer is genuinely absent from the provided context, expecting a refusal. (AEE31)
- [ ] Recovery cases distinguish recovered / gave up / looped, rather than collapsing to pass/fail. (AEE48)
- [ ] At least one injected failure cannot be resolved by retrying, and one requires escalation. (AEE49, AEE50)
- [ ] Cost and latency carry their own regression thresholds. (AEE42)
- [ ] Latency is reported at stated percentiles (p50, p95 minimum), never as a mean alone. (AEE43)
- [ ] Avoidable non-determinism (seeds, timestamps, live network) was removed before variance was attributed to the model. (AEE62)
- [ ] Accepted regressions are recorded with their reason and tradeoff. (AEE56)
- [ ] The dataset carries a written statement of the population it represents and how cases were drawn. (AEE2)
- [ ] The harness reports how many cases ran, how many were skipped, and why — no silent filtering. (AEE71)
- [ ] The harness itself has tests covering its path resolution, matching, and skip logic. (AEE74)

## Low

- [ ] Every case has a stable identifier that survives reordering. (AEE3)
- [ ] Cases drawn from public benchmarks or public documentation are labeled as such. (AEE66)
- [ ] Cases are refreshed on a stated cadence from recent real failures. (AEE68)
- [ ] Changes made in response to a specific eval case are recorded as such. (AEE69)
- [ ] Redundant tool calls within a run are counted and reported. (AEE45)
- [ ] Tool-call efficiency is measured per completed task, not per run. (AEE44)
- [ ] Hallucination rate is tracked as a trend, not only per release. (AEE33)
- [ ] Completion is reported per task category as well as in aggregate. (AEE39)
- [ ] Run reports are reproducible from recorded inputs. (AEE75)
- [ ] No stale report artifact is committed and readable as current. (AEE76)

## Process

- [ ] The review read the cases, the harness, and the baseline's git history — not only the pass rate.
- [ ] For each red case, the diagnosis was worked in order (flaky → harness → uncontrolled comparison → real regression → case is wrong), and "the case is out of date" was a conclusion reached rather than a starting hypothesis.
- [ ] Any metric computed over a curated corpus carries an explicit statement that it is a regression guard, not a population estimate. (AEE73)
- [ ] Every dimension the system is expected to hold either has a measurement or a recorded blind spot. (AE15)
- [ ] A suite sitting at or near 100% across several release cycles was treated as a signal to add harder cases, not as evidence of health. (AE16)
