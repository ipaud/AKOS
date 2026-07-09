# Engineering Rules — web.dev Practice Pack

- WE1. Routes/major features are code-split via dynamic import; the initial bundle contains only what's needed for the first interactive view.
- WE2. Below-the-fold images use `loading="lazy"`; above-the-fold/LCP-candidate images do not.
- WE3. Images are served in modern formats (AVIF/WebP) with appropriate fallback, and sized via `srcset`/responsive markup to match actual rendered dimensions — never shipping a source image significantly larger than its largest rendered size.
- WE4. Font loading is limited to actually-used families/weights/subsets; fonts are preloaded if they're needed for above-the-fold content.
- WE5. Static assets are served with long-lived cache headers and content-hashed filenames for cache-busting on change.
- WE6. Loading states for async content use skeleton layouts matching the eventual content's structure, not a generic spinner alone, for any load expected to exceed ~500ms.
- WE7. Dependency additions are reviewed for bundle-size impact (via a bundle analyzer or equivalent) before merge; unused dependencies are removed when found.
- WE8. Third-party scripts are loaded with `async`/`defer` and, where feasible, after the main content becomes interactive (e.g. via a script-loading library or manual deferred injection).
- WE9. CI includes a bundle-size budget check per route/chunk (e.g. landing page <150KB gzipped JS, app page <300KB), flagging regressions.
- WE10. Prefetching (hover-intent or viewport-based route prefetch) is used for high-confidence next navigations on primary user flows.
