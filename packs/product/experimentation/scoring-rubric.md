# Scoring Rubric — Experimentation Pack

Feeds [scoring/product-score.md](../../../scoring/product-score.md). Scores **the
experimentation practice**, not the product and not the result of any individual test.

Two refusals built in: a surface without the traffic to run experiments scores `n/a`, and
having no experimentation program is never itself a deduction.

## Deductions (from 100)

| Finding | Deduction |
|---------|-----------|
| An arm withholds safety, accessibility, or security from real users | −40 (CRITICAL) |
| Experiment data collected with no lawful basis, retention, or deletion path | −25 (CRITICAL) |
| A decision was made on an underpowered test and reported as evidence ("we tested it") | −25 (HIGH) |
| A test was stopped early because the number looked good, with no sequential method declared in advance | −25 (HIGH) |
| Decision criterion chosen after seeing the data | −25 (HIGH) |
| Sample ratio never checked, or a mismatch ignored | −15 (HIGH) |
| Randomization unit and analysis unit differ | −15 (HIGH) |
| No decision written before launch for each possible outcome | −10 (HIGH) |
| No guardrail metrics declared | −10 (HIGH) |
| A flat result reported as "no difference" with no detectable-effect threshold stated | −10 (HIGH) |
| Exposure logged at page load or flag evaluation rather than at perception | −10 (HIGH) |
| Post-hoc segment finding presented as a conclusion | −10 (HIGH) |
| Criterion trivially gameable by degrading the product | −6 (MEDIUM) |
| Results reported as bare significance rather than effect size with an interval | −6 (MEDIUM) |
| Multiple comparisons neither adjusted nor acknowledged | −6 (MEDIUM) |
| Variant changed mid-flight, or duration extended after launch | −6 (MEDIUM) |
| Filtering differs between arms, or was defined after launch | −6 (MEDIUM) |
| Duration shorter than a full weekly cycle | −4 (MEDIUM) |
| Pipeline never validated with an A/A test | −4 (MEDIUM) |
| Effect compared only against zero, never against the shipping threshold | −4 (MEDIUM) |
| Novelty trend not examined on a visible change to an established interface | −4 (MEDIUM) |
| Guardrail regression shipped alongside a win with no recorded tradeoff | −4 (MEDIUM) |
| Winner rolled out at once rather than gradually | −2 (LOW) |
| Losing variant's code and flag left in place | −2 (LOW) |
| Results not recorded, so the same idea gets re-tested | −2 (LOW) |
| Change shipped without a test and without instrumentation | −2 (LOW) |

## Caps and floors

- Any CRITICAL: score ≤ 59 (Blocked band), per
  [core/scoring-model.md](../../../core/scoring-model.md). Both CRITICALs are safety floor
  rather than methodology.
- **`n/a` when the surface lacks the traffic to run a powered experiment.** Not a low
  score — `n/a`. Scoring a small product's experimentation practice would penalize it for
  arithmetic it does not control, and would imply it should be running tests it cannot
  read.
- **Not running experiments is never a deduction.** A team that did the sample-size
  arithmetic, concluded it could not experiment, chose another method and recorded the
  judgement has done this correctly and scores at the top of the band.
- **`n/a` under Prototype and Startup MVP**, except the two CRITICALs.
- A test whose result was read but whose diagnostics were never checked scores as if the
  test had not been run — a void result is not partial credit.

## Anchors

- **95** — power calculated before building, decision written for every outcome, criterion
  and guardrails pre-registered, diagnostics before outcomes, fixed duration honored,
  results reported as intervals against a shipping threshold, negatives recorded.
- **85** — sound practice; MEDIUM gaps (no A/A validation, comparisons unadjusted)
  scheduled.
- **72** — tests run and read reasonably, but the discipline is informal: no pre-registered
  plan, occasional peeking, segments explored after the fact.
- **60** — results are being quoted that the tests could not support.
- **≤ 40** — decisions presented as evidence-based rest on tests that were never powered,
  never diagnosed, or read until they said something.
