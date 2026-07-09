# Mental Models — Clean Architecture Pack

## The four rings

**Entities** (enterprise business rules — data + logic true regardless of this application) → **Use cases** (application-specific business rules — orchestrate entities to accomplish a goal) → **Interface adapters** (convert data between use cases and the outside: controllers, presenters, gateways) → **Frameworks & drivers** (web framework, database, UI, external services). Real systems often collapse to 2–3 effective rings; the count isn't sacred, the direction is.

## The dependency rule

Nothing in an inner ring knows anything about an outer ring. Crossing the boundary the "wrong way" (a use case importing a database client) is only allowed via inversion: the inner ring defines an interface (`OrderRepository`), the outer ring implements it, and a composition root wires the concrete class in. Same shape as [SOLID's Dependency Inversion](../solid/mental-models.md).

## Ports and adapters (hexagonal architecture)

An equivalent framing: the application core exposes **ports** (interfaces for what it needs — persistence, notifications, external APIs); **adapters** implement those ports for specific technology. Swapping Postgres for DynamoDB, or REST for GraphQL, means writing a new adapter — the core is untouched. Clean Architecture's rings and hexagonal's ports/adapters are the same idea in different clothing; use whichever vocabulary the team already has.

## The humble object pattern

Hard-to-test things (UI rendering, database calls) are split into a humble wrapper (thin, untested, does only I/O) and testable logic (a presenter, a gateway interface) that the wrapper calls. This is how "the database is a detail" becomes concrete: the humble `SqlOrderRepository` implements `OrderRepository`; everything interesting is tested against the interface with a fake.

## Composition root

The one place (main/bootstrap) where concrete implementations are chosen and wired into interfaces. Everywhere else in the codebase talks to interfaces; only the root knows about frameworks and drivers. Finding business logic in the composition root, or framework imports scattered through use cases, are the two symptoms this model predicts and detects.
