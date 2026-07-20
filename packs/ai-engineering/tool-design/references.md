# References — Tool Design Pack

Attribution only. Nothing in this pack is copied from the sources below; the pack is an original operational distillation, reorganized into the AKOS 17-file contract. Read the originals — they carry the reasoning, the measurements, and the worked cases this pack compresses away.

## Primary sources (Level 2 — published engineering practice and specification)

- **Writing Effective Tools for AI Agents** — Anthropic. https://www.anthropic.com/engineering/writing-tools-for-agents
- **Model Context Protocol Specification** — Anthropic / Model Context Protocol. https://modelcontextprotocol.io/specification/2025-11-25

## Research (applied as a decision framework, not a commandment)

- **SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering** — Yang et al., arXiv. https://arxiv.org/abs/2405.15793

Cited for the interface-shape argument this pack restates operationally: that what an agent can accomplish is bounded as much by the shape of the interface it is given as by the model behind it.

## Related AKOS core documents

This pack composes with, rather than restates, the following:

- [core/authority-model.md](../../../core/authority-model.md) — the level assignments behind this pack's sources, and the general precedence rule.
- [core/decision-framework.md](../../../core/decision-framework.md) — the general decision pattern that this pack's granularity, primitive-selection, and bounding tables specialize.
- [core/source-policy.md](../../../core/source-policy.md) — the distillation rules this pack itself follows.
- [core/scoring-model.md](../../../core/scoring-model.md) — the bands behind `scoring-rubric.md`.

## In-repo artifacts audited by this pack

- [bin/akos](../../../bin/akos) — the AKOS CLI, whose subcommands function as agent-callable tools. Audited against this pack's checklist in [examples.md](examples.md).
- [rules/runner.py](../../../rules/runner.py) — the executable-rule runner, whose `Finding` shape is examined as a well-formed structured tool result in the same audit.

## Related AKOS packs

- [agent-foundations](../agent-foundations/README.md) — which architecture calls the tool, how its loop terminates, and when it retries. This pack's TD8 (repeat-safety declared at the tool boundary) is the tool-side counterpart to that pack's AF16 (the caller's obligation to take only repeat-safe actions).
- [context-engineering](../context-engineering/README.md) — what the agent can see. The two packs meet directly at the unbounded result set, where a tool-design defect (TD10) becomes a context-engineering failure (CE1, CE6) one call later.
- [agent-security](../agent-security/README.md) — the security controls guarding a tool: injection carried in tool output, poisoned tool descriptions, excessive permissions, consent and audit, and MCP's trust-boundary and authorization concerns. Deliberately out of scope here.
- [rest](../../backend/rest/README.md) — resource modelling, status semantics, pagination, and idempotency as API practice. Many of this pack's rules are the agent-facing case of concerns REST design has treated as first-class for far longer, with the difference that the caller cannot read documentation.
- [design-patterns](../../architecture/design-patterns/README.md) — interface design, composition over monoliths, and naming as a first-class concern. The composition ladder is that discipline applied to a tool surface.
