# Review Checklist — Clean Architecture Pack

## High

- [ ] Business-rule tests run without database/network/framework. (CR4)
- [ ] No domain/use-case file imports framework/ORM/HTTP packages. (CR1)
- [ ] External dependencies (persistence, notifications, third-party APIs) expressed as interfaces owned by the core. (CR2)
- [ ] Data crossing boundaries is plain DTOs, not ORM/framework objects. (CR5)

## Medium

- [ ] One composition root per deployable; it wires, doesn't decide. (CR3)
- [ ] Controllers/handlers are humble — no inline business rules. (CR7)
- [ ] New boundaries added with a stated reason (volatility/swappability/testability), not by template. (CR8)

## Low

- [ ] Top-level structure reflects business capabilities. (CR6)
- [ ] No interface-per-class ritual without a real second implementation or test need.
- [ ] Ring count matches actual complexity — not applied uniformly regardless of feature size.
