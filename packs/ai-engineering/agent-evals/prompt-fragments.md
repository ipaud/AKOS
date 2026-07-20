# Prompt Fragments — Agent Evals Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply agent-evals constraints (agent-evals pack, AKOS L2):
- Do not accept an agent improvement on demonstrations. A change is accepted
  on a suite result against a stated baseline, never on "here are a few
  outputs, they look better." The examples are fine as the first cases.
- Every reported number carries two things: what it was compared against, and
  the corpus it was computed over. A bare percentage is not a result.
- A golden dataset is fixed, representative, and versioned. All three. If one
  is being compromised - usually representativeness - say which, out loud.
- Include negative cases (the realistic near-miss where the right answer is
  not to act) and failure-injection cases (a tool errors, times out, returns
  garbage, or denies permission). Grade what happens next: recovered, gave up,
  or looped.
- Pick the cheapest grader the output shape allows: deterministic check first,
  then rubric, then LLM-as-judge, then pairwise. Never ask a model to decide
  something a schema, regex, test run, or numeric tolerance could decide.
- Never let a model grade its own output in the same context. Calibrate any
  judge against human labels before its scores gate anything, and re-calibrate
  when its model or the rubric changes.
- Score groundedness separately from correctness. An answer can be right and
  unsupported, or supported and wrong. Report hallucination rate on its own.
- Task completion is the headline metric, checked externally - the artifact
  exists, the record was written, the state changed. The agent's own claim of
  completion never satisfies the check. Step metrics are diagnostics beneath it.
- Record tokens, wall-clock, and tool-call count on every run. Report quality,
  cost, latency, and tool-call efficiency together, every comparison.
- Declare the regression bar in a committed config before running the change,
  set outside the suite's measured run-to-run variance.
- A baseline change is its own reviewed commit with a justification. It never
  happens in the same action as a failing run, and the harness must expose no
  flag that re-records it.
- Verify every case by deliberately breaking what it tests and watching it go
  red. A case never seen failing has not been shown to test anything.
- Run cases cold: no memory files, no carried session state, no leakage from an
  earlier case. Keep a held-out portion that is never iterated against.
```

## Fragment: review lens

```text
Review this work as an agent-evals reviewer (agent-evals pack). The question is
narrow: if this agent got worse, would anyone find out?
1. Evidence pass - what is the change actually backed by? Demonstrations, a
   suite with no baseline, a suite with a baseline but quality only, or a
   controlled comparison across all four dimensions? Name which.
2. Dataset pass - is the golden set fixed, representative, and versioned? Is
   the population it represents written down? Are there negative cases and
   failure-injection cases, or only the happy path?
3. Altitude pass - classify every case as unit / tool-call / trajectory /
   end-to-end. Report empty altitudes as named blind spots, not as silence.
4. Grader pass - for each case, name the grader type and ask whether the rung
   below would have worked. Flag any judge grading its own output, any
   uncalibrated judge that gates, any exact-match on free prose, any rubric
   whose levels lack behavioral anchors, and any pairwise win rate that has
   been converted into an absolute score.
5. Groundedness pass - is "is it supported" scored separately from "is it
   true"? Are fabricated citations/endpoints/figures full failures? Is there a
   case where the answer is absent from the context and a refusal is correct?
6. Completion pass - is completion checked externally, or inferred from the
   agent saying it finished? Multiply the step accuracies and compare against
   the observed completion rate; a large gap is itself the finding.
7. Cost pass - are tokens, latency (p50/p95), and tool-call count recorded and
   gated? An unmeasured dimension is a dimension that has been drifting.
8. Threshold pass - REQUIRES THE HISTORY. Was the bar committed before the run?
   Is there a measured noise floor behind it? Check the baseline's git log for
   an update landing in the same commit or command as a failing run, and check
   the harness for any flag that re-records a baseline.
9. Flakiness pass - is per-case pass rate tracked? Can anyone name "the flaky
   ones"? Does the report distinguish failed / flaky-known / re-run-to-green?
10. Contamination pass - do cases run cold? Is there a held-out set, and is its
    score reported next to the iterated set's? Are public-benchmark cases
    labeled? Any score rising with no plausible capability mechanism behind it
    is contamination until proven otherwise.
11. Vacuity pass - has each case been observed failing? If positive cases fail
    while negative cases pass after a harness change, suspect the harness, not
    the detectors - that asymmetry is the signature.
12. Run review-checklist.md; report findings by severity with the exact change
    needed - never "improve the evals" without naming the case, grader, or
    threshold to add.
