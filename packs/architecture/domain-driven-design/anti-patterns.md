# Anti-Patterns — DDD Pack

## Anemic domain model

Entities are bags of getters/setters; all logic lives in "service" classes operating on them from outside. Invariants aren't enforced anywhere consistently. Fix: DR5 — behavior and invariant enforcement move into the aggregate root.

## God aggregate

One aggregate (`Account`) accumulates every entity remotely related to it (orders, addresses, payment methods, support tickets) because "they're all about the account". Every transaction locks the whole thing; contention everywhere. Fix: DR4 + aggregate sizing — split by actual invariant boundaries, reference by ID.

## Primitive obsession

Emails, money, dates as raw strings/numbers validated ad-hoc in a dozen places, with subtly different rules each time. Fix: DD4 — value objects centralize validation and behavior.

## One model to rule the business

A single `Customer` class with 40 fields serving Sales, Support, Billing, and Marketing, each using a handful of fields and ignoring or misinterpreting the rest. Fix: DD3 — separate models per bounded context, translated at the seams.

## Tactical DDD on a CRUD app

Repositories, aggregates, and domain events wrapped around a settings page with three fields and no real invariants. Ceremony without payoff. Fix: DD9, decision-framework — reserve for core, complex subdomains.

## Microservices-first context mapping

Splitting into services along org-chart or deployment convenience lines before the domain model and bounded contexts are understood — resulting in chatty, tightly-coupled "distributed monolith" services. Fix: DD2 — model first, deploy second.

## Leaky external models

A third-party API's response shape used directly as internal domain types; every API change ripples through the whole codebase. Fix: DR7 — anti-corruption layer.
