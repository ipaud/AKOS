# References — Agent Evals Pack

Attribution only. Nothing in this pack is copied from the source below; the pack is an original operational distillation, reorganized into the AKOS 17-file contract. Read the original — it carries the reasoning and the worked cases this pack compresses away.

## Primary source (Level 2 — published engineering practice)

- **Demystifying Evals for AI Agents** — Anthropic. https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

This is the pack's only external source, deliberately. Where depth was needed beyond what one source supports, it came from the in-repo worked example below rather than from padding the citation list.

## In-repo worked example

- [`benchmarks/README.md`](../../../benchmarks/README.md), [`benchmarks/manifest.yaml`](../../../benchmarks/manifest.yaml), [`benchmarks/runners/run.py`](../../../benchmarks/runners/run.py), and [`docs/benchmarks/overview.md`](../../../docs/benchmarks/overview.md) — AKOS's own eval harness: 21 reproducible cases, recall and precision computed over a curated corpus, a deterministic offline mock provider for CI, positive and negative cases per rule, and every case verified by deliberate sabotage. Assessed honestly in [examples.md](examples.md), including what it does not do: it evaluates a deterministic rules engine, not an agent, and has no trajectory evals, no LLM-as-judge, and no pairwise comparison.

## Related AKOS core documents

This pack composes with, rather than restates, the following:

- [core/scoring-model.md](../../../core/scoring-model.md) — the 0–100 bands, severity anchors, and verdict linkage. This pack's `scoring-rubric.md` supplies deductions for a different surface (a suite's evaluation discipline) and defers to that file for the bands themselves. Scoring an AKOS review against the twelve-lens rubric is that file's job, not this pack's.
- [core/confidence-model.md](../../../core/confidence-model.md) — the confidence-versus-coverage distinction behind AE18. A narrow eval can be entirely trustworthy about what it measured; confidence is about the claim, coverage is about how much of the surface was looked at.
- [core/authority-model.md](../../../core/authority-model.md) — the Level 2 assignment for this pack's source.
- [core/source-policy.md](../../../core/source-policy.md) — the distillation rules this pack itself follows.

## Related AKOS packs

- [agent-foundations](../agent-foundations/README.md) — which architecture a task warrants and how it is bounded. This pack is the mechanism by which a change to that architecture is shown to have helped; its observability rules (a run trace with steps, tools, spend, and exit reason) are the precondition for trajectory and cost evals here.
- [context-engineering](../context-engineering/README.md) — what the agent gets to see. Its context changes are exactly the class of change that most needs a groundedness metric to evaluate, and its context-poisoning concern is this pack's contamination concern seen from the other side.
- [testing-pyramid](../../testing/testing-pyramid/README.md) — the apparatus this pack specializes. An eval suite is structurally a test suite whose assertions tolerate variation and grade judgment rather than compare exact values (AE4); everything except the assertion layer transfers, and testing deterministic code remains that pack's job.
- [qa-checklists](../../testing/qa-checklists/README.md) — human-executed release verification, the manual counterpart to an automated suite. Where an eval measures behavior across runs, a QA checklist confirms a build before it ships; they answer different questions and neither replaces the other.
- [lean-startup](../../product/lean-startup/README.md) — measurement discipline one level up: whether the thing being improved is worth improving. An eval answers "is this version better at this task," never "is this task worth doing," and a suite improving while the product fails is a coherent and well-documented outcome.
