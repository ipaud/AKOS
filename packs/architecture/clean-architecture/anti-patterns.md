# Anti-Patterns — Clean Architecture Pack

## Anemic ring theater

Four folders (entities/usecases/adapters/frameworks) exist, but business logic still lives in controllers, and use cases are pass-through calls to the ORM. The structure is cosplay; the dependency rule isn't actually enforced. Fix: CR1, CR4 — test without the framework; if you can't, the rings are decorative.

## Framework leaking inward

ORM entities used directly as domain objects; HTTP request objects passed into use cases; framework decorators/annotations on business logic. Fix: CR5 — plain DTOs at boundaries.

## Interface-per-class ritual

Every class gets an interface "for testability" regardless of whether more than one implementation will ever exist or a test ever mocks it. Adds indirection without buying anything. Fix: CR2 — interfaces at real seams (external I/O), not internal collaborators.

## The premature four rings

A CRUD internal tool with three screens gets full ring separation, repository interfaces for a database that will never change, and use-case classes wrapping single `save()` calls. Fix: decision-framework — apply where volatility/testability justify it.

## God composition root

Wiring logic accreting business rules ("if user.plan == 'pro', use the fast queue") — the one place meant to be dumb becomes the place nobody reviews for logic. Fix: CR3 — composition root wires, decides nothing.

## Big-bang rewrite paralysis

"We need Clean Architecture" becomes a stalled multi-month rewrite instead of incremental extraction. Fix: decision-framework retrofit steps — extract the highest-value rule first, ship, repeat.
