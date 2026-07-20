# Heuristics — Agent Foundations Pack

Fast defaults with known exceptions. Try these first; deviate with a reason.

## Choosing a shape

- **Start at the bottom of the spectrum and move up only under pressure.** One call, then a chain, then a router, then a workflow, then an agent. Each step up needs a specific failure of the step below.
- **If you can draw the flowchart, build the flowchart.** A path you can diagram at design time is a path that belongs in code, not in a prompt describing what the model should consider doing.
- **Count the distinct sequences in twenty real inputs.** Two or three means a router. Twenty with no pattern means the agent is earned.
- **A frozen requirement is a workflow; a moving one is an agent.** If the steps change every time the business changes, that's still design-time variance — encode it and redeploy.
- **Don't build an agent to work around a missing tool.** A model looping to compensate for an API you could have called directly is an expensive polyfill.
- **Prefer more capable steps over more steps.** Two well-specified steps beat six that each shave a little off the task; every boundary is a place information gets lost.

## Routing

- **Route on what the task needs, not on what it superficially resembles.** Surface features (length, keywords, format) correlate weakly with which handler will actually do better.
- **Define the fallback class explicitly.** Every router needs a named home for inputs that match nothing, and it must not be whichever branch happens to be last.
- **Let cheap classes take cheap paths.** The point of routing is partly that a simple request shouldn't pay for the machinery a hard one needs.
- **Log the classification, not just the outcome.** A misroute is invisible in the final answer and obvious in the route log.
- **Keep the class list short.** If a router has fifteen classes, several of them are the same handler wearing different names.

## Parallelization

- **Say which one you're buying — latency or confidence — before fanning out.** If it's neither, don't.
- **Never parallelize steps that share state or depend on each other's output.** Concurrency on dependent work produces results computed against premises that changed.
- **Voting is for high-variance tasks only.** If the single-pass answer is already stable across runs, N samples cost N times as much to reproduce the same answer.
- **Decide the aggregation rule before running the fan-out.** Majority, best-scoring, union, or first-success — picking after you've seen the outputs is picking the answer you liked.
- **Cap the fan-out width explicitly.** A dynamic fan-out with no ceiling is an unbounded cost multiplier one bad input away from firing.

## Orchestrator-worker

- **If the subtask list is stable, it isn't an orchestrator — it's a workflow with extra latency.**
- **Give each worker a self-contained brief.** A worker that needs the orchestrator's full context to be useful is a sign the decomposition didn't actually decompose anything.
- **Cap worker count and depth.** Workers that can spawn workers need a depth limit or the tree is unbounded.
- **Synthesis is a real step with its own quality bar.** Concatenating worker outputs is not synthesis, and it's where most orchestrator systems visibly fail.
- **Budget the workers against the whole task's envelope, not each against its own.** Ten workers each under budget can put the run far over it.

## Evaluator-optimizer

- **Write the criteria before the first generation, not after the first disappointing output.**
- **Prefer an external check to a model's opinion.** A passing test, a valid schema, a numeric tolerance — anything a second party could confirm the same way twice.
- **Two or three iterations, then stop.** Improvement past the third pass is rare and hard to distinguish from rewording; if it's genuinely needed, the criteria are probably wrong.
- **Track whether the score actually improved.** A loop where iteration N+1 doesn't beat N should exit, not continue on the assumption that it eventually will.
- **Separate the evaluator from the generator.** Same context, same blind spots — the critique inherits whatever the generation got wrong.
- **Skip the loop when the first pass is good enough.** Evaluator-optimizer earns its cost on tasks with a real quality gradient, not on tasks that were fine the first time.

## Planning and replanning

- **Declare the plan's status: fixed or revisable.** Undeclared is where both failure modes live.
- **Replan on a named invalidated assumption, never on a general sense of difficulty.**
- **Cap replans.** Three rewrites of the plan on one task is not adaptation, it's thrash — escalate instead.
- **Keep what's still valid.** A replan that discards completed, still-correct work re-pays for it.
- **A plan that survives contact unchanged suggests it could have been a workflow.** Notice when that keeps happening.

## Termination

- **Write the success condition before you write the loop.** If it's hard to write, that difficulty is information about the task, not about the loop.
- **Prefer a condition something external can check.** File exists, test passes, schema validates, value within tolerance.
- **Treat "the model says it's done" as a signal to verify, never as the verification.**
- **A loop that can't state what changed since last iteration should exit.** No progress is a termination condition too.
- **Test the termination path deliberately.** Feed it an input it cannot succeed at and check what comes back.

## Limits and budgets

- **Set the envelope first — cost, latency, tokens per invocation — then pick a shape that fits inside it.**
- **Four limits, always: iterations, tokens, tool calls, wall clock.** Each a number somebody chose, not a framework default nobody looked at.
- **Fail loud on exhaustion.** Exhausted is a third outcome alongside success and error, and it must be visible as one.
- **Instrument spend per run before you tune it.** Cost problems in agent systems are usually one runaway path, not a uniform overspend.
- **A cap you've never hit in testing is a cap you haven't tested.** Force it.

## Error recovery

- **Classify before responding: transient, approach-level, or terminal.**
- **Retry transient failures with backoff and a small cap** — three is usually enough to clear a blip and not enough to burn a budget.
- **Never retry an identical deterministic failure.** Same input, same error means the approach is wrong; retrying is the most expensive way to learn nothing.
- **Escalate on the second failure of the same subtask,** not on the fifth. Repeated identical failure is the signal.
- **Never swallow a failed step and continue.** An agent proceeding past a failure is building on a premise that isn't true.
- **Make partial failure visible.** "Three of five workers succeeded" is a result to report, not an average to quietly return.

## Escalation

- **Write the escalation conditions into the spec, next to the success condition.**
- **Default to asking on anything irreversible** — money moved, data deleted, a message sent to a third party, anything outside stated authority.
- **Ambiguity in the request escalates before execution, not after.** Guessing early and discovering the guess was wrong late is the expensive order.
- **Give the human what they need to answer in one message:** what was attempted, what blocked it, what the options are, what you recommend.
- **If everything escalates, the agent is a slow interface to a person.** Persistent over-escalation means the authority boundary is drawn wrong.

## Idempotency and side effects

- **Assume every action happens twice.** Design for it rather than trying to guarantee it doesn't.
- **Attach an idempotency key to every side-effecting call the agent can make.**
- **Never place a non-idempotent action behind an automatic retry.** If it can't be made safe to repeat, it needs a guard or a confirmation, not a backoff.
- **Prefer reversible actions where the choice exists,** and prefer a staged action a human confirms over a direct one an agent takes alone.
- **Check-then-act is not safe unless it's atomic.** The gap between the check and the act is where the duplicate lands.

## Observability

- **Emit the trace as a product, not as debug output:** steps, tool calls, tokens, exit reason.
- **Record the exit reason on every run.** "Succeeded / errored / exhausted" is the single most useful field an agent system can log.
- **Log the shape decision too.** Six months later, "why is this an agent" should be answerable from the repo, not from memory.
