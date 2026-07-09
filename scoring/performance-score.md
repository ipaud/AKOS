# Performance Score (0–100)

Measures perceived + measured performance.

## Inputs

- [core-web-vitals](../packs/performance/core-web-vitals/scoring-rubric.md) — LCP/INP/CLS (primary)
- [web-dev](../packs/performance/web-dev/scoring-rubric.md) — bundles/caching/images
- [browser-rendering](../packs/performance/browser-rendering/scoring-rubric.md) — jank/frame budget
- [network-performance](../packs/performance/network-performance/scoring-rubric.md)

## Deductions

- A vital in "Poor" band on a key page (LCP >4s / INP >500ms / CLS >0.25): −25 (CRITICAL)
- A vital in "Needs Improvement"; no field data; monolithic bundle; unoptimized key-page images: −10 (HIGH)
- Missing media dimensions, no CI budget, layout-property animation: −4 (MEDIUM)
- Missing prefetch, minor caching gaps: −1-2 (LOW)

## Interpretation

- **95** — all three vitals "Good" at p75 with field data; assets optimized.
- **80** — vitals good/borderline, minor gaps.
- **65** — one vital "Needs Improvement."
- **<50** — a vital in "Poor" on a key page; BLOCKED for Production.

Field/RUM data is ground truth; lab-only verification caps the confidence of any "Good" claim. Low-traffic internal tools: don't over-penalize — match effort to the profile.
