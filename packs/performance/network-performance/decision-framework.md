# Decision Framework — Network Performance Pack

## Bundling strategy under HTTP/2+ vs HTTP/1.1

If the hosting/CDN guarantees HTTP/2+ for all users (verify — some corporate/legacy networks or old clients may still negotiate HTTP/1.1): prefer many small, cacheable, well-scoped bundles over one giant bundle — better cache granularity, better parallelism. If HTTP/1.1 support must be assumed broadly: some consolidation still helps due to per-connection request limits, though this is an increasingly rare constraint.

## When to invest in offline support

Full offline-first (service worker precaching, background sync, offline queue for mutations) is worth the complexity for: apps with a meaningful mobile/poor-connectivity user base, apps where users expect continuity (note-taking, forms), or PWA-positioned products. Skip it for internal tools or apps only ever used on stable office/home networks — the complexity isn't repaid.

## CDN choice and configuration

Use a CDN with edge locations matching the actual user base's geography; configure cache rules per content type (static assets: long TTL; API responses: per freshness need, often bypassed or very short TTL for personalized data). For Prototype/MVP profiles, a platform's built-in CDN (Vercel, Netlify, Cloudflare Pages, etc.) is sufficient — custom CDN configuration is a Production+ concern.

## Retry/backoff strategy

Transient network failures (timeout, 5xx, connection reset) warrant automatic retry with exponential backoff (and jitter, to avoid synchronized retry storms across many clients) up to a small bounded attempt count. Non-transient failures (4xx client errors, validation failures) should never be retried automatically — retrying a malformed request just wastes another round trip and delays the user seeing the real error.

## Preconnect budget

Preconnect is not free — each preconnected origin consumes a connection the browser reserves speculatively. Limit preconnect to the 2-4 most critical third-party origins (the ones on the actual critical rendering path); preconnecting every third-party script's origin dilutes the benefit and can itself cost bandwidth/battery.
