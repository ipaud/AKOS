# Mental Models — PostgreSQL Pack

- **Constraints as free correctness:** foreign keys, unique constraints, and check constraints enforce invariants at the one place they can never be bypassed — the database itself.
- **The index tradeoff:** every index speeds reads matching its columns/order but slows every write to that table and consumes storage — index the queries that actually run, not every column that might be queried.
- **EXPLAIN ANALYZE as ground truth:** query performance intuition is frequently wrong; the query planner's actual execution plan (not the query's apparent simplicity) determines real cost.
- **Migrations as forward-only, reversible-in-practice:** a migration should be safe to run on a live database with real traffic — locking implications matter as much as the schema change itself.
