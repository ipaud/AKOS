# Workflow: Security Review

Focused security pass — mandatory before any deployed project is "done."

## Agents

1. [security-reviewer](../agents/security-reviewer.md) — OWASP Top 10, API Top 10, ASVS level, SSDF process.
2. [database-reviewer](../agents/database-reviewer.md) — Supabase RLS check (enabled at creation, `auth.uid()`-scoped, service_role server-only, tested multi-user), PII access control.

## Sweep

- OWASP Top 10 category-by-category; API Top 10 for endpoints.
- The four key tests: "what if the frontend lied," ID-swap/IDOR, string-concatenation grep, SSRF smell.
- Supabase: grep client bundles for service_role; test policies as two real users.
- On any CRITICAL: STOP, fix, rotate exposed secrets, sweep for similar issues.

## Profile adjustments

- **Prototype (deployed):** floor only — no secrets in code, no exposed endpoints with real data, RLS on. Prototype (never deployed) may defer.
- **Production:** full ASVS L2; **Enterprise:** L2+ with SSDF process and audit trail.

## Exit criteria

No open CRITICAL. Score ≥ the profile's bar. This owner: **required before any deployed project ships** ([pau-avila principle 6](../packs/personal/pau-avila/principles.md)).
