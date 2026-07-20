# Pack: Agent Security — Untrusted Text, Bounded Actions

**Domain:** AI Engineering · **Authority:** Level 1 (official standards — OWASP GenAI Security Project, NIST, and the Model Context Protocol specification) · **Version:** 1.0.0

Operationalizes the security of a system where a language model plans, calls tools, and acts. The governing idea: retrieved text, documents, web content, and tool output are untrusted data, never instructions — a boundary application security has enforced for thirty years at every other layer, and which language models collapse by construction, because instructions and data are the same substrate read by the same mechanism. From that collapse follow prompt injection in both forms, tool and resource poisoning, exfiltration through channels nobody classified as egress, memory that stays poisoned across sessions, and a confused deputy acting with permissions its requester never held. The remedy is not a better prompt. It is bounding what the agent CAN do — scoped credentials, sandboxes, egress allowlists, approval gates on irreversible actions, and an audit record — so that a model persuaded by a hostile document achieves nothing outside those bounds.

Independent distillation for personal engineering use. Not affiliated with or endorsed by OWASP, NIST, or the Model Context Protocol maintainers. Item names and numbers are cited as identifiers so the normative text is one click away; where the current numbering of an OWASP category was not certain at authoring time, the category is named without a number rather than guessed at. See [references.md](references.md) for the originals — read them; this pack is a lossy operational index, not a substitute, and the sources are authoritative over its restatements.

## When to load this pack

- Designing, building, or reviewing anything where a model reads external content and then calls a tool, uses a credential, or takes an action.
- Deciding what an agent is permitted to do: which tools load by default, how narrowly credentials are scoped, what needs human confirmation.
- Adding an MCP server, tool package, plugin, or skill to an agent's configuration — or accepting an update to one already installed.
- Building retrieval, browsing, inbox, ticket, or document-processing features, where content authored by one principal is read by an agent acting for another.
- Designing persistent memory: what an agent may write, from which sources, into which tier, and for how long.
- Deciding how agent output is consumed — rendered in a browser, executed in a shell, interpolated into a query, used as a path, or fed to another agent.
- Designing an approval flow for consequential actions, or reviewing one that already exists.
- Writing injection tests, running a red-team pass, or investigating an incident where an agent did something nobody asked it to.
- Any Production or Enterprise review of a surface with an agent component — and any Prototype one too, because the floor here does not move.

## Scope boundary

This pack covers only the **new attack surface introduced when an LLM agent plans, calls tools, and acts autonomously**. General web and API security is not restated: injection into your own database, broken access control on your own endpoints, TLS, session handling, and dependency CVEs belong to [owasp-top-10](../../security/owasp-top-10/README.md) and [owasp-api-top-10](../../security/owasp-api-top-10/README.md), and both must be loaded alongside this one whenever the surface under review has an agent component — the agent adds a surface without removing the original. Several rules here extend a specific OW rule and name it. The *shape* of an agent-facing tool — its parameters, return type, error behavior, and description as an affordance — is [tool-design](../tool-design/README.md); this pack covers the controls guarding that tool once it exists. The agent's architecture, its termination conditions, and its authority boundary as an engineering artifact are [agent-foundations](../agent-foundations/README.md), whose escalation contract is where this pack's approval gates get specified. And the assembly of the context window as a quality discipline is [context-engineering](../context-engineering/README.md) — its instruction hierarchy is this pack's provenance ladder, viewed there as a correctness concern and here as a security control with an enforcing component behind it.

This pack is Level 1, which places it on the safety floor [core/constitution.md](../../../core/constitution.md) Article 2 never waives. The reasoning profile scales the ceremony — the written threat model, the review cadence, the sign-off — never whether the sandbox, the egress allowlist, the approval gate, and the audit log exist. Prototype credentials are real credentials.

## What's inside

| File | Highlights |
|------|-----------|
| [philosophy.md](philosophy.md) | Why the code/data boundary collapsed and has to be rebuilt from outside; the attack nobody sent; why capability is the security boundary and intent isn't |
| [mental-models.md](mental-models.md) | The provenance ladder, the exfiltration triangle, the actuator boundary, mitigation vs. control, the confused deputy, the blast-radius envelope, the sleeper fact, the rubber stamp, the tool description as a second system prompt, the reconstruction test |
| [principles.md](principles.md) | AS1–AS18: always-true rules of agent security, each with an operational corollary |
| [heuristics.md](heuristics.md) | Fast defaults per concern — trust, blast radius, egress, permissions, memory, approval, supply chain, secrets, output, testing |
| [engineering-rules.md](engineering-rules.md) | ASE1–ASE95: checkable in a tool manifest, a permission grant, a sandbox config, or a run trace; ★ items hold in every profile |
| [decision-framework.md](decision-framework.md) | What trust class is this content, control or mitigation, what gate does this action need, should the agent hold this capability, whose permissions authorize it, which memory tier, remediation order, profile-adjusted rigor |
| [anti-patterns.md](anti-patterns.md) | The obedient document, the helpful markdown image, the god-mode token, the agent that is everyone, the tool that changed its mind, the rubber stamp, the sleeper fact, the trusted echo, the sandbox with a network card, the test suite that only types |
| [review-checklist.md](review-checklist.md) | Binary pass/fail security review, severity-ordered, with the safety-floor items marked |
| [examples.md](examples.md) | Invented before → after cases, including a blast radius scoped down and an injection suite that proves a bound rather than a refusal |
| [prompt-fragments.md](prompt-fragments.md) | Injectable blocks for build and review agents, plus a threat-model worksheet, an egress enumeration audit, and an indirect-injection test generator |
| [scoring-rubric.md](scoring-rubric.md) | Agent-security scoring, 0–100, feeding `scoring/security-score.md` |
| [glossary.md](glossary.md) | Terms this pack uses precisely |

## Core claim, one line

Retrieved text, documents, web content, and tool output are untrusted data and never instructions — and because no prompt can enforce that boundary from inside the model, security comes from bounding what the agent CAN do with scoped credentials, sandboxes, egress allowlists, approval gates, and an audit trail, so that a persuaded agent is a contained one.

## Related packs

[owasp-top-10](../../security/owasp-top-10/README.md) · [owasp-api-top-10](../../security/owasp-api-top-10/README.md) · [nist-ssdf](../../security/nist-ssdf/README.md) · [tool-design](../tool-design/README.md) · [context-engineering](../context-engineering/README.md) · [agent-foundations](../agent-foundations/README.md)
