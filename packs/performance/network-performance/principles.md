# Principles — Network Performance Pack

- **NP1 — Serve over HTTP/2 or HTTP/3** wherever the hosting platform/CDN supports it — multiplexing and reduced head-of-line blocking benefit nearly every page with minimal effort (usually a hosting/CDN configuration, not a code change).
- **NP2 — Compress all text-based responses** (HTML, CSS, JS, JSON, SVG) with Brotli (preferred) or gzip (fallback), applied at the server/CDN level.
- **NP3 — Reduce connection setup cost for known-critical origins** via `<link rel="preconnect">` (and `dns-prefetch` as a lighter-weight fallback) for third-party origins the page definitely needs (CDN, API, font provider).
- **NP4 — Use CDN/edge delivery for static assets**, minimizing the physical distance (and thus latency) between the user and the server for content that doesn't require origin compute.
- **NP5 — Set resource priority hints deliberately**: `fetchpriority="high"` for LCP-critical resources, `fetchpriority="low"` for non-critical ones, `rel="preload"` for resources the browser wouldn't discover early enough on its own.
- **NP6 — Design for intermittent/poor connectivity**: requests have sensible timeouts, retries with backoff, and the UI communicates network state (offline, slow, retrying) rather than hanging silently.
- **NP7 — Cache and serve previously-fetched content instantly where feasible** (service worker cache, HTTP cache), updating in the background rather than blocking the UI on a fresh network round trip for unchanged content.
- **NP8 — Minimize request waterfalls**: avoid resources that can only be discovered after another resource loads and executes (e.g. a CSS file that imports another CSS file, or JS that dynamically imports before starting a data fetch) when they could be requested in parallel from the start.
