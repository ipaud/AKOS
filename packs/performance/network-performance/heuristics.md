# Heuristics — Network Performance Pack

- **The protocol check:** inspect response headers/DevTools network panel — is the site served over `h2`/`h3`, or still `http/1.1`? The latter is a quick, usually infrastructure-level win to flag.
- **The compression check:** inspect `Content-Encoding` on text responses — is Brotli/gzip applied? An uncompressed JSON API response is an easy, sizeable win.
- **The waterfall shape check:** in DevTools Network panel (waterfall view), look for staircase patterns (resource B only starts after resource A finishes) where B doesn't actually depend on A's content — a parallelization opportunity.
- **The third-party origin count:** count distinct origins the page connects to (fonts, analytics, ads, APIs) — each is a fresh DNS+TCP+TLS cost unless preconnected; consider consolidating or preconnecting the critical ones.
- **The "does this page work offline-ish" test:** throttle to "Slow 3G" or go fully offline in DevTools — does the page fail silently, hang indefinitely, or communicate the network state and degrade gracefully?
- **The priority-hint gap check:** is the LCP-candidate resource marked `fetchpriority="high"`, or is it competing on equal footing with non-critical resources for bandwidth priority?
- **CDN reachability check:** are static assets served from a CDN/edge network, or directly from the origin server regardless of the requesting user's location?
