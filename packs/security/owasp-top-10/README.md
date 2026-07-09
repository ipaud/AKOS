# Pack: OWASP Top 10

**Domain:** Security · **Authority:** Level 1 (official industry-standard security reference) · **Version:** 1.0.0

Operationalizes the OWASP Top 10 web application security risks as concrete build and review rules — the baseline every web-facing application must clear regardless of reasoning profile beyond Prototype.

Independent distillation; not affiliated with or endorsed by OWASP. Normative source: owasp.org — see [references.md](references.md).

## When to load

- Any code handling user input, authentication, authorization, or sensitive data.
- API and web application security reviews.
- Any Production or Enterprise profile review (mandatory per [security-reviewer agent](../../../agents/security-reviewer.md)).

## The Top 10 (2021 edition, index)

| # | Category | One-line |
|---|----------|----------|
| A01 | Broken Access Control | Users acting outside intended permissions |
| A02 | Cryptographic Failures | Sensitive data exposed via weak/missing crypto |
| A03 | Injection | Untrusted input executed as code/query |
| A04 | Insecure Design | Missing/weak security controls by design, not just bugs |
| A05 | Security Misconfiguration | Insecure defaults, verbose errors, open services |
| A06 | Vulnerable and Outdated Components | Known-vulnerable dependencies in use |
| A07 | Identification and Authentication Failures | Weak auth allowing account compromise |
| A08 | Software and Data Integrity Failures | Unverified updates/CI/serialization trust |
| A09 | Security Logging and Monitoring Failures | Attacks go undetected |
| A10 | Server-Side Request Forgery (SSRF) | App fetches attacker-controlled URLs server-side |

## Related packs

[owasp-api-top-10](../owasp-api-top-10/README.md) · [owasp-asvs](../owasp-asvs/README.md) · [nist-ssdf](../nist-ssdf/README.md) · [backend/supabase](../../backend/supabase/README.md)
