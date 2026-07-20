# Scoring Rubric — Agent Evals Pack

Standalone 0–100 score for an agent system's **evaluation discipline** — the suite, its graders, its thresholds, and its reporting. Not a dimension of the twelve-lens review pipeline (`core/review-pipeline.md` covers product/UX/accessibility/mobile/copy/frontend/architecture/security/performance/testing/database/release), and not a score of the agent itself. It answers a narrower question: *if this agent got worse, would anyone find out?*

Score = 100 − deductions, floor 0. Bands per [core/scoring-model.md](../../../core/scoring-model.md); this rubric supplies the deductions, that file supplies the bands, the severity anchors, and the verdict linkage.

One class of finding is scored as a correctness defect rather than a process concern: **a suite that reports something false about the system it measures**. A moving baseline, a vacuous case, a self-grading judge, and a contaminated run all produce numbers that are wrong in the direction of comfort, and every decision downstream of them inherits the error. These are graded like a wrong calculation, not like a missing best practice.

## Deductions

| Finding | Deduction |
|---------|-----------|
| A baseline was updated in the same commit or command as a run that failed against it (AEE54) | −25 (CRITICAL) |
| The harness exposes a flag/script/target that re-records a baseline as a side effect of a run (AEE55) | −25 (CRITICAL) |
| Cases exist that have never been observed failing, and no sabotage verification was done (AEE70) | −25 (CRITICAL) |
| A grader is the same model instance, in the same context, that produced the output under test (AEE24) | −25 (CRITICAL) |
| A gating LLM-judge has never been calibrated against human labels, or was not re-calibrated after its model changed (AEE22, AEE23) | −25 (CRITICAL) |
| Eval cases run with carried session state, memory files, or cross-case leakage (AEE64) | −25 (CRITICAL) |
| Case fixtures contain real secrets, real customer data, or copied production records (AEE8) | −25 (CRITICAL) |
| No baseline at all — results are reported with nothing to compare against (AE2) | −15 (HIGH) |
| The pass bar is not declared in a committed config predating the change under test (AEE51) | −15 (HIGH) |
| No run-to-run variance measured; the regression threshold has no noise floor behind it (AEE52) | −10 (HIGH) |
| A comparison moved more than the variable under test (corpus, grader, or run count also changed), unstated (AEE58) | −10 (HIGH) |
| Metrics reported without the corpus they were computed over (AEE9, AEE72) | −10 (HIGH) |
| A comparison reports quality without cost, latency, and tool-call efficiency (AEE41) | −10 (HIGH) |
| Task completion is not measured, or is satisfied by the agent's own claim of completion (AEE35, AEE38) | −15 (HIGH) |
| Groundedness is not scored separately from correctness on a retrieval or tool-using system (AEE29) | −10 (HIGH) |
| No failure-injection cases; recovery rate is unmeasured (AEE46, AEE47) | −10 (HIGH) |
| No negative cases — every case expects the system to act (AEE6, AEE13) | −10 (HIGH) |
| No held-out set, or the held-out score is not reported alongside the iterated one (AEE7, AEE67) | −10 (HIGH) |
| A known-flaky case remains in the gating suite (AEE61) | −10 each, cap −20 (HIGH) |
| Fabricated specifics graded as partial credit rather than full failure (AEE32) | −10 (HIGH) |
| Per-case pass rate is not tracked; flakiness is identified from memory (AEE60) | −6 (MEDIUM) |
| Cases do not declare their altitude, or an empty altitude is unrecorded (AEE10, AEE15) | −4 each, cap −12 (MEDIUM) |
| A judged grader decides something a schema check, regex, test run, or tolerance could decide (AEE18) | −4 each, cap −16 (MEDIUM) |
| Exact-match grading applied to free prose (AEE19) | −6 (MEDIUM) |
| A rubric's levels have no behavioral anchors, or per-criterion results are not reported (AEE20, AEE21) | −6 (MEDIUM) |
| Pairwise comparisons do not randomize order or report the position-bias check (AEE26) | −6 (MEDIUM) |
| A pairwise win rate has been converted into an absolute quality score (AEE27) | −6 (MEDIUM) |
| Cost and latency have no regression thresholds of their own (AEE42) | −6 (MEDIUM) |
| Latency reported as a mean with no percentiles (AEE43) | −4 (MEDIUM) |
| Recovery cases collapse recovered / gave up / looped into one pass/fail (AEE48) | −4 (MEDIUM) |
| Avoidable non-determinism (unseeded randomness, live network, wall-clock) left in place before variance was blamed on the model (AEE62) | −4 (MEDIUM) |
| An accepted regression carries no recorded reason or tradeoff (AEE56) | −4 (MEDIUM) |
| The dataset has no written statement of the population it represents (AEE2) | −4 (MEDIUM) |
| The harness has no tests of its own path resolution, matching, or skip logic (AEE74) | −4 (MEDIUM) |
| Cases are silently filtered or skipped without the report saying how many and why (AEE71) | −4 (MEDIUM) |
| A metric over a curated corpus is reported without the regression-guard caveat (AEE73) | −4 (MEDIUM) |
| Cases lack stable identifiers (AEE3) | −1 (LOW) |
| Cases drawn from public benchmarks are unlabeled (AEE66) | −1 each, cap −5 (LOW) |
| Redundant tool calls within a run are not counted (AEE45) | −1 (LOW) |
| Hallucination rate tracked per release only, not as a trend (AEE33) | −1 (LOW) |
| Completion reported only in aggregate, not per task category (AEE39) | −1 (LOW) |
| A stale report artifact is committed and readable as current (AEE76) | −1 (LOW) |

