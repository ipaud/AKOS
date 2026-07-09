# Scoring Rubric — Refactoring Pack

Feeds [scoring/architecture-score.md](../../../scoring/architecture-score.md) and [scoring/maintainability](../../../scoring/overall-score.md) inputs.

| Finding | Deduction |
|---------|-----------|
| Refactoring landed with broken/skipped tests | −15 (HIGH) |
| Behavior change bundled with structural refactor, unreviewable | −10 (HIGH) |
| Refactoring performed on uncovered code with no characterization tests added | −10 (HIGH) |
| Premature abstraction from a single occurrence | −4 (MEDIUM) |
| Undisciplined big-bang rewrite chosen over available incremental path | −10 (HIGH) |
| Unnamed/unreviewable ad-hoc restructuring instead of catalog refactorings | −2 (LOW) |

Anchors: **90** disciplined small steps, tests green throughout, smells named and addressed · **75** generally sound, occasional mixing · **60** frequent behavior/structure conflation · **<50** refactoring routinely breaks things, BLOCKED for Production-profile merges.
