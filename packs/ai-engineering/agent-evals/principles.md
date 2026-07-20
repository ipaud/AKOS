# Principles — Agent Evals Pack

Durable rules of measuring an agent. Each carries an **operational corollary** — the form the principle takes when it hits a suite, a grader, a threshold, or a review. Violating one requires an explicit tradeoff statement.

## AE1 — Three examples that worked is an anecdote, not evidence

The default way an agent improvement gets proposed is a handful of prompts the author tried after making the change, all of which look better than they did before. That evidence is selected twice over: the author chose which prompts to try, and chose when to stop trying. It cannot distinguish a real improvement from a change that helped these three inputs and hurt the twenty nobody ran. The count is not the deepest problem — the selection is — but a suite large enough to be inconvenient to cherry-pick is the cheapest available defense.

**Corollary:** an agent change is accepted on a suite result, not on demonstrations. If the only evidence is "here are some outputs, they look better," the correct response is to ask for the suite, not to read the outputs more carefully.

## AE2 — A measurement without a baseline is decoration

"The agent completes 74% of tasks" is an unusable sentence. Compared to what — the previous version, a simpler prompt, no agent at all, a human? Every eval result is a comparison, and when the comparison is left implicit the reader supplies a flattering one. A number reported alone gets read as good, because nobody volunteers a number they think is bad.

**Corollary:** every reported eval result names what it is compared against and states both figures. A result with no stated comparison is an incomplete report — returned, not interpreted.

## AE3 — A golden dataset is fixed, representative, and versioned, and the three are inseparable

Drop *fixed* and two runs cannot be compared, because the input moved underneath them. Drop *representative* and the suite measures a distribution nobody encounters — in practice, the easy one. Drop *versioned* and last month's result cannot be reproduced or explained, because nobody can reconstruct what ran. A set with two of the three is not a golden dataset with a caveat; it is a pile of examples that will be mistaken for one.

**Corollary:** a dataset earns the word "golden" only when it lives under version control, changes only through a reviewed commit, and carries a written statement of the population it represents and how its cases were drawn from that population.

## AE4 — An eval is a test suite whose assertions tolerate variation and grade judgment

Structurally an eval suite is the same object as a test suite: fixed inputs, expected behavior, a runner, a pass/fail report, a CI gate. What differs is the assertion. Traditional tests compare exact values produced by a deterministic system; evals grade a distribution of plausible outputs from a non-deterministic one. That single difference propagates everywhere — into how many times a case runs, into what "expected" can even mean, into whether one red result is a regression or a sample.

**Corollary:** reuse the entire apparatus of testing — fixtures, CI, coverage thinking, red-green discipline — and replace only the assertion layer. Rebuilding the harness is wasted work; reusing the exact-match assertion is a category error. See [packs/testing/testing-pyramid](../../testing/testing-pyramid/README.md) for the apparatus this specializes.

## AE5 — Different eval granularities catch different failures, and none subsumes the others

A unit eval on one prompt-and-response catches a broken instruction. A tool-call eval catches wrong arguments and wrong tool selection. A trajectory eval catches a path that reached the right answer by an unacceptable route, or wandered thirty steps before converging. An end-to-end eval catches whether the user's actual task got done. Running only the cheap layer misses the expensive failures; running only the expensive layer says something broke without saying where.

**Corollary:** state which granularity each case operates at, and audit the suite for a layer with no cases in it. A suite made entirely of one layer has a known blind spot, and naming which one is part of reporting the result.

## AE6 — The grader is part of the system under test and needs its own evaluation

A rubric two people apply differently, or an LLM judge that prefers longer answers regardless of quality, produces numbers that move for reasons having nothing to do with the agent. The grader is not neutral instrumentation sitting outside the experiment — it is a component with its own error rate, its own biases, and its own capacity to regress when the model behind it changes.

**Corollary:** every non-deterministic grader is calibrated against human-labeled cases before its scores are trusted, and re-calibrated whenever the grader model or the rubric changes. An uncalibrated judge emits a measurement with an unknown error bar, which is not a measurement.

## AE7 — Groundedness is a separate axis from correctness

An answer can be correct and ungrounded — right by coincidence or by prior knowledge rather than derived from the context and tools the agent was actually given. It can also be grounded and wrong, faithfully reflecting a source that was itself wrong. Collapsing the two into one "is it right" score hides the failure mode that matters most in a retrieval or tool-using system: a fluent, plausible claim with nothing behind it.

**Corollary:** score whether each load-bearing claim traces to the provided context or a tool result, separately from whether the claim is true. Report hallucination rate as its own number, never folded into an accuracy figure.

## AE8 — Task completion is the outcome metric; step correctness is a diagnostic

Every intermediate step can be individually defensible while the task still fails — the agent picked reasonable tools, made reasonable calls, produced reasonable intermediate output, and never delivered what was asked. Step-level metrics are how you find *where* it went wrong; they do not establish *whether* it went wrong, and a suite reporting only step metrics will report health during a failure.

**Corollary:** every end-to-end case defines completion in terms an outside observer can check — the artifact exists, the record was written, the value is within tolerance — and reports completion rate as the headline. Step metrics sit underneath it as diagnosis, never in place of it.

## AE9 — Cost, latency, and tool-call efficiency are eval dimensions, not afterthoughts

A change that lifts task completion from 71% to 74% while tripling token spend and doubling p95 latency is not obviously an improvement, and a correctness-only suite reports it as one. These are not operational concerns to check once the quality question is settled; they are part of the quality question, because a system nobody can afford to run has no completion rate at all.

