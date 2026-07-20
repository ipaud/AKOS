# Engineering Rules — Agent Evals Pack

Checkable in an eval suite's cases, its harness, its config, its CI wiring, or a run report. A reviewer verifies each against the actual artifact; violations are findings.

## Golden datasets

- AEE1. The eval dataset lives under version control, and a case changes only through a reviewed commit — never by editing a file the runner also writes to.
- AEE2. The dataset carries a written statement of the population it represents and how cases were drawn from it (sampled from production logs, enumerated from a taxonomy, hand-built from known failures).
- AEE3. Every case has a stable identifier that survives reordering, so a result from an earlier run is still attributable after the set grows.
- AEE4. Every case states its expected behavior explicitly — a value, a rubric, a set of required properties, or a must/must-not list — rather than leaving "expected" to the reader's judgment at review time.
- AEE5. The dataset includes cases derived from real observed failures, not only from the happy path the feature was designed against.
- AEE6. The dataset includes negative cases — realistic near-misses where the correct behavior is *not* to act, not to flag, or not to call the tool.
- AEE7. A held-out portion of the dataset is designated and never used for iteration or prompt tuning; it is run separately and its result reported separately.
- AEE8. Case inputs contain no real secrets, real customer data, or copied production records; fixtures are synthetic or scrubbed, and that property is checkable.
- AEE9. The dataset's size and composition are reported alongside every metric computed over it, not only in its own README.

## Eval granularity

- AEE10. Every case declares its altitude — unit, tool-call, trajectory, or end-to-end — as a field, not as an inference from its shape.
- AEE11. The suite has at least one case at the end-to-end altitude for every user-facing task the agent is expected to complete.
- AEE12. Tool-call cases assert both the tool selected and the arguments passed, not only that some call was made.
- AEE13. Tool-call cases include at least one where the correct behavior is to call no tool at all.
- AEE14. Trajectory cases assert a property of the path (step count within a bound, no repeated identical call, a required step present in order), not merely that the path terminated.
- AEE15. A suite with no cases at a given altitude records that gap explicitly in its documentation rather than letting the aggregate pass rate imply full coverage.
- AEE16. Multi-turn tasks are evaluated across the full conversation, not by grading the final turn in isolation.

## Graders

- AEE17. Each case names its grader type (deterministic, rubric, LLM-judge, pairwise) in the case definition.
- AEE18. A deterministic grader is used wherever the output shape permits one; a judge is not used to decide something a schema check, a regex, a test run, or a numeric tolerance could decide.
- AEE19. Exact-match graders are applied only to outputs with a canonical form (an enum, an ID, a number, a structured field), never to free prose.
- AEE20. Rubric graders enumerate named criteria with independently checkable levels; a rubric whose levels are "good / fair / poor" without behavioral anchors is not a rubric.
- AEE21. Rubric scoring reports per-criterion results, not only the aggregate, so a drop is locatable without re-running.
- AEE22. Every LLM-as-judge grader is calibrated against a human-labeled sample before its scores gate anything, and the agreement rate is recorded.
- AEE23. Judge calibration is repeated whenever the judge model, its version, or the rubric text changes; a judge whose model changed without re-calibration is treated as uncalibrated.
- AEE24. The judge is not the same model instance, with the same context, that produced the output under test; self-grading within one context is not an evaluation.
- AEE25. Judge prompts state the criteria and the output format, and forbid the judge from rewarding length, confidence, or stylistic similarity to its own idiom.
- AEE26. Pairwise comparisons randomize presentation order and report the position-bias check, since a judge preferring whichever candidate came first is a known and measurable defect.
- AEE27. Pairwise results are reported as win rate against a named opponent, never converted into an absolute quality score.
- AEE28. Where both a deterministic and a judged grader apply to the same case, disagreements between them are surfaced rather than resolved by preferring whichever agrees with the expected result.

## Groundedness and hallucination

- AEE29. Groundedness is scored as its own metric, separate from correctness, and reported as its own number.
- AEE30. A groundedness case supplies a known context or tool result and asserts that each load-bearing claim in the output traces to it.
- AEE31. The suite includes cases where the provided context does **not** contain the answer, and the expected behavior is an explicit "not available in the provided sources" rather than a plausible fabrication.
- AEE32. Fabricated specifics — an invented citation, a non-existent function or endpoint, a fabricated numeric figure — are graded as failures at full severity, not as partial credit for an otherwise good answer.
- AEE33. Hallucination rate is tracked over time as a trend, not only as a per-release pass/fail, so slow degradation is visible.
- AEE34. Where the agent cites sources, the suite checks that cited sources exist and support the claim attached to them, not merely that a citation is formatted correctly.

## Task completion

- AEE35. Every end-to-end case defines completion in externally checkable terms — an artifact exists, a record was written, a value falls within tolerance, a state transition occurred.
- AEE36. Task completion rate is the headline metric of any end-to-end suite; step-level metrics appear beneath it, labeled as diagnostics.
- AEE37. Partial completion is a distinct graded outcome, not silently counted as success or as failure; the report states which cases partially completed and on what.
- AEE38. An agent's own claim of completion never satisfies a completion check; the external condition is verified independently of what the agent said it did.
- AEE39. Completion is reported per task category as well as in aggregate, so a category failing entirely is not masked by a strong average.

