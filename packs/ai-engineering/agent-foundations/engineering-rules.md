# Engineering Rules — Agent Foundations Pack

Checkable in an agent's code, its configuration, its specification, or a run trace. A reviewer verifies each against the actual artifact; violations are findings.

## Shape selection

- AFE1. The chosen shape (single call / chain / router / parallel / workflow / orchestrator-worker / evaluator-optimizer / agent / multi-agent) is named explicitly in the system's documentation or code comments, not left implicit in the implementation.
- AFE2. The record of that choice states what the next-simpler shape would have been and the specific failure that ruled it out.
- AFE3. No component uses a loop where a single call or a fixed sequence produces the same output; a loop present "for flexibility" with no observed variance to absorb is removed.
- AFE4. Every point at which the model chooses the next action (rather than executing a predetermined one) is identifiable in the code, and each is justified by a named class of input variance.
- AFE5. A task whose execution path is stable across real inputs is implemented as a fixed workflow, not as an agent prompted to discover the path per invocation.
- AFE6. Each additional agent, coordinator, or handoff beyond the simplest working topology cites a measured failure of the simpler topology, not a structural preference.
- AFE7. Deterministic subtasks (arithmetic, formatting, validation, lookup, sorting, deduplication) are implemented as code called by the system, never delegated to a model call.
- AFE8. The system does not use an agent to compensate for a missing direct integration; where a deterministic API or query would answer the question, it is called directly.

## Routing

- AFE9. Where inputs fall into distinguishable classes, a classification step runs before dispatch rather than one generic handler serving all classes.
- AFE10. Each route maps to a named handler with its own stated inputs, outputs, and quality bar; routes do not share one undifferentiated implementation.
- AFE11. A default/fallback class is defined explicitly and handles unclassifiable input; it is not the last branch by accident or a silent pass-through.
- AFE12. The classification decision for each request is recorded in the trace, separately from the request's outcome, so misroutes are detectable without re-running the request.
- AFE13. The routing criterion is the handling the task needs, not a surface feature of the input (length, keyword presence, format) unless that feature is demonstrated to predict the right handler.
- AFE14. Routing confidence, where the classifier produces one, has a stated threshold below which the input goes to the fallback class or escalates, rather than being dispatched on a weak match.

## Parallelization

- AFE15. Every fan-out states which pattern it implements — sectioning (independent subtasks) or voting (repeated attempts at the same task) — and that statement matches the implementation.
- AFE16. Subtasks run in parallel are verified independent: none consumes another's output, and none writes state another reads within the same fan-out.
- AFE17. Voting fan-outs declare their aggregation rule (majority, highest-scoring, unanimous, first-success) before execution; the rule is not selected after inspecting the results.
- AFE18. Fan-out width is capped by an explicit maximum; a width derived from input data is bounded by that maximum rather than growing with the input.
- AFE19. A voting fan-out is justified by measured output variance on the task; where a single pass is already stable, the fan-out is removed rather than kept as insurance.
- AFE20. Partial failure in a fan-out is reported explicitly (which branches succeeded, which failed), not silently absorbed into an aggregate that looks complete.

## Orchestrator-worker

- AFE21. An orchestrator-worker topology is used only where the number or nature of subtasks varies with the input; a fixed subtask list is implemented as a workflow instead.
- AFE22. Each worker receives a self-contained brief — its task, its inputs, its expected output shape, and its own budget — rather than inheriting the orchestrator's full working state.
- AFE23. Worker count per orchestration and spawn depth (workers spawning workers) are both capped by explicit limits.
- AFE24. The synthesis step that combines worker results is an explicit, specified step with its own success condition, not a concatenation of worker outputs.
- AFE25. Worker budgets are allocated from the orchestration's total envelope, so the sum of worker spend cannot exceed the run's stated budget.
- AFE26. A worker's failure is surfaced to the orchestrator as a typed result (failed, partial, exhausted) that the orchestrator handles explicitly, not as a missing or empty output.

## Evaluator-optimizer

- AFE27. The evaluation criteria are written and fixed before the first generation, in terms specific enough that two evaluators applying them to the same output would reach the same verdict.
- AFE28. Where an external check is available (a test run, a schema validation, a compile, a numeric tolerance), it is used as the criterion rather than a model's unstructured judgment.
- AFE29. The optimize loop has an explicit maximum iteration count; the default is small (two to three) and any larger value carries a stated reason.
- AFE30. The loop exits when the criteria pass, when the iteration cap is hit, or when an iteration fails to improve on the previous one — all three exits are implemented, not just the first two.
- AFE31. Each iteration's evaluation result is recorded, so a non-improving loop is detectable from the trace rather than only from the final output.
- AFE32. The evaluator's feedback names what specifically failed which criterion and what would satisfy it; a bare score or a general "improve this" is not an evaluation.

## Planning and replanning

