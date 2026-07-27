# References — Observability Pack

Attribution only. Nothing here is copied from these sources; the pack is an original
operational distillation, organized by the AKOS file contract rather than by any source's
structure.

## Primary sources

- **OpenTelemetry Specification** — OpenTelemetry Authors (CNCF). https://opentelemetry.io/docs/specs/otel/
- **OpenTelemetry Semantic Conventions** — OpenTelemetry Authors (CNCF). https://opentelemetry.io/docs/specs/semconv/
- **Trace Context** — W3C. https://www.w3.org/TR/trace-context/
- **Observability Engineering: Achieving Production Excellence** — Charity Majors, Liz Fong-Jones, George Miranda. https://www.oreilly.com/library/view/observability-engineering/9781492076438/

## Why this pack is Level 2, not Level 1

The roadmap entry that queued it proposed Level 1 on the strength of the OpenTelemetry
specification. That was reconsidered while writing:

- OpenTelemetry is a CNCF project defining its own protocol and conventions. It is
  authoritative *about itself*, and broadly adopted — but it is not a normative standard
  from a standards body in the sense `wcag`, `owasp-asvs`, or the IETF RFCs behind
  [security/auth](../../security/auth/README.md) are.
- The reasoning half of this pack — unknown-unknowns, wide events, high cardinality as a
  feature, the narrowing debug loop — comes from a book, which is Level 3 territory.
- Claiming Level 1 would give book-derived judgment the deference owed to normative
  requirements. Level 2 is the honest level for the blend, and it matches the sibling
  [devops/sre](../sre/README.md), which distills the Google SRE book at the same level.

W3C Trace Context genuinely is Level 1, and where this pack restates it (context
propagation headers) that source is the authority.

## Related AKOS packs

[devops/sre](../sre/README.md) · [devops/deployment](../deployment/README.md) ·
[devops/ci-cd](../ci-cd/README.md) · [security/privacy](../../security/privacy/README.md) ·
[performance/core-web-vitals](../../performance/core-web-vitals/README.md) ·
[ai-engineering/agent-evals](../../ai-engineering/agent-evals/README.md)
