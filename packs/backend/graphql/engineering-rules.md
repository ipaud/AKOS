# Engineering Rules — GraphQL Pack

- GR1. All list-relation resolvers use DataLoader (or equivalent) batching; no per-item database call inside a resolver loop.
- GR2. Query depth limit and/or cost-based complexity limit is enforced at the gateway/server level.
- GR3. Every resolver returning user-scoped or role-scoped data verifies authorization for that specific field/object, not solely a top-level session check.
- GR4. Internal-only database fields are not exposed in the public schema unless explicitly intended for API consumers.
- GR5. Deprecated schema fields carry `@deprecated(reason: "...")` before removal, with a removal timeline communicated.
- GR6. Mutations return the created/updated/deleted object's data (or its ID at minimum) for cache updates.
- GR7. Production GraphQL endpoints use persisted queries/an allowlist, or at minimum disable introspection and have query cost limiting active.
