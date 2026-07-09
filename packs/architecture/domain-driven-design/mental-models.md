# Mental Models — DDD Pack

## Ubiquitous language

One vocabulary spanning conversation, docs, and code within a bounded context. Class names, method names, and even test descriptions use the domain expert's words verbatim. When a developer and a domain expert use different words for the same concept, that's a defect to fix immediately, not a translation to maintain.

## Bounded context

An explicit boundary within which a particular model is consistent and a term has one meaning. Different contexts may use the same word differently on purpose (Sales' "Customer" tracks leads and deals; Billing's "Customer" tracks payment methods and invoices) — that's not inconsistency, it's honest modeling of genuinely different concerns. A **context map** documents how contexts relate: shared kernel, customer-supplier, anti-corruption layer, conformist, etc.

## Entity vs. value object

**Entity** — has identity that persists through change; two entities with identical attributes are still different things (two `Order`s with the same items are different orders). **Value object** — defined entirely by its attributes, immutable, interchangeable if equal (`Money(10, "EUR")` is the same value regardless of which "instance" created it). Getting this distinction right eliminates a whole class of identity-confusion bugs and unlocks free immutability wins for the value side.

## Aggregate

A cluster of entities/value objects treated as one consistency unit, with a single **aggregate root** as its only external entry point — nothing outside touches the internals directly. Invariants that must hold *within* the aggregate are enforced by the root; anything crossing aggregate boundaries is eventually consistent, not transactional.

## Domain events

Something that happened in the domain that other parts of the system (or other bounded contexts) care about (`OrderPlaced`, `PaymentFailed`). Modeling them explicitly turns implicit side effects ("also send an email, also update inventory") into named, testable, replayable facts.

## Anti-corruption layer

A translation layer at the boundary between your bounded context and an external system (legacy system, third-party API, another team's context) that prevents their model from leaking into yours. The cost of translation is cheaper than the cost of a corrupted domain model.
