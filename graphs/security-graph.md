# Security Knowledge Graph

How the security packs (and their neighbors) relate. Parent: [knowledge-graph](knowledge-graph.md).

## The layers

- **Common web risks:** [OWASP Top 10](../packs/security/owasp-top-10/README.md).
- **API-specific risks:** [OWASP API Top 10](../packs/security/owasp-api-top-10/README.md).
- **Verification depth:** [OWASP ASVS](../packs/security/owasp-asvs/README.md) (L1/L2/L3 calibration).
- **Process/lifecycle:** [NIST SSDF](../packs/security/nist-ssdf/README.md).
- **Stack-specific application:** [Supabase RLS](../packs/backend/supabase/README.md) + [personal supabase-rules](../packs/personal/pau-avila/supabase-rules.md).

## Key concept edges

- **Broken access control (A01)** ([Top 10](../packs/security/owasp-top-10/principles.md)) ↔ **object/function/property-level authz** ([API Top 10](../packs/security/owasp-api-top-10/mental-models.md)) ↔ **RLS as the API's authz layer** ([Supabase](../packs/backend/supabase/philosophy.md)) ↔ **centralized access control** ([ASVS AS5](../packs/security/owasp-asvs/principles.md)).
- **SSRF (A10)** ([Top 10](../packs/security/owasp-top-10/principles.md)) ↔ **API7** ([API Top 10](../packs/security/owasp-api-top-10/principles.md)) — identical discipline, allowlist server-side outbound.
- **Secure config (A05)** ([Top 10](../packs/security/owasp-top-10/principles.md)) ↔ **config from environment** ([Twelve-Factor TF1](../packs/architecture/twelve-factor-app/principles.md)) ↔ **PS/PW config verification** ([SSDF](../packs/security/nist-ssdf/principles.md)).
- **Verification level (ASVS)** ↔ **reasoning profile** — Prototype/MVP ≈ L1, Production ≈ L2, Enterprise ≈ L3 ([reasoning-profiles](../core/reasoning-profiles.md)).

## The floor

All security packs feed the [security-as-a-floor node](knowledge-graph.md): non-negotiable per [constitution Art. 2](../core/constitution.md), enforced by [security-reviewer](../agents/security-reviewer.md) and [database-reviewer](../agents/database-reviewer.md), mandatory before any deployed project ships ([pau-avila principle 6](../packs/personal/pau-avila/principles.md)). All L1 authority except SSDF process practices which are L1 (NIST standard).
