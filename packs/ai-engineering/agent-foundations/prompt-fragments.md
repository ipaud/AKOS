# Prompt Fragments — Agent Foundations Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply agent-architecture constraints (agent-foundations pack, AKOS L2):
- Do not reach for an agent when a deterministic function, a fixed workflow,
  or a direct query solves the problem. Name the simpler shape and the
  specific failure that rules it out before building the more autonomous one.
- Pick a shape from the spectrum explicitly and record the choice: single call
  -> prompt chain -> routing -> parallelization -> fixed workflow ->
  orchestrator-worker -> evaluator-optimizer -> agent -> multi-agent. Each
  step down transfers a decision from you to the model and costs
  predictability.
- If the execution path is enumerable from real inputs, encode it as a
  workflow. An agent is for variance you genuinely cannot enumerate.
- Implement deterministic subtasks (arithmetic, formatting, validation,
  lookup, sorting) as code, never as a model call.
- Route before dispatching where inputs fall into distinguishable classes,
  and define the fallback class explicitly.
- Before any fan-out, state whether it buys latency (sectioning: independent
  subtasks) or confidence (voting: repeated attempts, stated aggregation
  rule). Branches may share reads, never writes. Cap the width.
- Use orchestrator-worker only where the subtask list varies with the input.
  If you can write the list into the code, write it into the code.
- An evaluator-optimizer loop states its criteria before the first
  generation, prefers an external check (test, schema, tolerance) over a
  model's opinion, and exits on criteria passing, on the iteration cap, or on
  a non-improving iteration.
- Declare every plan as fixed or revisable. Replan only on a named
  invalidated assumption, never on a general sense of slow progress. Cap
  replans; escalate at the cap.
- State the success condition in checkable terms BEFORE the loop starts. The
  model saying it is done is a signal to verify, not a termination condition.
- Every loop carries four limits - iterations, tokens, tool calls, wall clock
  - each a value you chose on purpose, not a framework default.
- Budget exhaustion is a third outcome alongside success and error. Return an
  explicit `exhausted` status carrying which limit fired, what completed, and
  what did not. Never return partial work in the shape of complete work.
- Classify failures before responding: transient -> retry with backoff and a
  small cap; approach-level -> replan and name the invalidated assumption;
  terminal -> escalate. Never retry an identical deterministic failure.
- Write the escalation conditions and the authority boundary into the spec:
  what the agent may do alone, what needs confirmation, what it may never do.
  Anything irreversible or unlisted defaults to asking.
- Assume every action happens twice. Every side-effecting call is idempotent,
  keyed, or atomically guarded; retries reuse the original key; a timeout is
  not evidence the action failed.
- State the cost and latency envelope before choosing a shape, and eliminate
  shapes that cannot fit inside it.
- Emit a trace: steps, tool calls, tokens spent, and a structured exit reason.
```

## Fragment: review lens

```text
Review this work as an agent-architecture reviewer (agent-foundations pack).
1. Shape pass - name the shape actually implemented and the simplest shape
   that would have worked. If they differ, that is the headline finding, and
   it must name the specific alternative, never just "over-engineered."
2. Warrant pass - if this is an agent, check all four: are the paths
   genuinely non-enumerable across real inputs; does the environment return
   feedback the model can steer on; is every reachable step recoverable or
   gated; does the cost/latency envelope admit a loop at all.
3. Determinism pass - flag any subtask delegated to a model that a function
   could compute exactly (arithmetic, formatting, validation, lookup,
   sorting, deduplication).
4. Routing pass - do distinguishable input classes get distinguishable
   handling; is there an explicit fallback class; is the classification
   recorded separately from the outcome.
5. Parallelization pass - for each fan-out: sectioning or voting, stated
   which; branches verified independent (no shared writes, no consumed
   outputs); width capped; aggregation rule declared before execution.
6. Decomposition pass - for orchestrator-worker, does the subtask list
   actually vary with the input, or is a constant being re-derived at cost.
   Check worker briefs, caps on count and depth, and whether synthesis is a
   real step with its own success condition.
7. Loop pass - for every loop: a checkable success condition stated before
   the loop, an iteration cap, a token budget, a tool-call budget, a
   wall-clock bound, and a no-progress exit. Flag any loop terminating on the
   model's self-assessment alone.
8. Exhaustion pass - CRITICAL. Trace what a run returns when it hits a limit.
   If exhaustion is indistinguishable from success without inspecting the
   content, that is a correctness defect, not a performance issue.
9. Error pass - are failures classified (transient / approach-level /
   terminal) before a response is chosen. Flag any generic retry applied to
   all three, any retry of an identical deterministic failure, and any failed
   step swallowed with execution continuing.
10. Escalation pass - is the authority boundary written down (may act alone /
    must confirm / never). Flag both an agent that has never escalated and one
    that escalates on routine cases; both mean the boundary was defaulted, not
    designed.
