# Principles — OWASP API Security Pack

- **API1 Object-level authz:** every endpoint returning/mutating a specific object verifies the requester owns or is permitted to access that exact object ID — on every call, not just list endpoints.
- **API2 Authentication:** all API endpoints (including internal/partner APIs) require proper authentication; no endpoint relies on "security through obscurity" of an unguessable URL.
- **API3 Property-level authz:** response payloads and accepted update fields are explicitly allowlisted per role — never serialize/deserialize entire internal models directly.
- **API4 Resource consumption:** every endpoint has limits on rate, payload size, response size, pagination bounds, and execution cost (query complexity, timeouts) — unbounded is never the default.
- **API5 Function-level authz:** privileged/administrative endpoints check role/permission explicitly, independent of object-level checks; never infer admin access from a client-supplied flag.
- **API6 Business-flow abuse:** flows valuable to abuse at scale (signup, checkout, coupon redemption, inventory reservation) have anti-automation controls (rate limits, CAPTCHA where appropriate, anomaly detection).
- **API7 SSRF:** identical discipline to [OWASP Top 10 A10](../owasp-top-10/principles.md) — allowlist server-side outbound requests triggered by API input.
- **API8 Misconfiguration:** CORS scoped to actual needed origins (never wildcard with credentials), API specs/docs not exposing internal-only endpoints publicly, debug/verbose modes disabled in production.
- **API9 Inventory:** every deployed API version is tracked; deprecated versions are actually decommissioned (not just undocumented), staging/internal APIs are not internet-reachable without auth.
- **API10 Safe consumption:** third-party API responses are validated (schema, size, content) before use; failures/malformed responses are handled without propagating trust blindly into your system.
