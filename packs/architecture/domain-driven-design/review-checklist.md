# Review Checklist — DDD Pack

## High

- [ ] Domain-layer naming matches the ubiquitous language / a maintained glossary. (DR1)
- [ ] Invariants enforced inside aggregate roots, not left to external calling code. (DR5)
- [ ] Cross-aggregate references are by ID, not direct object reference. (DR4)
- [ ] External system models don't leak directly into the domain layer (anti-corruption layer present). (DR7)

## Medium

- [ ] Value objects immutable with structural equality; entities with identity-based equality. (DR2, DR3)
- [ ] Cross-aggregate/cross-context effects use domain events, not reaching into another aggregate's internals. (DR6)
- [ ] Repositories operate at aggregate-root granularity only. (DR8)
- [ ] Tactical patterns applied only in identified core/complex subdomains — not on trivial CRUD. (DR9)

## Low

- [ ] Bounded context boundaries documented (context map) for multi-context systems.
- [ ] No primitive obsession on core domain concepts (email, money, identifiers).
