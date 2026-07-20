# Decision Framework — Agent Foundations Pack

Decision rules for agent-architecture calls. Compose with [core/decision-framework.md](../../../core/decision-framework.md).

## Which shape does this task want

Work down the table and stop at the first row that fits. The order is deliberate: the cheapest shape that works is the answer, and each row is more expensive and less predictable than the one above it.

| The task looks like | Shape | Why not the next one down |
|---|---|---|
| One transformation, one output, no branching | **Single model call** | A chain adds boundaries where information gets lost, for no gain |
| A fixed sequence where each step's output feeds the next | **Prompt chain** | A router adds a classifier for classes that don't exist here |
| Distinguishable classes of input that want different handling | **Routing** | Parallelism doesn't help; the classes are alternatives, not parts |
| Independent subtasks that can run at once, or one task worth sampling repeatedly | **Parallelization** (sectioning / voting) | A workflow serializes what could have run concurrently |
| A known, enumerable set of paths through several steps | **Fixed workflow** | An orchestrator re-derives a decomposition you already have |
| Subtasks whose number and nature depend on the input | **Orchestrator-worker** | An open agent gives up the decompose-then-synthesize structure that fits here |
| Clear criteria exist, and iteration measurably improves the output | **Evaluator-optimizer** | A bare agent has no exit condition; this one does |
| The path genuinely can't be enumerated, and the environment gives feedback the model can act on | **Agent** | Multi-agent multiplies failure surface before the single agent has failed |
| A measured, specific failure of the single-agent version | **Multi-agent** | Nothing below it worked |

**Rule:** name the row before building. If two rows seem to fit, take the higher one and find out empirically whether it's insufficient — moving up the table later is a refactor; moving down is a rewrite of a system people have already come to trust.

## Is the agent warranted at all

Answer all four. Any "no" sends you back up the table.

1. **Can you enumerate the paths?** Collect twenty real inputs, write the step sequence each needs, count distinct sequences. Few and stable → workflow with a router. Many and patternless → the variance is real.
2. **Is there feedback the model can act on?** An agent adapts by observing the result of its last action. Where the environment returns nothing informative — no test result, no tool error, no state change to observe — the loop has nothing to steer on and is just repeated sampling.
3. **Is the cost of a wrong step recoverable?** Agents take steps nobody enumerated. If any reachable step is irreversible and expensive, either that step goes behind an escalation gate or the shape is wrong.
4. **Does the envelope allow a loop?** A latency budget in the hundreds of milliseconds, or a token budget of a few thousand per invocation, excludes an agent regardless of how well it fits the other three.

## Sectioning, voting, or don't parallelize

| Situation | Choice |
|---|---|
| The task splits into parts that don't depend on each other, and you want the wall-clock time down | **Sectioning** — fan out the parts, combine the pieces |
| One task, high output variance across runs, and confidence matters more than cost | **Voting** — N attempts, stated aggregation rule |
| Subtasks where one consumes another's output | **Don't** — run serially; parallel work here computes against stale premises |
| A single pass is already stable across runs | **Don't** — N samples reproduce the same answer at N times the price |
| You want "a second opinion" but can't say what would make one output beat another | **Don't** — that's an aggregation rule you haven't written, and you'll pick it after seeing the results |

**Rule:** state which of latency or confidence you're buying, and the aggregation rule, before the fan-out runs. Cap the width explicitly — a fan-out sized by input data is an unbounded cost multiplier.

## Fixed workflow or orchestrator-worker

| Question | Fixed workflow | Orchestrator-worker |
|---|---|---|
| Do you know the subtasks at design time? | Yes | No — they depend on the input |
| Does the subtask count vary per input? | No | Yes |
| Is the value in the decomposition itself? | No, it's in the steps | Yes — deciding what the parts are *is* the work |
| Can each step be tested independently? | Yes | Only the workers, not the decomposition |
| What does it cost when it goes wrong? | A step fails, visibly, at a known place | The decomposition is wrong and every worker does good work on the wrong parts |

**Rule:** if you can write the subtask list into the code, write it into the code. An orchestrator that produces the same decomposition every time is a workflow that pays a model call to remember itself, and it has traded testability for nothing.

## Add an evaluator loop, or don't

Add it when **all** of these hold:

- The criteria for a good output can be written down before the first attempt.
- A second party applying those criteria to the same output would reach the same verdict.
- Iteration measurably improves the result — you have seen pass two beat pass one on this task class.
- The envelope affords two or three full generations plus evaluations.

