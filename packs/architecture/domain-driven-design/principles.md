# Principles — DDD Pack

- **DD1 — One term, one meaning, per context.** Code, docs, and conversation inside a bounded context use identical vocabulary; a naming mismatch between a developer and a domain expert is fixed immediately.
- **DD2 — Draw bounded contexts around real organizational/semantic seams**, not around technical convenience (a context per microservice-that-was-already-planned is backwards — model first, service boundaries follow).
- **DD3 — Different contexts may define the same term differently, deliberately**, with translation made explicit at the boundary (context map, anti-corruption layer) rather than forcing one universal model.
- **DD4 — Value objects are immutable and defined by their attributes**; prefer them over primitive obsession (`Money`, `EmailAddress`, `DateRange` instead of raw numbers/strings scattered with ad-hoc validation).
- **DD5 — Entities are defined by identity, not attributes**; equality compares identity, not field values.
- **DD6 — Aggregates are the transaction boundary.** Only the aggregate root is referenced from outside; invariants inside the aggregate are always consistent; cross-aggregate consistency is eventual, coordinated via domain events, not distributed transactions.
- **DD7 — Aggregates are small.** Default to the smallest cluster that must be transactionally consistent; reference other aggregates by ID, not by object reference, to prevent silent growth.
- **DD8 — Domain events name things that happened**, past tense, and are the mechanism for cross-aggregate and cross-context side effects.
- **DD9 — Apply tactical patterns (aggregates, repositories, events) only in the core domain's genuinely complex subdomains**; supporting/generic subdomains (auth, admin CRUD, reporting) get simpler treatment — buy or build plainly.
- **DD10 — Strategic DDD (language + context boundaries) applies far more broadly than tactical DDD**; use the former on nearly any domain with real complexity, reserve the latter for where invariants are genuinely gnarly.
