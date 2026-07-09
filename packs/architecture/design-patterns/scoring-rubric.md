# Scoring Rubric — Design Patterns Pack

Feeds [scoring/architecture-score.md](../../../scoring/architecture-score.md).

| Finding | Deduction |
|---------|-----------|
| Global-state Singleton causing test/coupling problems | −10 (HIGH) |
| Pattern applied with no real trigger (hypothetical variant, single case) | −6 (MEDIUM) |
| Pattern-name/structure mismatch causing reader confusion | −4 (MEDIUM) |
| Class-based pattern where a native language feature was simpler | −2 (LOW) |
| Layered/nested creational-pattern ceremony beyond actual complexity | −4 (MEDIUM) |

Anchors: **90** patterns used sparingly and correctly, matched to real triggers · **75** mostly sound, a couple of speculative applications · **60** frequent pattern-for-pattern's-sake · **<50** pattern ceremony actively obstructing readability/change.
