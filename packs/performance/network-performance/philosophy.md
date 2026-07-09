# Philosophy — Network Performance Pack

## Latency, not just bandwidth, is the real enemy

Modern connections often have plenty of bandwidth but fixed, physics-bound latency (the speed of light over the distance to the server, plus per-hop processing). A page making many sequential round trips (DNS lookup, TCP handshake, TLS handshake, then request/response, then discovering and requesting the next resource) pays that latency cost repeatedly, even on a fast connection — this is why reducing round trips and connection setup overhead often matters more than compressing an already-small payload further.

## Every connection setup is a tax paid before any content arrives

DNS resolution, TCP handshake, and TLS negotiation all happen before the first byte of actual content can be requested — on a high-latency connection (mobile, long-distance), this setup tax alone can exceed a full second before anything useful starts downloading. Techniques that avoid or amortize this cost (connection reuse, preconnect, HTTP/2+ multiplexing) are disproportionately valuable precisely because they eliminate repeated fixed costs, not variable ones.

## Design for the network you don't control

Developers typically build and test on fast, stable connections; real users are on a huge diversity of network conditions — spotty mobile signal, high-latency satellite, shared congested WiFi, intermittent connectivity. Performance work that only accounts for the developer's own network conditions systematically underestimates real-world experience; resilience to poor/intermittent networks (offline support, retry logic, graceful degradation) is a performance requirement, not just a UX nicety.

## Fewer, smaller, more parallel-friendly requests

The historical practice of bundling everything into one giant file to minimize request count made sense under HTTP/1.1's connection-per-request limits; HTTP/2 and HTTP/3's multiplexing changed the calculus — many small, cacheable, parallel-loadable resources can now outperform one giant bundle, because a single-byte change no longer invalidates the whole cache and resources can load concurrently over one connection.
