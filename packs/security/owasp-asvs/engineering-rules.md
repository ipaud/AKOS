# Engineering Rules — OWASP ASVS Pack

- AV1. Every application/service has a documented target ASVS level (L1/L2/L3), recorded in a discoverable location (README, security doc, `.akos/config.md`).
- AV2. Authentication and authorization are implemented via a single canonical mechanism (shared middleware/guard/library) reused across all endpoints — not reimplemented per feature.
- AV3 (L2+). A trust-boundary diagram or equivalent documentation exists, naming the control at each boundary crossing.
- AV4. Session tokens are generated server-side with sufficient entropy, expire server-side on a defined policy, and are invalidated server-side on logout/password change (overlaps [OW12](../owasp-top-10/engineering-rules.md)).
- AV5. Authorization checks occur on every layer capable of independently reaching protected data (API layer, and database layer via RLS/row-level policies where applicable) — not solely at the API layer.
- AV6. All input validation uses an allowlist approach (define what's valid) over a denylist approach (define what's forbidden) wherever the valid value space is enumerable.
- AV7 (L2+). Cryptographic key management is documented: where keys are stored, how they're rotated, who/what can access them.
- AV8. Logs capture sufficient detail to reconstruct a security incident timeline (who, what, when, from where) without containing secrets or full PII payloads.
- AV9 (L2+). At least one critical business workflow has a documented state-machine/sequence model verifying out-of-order and excessive-repetition abuse are prevented or rate-limited.
- AV10 (L2+). Environment-specific configuration (CORS, debug settings, feature flags, credentials) is reviewed and diffed as part of the release process, not assumed consistent across environments.
