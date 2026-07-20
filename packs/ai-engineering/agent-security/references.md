# References — Agent Security Pack

Attribution only. Nothing in this pack is copied from the sources below; the pack is an original operational distillation, reorganized into the AKOS 17-file contract. The sources are normative and authoritative over this pack's restatements — where they and this pack disagree, they win, and this pack is the thing that gets fixed.

Per [core/source-policy.md](../../../core/source-policy.md), standards documents get the same distillation treatment as any other source, with one addition: **item names and numbers are identifiers and are always cited**, so the normative text is one click away. Where the current numbering of an OWASP category was not certain at authoring time, the category is named without a number and marked "see the OWASP GenAI Security Project for current numbering" — accuracy over the appearance of precision. Verify against the live lists before quoting a number anywhere.

## Primary sources (Level 1 — standards bodies)

- **OWASP Top 10 for Large Language Model Applications** — OWASP GenAI Security Project, OWASP. https://genai.owasp.org/llm-top-10/
  The list this pack draws on for prompt injection (LLM01), sensitive information disclosure, supply chain, data and model poisoning, improper output handling, excessive agency, and system prompt leakage. Cited by name throughout `principles.md` and `engineering-rules.md`.
- **OWASP Top 10 for Agentic Applications** — OWASP GenAI Security Project, OWASP. https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
  The agent-specific list covering the risks that only appear once a model plans and acts: tool and resource poisoning, memory poisoning, privilege escalation and identity confusion, human-approval bypass, and agent supply-chain compromise. Item identifiers for this list are deliberately not reproduced here; consult the source for current numbering.
- **AI Risk Management Framework** — NIST. https://www.nist.gov/itl/ai-risk-management-framework
  The lifecycle frame this pack's controls live inside — govern, map, measure, and manage as a cycle rather than a one-time review. The profile-adjusted rigor table in `decision-framework.md` is the AKOS-shaped expression of "measure and manage continuously," and AS17's audit requirements are what make measurement possible at all.
- **Model Context Protocol Specification** — Anthropic, Model Context Protocol. https://modelcontextprotocol.io/specification/2025-11-25
  The protocol whose trust model this pack's supply-chain rules (ASE72–ASE78) operationalize. Its security expectations — explicit user consent before tool invocation, user control over what data is exposed, treating tool descriptions as untrusted unless the server is trusted, and human review of model-sampling requests — are restated here as host-enforced engineering rules rather than as guidance.

## Related AKOS core documents

This pack composes with, rather than restates, the following:

- [core/constitution.md](../../../core/constitution.md) — Article 2's safety floor, which is why this pack's controls are not waivable by reasoning profile (AS18).
- [core/authority-model.md](../../../core/authority-model.md) — the Level 1 assignment behind this pack: its defining sources are standards bodies (OWASP, NIST) plus the specification owner for MCP. Their normative requirements are non-negotiable; their recommendations are near-mandatory with recorded justification for exceptions.
- [core/source-policy.md](../../../core/source-policy.md) — the distillation rules this pack follows, including the standards-document clause that requires citing item identifiers.
- [core/scoring-model.md](../../../core/scoring-model.md) — the bands behind `scoring-rubric.md`.
- [scoring/security-score.md](../../../scoring/security-score.md) — the composite this pack's score feeds, alongside the OWASP application packs.

## Related AKOS packs

- [owasp-top-10](../../security/owasp-top-10/README.md) — the general web application floor. This pack does not restate it; load both whenever the surface under review has an agent component, because the agent adds a surface without removing the original one. Several rules here extend a specific OW rule and say which.
- [owasp-api-top-10](../../security/owasp-api-top-10/README.md) — the API surface an agent's tools usually sit on top of. Broken object-level authorization behind a tool is still broken object-level authorization.
- [nist-ssdf](../../security/nist-ssdf/README.md) — the secure development lifecycle these controls are practiced within: threat modeling, review gates, and dependency discipline as process rather than as one-off checks.
- [tool-design](../tool-design/README.md) — the *shape* of an agent-facing tool: its parameters, return type, error behavior, and description as an affordance. That pack designs the tool; this one guards it. The two meet at ASE18–ASE25, where a tool's description is treated as prompt content.
- [context-engineering](../context-engineering/README.md) — what enters the context window, in what order, for how long. Its instruction hierarchy is this pack's provenance ladder viewed as a quality discipline; here the same labeling is a security control with an enforcing component behind it.
- [agent-foundations](../agent-foundations/README.md) — the agent's architecture, termination conditions, and written authority boundary. Its escalation contract is where this pack's approval gates get specified, and its idempotency rules guard the same actuator boundary against a different failure.
