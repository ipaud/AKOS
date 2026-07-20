# Anti-Patterns — Agent Foundations Pack

Named failure modes. Detection cue → why it fails → fix. The first block covers failures that produce *wrong or truncated output presented as complete*, or *a side effect applied more times than intended*; those are correctness defects and are scored as such.

## The silent truncation

**Detect:** a run hits its iteration cap, token budget, or wall-clock deadline, and returns whatever it had — in the same shape a successful run returns, with no field distinguishing the two.
**Why it fails:** every downstream consumer, human or machine, treats the partial result as the finished one. The cap did its job and the system converted a working safety limit into a confident wrong answer. This is the most common way a correctly-bounded agent still causes damage.
**Fix:** make `exhausted` a distinct outcome carrying which limit fired, what completed, and what did not (AF13, AFE46–AFE47). A caller must be able to tell success from exhaustion without reading the content.

## The double-charged retry

**Detect:** a side-effecting call (a payment, a message send, a row insert, a deploy) times out or errors, an automatic retry fires, and the original call had actually succeeded.
**Why it fails:** retries are the normal condition in an agentic system, not the exception — and an action correct only when executed exactly once will eventually execute twice. A timeout is not evidence of failure; it is evidence of no response.
**Fix:** every side-effecting action is idempotent, keyed, or atomically guarded, and retries reuse the original key (AF16, AFE63–AFE68). Actions that can't be made safe to repeat never sit on an automatic retry path.

## The agent that should have been a function

**Detect:** an agent with a loop, a tool set, and a planning prompt, whose actual runs all execute the same three steps in the same order.
**Why it fails:** it pays the full cost of nondeterminism — latency, tokens, untestability, an unpredictable step count — to absorb variance the task doesn't have. The flexibility is real and permanently unused, and every run is a fresh chance to do the known-correct sequence slightly wrong.
**Fix:** enumerate the paths across twenty real inputs. Few and stable → a fixed workflow, with a router at the front if there are two or three classes (AF1, AF3, AFE3, AFE5).

## The unbounded loop

**Detect:** a loop whose only stopping condition is the model deciding it's finished, or an iteration cap that exists but was never chosen — a framework default nobody looked at.
**Why it fails:** the model's sense of completion tracks plausibility, not correctness, and it fires earliest on exactly the tasks the model handles worst. Where completion never feels reached, the loop runs until something external kills it, usually the bill.
**Fix:** a checkable success condition stated before the loop starts, plus all four limits — iterations, tokens, tool calls, wall clock — each a number someone chose (AF11, AF12, AFE38, AFE44).

## The deterministic retry spiral

**Detect:** the same step fails with the same error on the same input, three, five, ten times, each retry separated by a growing backoff, consuming the run's entire budget.
**Why it fails:** backoff solves contention and transience. It does nothing for a failure whose cause is the approach — a malformed query, a wrong endpoint, a missing field — which will reproduce identically forever. The retry loop is the most expensive possible way to learn nothing.
**Fix:** classify before responding. An identical deterministic failure is never retried; the second identical occurrence replans or escalates (AF14, AFE51, AFE53).

## The vanity fan-out

**Detect:** a parallel fan-out where the branches all attempt the same task, and the aggregation step picks whichever output the model likes best — on a task whose single-pass output was already stable across runs.
**Why it fails:** voting buys confidence only where output quality genuinely varies between runs. Where it doesn't, N branches reproduce the same answer at N times the cost, and a model-chosen "best of" adds a selection step with its own error rate on top.
**Fix:** measure single-pass variance before adding a vote. Where it's low, remove the fan-out. Where it's high, state the aggregation rule before running, not after seeing the outputs (AF7, AFE17, AFE19).

## The dependent parallel

**Detect:** subtasks launched concurrently where one reads state another writes, or one's premise depends on another's result.
**Why it fails:** the concurrent branches compute against a world that the other branches are changing. The output isn't just slower to trust — it's derived from premises that were true when the branch started and false when it finished, and the inconsistency is invisible in the aggregate.
**Fix:** verify independence before fanning out — no shared writes, no consumed outputs. Dependent steps run serially, and the latency is the honest cost of the dependency (AF7, AFE16).

## The self-approving loop

**Detect:** an evaluator-optimizer where the criterion is some form of "is this good," and the loop exits when the evaluator says yes — typically on iteration one or two, with the evaluator praising output the generator produced from the same context.
**Why it fails:** an evaluator can only distinguish quality its criteria can express. Vague criteria give the loop a ceiling at superficial satisfaction, and a critic sharing the generator's context inherits its blind spots — so the loop converges quickly on mutual agreement rather than on quality.
**Fix:** criteria written before the first generation, specific enough that two evaluators would agree, and grounded in an external check wherever one exists (AF9, AFE27–AFE28, AFE32).

## The eternal refinement

