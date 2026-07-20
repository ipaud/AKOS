# Scoring Rubric — Agent Foundations Pack

Standalone 0–100 score for the architecture of an agentic system — the shape chosen and how well it is bounded. Not a dimension of the twelve-lens UI review pipeline (`core/review-pipeline.md` covers product/UX/accessibility/mobile/copy/frontend/architecture/security/performance/testing/database/release); this pack scores a different surface: whether the system should have been an agent at all, and whether the one that exists terminates, recovers, and is safe to repeat.

Score = 100 − deductions, floor 0. Bands per [core/scoring-model.md](../../../core/scoring-model.md).

Three classes of finding are scored as correctness defects rather than efficiency concerns: **truncated work returned as complete**, **a side effect that can be applied more than once**, and **an action taken outside a stated authority boundary**. All three change what the system does or claims in the world; all three are graded like a wrong calculation, not like an inefficiency.

## Deductions

| Finding | Deduction |
|---------|-----------|
| Budget exhaustion returns in the same shape as success; a caller cannot distinguish them (AFE46, AFE47) | −25 (CRITICAL) |
| A non-idempotent side-effecting action sits on an automatic retry path (AFE63, AFE64) | −25 (CRITICAL) |
| A timed-out side-effecting call is retried without verifying its actual state (AFE68) | −25 (CRITICAL) |
| An irreversible action, or one outside the stated authority boundary, executes without confirmation (AFE59) | −25 (CRITICAL) |
| A failed step is swallowed and execution continues past it (AFE55) | −25 (CRITICAL) |
| A loop has no stated success condition, or none beyond the model's self-assessment (AFE38, AFE39) | −15 (HIGH) |
| A loop is missing an iteration cap, token budget, tool-call budget, or wall-clock bound (AFE44) | −10 per missing limit, cap −20 (HIGH) |
| An agent was built where an enumerable path made a fixed workflow sufficient (AFE5) | −15 (HIGH) |
| No authority boundary or escalation conditions are written down (AFE57, AFE58) | −15 (HIGH) |
| Failures are not classified before a response is chosen; one generic response serves all three classes (AFE51) | −10 (HIGH) |
| An identical deterministic failure is retried rather than replanned or escalated (AFE53) | −10 (HIGH) |
| The shape decision is unrecorded — no named alternative, no stated reason (AFE1, AFE2) | −10 (HIGH) |
| Parallel branches share writes or consume each other's outputs (AFE16) | −10 (HIGH) |
| The cost/latency envelope was not stated before the shape was chosen (AFE45) | −10 (HIGH) |
| A deterministic subtask is delegated to a model call (AFE7) | −4 each, cap −16 (MEDIUM) |
| An evaluator loop's criteria are vague enough that two evaluators would disagree (AFE27) | −6 (MEDIUM) |
| An evaluator loop lacks the non-improving-iteration exit (AFE30) | −4 (MEDIUM) |
| An orchestrator re-derives a subtask list that is constant across inputs (AFE21) | −6 (MEDIUM) |
| Fan-out width, worker count, or spawn depth is uncapped (AFE18, AFE23) | −6 each, cap −12 (MEDIUM) |
| A plan's status (fixed vs. revisable) is undeclared, or replan triggers are unnamed (AFE33, AFE34) | −6 (MEDIUM) |
| Replans are uncapped (AFE35) | −4 (MEDIUM) |
| No routing step where inputs fall into clearly distinguishable classes (AFE9) | −6 (MEDIUM) |
| No explicit fallback class on a router (AFE11) | −4 (MEDIUM) |
| A voting fan-out with no measured output variance justifying it (AFE19) | −4 (MEDIUM) |
| An additional agent or coordination layer with no measured failure of the simpler topology behind it (AFE6) | −6 each, cap −18 (MEDIUM) |
| No-progress is not implemented as a termination condition (AFE40) | −4 (MEDIUM) |
| The aggregation rule for a voting fan-out was not declared before execution (AFE17) | −4 (MEDIUM) |
| No run trace, or an exit reason that must be inferred from output shape (AFE69, AFE70) | −4 (MEDIUM) |
| A limit is set to a framework default nobody chose (AFE44) | −1 each, cap −5 (LOW) |
| A limit has never been deliberately exercised in a test (AFE50) | −1 each, cap −5 (LOW) |
| Sub-agent runs are not traceable to their parent (AFE71) | −1 (LOW) |
| The classification decision is not recorded separately from the outcome (AFE12) | −1 (LOW) |
| Plan revisions are recorded without the trigger that caused each (AFE37) | −1 (LOW) |

## Hard caps

- **Any open CRITICAL finding: score ≤ 59 (BLOCKED).** A system that returns truncated work as complete, can double-apply a side effect, or acts outside its authority fails this dimension regardless of how well the rest of its architecture is chosen.
- An agent shape with no warrant on record — no enumeration of paths, no named simpler alternative: cap 79.
- Any loop without both a success condition and at least one hard limit: cap 69.
- A multi-agent topology with no measured failure of the single-agent version behind it: cap 79.
- No run trace at all on a system with loops: cap 69. Every other rule in this pack is unenforceable without one.

## Modifiers

- The termination-failure path is exercised in tests — an input the system cannot succeed at is run and the exit asserted (AFE42): **+5**.
- Every limit has been deliberately hit in testing with the behavior asserted (AFE50): **+3**.
- The shape decision is recorded in the repository with the rejected alternative and the reason (AFE1, AFE2, AFE72): **+3**.
- Evaluator criteria are grounded in an external check (test run, schema validation, compile, numeric tolerance) rather than a model's judgment (AFE28): **+3**.
- Every side-effecting tool has a documented answer to "what happens if this is called twice" (AFE63): **+3** (cap 100).
- Repeat finding from a previous review, unfixed without a recorded tradeoff: **double its deduction**.

## Interpretation anchors

- **95** — the shape is the simplest one that works and the choice is on record with its rejected alternative; every loop has a checkable success condition and four chosen limits; exhaustion is a distinct loud outcome; failures are classified before they're handled; the authority boundary is written down; every side effect is safe to repeat. Remaining findings are trace-detail polish.
- **85** — sound and well-bounded, with a cluster of MEDIUMs to schedule: a vague evaluator criterion, an uncapped fan-out width, an orchestrator re-deriving a constant, a deterministic subtask still going through a model call.
- **72** — works, but the shape was never justified and the plan's status was never declared. Usable pre-production with the warrant and the bounds queued as real work, not as documentation chores.
- **58** — a limit fires and the run returns partial work indistinguishable from a finished answer, or a retry can double-apply a payment. BLOCKED until the outcome type is split and the idempotency guarantee is installed at the tool boundary — not until the individual instance is patched, which leaves the next one open.