11. Idempotency pass - CRITICAL. For every side-effecting tool: what happens
    if it is called twice with identical arguments. Flag any non-idempotent
    action on an automatic retry path, any retry generating a fresh key, and
    any timeout treated as proof of failure.
12. Observability pass - does each run emit steps, tool calls, spend, and a
    structured exit reason; are sub-agent runs linked to their parent.
13. Run review-checklist.md; report findings by severity with the exact
    architectural change needed - never "simplify this" without naming the
    shape to simplify to.
```

## Fragment: shape-selection worksheet

```text
Choose the architecture for this task. Answer in order; stop at the first
shape that fits and justify why the next one down is unnecessary.

INPUT ANALYSIS
- Collect 20 representative real inputs. For each, write the step sequence it
  needs. How many DISTINCT sequences? ______
- Do the sequences share a pattern, or is each one different? ______
- What varies between inputs: the data, the number of steps, the ORDER of
  steps, or which steps exist at all? ______

ENVELOPE (state before choosing a shape)
- Cost ceiling per invocation: ______
- Latency target (P95): ______
- Token budget per invocation: ______
- Which shapes does this envelope already exclude? ______

SHAPE
- Chosen shape: ______
- Next-simpler shape: ______
- The specific failure of that simpler shape: ______
  (If you cannot state it concretely, build the simpler shape.)
- Model decision points in the chosen design: ______
- For each, the class of input variance it absorbs: ______

BOUNDS (required for any shape with a loop)
- Success condition, in checkable terms: ______
- Iteration cap / token budget / tool-call budget / wall-clock bound: ______
- Behavior on exhaustion (must be a distinct outcome): ______
- Replan triggers, or "plan is fixed": ______
- Escalation conditions and authority boundary: ______
- Side-effecting actions, and how each is made safe to repeat: ______

Output the filled worksheet, then the recommended shape in one sentence.
No prose preamble.
```

## Fragment: loop-boundedness audit

```text
Audit every loop in this system. For each one, produce a row:
- Location and what it iterates over.
- Success condition, quoted from the code/spec. Mark MISSING if it is only
  the model's self-assessment, and mark UNCHECKABLE if it cannot be verified
  by anything outside the model.
- Iteration cap / token budget / tool-call budget / wall-clock bound. Mark
  each PRESENT (chosen), DEFAULT (framework value nobody selected), or ABSENT.
- No-progress exit: PRESENT / ABSENT.
- What the loop returns on exhaustion, and whether a caller can distinguish it
  from success WITHOUT inspecting the content. Mark SILENT-TRUNCATION if not.
- Has each limit been deliberately exercised in a test? YES / NO.
Then list, in severity order: every SILENT-TRUNCATION (critical), every
MISSING or ABSENT success condition or cap (high), every DEFAULT limit and
untested limit (medium). For each, give the specific change.
```

## Fragment: failure-and-recovery trace

```text
Trace this system's failure handling. For every failure path:
- What failure it handles, and its class: TRANSIENT (timeout, rate limit,
  5xx, intermittent) / APPROACH-LEVEL (step succeeded but result is wrong; the
  identical error recurs) / TERMINAL (missing permission, missing information
  only a human has, outside stated authority).
- The response taken: RETRY / REPLAN / ESCALATE / CONTINUE / SWALLOW.
- Verdict: MATCHED (response fits the class) or MISMATCHED (say which
  response it should have been).
Flag as CRITICAL: any failed step swallowed with execution continuing; any
non-idempotent side effect on an automatic retry path; any timed-out side
effect retried without first verifying its actual state.
Flag as HIGH: any generic retry applied to all three classes; any identical
deterministic failure retried; any absence of an escalation path for terminal
failures.
Then: list every side-effecting action the system can take and state, for
each, what happens if it executes twice with identical arguments.
```

## One-liner (for tight token budgets)

```text
Agent rules: don't build an agent when a function, a fixed workflow, or a
direct query solves it - name the simpler shape and why it fails, first;
encode the path when the path is knowable, and reserve agents for variance you
genuinely cannot enumerate; route distinguishable input classes to
distinguishable handlers with an explicit fallback; fan out only for latency
(independent subtasks) or confidence (repeated attempts, aggregation rule
declared up front), never across shared writes; orchestrate dynamically only
when the subtask list varies with the input; critique loops need explicit
external criteria or they just reshuffle; declare every plan fixed or
revisable and replan only on a named invalidated assumption; state the success
condition in checkable terms before the loop starts; cap iterations, tokens,
tool calls, and wall clock; make exhaustion a distinct loud outcome, never
partial work shaped like complete work; classify failures before responding -
retry transient, replan approach-level, escalate terminal, and never retry an
identical deterministic error; write the authority boundary and escalation
conditions into the spec; assume every action happens twice and make it safe
to repeat; choose the shape against a stated cost and latency envelope, not
after one; emit a trace with a structured exit reason.
```
