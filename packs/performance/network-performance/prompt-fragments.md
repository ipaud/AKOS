# Prompt Fragments — Network Performance Pack

## Fragment: build-mode constraint block

```text
Apply network performance constraints (AKOS L1):
- Serve over HTTP/2 or HTTP/3; compress all text responses (Brotli/gzip).
- Serve static assets via CDN, not directly from the origin server.
- Preconnect to the 2-4 most critical third-party origins only; use
  dns-prefetch for lower-priority ones.
- Set fetchpriority="high"/preload on LCP-critical resources,
  fetchpriority="low" on non-critical ones.
- Network requests have explicit timeouts and retry-with-backoff for
  transient failures (5xx/timeout) only — never auto-retry 4xx errors.
- Communicate offline/slow-network states in the UI rather than hanging
  silently; cache repeat-visit content with background revalidation
  where feasible.
- Avoid resource-discovery waterfalls where a resource could be
  requested in parallel from the initial HTML instead of after another
  resource loads/executes.
```

## Fragment: review lens

```text
Review this application's network performance:
1. Protocol/compression check — HTTP/2+? Text responses compressed?
2. CDN check — static assets served from edge, or origin-only?
3. Connection-setup check — critical third-party origins preconnected?
   Preconnect budget reasonable (not overused)?
4. Priority-hint check — LCP-critical resources prioritized correctly?
5. Resilience check — timeouts and backoff-retry (transient only) on
   requests? Offline/slow-network states communicated in the UI?
6. Waterfall check — any avoidable serial resource-discovery chains?
```

## One-liner

```text
Network: HTTP/2+, compressed text responses, CDN-served static assets,
targeted preconnect, correct priority hints, timeout+backoff retry on
transient failures only, offline-aware UI, minimized serial waterfalls.
```
