# Anti-Patterns — SOLID Pack

## God class (SRP violated)

One class owning validation, persistence, notification, and formatting — every feature touches it, every PR conflicts. Fix: SD1, split by axis of change.

## Interface-per-class ceremony (DIP/OCP overused)

Every class has a matching `IFoo` interface with exactly one implementation, forever. Adds a navigation hop with zero payoff. Fix: SD6 — interfaces at real seams only.

## Speculative strategy pattern (OCP overused)

A `DiscountStrategy` abstraction built for "future discount types" that never materialize; one concrete implementation, extra ceremony for years. Fix: apply on the second real variant (decision-framework).

## Refused-bequest hierarchies (LSP violated)

`Penguin extends Bird` with `fly()` overridden to throw. The type signature lies to every caller that reasonably assumes birds fly. Fix: SD3 — composition or a `Flying` capability interface instead.

## Fat interface with stub implementers (ISP violated)

`Repository` interface with 15 methods; most implementations stub 10 of them with `throw new NotImplementedException()`. Fix: SD4 — split by actual client need (`Readable`, `Writable`, `Searchable`).

## Concrete-dependency business logic (DIP violated)

Use case directly instantiating `new StripeClient()` — untestable without hitting Stripe, unswappable without editing the use case. Fix: SD5 — interface owned by the use case.

## SOLID-as-code-review-hazing

Blocking a PR because a 20-line utility function "should really implement an interface" with no second implementation ever proposed. Fix: SD6 and the decision framework — principles apply to real pain, not as a purity test.
