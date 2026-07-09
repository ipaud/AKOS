# Security Score (0–100)

Safety-floor dimension. Any CRITICAL finding caps the score at 59 (Blocked), per [core/scoring-model.md](../core/scoring-model.md).

## Inputs

- [owasp-top-10](../packs/security/owasp-top-10/scoring-rubric.md) — primary
- [owasp-api-top-10](../packs/security/owasp-api-top-10/scoring-rubric.md) — APIs
- [owasp-asvs](../packs/security/owasp-asvs/scoring-rubric.md) — verification level
- [nist-ssdf](../packs/security/nist-ssdf/scoring-rubric.md) — process
- [supabase](../packs/backend/supabase/scoring-rubric.md) — RLS

## Deductions

- Exploitable by anonymous attacker (SQLi, broken authz, RLS off on user data, service_role in client, SSRF to internal): −40 (CRITICAL)
- Exploitable by authenticated user against others' data (IDOR, stored XSS): −25 (CRITICAL)
- Plaintext/weak password storage: −25 (CRITICAL)
- Verbose errors, no brute-force protection, unpatched critical CVE: −10 (HIGH)
- Missing threat model, thin logging: −4-6 (MEDIUM)
- Missing MFA, unpinned CI deps: −2 (LOW)

## Hard caps

- Any CRITICAL → ≤ 59 (Blocked).
- No dependency scanning at all → cap 69.

## Interpretation

- **95** — no known exploitable path, defense-in-depth, logging solid.
- **80** — solid floor, a few HIGHs scheduled.
- **65** — floor mostly holds, notable gaps; MVP-acceptable only.
- **≤59** — an exploitable path exists; BLOCKED except pure local Prototype.

For this owner: security + Supabase/RLS score is a mandatory gate before any deployed project ships.
