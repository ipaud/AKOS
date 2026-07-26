# Security Knowledge Graph

How the security packs (and their neighbors) relate. Parent: [knowledge-graph](knowledge-graph.md).

## The layers

- **Common web risks:** [OWASP Top 10](../packs/security/owasp-top-10/README.md).
- **API-specific risks:** [OWASP API Top 10](../packs/security/owasp-api-top-10/README.md).
- **Identity and session design:** [auth](../packs/security/auth/README.md) (who the user is, and how that claim stays bound).
- **What is held about a person:** [privacy](../packs/security/privacy/README.md) (a different question about the same data — not a security pack).
- **Verification depth:** [OWASP ASVS](../packs/security/owasp-asvs/README.md) (L1/L2/L3 calibration).
- **Process/lifecycle:** [NIST SSDF](../packs/security/nist-ssdf/README.md).
- **The agent surface:** [agent-security](../packs/ai-engineering/agent-security/README.md) (a model that reads external content and then acts).
- **Stack-specific application:** [Supabase RLS](../packs/backend/supabase/README.md) + [personal supabase-rules](../packs/personal/pau-avila/supabase-rules.md).

## Key concept edges

- **Broken access control (A01)** ([Top 10](../packs/security/owasp-top-10/principles.md)) ↔ **object/function/property-level authz** ([API Top 10](../packs/security/owasp-api-top-10/mental-models.md)) ↔ **RLS as the API's authz layer** ([Supabase](../packs/backend/supabase/philosophy.md)) ↔ **centralized access control** ([ASVS AS5](../packs/security/owasp-asvs/principles.md)).
- **SSRF (A10)** ([Top 10](../packs/security/owasp-top-10/principles.md)) ↔ **API7** ([API Top 10](../packs/security/owasp-api-top-10/principles.md)) — identical discipline, allowlist server-side outbound.
- **Secure config (A05)** ([Top 10](../packs/security/owasp-top-10/principles.md)) ↔ **config from environment** ([Twelve-Factor TF1](../packs/architecture/twelve-factor-app/principles.md)) ↔ **PS/PW config verification** ([SSDF](../packs/security/nist-ssdf/principles.md)).
- **Verification level (ASVS)** ↔ **reasoning profile** — Prototype/MVP ≈ L1, Production ≈ L2, Enterprise ≈ L3 ([reasoning-profiles](../core/reasoning-profiles.md)).
- **Authentication failures (A07)** ([Top 10](../packs/security/owasp-top-10/principles.md)) ↔ **the flow that produces them** ([auth AU1–AU60](../packs/security/auth/engineering-rules.md)) ↔ **verification requirements** ([ASVS](../packs/security/owasp-asvs/README.md)). The Top 10 says authentication failed; the auth pack says which transition failed.
- **Access control (A01)** ↔ **who the token says you are** ([auth P1](../packs/security/auth/principles.md)) — authorization is only as sound as the identity it reads, and the two are separate decisions with separate tokens.
- **Cryptographic failures (A02)** ↔ **what you never stored** ([privacy P3](../packs/security/privacy/principles.md)) — encryption reduces the consequence of holding data; minimization removes it. Minimization is the cheaper control and the one applied earlier.
- **Data at rest** ([Supabase RLS](../packs/backend/supabase/README.md)) ↔ **retention as an enforced job** ([privacy PR20](../packs/security/privacy/engineering-rules.md)) — access control decides who reads a row, retention decides whether the row still exists to read.

## The floor

All security packs feed the [security-as-a-floor node](knowledge-graph.md): non-negotiable per [constitution Art. 2](../core/constitution.md), enforced by [security-reviewer](../agents/security-reviewer.md) and [database-reviewer](../agents/database-reviewer.md), mandatory before any deployed project ships ([pau-avila principle 6](../packs/personal/pau-avila/principles.md)). All L1 authority except SSDF process practices which are L1 (NIST standard).
