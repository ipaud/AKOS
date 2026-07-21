# Benchmarks — overview

`benchmarks/README.md` covers the mechanics (structure, running, adding a case). This is the *why* and the methodology.

## The problem this solves

A knowledge pack can say "enable RLS on every table" as an engineering rule. Nothing before this initiative could answer: does an agent following that rule actually *catch* a table missing RLS? The rules registry (`rules/`) is the executable half of that engineering rule; benchmarks are how you know the executable half still works after the next change.

## Methodology

Each case is a synthetic mini-project (`fixture/`) small enough to read in one screen, plus an `expected.yaml` stating exactly which findings must and must not appear. The harness runs the real rules engine against the fixture and diffs.

**Every rule has at least one true-positive case and one true-negative case** — the realistic near-miss that shouldn't fire (a suppressed policy, an anon-role JWT, a guarded destructive statement, a project that never adopted a migration convention). A rule with only positive cases can regress into false-positive noise without any test catching it; the negative cases are what actually caught real bugs during this initiative's own construction (see below).

## What the numbers mean, and don't

`akos benchmark run` reports recall and precision. Read the printed caveat literally: this is computed **only** over the curated `must_detect`/`must_not_detect` corpus in `benchmarks/cases/`, 28 cases as of this writing. It is a **regression guard** — did a change break a case that used to pass — not a statistically valid claim about detection rates on arbitrary real-world code. A 100% recall/precision score here means "every case we thought to write still passes," not "this rule never misses anything real." The corpus gets more representative only as it grows, and growth is a real, ongoing task — see "No silent caps" below.

## No silent caps

If a rule or domain isn't covered by any case, that's a real gap, not a hidden one. `PACK_EXPIRED` is the one rule in `rules/` with no benchmark case (see `benchmarks/README.md` for why — it needs the harness to monkeypatch `AKOS_HOME`, not worth the complexity for one rule already covered by a unit test). Every other rule has at least 2 cases. When a ninth rule is added, it needs benchmark coverage before it's trusted, not after.

## Level A/B vs. Level C

The 28 cases split 26 deterministic (Level A/B, the rules engine) and 2 Level-C (mock-provider, keyword-matched). The deterministic cases are the ones the recall/precision arithmetic covers — Level C cases are graded pass/fail individually and explicitly not pooled into that arithmetic, since "does the response mention this phrase" is a much weaker signal than "did the detector find this exact line."

## Real bugs this benchmark suite already caught

Two, during its own construction — both stated in the M8 commit message, repeated here because it's the point of the exercise:

1. The harness resolved `expected.yaml`'s fixture paths relative to `benchmarks/` instead of the case's own directory. Every true-positive case failed while every true-negative case passed *vacuously* — a broken path match makes a "must not detect" check pass for the wrong reason. The asymmetric failure pattern was itself the diagnostic clue.
2. The mock provider's canned Level-C responses paraphrased their own trigger words ("loading indicator" instead of "loading state"), so `must_mention` — which checks the response text, not the prompt — failed even though the underlying trigger match was correct.

Neither bug was in a *rule detector* — both were in the harness testing the rules. That's worth sitting with: a benchmark suite needs its own verification pass before it's trusted to verify anything else, exactly like every detector needed a synthetic true-positive-and-near-miss test before being trusted (see `rules/README.md`'s "Adding a rule" checklist).
