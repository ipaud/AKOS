# Principles — Agent Foundations Pack

Durable rules of agent architecture. Each carries an **operational corollary** — the form the principle takes when it hits a system design. Violating one requires an explicit tradeoff statement.

## AF1 — The agent is the last shape to reach for, not the first

A deterministic function, a fixed workflow, or a direct query is cheaper, faster, testable, and reproducible. An agent is none of those things. Reaching for an agent because the problem involves language, or because agents are the interesting shape to build, produces a system that costs more and fails in more ways than the thing it replaced — usually to solve a problem whose path was knowable in advance all along.

**Corollary:** before building an agent, state what the deterministic version would look like and why it fails. If that sentence can't be written, build the deterministic version.

## AF2 — Agency trades predictability for adaptability, and the trade is always paid

Letting a model choose the path buys the ability to handle tasks whose steps can't be enumerated ahead of time. It costs determinism, testability, latency ceilings, cost ceilings, and the ability to say in advance what the system will do. There is no configuration that gets the adaptability without the cost — every increment of agency is bought with an increment of unpredictability.

**Corollary:** every place a model decides the next step is a design decision that must be justified by a specific kind of variance the system genuinely faces. Decision points a fixed edge could have covered are removed, not tuned.

## AF3 — If the path is knowable in advance, encode the path

The distinction between a workflow and an agent is not sophistication — it's who chooses the sequence. When the sequence is known at design time, encoding it as a fixed workflow gives you the model's language ability at each step without surrendering control of the order, and it makes every step independently testable. Handing a known sequence to an agent to rediscover per invocation pays for flexibility that is never used.

**Corollary:** enumerate the paths the task actually takes in production. If the list is short and stable, wire it as a workflow with a routing step at the front, not as an agent with a prompt describing the paths.

## AF4 — Agency is a spectrum, and the right answer is usually further down it than instinct suggests

Between one model call and a full agent there are several intermediate shapes — a prompt chain, a router, a parallel fan-out, a fixed workflow with model-powered steps — each of which handles a real class of task and none of which requires the model to control the loop. Treating the choice as binary ("is this an agent or not") skips past the shapes that solve most problems.

**Corollary:** pick a shape from the spectrum explicitly and record the choice. "We considered a workflow and chose an agent because X" is a design artifact; drifting into an agent because nobody named the alternative is not.

## AF5 — Complexity in agent systems compounds multiplicatively

Adding a second agent does not add one component's worth of failure surface; it adds the failures of that agent, plus every handoff, plus every way the two can disagree, plus every way one can wait on the other. Multi-agent topologies are occasionally the right answer and routinely reached for a step too early, because the org-chart metaphor is intuitive in a way that the cost is not.

**Corollary:** each additional agent, tool, or coordination layer must buy a specific capability the simpler topology demonstrably cannot deliver. "Separation of concerns" is not a capability; a measured failure of the single-agent version is.

## AF6 — Routing is a classification problem, and it belongs at the front

Many systems handle several distinct kinds of request badly through one generic path, because the prompt tries to be adequate for all of them at once. Classifying the incoming task first and dispatching to a handler specialized for that class lets each handler be sharp instead of average, and lets simple classes take a cheap path while hard classes take an expensive one.

**Corollary:** where inputs fall into distinguishable classes, put a classification step first, dispatch to a named handler per class, and define the fallback class explicitly. An unroutable input must land somewhere stated, never in whichever handler happens to be last.

## AF7 — Parallelism buys latency or confidence, never correctness on its own

Running independent subtasks concurrently (sectioning) shortens wall-clock time. Running the same task several times and aggregating (voting) raises confidence in the result. Neither makes a wrong approach right, and both multiply cost per invocation. Parallelizing dependent steps produces work done against stale premises, which is worse than the serial version, not faster.

**Corollary:** name which of the two you're buying before fanning out. If the answer is neither — if the subtasks depend on each other, or a single pass was already reliable — the fan-out is cost and complexity with no return.

## AF8 — Decompose dynamically only when the subtasks aren't knowable in advance

An orchestrator that decides at run time what the subtasks are, spawns workers for them, and synthesizes their results is the right shape when the decomposition genuinely depends on the input. When the subtasks are the same every time, the orchestrator is an expensive, nondeterministic way to re-derive a list you already had.

**Corollary:** if you can write the subtask list into the code, write it into the code. Reserve orchestrator-worker for cases where the number and nature of subtasks vary with the input in ways a fixed decomposition can't cover.

## AF9 — A critique loop is only as good as its criteria, and the criteria must be external

Asking a model to improve its own output without stating what "better" means produces churn: rewording, restructuring, and confident declarations of improvement that don't converge on anything. An evaluator with explicit, checkable criteria — ideally ones an external check can confirm, like a passing test or a schema validation — turns the same loop into genuine iteration.

**Corollary:** every evaluator-optimizer loop states its criteria before the first generation, in a form the evaluator can apply the same way twice. A loop whose exit condition is the evaluator's unstructured satisfaction has no exit condition.