## Cost, latency, and efficiency

- AEE40. Every eval run records tokens consumed, wall-clock duration, and tool-call count per case, alongside the grade.
- AEE41. Every baseline comparison reports quality, cost, latency, and tool-call efficiency together; a quality delta published without the other three is an incomplete result.
- AEE42. Cost and latency have their own regression thresholds, gated the same way quality is.
- AEE43. Latency is reported at a stated percentile (p50 and p95 at minimum), never as a mean alone.
- AEE44. Tool-call efficiency is measured as calls per completed task, so a system that completes more tasks by calling far more tools is visible as the tradeoff it is.
- AEE45. Redundant tool calls — the same call with the same arguments repeated within one run — are counted and reported as their own metric.

## Recovery

- AEE46. The suite contains failure-injection cases: a tool returning an error, a timeout, a malformed response, a missing permission, an empty result set.
- AEE47. Recovery rate — the share of injected failures after which the agent reaches the goal or escalates correctly — is reported as its own metric.
- AEE48. Recovery cases distinguish the three outcomes explicitly: recovered, gave up prematurely, and looped without progress. A single pass/fail collapses two distinct defects.
- AEE49. At least one case injects a failure that cannot be resolved by retrying, so the suite measures whether the agent changes approach rather than repeating.
- AEE50. At least one case injects a failure requiring escalation, and asserts that escalation happened rather than the agent proceeding on an assumption.

## Regression thresholds and baselines

- AEE51. The pass bar — absolute floor, maximum permitted drop from baseline, and which metrics are gated — is declared in a config file committed before the change under test is run.
- AEE52. The regression threshold is set outside the measured run-to-run variance of the suite, and that variance figure is recorded.
- AEE53. The baseline records the version, the corpus revision, the grader version, and the run count that produced it — not the number alone.
- AEE54. A baseline update is a separate, reviewed commit with a written justification; it never happens in the same commit or the same command as a failing run.
- AEE55. The harness provides no flag, script, or make target that re-records a baseline as a side effect of running the suite.
- AEE56. Any accepted regression is recorded with the reason it was accepted and the tradeoff taken, so it can be revisited rather than forgotten.
- AEE57. CI fails the build on a threshold breach; a suite that only reports a number without gating anything is documented as advisory, not described as a gate.
- AEE58. Comparisons are run with only the variable under test changed — same corpus revision, same grader version, same run count — and any other difference is stated.

## Flakiness

- AEE59. Each case is run more than once where the system is non-deterministic, and the metric is a rate over runs rather than a single pass/fail.
- AEE60. Per-case pass rate across runs is tracked; a case whose rate sits between the stated bounds (neither reliably passing nor reliably failing) is flagged as flaky automatically, not by memory.
- AEE61. A flaky case is fixed, re-scoped, or removed from the gate with the removal recorded; it is never left in the gating suite as a known re-run.
- AEE62. Sources of avoidable non-determinism are removed first — seeds fixed, timestamps and randomness stubbed, network calls mocked or pinned — before variance is attributed to the model.
- AEE63. Re-running a red suite without investigating is not a permitted resolution; the report distinguishes "failed" from "flaky, known" from "re-run to green."

## Contamination

- AEE64. Eval cases run against a clean context: no carried session state, no memory files, no prior-turn contamination from an earlier case in the same run.
- AEE65. Case ordering does not leak information between cases; either cases are independent by construction or the order is fixed and the dependency documented.
- AEE66. Cases drawn from public benchmarks or public documentation are labeled as such, since their answers may be in training data.
- AEE67. The held-out set's score is reported next to the iterated set's; a divergence between them is investigated as contamination before it is explained as noise.
- AEE68. Cases are refreshed on a stated cadence, with new cases drawn from recent real failures, so the suite does not become a fixed target the system has been fitted to.
- AEE69. Any prompt, memory, or fine-tuning change made in response to a specific eval case is recorded, since it converts that case from a measurement into a target.

## Harness and reporting

- AEE70. Every case has been verified by deliberately breaking the behavior it tests and observing the case go red; cases never seen red are marked unverified.
- AEE71. The harness reports how many cases ran, how many were skipped, and why — no silent filtering, no silent caps.
- AEE72. Aggregate metrics state the corpus they were computed over, in the same output as the number.
- AEE73. Metrics computed over a curated corpus carry an explicit statement that they are a regression guard rather than a population estimate.
- AEE74. The harness itself is tested: its path resolution, its matching logic, and its skip logic have their own checks, since a harness bug produces vacuous passes that look identical to real ones.
- AEE75. Run reports are reproducible from the recorded inputs — corpus revision, harness version, grader version, seed, run count — without re-deriving them from anyone's recollection.
- AEE76. Reports are generated, not committed as stale artifacts; a checked-in report that no longer matches the current suite is removed rather than left to be read as current.