Skip it when any of these hold:

- The criteria amount to "better" — the loop's ceiling is the evaluator's superficial satisfaction, and iterations mostly reshuffle.
- The first pass is already adequate; the loop is insurance against a failure that isn't occurring.
- An external check (a test, a validator, a compiler) could gate the output directly — use the check as the gate, without the loop.
- The evaluator shares the generator's context and blind spots, so its critique inherits whatever the generation got wrong.

**Rule:** the exit condition is the criteria passing, the iteration cap, or a non-improving iteration — implement all three. A loop that only exits on success runs to the cap whenever success isn't reachable.

## Fixed plan or revisable plan

| Situation | Status | Trigger to replan |
|---|---|---|
| The steps are known and the environment is stable | **Fixed** | None — deviation is a failure to report, not to route around |
| The plan rests on assumptions the execution will test | **Revisable** | A named assumption is invalidated |
| A required resource may turn out to be unavailable | **Revisable** | The resource is confirmed unavailable — not suspected |
| A subtask may prove harder than estimated | **Revisable** | The same subtask failed identically twice |
| Progress feels slow | **Neither** | Not a trigger. This is where thrash comes from |

**Rule:** declare the status at design time. Cap replans on a single task — three rewrites is thrash, and the correct response at the cap is escalation, not a fourth plan.

## Retry, replan, or escalate

Classify the failure first; the class determines the response.

| Signal | Class | Response |
|---|---|---|
| Timeout, rate limit, 5xx, intermittent tool error | **Transient** | **Retry** with backoff, small explicit cap |
| The step completed but produced a wrong or unusable result | **Approach-level** | **Replan** — name the invalidated assumption |
| The identical error recurs on the identical input | **Approach-level** | **Replan**, never retry — the third attempt fails the same way |
| Missing permission, missing credential, action outside stated authority | **Terminal** | **Escalate** |
| Information only a human has (a decision, an ambiguous requirement, a business judgment) | **Terminal** | **Escalate** |
| The same subtask has now failed twice on its own terms | **Terminal for this run** | **Escalate** — further iteration is budget spend, not progress |

**Rule:** the classification is recorded, not just the response. An error handler that retries everything is applying one response to three classes and will be wrong on two of them — most expensively on the deterministic failure, where it burns the entire budget reproducing an identical error.

## When must this stop and ask

Escalate by default on any of the following, and write them into the spec rather than deciding at run time:

- **Irreversibility.** Money moves, data is deleted, a message reaches a third party, a deployment goes out.
- **Authority.** The action sits outside what the agent was explicitly permitted to do — the default for anything unlisted is "ask," not "assume."
- **Ambiguity in the request.** Escalate before execution. Guessing early and discovering the guess was wrong after ten steps is the expensive order.
- **Threshold breach.** A value exceeds a stated bound — a refund over a limit, a diff over a size, a spend over a cap.
- **Repeated failure.** The same subtask has failed twice.
- **Budget exhaustion on incomplete work.** The run stopped at a limit with the task unfinished; a human decides whether to extend or abandon.

**Rule:** if these conditions can't be written down for a given agent, its authority is currently "whatever its tools permit," which is a permission model nobody chose.

## What does a run return

Three outcomes, three shapes — never two.

| Outcome | Meaning | Must carry |
|---|---|---|
| **Success** | The stated termination condition was met | The result, and the trace |
| **Error** | Something failed in a way the system could not recover from | What failed, at which step, whether anything was partially applied |
| **Exhausted** | A limit fired before the termination condition was met | Which limit, what completed, what did not, and whether partial side effects landed |

**Rule:** a caller must be able to distinguish these without inspecting the content of the result. Collapsing `exhausted` into `success` is how truncated work becomes a confident answer, and it is scored as a correctness defect rather than as a performance issue.

## Can this action be taken twice

Ask it of every side-effecting tool before the agent is allowed to retry through it.

1. **Is it naturally idempotent?** (Setting a value, writing a known file, upserting by key.) Safe.
2. **Can it take an idempotency key?** Attach one, and reuse the same key on retry rather than generating a fresh one.
3. **Can it be guarded by an atomic check-then-act?** Only if the check and the act are genuinely atomic — a check followed by a separate act has a gap, and the duplicate lands in the gap.
4. **None of the above?** It does not go on an automatic retry path. It goes behind a confirmation, or the run escalates instead of retrying.

**Rule:** a timeout is not evidence the action failed. Before retrying a timed-out side effect, verify the actual state of the thing it would have changed.
