# Mental Models — Network Performance Pack

## The connection setup waterfall

DNS lookup → TCP handshake → TLS handshake → first request sent → first byte received. Each step is a round trip (or more); on a connection with 100ms latency, this waterfall alone can consume 300-400ms+ before any content-relevant byte arrives. `preconnect`/`dns-prefetch` hints let the browser start this waterfall for a known-needed origin before the resource request is actually discovered, hiding the cost behind other work.

## HTTP/2 and HTTP/3 multiplexing

HTTP/1.1 allowed a limited number of parallel requests per connection (browsers typically capped around 6 per origin), making request count itself a bottleneck (hence bundling). HTTP/2 multiplexes many requests over one connection; HTTP/3 (built on QUIC/UDP) further removes head-of-line blocking at the transport level, so a lost packet doesn't stall unrelated streams. Under HTTP/2+, many small cacheable resources loaded in parallel is often *faster* than one large bundle, not slower.

## Compression as a nearly-free win

Text-based resources (HTML, CSS, JS, JSON) compress extremely well (often 60-80% size reduction) with essentially no downside — Brotli (better ratio) or gzip (universal support) applied at the server/CDN level costs nothing at request time (pre-compressed at build/deploy) and meaningfully shrinks transfer size and time.

## Resource priority hints

Browsers use heuristics to decide what to fetch first, but developers can override them: `fetchpriority="high"` for the LCP-critical resource, `fetchpriority="low"` for below-the-fold images, `rel="preload"` for resources the browser wouldn't otherwise discover early enough. Getting priority hints right means the *critical path* resources arrive first even when many resources are requested near-simultaneously.

## Offline-first as a network-latency escape hatch

A service worker cache (or equivalent offline-storage strategy) that serves previously-fetched content instantly, then updates in the background, removes network latency from the critical path entirely for repeat visits — the fastest network request is still the one never made, and the second-fastest is the one served from local cache while a background update happens invisibly.
