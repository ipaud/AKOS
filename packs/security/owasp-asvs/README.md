# Pack: OWASP ASVS (Application Security Verification Standard)

**Domain:** Security · **Authority:** Level 1 (official industry-standard verification framework) · **Version:** 1.0.0

Operationalizes ASVS's tiered verification model (Levels 1-3) as a way to calibrate *how much* security verification an application needs, and its broader control catalog (beyond the Top 10's "most common risks" framing) covering architecture, session management, access control, and more systematically.

Independent distillation; not affiliated with or endorsed by OWASP. Normative source: owasp.org — see [references.md](references.md).

## When to load

- Deciding how rigorous security verification should be for a given application (mapping to [reasoning profiles](../../../core/reasoning-profiles.md)).
- Enterprise/regulated-industry security review needing a structured, auditable standard.
- Building a security requirements checklist broader than "the Top 10."

## The three levels (index)

| Level | Target | Rigor |
|-------|--------|-------|
| L1 | Any application handling any sensitive data | Baseline: fully penetration-testable, opportunistic-attacker resistant |
| L2 | Applications handling significant business/personal/financial data | Standard: resistant to skilled, motivated attackers with time |
| L3 | High-value applications (critical infrastructure, high-value transactions) | Advanced: resistant to sophisticated, well-resourced attackers |

## Related packs

[owasp-top-10](../owasp-top-10/README.md) · [owasp-api-top-10](../owasp-api-top-10/README.md) · [nist-ssdf](../nist-ssdf/README.md)
