# Review Checklist — Network Performance Pack

## High

- [ ] HTTP/2 or HTTP/3 enabled in production. (NW1)
- [ ] All text-based responses compressed (Brotli/gzip). (NW2)
- [ ] Static assets served via CDN, not directly from origin. (NW4)
- [ ] Network requests have timeouts and appropriate retry-with-backoff (transient failures only). (NW6)

## Medium

- [ ] Critical third-party origins preconnected; budget limited to 2-4 origins. (NW3)
- [ ] LCP-critical resources use fetchpriority="high"/preload; non-critical use low priority. (NW5)
- [ ] Repeat-visit assets served from cache with background revalidation where feasible. (NW7)
- [ ] Avoidable serial resource-discovery waterfalls minimized. (NW8)

## Low

- [ ] UI communicates offline/slow-network states rather than hanging silently.
