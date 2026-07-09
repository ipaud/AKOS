# Scoring Rubric — web.dev Practice Pack

Feeds [scoring/performance-score.md](../../../scoring/performance-score.md) alongside [core-web-vitals](../core-web-vitals/scoring-rubric.md).

| Finding | Deduction |
|---------|-----------|
| No code splitting at all (single monolithic bundle) on a multi-route app | −15 (HIGH) |
| Unoptimized images (wrong format/oversized) on key pages | −10 (HIGH) |
| No caching strategy for static assets | −10 (HIGH) |
| No bundle-size budget/monitoring | −6 (MEDIUM) |
| Excessive font family/weight sprawl | −4 (MEDIUM) |
| Blank/generic loading states where skeletons would help significantly | −4 (MEDIUM) |
| Unaudited dependency bloat | −4 (MEDIUM) |
| Missing prefetch opportunities on obvious high-confidence flows | −1 (LOW) |

Anchors: **90** disciplined splitting, caching, and asset optimization with CI budgets · **75** solid practice, a gap or two · **60** monolithic bundle or unoptimized images on key pages · **<50** no performance discipline at all, bundle bloat unchecked.
