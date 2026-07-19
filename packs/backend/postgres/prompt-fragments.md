# Prompt Fragments — PostgreSQL Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply PostgreSQL practice (AKOS L2):
- Declare referential integrity as real FOREIGN KEY constraints. A column
  holding another table's id without one is a defect unless the reason
  is documented (cross-database sharding and similar).
- Set NOT NULL on every column the domain never allows to be null; add
  CHECK constraints for simple invariants (price >= 0, valid enum set,
  end_at > start_at). Enforce in the schema, not defensively in app code.
- Index the columns that real queries filter, join, and sort on — FK
  columns included, since Postgres does not index them automatically.
  Prove each index against an actual query pattern; do not add indexes
  speculatively, every one taxes writes and storage.
- Use a partial index when queries always carry the same predicate
  (WHERE deleted_at IS NULL); GIN for full-text, array, or JSONB
  containment; B-tree otherwise.
- Migrations on large tables must not hold a long exclusive lock. To add
  a non-null column: add it nullable, backfill in batches, then SET NOT
  NULL. Volatile defaults and adding NOT NULL to an existing column force
  a rewrite — plan for it.
- Test migrations against production-like data volume before production.
- Tables holding PII or secrets carry documented access control (RLS
  policies or explicit application-layer scoping), not implicit trust.
- Fetch named columns, not SELECT *. Batch or join relation loads; no ORM
  lazy-load inside a loop over rows.
- Normalized by default. Any duplicated or derivable column is a
  deliberate denormalization with its sync mechanism written down.
```

## Fragment: review lens

```text
Review this schema and its queries as a PostgreSQL reviewer:
1. Constraints — every id-shaped column backed by a FK? NOT NULL and
   CHECK matching the domain's real invariants, or is correctness being
   re-checked in application code instead?
2. Indexes — does each frequent WHERE/JOIN/ORDER BY have a supporting
   index, FK columns included? Any index with no query that uses it?
3. Plans — for each slow or hot query, read EXPLAIN ANALYZE before
   proposing anything. Flag sequential scans on large tables where an
   index scan belongs. Never propose an index from intuition alone.
4. Migrations — does any statement rewrite or exclusively lock a large
   live table? Rewrite it into the nullable-backfill-constrain pattern.
   Has it been run against production-like volume?
5. Access control — do PII/sensitive tables have documented scoping?
6. Query shape — SELECT * in application code, ORM lazy-loads inside
   loops, or unbounded result sets?
Report by severity per review-checklist.md, each finding with the exact
DDL or query rewrite, not a direction to "optimize".
```

## Fragment: slow-query diagnosis pass

```text
Diagnose this query with evidence, in order:
- Run EXPLAIN (ANALYZE, BUFFERS) and read the actual plan. State the
  dominant cost node and the row-estimate versus actual-row gap.
- Name the cause: missing index, unusable index (function or type
  mismatch on the column, leading-column order wrong), stale statistics,
  needless sort, or genuinely large result set.
- Propose the narrowest fix — a partial or composite index over a broad
  one, a query rewrite over a new index where the rewrite suffices.
- Re-run EXPLAIN ANALYZE after the fix and report the before/after.
- State the write-side cost any new index introduces.
Guessing at fixes without a plan is not a diagnosis.
```

## Fragment: migration safety pass

```text
Before this migration touches production, answer each:
- Which statements take ACCESS EXCLUSIVE locks, and for how long at the
  target table's real row count?
- Does any statement rewrite the table (adding NOT NULL to an existing
  column, a volatile default, most type changes)?
- Can it be split into fast, individually safe steps: nullable column →
  batched backfill → constraint added afterwards?
- Are new indexes on live tables created CONCURRENTLY?
- Is it reversible, and is the reverse path written and tested?
- Has it been run against production-like data volume?
Any unanswered question blocks the migration.
```

## One-liner (for tight token budgets)

```text
Postgres rules: real FK/NOT NULL/CHECK constraints in the schema, not in
app code; index the queries that actually run (FK columns included) and
verify with EXPLAIN ANALYZE before and after; no blocking rewrites on
large tables — nullable, backfill, then constrain, indexes CONCURRENTLY;
documented access control on PII tables; no SELECT * and no ORM N+1;
normalized by default, denormalization documented with its sync path.
```
