# Glossary — PostgreSQL Pack

- **Foreign key constraint** — a database-enforced reference between tables.
- **EXPLAIN ANALYZE** — Postgres's command showing the actual query execution plan and timing.
- **Sequential scan** — reading an entire table row-by-row, the fallback when no usable index exists.
- **Partial index** — an index covering only rows matching a WHERE condition.
- **Normalization / denormalization** — organizing data to avoid duplication vs. deliberately duplicating for read performance.
- **Table rewrite** — a full table lock/copy operation triggered by certain schema changes on large tables.
