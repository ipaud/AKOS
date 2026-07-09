# Scoring Rubric — Testing Pyramid Pack

Feeds [scoring/overall-score.md](../../../scoring/overall-score.md) maintainability component.

| Finding | Deduction |
|---------|-----------|
| Inverted pyramid (E2E-dominant, slow flaky CI) | −15 (HIGH) |
| No unit tests on core business logic | −15 (HIGH) |
| Chronically flaky tests left unfixed | −10 (HIGH) |
| No integration layer at all | −6 (MEDIUM) |
| E2E coverage missing on a genuinely critical journey | −6 (MEDIUM) |

Anchors: 90 well-shaped pyramid, fast reliable CI · 75 solid with a layer gap · 60 inverted or flaky · <50 no meaningful automated coverage.
