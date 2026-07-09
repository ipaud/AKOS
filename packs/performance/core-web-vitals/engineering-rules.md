# Engineering Rules — Core Web Vitals Pack

- CV1. The LCP element's resource is requestable from the initial HTML response (server-rendered or preloaded), not injected exclusively via client-side JS after hydration.
- CV2. Server response time (TTFB) for primary pages is measured and budgeted (target <600ms at p75 as a starting point, tuned per stack).
- CV3. Hero images and other likely-LCP resources use `fetchpriority="high"` and are not `loading="lazy"`.
- CV4. Critical above-the-fold CSS is inlined or loaded render-blocking-minimally; non-critical CSS is deferred.
- CV5. Long tasks (>50ms) triggered by user interaction are broken into yieldable chunks (e.g. via `scheduler.yield()`/`setTimeout(0)`/chunked processing) rather than one synchronous block.
- CV6. Third-party scripts are loaded with `async`/`defer` by default; any synchronous third-party script requires a stated reason.
- CV7. Every `<img>`, `<video>`, iframe, and ad/embed slot has explicit dimensions or `aspect-ratio` reserved in CSS before content loads.
- CV8. Web font loading uses `font-display: swap` or `optional`, with a fallback font metric-matched closely enough to avoid visible reflow (or a font-loading strategy avoiding FOUT/FOIT layout shift).
- CV9. Animations and transitions use `transform`/`opacity` exclusively; layout-triggering properties (`top`, `left`, `width`, `height`, `margin`) are not animated.
- CV10. Real-user monitoring (field data) is collected for LCP/INP/CLS on production traffic; lab tools (Lighthouse) are used for local debugging, not as the sole release gate.
- CV11. Performance budgets are checked in CI (bundle size, Lighthouse score thresholds) to catch regressions before merge.
