# Pack: Agent Evals — Prove It Got Better

**Domain:** AI Engineering · **Authority:** Level 2 (industry authority — Anthropic engineering practice) · **Version:** 1.0.0

Operationalizes the measurement of an agent: whether a change made it better, and whether anyone would find out if it made it worse. The governing idea: do not accept an agent improvement backed by three manual examples — demand a representative suite and a comparison against a stated baseline. This is the discipline traditional testing already applies to deterministic code, applied to non-deterministic, judgment-laden output. Structurally almost everything transfers — fixed inputs, a runner, CI, red-before-green, coverage as a question worth asking — and exactly one thing does not: the assertion. A deterministic system lets you compare exact values; a judgment-laden one needs a grader that tolerates variation and still says something falsifiable. Everything hard about evals lives in that substitution, and everything else is a solved problem being re-solved badly.

Independent distillation for personal engineering use. Not affiliated with or endorsed by the source authors. See [references.md](references.md) for the original — read it; this pack is a lossy operational index, not a substitute.

## When to load this pack

- Someone proposes an agent change and the evidence is a handful of outputs that look better.
- Building a golden dataset, or deciding whether the set of examples you have qualifies as one.
- Choosing a grader — exact match, rubric, LLM-as-judge, pairwise — and deciding which is warranted for this output shape.
- An LLM judge is scoring something that gates a release, and nobody has checked it against human labels.
- Deciding what a regression threshold should be, or being asked to move a baseline after a failing run.
- The eval suite is red and the fastest path to green is a re-run.
- A dashboard of step-level metrics looks healthy and users report the agent doesn't finish tasks.
- Scores are rising and nobody can name the capability change behind the rise.
- Adding a tool, bumping a model version, or changing retrieval — and deciding what has to be measured before it merges.
- Reviewing whether an agent's cost, latency, or tool-call efficiency has been drifting unmeasured while correctness improved.

## Scope boundary

This pack evaluates an **agent's behavior and output quality across runs**. Traditional software unit, integration, and E2E testing of deterministic code is [packs/testing/testing-pyramid](../../testing/testing-pyramid/README.md) and [packs/testing/tdd](../../testing/tdd/README.md)'s job, and the relationship is stated rather than blurred: an eval suite is structurally a test suite whose assertions must tolerate variation and grade judgment rather than compare exact values (AE4). Reuse their apparatus; replace only the assertion layer. Human-executed release verification is [packs/testing/qa-checklists](../../testing/qa-checklists/README.md). Scoring an AKOS review — the twelve-lens rubric, its severity anchors, its bands — belongs to [core/scoring-model.md](../../../core/scoring-model.md); this pack is about measuring an agent system, not about that rubric, and its own `scoring-rubric.md` supplies deductions for a different surface while deferring to that file for the bands. Which architecture an agent should have is [agent-foundations](../agent-foundations/README.md); what enters its context window is [context-engineering](../context-engineering/README.md) — this pack is how a change to either is shown to have helped. And it does not answer whether the task is worth doing at all; a suite improving while the product fails is a coherent outcome, and that question is [packs/product/lean-startup](../../product/lean-startup/README.md)'s.

## What's inside

| File | Highlights |
|------|-----------|
| [philosophy.md](philosophy.md) | Only the assertion is new; measurement as a specification of "better"; trust in a suite as the real asset, destroyed cheaply |
| [mental-models.md](mental-models.md) | The four eval altitudes, the grader ladder, the completion cliff, the baseline as a contract, the contamination gradient, the flakiness tax, two populations not two numbers, the vacuous pass |
| [principles.md](principles.md) | AE1–AE18: always-true rules of measuring an agent, each with an operational corollary |
| [heuristics.md](heuristics.md) | Fast defaults per concern — starting a suite, datasets, grader choice, judge hygiene, thresholds, flakiness, contamination, reporting |
| [engineering-rules.md](engineering-rules.md) | AEE1–AEE76: checkable in cases, harness, threshold config, CI wiring, or a run report |
| [decision-framework.md](decision-framework.md) | Evidence vs. demonstration, which altitude, which grader, red-suite triage in order, when a baseline may move, contamination vs. noise, how much eval this change needs |
| [anti-patterns.md](anti-patterns.md) | The moving baseline, the vacuous pass, the contaminated benchmark, the self-approving judge, the three-example proof, the all-green dashboard over a failing task, the retry-to-green suite |
| [review-checklist.md](review-checklist.md) | Binary pass/fail eval-discipline review, severity-ordered |
| [examples.md](examples.md) | An honest worked assessment of this repo's own `benchmarks/` harness — what it gets right and what it does not do — plus invented before/after cases |
| [prompt-fragments.md](prompt-fragments.md) | Injectable blocks for build and review agents, plus a suite audit, a result interrogation, a red-suite triage, and a grader-selection worksheet |
| [scoring-rubric.md](scoring-rubric.md) | Evaluation-discipline scoring, 0–100 |
| [glossary.md](glossary.md) | Terms this pack uses precisely |

## Core claim, one line

Do not accept an agent improvement backed by three manual examples — demand a representative suite and a comparison against a stated baseline, and treat a suite that reports something false about the system it measures (a moved baseline, a case never seen failing, a self-grading judge, a contaminated run) as a correctness defect rather than a process concern.

## Related packs

[agent-foundations](../agent-foundations/README.md) · [context-engineering](../context-engineering/README.md) · [testing-pyramid](../../testing/testing-pyramid/README.md) · [qa-checklists](../../testing/qa-checklists/README.md) · [lean-startup](../../product/lean-startup/README.md)
