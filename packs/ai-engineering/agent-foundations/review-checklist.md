# Review Checklist — Agent Foundations Pack

Binary checks, ordered by severity. Each unchecked box is a finding at the listed severity. Checks marked ★ are safety-floor items (truncated work returned as complete, duplicated side effects, or actions taken outside stated authority) and block in every reasoning profile.

Reviewing an agent architecture means reading the code, the specification, and at least one real run trace — not the final output alone. Several checks require the trace; those say so.

## Critical (blocks in every profile)

- [ ] ★ Budget exhaustion returns a distinct `exhausted` outcome; no code path returns partial work in the same shape as complete work. (AFE46, AFE47)
- [ ] ★ Every side-effecting action reachable by the agent is idempotent, keyed, or atomically guarded. (AFE63)
- [ ] ★ No non-idempotent action sits on an automatic retry path. (AFE64)
- [ ] ★ Retries reuse the original idempotency key rather than generating a new one. (AFE65)
- [ ] ★ A timed-out side-effecting call has its actual state verified before being retried. (AFE68)
- [ ] ★ Any irreversible action, or any action outside the stated authority boundary, stops and requests human confirmation. (AFE59)
- [ ] ★ The agent's authority boundary is stated explicitly — what it may do alone, what needs confirmation, what it may never do. (AFE58)
- [ ] ★ **Trace check:** no failed step was swallowed and execution continued past it. (AFE55)
- [ ] ★ Every loop has both a stated success condition and an iteration cap; neither substitutes for the other. (AFE38, AFE44)

## High

- [ ] The chosen shape is named explicitly, with the next-simpler shape and the specific failure that ruled it out. (AFE1, AFE2)
- [ ] Deterministic subtasks (arithmetic, formatting, validation, lookup, sorting) are implemented as code, not delegated to a model call. (AFE7)
- [ ] A task whose execution path is stable across real inputs is implemented as a fixed workflow, not as an agent rediscovering it per run. (AFE5)
- [ ] All four limits are present on every loop — iterations, tokens, tool calls, wall clock — each set to a deliberately chosen value. (AFE44)
- [ ] The cost and latency envelope was stated before the shape was chosen, and the chosen shape fits inside it. (AFE45)
- [ ] Failures are classified (transient / approach-level / terminal) before a response is chosen, and the classification is recorded. (AFE51)
- [ ] An identical deterministic failure is never retried; the second identical occurrence replans or escalates. (AFE53)
- [ ] Transient retries have backoff and a small explicit cap. (AFE52)
- [ ] Escalation conditions are written in the specification, not decided at run time. (AFE57)
- [ ] Ambiguity in the request escalates before execution rather than being resolved by an unstated assumption. (AFE60)
- [ ] Repeated failure on the same subtask escalates at a stated threshold. (AFE62)
- [ ] Each run emits a trace with steps, tool calls, tokens spent, and a structured exit reason. (AFE69, AFE70)
- [ ] Each plan-carrying component declares whether its plan is fixed or revisable. (AFE33)
- [ ] Every fan-out states whether it is sectioning or voting, and the statement matches the implementation. (AFE15)
- [ ] Subtasks run in parallel are verified independent — no shared writes, no consumed outputs. (AFE16)
- [ ] Evaluation criteria are written and fixed before the first generation, specific enough for two evaluators to agree. (AFE27)
- [ ] Nested budgets are enforced against the parent envelope; a worker cannot spend past the run's remaining budget. (AFE49)

## Medium

