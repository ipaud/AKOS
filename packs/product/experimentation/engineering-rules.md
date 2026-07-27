# Engineering Rules — Experimentation Pack

Checkable before, during, and after a test. `★` marks the two rules that are floor
business rather than methodology: consent and harm do not suspend behind a feature flag.
Everything else is Level 3 practice — strong defaults with a stated context, not a floor.
Parenthetical codes cite the principle in [principles.md](principles.md).

## Before it starts

- EXP1. The decision is written down before launch: what ships if the result is positive,
  negative, or flat. If every branch ships, the test is cancelled. (P1)
- EXP2. Required sample size per arm is calculated from the baseline rate, the smallest
  effect worth shipping for, and the chosen significance and power. Calculated, not
  guessed. (P2)
- EXP3. Expected traffic is checked against that number *before* building the test. If the
  test would take more than about four weeks to reach it, it is not run — the answer is a
  different method. (P2, P3)
- EXP4. One decision criterion is declared in advance, along with the smallest effect on it
  that would justify shipping. (P4, P12)
- EXP5. Guardrail metrics are declared in advance: latency, error rate, and at least one
  measure of user harm relevant to this surface. (P6)
- EXP6. Metrics chosen as targets are checked against the way they could be gamed. If the
  cheapest way to move the number is to make the product worse, the metric is wrong. (P5)
- EXP7. The planned duration covers whole weeks and at least one full weekly cycle, so
  weekday and weekend behavior are both represented. (P15)
- EXP8. Segments to be analyzed are named in advance. Anything discovered later is recorded
  as a hypothesis, not a result. (P14)
- EXP9. The plan — criterion, guardrails, duration, sample size, segments, decision rule —
  is recorded somewhere durable before launch, so it can be compared with what was
  eventually reported. (P1, P8)

## Assignment and instrumentation

- EXP10. The randomization unit matches the analysis unit. Randomize by user and analyze by
  user; randomizing by user and analyzing by session inflates significance. (P9)
- EXP11. Assignment is stable — the same subject sees the same variant across sessions and
  devices where identity allows. (P9)
- EXP12. Assignment is independent of any user attribute: pure hashing on the unit
  identifier, never a rule that correlates with behavior. (P9)
- EXP13. Exposure is logged at the point the user could actually perceive the difference,
  not at page load or flag evaluation. Counting unexposed users dilutes the effect toward
  zero. (P9)
- EXP14. The observed traffic split is compared against the intended ratio, and a
  meaningful mismatch invalidates the test until explained. This is checked **before**
  looking at outcomes. (P9)
- EXP15. Filtering — bots, internal traffic, test accounts — is applied identically to
  every arm, and defined before launch. (P9)
- EXP16. The control arm is the current experience, unmodified, and receives the same
  instrumentation as the treatment. (P9)
- EXP17. The pipeline is validated with an A/A test before the first real experiment on a
  new setup: two identical arms should show no significant difference roughly as often as
  the threshold predicts. If A/A finds winners, the analysis is broken. (P9, P11)

## While it runs

- EXP18. The test runs to its planned duration. Stopping early because the number looks
  good is not permitted; stopping early for harm always is. (P8)
- EXP19. If early stopping is genuinely required, a sequential method with corrected
  thresholds is chosen in advance — not repeated looks at a fixed-horizon test. (P8)
- EXP20. Neither variant is changed mid-flight. A change restarts the test. (P8, P10)
- EXP21. Guardrails are monitored throughout, and a serious guardrail breach stops the test
  regardless of how the target metric is doing. (P6)
- EXP22. Traffic allocation is not adjusted mid-test unless the method accounts for it. (P8)
- EXP23. One change per test, or the analysis explicitly states that the bundle — not any
  component — is what was measured. (P10)

## Reading the result

- EXP24. Diagnostics are reviewed first: split ratio, exposure counts, filtering, data
  completeness. A failed diagnostic voids the result before it is interpreted. (P9)
- EXP25. Results are reported as an effect size with a confidence interval, never as a bare
  "significant" or "not significant". (P12)
- EXP26. The interval is compared against the smallest effect worth shipping for, declared
  in EXP4. A statistically significant effect below that threshold is a negative
  result. (P12)
- EXP27. A flat result is reported as "no detectable difference at this power", with the
  detectable threshold stated. It is never reported as "no difference". (P2, P12)
- EXP28. When several metrics or variants are compared, the threshold is adjusted or the
  inflated false-positive rate is stated explicitly. (P13)
- EXP29. Segment findings not pre-registered are labelled exploratory and, if they matter,
  become the next test rather than the current conclusion. (P14)
- EXP30. Where the effect trends across the test window, that is reported — a shrinking
  effect suggests novelty rather than a durable gain. (P15)
- EXP31. The result states what changed, not why it changed. Explanations are labelled as
  hypotheses. (P16)
- EXP32. The reported analysis matches the pre-registered plan; any deviation is stated,
  with its reason. (P1, P9)

## Deciding and shipping

- EXP33. The decision follows the rule written in EXP1. Re-litigating it after seeing the
  data is recorded as a deviation. (P1)
- EXP34. A win on the criterion with a guardrail regression is not shipped without an
  explicit, recorded tradeoff. (P6)
- EXP35. Shipped winners are rolled out gradually with the guardrails still monitored — an
  effect measured at 50% can behave differently at 100%. (P6)
- EXP36. The losing variant's code and the flag are removed once the decision is made.
  Stale experiment branches are a maintenance cost that compounds. (P1)
- EXP37. Results are recorded — including the negatives and the flat ones — so the same
  idea is not re-tested every year. Most tests fail, and that record is most of the
  value. (P11)

## When you cannot experiment

The common case. See [decision-framework.md](decision-framework.md).

- EXP38. Where power is insufficient, the honest alternatives are named and one is chosen:
  qualitative research, usability testing, a staged rollout watched for harm, an
  instrumented launch with a rollback trigger, or simply deciding on judgement and saying
  so. (P3)
- EXP39. A change shipped without an experiment is still instrumented, so a regression is
  visible even though the causal claim is not available. (P3,
  [observability](../../devops/observability/README.md))
- EXP40. A decision made on judgement is recorded as such. "We tested it" is never claimed
  for a test that was not powered to detect the effect. (P3, EXP27)
- EXP41. Where an effect is genuinely too small to detect but the change is cheap and
  low-risk, shipping it and moving on is a legitimate answer. Not everything needs
  evidence proportional to its cost. (P1)

## The people in it

- EXP42 ★. Experiments do not withhold safety, accessibility, or security from an arm.
  Testing a degraded experience against a floor requirement is not a valid design. (P17)
- EXP43 ★. Data collected for experimentation is personal data and is treated as such —
  inventoried, minimized, retained deliberately, and covered by the deletion path
  ([privacy PR1/PR20](../../security/privacy/engineering-rules.md)). (P17)
- EXP44. Changes that could plausibly cause distress, financial loss, or discrimination get
  a review before launch, not after a complaint. (P17)
- EXP45. A test that could not be described to its participants without embarrassment is
  not run. (P17)
