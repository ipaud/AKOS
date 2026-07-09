# Heuristics — OWASP ASVS Pack

- **Level selection shortcut:** does the app handle payments, health data, or high-value credentials, or is it a plausible target for a motivated/skilled attacker (not just opportunistic)? → L2 minimum. Critical infrastructure, very high transaction values, or regulatory mandate → L3. Everything else with any real user data → L1.
- **The "one auth check to rule them all" test:** grep for how many distinct places implement authentication/authorization logic — if it's more than one canonical middleware/guard, centralization (AS2) has already eroded.
- **The workflow-replay test:** can a multi-step business flow (checkout, application submission, approval) be replayed out of order or repeated beyond its intended count by directly calling later-step endpoints? (AS9)
- **The trust-boundary walk:** for L2+, walk the data flow diagram and mark every boundary crossing; if a boundary has no named control, that's a gap (AS3).
- **The environment-diff check:** compare security-relevant configuration (CORS, debug flags, verbose logging, default accounts) across dev/staging/production — differences that matter should be intentional and documented, not accidental (AS10).
- **Domain-by-domain sweep for L2/L3 audits:** rather than one flat pass, review one ASVS domain at a time (auth, session, access control, validation, crypto, logging, data protection, business logic) — mirrors the [NN/g one-heuristic-at-a-time](../../ux/nielsen-norman-group/heuristics.md) discipline and catches domain-specific gaps a blended pass misses.
