# Scoring Rubric — OWASP ASVS Pack

Feeds [scoring/security-score.md](../../../scoring/security-score.md) as the verification-completeness dimension.

| Finding | Deduction |
|---------|-----------|
| No stated target level for a Production+ application | −15 (HIGH) |
| Authorization missing at a reachable layer (e.g. no RLS while direct DB access exists) | −25 (CRITICAL) |
| Scattered/duplicated authorization logic with inconsistent enforcement | −15 (HIGH) |
| Denylist-only validation on security-relevant input | −10 (HIGH) |
| No business-logic sequence protection on a financially significant workflow (L2+) | −15 (HIGH) |
| No documented key management (L2+) | −6 (MEDIUM) |
| No trust-boundary documentation (L2+) | −6 (MEDIUM) |
| Configuration not diffed across environments at release | −4 (MEDIUM) |

Anchors: **90** target level stated and substantially met, centralized controls, business logic modeled · **75** solid L1/L2 baseline, a documentation gap or two · **60** ad hoc security posture, no stated level · **<50** authorization bypassable at an alternate layer, BLOCKED for the stated level.
