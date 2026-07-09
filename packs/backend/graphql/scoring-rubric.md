# Scoring Rubric — GraphQL Pack

| Finding | Deduction |
|---------|-----------|
| N+1 resolver pattern on primary query paths | −15 (HIGH) |
| No query depth/complexity limiting | −15 (HIGH — also security) |
| Missing field-level authorization | −25 (CRITICAL — also security) |
| Database-mirror schema leaking internal fields | −6 (MEDIUM) |
| Introspection open in production with no other mitigation | −6 (MEDIUM) |
| Deprecated fields removed without notice | −2 (LOW) |

Anchors: 90 batched resolvers, bounded queries, field-level authz solid · 75 solid with a perf gap · 60 N+1 patterns present · <50 unbounded queries and missing field authz — BLOCKED.
