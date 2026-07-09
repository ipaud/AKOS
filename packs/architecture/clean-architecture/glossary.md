# Glossary — Clean Architecture Pack

- **Dependency rule** — source dependencies point only inward, toward higher-level policy.
- **Entity** — enterprise-wide business rule/data, independent of any one application.
- **Use case** — application-specific orchestration of entities to achieve a goal.
- **Interface adapter** — converts data between use cases and the outside world (controllers, presenters, gateways).
- **Composition root** — the single place concrete implementations are wired to interfaces.
- **Humble object** — a thin, untested wrapper around hard-to-test I/O, paired with tested logic behind an interface.
- **Ports and adapters (hexagonal)** — equivalent vocabulary: the core exposes ports, adapters implement them for specific tech.
- **Screaming architecture** — top-level structure that announces business purpose over framework choice.
- **DTO (data transfer object)** — plain structure carrying data across a boundary without framework/ORM behavior attached.
