# References — Coding Agents Pack

Attribution only. Nothing in this pack is copied from the source below; the pack is an original operational distillation, reorganized into the AKOS 17-file contract. Read the original — it carries the measurements and the experimental detail this pack compresses away.

## Primary source (Level 2)

- **SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering** — Yang et al., arXiv. https://arxiv.org/abs/2405.15793

Cited for one idea this pack builds on operationally: the interface through which an agent acts on a repository shapes its error rate, and cheap feedback placed at the moment of the edit — a syntax or lint check gating an edit before it is accepted — prevents a class of defect that is expensive to catch later. This pack's insistence on build, lint, and type verification as part of the change (CA13) rather than as a later CI concern is that idea restated as process discipline.

## In-repo case study (this repository's own practice, not an external source)

The depth of this pack comes primarily from a real, inspectable engineering record rather than from published literature. AKOS's v1.4.0 quality-infrastructure initiative shipped schemas, a validation CLI, an executable rules engine, a benchmark harness, CI, and tests across thirteen commits, and found a series of real bugs in the process — each caught only because a command was executed and its actual exit code read.

- [CHANGELOG.md](../../../CHANGELOG.md) — the `[1.4.0]` entry, which enumerates the bugs found and fixed.
- Commit `748db87` — the piped-`tail` exit-code trap, hit during the first end-to-end test of `akos validate`'s exit convention.
- Commit `32905fa` — five detector bugs found by running each detector against a constructed fixture before building on it.
- Commit `b9e0b93` — the benchmark harness's fixture-path resolution bug, whose failure pattern (every true positive failing, every true negative vacuously passing) is the clearest instance of a check that could not fail.
- Commit `b765cd7` — the inverted `--fail-on` severity comparison, caught by a run that exited 2 where it should have exited 0.
- Commit `4925d34` — the unit and integration suites, including a test that was itself the wrong party and was fixed rather than having its assertion relaxed.

See [examples.md](examples.md) for the worked case study. The practice visible across these commits — leaving the project verifiable after each step — is recorded here as **this repository's own observed working discipline**, not attributed to any external paper. The broader question it opens, how an agent maintains that property across a long-running multi-session effort, is deliberately deferred to a future `long-running-agents` pack.

## Related AKOS core documents

This pack composes with, rather than restates, the following:

- [core/authority-model.md](../../../core/authority-model.md) — the level assignment behind this pack's source, and the general precedence rule.
- [core/confidence-model.md](../../../core/confidence-model.md) — the confidence classes behind CA15's rule that a claim's strength is capped by what was actually executed.
- [core/source-policy.md](../../../core/source-policy.md) — the distillation rules this pack itself follows.
- [core/scoring-model.md](../../../core/scoring-model.md) — the bands behind [scoring-rubric.md](scoring-rubric.md).

## Related AKOS packs

- [agent-foundations](../agent-foundations/README.md) — what shape the surrounding system should be and how it is bounded: termination, budgets, error classification, escalation, idempotency. That pack explicitly defers repository-editing discipline to this one.
- [context-engineering](../context-engineering/README.md) — what the agent gets to see while it works: retrieval timing, progressive disclosure, memory tiers, and the search-and-navigate discipline for large repositories that this pack's "search before edit" rules depend on.
- [tdd](../../testing/tdd/README.md) — the red-green-refactor cycle whose first half this pack's CA11 (reproduce before fixing) and CA3 (prove the check can fail) are the agent-shaped case of.
- [git](../../devops/git/README.md) — commit granularity, history hygiene, and branching. This pack's revert test and atomic-commit rules are that discipline stated as a checkable property of an agent's output.
- [martin-fowler-refactoring](../../architecture/martin-fowler-refactoring/README.md) — behavior-preserving change as its own discipline, and the reason this pack insists a refactor is landed separately from the fix that motivated it rather than interleaved with it.