**Detect:** an optimize loop running to its cap on every invocation, with iteration five's output no better than iteration two's — sometimes worse, having been polished past the point of improvement.
**Why it fails:** the loop has no notion of progress, only of "not yet done." Without an improvement check, an iteration that changes nothing looks identical to one that's about to break through.
**Fix:** implement the third exit — a non-improving iteration terminates the loop — and record each iteration's evaluation so churn is visible in the trace (AFE30–AFE31).

## The plan that was never revisited

**Detect:** an executing system discovers mid-run that a premise of its plan is false — the file doesn't exist, the API changed, the data has a different shape — and continues executing the remaining steps anyway.
**Why it fails:** the plan's status was never declared, so nothing in the system is responsible for noticing that it stopped applying. Every subsequent step does careful work on a false foundation, and the failure surfaces at the end as a confidently wrong result rather than at the point of contradiction.
**Fix:** declare the plan fixed or revisable; for revisable, name the triggers that force a replan, and make an invalidated assumption one of them (AF10, AFE33–AFE34).

## The replan thrash

**Detect:** a run that rewrites its plan four, six, eight times, each rewrite triggered by nothing more specific than the sense that progress is slow — often oscillating between two approaches, each looking attractive right after the other has failed.
**Why it fails:** replanning without a named trigger is a random walk with a planning step's cost attached. Work completed under each plan is discarded by the next, so the run pays repeatedly for the same ground.
**Fix:** replan only on a named invalidated assumption, cap replans per task, and escalate at the cap instead of writing plan seven (AFE34–AFE36).

## The multi-agent org chart

**Detect:** a system decomposed into agents mirroring human job titles — a researcher, a writer, an editor, a reviewer — where each handoff is a fresh model call and no single agent's failure was ever measured.
**Why it fails:** the org-chart metaphor is intuitive and the cost isn't. Each agent adds its own failure modes plus every handoff, every disagreement, every partial failure leaving the system in a state no component understands. The complexity is multiplicative while the perceived structure is additive.
**Fix:** build the single-agent version, measure where it actually fails, and add a second component only against that measurement (AF5, AFE6).

## The orchestrator that already knew

**Detect:** an orchestrator whose decomposition step produces the same subtask list on every input, spawning the same workers in the same configuration each run.
**Why it fails:** it pays a model call and a round of nondeterminism to re-derive a constant. Worse, it forfeits testability — a fixed workflow's steps can each be tested, while a re-derived decomposition can differ on the run you weren't watching.
**Fix:** if the subtask list can be written into the code, write it into the code. Reserve orchestration for decompositions that genuinely vary with the input (AF8, AFE21).

## The swallowed step

**Detect:** a step fails, the failure is logged at debug level or caught into a generic handler, and the run continues to the next step as though the failed one had produced something.
**Why it fails:** everything downstream now builds on a result that doesn't exist. The run usually completes — that's the problem — and returns an output whose defect traces back to a step that failed quietly twenty turns earlier.
**Fix:** a failed step recovers explicitly, replans, or escalates. "Continue anyway" is not an option, and mid-run failures appear in the final output even when the run ultimately succeeds (AFE55–AFE56).

## The escalation that never fires

**Detect:** an agent with no stated authority boundary, which has therefore never escalated anything — it resolves every ambiguity by assumption and takes every action its tools permit.
**Why it fails:** absent a written boundary, the agent's authority is implicitly the union of its tools' capabilities, which is a permission model nobody designed. The first genuinely ambiguous or irreversible case gets a confident guess instead of a question.
**Fix:** write the escalation conditions and the authority boundary into the spec, next to the success condition; default anything unlisted to "ask" (AF15, AFE57–AFE59).

## The escalation that always fires

**Detect:** an agent that stops and asks on nearly every run, so that a human is in the loop for routine cases the agent was built to handle.
**Why it fails:** the authority boundary is drawn too tight, making the agent a slower, more expensive interface to a person. It is the mirror image of the previous anti-pattern and produces the same conclusion: the boundary was never designed, just defaulted in one direction or the other.
**Fix:** widen the boundary on the classes that escalate routinely and have never needed the human, and keep the gate on irreversibility and threshold breach (AF15, AFE58).

## Budget as an afterthought

**Detect:** an architecture chosen for capability, with cost and latency caps added later — producing a system that works in development and is throttled in production into returning truncated work.
**Why it fails:** budget is not a constraint on a design, it's a filter on which designs are admissible. A shape that can't fit the envelope doesn't become able to by being capped; it becomes a shape that stops halfway.
**Fix:** state the per-invocation cost and latency envelope first, eliminate shapes that can't fit, then design inside what remains (AF17, AFE45).

## The untraceable run

**Detect:** an agent that emits only its final answer — no step log, no tool-call record, no token accounting, no exit reason.
**Why it fails:** every other rule in this pack becomes unenforceable. Nobody can tell how many iterations ran, whether the run exited on success or exhaustion, which retries fired, or where the budget went — so failures are unattributable and regressions are undetectable.
**Fix:** treat the trace as a first-class output with a structured exit reason, and link sub-agent runs to their parent (AF18, AFE69–AFE71).
