# Engineering Rules — PostgreSQL Pack

- PG-E1. Foreign key relationships are declared as actual FK constraints, not enforced only in application code.
- PG-E2. NOT NULL is set on any column the domain never allows to be null; CHECK constraints enforce simple invariants (e.g. `price >= 0`).
- PG-E3. Indexes exist for columns used in frequent WHERE/JOIN/ORDER BY clauses, verified against real query patterns (not speculative).
- PG-E4. Migrations adding NOT NULL columns to large existing tables use a safe pattern (nullable + backfill + constraint) rather than a single blocking statement.
- PG-E5. Migrations are tested against a production-like data volume before running on production, where feasible.
- PG-E6. Tables containing PII/sensitive data have documented access controls (RLS policies or equivalent application-layer scoping).
- PG-E7. Slow queries (identified via monitoring/EXPLAIN ANALYZE) are indexed or rewritten before being accepted as "normal."
