# Prompt Fragments — OWASP API Security Pack

## Fragment: build-mode constraint block

```text
Apply OWASP API Security constraints (AKOS L1) to any API endpoint:
- Object-level authorization checked on every object-scoped call
  (ownership/scope verified, not assumed).
- All endpoints authenticated except an explicit reviewed public allowlist.
- Request/response fields explicitly allowlisted per role via DTOs; never
  bind entire request bodies to internal models or serialize them wholesale.
- Privileged endpoints check role independently of object-level checks.
- Rate limits, payload size limits, and bounded pagination on every endpoint.
- Anti-automation controls on high-value flows (signup, checkout,
  redemption, password reset).
- Server-side requests from API input allowlist-validated (SSRF).
- CORS scoped to actual origins; never wildcard + credentials.
- Third-party API responses schema-validated before use.
```

## Fragment: API review lens

```text
Review this API against the OWASP API Security Top 10:
API1 — object-level authz on every object-scoped endpoint?
API2 — authentication required everywhere except an explicit allowlist?
API3 — fields explicitly allowlisted, or mass-assignment possible?
API4 — rate limits, payload caps, bounded pagination present?
API5 — privileged endpoints check role independently?
API6 — anti-automation on high-value flows?
API7 — SSRF allowlisting on server-side requests from API input?
API8 — CORS scoped correctly; no debug endpoints exposed?
API9 — inventory current; deprecated versions decommissioned?
API10 — third-party responses validated before use?
Report findings with the specific endpoint and severity (CRITICAL for
object/function-level authz gaps reachable by any authenticated user).
```

## One-liner

```text
API security: object-level, function-level, and property-level
authorization checked independently and on every call; explicit field
allowlisting (no mass assignment); rate limits + payload caps + bounded
pagination everywhere; anti-automation on high-value flows; scoped CORS;
validated third-party responses; real API inventory with real decommissioning.
```
