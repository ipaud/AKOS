# Scoring Rubric — REST Pack

| Finding | Deduction |
|---------|-----------|
| Always-200 anti-pattern hiding errors | −10 (HIGH) |
| Unbounded list endpoints | −10 (HIGH) |
| No versioning strategy for a public API | −6 (MEDIUM) |
| Inconsistent response envelopes | −6 (MEDIUM) |
| Verb-in-URL RPC style throughout | −4 (MEDIUM) |
| Missing machine-readable error codes | −2 (LOW) |

Anchors: 90 consistent, correctly-coded, paginated, versioned · 75 solid with a gap · 60 inconsistent conventions across endpoints · <50 RPC-style with no status-code discipline.
