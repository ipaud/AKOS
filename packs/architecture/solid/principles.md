# Principles — SOLID Pack

## S — Single Responsibility Principle

A class/module has one reason to change — one stakeholder/axis it answers to. **Applied:** split classes serving two unrelated concerns (business logic + formatting, domain rule + persistence). **Overuse boundary:** don't split a class because it has multiple *methods* — cohesive methods serving one responsibility belong together.

## O — Open/Closed Principle

Modules should be extensible without modifying their existing, tested source. **Applied:** new payment provider = new class implementing `PaymentGateway`, not an edited `if/else` chain in the existing one. **Overuse boundary:** don't pre-build extension points (strategy interfaces, plugin hooks) for variation that hasn't happened yet — that's speculative generality, YAGNI's target.

## L — Liskov Substitution Principle

Subtypes must be substitutable for their base type without breaking caller expectations (same preconditions or weaker, same postconditions or stronger, no new exceptions the base didn't promise). **Applied:** if a subclass needs to override a method to throw "not supported", the hierarchy is wrong — reach for composition or a narrower interface. **Overuse boundary:** LSP doesn't forbid all inheritance, only inheritance that silently changes behavior contracts.

## I — Interface Segregation Principle

Clients depend only on the methods they use; split fat interfaces by client need. **Applied:** `Readable`/`Writable` instead of one `FileHandler` with both, when some clients only ever read. **Overuse boundary:** don't fragment into single-method interfaces reflexively — segregate where clients actually differ, not preemptively.

## D — Dependency Inversion Principle

High-level policy and low-level detail both depend on abstractions; the abstraction is owned by the policy (consumer) side. **Applied:** a use case defines `NotificationSender`; email/SMS/push implementations depend on it, not vice versa. **Overuse boundary:** don't invert every dependency — stable, unlikely-to-vary internal collaborators (a `Money` value object, a math utility) don't need an interface.

## Meta-rule

Every principle in this pack is a response to *observed or reasonably certain* pain (a real second implementation, a real recurring change, a real test that needs isolation). Applied preemptively against imagined future requirements, all five produce more code, more indirection, and no benefit — see [anti-patterns.md](anti-patterns.md).