## AF10 — A plan is a hypothesis, and its status must be declared

Plans made before execution are made with less information than execution produces. A system that treats its initial plan as fixed will drive straight through a discovered contradiction; a system that rewrites the plan on every surprise will thrash and never finish. Both failures come from the same omission: nobody stated whether this plan is revisable, and under what trigger.

**Corollary:** state at design time whether a plan is fixed or revisable, and if revisable, what specific conditions trigger a replan. Replanning on a vague sense that things are going badly is thrash; replanning on a named invalidated assumption is engineering.

## AF11 — "Done" is defined before the loop starts, never inferred after

A loop whose termination is left to the model's judgment terminates when the model feels finished, which correlates with plausibility rather than with completion. The condition that ends a loop is part of the loop's specification, and writing it forces the harder question of what the task actually produces.

**Corollary:** every loop declares its success condition in checkable terms before it runs — an artifact exists, a test passes, a schema validates, a value is within tolerance. "The model says it's done" is a signal, not a termination condition.

## AF12 — Every loop needs a limit, and the limit is separate from the success condition

Success conditions say when the loop should stop happily. Limits say when it must stop regardless. A loop with only a success condition runs forever whenever the success condition can't be met, and the cases where it can't be met are exactly the cases you didn't anticipate.

**Corollary:** every loop carries an iteration cap, a token budget, a tool-call budget, and a wall-clock bound, each set to a number someone chose on purpose. A loop bounded only by "it'll finish eventually" is unbounded.

## AF13 — Hitting a limit is a result, and it must be reported as one

The dangerous version of budget exhaustion is the quiet one: the loop stops, the last partial output is returned, and it looks exactly like a completed answer. Downstream systems and humans then act on truncated work with no signal that anything was cut short. An exhausted budget is a specific outcome with a specific name, distinct from both success and error.

**Corollary:** budget exhaustion returns an explicit exhausted status carrying what was completed, what wasn't, and which limit was hit. Silently returning partial work as if it were complete is a correctness defect, not a degradation.

## AF14 — Errors come in three kinds, and the response differs by kind

A transient failure wants a retry. A wrong approach wants a replan — retrying it just fails identically, more expensively. A failure the system cannot resolve at all wants escalation to a human. Applying the wrong response is its own failure mode: retrying a deterministic error burns the whole budget on repetition, replanning a network blip discards a good approach over noise, and escalating everything makes the agent a slower interface to a human.

**Corollary:** classify a failure before responding to it — transient, approach-level, or terminal — and route it to retry, replan, or escalate accordingly. An undifferentiated "on error, try again" is a budget-burning loop wearing a recovery strategy's clothes.

## AF15 — Escalation conditions are design-time artifacts

Deciding mid-task whether a situation warrants a human is a judgment call made by the component least equipped to make it, at the moment it has the least perspective. The conditions under which an agent must stop and ask — irreversible actions, thresholds exceeded, ambiguity in the request, repeated failure on the same subtask — are properties of the system, and they're specified with the system.

**Corollary:** write the escalation conditions into the agent's specification, alongside its success condition and its limits. Any action outside the agent's stated authority stops and asks by default, rather than proceeding on an assumption of permission.

## AF16 — Every agent action must be safe to repeat

Retries, replans, timeouts that fire after a call actually succeeded, and parallel workers overlapping on the same resource all produce duplicate execution. In an agentic system this is the normal case, not the exceptional one — which means an action that is only correct when it happens exactly once is an action that will eventually be wrong.

**Corollary:** every side-effecting action an agent can take is idempotent, or carries an idempotency key, or is guarded by a check-then-act that is itself atomic. Where true idempotency is impossible, the action requires confirmation and cannot be reached by an automatic retry path.

## AF17 — Budget is an input to shape selection, not a cap bolted on afterward

Cost, latency, and token budget don't just constrain an architecture — they determine which architecture is admissible. A task with a sub-second latency requirement cannot be an agent, whatever the prompt says. A task whose per-invocation budget is a few thousand tokens cannot afford an evaluator loop with three iterations. Discovering this after the shape is built produces a system that is throttled into uselessness rather than designed to fit.

**Corollary:** state the per-invocation cost and latency envelope before choosing a shape, and eliminate shapes that can't fit inside it. A shape chosen first and budgeted second is a shape that will be capped mid-loop and return truncated work.

## AF18 — An agent that can't be observed can't be bounded

Every rule in this pack — termination, limits, error classification, escalation, idempotency — assumes someone can tell what the agent actually did. A system that emits only its final answer offers no way to know how many iterations ran, which tool calls failed, where the budget went, or whether the loop exited on success or exhaustion. The rules become unenforceable, and the failures become unattributable.

**Corollary:** the trace of a run — steps taken, tools called, tokens spent, exit reason — is a first-class output, not a debugging afterthought. If you can't answer "why did this run stop" from the trace, the system has no termination discipline regardless of what its code says.
