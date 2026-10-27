# References — Agent Security Pack

Attribution only. Nothing in this pack is copied from the sources below; the pack is an original operational distillation, reorganized into the AKOS 17-file contract. Distinguish published OWASP standards/guidance and protocol specifications from NIST frameworks, research reports, and initiatives: only normative requirements in a source are mandatory. Informational reports and initiative announcements are evidence or signals for monitoring, not standards.

Per [core/source-policy.md](../../../core/source-policy.md), standards documents get the same distillation treatment as any other source, with one addition: **item names and numbers are identifiers and are always cited**, so the normative text is one click away. The 2026 LLM Top 10 edition is used by its current identifiers below; verify against OWASP before reuse because lists may change.

## Official primary sources and their status

- **OWASP Top 10 for LLM Applications 2026** — OWASP GenAI Security Project, OWASP. https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/
  Published community risk guidance, not a regulation. Current entries include LLM01:2026 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM03 Excessive Agency, LLM04 Supply Chain, LLM05 Data and Model Poisoning, LLM06 Unbounded Consumption, LLM07 Misinformation, LLM08 Hidden Context Exposure, LLM09 Vector and Embedding Weaknesses, and LLM10 Improper Output Handling. This edition makes the agent boundary explicit: pair it with the Agentic Top 10 when the model acts. It adds practical emphasis here on multimodal and cross-session injection, bounded consumption, and checking whether fluent but false output drives decisions or tools. Existing agent-specific controls remain grounded in the Agentic Top 10 below.
- **Agent Control Standard (ACS)** — OWASP GenAI Security Project, OWASP. https://genai.owasp.org/resource/agent-control-standard-acs/
  Published open runtime-control standard describing middleware hooks through which agent platforms expose behavior and enforce safety policies. This pack distills its practical direction into external policy hooks, structured decision inputs, fail-closed behavior, trace linkage, and change-controlled policy configuration (ASE96–ASE99). These are AKOS engineering rules informed by ACS; use the source for its actual normative language and implementation details.
- **OWASP Top 10 for Agentic Applications** — OWASP GenAI Security Project, OWASP. https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
  The agent-specific list covering the risks that only appear once a model plans and acts: tool and resource poisoning, memory poisoning, privilege escalation and identity confusion, human-approval bypass, and agent supply-chain compromise. Item identifiers for this list are deliberately not reproduced here; consult the source for current numbering.
- **AI Risk Management Framework** — NIST. https://www.nist.gov/itl/ai-risk-management-framework
  The lifecycle frame this pack's controls live inside — govern, map, measure, and manage as a cycle rather than a one-time review. The profile-adjusted rigor table in `decision-framework.md` is the AKOS-shaped expression of "measure and manage continuously," and AS17's audit requirements are what make measurement possible at all.
- **Summary Analysis of Responses to the Request for Information Regarding Security Considerations for AI Agents** — Jared Riggs, Maia Hamin, Neil Perry, Benjamin Edelman, and Peter Cihon, NIST, May 18, 2026. https://www.nist.gov/publications/summary-analysis-responses-request-information-regarding-security-considerations-ai
  Informational synthesis of RFI comments, not a finalized standard or NIST control baseline. Respondents highlighted novel agent risks and the need to adapt fundamental cybersecurity practices, plus possible roles for implementation guidance, information sharing, and standards. It supports the pack's emphasis on applying existing controls at agent action boundaries while monitoring forthcoming work.
- **AI Agent Standards Initiative** — Center for AI Standards and Innovation, NIST, announced February 17, 2026. https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure
  An initiative announcement describing work on industry-led standards, open protocols, and research in agent security and identity; NIST said further research, guidelines, and deliverables would follow. This is an emerging work program, not itself a standard or a control requirement.
- **Model Context Protocol Specification, 2026-07-28** — Model Context Protocol maintainers. https://modelcontextprotocol.io/specification/2026-07-28
  Current protocol source as of this pack's review date. This pack's MCP-specific controls (ASE72–ASE78) cover server/tool provenance, host-enforced consent and data exposure, and trust in tool descriptions; they do not attempt to restate protocol transport or authorization requirements exhaustively. Check this dated revision and its security sections when implementing MCP. Older deployments may negotiate or pin an earlier revision; apply the protocol version they actually support and plan upgrades against its compatibility rules.

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
