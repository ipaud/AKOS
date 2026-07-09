# Mental Models — web.dev Practice Pack

## The critical rendering path

The sequence from receiving HTML to painting pixels: parse HTML → build DOM → discover and load CSS/JS → build render tree → layout → paint. Anything blocking this path (synchronous scripts in `<head>`, render-blocking CSS) delays first paint; anything unnecessary in this path (unused CSS, oversized images) wastes the budget. Optimization means shortening or removing links in this specific chain.

## Code splitting as demand-based loading

Instead of one monolithic bundle, split code along natural boundaries (route, feature, rarely-used component) so each view loads only its own code plus shared foundations — deferred chunks load on demand (navigation, interaction, viewport entry). The mental model: bundle boundaries should mirror *usage* boundaries, not just *file organization* boundaries.

## The image/font tax

Images and fonts are frequently the largest bytes on a page and the least optimized by default — a single unoptimized hero photo can outweigh an entire JS bundle. Treating image format (AVIF/WebP), sizing (responsive `srcset`), and font subsetting as first-class performance work (not an afterthought after "the code is fast") closes the largest easy win on most real pages.

## Perceived vs. actual performance

Actual performance is measured time; perceived performance is what the user *feels*. Techniques like skeleton screens, optimistic UI updates, and progressive image loading (blur-up) manipulate perceived performance independent of actual load time — genuinely valuable because user satisfaction tracks perceived speed at least as strongly as measured speed.

## Cache layers as a hierarchy

Browser HTTP cache (fastest, per-browser) → CDN/edge cache (fast, shared across users near a region) → server-side cache (application/database query cache) → origin computation (slowest). Each layer that successfully serves a request skips all the more expensive layers below it — cache-hit-rate at the outermost layer is the highest-leverage performance lever available for repeat traffic.
