# Principles — OWASP Top 10 Pack

- **A01 Broken Access Control:** enforce authorization server-side on every request, by default deny; never trust client-supplied role/ID claims; check ownership on every object access (IDOR prevention).
- **A02 Cryptographic Failures:** encrypt sensitive data at rest and in transit (TLS everywhere); use current, vetted algorithms (never roll your own crypto); never store passwords other than via a modern adaptive hash (bcrypt/argon2/scrypt); classify data sensitivity so protection effort matches risk.
- **A03 Injection:** treat all user input as untrusted; use parameterized queries/prepared statements for all data access, never string concatenation; validate and encode output per context (HTML/SQL/shell/URL each have different escaping needs).
- **A04 Insecure Design:** threat-model before building sensitive flows; apply secure-by-default patterns (deny-by-default access control, rate limiting by design); insecure design is an architecture defect, not a patchable bug.
- **A05 Security Misconfiguration:** no default credentials, no verbose error messages leaking stack traces/internals to users, no unnecessary services/ports exposed, security headers set by default, hardened configuration templates reused across environments.
- **A06 Vulnerable and Outdated Components:** track dependency versions and known CVEs; patch promptly; remove unused dependencies; prefer actively maintained libraries.
- **A07 Identification and Authentication Failures:** enforce strong password/passkey policies, rate-limit and lock out brute-force attempts, support MFA, invalidate sessions properly on logout/password change, never expose session identifiers in URLs.
- **A08 Software and Data Integrity Failures:** verify signatures/checksums on updates and CI artifacts; never deserialize untrusted data without strict type/schema constraints; pin CI/CD dependencies.
- **A09 Security Logging and Monitoring Failures:** log authentication events, access-control failures, and input-validation failures with enough context to investigate, without logging secrets/PII; alert on suspicious patterns; ensure logs are tamper-resistant.
- **A10 SSRF:** validate and allowlist any server-side outbound request destinations built from user input; never let user input directly control internal-network-reachable URLs.
