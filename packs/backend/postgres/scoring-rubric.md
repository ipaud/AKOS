# Scoring Rubric — PostgreSQL Pack

| Finding | Deduction |
|---------|-----------|
| Blocking migration risked on a large production table | −20 (CRITICAL) |
| Missing FK constraints causing orphaned data risk | −10 (HIGH) |
| No access control on PII table | −25 (CRITICAL — also security) |
| Missing index on a hot query path (verified via EXPLAIN) | −6 (MEDIUM) |
| N+1 query pattern from ORM | −6 (MEDIUM) |
| Index-everything bloat | −2 (LOW) |

Anchors: 90 constrained, indexed to real patterns, safe migrations · 75 solid with a gap · 60 missing constraints or unverified indexing · <50 unsafe migrations or unprotected PII — BLOCKED.
