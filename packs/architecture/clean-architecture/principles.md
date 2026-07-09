# Principles — Clean Architecture Pack

- **CA1 — Dependencies point inward.** No inner-ring file imports an outer-ring concrete type. Enforced by import-direction linting where the team's size justifies it.
- **CA2 — Business rules are framework-agnostic.** Entities and use cases compile and test without the web framework, the ORM, or a running database.
- **CA3 — Interfaces are owned by the inner ring.** `OrderRepository` is defined next to the use case that needs it, not next to its SQL implementation — the consumer owns the contract.
- **CA4 — One composition root.** Concrete wiring (which database, which framework) happens in exactly one place per deployable; everywhere else depends on interfaces.
- **CA5 — Screaming architecture.** Top-level folder/module names describe what the system does, not the frameworks it uses.
- **CA6 — Boundaries follow volatility and testability need, not ritual.** Add a ring where something actually varies independently (swappable persistence, multiple delivery mechanisms) or where core logic needs isolated testing — not on every object by default.
- **CA7 — Humble objects isolate the untestable.** I/O-heavy code is a thin wrapper; the logic behind it is tested in isolation.
- **CA8 — Data crossing boundaries is plain.** DTOs/plain structures cross ring boundaries, not framework-specific objects (ORM entities, HTTP request objects) — prevents outer-ring types leaking inward.
