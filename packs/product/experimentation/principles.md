# Principles — Experimentation Pack

Durable rules for controlled experiments on real users. Level 3: decision frameworks, not
commandments — and the first three exist to stop most readers from using the rest. The
`EXP*` codes in [engineering-rules.md](engineering-rules.md) derive from these.

## Whether to run one at all

- **P1 — An experiment is a decision procedure, not a measurement.** Before it starts, name
  what you will do for each possible outcome. If every outcome leads to shipping, you have
  a launch with extra steps; if no outcome would change anything, you have theatre. Both
  are common and both cost weeks.
- **P2 — Power comes before p-values, and it is arithmetic rather than opinion.** A test
  that cannot detect the effect you care about will not report "no effect" — it will report
  noise, and somebody will believe it. Detecting a 10% relative lift on a 3% conversion
  rate needs roughly fifty thousand users *per arm*. Halve the effect and the requirement
  quadruples.
- **P3 — Most products do not have the traffic, and that is the finding.** Running an
  underpowered experiment is worse than running none: it converts "we don't know" into a
  number people will quote. When the arithmetic says no, the honest answer is a different
  method — see [decision-framework.md](decision-framework.md) — not a smaller threshold.

## What you measure

- **P4 — Decide the metric before you see the data.** The single criterion the decision
  rests on, chosen up front. Picking it afterwards means picking whichever moved, which is
  a procedure guaranteed to find something.
- **P5 — A metric optimized is a metric distorted.** Any measure adopted as a target stops
  measuring what it did. The decision criterion must be close enough to real value that
  gaming it *is* delivering value — engagement measures are the classic failure, because
  the easiest way to raise them is usually to make the product worse.
- **P6 — Guardrails exist so that a win can still be a loss.** Latency, error rate, refund
  rate, unsubscribes, accessibility regressions. A change that lifts the target while
  degrading a guardrail is not a winner, and without guardrails declared in advance nobody
  will look.
- **P7 — Short-term measurable and long-term valuable are different things,** and the gap
  is where most damage is done. Dark patterns, aggressive notifications, and interstitials
  all win two-week experiments.

## Running it honestly

- **P8 — Fix the duration in advance and do not stop early because you like the number.**
  Repeatedly checking a running test and stopping at significance manufactures significance:
  the p-value was defined for one look, not many. This is the most common way to be
  confidently wrong.
- **P9 — Diagnostics are checked before results, and a failed diagnostic voids the
  result.** If the traffic split does not match the intended ratio, something is broken in
  assignment, logging, or filtering — and the comparison is invalid however clean the
  numbers look. Reading the outcome first makes it impossible to unsee.
- **P10 — Test one change at a time, or accept that you learned about a bundle.** Shipping
  five changes together and measuring the total tells you the bundle won; it tells you
  nothing about which parts to keep.
- **P11 — Effects are small and most ideas fail.** Across mature products the large majority
  of tested changes do nothing or hurt. A pipeline reporting mostly wins is not unusually
  good at product; it is measuring wrong.

## Reading it honestly

- **P12 — Statistical significance is not practical significance.** With enough traffic,
  trivial differences become significant. Decide in advance the size of effect worth
  shipping for, and read the interval rather than the verdict.
- **P13 — The more comparisons you make, the more false winners you find.** Twenty metrics
  at the 5% threshold produce one spurious result on average. This applies to metrics,
  variants, and segments alike.
- **P14 — Segments discovered after the fact are hypotheses, not results.** "It worked for
  mobile users in Spain" found by slicing a flat result is the same procedure as P13 with
  more dignity. Pre-register the segments that matter or treat the finding as something to
  test next.
- **P15 — Novelty and primacy fade.** Regular users react to change *as change*; a
  short test measures the reaction, not the steady state. Effects that shrink across the
  test window are the tell.
- **P16 — An experiment says what happened, never why.** Causal attribution is its
  strength; explanation is not. Pair it with qualitative work
  ([continuous-discovery-habits](../continuous-discovery-habits/README.md)) or ship a
  correct number attached to a wrong story.

## The people in it

- **P17 — Experiment subjects are users, not units.** Consent obligations, harm, and
  fairness do not suspend because a change is behind a flag. A test that would be
  indefensible if described to the people in it is indefensible —
  see [security/privacy](../../security/privacy/README.md) for what the measurement data
  itself obliges you to.

## Scope

This pack covers designing, running, and reading controlled experiments: power and sample
size, criterion and guardrail selection, assignment integrity, stopping rules, and
interpretation. It does not cover deciding *what* to build
([inspired](../inspired/README.md)), the hypothesis-and-learning loop around it
([lean-startup](../lean-startup/README.md)), talking to users
([continuous-discovery-habits](../continuous-discovery-habits/README.md)), the
instrumentation that produces the numbers
([devops/observability](../../devops/observability/README.md)), or evaluating
non-deterministic model output
([ai-engineering/agent-evals](../../ai-engineering/agent-evals/README.md)).
