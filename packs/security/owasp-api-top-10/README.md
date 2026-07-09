# Pack: OWASP API Security Top 10

**Domain:** Security · **Authority:** Level 1 (official industry-standard security reference) · **Version:** 1.0.0

Operationalizes the OWASP API Security Top 10 — risks specific to API-first architectures (REST/GraphQL/RPC) that the general web Top 10 doesn't fully cover: object/property-level authorization at the API layer, resource exhaustion, mass assignment, and unsafe API consumption.

Independent distillation; not affiliated with or endorsed by OWASP. Normative source: owasp.org — see [references.md](references.md).

## When to load

- Designing or reviewing any REST/GraphQL/RPC API.
- Reviewing endpoints that accept object updates (mass assignment risk).
- Rate limiting and resource-consumption design.
- Third-party/partner API integrations (both as provider and consumer).

## The Top 10 (2023 edition, index)

| # | Category | One-line |
|---|----------|----------|
| API1 | Broken Object Level Authorization | Object access not scoped to the requesting user |
| API2 | Broken Authentication | Weak/missing auth on API endpoints |
| API3 | Broken Object Property Level Authorization | Individual fields exposed/writable beyond intent |
| API4 | Unrestricted Resource Consumption | No limits on requests, payload size, or costly operations |
| API5 | Broken Function Level Authorization | Privileged endpoints reachable without proper role checks |
| API6 | Unrestricted Access to Sensitive Business Flows | Automatable abuse of legitimate flows (scalping, spam) |
| API7 | Server Side Request Forgery | API triggers server-side fetches to attacker-chosen URLs |
| API8 | Security Misconfiguration | API-specific config gaps (CORS, verbose specs, debug endpoints) |
| API9 | Improper Inventory Management | Undocumented/old API versions still reachable |
| API10 | Unsafe Consumption of APIs | Blind trust of third-party API responses |

## Related packs

[owasp-top-10](../owasp-top-10/README.md) · [owasp-asvs](../owasp-asvs/README.md) · [backend/rest](../../backend/rest/README.md) · [backend/graphql](../../backend/graphql/README.md)
