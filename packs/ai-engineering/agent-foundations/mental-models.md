# Mental Models — Agent Foundations Pack

Named models this pack contributes. Use them as diagnostic lenses while choosing, bounding, or debugging an agent architecture.

## The shape spectrum

Systems built on language models fall along an ordered spectrum defined by one variable: who chooses what happens next.

| Shape | Who chooses the path | Right when | Wrong when |
|---|---|---|---|
| **Single call** | The engineer (there is no path) | One transformation, one output, no branching | The task has genuinely distinct sub-steps that need separate quality control |
| **Prompt chain** | The engineer, at design time | Steps are fixed, sequential, and each one's output is the next one's input | The steps aren't actually sequential, or the order varies by input |
| **Routing** | A classifier, once, at the front | Inputs fall into distinguishable classes that want different handling | The classes overlap so heavily that one handler serves all of them equally well |
| **Parallelization** | The engineer (fan-out is fixed) | Subtasks are independent (sectioning), or repeated sampling raises confidence (voting) | Subtasks depend on each other, or one pass was already reliable |
| **Fixed workflow** | The engineer, as a graph of steps | The set of paths is enumerable and stable | Real inputs keep producing paths nobody enumerated |
| **Orchestrator-worker** | A model, deciding the decomposition at run time | The number and nature of subtasks vary with the input | The subtask list is the same every time — write it down instead |
| **Evaluator-optimizer** | A model, judging against criteria until they pass | Clear criteria exist and iteration measurably improves the output | Criteria are vague, or the first pass is already good enough |
| **Agent** | The model, continuously, including when to stop | The path genuinely cannot be enumerated ahead of time and the environment gives feedback | Anything above would have worked |
| **Multi-agent** | Several models, plus the coordination between them | A measured failure of the single-agent version, in a specific dimension | It was reached for because the domain has several roles in it |

The spectrum is not a capability ladder — it's a schedule of decisions transferred from the engineer to the model. Every step down transfers more.

**Diagnostic:** name the shape you're building, out loud, before building it. If the honest answer is "an agent, because that's what we're building," you haven't made the choice yet.

## The path-knowability test

The whole workflow-vs-agent question reduces to one empirical question: at design time, can you enumerate the sequences this task actually takes? Not the sequences it could conceivably take — the ones observed on real inputs. If the list is short and stable, it belongs in code as a workflow, where each edge is testable and each step is separately improvable. If real inputs keep generating sequences nobody anticipated, that variance is what an agent is for.

**Diagnostic:** collect twenty real inputs and write out the step sequence each one needs. Count distinct sequences. Two or three means a router in front of a workflow. Twenty distinct sequences with no pattern means the agent is earned.

## The decision-point budget

Think of each place the model chooses the next action as an item you're purchasing, priced in unpredictability. A fixed workflow with model-powered steps has zero decision points — the model does work but never chooses order. A router has one. An agent has one per turn, unbounded. This reframes architecture review from "is this too agentic" (unanswerable) to "how many decision points does this have, and what does each one buy" (checkable, and usually revealing that half of them cover variance the system doesn't actually face).

**Diagnostic:** count the decision points in a proposed design. For each, name the specific input variance it exists to absorb. Any point without an answer is a fixed edge waiting to be written down.

## Sectioning vs. voting

Two entirely different things get called parallelization, and conflating them produces fan-outs that cost N times as much for no benefit. **Sectioning** splits one task into independent parts, runs them concurrently, and combines the pieces — it buys wall-clock latency and lets each part be handled with focused attention. **Voting** runs the same task N times and aggregates — it buys confidence on tasks with a high variance in output quality, at N times the cost, and buys nothing at all on tasks where the model is already reliable.

**Diagnostic:** for any fan-out, say whether the branches produce *different pieces of one answer* or *different attempts at the same answer*. If neither describes it, the fan-out isn't parallelization — it's duplication.

## The runaway loop

The characteristic failure of an under-specified agent is not a crash — it's a loop that keeps going. It has three common shapes: retrying a deterministic failure that will fail identically every time; oscillating between two approaches, each of which looks better when the other has just failed; and refining an output that is already adequate, because nothing states what adequate is. All three consume the entire budget and produce something between nothing and slightly-worse-than-turn-three.

