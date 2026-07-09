# Principles — GraphQL Pack

- **GQ1** — Every relation-fetching resolver uses batching (DataLoader or equivalent) to prevent N+1 query patterns.
- **GQ2** — Query depth and complexity are bounded (max depth, cost-based limiting) so no client query can trigger unbounded server work.
- **GQ3** — Field-level authorization is enforced in resolvers, matching [OWASP API3](../../security/owasp-api-top-10/principles.md) — not assumed from a top-level auth check alone.
- **GQ4** — Schema models the domain/client needs, not a 1:1 mirror of database tables.
- **GQ5** — Deprecated fields are marked `@deprecated` with a reason and migration path, not silently removed.
- **GQ6** — Mutations return the affected object(s), enabling clients to update local cache without a follow-up query.
- **GQ7** — Persisted queries or an allowlist are used in production to prevent arbitrary untrusted query execution where feasible.