- [ ] Every model decision point is identifiable in the code and justified by a named class of input variance. (AFE4)
- [ ] Each additional agent or coordination layer cites a measured failure of the simpler topology. (AFE6)
- [ ] Where inputs fall into distinguishable classes, a classification step runs before dispatch. (AFE9)
- [ ] A default/fallback class is defined explicitly and is not the last branch by accident. (AFE11)
- [ ] The classification decision is recorded in the trace, separately from the outcome. (AFE12)
- [ ] Routing confidence below a stated threshold routes to fallback or escalates rather than dispatching on a weak match. (AFE14)
- [ ] Fan-out width is capped by an explicit maximum. (AFE18)
- [ ] Voting aggregation rules are declared before execution, not chosen after inspecting results. (AFE17)
- [ ] Partial failure in a fan-out is reported explicitly rather than absorbed into a complete-looking aggregate. (AFE20)
- [ ] An orchestrator-worker topology is used only where the subtask list varies with the input. (AFE21)
- [ ] Each worker receives a self-contained brief with its own budget. (AFE22)
- [ ] Worker count and spawn depth are capped. (AFE23)
- [ ] The synthesis step has its own success condition and is not a concatenation of worker outputs. (AFE24)
- [ ] A worker's failure reaches the orchestrator as a typed result the orchestrator handles explicitly. (AFE26)
- [ ] Where an external check exists (test, schema, compile, tolerance), it is the evaluator's criterion rather than a model's unstructured judgment. (AFE28)
- [ ] The optimize loop implements all three exits: criteria pass, iteration cap, non-improving iteration. (AFE30)
- [ ] Evaluator feedback names what failed which criterion and what would satisfy it. (AFE32)
- [ ] Replan triggers are named conditions, not general dissatisfaction with progress. (AFE34)
- [ ] Replans are capped per task, and hitting the cap escalates. (AFE35)
- [ ] A replan preserves completed work that remains valid and states what it discards. (AFE36)
- [ ] The model's self-assessment does not by itself terminate a loop. (AFE39)
- [ ] No-progress is implemented as a termination condition. (AFE40)
- [ ] Approach-level failures trigger a replan that names the invalidated assumption. (AFE54)
- [ ] Mid-run failures appear in the final output even when the run ultimately succeeds. (AFE56)
- [ ] Escalation messages carry what was attempted, what blocked it, the options, and a recommendation. (AFE61)
- [ ] A replan re-executing completed steps either skips them or re-executes only repeat-safe actions. (AFE66)
- [ ] Parallel workers that could touch the same resource are partitioned or serialized at the point of contact. (AFE67)

## Low

- [ ] No loop exists where a single call or fixed sequence produces the same output. (AFE3)
- [ ] The system does not use an agent to compensate for a missing direct integration. (AFE8)
- [ ] Each route maps to a named handler with its own stated inputs, outputs, and quality bar. (AFE10)
- [ ] The routing criterion is the handling the task needs, not an unvalidated surface feature. (AFE13)
- [ ] Voting fan-outs are justified by measured output variance on the task. (AFE19)
- [ ] Worker budgets are allocated from the orchestration's total envelope. (AFE25)
- [ ] The optimize loop's iteration cap is small (two to three), or a larger value carries a stated reason. (AFE29)
- [ ] Each iteration's evaluation result is recorded so a non-improving loop is visible in the trace. (AFE31)
- [ ] Plan revisions are recorded with the trigger that caused each. (AFE37)
- [ ] Termination conditions are stated per loop, including nested loops. (AFE43)
- [ ] Token, tool-call, and wall-clock spend per run are recorded. (AFE48)
- [ ] Sub-agent runs are traceable to their parent run. (AFE71)
- [ ] The architecture decision is recorded in the repository, reviewable without relying on recollection. (AFE72)

## Process

- [ ] The review inspected the code and at least one real run trace, not the final output alone.
- [ ] The termination condition's failure path was exercised: an input the system cannot succeed at was run and the exit asserted. (AFE42)
- [ ] Each limit was hit deliberately at least once in testing, with the resulting behavior asserted. (AFE50)
- [ ] The exit reason of each sampled run is determinable from the trace without re-execution. (AFE41)
- [ ] For each shape finding, the review names the specific simpler shape that would have worked — never "this is over-engineered" without the alternative.
