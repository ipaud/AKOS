# Glossary — OWASP API Security Pack

- **Object-level authorization** — verifying a caller may access a *specific* record, not just that they're authenticated.
- **Function-level authorization** — verifying a caller may call a *specific endpoint* at all (role/permission check).
- **Property-level authorization** — verifying which fields on a record a caller may read/write.
- **Mass assignment** — binding an entire request body to a model without allowlisting permitted fields.
- **Shadow API** — an undocumented, unmonitored, live API endpoint.
- **Zombie API** — a deprecated API version left running and unpatched.
- **Business-flow abuse** — automated exploitation of a legitimate feature (scalping, spam signups, coupon farming) at scale.
- **DTO (Data Transfer Object)** — an explicit schema defining exactly which fields cross an API boundary.
- **Query complexity limiting** — bounding GraphQL (or similar) query cost/depth to prevent resource-exhaustion attacks.
