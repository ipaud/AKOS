# Prompt Fragments — Experimentation Pack

Copy-paste blocks for injecting this pack into an agent prompt. Read this file first — in
most cases the gate block below is the whole answer.

## Fragment: the gate (use this before anything else)

```text
Someone proposed an experiment. Before designing it, do the arithmetic:

n per arm ≈ 16 · p · (1 − p) / δ²
   p = baseline rate, δ = smallest ABSOLUTE difference worth detecting
   (5% significance, 80% power — an approximation; the point is the scaling)

On a 3% baseline: detecting a 10% relative lift needs ~52,000 per arm (~104,000 total).
A 5% relative lift needs ~207,000 per arm. Halving the effect quadruples the requirement.

Divide by weekly traffic into the funnel:
  under ~5,000/week   → cannot A/B test conversion. Say so.
  5,000-50,000/week   → only large effects. Check each test individually.
  over ~100,000/week  → real experimentation is available.

If the answer is no, THAT IS THE FINDING. Do not lower the threshold, do not shorten the
test, do not run it anyway. An underpowered test does not give a weaker answer — it gives
a wrong one that sounds like an answer, and someone will quote it.

Instead pick and record one of:
  - usability testing (five people, no statistics)
  - user interviews for "do they want this"
  - staged rollout with instrumentation and a rollback trigger
  - decide on judgement, record the reasoning, ship, watch

"We decided" is honest. "We tested it" about an underpowered test is not.
```

## Fragment: build-mode constraint block (only if the gate passed)

```text
EXPERIMENT CONSTRAINTS:

Before launch — all of this written down, before any data exists
- What ships if the result is positive / negative / flat? If every branch ships, cancel.
- ONE decision criterion, plus the smallest effect on it worth shipping for.
- Guardrails: latency, error rate, and at least one measure of user harm.
- Ask: could this criterion go up while the product gets worse? If easily, it's wrong.
- Duration: the calculated sample size, whole weeks, at least one full weekly cycle.
- Segments to be analyzed, named now.

Assignment
- Randomize by user, analyze by user. Mismatched units manufacture significance.
- Assignment stable across sessions and devices; hash the identifier, never a rule
  correlated with behavior.
- Log exposure where the user could PERCEIVE the difference — not at page load or flag
  evaluation. Counting unexposed users drags every effect toward zero.
- Identical filtering across arms, defined before launch.

While running
- Run to the planned duration. Do not stop early because the number looks good — that
  manufactures significance and it feels like diligence. Harm is the only valid early stop.
- Do not change either variant mid-flight.
- Monitor guardrails throughout.

Reading it
- DIAGNOSTICS FIRST, outcomes second. Split ratio matches intended? A mismatch voids the
  test — and once you've seen the outcome you can't un-see it.
- Report effect size with an interval, never a bare "significant".
- Compare the interval against the shipping threshold, not against zero.
- A flat result is "no difference larger than X detectable at this power" — NEVER
  "no difference".
- Segments not pre-registered are exploratory: the next test, not this conclusion.

FLOOR (applies at any scale, even where the rest of this doesn't):
- No arm withholds safety, accessibility, or security. The floor is not contingent on
  whether users are observed to want it.
- Experiment data is personal data: inventoried, minimized, retained deliberately, covered
  by the deletion path.
```

## Fragment: review lens

```text
Review this experiment against the AKOS experimentation pack (product/experimentation).

CHECK POWER FIRST. If the test could not detect the effect it was meant to find, that is
the finding and every methodology comment after it is moot — reviewing the design of a test
that should not exist legitimizes it. Ask what effect the test could have detected; if
nobody knows, say so.

Only two findings are CRITICAL and both are floor: an arm withholding safety,
accessibility or security (EXP42), and experiment data with no lawful basis or deletion
path (EXP43).

Then in order: a decision reported as evidence from an underpowered test, early stopping
without a pre-declared sequential method, criterion chosen after seeing data, unchecked
sample ratio, randomization/analysis unit mismatch, post-hoc segments presented as
conclusions.

Two specific things to look for that reviewers usually miss:
- "Not significant" reported as "no effect".
- A program reporting mostly wins. Most tested changes do nothing or hurt; a high win rate
  means peeking, post-hoc metric choice, or a broken pipeline — not product skill.

For each finding: rule code, what claim it invalidates, and the smallest fix.
```

## One-liner (for tight token budgets)

```text
Experiment floor: calculate n ≈ 16p(1−p)/δ² per arm FIRST — under ~5k weekly users you
cannot A/B test conversion and that's the finding, not a reason to lower the bar. Write the
decision for every outcome before launch; one pre-declared criterion plus guardrails;
randomize and analyze on the same unit; log exposure at perception; fixed duration, no
peeking; check the split ratio BEFORE the outcome; report intervals not verdicts; "no
detectable difference at this power", never "no difference"; post-hoc segments are the next
test. Never withhold safety/accessibility/security from an arm; experiment data is personal
data. Can't test? Decide, record why, ship, watch — and never say "we tested it".
```
