# Scoring Rubric — Network Performance Pack

Feeds [scoring/performance-score.md](../../../scoring/performance-score.md).

| Finding | Deduction |
|---------|-----------|
| HTTP/1.1 only in production (HTTP/2+ available but unused) | −10 (HIGH) |
| No compression on text responses | −10 (HIGH) |
| Static assets served origin-only, no CDN, high-latency user base | −10 (HIGH) |
| No timeout/retry logic, requests can hang indefinitely | −10 (HIGH) |
| Blind retry of 4xx client errors | −4 (MEDIUM) |
| No offline/slow-network UI communication | −4 (MEDIUM) |
| Missing/incorrect priority hints on LCP-critical resources | −4 (MEDIUM) |
| Preconnect overused (diluted budget) or missing on critical origins | −2 (LOW) |
| Avoidable serial resource waterfalls | −2 (LOW) |

Anchors: **90** modern protocol, compressed, CDN-delivered, resilient to poor networks · **75** solid with a gap or two · **60** missing CDN/compression, noticeable on slow connections · **<50** hangs/fails silently on poor networks, no resilience at all.
