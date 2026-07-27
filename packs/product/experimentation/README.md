# Pack: Experimentation — Power Before p-values

**Domain:** Product · **Authority:** Level 3 (book) · **Version:** 1.0.0

Controlled experiments on real users: power and sample size, criterion and guardrail
selection, assignment integrity, stopping rules, and how to read a result without fooling
yourself.

Independent distillation for personal engineering use. Not affiliated with or endorsed by
the source authors. See [references.md](references.md) for the original — read it; this
pack is a lossy operational index, not a substitute.

## Read this first: you probably cannot run experiments

The required sample per arm, for a conversion comparison at the usual thresholds, is
approximately `16·p·(1−p)/δ²`. On a 3% baseline:

| Detect | Per arm | Total |
|---|---|---|
| 10% relative lift | ~52,000 | ~104,000 |
| 5% relative lift | ~207,000 | ~414,000 |

Halve the effect, quadruple the requirement. Under roughly 5,000 weekly users into the
funnel, conversion is not experimentable — and **that is the finding**, not a reason to
lower a threshold.

Running an underpowered test is worse than running none: it converts "we don't know" into a
number people will quote. The [decision framework](decision-framework.md) opens with the
arithmetic and lists what to do instead.

## When to load this pack

- Someone proposed an A/B test — the sample-size check is two minutes and cancels most of
  them.
- A result is being used to justify a decision and you want to know whether it can bear
  the weight.
- A product genuinely has the traffic and the practice needs setting up.
- Any experiment touching accessibility, safety, or personal data — the two floor rules
  apply at every scale.

## What's inside

| File | Highlights |
|------|-----------|
| [principles.md](principles.md) | P1–P17. Whether to run one, what to measure, running and reading honestly, the people in it. |
| [engineering-rules.md](engineering-rules.md) | EXP1–EXP45, including a section on what to do when you *cannot* experiment. Only two rules are starred. |
| [decision-framework.md](decision-framework.md) | **The arithmetic**, a traffic table, alternatives when the answer is no, choosing the criterion, how long to run, a result-reading ladder. |
| [review-checklist.md](review-checklist.md) | Gate first, then by severity. Reviewer discipline: check power before anything else. |
| [anti-patterns.md](anti-patterns.md) | The underpowered test, peeking, the metric chosen afterwards, sample ratio mismatch, segment mining, the suspiciously successful program. |
| [scoring-rubric.md](scoring-rubric.md) | `n/a` without the traffic; not running experiments is never a deduction. |
| [heuristics.md](heuristics.md) | Defaults while deciding whether and how to test. |
| [prompt-fragments.md](prompt-fragments.md) | Build-mode block, review lens, the pre-launch plan. |
| [glossary.md](glossary.md) | Terms used precisely, including collisions with other packs. |
| [references.md](references.md) | The source, the arithmetic's caveat, and what Level 3 means here. |

## Core claim, one line

A test that cannot detect the effect you care about will not report "no effect" — it will
report noise, and somebody will believe it.

## The two starred rules

Both are floor rather than methodology, and both apply even where the rest of the pack does
not: **no arm withholds safety, accessibility, or security** (EXP42 — the floor is not
contingent on whether users are observed to want it), and **experiment data is personal
data** (EXP43), inventoried and deletable like any other
([security/privacy](../../security/privacy/README.md)).

## Related packs

[product/lean-startup](../lean-startup/README.md) ·
[product/inspired](../inspired/README.md) ·
[product/continuous-discovery-habits](../continuous-discovery-habits/README.md) ·
[devops/observability](../../devops/observability/README.md) ·
[ai-engineering/agent-evals](../../ai-engineering/agent-evals/README.md)
