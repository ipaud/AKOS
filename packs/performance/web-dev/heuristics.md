# Heuristics — web.dev Practice Pack

- **Bundle-analyzer reflex:** run a bundle analyzer before optimizing blindly — the biggest offender is often one or two unexpectedly large dependencies (a whole date library imported for one function, a chart library imported for a rarely-used page).
- **The "does this need to be in the main bundle" test:** for any component/route, ask whether it's needed for the *first* interactive view — if not, dynamic-import it.
- **Image weight audit:** sort a page's network requests by size; images are almost always in the top few — check format (AVIF/WebP available?), sizing (`srcset` matching actual display size?), and compression quality.
- **Font count audit:** count distinct font-family + weight combinations loaded — more than 2-3 total is worth questioning.
- **Cache-header spot check:** inspect response headers for static assets — are they cached for a long duration with content-hashed filenames, or re-fetched every visit?
- **The skeleton test:** load the page on a throttled connection — does the loading state resemble the eventual layout (reducing perceived shift and improving perceived speed), or is it a blank screen/generic spinner?
- **Third-party script cost check:** in DevTools, filter network/performance by third-party domain — how much bytes/main-thread-time do they cost relative to first-party code?
- **Prefetch opportunity scan:** are there obvious "next click" destinations (a clear primary CTA, a paginated next page) that could be prefetched on hover/viewport-entry?
