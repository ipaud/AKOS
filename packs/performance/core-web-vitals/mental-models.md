# Mental Models — Core Web Vitals Pack

## LCP as "when did the main thing appear"

LCP measures the render time of the largest content element visible in the viewport (usually a hero image, a headline block, or a large text block) — it's a proxy for "when did the user see the thing they came for," not "when did everything finish loading." Optimizing LCP means identifying that specific element and shortening the path to its render: server response time, resource discovery time, resource load time, and render-blocking time all sit on that path.

## INP as "does the page feel alive"

INP samples the latency of all (or a representative set of) user interactions across the page's lifetime and reports a high percentile — capturing not just the average click but the worst frustrating one. Unlike its predecessor (First Input Delay, which only measured the *first* interaction), INP reflects sustained responsiveness throughout the session, including interactions after the page has been open and accumulating background work for a while.

## CLS as "did the ground move"

CLS sums the impact of unexpected layout shifts — content moving after it's already been rendered and potentially already read or about to be tapped. The canonical bad experience: a user starts to tap a button, an ad loads above it, and they tap something else entirely. CLS is unusual among the three vitals in being almost entirely preventable through space-reservation discipline rather than requiring runtime optimization.

## The render-blocking chain

Every millisecond between "browser starts requesting the page" and "the LCP element is painted" is a chain: DNS/connection → server response (TTFB) → HTML parsing → resource discovery → resource loading → CSS/JS blocking → render. Optimizing LCP means finding and shortening the longest link in this specific chain for the specific page, not applying generic advice — the bottleneck differs page to page.

## Main thread contention

INP suffers when the browser's single JavaScript execution thread is busy with something else when an interaction occurs (a long task, a large re-render, a third-party script's synchronous work) — the interaction is queued behind that work. The mental model: every long task is a window during which the page *looks* interactive but isn't.
