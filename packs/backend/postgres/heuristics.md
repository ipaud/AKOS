# Heuristics — PostgreSQL Pack

- A slow query? Run `EXPLAIN ANALYZE` before guessing — look for sequential scans on large tables where an index scan should occur.
- A column referencing another table's ID with no foreign key constraint → add one, unless there's a specific documented reason (e.g. cross-database sharding).
- A migration adding a column with a computed default on a large table → check if it requires a table rewrite/lock; consider a nullable column + backfill + constraint-add pattern instead.
- Repeated identical WHERE-clause shapes across the codebase not backed by a matching index → add the index.
- Data duplicated across tables "for query convenience" → confirm it's a deliberate denormalization decision, not an oversight.
