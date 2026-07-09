# Scoring Rubric — OWASP Top 10 Pack

Primary input to [scoring/security-score.md](../../../scoring/security-score.md).

## Deductions (from 100)

| Finding | Deduction |
|---------|-----------|
| Exploitable by anonymous/unauthenticated attacker (SQLi, broken authz on public endpoint, SSRF to internal services) | −40 each (CRITICAL — caps score at Blocked band) |
| Exploitable by authenticated user against other users' data (IDOR, stored XSS) | −25 (CRITICAL) |
| Plaintext/weakly-hashed password storage | −25 (CRITICAL) |
| Verbose errors leaking internals | −10 (HIGH) |
| No brute-force protection on auth endpoints | −10 (HIGH) |
| Known critical/high CVE in production dependency, unpatched | −10 (HIGH) |
| Missing threat model on a sensitive flow | −6 (MEDIUM) |
| Missing security headers, default (but non-exploited) credentials in non-prod | −4 (MEDIUM) |
| Logging gaps on security events | −4 (MEDIUM) |
| Missing MFA option, unpinned CI dependencies | −2 (LOW) |

## Hard caps

- Any CRITICAL finding: score ≤ 59 (Blocked band), per [core/scoring-model.md](../../../core/scoring-model.md).
- No dependency vulnerability scanning at all: cap 69.

## Anchors

- **95** — no known exploitable path, full defense-in-depth, logging solid.
- **80** — solid floor, a few HIGH findings scheduled.
- **65** — floor mostly holds, notable gaps (no MFA, thin logging) — acceptable pre-PMF only.
- **≤59** — an exploitable path exists; BLOCKED everywhere except Prototype.
