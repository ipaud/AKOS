# References — Agent Foundations Pack

Attribution only. Nothing in this pack is copied from the sources below; the pack is an original operational distillation, reorganized into the AKOS 17-file contract. Read the originals — they carry the reasoning, the measurements, and the worked cases this pack compresses away.

## Primary sources (Level 2 — published engineering practice)

- **Building Effective Agents** — Anthropic. https://www.anthropic.com/engineering/building-effective-agents
- **A Practical Guide to Building Agents** — OpenAI. https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf

## Methodology papers (Level 3 — applied as decision frameworks, not commandments)

Per [core/authority-model.md](../../../core/authority-model.md), a paper alone doesn't earn Level 3; corroborated adoption in practice does. Both below are cited for the shapes they named, which this pack restates operationally rather than reproducing.

- **ReAct: Synergizing Reasoning and Acting in Language Models** — Yao et al., arXiv. https://arxiv.org/abs/2210.03629
- **Reflexion: Language Agents with Verbal Reinforcement Learning** — Shinn et al., arXiv. https://arxiv.org/abs/2303.11366

## Related AKOS core documents

This pack composes with, rather than restates, the following:

- [core/authority-model.md](../../../core/authority-model.md) — the level assignments behind this pack's sources, and the general precedence rule.
- [core/decision-framework.md](../../../core/decision-framework.md) — the general decision pattern that this pack's shape-selection and error-classification tables specialize.
- [core/source-policy.md](../../../core/source-policy.md) — the distillation rules this pack itself follows.
- [core/scoring-model.md](../../../core/scoring-model.md) — the bands behind `scoring-rubric.md`.

## Related AKOS packs

- [context-engineering](../context-engineering/README.md) — what the agent gets to *see*: context assembly, progressive disclosure, just-in-time retrieval, memory tiers. The direct sibling to this pack's "what shape is it, and how is it bounded."
- [design-patterns](../../architecture/design-patterns/README.md) — the general discipline of naming a structure before building it, and of not reaching for the elaborate pattern when the simple one solves the problem. The shape spectrum is that discipline applied to agent topologies.
- [sre](../../devops/sre/README.md) — retries, backoff, budgets, timeouts, escalation, and idempotency as operational practice. This pack's error-recovery and limits rules are the agent-shaped case of concerns SRE has treated as first-class for far longer.
- [testing-pyramid](../../testing/testing-pyramid/README.md) — why testability is one of the real costs of moving up the agency spectrum: a fixed workflow's steps can each be tested, while a re-derived path can differ on the run nobody watched.
