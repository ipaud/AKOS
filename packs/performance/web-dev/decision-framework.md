# Decision Framework — web.dev Practice Pack

## Which optimization technique for which symptom

| Symptom | Technique |
|---------|-----------|
| Large initial JS bundle | Code splitting (WE1) |
| Slow image-heavy page | Format/sizing optimization (WE3), lazy loading (WE2) |
| Repeat visits still slow | Caching strategy review (WE5) |
| Feels slow before content appears | Skeleton/perceived-performance work (WE6) |
| Slow after a dependency was added | Bundle-analyzer audit (WE7) |
| Third-party widget tanking metrics | Defer/async loading, consider removal (WE8) |

## Code-splitting granularity

Split by route always (cheap, high-value). Split by feature/component when a component is large (charting libraries, rich text editors) and used on only some views. Don't split every small component — chunk-request overhead can exceed the savings below a certain size threshold; a bundle analyzer showing many tiny chunks each <5-10KB is a sign of over-splitting.

## Image format/CDN choice

Use an image CDN/service with automatic format negotiation (AVIF/WebP with fallback) and on-the-fly resizing where available — it centralizes WE3 without per-image manual work. For static sites without such infrastructure, build-time image optimization (via the framework's image component or a build plugin) is the next-best option; manual per-image optimization is the last resort for small projects only.

## Caching strategy by content type

Static assets (JS/CSS/fonts/images with hashed filenames): cache forever, safe because the filename changes on content change. HTML/API responses: cache per actual freshness need — short TTL with revalidation for frequently-changing data, longer for rarely-changing data, explicit no-cache for user-specific sensitive data.

## When NOT to over-optimize

A low-traffic internal tool or Prototype-profile project doesn't need aggressive code-splitting/CDN/caching infrastructure — the effort-to-value ratio is poor. Reserve full WE1-WE10 discipline for Production+ profiles and public-facing, traffic-significant pages.