```

## Fragment: suite audit

```text
Audit this eval suite. For each case:
- ID, altitude (unit / tool-call / trajectory / end-to-end), grader type.
- What it would catch, and one failure it structurally cannot catch.
- Has it ever been observed failing? If no, mark UNVERIFIED.
- Positive or negative case?
Then, for the suite as a whole:
- Corpus size and how cases were drawn. Held-out portion, if any.
- Altitude coverage table; empty rows named as blind spots.
- Grader distribution; flag any judged grade that a deterministic check could
  have produced.
- Dimensions measured vs. dimensions the system is expected to hold. Every
  unmeasured dimension is listed as a drift risk, not omitted.
- Threshold config: where it lives, when it was committed, whether a noise
  floor was measured.
- Baseline: where it lives, what it records beyond the number, and every way it
  can change.
Output a table, then the smallest set of additions that would close the largest
blind spot. No prose preamble.
```

## Fragment: result interrogation

```text
Interrogate this eval result before accepting it.
- What is the number compared against? If nothing, stop here: it is not a
  result yet.
- What corpus produced it - how many cases, drawn how, covering what?
- How many runs per case? What is the suite's run-to-run variance? Is the
  claimed delta larger than that variance?
- Did anything other than the variable under test change (corpus revision,
  grader version, model version, run count)?
- Are quality, cost, latency, and tool-call count all reported? Name any that
  are missing; a quality gain with an unreported cost is an incomplete result.
- Was the threshold set before or after this number was known?
- Could this comparison have come out against the change? If no design of it
  permitted a negative result, it is a demonstration, not evidence.
Verdict: EVIDENCE / INCOMPLETE / DEMONSTRATION, with the single question that
would move it up a rung.
```

## Fragment: red-suite triage

```text
The suite went red. Work this order exactly - the order is what stops the
convenient answer from being reached first.
1. FLAKY? Check the case's historical pass rate. Sitting between the bounds
   means this is a flakiness finding, not a regression finding. Do not re-run.
2. HARNESS? Did path resolution, matching, or skip logic change? Positive cases
   failing while negative cases pass is the signature of a harness bug, because
   a broken match makes "must not detect" hold for the wrong reason.
3. UNCONTROLLED? Did the corpus, grader, or run count move alongside the change
   under test? If so this is not a comparison; re-run controlled.
4. REAL REGRESSION? The change made the system worse. Fix the change.
5. CASE IS WRONG? Legitimate, and the most dangerous branch here, because it is
   what every regression wants to be mistaken for. Requires an explicit
   decision, a separate commit, and a reviewer who did not author the change
   that motivated it.
"The case is out of date" is a conclusion you may reach. It is never a
hypothesis you may start from. Re-running to green is not a resolution and is
reported as its own category.
```

## Fragment: grader selection

```text
Choose a grader for this eval case. Climb only as far as the output forces.
1. Can an external check decide it - a test run, a compile, a schema
   validation, a numeric tolerance? Use that. Best case; stop.
2. Does the output have a canonical form (enum, ID, number, structured field)?
   Exact match. Never exact-match free prose.
3. Does it have named quality dimensions? Rubric - with behavioral anchors per
   level, and per-criterion reporting so a drop is locatable.
4. Is it open-ended with no reference answer? LLM-as-judge. Separate instance,
   clean context, calibrated against human labels with the agreement rate
   recorded, re-calibrated on any model or rubric change, and explicitly told
   not to reward length, confidence, or stylistic self-similarity.
5. Is the real question "is B better than A"? Pairwise. Randomize order, report
   the position-bias check, and report a win rate against a named opponent -
   never converted into an absolute quality score.
State the rung chosen and why the rung below was insufficient.
```

## One-liner (for tight token budgets)

```text
Eval rules: never accept an agent change on three examples that looked better -
demand a suite and a stated baseline; every number carries its comparison and
its corpus or it isn't a result; golden sets are fixed, representative, and
versioned; include negative cases and injected failures, and grade recovery as
recovered/gave-up/looped; pick the cheapest grader that works (deterministic >
rubric > judge > pairwise) and never let a model grade its own output or an
uncalibrated judge gate anything; score groundedness apart from correctness;
task completion is the headline and is checked externally, never taken from the
agent's word; report cost, latency, and tool calls beside quality every time;
commit the regression bar before the run, outside the measured noise floor; a
baseline moves only by reviewed commit, never as a side effect of a failing run;
verify every case by breaking what it tests; run cold and hold out a set you
never iterate against.
```
