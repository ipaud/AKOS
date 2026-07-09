# Scoring Rubric — TDD Pack

| Finding | Deduction |
|---------|-----------|
| No tests at all for new business logic | −15 (HIGH) |
| Tests assert implementation internals, break on harmless refactor | −6 (MEDIUM) |
| Never-observed-red tests (suspected non-functional assertions) | −6 (MEDIUM) |
| Behavior changes smuggled into refactor commits | −6 (MEDIUM) |
| Giant untested implementation blocks with tests bolted on after | −4 (MEDIUM) |

Anchors: 90 disciplined cycle evident, behavior-focused tests · 75 solid coverage, test-after common but effective · 60 sparse/brittle tests · <50 no meaningful test discipline.
