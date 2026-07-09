# Architecture Knowledge Graph

How the six architecture packs relate. Parent: [knowledge-graph](knowledge-graph.md).

## The layers

- **Class/module level:** [SOLID](../packs/architecture/solid/README.md) (design principles), [Design Patterns](../packs/architecture/design-patterns/README.md) (named solutions).
- **System level:** [Clean Architecture](../packs/architecture/clean-architecture/README.md) (dependency rule), [DDD](../packs/architecture/domain-driven-design/README.md) (domain modeling).
- **Change discipline:** [Refactoring](../packs/architecture/martin-fowler-refactoring/README.md) (how to get there safely).
- **Deployment level:** [Twelve-Factor App](../packs/architecture/twelve-factor-app/README.md).

## Key concept edges

- **Dependency Inversion** ([SOLID D](../packs/architecture/solid/principles.md)) ↔ **the dependency rule** ([Clean Architecture](../packs/architecture/clean-architecture/mental-models.md)) — the same idea at class vs system scale.
- **Entities ring** ([Clean Architecture](../packs/architecture/clean-architecture/mental-models.md)) ↔ **aggregates/value objects** ([DDD](../packs/architecture/domain-driven-design/mental-models.md)) — the domain core, modeled deeply by DDD.
- **Refactoring toward patterns** ([Refactoring](../packs/architecture/martin-fowler-refactoring/mental-models.md)) ↔ **pattern trigger conditions** ([Design Patterns](../packs/architecture/design-patterns/principles.md)) — patterns arrive via incremental refactoring on real need.
- **Config out of code** ([Twelve-Factor](../packs/architecture/twelve-factor-app/principles.md)) ↔ **framework is a detail** ([Clean Architecture](../packs/architecture/clean-architecture/philosophy.md)) — both isolate the important from the swappable.

## The complexity-challenge spine

Every pack here carries an anti-overuse guard, all feeding the [complexity-cost concept node](knowledge-graph.md): SOLID's "apply to real pain," Clean Architecture's "boundaries follow volatility," DDD's "tactical only in the complex core," Design Patterns' "trigger condition first," Refactoring's "rule of three." Together they operationalize [constitution Art. 7](../core/constitution.md) and [pau-avila principle 2](../packs/personal/pau-avila/principles.md).

## Authority

All L3 (methodologies) except [Refactoring](../packs/architecture/martin-fowler-refactoring/README.md) and [Twelve-Factor](../packs/architecture/twelve-factor-app/README.md) (L2 industry-authority). Contextual — apply proportionally to profile.
