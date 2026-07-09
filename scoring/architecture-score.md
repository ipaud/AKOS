# Architecture Score (0–100)

Measures structural soundness — right-sized, changeable, testable. Also reflects the complexity-challenge (both under- and over-engineering are findings).

## Inputs

- [clean-architecture](../packs/architecture/clean-architecture/scoring-rubric.md)
- [solid](../packs/architecture/solid/scoring-rubric.md)
- [domain-driven-design](../packs/architecture/domain-driven-design/anti-patterns.md) (via review findings)
- [martin-fowler-refactoring](../packs/architecture/martin-fowler-refactoring/scoring-rubric.md)
- [design-patterns](../packs/architecture/design-patterns/scoring-rubric.md)
- [twelve-factor-app](../packs/architecture/twelve-factor-app/scoring-rubric.md) — for deployables

## Deductions

CRITICAL −25 (untestable/unchangeable at rewrite scale, committed secrets), HIGH −10-15 (framework-entangled core, god classes, LSP breaks), MEDIUM −4-6 (over-engineered rings/interfaces on trivial features, missing boundaries at real seams), LOW −2.

Over-engineering and under-engineering both deduct — a four-ring CRUD tool and a framework-entangled untestable core are opposite failures scored the same way.

## Interpretation

- **90** — core testable in isolation, boundaries placed deliberately, proportional to complexity.
- **75** — mostly sound, some leakage or minor ceremony.
- **60** — framework-entangled or over-abstracted; hard to change.
- **<50** — rewrite-scale entanglement; BLOCKED for Production profile.
