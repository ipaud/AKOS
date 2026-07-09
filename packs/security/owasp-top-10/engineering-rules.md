# Engineering Rules — OWASP Top 10 Pack

- OW1 ★. Authorization is checked server-side on every request that reads or mutates data scoped to a user/tenant; ownership is verified, not assumed from a client-supplied ID. (A01)
- OW2 ★. Passwords are stored only via a modern adaptive hash (bcrypt/argon2/scrypt) with per-user salt; never plaintext, never reversible encryption, never a fast general-purpose hash (MD5/SHA1/SHA256 alone). (A02)
- OW3 ★. All database queries use parameterized queries/prepared statements or a query builder that parameterizes internally — no string concatenation of user input into SQL. (A03)
- OW4 ★. All external command execution (shell, subprocess) with user-influenced arguments uses argument arrays / escaping libraries, never raw string concatenation. (A03)
- OW5. Output is encoded per rendering context (HTML-escape for HTML, attribute-escape for attributes, JS-escape for inline scripts) — templating engines with auto-escaping are the default, raw/unescaped output requires explicit justification.
- OW6. Sensitive-flow features (payments, account recovery, permission changes, bulk export) have a documented threat model before implementation. (A04)
- OW7. TLS is enforced for all traffic (HSTS enabled); no sensitive data transmitted over plaintext HTTP. (A02)
- OW8 ★. Error responses to clients never include stack traces, internal file paths, or library/framework version details; detailed errors are logged server-side only. (A05)
- OW9. Default credentials are never shipped; all environments require credential rotation from any seed/default value before going live. (A05)
- OW10. Dependency vulnerability scanning runs in CI; critical/high severity findings in production dependencies block release. (A06)
- OW11 ★. Failed login attempts are rate-limited and lockout/backoff applied; brute-force protection exists on all authentication endpoints. (A07)
- OW12. Sessions/tokens are invalidated server-side on logout and password change; session identifiers never appear in URLs (query strings, logs). (A07)
- OW13. MFA/passkey support exists for accounts handling sensitive data or elevated privileges, at minimum as an available option. (A07)
- OW14. CI/CD pipelines verify artifact integrity (signed commits/tags, checksum verification) and pin action/dependency versions. (A08)
- OW15. Deserialization of untrusted data uses strict schema validation; unsafe deserialization functions (e.g. `pickle.loads` on untrusted input, `eval`) are never used on external data. (A08)
- OW16 ★. Authentication events, authorization failures, and input-validation failures are logged with actor/timestamp/action context, excluding secrets/full PII; logs are protected from tampering. (A09)
- OW17 ★. Any server-side outbound request whose destination is influenced by user input is validated against an allowlist of permitted hosts/schemes; internal/private IP ranges are blocked by default. (A10)
