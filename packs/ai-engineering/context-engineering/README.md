# Pack: Context Engineering — What Enters the Window

**Domain:** AI Engineering · **Authority:** Level 2 (industry authority — Anthropic engineering practice) · **Version:** 1.0.0

Operationalizes the discipline of deciding what an agent gets to see. The governing idea: context is a finite, expensive resource — every token in it competes with every other token for the model's limited attention, costs latency and money, and can be wrong in a way nothing downstream will catch on its own. The job is not to write a longer, more thorough prompt or to load everything that might conceivably matter; it is to decide, continuously, what earns a place in the window, in what order, and for how long. Agent quality tracks what an agent can see at least as much as it tracks how cleverly it was instructed.

Independent distillation for personal engineering use. Not affiliated with or endorsed by the source authors. See [references.md](references.md) for the originals — read them; this pack is a lossy operational index, not a substitute.

## When to load this pack

- Building or reviewing an agent's system prompt, skill file, subagent definition, or tool-selection logic.
- Deciding whether to load a document, pack, or memory file into a session now, or fetch it later instead.
- A session or agent is producing worse answers as the conversation grows, and the cause might be volume rather than task difficulty.
- Designing memory persistence (project notes, user preferences, learned instincts) and deciding which tier a given fact belongs in.
- Building a retrieval pipeline, a routing table, or any "which source loads for which task" mechanism.
- Reviewing whether an agent is treating retrieved or tool-returned content as an instruction it should obey.
- Working on or in a large repository and deciding between a full read, a targeted read, and a search.
- Designing a compaction or summarization step and deciding what must survive it.

## Scope boundary

This pack is about **what enters context, in what order, and for how long** — the assembly problem. Its siblings divide the rest: which architecture is warranted and how it is bounded is [agent-foundations](../agent-foundations/README.md); the shape of the tools it calls is [tool-design](../tool-design/README.md); how its behavior is measured is [agent-evals](../agent-evals/README.md); the controls guarding it are [agent-security](../agent-security/README.md). How an instruction is *phrased* once the decision to include it has been made — imperative vs. descriptive wording, few-shot example design, chain-of-thought scaffolding — is currently covered by no pack in this domain, and is deliberately out of scope here rather than silently absorbed. It is also not a restatement of [core/confidence-model.md](../../../core/confidence-model.md)'s confidence levels or [core/source-policy.md](../../../core/source-policy.md)'s distillation rules — this pack tells an agent what to load and when; those tell it how sure to be about a claim, and how to write about a source once it has decided to use one. Load this pack alongside them rather than expecting it to duplicate them.

## What's inside

| File | Highlights |
|------|-----------|
| [philosophy.md](philosophy.md) | Context as a budget, not a warehouse; why "it fits" isn't "it's usable"; the agent's blindness to its own poisoned facts |
| [mental-models.md](mental-models.md) | The attention economy, the context-rot curve, the poisoning chain, the instruction stack, the compaction boundary, the four memory tiers, the manifest vs. the dump |
| [principles.md](principles.md) | CE1–CE16: always-true rules of what belongs in a context window and why |
| [heuristics.md](heuristics.md) | Fast defaults per concern — loading, disclosure, retrieval timing, memory filing, routing |
| [engineering-rules.md](engineering-rules.md) | CEE1–CEE58: checkable in a prompt, a skill, a memory store, or a session transcript |
| [decision-framework.md](decision-framework.md) | When to load vs. defer, which memory tier, what survives compaction, how routing should work — including a worked critique of `skills/akos/SKILL.md`'s own routing table |
| [anti-patterns.md](anti-patterns.md) | The kitchen-sink prompt, context poisoning, the instruction that wasn't, the wrong-tier memory, the full-repo dump |
| [review-checklist.md](review-checklist.md) | Binary pass/fail context-assembly review, severity-ordered |
| [examples.md](examples.md) | Invented before → after cases, including the self-referential AKOS routing example |
| [prompt-fragments.md](prompt-fragments.md) | Injectable blocks for build and review agents |
| [scoring-rubric.md](scoring-rubric.md) | Context-engineering scoring, 0–100 |
| [glossary.md](glossary.md) | Terms this pack uses precisely |

## Core claim, one line

Context is a finite, expensive resource, and the entire discipline is deciding what earns a place in it, in what order, and for how long — not writing a longer prompt.

## Related packs

[agent-foundations](../agent-foundations/README.md) · [personal/pau-avila](../../personal/pau-avila/README.md) · [nielsen-norman-group](../../ux/nielsen-norman-group/README.md) · [clean-architecture](../../architecture/clean-architecture/README.md)
