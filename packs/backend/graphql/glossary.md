# Glossary — GraphQL Pack

- **N+1 problem** — one query per parent-list item instead of a single batched query.
- **DataLoader** — a batching/caching utility solving N+1 by collapsing per-item loads into one call.
- **Query depth/complexity limiting** — bounding how expensive a client query can be.
- **Resolver** — the function fetching data for a schema field.
- **Persisted query** — a pre-registered query referenced by ID, preventing arbitrary query execution.
- **Introspection** — GraphQL's built-in schema self-description capability.
