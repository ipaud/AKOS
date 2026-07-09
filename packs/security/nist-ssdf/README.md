# Pack: NIST SSDF (Secure Software Development Framework)

**Domain:** Security · **Authority:** Level 1 (official US government standard, SP 800-218) · **Version:** 1.0.0

Operationalizes NIST's Secure Software Development Framework: secure development practices organized by lifecycle phase (Prepare, Protect, Produce, Respond) — process-level discipline complementing OWASP's code/application-level controls.

Independent distillation; not affiliated with or endorsed by NIST. Normative source: nist.gov — see [references.md](references.md).

## When to load

- Establishing or reviewing a team's secure-development lifecycle process (not just point-in-time code review).
- Supply-chain security (dependency provenance, build integrity).
- Vulnerability response process design.
- Any Enterprise-profile or regulated/compliance-adjacent work.

## The four practice groups (index)

| Group | Focus |
|-------|-------|
| PO (Prepare the Organization) | Security requirements, roles, tooling defined before development starts |
| PS (Protect the Software) | Protecting code/artifacts from unauthorized access and tampering |
| PW (Produce Well-Secured Software) | Secure design, secure coding, testing, review practices |
| RV (Respond to Vulnerabilities) | Identifying, triaging, and remediating vulnerabilities post-release |

## Related packs

[owasp-top-10](../owasp-top-10/README.md) · [owasp-asvs](../owasp-asvs/README.md) · [architecture/twelve-factor-app](../../architecture/twelve-factor-app/README.md) · [devops/ci-cd](../../devops/ci-cd/README.md)