- AFE33. Every plan-carrying component declares whether its plan is fixed (deviation is a reportable failure) or revisable (replanning is expected under stated triggers).
- AFE34. For a revisable plan, the replan triggers are named conditions (an assumption invalidated, a required resource unavailable, a subtask failed identically twice), not general dissatisfaction with progress.
- AFE35. The number of replans on a single task is capped; hitting the cap escalates rather than continuing to rewrite.
- AFE36. A replan preserves completed work that remains valid, and states what it discards and why; it does not restart the task from scratch by default.
- AFE37. Plan revisions are recorded in the trace with the trigger that caused each, so plan churn is measurable.

## Termination conditions

- AFE38. Every loop has a success condition stated before the loop begins, in checkable terms (an artifact exists, a test passes, a schema validates, a value is within tolerance).
- AFE39. The model's self-assessment ("I'm done") does not by itself terminate a loop; where it is used as a trigger, it is followed by the stated external check.
- AFE40. No-progress is implemented as a termination condition: a loop whose iteration produced no change in the tracked state exits rather than continuing.
- AFE41. The termination condition is verifiable from the run trace after the fact — a reviewer can tell which condition ended the run without re-executing it.
- AFE42. The failure path of the termination condition is exercised in tests: an input the system cannot succeed at is run, and the resulting exit is asserted.
- AFE43. Termination conditions are stated per loop, including nested loops; an inner loop does not rely on the outer loop's condition to stop.

## Limits and budgets

- AFE44. Every loop carries all four limits — maximum iterations, maximum tokens, maximum tool calls, and a wall-clock deadline — each set to a deliberately chosen value rather than a framework default.
- AFE45. The cost and latency envelope per invocation is stated before the architecture is chosen, and the chosen shape is shown to fit inside it.
- AFE46. Budget exhaustion returns a distinct `exhausted` outcome, separate from both success and error, carrying which limit was hit, what completed, and what did not.
- AFE47. No code path returns partial work in the same shape as complete work; a caller can always distinguish the two without inspecting the content.
- AFE48. Token, tool-call, and wall-clock spend per run are recorded in the trace, so a runaway path is attributable to a specific run rather than visible only as an aggregate bill.
- AFE49. Nested budgets are enforced against the parent envelope: a sub-agent or worker cannot spend beyond the remaining budget of the run that invoked it.
- AFE50. Each limit has been exercised deliberately at least once in testing, with the resulting behavior asserted.

## Error recovery

- AFE51. Failures are classified before a response is chosen — transient, approach-level, or terminal — and the classification is recorded in the trace.
- AFE52. Transient failures retry with backoff and an explicit retry cap; the cap is small and stated.
- AFE53. An identical deterministic failure (same input, same error, same step) is never retried; the second identical occurrence triggers a replan or an escalation.
- AFE54. Approach-level failures trigger a replan rather than a retry, and the replan states the assumption the failure invalidated.
- AFE55. No step's failure is swallowed and execution continued; a failed step either recovers explicitly, replans, or escalates, and "continue anyway" is not one of the options.
- AFE56. Failures encountered mid-run are reported in the final output even when the run ultimately succeeds, rather than being erased by the successful retry.

## Escalation

- AFE57. The agent's escalation conditions are written in its specification alongside its success condition and its limits — not decided at run time.
- AFE58. The agent's authority boundary is stated explicitly: what it may do alone, what requires confirmation, and what it may never do.
- AFE59. Any action that is irreversible or outside the stated authority boundary stops and requests human confirmation, regardless of the agent's confidence.
- AFE60. Ambiguity in the request escalates before execution begins rather than being resolved by an unstated assumption and discovered afterward.
- AFE61. An escalation message contains what was attempted, what blocked it, the options available, and a recommendation — enough for the human to decide in one round trip.
- AFE62. Repeated failure on the same subtask escalates at a stated threshold (typically the second identical failure) rather than continuing to consume budget.

## Idempotency and side effects

- AFE63. Every side-effecting action available to an agent is idempotent, carries an idempotency key, or is guarded by an atomic check-then-act.
- AFE64. No non-idempotent action sits on an automatic retry path; where an action cannot be made safe to repeat, the retry path requires explicit confirmation instead.
- AFE65. Retries reuse the original idempotency key rather than generating a new one, so the retry is recognizable as the same logical action.
- AFE66. A replan that re-executes steps already completed either detects the completed state and skips them, or re-executes only actions that are safe to repeat.
- AFE67. Parallel workers that could touch the same resource are either partitioned so they cannot, or serialized through a lock or queue at the point of contact.
- AFE68. A timeout on a side-effecting call does not imply the call failed; the recovery path verifies the action's actual state before retrying it.

## Observability

- AFE69. Each run emits a trace containing the steps taken, tools called, tokens spent, and the exit reason (success / error / exhausted).
- AFE70. The exit reason is a structured field, not inferred from the shape of the output.
- AFE71. Sub-agent and worker runs are traceable to their parent run, so a multi-component run can be reconstructed end to end.
- AFE72. The architecture decision (which shape, and why) is recorded in the repository, so it is reviewable later without relying on anyone's recollection.
