# Principles — OWASP ASVS Pack

- **AS1 — Choose a target level explicitly, before building.** Every application (or major component) has a stated ASVS level target, derived from data sensitivity and attacker motivation, recorded where the team can reference it.
- **AS2 — Security controls are centralized, not duplicated.** Authentication, authorization, validation, and encoding logic live in shared, reusable components — not reimplemented per endpoint/feature.
- **AS3 — Trust boundaries are explicitly documented**, especially at L2+ — where does data cross from less-trusted to more-trusted context, and what control sits at that exact boundary.
- **AS4 — Session management is server-authoritative.** Session state, expiry, and invalidation are controlled server-side; client-supplied session claims are never trusted without server verification.
- **AS5 — Access control decisions cannot be bypassed by direct object/URL manipulation** (ties to [OWASP API A01](../owasp-api-top-10/principles.md)), and are enforced on every layer a request could reach (API, direct DB access if applicable, admin tooling).
- **AS6 — All input is validated, canonicalized, and encoded for its output context** — consistent with [OWASP Top 10 A03](../owasp-top-10/principles.md), applied as a first-class architectural control, not per-field ad hoc.
- **AS7 — Cryptographic operations use vetted, current libraries and algorithms**, with key management (rotation, storage, access) explicitly designed, not incidental.
- **AS8 — Errors and logs never leak sensitive data**, and logs are sufficient to reconstruct security-relevant events for incident investigation.
- **AS9 — Business logic workflows are explicitly modeled** (state machines, sequence requirements, rate/volume limits per workflow step) so out-of-order or excessive-repetition abuse is a defined, checkable property — not an afterthought.
- **AS10 — Configuration is verified for each environment**, not assumed correct because it worked in one — L2+ requires environment-specific configuration review as part of release.
