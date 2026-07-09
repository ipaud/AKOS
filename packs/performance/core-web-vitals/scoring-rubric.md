# Scoring Rubric — Core Web Vitals Pack

Feeds [scoring/performance-score.md](../../../scoring/performance-score.md).

| Finding | Deduction |
|---------|-----------|
| LCP >4s at p75 on a key page | −25 (CRITICAL) |
| INP >500ms at p75 on a key page | −25 (CRITICAL) |
| CLS >0.25 on a key page | −25 (CRITICAL) |
| LCP 2.5-4s / INP 200-500ms / CLS 0.1-0.25 (Needs Improvement band) | −10 each (HIGH) |
| No field data collection at all (lab-only verification) | −10 (HIGH) |
| Missing dimensions on media causing measurable shift | −4 each, cap −12 (MEDIUM) |
| No performance budget in CI | −6 (MEDIUM) |
| Third-party script blocking main thread, unaudited | −4 (MEDIUM) |

Anchors: **95** all three vitals in "Good" band at p75 with field data · **80** all vitals "Good" or borderline, minor gaps · **65** one vital in "Needs Improvement" · **<50** any vital in "Poor" band on a key page — BLOCKED for Production.
