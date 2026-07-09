# Mental Models — SOLID Pack

## Axis of change

For any class, ask: what are the distinct *reasons* this file would need to change, and who requests each one? SRP names this the axis-of-change test — a class with reasons to change from two different stakeholders (e.g. business-rule changes and reporting-format changes) has two responsibilities wearing one file.

## Closed for modification, open for extension

New behavior should be addable by adding new code (a new implementation of an interface, a new subclass, a new strategy) rather than editing existing, already-tested code. This is what makes plugin systems, payment-provider integrations, and notification channels safe to extend without regression risk on the existing paths.

## Behavioral subtyping (LSP)

A subtype must be usable anywhere its supertype is expected without the caller needing to know which concrete type it got. Violations aren't always obvious from the type signature — they show up as strengthened preconditions, weakened postconditions, or thrown exceptions the base type never promised. LSP violations are often the first sign that inheritance was the wrong tool for the relationship (composition may fit better).

## Fat interfaces force irrelevant coupling

ISP: no client should be forced to depend on methods it doesn't use. A `Worker` interface with `eat()` and `work()` forces a `RobotWorker` to implement `eat()` with a stub — that stub is coupling with no payoff. Split by client need, not by conceptual grouping.

## Depend on abstractions that the client owns

DIP: high-level modules shouldn't depend on low-level modules; both depend on abstractions — and specifically, the abstraction is defined where the *client* needs it, not where the implementation lives. This is the same mechanism as [Clean Architecture's dependency rule](../clean-architecture/mental-models.md); SOLID's DIP is that rule's class-level ancestor.
