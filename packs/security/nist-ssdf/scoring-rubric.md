# Scoring Rubric — NIST SSDF Pack

Feeds [scoring/security-score.md](../../../scoring/security-score.md) as the process/lifecycle dimension, alongside code-level OWASP findings.

| Finding | Deduction |
|---------|-----------|
| No dependency vulnerability scanning in CI (Production+) | −15 (HIGH) |
| No named security ownership at all | −10 (HIGH) |
| No vulnerability disclosure channel (Production+, public-facing) | −10 (HIGH) |
| No threat model on a sensitive feature before implementation | −10 (HIGH) |
| Unprotected CI/build pipeline (unreviewed config changes possible) | −10 (HIGH) |
| No SBOM (Enterprise/regulated) | −6 (MEDIUM) |
| No severity-based patch SLA / ad hoc remediation timing | −6 (MEDIUM) |
| No security requirements documentation | −4 (MEDIUM) |
| Third-party dependencies adopted with no vetting process | −4 (MEDIUM) |

Anchors: **90** full lifecycle discipline, SBOM current, disclosure channel active, threat modeling routine · **75** solid production practice, an Enterprise-tier gap or two · **60** minimal process, dependency scanning only · **<50** no process at all — ownership, scanning, and disclosure all missing.
