# Engineering Rules — OWASP API Security Pack

- AP1 ★. Every endpoint accepting an object identifier verifies the authenticated requester's authorization over that specific object before returning/mutating it — checked on every call, including nested/related-object lookups.
- AP2 ★. Every API endpoint (internal, partner, and public) requires authentication; no endpoint is reachable unauthenticated except an explicit, reviewed public allowlist (e.g. health check, public content).
- AP3 ★. Request/response schemas explicitly allowlist fields per role (DTOs/serializers); internal model objects are never directly bound to request bodies or serialized wholesale to responses.
- AP4. Every endpoint enforces: a rate limit, a maximum request payload size, bounded pagination (max page size), and a query/execution timeout.
- AP5 ★. Privileged/administrative endpoints check the caller's role/permission explicitly and independently of any object-level check.
- AP6. High-value-to-abuse flows (signup, checkout, redemption, password reset) have rate limiting and/or anomaly-based anti-automation controls.
- AP7 ★. Any server-side outbound request whose target is influenced by API input is allowlist-validated, matching [OW17](../owasp-top-10/engineering-rules.md).
- AP8. CORS configuration is scoped to the actual set of needed origins; wildcard origin is never combined with credentialed requests.
- AP9. A maintained inventory records every deployed API version and its status (active/deprecated/decommissioned); deprecated versions are actually removed from deployment, not merely undocumented.
- AP10. Third-party API responses are validated against an expected schema before being used; malformed or unexpected responses fail safely (logged, not silently trusted or crash-propagated).
