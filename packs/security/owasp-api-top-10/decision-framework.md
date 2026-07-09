# Decision Framework — OWASP API Security Pack

## Authorization layering decision

For every endpoint, explicitly answer three separate questions (don't let one substitute for another):
1. **Function-level:** is this caller allowed to hit this endpoint at all (role check)?
2. **Object-level:** is this caller allowed to access *this specific* object (ownership/scope check)?
3. **Property-level:** which fields can this caller read, and which can they write, on this object?

A design that only answers question 1 and assumes 2/3 follow automatically is the most common real-world API breach pattern.

## Rate limiting strategy

| Endpoint type | Limit strategy |
|----------------|-----------------|
| Authentication (login, password reset) | Strict per-IP and per-account limits, exponential backoff |
| High-value business flows (checkout, redemption) | Per-account limits + anomaly detection |
| General read endpoints | Generous per-API-key/per-user limits |
| Expensive computation (search, reports, GraphQL deep queries) | Cost-based limiting (query complexity budget), not just request count |

## Public API vs. internal API posture

Public/partner-facing APIs: full AP1-AP10 discipline, versioned with a deprecation policy, documented and monitored for shadow-endpoint drift. Internal-only APIs: still require AP1/AP2/AP5 (internal doesn't mean untrusted — internal services get compromised too) but may relax AP4/AP6 rate limiting to match legitimate internal traffic patterns.

## GraphQL-specific considerations

Field-level authorization (API3) is especially important in GraphQL since a single query can traverse many object types; query depth/complexity limiting (API4) prevents a single malicious query from causing a denial-of-service via nested resolvers. See [backend/graphql](../../backend/graphql/decision-framework.md) for implementation specifics.
