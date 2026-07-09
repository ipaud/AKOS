# Prompt Fragments — DDD Pack

## Fragment: build-mode constraint block

```text
Apply DDD proportionally (AKOS L3):
- Naming matches the domain's real vocabulary (ubiquitous language) — no
  translation gap between what stakeholders say and what code says.
- Value objects: immutable, structural equality, for concepts like money/
  email/date-ranges instead of raw primitives.
- Entities: identity-based equality, not attribute comparison.
- Aggregates: small consistency boundaries; invariants enforced inside
  the root; cross-aggregate references by ID only; cross-aggregate
  effects via domain events.
- External systems/other teams' models translated at an explicit boundary
  (anti-corruption layer), never used directly as domain types.
- Apply full tactical patterns only in the core, genuinely complex
  subdomain; supporting/generic subdomains get plain CRUD.
```

## Fragment: review lens

```text
Review this domain model against DDD:
1. Vocabulary check — does code naming match how domain experts actually
   talk? Any silent synonym drift?
2. Aggregate check — are invariants enforced at the root? Any direct
   references crossing aggregate boundaries?
3. Value-object check — primitive obsession on money/email/identifiers?
4. Boundary check — does an external/legacy model leak into domain code
   without translation?
5. Proportionality check — is tactical DDD ceremony applied to a trivial
   CRUD subdomain that didn't need it, or missing where real invariants
   exist?
```

## One-liner

```text
DDD: one vocabulary matching domain experts per bounded context; small
aggregates enforcing invariants at the root, referenced by ID elsewhere;
immutable value objects over primitives; external models translated at
the boundary; full tactical patterns only in the genuinely complex core.
```
