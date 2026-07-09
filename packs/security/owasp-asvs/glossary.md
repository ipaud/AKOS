# Glossary — OWASP ASVS Pack

- **ASVS** — Application Security Verification Standard; OWASP's tiered, domain-organized verification framework.
- **Level 1 (L1)** — baseline verification for any application handling sensitive data; opportunistic-attacker resistant.
- **Level 2 (L2)** — standard verification for significant business/personal/financial data; resistant to skilled, motivated attackers.
- **Level 3 (L3)** — advanced verification for critical/high-value applications; resistant to sophisticated, well-resourced attackers.
- **Trust boundary** — a point where data crosses from less-trusted to more-trusted context.
- **Centralized security control** — a single, reusable implementation of a security function (auth, validation) used everywhere it's needed.
- **Allowlist validation** — defining what's valid and rejecting everything else, vs. denylist (defining what's forbidden).
- **Business logic flaw** — an exploitable workflow-sequence or volume issue with no single "buggy" line of code.
- **Row-Level Security (RLS)** — database-enforced access control scoping rows to the requesting identity.
