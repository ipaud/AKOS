# Scoring Rubric — DDD Pack

Feeds [scoring/architecture-score.md](../../../scoring/architecture-score.md).

| Finding | Deduction |
|---------|-----------|
| Invariant violated because enforcement lives outside the aggregate root | −15 (HIGH) |
| External model leaking directly into domain layer, no translation | −10 (HIGH) |
| God aggregate causing contention on unrelated concerns | −10 (HIGH) |
| Vocabulary mismatch between code and domain experts on core concepts | −6 (MEDIUM) |
| Primitive obsession on core value concepts | −4 (MEDIUM) |
| Tactical DDD ceremony on trivial CRUD subdomain (over-engineering) | −4 (MEDIUM) |

Anchors: **90** clean context boundaries, invariants enforced, language matches domain · **75** sound core with local gaps · **60** anemic model or god aggregate · **<50** invariants routinely violated, BLOCKED for Production on the affected subdomain.
