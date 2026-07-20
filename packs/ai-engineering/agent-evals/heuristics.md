# Heuristics — Agent Evals Pack

Fast defaults with known exceptions. Try these first; deviate with a reason.

## Starting a suite

- **Start from failures, not features.** The first twenty cases should be things you have actually seen go wrong, not a tour of the happy path. A suite built from the spec measures the spec.
- **Twenty imperfect cases beat two perfect ones, and beat zero indefinitely.** The suite that exists and grows is worth more than the representative corpus that is still being designed.
- **Write the case before the fix.** A production failure becomes a red case first, then gets fixed — the same discipline as a regression test, for the same reason.
- **If a case took an hour to write, it is probably an end-to-end case, and that's fine.** Expect the altitudes to cost different amounts and budget accordingly.

## Datasets

- **Fixed, representative, versioned — say which one you're compromising.** Most real suites compromise representativeness. Saying so out loud is what keeps the number honest.
- **Every positive case wants a near-miss twin.** The realistic input where the correct answer is "don't act" catches false-positive drift that no amount of positive cases will.
- **Hold out 20% and never look at it.** The moment you iterate against a case, it stops measuring and starts targeting.
- **Prefer sampled-from-production over invented, where privacy permits.** Invented cases encode what you imagine users do; sampled ones encode what they do.

## Choosing a grader

- **Climb the ladder as little as possible.** Deterministic check → rubric → judge → pairwise, and stop at the first rung that works. Every rung up adds variance and cost.
- **If a schema, a regex, a test run, or a numeric tolerance can decide it, don't ask a model.** A judge grading something checkable is paying for uncertainty.
- **Reach for pairwise when the question is "did this change help."** It is the shape of the question you usually have, and it is far easier to judge than absolute quality.
- **Don't convert a win rate into a quality score.** "B beats A 63% of the time" is a real result; "B scores 63" is not the same claim and is not supported by it.
- **Calibrate the judge on twenty human-labeled cases before you trust it.** If agreement is poor, the rubric is the problem, not the humans.

## Judge hygiene

- **Assume length bias until measured otherwise.** If the longer answer wins most pairs, check whether it wins on quality or on length.
- **Never let a model grade its own output in the same context.** It has already committed to the answer; the grade is a defense of it.
- **Swap the order and re-run a sample.** If the win rate moves materially, position bias is contaminating every pairwise number in the report.
- **Give the judge the criteria, not the expected answer**, when the point is open-ended quality — handing it the reference turns a judgment into a similarity check.

## Groundedness

- **Score "is it supported" separately from "is it true."** They fail independently and demand different fixes.
- **Include cases where the answer is genuinely absent from the context.** The correct output is a refusal, and a system that never gets tested on absence will confabulate on it.
- **Treat an invented citation as a full failure, not a deduction.** A fabricated source is the failure mode retrieval systems exist to prevent.

## Completion and trajectory

- **Ask "did the user get the thing," not "did the steps look right."** Step metrics are for diagnosis after the answer is no.
- **Multiply your step accuracies.** If twelve steps at 95% each are supposed to yield 90% completion, someone has not done the arithmetic.
- **Never accept the agent's own word for completion.** Check the artifact, the record, the state — externally.
- **Bound the trajectory, not just the outcome.** A correct answer reached in forty tool calls is a cost regression wearing a pass.

## Cost and latency

- **Report the quad or don't report.** Quality, cost, latency, tool calls — four numbers, every comparison, every time.
- **Gate cost like you gate quality.** An unthresholded dimension is an unmanaged one.
- **p95, not mean.** The mean hides exactly the runs users complain about.
- **Count redundant calls.** The same call twice in one run is usually a loop symptom that has not yet grown large enough to fail.

## Recovery

- **Break something on purpose in at least one case per tool.** An untested error path is an unmeasured recovery rate.
- **Grade three outcomes, not two:** recovered, gave up, looped. Collapsing them into pass/fail hides which defect you have.
- **Include one failure that retrying cannot fix.** It is the only way to find out whether the agent changes approach or just repeats itself louder.

## Thresholds and baselines

- **Set the bar before the run. Write it in a file.** A threshold you can recall from memory is a threshold you can revise from memory.
- **Measure your noise floor first.** Run the same version through the suite twice; the delta is the smallest regression you can honestly detect.
- **A baseline update is a commit with a reviewer, never a flag.** If your harness can re-record a baseline in the same breath as a failing run, delete the flag before writing another case.
- **Accepted regressions get written down with their reason.** Unwritten acceptance becomes the new normal within one release.

## Flakiness

- **Fix the harness before blaming the model.** Unseeded randomness, live network calls, and wall-clock timestamps account for most "model non-determinism."
- **Track per-case pass rate, and let the tracker call flakiness — not memory.** People are generous to cases they wrote.
- **A case re-run to green is a case that failed.** Say so in the report, or the suite stops meaning anything.
- **Better to delete a flaky case than to keep it and re-run past it.** A recorded gap is honest; a discounted red is corrosive.

## Contamination

- **Run cold.** No memory, no carried session, no earlier case leaking into this one.
- **If the held-out set diverges from the iterated set, that's contamination until proven otherwise.** "Noise" is the explanation to reach for last.
- **Label any case lifted from a public benchmark.** Its answer may be in training data, which makes the case a memory test.
- **Record every prompt change made in response to a specific case.** That case is now a target, and its score no longer measures what it used to.

## Reporting

- **Say the corpus with the number.** "100% over 21 curated cases" is honest; "100% recall" is an invitation to misread.
- **Name what a regression guard is not.** It does not estimate real-world detection rates, and saying so once in the report costs a sentence.
- **Report skipped cases and why.** A silent filter is how a suite quietly stops covering the thing that broke.
- **Prefer a trend to a snapshot.** One number is a state; a series is a signal, and slow degradation only ever shows up in the series.
