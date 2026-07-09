# Principles — web.dev Practice Pack

- **WD1 — Split code by route/feature boundary**, so navigating to a view doesn't download code for views the user hasn't visited.
- **WD2 — Lazy-load below-the-fold and non-critical resources** (images via `loading="lazy"`, heavy components via dynamic import), reserving eager loading for what's needed immediately.
- **WD3 — Serve modern image formats (AVIF/WebP) with fallbacks**, sized to actual rendered dimensions via `srcset`/responsive images — never ship a source image far larger than its rendered size.
- **WD4 — Subset and preload critical fonts**; limit font family/weight count to what's actually used — fewer families and weights load faster and render more predictably.
- **WD5 — Cache aggressively with correct invalidation.** Static assets get long cache lifetimes with content-hashed filenames (cache-busting via the URL, not cache-control gymnastics); API responses cache per their actual freshness requirements.
- **WD6 — Design loading states deliberately** (skeleton screens matching eventual layout, progressive/blur-up images, optimistic UI) — perceived performance is a designed property, not a byproduct.
- **WD7 — Audit and minimize dependencies.** Every dependency added to a bundle is evaluated for its size cost relative to its value; prefer smaller/tree-shakeable alternatives; remove unused dependencies.
- **WD8 — Defer non-critical third-party scripts** and load them after the main content is interactive, never blocking the critical rendering path.
- **WD9 — Measure bundle size in CI** with a budget per route/chunk, failing the build (or at least flagging) on regression beyond the budget.
- **WD10 — Prefetch likely next navigations** (hover-intent prefetch, viewport-based route prefetch) when confidently predictable, trading a small bandwidth cost for a much faster subsequent navigation.
