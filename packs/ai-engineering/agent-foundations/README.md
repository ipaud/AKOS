# Pack: Agent Foundations — Which Shape, and How Bounded

**Domain:** AI Engineering · **Authority:** Level 2 (industry authority — Anthropic and OpenAI engineering practice) · **Version:** 1.0.0

Operationalizes the choice of architecture for a system built on a language model, and the discipline of keeping the chosen one under control. The governing idea: don't reach for an agent when a deterministic function, a fixed workflow, or a direct query solves the problem. Between one model call and a full agent lies a spectrum of shapes — chains, routers, fan-outs, workflows, orchestrators, critique loops — and each step along it transfers a decision from the engineer to the model, buying adaptability with predictability, testability, and a cost ceiling. Most of the work is knowing which shape fits the task. The rest is making a warranted agent terminate on a stated condition, stay inside budgets that fail loudly, recover by the right response to the right class of failure, and take only actions that are safe to take twice.

Independent distillation for personal engineering use. Not affiliated with or endorsed by the source authors. See [references.md](references.md) for the originals — read them; this pack is a lossy operational index, not a substitute.

## When to load this pack

- Deciding whether a task needs an agent at all, or whether a function, a fixed workflow, or a single query already answers it.
- Designing or reviewing a system built on a language model, before the shape is committed to code.
- A system already built as an agent behaves unpredictably, costs more than expected, or runs longer than expected — and the cause might be the shape rather than the prompt.
- Adding a second agent, a coordinator, or a handoff to a working single-agent system.
- Writing termination conditions, iteration limits, or token and wall-clock budgets for anything that loops.
- Designing error recovery: deciding when to retry, when to replan, and when to stop and ask a human.
- Specifying an agent's authority — what it may do alone, what needs confirmation, what it may never do.
- Auditing side-effecting tools an agent can call, for whether they are safe to call twice.
- Reviewing whether a fan-out actually buys latency or confidence, or is duplicating work at N times the cost.

## Scope boundary

This pack is about **which architecture to build, and how to bound it**. What the agent gets to *see* — the assembly of its context window, what loads when and for how long, progressive disclosure, memory tiers, retrieval timing — is [context-engineering](../context-engineering/README.md), and the two are genuinely separate problems: a perfectly-shaped agent fed the wrong context fails, and so does a perfectly-contexted agent with no termination condition. Load both when designing an agent from scratch. This pack is also not about the discipline of an agent editing a repository — how to scope a change, when to run the tests, what a safe diff looks like — which is a distinct subject deserving a sibling pack of its own rather than a section here. And it does not restate [core/authority-model.md](../../../core/authority-model.md) or [core/decision-framework.md](../../../core/decision-framework.md); it specializes them for one class of system.

## What's inside

| File | Highlights |
|------|-----------|
| [philosophy.md](philosophy.md) | Why the interesting shape is rarely the right one; autonomy as control given away; failures as the design surface, not the exception path |
| [mental-models.md](mental-models.md) | The shape spectrum, the path-knowability test, the decision-point budget, sectioning vs. voting, the three error responses, the escalation contract, the at-least-once world, the evaluator's ceiling, the exhaustion outcome |
| [principles.md](principles.md) | AF1–AF18: always-true rules of agent architecture, each with an operational corollary |
| [heuristics.md](heuristics.md) | Fast defaults per concern — shape choice, routing, parallelization, loops, budgets, recovery, escalation, idempotency |
| [engineering-rules.md](engineering-rules.md) | AFE1–AFE72: checkable in an agent's code, its spec, or a run trace |
| [decision-framework.md](decision-framework.md) | Which shape the task wants, is the agent warranted, sectioning vs. voting vs. neither, workflow vs. orchestrator, retry vs. replan vs. escalate, what a run returns |
| [anti-patterns.md](anti-patterns.md) | The silent truncation, the double-charged retry, the agent that should have been a function, the deterministic retry spiral, the self-approving loop, the multi-agent org chart |
| [review-checklist.md](review-checklist.md) | Binary pass/fail architecture review, severity-ordered |
| [examples.md](examples.md) | Invented before → after cases, including a written authority boundary and an orchestration that is genuinely earned |
| [prompt-fragments.md](prompt-fragments.md) | Injectable blocks for build and review agents, plus a shape-selection worksheet |
| [scoring-rubric.md](scoring-rubric.md) | Agent-architecture scoring, 0–100 |
| [glossary.md](glossary.md) | Terms this pack uses precisely |

## Core claim, one line

Don't reach for an agent when a deterministic function, a fixed workflow, or a direct query solves the problem — and when one is genuinely warranted, its termination condition, its budgets, its error classification, its escalation conditions, and its safety under repetition are all decided before the loop starts, never inferred after.

## Related packs

[context-engineering](../context-engineering/README.md) · [design-patterns](../../architecture/design-patterns/README.md) · [sre](../../devops/sre/README.md) · [testing-pyramid](../../testing/testing-pyramid/README.md)
