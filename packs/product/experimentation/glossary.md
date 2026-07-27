# Glossary — Experimentation Pack

Terms this pack uses precisely. Where a word collides with another pack's usage, the entry
says so.

- **Controlled experiment / A/B test** — randomly assigning subjects to variants so the
  difference in outcomes can be attributed to the change. Its strength is causal
  attribution; it cannot say *why*.
- **Arm / variant** — one experience under test. Control is the current experience,
  unmodified.
- **Randomization unit** — what gets assigned: a user, a session, an account. Must match
  the analysis unit, or significance is manufactured.
- **Exposure** — the moment a subject could actually perceive the difference. Logging
  assignment instead of exposure dilutes every effect toward zero.
- **Decision criterion (OEC)** — the single measure the decision rests on, chosen before
  the data exists.
- **Guardrail metric** — something that must not get worse while the criterion improves.
  `devops/sre` uses "guardrail" for an SLO-adjacent limit; here it is an experiment's veto
  condition.
- **Statistical power** — the probability of detecting an effect of a given size if it is
  real. Conventionally 80%. Low power does not produce cautious results; it produces noise.
- **Minimum detectable effect** — the smallest effect a test can reliably find at its
  sample size. The number that turns "not significant" into a meaningful statement.
- **Sample size** — subjects needed *per arm*. Scales with the inverse square of the effect,
  which is why halving the effect quadruples the requirement.
- **Statistical significance** — the result is unlikely under the assumption of no
  difference. Not a measure of importance, and not proof of anything.
- **Practical significance** — the effect is large enough to be worth shipping for. With
  enough traffic, trivial differences become statistically significant.
- **Confidence interval** — the range of effects consistent with the data. More informative
  than a significance verdict, and what should be reported.
- **Peeking** — repeatedly checking a running test with the option to stop at significance.
  Manufactures significance; the threshold was defined for one look.
- **Sequential testing** — a method allowing valid early stopping, with corrected
  thresholds. Must be chosen before launch, not applied retroactively.
- **Sample ratio mismatch (SRM)** — observed traffic split differing meaningfully from the
  intended ratio. Evidence that assignment, logging, or filtering is broken; voids the
  result.
- **A/A test** — two identical arms. Should find a difference no more often than the
  threshold predicts; if it finds winners, the pipeline is broken.
- **Multiple comparisons** — testing many metrics, variants, or segments inflates the
  false-positive rate. Twenty at the 5% threshold yield one spurious winner on average.
- **Post-hoc segment** — a subgroup found by slicing after the fact. A hypothesis for the
  next test, never a conclusion from this one.
- **Novelty effect** — regular users reacting to change *as change*. Decays; a short test
  measures the reaction rather than the steady state.
- **Primacy effect** — the mirror case: users initially performing worse because the
  familiar path moved.
- **Pre-registration** — recording the plan — criterion, guardrails, duration, sample size,
  segments, decision rule — before launch, so the report can be compared against it.
- **Underpowered** — unable to detect the effect of interest. The default state of most
  products, and the reason this pack opens with arithmetic.
