# Glossary — OWASP Top 10 Pack

- **IDOR (Insecure Direct Object Reference)** — accessing another user's resource by guessing/modifying an ID, due to missing ownership checks.
- **Injection** — untrusted input executed as code/query (SQL, command, LDAP, etc.).
- **SSRF (Server-Side Request Forgery)** — tricking a server into making requests to attacker-chosen destinations, often reaching internal-only services.
- **Trust boundary** — the point where data crosses from less-trusted to more-trusted context, requiring validation.
- **Least privilege** — granting only the minimum permissions needed for a task.
- **Defense in depth** — layering independent security controls so one failure doesn't equal full compromise.
- **Fail closed** — defaulting to deny access when a security check errors.
- **Threat model** — a structured analysis of what could go wrong and who might attack a system, done before building sensitive flows.
- **CVE** — Common Vulnerabilities and Exposures; a known, catalogued security vulnerability.
- **Adaptive hash (bcrypt/argon2/scrypt)** — password-hashing algorithms deliberately slow/tunable to resist brute-force.
