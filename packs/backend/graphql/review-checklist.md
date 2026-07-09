# Review Checklist — GraphQL Pack

## High
- [ ] Relation resolvers batched (no N+1). (GR1)
- [ ] Query depth/complexity limits enforced. (GR2)
- [ ] Field-level authorization checked in resolvers. (GR3)

## Medium
- [ ] Schema doesn't leak internal-only database fields. (GR4)
- [ ] Deprecated fields marked with reason before removal. (GR5)
- [ ] Mutations return affected object data. (GR6)

## Low
- [ ] Production uses persisted queries/allowlist or introspection disabled. (GR7)
