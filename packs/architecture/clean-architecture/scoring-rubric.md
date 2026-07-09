# Scoring Rubric — Clean Architecture Pack

Feeds [scoring/architecture-score.md](../../../scoring/architecture-score.md).

| Finding | Deduction |
|---------|-----------|
| Business rules untestable without DB/network/framework | −15 (HIGH) |
| Framework/ORM types leaking into core logic | −10 (HIGH) |
| No composition root (wiring scattered, or wiring contains business logic) | −10 (HIGH) |
| Over-engineered rings on trivial features (interface-per-class ritual) | −6 (MEDIUM) |
| Missing boundary where real volatility exists (undocumented, painful to change) | −6 (MEDIUM) |
| Framework-organized top-level structure obscuring business capability | −2 (LOW) |

Anchors: **90** core testable in isolation, boundaries placed deliberately · **75** mostly sound, some leakage · **60** framework-entangled core, hard to test · **<50** rewrite-scale entanglement, BLOCKED for Production profile.
