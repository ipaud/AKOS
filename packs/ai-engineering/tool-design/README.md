# Pack: Tool Design — What the Agent Reaches For

**Domain:** AI Engineering · **Authority:** Level 2 (industry authority — Anthropic engineering practice, MCP specification, agent-computer-interface research) · **Version:** 1.0.0

Operationalizes the design of a tool an agent calls. The governing idea: a tool built for a human is not automatically a good tool for an agent. A person calling an API brings a docs tab, a memory of last week, a colleague to ask, and a willingness to read the stack trace; an agent brings a name, a description, a schema, and whatever came back last time. Naming, description, input shape, response shape, and blast-radius limits are therefore not packaging around the real capability — they are the capability, as far as the agent is concerned. A good agent tool reduces ambiguity to the point where the right call is obvious without a trial, and returns enough evidence for the agent to verify the result itself rather than take "OK" on faith.

Independent distillation for personal engineering use. Not affiliated with or endorsed by the source authors. See [references.md](references.md) for the originals — read them; this pack is a lossy operational index, not a substitute.

## When to load this pack

- Designing or reviewing a tool, function, or MCP server an agent will call.
- Wrapping an existing human-facing API or CLI for agent use, and deciding how much of it to expose and in what shape.
- An agent is calling the wrong tool, filling a parameter with the wrong kind of value, or making several exploratory calls where one should have sufficed.
- Deciding whether one capability should be one tool or several, or whether a growing tool surface has started degrading selection accuracy.
- Designing a tool's response shape, error shape, or pagination — especially where results can be large or unbounded.
- Adding a destructive or consequential operation to a surface an agent can reach, and deciding what preview and confirmation it needs.
- Building an MCP server and choosing between the tool, resource, and prompt primitives for a given capability.
- Writing or revising a tool description after watching how an agent actually calls it.

## Scope boundary

This pack is about **how an agent-facing tool is shaped** — its name, description, inputs, outputs, errors, limits, and the primitive it is exposed as. It is not about the security controls guarding that tool: injection carried in tool output, poisoned tool descriptions, excessive permissions, consent, and audit belong to the sibling [agent-security](../agent-security/README.md) pack, and MCP's trust-boundary and authorization concerns go there rather than here. Which architecture calls the tool — whether the system should be an agent at all, how its loop terminates, when it retries — is [agent-foundations](../agent-foundations/README.md); this pack's TD8 (repeat-safety declared at the tool boundary) is the tool-side counterpart to that pack's AF16 (the caller's obligation to take only repeat-safe actions). What the agent can *see*, including what an unbounded tool response costs once it lands in the window, is [context-engineering](../context-engineering/README.md). Load those alongside this one rather than expecting it to duplicate them.

## What's inside

| File | Highlights |
|------|-----------|
| [philosophy.md](philosophy.md) | The tool as the agent's whole world; ambiguity as the real cost center; why "OK" is a lie of omission |
| [mental-models.md](mental-models.md) | The blind selection, the ambiguity tax, the evidence gap, the blast radius, the three primitives, the composition ladder, the description as a live artifact, the surface as a set |
| [principles.md](principles.md) | TD1–TD16: always-true rules of agent-facing tool shape, each with an operational corollary |
| [heuristics.md](heuristics.md) | Fast defaults per concern — naming, granularity, inputs, outputs, errors, limits, iteration |
| [engineering-rules.md](engineering-rules.md) | TDE1–TDE86: checkable in a tool definition, a schema, a payload, or a call trace |
| [decision-framework.md](decision-framework.md) | One tool or several, which primitive, what a response returns, what needs a preview, how to bound a result set |
| [anti-patterns.md](anti-patterns.md) | The tool that does too much, the acknowledgement response, the stringly-typed parameter, the unbounded return, the positional reference |
| [review-checklist.md](review-checklist.md) | Binary pass/fail tool-surface review, severity-ordered |
| [examples.md](examples.md) | Invented before → after cases, plus an honest self-check of this repo's own `bin/akos` subcommands and `rules/runner.py` against this pack's checklist |
| [prompt-fragments.md](prompt-fragments.md) | Injectable blocks for build and review agents, plus a tool-definition worksheet |
| [scoring-rubric.md](scoring-rubric.md) | Tool-design scoring, 0–100 |
| [glossary.md](glossary.md) | Terms this pack uses precisely |

## Core claim, one line

A tool built for a human is not automatically a good tool for an agent — naming, description, response shape, and blast-radius limits determine whether an agent uses it correctly, and a good agent tool reduces ambiguity and returns verifiable evidence rather than acknowledgement.

## Related packs

[agent-foundations](../agent-foundations/README.md) · [context-engineering](../context-engineering/README.md) · [agent-security](../agent-security/README.md) · [rest](../../backend/rest/README.md) · [design-patterns](../../architecture/design-patterns/README.md)
