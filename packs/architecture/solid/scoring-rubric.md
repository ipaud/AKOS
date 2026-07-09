# Scoring Rubric — SOLID Pack

Feeds [scoring/architecture-score.md](../../../scoring/architecture-score.md).

| Finding | Deduction |
|---------|-----------|
| God class blocking parallel work (SRP) | −10 (HIGH) |
| LSP violation (throwing/no-op override) live in production paths | −10 (HIGH) |
| Business logic hard-wired to concrete infra with no test isolation possible (DIP) | −10 (HIGH) |
| Fat interface with stub implementers (ISP) | −4 (MEDIUM) |
| Editing existing tested cases required to add a variant (OCP), ≥2 variants already present | −4 (MEDIUM) |
| Interface-per-class ceremony / speculative strategy patterns (overuse) | −4 each, cap −12 (MEDIUM) |

Anchors: **90** cohesive, low-coupling, abstractions at real seams only · **75** sound with local violations · **60** god classes or LSP breaks recurring · **<50** pervasive coupling blocking change, BLOCKED for Production.
