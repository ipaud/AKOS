# Decision Framework — Experimentation Pack

The choices this domain presents. The first section decides whether the rest applies, and
for most projects it does not.

## Do you have the traffic? Do the arithmetic first

For a comparison of two conversion rates at the usual 5% significance and 80% power, the
required sample **per arm** is approximately:

```
n  ≈  16 · p · (1 − p) / δ²

p = baseline rate,  δ = smallest absolute difference worth detecting
```

Worked, on a 3% baseline conversion rate:

| Effect you want to detect | Per arm | Total |
|---|---|---|
| 10% relative lift (3.0% → 3.3%) | ~52,000 | ~104,000 |
| 5% relative lift (3.0% → 3.15%) | ~207,000 | ~414,000 |

Halving the effect quadruples the requirement. That relationship is the whole reason this
pack opens here.

Now divide by your weekly traffic:

| Weekly users into the funnel | Verdict |
|---|---|
| Under ~5,000 | Not experimentable on conversion. Nothing in this pack applies except the ethics rules. |
| 5,000 – 50,000 | Only large effects (20%+) or high-frequency metrics. Most tests will be underpowered — check each one. |
| Over ~100,000 | Genuine experimentation is available. |

**If the answer is no, that is the finding.** Say so and pick a method below. Running the
test anyway does not produce a weaker answer; it produces a wrong one that sounds like an
answer (P3).

## When you cannot experiment, what then?

| Situation | Method |
|---|---|
| "Will people understand this?" | Usability testing. Five people, no statistics required. |
| "Do people want this?" | [continuous-discovery-habits](../continuous-discovery-habits/README.md) — interviews, not a test. |
| "Will this break anything?" | Staged rollout with instrumentation and a rollback trigger ([observability](../../devops/observability/README.md), [deployment](../../devops/deployment/README.md)). |
| "Which of these two is better?" and traffic is thin | Pick one on judgement, record why, move on. The cost of being wrong is usually lower than the cost of waiting. |
| High-frequency in-session metric rather than conversion | May be powered even when conversion is not — recalculate with that metric's baseline and variance. |

The most common correct answer for a small product is the fourth: **decide, record the
reasoning, ship, watch**. That is not a failure to be rigorous; running an underpowered
test would be.

## Choosing the decision criterion

1. **What outcome does the business actually need?** Not what is easy to measure.
2. **Could the metric be moved by making the product worse?** If yes, it is the wrong
   criterion (P5). Engagement measures fail this most often.
3. **Is it sensitive enough to move within the test window?** Retention measured over 90
   days cannot decide a two-week test.
4. **What must not get worse while it moves?** Those are the guardrails (P6). Latency,
   errors, and at least one measure of user harm.

Write all of it down before launch. A criterion chosen after seeing the data is whichever
one moved.

## How long to run

- **Minimum:** the sample size from the arithmetic above.
- **And:** whole weeks, covering at least one full weekly cycle.
- **And:** long enough for novelty to decay if the change is visible to regular users (P15).
- **Cap:** if that exceeds about four weeks, do not run it. Longer tests accumulate
  contamination — releases, seasonality, cookie churn — faster than they accumulate power.

Fix the number before launch and do not move it (EXP18).

## Reading a result

```
1. Diagnostics first, outcomes second.
   Split ratio matches intended? Exposure logged at perception?
   Filtering identical across arms?
      any failure → the result is void. Fix and rerun. Do not peek at outcomes first.

2. Effect size and interval — not "significant / not significant".

3. Interval vs the smallest effect worth shipping for.
      significant but below threshold → negative result
      interval spans the threshold → underpowered, say so

4. Guardrails.
      target up, guardrail down → not a winner without an explicit tradeoff

5. Was this comparison pre-registered?
      no → exploratory. It is the next test, not this conclusion.
```

## Profile modulation

- **Prototype / Startup MVP** — you almost certainly cannot experiment. Use the pack for
  its refusal and its alternatives, plus the two ethics rules. Do not build an
  experimentation platform.
- **Production** — experiment where powered; the full checklist applies to those tests.
- **Enterprise** — plus an A/A validation of the pipeline before trusting it (EXP17), and a
  recorded history of results including the failures (EXP37).

## When NOT to use this pack

- **You don't have the traffic.** The most common case, and the pack says so first.
- **The question is what to build.** [inspired](../inspired/README.md).
- **The question is why users behave that way.** An experiment cannot answer it (P16) —
  [continuous-discovery-habits](../continuous-discovery-habits/README.md).
- **The change is a bug fix, a safety requirement, or an accessibility fix.** Do not test
  whether to meet the floor; EXP42 forbids withholding it from an arm.
- **The change is cheap, reversible, and low-risk.** Ship it. Not everything needs evidence
  proportional to its cost (EXP41).
- **You are evaluating model or agent output.** Non-deterministic quality is
  [agent-evals](../../ai-engineering/agent-evals/README.md), a different discipline with a
  different failure mode.
