# Philosophy — web.dev Practice Pack

## Ship only what the current view needs

The default posture of most bundlers and frameworks is to ship everything eventually needed by the application in one (or a few) bundles, loaded upfront. Performance-conscious development inverts this: ship only what the *current view* needs to become interactive, and defer everything else until it's actually needed (route change, user interaction, viewport visibility). Every byte shipped before it's needed is pure latency with no offsetting value.

## Perceived performance is partly a UX discipline, not just a bytes discipline

Two pages with identical load times can feel completely different depending on what's shown *during* the wait — a blank white screen feels slower than a skeleton screen that resembles the eventual content, even at identical actual load time. This pack treats loading-state design (skeletons, progressive rendering, optimistic UI) as a performance technique in its own right, not merely a UX nicety — perceived speed is a legitimate optimization target alongside measured speed.

## Caching is the cheapest performance win available

A resource fetched once and reused (via HTTP caching, service workers, or in-memory application caching) costs nothing on subsequent loads — no network round-trip, no server compute, no bytes transferred. Aggressive, correct caching (with sound invalidation) routinely outperforms any amount of algorithmic optimization on the "make each request faster" side, because the fastest request is the one never made.

## Optimization has diminishing returns — measure before and after

Not every optimization technique pays off equally on every page; a technique that meaningfully improves a content-heavy marketing page may be irrelevant on a data-dense authenticated dashboard. This pack's techniques are levers to pull deliberately based on measured bottlenecks (per [Core Web Vitals](../core-web-vitals/heuristics.md) diagnosis), not a checklist to apply uniformly regardless of what's actually slow.
