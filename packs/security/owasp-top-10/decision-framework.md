# Decision Framework — OWASP Top 10 Pack

## Profile-adjusted rigor (per reasoning profile)

| Category | Prototype | Startup MVP | Production | Enterprise |
|----------|-----------|-------------|------------|------------|
| A01 Access control | Basic auth check | Full server-side authz | Full + tested | Full + audited |
| A02 Crypto | HTTPS if public | HTTPS + hashed passwords | Full OW2/OW7 | + key rotation policy |
| A03 Injection | Parameterized queries (never optional, cheap to do right) | Same | Same + SAST scanning | Same + pen test |
| A06 Dependencies | Best effort | CI audit | Blocking CI audit | + license/SBOM tracking |
| A09 Logging | Minimal | Auth events logged | Full OW16 | + SIEM integration |

★-marked rules in [engineering-rules.md](engineering-rules.md) hold even at Prototype — they're cheap to do right from the start and expensive to retrofit (parameterized queries, password hashing cost nothing extra to do correctly the first time).

## Prioritizing remediation when everything can't be fixed at once

1. Anything currently exploitable with public/anonymous access (unauthenticated A01/A03) — fix immediately, treat as an incident if in production.
2. Authenticated-user-exploitable issues (IDOR against other users' data, stored XSS) — fix before next release.
3. Requires insider/elevated access to exploit — schedule, don't block.
4. Best-practice gaps with no known exploitable path yet (missing security headers, verbose but non-sensitive errors) — backlog.

## Build vs. buy for security controls

Authentication, session management, and cryptographic primitives: use established, audited libraries/services (never hand-roll). Rate limiting, input validation: light custom code is fine, reviewed carefully. The bar rises with the stakes — payment handling and access control for regulated data lean harder toward established, audited solutions (managed auth providers, established RBAC/ABAC libraries) over custom implementations.
