# Maintainability Score (0–100)

Measures how cheaply the next person can read, change, and trust this code —
naming, function and file size, nesting depth, error handling, test coverage,
comment health, and dead code. Distinct from Architecture (which scores
structure and boundaries): a well-layered system can still be unmaintainable
line by line, and a flat one can be a pleasure to change. Mechanics per
[core/scoring-model.md](../core/scoring-model.md); bands as below.

## Inputs

- [testing/testing-pyramid](../packs/testing/testing-pyramid/scoring-rubric.md) · [testing/tdd](../packs/testing/tdd/scoring-rubric.md) — is the change covered at the right level
- [architecture/martin-fowler-refactoring](../packs/architecture/martin-fowler-refactoring/scoring-rubric.md) — code smells, duplication, shotgun surgery
- [architecture/clean-architecture](../packs/architecture/clean-architecture/scoring-rubric.md) — for the readability/coupling overlap
- The active personal profile's coding preferences (e.g. [packs/personal/pau-avila/coding-preferences.md](../packs/personal/pau-avila/coding-preferences.md)) — naming, file-size, immutability conventions

## Deductions

CRITICAL −25 (no tests on a money/security/data-loss path; a change here can't be made safely), HIGH −10 (functions or files far past the project's own limits, swallowed errors that hide failure, duplicated logic that will drift), MEDIUM −4 (deep nesting where an early return fits, magic numbers, a comment that contradicts the code), LOW −1 (naming that reads against convention, dead code, a stale TODO). Confidence gates severity ([confidence-model](../core/confidence-model.md)).

Both directions deduct: an untested critical path and a test suite so brittle it blocks every refactor are opposite failures scored the same way.

## Interpretation

- **90** — reads top to bottom without cross-referencing; small focused units; critical paths covered; a newcomer ships a change on day one.
- **75** — sound, with a few long functions or thin spots in coverage to schedule.
- **60** — changeable only by the author; sparse tests, some swallowed errors, growing duplication.
- **<50** — every change risks a regression nobody catches; BLOCKED for Production profile.

Production profile with no tests on a critical path: capped at 59.
