# Mental Models — OWASP Top 10 Pack

## Trust boundaries

Every point where data crosses from a less-trusted context to a more-trusted one (user input → server, third-party API response → your logic, uploaded file → your storage, another microservice → yours) is a trust boundary. Security controls belong *at* the boundary, applied to everything crossing it, not sprinkled ad hoc downstream where it's easy to forget a path.

## Least privilege

Every account, service, API key, and database role should hold the minimum permissions needed for its actual job — not because compromise is expected, but because when it inevitably happens (a leaked key, a compromised dependency), least privilege bounds the blast radius. A backend service account with full database admin rights turns a single SQL injection into a total breach; the same injection against a role scoped to one table is contained.

## Defense in depth

No single layer (input validation, or authentication, or a firewall) is assumed sufficient alone. Layer independent controls so that one failure doesn't cascade into full compromise — parameterized queries *and* least-privilege DB roles *and* WAF rules, each catching what the others might miss.

## Attack surface

Everything reachable by an attacker: every endpoint, every input field, every third-party integration, every dependency, every exposed service. Reducing attack surface (removing unused endpoints, disabling unnecessary services, minimizing dependencies) is often cheaper and more durable than hardening a large surface.

## Fail closed, not open

When a security check errors or can't complete (auth service down, permission check throws), the safe default is to deny access, not grant it. Systems that fail open under error conditions turn availability problems into security breaches.
