# Scoring Rubric — OWASP API Security Pack

Feeds [scoring/security-score.md](../../../scoring/security-score.md) alongside [owasp-top-10](../owasp-top-10/scoring-rubric.md).

| Finding | Deduction |
|---------|-----------|
| Object-level authz missing on any object-scoped endpoint | −40 (CRITICAL) |
| Unauthenticated access to a non-public endpoint | −40 (CRITICAL) |
| Mass assignment allowing privilege/field escalation | −25 (CRITICAL) |
| Privileged endpoint missing independent role check | −25 (CRITICAL) |
| SSRF via API input | −25 (CRITICAL) |
| No rate limiting/payload caps on public endpoints | −10 (HIGH) |
| No anti-automation on high-value flows | −10 (HIGH) |
| CORS wildcard + credentials | −10 (HIGH) |
| Unvalidated third-party API response consumption | −6 (MEDIUM) |
| Undecommissioned deprecated API version live | −6 (MEDIUM) |

Hard cap: any CRITICAL finding → score ≤59 (Blocked band).

Anchors: **95** layered authz verified at all three levels, rate-limited, inventoried · **80** solid with a MEDIUM gap or two · **65** missing rate limits/anti-automation but authz sound · **≤59** an authz or SSRF gap exists — BLOCKED.
