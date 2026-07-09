# Principles — PostgreSQL Pack

- **PG1** — Foreign key constraints enforce referential integrity at the database level, not solely in application code.
- **PG2** — Columns get NOT NULL and CHECK constraints wherever the domain genuinely disallows null/invalid values.
- **PG3** — Indexes are added for columns used in WHERE/JOIN/ORDER BY on frequently-run queries, verified via EXPLAIN ANALYZE, not added speculatively.
- **PG4** — Migrations are reviewed for locking behavior on large tables (e.g. adding a NOT NULL column without a default locks/rewrites the table) before running against production.
- **PG5** — Normalization avoids duplicate/derivable data by default; denormalization is a deliberate, documented performance tradeoff, not a default.
- **PG6** — Sensitive columns (PII, secrets) are identified and access-controlled (via RLS or application-layer scoping) explicitly.
- **PG7** — N+1 query patterns from application code are batched/joined, mirroring [GraphQL GQ1](../graphql/principles.md) at the SQL layer.