## Hard caps

- **Any open CRITICAL finding: score ≤ 59 (BLOCKED).** A suite that can be silently re-baselined, that contains cases never shown to fail, or that grades an output with the model that produced it is not measuring the system — it is producing numbers about it. How well the rest of the suite is built does not compensate, because every number it emits inherits the defect.
- No suite at all — changes accepted on demonstrations: **cap 39**. This is the state AE1 exists to name, and it is Blocked-band on purpose.
- Suite exists but gates nothing (advisory only, undocumented as such): **cap 69**.
- Suite lives entirely at one altitude with no gap recorded: **cap 79**.
- Correctness measured, cost and latency unmeasured: **cap 79**. AE15's drift is mechanical, not hypothetical.
- Suite unchanged for several release cycles while production failures arrived that no case describes: **cap 69**.

## Modifiers

- Every case verified by deliberate sabotage, with the procedure written down (AEE70): **+5**.
- A held-out set exists, is genuinely never iterated against, and its score is reported next to the iterated set's (AEE7): **+4**.
- Run-to-run variance measured and the threshold set outside it, both recorded (AEE52): **+3**.
- The harness has no mechanism by which a baseline can move as a side effect (AEE55): **+3**.
- Every production failure of the last release cycle became a case before its fix merged (AE16): **+3**.
- Known gaps stated in the suite's own documentation rather than left for the aggregate to imply (AEE15, AEE71): **+2** (cap 100).
- Repeat finding from a previous review, unfixed without a recorded tradeoff: **double its deduction**.

## Interpretation anchors

- **95** — a versioned golden set with negative and failure-injection cases across more than one altitude; graders chosen at the lowest rung that works and calibrated where they aren't deterministic; thresholds committed ahead of the run and set outside a measured noise floor; completion checked externally; quality, cost, latency, and tool calls reported together; baselines movable only by reviewed commit. Remaining findings are reporting polish.
- **85** — sound and trusted, with a cluster of MEDIUMs to schedule: a rubric criterion without anchors, latency reported as a mean, an altitude with thin coverage, a judge doing work a schema check could do.
- **72** — a real suite that genuinely gates, but narrow: one altitude, correctness only, no held-out set, thresholds by convention rather than by config. Acceptable pre-production with the gaps queued as real work rather than as documentation chores.
- **58** — the baseline moved to make a regression go away, or the suite contains cases nobody has ever seen fail. BLOCKED until the mechanism is removed and the affected numbers are re-established — not until the individual instance is explained, which leaves the next one open.
- **35** — changes are accepted on three examples that looked better. There is no measurement here to score, and the finding is the absence itself.