**Corollary:** every eval run records tokens, wall-clock, and tool-call count per case alongside its grade, and every baseline comparison reports all four. A correctness gain paired with an unreported cost regression is an incomplete result.

## AE10 — Recovery is a capability, and only failure-injecting cases measure it

An agent that never meets a failing tool in its suite has an unmeasured recovery rate, and the two failure modes that hides — giving up at the first error, and looping on the same failing call until the budget dies — are both common and both invisible on a happy-path suite. Recovery does not show up as a slightly degraded score on normal cases; it shows up as a cliff the first time production returns a 503.

**Corollary:** the suite contains cases that deliberately fail — a tool returning an error, a missing permission, a malformed response, a dead end requiring a different approach — and grades what the agent does next, not merely whether it survived.

## AE11 — The regression bar is a number stated before the run, not a judgment made after it

A threshold decided after seeing the result is not a threshold; it is a rationalization with a percent sign attached. The pressure is specific and real: a change everyone wants to ship lands two points below the previous version, and "two points is within noise" becomes an appealing sentence precisely because it is sometimes true. Deciding in advance is what makes it checkable rather than negotiable.

**Corollary:** the suite declares its pass bar — absolute floor, maximum allowed drop from baseline, and which metrics are gated — in a config file, before the change is run. A bar edited in the same commit as a failing result is a finding, not a tuning.

## AE12 — A flaky eval destroys trust faster than a missing one

A case that passes and fails on the same input at the same version teaches everyone who reads the report to discount failures. Once a suite holds a few of those, red stops carrying information — people re-run until green, and the one genuine regression in the batch gets re-run away with the rest. A missing eval leaves a known gap; a flaky eval corrodes the credibility of the cases around it.

**Corollary:** a case identified as flaky is fixed — by tightening the grader, seeding the inputs, or raising the run count so the metric is a rate rather than a coin flip — or removed from the gate with the removal recorded. It is never left in the suite to be re-run past.

## AE13 — An eval whose answer has leaked measures memory, not capability

Contamination has three routes and only one involves training data. An expected answer can leak into pretraining. It can leak into the agent's own accumulated context — a memory file, a cached note, an earlier turn of the same session. And it can leak in by iteration, when the system is tuned against the suite until it fits those particular cases. All three produce the same signature: a score that rises with no corresponding rise in capability.

**Corollary:** hold out a portion of the suite that is never used for iteration, refresh cases periodically, and run every case against a clean context. A score improving on the iterated set but not on the held-out set is a contamination signal, not a win.

## AE14 — Updating a baseline is a decision, never a side effect

The most damaging single action available to anyone maintaining a suite is quietly re-recording the baseline after a failing run. It makes the regression disappear without anyone deciding to accept it, and after it happens once every later comparison is against a number nobody vouched for. The mechanism matters more than the intent: a harness with a convenient `--update-baseline` flag will have its baseline updated conveniently, by people who meant no harm and were in a hurry.

**Corollary:** a baseline change is its own commit with its own justification, reviewed separately from the change that motivated it. It never happens in the same action as a failing run, and never as a flag on the runner.

## AE15 — Any dimension not measured drifts, and the drift is silent

A suite that evaluates correctness and not cost produces a system that gets more correct and more expensive. One that evaluates helpfulness and not groundedness produces a system that hallucinates more helpfully. This is not a hypothesis about incentives — it follows mechanically from the fact that every change is accepted or rejected on measured dimensions, which leaves the unmeasured ones free to move.

**Corollary:** for every dimension the system is expected to hold (correctness, groundedness, cost, latency, safety, tone), either a measurement exists or its absence is recorded as a known blind spot. Silence is not the same as "fine."

## AE16 — A suite that never grows stops discovering anything

A fixed set of cases is a regression guard for failures already known. It cannot surface a new failure mode, because no case describes one. Suites that stop growing converge on 100% and stay there while the system's real failure rate is determined entirely by inputs the suite never contemplated.

**Corollary:** every production failure a reviewer would have wanted the suite to catch becomes a new case, before the fix is merged. A suite at 100% across several release cycles needs harder cases; it is not evidence that the system stopped failing.

## AE17 — A case that cannot fail is not a case

A case that passes vacuously — because its grader matches anything, because its path resolution is broken, because its assertion is tautological — is worse than no case: it occupies a slot in a coverage claim while testing nothing. This is not exotic; it is the ordinary failure mode of eval harnesses, and it hides specifically in negative cases, where "nothing was detected" is simultaneously the expected result and what a broken check produces.

**Corollary:** every case is verified by deliberately breaking the thing it tests and confirming the case goes red. A case never observed failing has never been shown to test anything.

## AE18 — A score means nothing without the coverage behind it

100% over twenty-one curated cases and 100% over two thousand sampled from production are the same number and entirely different claims. Reporting the figure without the corpus invites the reader to assume the second when it is almost always the first, and the assumption goes uncorrected because the number itself is honest.

**Corollary:** every reported metric carries its corpus — how many cases, drawn how, covering what — in the same breath as the number. This composes with [core/scoring-model.md](../../../core/scoring-model.md)'s bands and [core/confidence-model.md](../../../core/confidence-model.md)'s coverage-versus-confidence distinction rather than restating them: a narrow eval can be entirely trustworthy about what it measured, and should say so.
