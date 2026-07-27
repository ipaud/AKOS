# Pack: Observability — Instrumenting for Questions Nobody Asked Yet

**Domain:** DevOps · **Authority:** Level 2 (OpenTelemetry + published practice) · **Version:** 1.0.0

[devops/sre](../sre/README.md) owns the *targets* — SLOs, error budgets, alerting, on-call.
This pack owns the *signals* those targets are measured from, and the debugging that starts
once an alert fires: which signal answers which question, how trace context survives a
queue, where an attribute may go, what sampling keeps, and what telemetry must never carry.

Independent distillation for personal engineering use. Not affiliated with or endorsed by
the OpenTelemetry project, the CNCF, the W3C, or the source authors. See
[references.md](references.md) for the originals.

## Read this first

**You probably don't need this pack yet.** The trigger is *"we could not answer a question
about production"* — not headcount, not a diagram. A managed-platform app with a few
hundred users needs three things (OBS41–OBS43), and building a collector-and-tracing stack
around it is the exact over-engineering this pack warns about. The
[decision framework](decision-framework.md) opens with a table telling you which row you're
in.

## When to load this pack

- More than one service, or async/queued work, and "it's slow but only sometimes".
- A per-customer problem you cannot reproduce.
- Telemetry costs surprised someone.
- Reviewing whether a feature shipped debuggable.
- Anything about what telemetry carries — that part is a floor, at any size.

## What's inside

| File | Highlights |
|------|-----------|
| [principles.md](principles.md) | P1–P16. What observability is, the signals, cardinality as the cost model, discipline. |
| [engineering-rules.md](engineering-rules.md) | OBS1–OBS44, including a small-stack section. Only two rules are starred. |
| [decision-framework.md](decision-framework.md) | **Do you need this yet**, which signal for which question, where an attribute goes, how much to sample, build vs buy, when NOT to use it. |
| [review-checklist.md](review-checklist.md) | By severity, plus a separate small-stack list to use *instead of* most of it. |
| [anti-patterns.md](anti-patterns.md) | Cardinality bomb, broken trace, the average, secret in the span, uniform sampling, the platform nobody needed. |
| [scoring-rubric.md](scoring-rubric.md) | Scored against the stack in use; `n/a` under Prototype except the floor. |
| [heuristics.md](heuristics.md) | Defaults while deciding what to instrument. |
| [prompt-fragments.md](prompt-fragments.md) | Build-mode block, review lens, incident-follow-up prompt. |
| [glossary.md](glossary.md) | Terms used precisely, including where they collide with other packs. |
| [references.md](references.md) | Sources, and why this is Level 2 rather than Level 1. |

## Core claim, one line

Aggregating at write time trades tomorrow's unknown question for today's storage bill —
so put identity on spans and events where cardinality is free, keep it off metric labels
where it is not, and sample away the routine rather than the anomalies.

## The floor inside it

Two rules are starred, and they are data protection rather than observability: **no
credential or token in telemetry** (OBS31), and **personal data in telemetry is personal
data** — inventoried, pseudonymized where possible, retained deliberately, reachable by the
deletion path (OBS32). Telemetry leaves your system into a third party's store with long
retention and broad access; the vendor is a processor like any other
([security/privacy](../../security/privacy/README.md)).

## Related packs

[devops/sre](../sre/README.md) · [devops/deployment](../deployment/README.md) ·
[devops/ci-cd](../ci-cd/README.md) · [security/privacy](../../security/privacy/README.md) ·
[performance/core-web-vitals](../../performance/core-web-vitals/README.md)
