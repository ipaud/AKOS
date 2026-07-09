# Principles — Core Web Vitals Pack

## LCP (target ≤2.5s at 75th percentile)

- **CW1** — Identify the actual LCP element (usually via DevTools/field data) before optimizing blindly; different pages have different LCP elements.
- **CW2** — Server response time (TTFB) is the first lever: fast backend responses, CDN/edge caching, and minimal redirect chains shorten the whole downstream chain.
- **CW3** — The LCP resource (hero image, font, critical CSS) is discoverable early in the HTML (not injected late via JS) and preloaded if it's not naturally early.
- **CW4** — Render-blocking resources (synchronous CSS/JS in `<head>`) are minimized; critical CSS is inlined, non-critical CSS/JS deferred.

## INP (target ≤200ms at 75th percentile)

- **CW5** — Long tasks (>50ms of uninterrupted main-thread work) are broken up (yielding to the browser between chunks) so interactions can be processed promptly.
- **CW6** — Expensive work triggered by interactions (large re-renders, heavy computation) is deferred, debounced, or moved off the main thread (Web Workers) where possible.
- **CW7** — Third-party scripts are loaded async/deferred and audited for their main-thread cost; scripts that block interactivity are the most common real-world INP killer.
- **CW8** — Visual feedback for an interaction (state change, disabled state) is applied immediately even if the underlying operation takes longer, so the *perceived* response is fast even when the *complete* operation isn't instant.

## CLS (target ≤0.1)

- **CW9** — Every image, video, ad slot, and embed has explicit dimensions (width/height or aspect-ratio) reserved before content loads, so nothing shifts to make room later.
- **CW10** — Web fonts use `font-display: swap` or `optional` with matched fallback metrics, so font-swap doesn't cause a visible reflow.
- **CW11** — Content is never injected above existing content in response to user action without an explicit trigger (e.g. a "load more" click is fine; an unprompted insertion above the fold isn't).
- **CW12** — Animations use compositor-friendly properties (`transform`, `opacity`) rather than properties that trigger layout (`top`, `width`, `margin`), matching the [web coding-style animation rules](../../frontend/css/README.md).

## Cross-cutting

- **CW13** — Measure with field data (real-user monitoring / CrUX) as ground truth; use lab tools (Lighthouse) for debugging root cause, not for the final verdict.
- **CW14** — Targets are 75th-percentile thresholds, not averages — a page passing on average with a bad tail is still failing.