**Diagnostic:** for any loop, ask what makes iteration N+1 different from iteration N. If the answer is "the model will think about it again," it's a runaway waiting for the right input.

## The three error responses

Failures sort into three classes with three different correct responses, and the cost of misclassifying is high in both directions.

| Class | Looks like | Response | Cost of getting it wrong |
|---|---|---|---|
| **Transient** | Timeout, rate limit, network blip, intermittent tool failure | **Retry**, with backoff and a cap | Replanning discards a working approach over noise |
| **Approach-level** | The step succeeded mechanically but the result is wrong; the same error recurs identically | **Replan** — the plan rested on a false premise | Retrying burns the whole budget repeating an identical failure |
| **Terminal** | Missing permission, missing information only a human has, an action outside stated authority | **Escalate** | Retrying and replanning both consume budget on something no amount of iteration can resolve |

**Diagnostic:** before responding to any failure, say which class it's in and why. An error handler that doesn't distinguish the classes is applying one response to all three, and two of them will be wrong.

## The escalation contract

An agent operating without stated escalation conditions is implicitly claiming authority over everything it can reach. The contract makes that explicit and inverts the default: here is what this agent may decide alone, here is what it must stop and ask about, and here is what it may never do. Written at design time, it's a specification. Left to run time, it's a judgment call made by the component with the least perspective, at the moment it most wants to finish.

**Diagnostic:** ask what this agent is not allowed to do without asking. If the answer has to be constructed on the spot, the contract doesn't exist and the agent's authority is whatever its tools happen to permit.

## The at-least-once world

Distributed systems long ago accepted that delivery is at-least-once and built idempotency accordingly. Agent systems are in the same world and often haven't noticed: retries duplicate, timeouts fire after the call succeeded, parallel workers overlap, replans re-execute completed steps. The model to hold is that any side-effecting action may execute twice, and the second execution is not a bug to prevent but a condition to survive.

**Diagnostic:** for every side-effecting tool an agent can call, ask what happens if it's called twice with identical arguments. If the answer is "two of them," that tool needs an idempotency key or a guard before the agent is allowed to retry through it.

## The evaluator's ceiling

An evaluator-optimizer loop cannot produce output better than its criteria can distinguish. If the criteria are "make it better," the loop's ceiling is whatever the evaluator finds superficially satisfying, and iterations past the first mostly reshuffle. If the criteria are checkable against something external — a test suite, a schema, a numeric tolerance, a named list of required elements — the ceiling rises to the quality the criteria encode, and iteration converges instead of wandering.

**Diagnostic:** could a second evaluator, given the same criteria, reach the same verdict on the same output? If not, the criteria aren't criteria, and the loop has no exit condition.

## The plan's status

Every plan in an executing system is in one of two declared states: **fixed** (execute as written; deviation is a failure to report) or **revisable** (execute, and replan when a stated trigger fires). Systems get into trouble when the status was never declared, because the two failure modes look opposite but share a cause: an undeclared-fixed plan drives through a discovered contradiction, and an undeclared-revisable plan thrashes between approaches on vibes.

**Diagnostic:** ask what would have to be discovered mid-execution for this plan to be rewritten. A crisp answer means revisable with a trigger. "Nothing, it's the plan" means fixed, which is fine if it was chosen. No answer at all means the failure is already latent.

## The exhaustion outcome

Runs end in one of three states, not two: **success** (the termination condition was met), **error** (something failed unrecoverably), and **exhausted** (a limit fired first). The third is routinely collapsed into the first, and that collapse is where truncated work gets returned as if it were finished. Holding exhaustion as a distinct, first-class outcome — with its own return shape carrying what was and wasn't completed — is what keeps a budget cap from becoming a silent correctness bug.

**Diagnostic:** look at what a run returns when it hits its iteration cap. If it's indistinguishable from a successful return, the cap is producing confident partial answers and nobody downstream can tell.

## The compounding surface

Each component added to an agent system contributes its own failure modes plus an interaction with every existing component: handoffs that lose information, agents that disagree, one waiting on another, partial failure leaving the system in a state no single component understands. The growth is not additive, which is why the second agent is a much bigger step than it looks and the fifth is a different system entirely.

**Diagnostic:** for each additional agent or coordination layer, name the specific measured failure of the simpler topology that it fixes. "Cleaner separation" is a description of the diagram, not a capability.
