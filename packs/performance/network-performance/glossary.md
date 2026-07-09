# Glossary — Network Performance Pack

- **DNS lookup / TCP handshake / TLS handshake** — the sequential connection-setup steps preceding any content request.
- **HTTP/2 / HTTP/3** — modern HTTP protocol versions supporting multiplexed (HTTP/2) or transport-level non-blocking (HTTP/3, via QUIC) parallel requests over one connection.
- **Multiplexing** — sending multiple requests/responses concurrently over a single connection.
- **Head-of-line blocking** — a delay where one stalled request/packet blocks unrelated ones behind it.
- **Brotli / gzip** — text-compression algorithms applied to HTTP responses.
- **CDN (Content Delivery Network)** — geographically-distributed edge servers caching content closer to users.
- **`preconnect` / `dns-prefetch`** — resource hints starting connection setup for a known-needed origin early.
- **`fetchpriority`** — an HTML/fetch attribute hinting a resource's relative loading priority.
- **Service worker** — a script enabling offline caching, background sync, and request interception.
- **Exponential backoff with jitter** — a retry strategy increasing wait time between attempts, randomized to avoid synchronized retry storms.
