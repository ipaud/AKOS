# Engineering Rules — Network Performance Pack

- NW1. HTTP/2 or HTTP/3 is enabled at the hosting/CDN layer for all production traffic.
- NW2. All text-based responses (HTML, CSS, JS, JSON, SVG, fonts where applicable) are served with Brotli or gzip compression.
- NW3. Critical third-party origins (font provider, primary API, CDN if on a separate origin) use `<link rel="preconnect">`; less-critical-but-needed origins use `dns-prefetch`.
- NW4. Static assets (images, JS, CSS, fonts) are served via a CDN/edge network, not directly from the application origin server.
- NW5. The LCP-candidate resource and other critical-path resources use `fetchpriority="high"` or `rel="preload"`; below-the-fold/non-critical resources use `fetchpriority="low"` or default priority.
- NW6. Network requests have explicit timeouts and retry-with-backoff logic for transient failures; the UI surfaces offline/slow-network/retrying states rather than hanging with no feedback.
- NW7. Repeat-visit critical assets are served from cache (HTTP cache or service worker) with background revalidation, rather than always blocking on a fresh network round trip.
- NW8. Resource loading is audited for avoidable serial waterfalls (a resource discoverable only after another resource loads/executes when it could be requested in parallel from the initial HTML).
