# Anti-Patterns — GraphQL Pack

- **N+1 resolver** — fetching related data per-item in a loop instead of batched, tanking performance on any list query.
- **Unbounded query depth** — no limit on nested query depth, allowing a trivially crafted deeply-nested query to exhaust server resources ([API4](../../security/owasp-api-top-10/anti-patterns.md)).
- **Database-mirror schema** — GraphQL types that are literally the database schema, leaking internal fields and coupling the API to internal storage structure.
- **Auth-check-once** — verifying authentication at the gateway but trusting every resolver to return only authorized data with no field-level check.
- **Introspection open in production** — full schema introspection enabled publicly, handing attackers a complete map of the API surface.
