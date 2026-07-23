---
schema_version: 1
id: performance-review
description: Focused performance pass.
agents: [performance-reviewer]
packs: [performance/browser-rendering, performance/core-web-vitals, performance/network-performance, performance/web-dev]
profiles: [Prototype, Production, Game Dev, Internal Tool]
status: stable
maintainer: core
---

# Workflow: Performance Review

Focused performance pass.

## Agent

[performance-reviewer](../agents/performance-reviewer.md), loading the four [performance packs](../packs/performance/core-web-vitals/README.md).

## Sweep

1. **LCP triage** — TTFB → resource discoverability → render-blocking. Is LCP content server-rendered/preloaded?
2. **INP** — long tasks, third-party script cost, immediate visual feedback on interactions.
3. **CLS** — reserved dimensions on media, font-swap discipline, no unprompted content injection.
4. **Bundle/resource** — code splitting, image formats/sizing, caching, dependency bloat.
5. **Rendering** — animate transform/opacity only, no layout thrashing, virtualize large lists.
6. **Network** — HTTP/2+, compression, CDN, priority hints.

Trust field/RUM data over lab measurements when they diverge.

## Profile adjustments

- **Prototype/Internal Tool:** skip unless something's visibly slow.
- **Production:** full sweep, Core Web Vitals in "Good" band on key pages.
- **Game Dev:** weight frame budget (browser-rendering) over page-load metrics.

## Exit criteria

No vital in the "Poor" band on a key page (that's BLOCKED). Findings name the vital/stage and estimated savings.
