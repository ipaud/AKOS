# Prompt: Run Security Review

---

Load AKOS (`~/DEV/AKOS/prompts/load-akos.md`) and run the security review workflow (`~/DEV/AKOS/workflows/security-review.md`) on [describe the codebase/feature].

Act as `agents/security-reviewer.md` and `agents/database-reviewer.md`, loading the OWASP Top 10, API Top 10, ASVS, NIST SSDF, and Supabase packs.

Sweep:
- OWASP Top 10 category-by-category; API Top 10 for endpoints.
- The four tests: "what if the frontend lied," ID-swap/IDOR, string-concatenation grep, SSRF smell.
- Supabase: is RLS enabled on every user-data table? Policies `auth.uid()`-scoped? service_role never in client code? Policies tested as two real users? Grep client bundles for the service key.

On any CRITICAL: STOP, report it, note that any exposed secret must be rotated, and sweep for similar issues.

Produce a Review Summary. Score CRITICAL for anonymous-exploitable, HIGH for authenticated-exploitable. Final decision BLOCKED if any CRITICAL is open. This review is **mandatory before any deployed project is considered done.**
