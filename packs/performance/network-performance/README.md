# Pack: Network Performance

**Domain:** Performance · **Authority:** Level 1 (web platform / HTTP standards-adjacent performance practice) · **Version:** 1.0.0

Operationalizes network-layer performance: connection setup cost (DNS/TLS), HTTP/2/3 multiplexing, resource prioritization, compression, and offline/poor-network resilience — the layer beneath rendering that determines how fast bytes actually arrive.

Independent distillation; not affiliated with or endorsed by any standards body. See [references.md](references.md).

## When to load

- Diagnosing slow Time to First Byte or slow resource loading independent of rendering.
- API/asset delivery architecture decisions (CDN, compression, protocol).
- Designing for poor-network/offline resilience (mobile, low-connectivity users).

## Related packs

[core-web-vitals](../core-web-vitals/README.md) · [web-dev](../web-dev/README.md) · [backend/rest](../../backend/rest/README.md) · [architecture/twelve-factor-app](../../architecture/twelve-factor-app/README.md)
