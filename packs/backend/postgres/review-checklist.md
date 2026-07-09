# Review Checklist — PostgreSQL Pack

## High
- [ ] Foreign keys declared as real constraints. (PG-E1)
- [ ] Migrations on large tables use safe patterns (no blocking rewrites). (PG-E4)
- [ ] PII/sensitive tables have documented access controls. (PG-E6)

## Medium
- [ ] NOT NULL/CHECK constraints match domain invariants. (PG-E2)
- [ ] Indexes match real query patterns, verified via EXPLAIN. (PG-E3)
- [ ] Migrations tested against production-like data volume. (PG-E5)

## Low
- [ ] Slow queries addressed via indexing/rewriting, not accepted as normal. (PG-E7)
