# Prompt Fragments — Clean Architecture Pack

## Fragment: build-mode constraint block

```text
Apply Clean Architecture constraints (AKOS L3) proportionally to complexity:
- Dependencies point inward: domain/use-case code never imports framework/
  ORM/HTTP packages directly.
- External needs (persistence, notifications, third-party APIs) are
  interfaces owned by the core, implemented outside.
- One composition root wires concrete implementations; it contains no
  business rules.
- Data crossing boundaries is plain DTOs, not ORM entities or framework
  request objects.
- Only add this structure where volatility or testability genuinely
  justify it (multiple delivery mechanisms, swappable persistence, complex
  rules needing isolated tests) — a 3-screen CRUD tool doesn't need four
  rings. State the reason when adding a boundary.
```

## Fragment: review lens

```text
Review this codebase's architecture against Clean Architecture:
1. Import-direction check — any domain/use-case file importing framework/
   ORM/HTTP packages?
2. Unplug test — can business-rule tests run without DB/network/framework?
3. Composition-root check — is wiring separated from business decisions?
4. Boundary-cost check — are interfaces/rings present without a real
   second implementation or testability need (over-engineering), or
   missing where genuine volatility exists (under-engineering)?
Report findings with the specific file/module and the minimal fix
(extract an interface, inline an unnecessary one).
```

## One-liner

```text
Clean Architecture: dependencies point inward; core has no framework
imports; external needs are core-owned interfaces; one composition root;
plain DTOs at boundaries; apply proportional to actual volatility/
testability need, not by default.
```
