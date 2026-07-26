# Architecture Knowledge Graph

How the seven architecture packs relate. Parent: [knowledge-graph](knowledge-graph.md).

## The layers

- **Class/module level:** [SOLID](../packs/architecture/solid/README.md) (design principles), [Design Patterns](../packs/architecture/design-patterns/README.md) (named solutions).
- **Cost of a boundary:** [Philosophy of Software Design](../packs/architecture/philosophy-of-software-design/README.md) — cuts across every level, because module depth applies to a function, a class, a service, and an API alike.
- **System level:** [Clean Architecture](../packs/architecture/clean-architecture/README.md) (dependency rule), [DDD](../packs/architecture/domain-driven-design/README.md) (domain modeling).
- **Change discipline:** [Refactoring](../packs/architecture/martin-fowler-refactoring/README.md) (how to get there safely).
- **Deployment level:** [Twelve-Factor App](../packs/architecture/twelve-factor-app/README.md).

## Key concept edges

- **Dependency Inversion** ([SOLID D](../packs/architecture/solid/principles.md)) ↔ **the dependency rule** ([Clean Architecture](../packs/architecture/clean-architecture/mental-models.md)) — the same idea at class vs system scale.
- **Entities ring** ([Clean Architecture](../packs/architecture/clean-architecture/mental-models.md)) ↔ **aggregates/value objects** ([DDD](../packs/architecture/domain-driven-design/mental-models.md)) — the domain core, modeled deeply by DDD.
- **Refactoring toward patterns** ([Refactoring](../packs/architecture/martin-fowler-refactoring/mental-models.md)) ↔ **pattern trigger conditions** ([Design Patterns](../packs/architecture/design-patterns/principles.md)) — patterns arrive via incremental refactoring on real need.
- **Config out of code** ([Twelve-Factor](../packs/architecture/twelve-factor-app/principles.md)) ↔ **framework is a detail** ([Clean Architecture](../packs/architecture/clean-architecture/philosophy.md)) — both isolate the important from the swappable.
- **Single responsibility** ([SOLID S](../packs/architecture/solid/principles.md)) ↔ **module depth** ([PSD](../packs/architecture/philosophy-of-software-design/mental-models.md)) — the corpus's one genuine intra-domain disagreement, on how far to decompose. SOLID asks whether a unit has one reason to change; PSD asks whether the boundary lets a caller stop knowing something. Resolved in [PSD's decision framework](../packs/architecture/philosophy-of-software-design/decision-framework.md), not by picking a winner.
- **Boundaries follow volatility** ([Clean Architecture](../packs/architecture/clean-architecture/philosophy.md)) ↔ **a split must hide something** ([PSD1/PSD3](../packs/architecture/philosophy-of-software-design/engineering-rules.md)) — two tests for the same question, applied at different scales.
- **Divergent change / shotgun surgery smells** ([Refactoring](../packs/architecture/martin-fowler-refactoring/mental-models.md)) ↔ **change amplification and information leakage** ([PSD](../packs/architecture/philosophy-of-software-design/mental-models.md)) — the same phenomenon named from the symptom side and from the cause side.

## The complexity-challenge spine

Every pack here carries an anti-overuse guard, all feeding the [complexity-cost concept node](knowledge-graph.md): SOLID's "apply to real pain," Clean Architecture's "boundaries follow volatility," DDD's "tactical only in the complex core," Design Patterns' "trigger condition first," Refactoring's "rule of three." [PSD](../packs/architecture/philosophy-of-software-design/README.md) is the spine stated directly rather than as a guard on something else — it makes complexity the measured quantity, and supplies the vocabulary (change amplification, cognitive load, unknown unknowns) the others' guards imply. Together they operationalize [constitution Art. 7](../core/constitution.md) and [pau-avila principle 2](../packs/personal/pau-avila/principles.md).

## Authority

All L3 (methodologies) except [Refactoring](../packs/architecture/martin-fowler-refactoring/README.md) and [Twelve-Factor](../packs/architecture/twelve-factor-app/README.md) (L2 industry-authority). Contextual — apply proportionally to profile. [PSD](../packs/architecture/philosophy-of-software-design/README.md) is the only pack in the corpus with no starred floor rule and no CRITICAL scoring band, deliberately: a design opinion must not acquire floor authority.
