# Review Checklist — OWASP API Security Pack

Floor items (★) block in every profile beyond Prototype.

## Critical ★

- [ ] Object-level authorization checked on every object-scoped endpoint call. (AP1)
- [ ] All endpoints require authentication except an explicit reviewed public allowlist. (AP2)
- [ ] Request/response fields explicitly allowlisted per role; no wholesale model binding. (AP3)
- [ ] Privileged endpoints check role independently of object-level checks. (AP5)
- [ ] Server-side requests from API input are allowlist-validated (SSRF). (AP7)

## High

- [ ] Rate limits, payload size limits, and bounded pagination on every endpoint. (AP4)
- [ ] Anti-automation controls on high-value business flows. (AP6)
- [ ] CORS scoped to actual origins; no wildcard + credentials. (AP8)

## Medium

- [ ] API inventory current; deprecated versions actually decommissioned. (AP9)
- [ ] Third-party API responses schema-validated before use. (AP10)
