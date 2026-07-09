# Prompt Fragments — OWASP Top 10 Pack

## Fragment: build-mode constraint block

```text
Apply OWASP Top 10 constraints (AKOS L1 security floor):
- Authorization checked server-side on every data-scoped request;
  ownership verified, never assumed from client-supplied IDs.
- All database access via parameterized queries/prepared statements;
  never string-concatenated SQL. Shell/command execution uses safe
  argument passing, never concatenation.
- Passwords stored via bcrypt/argon2/scrypt only; never plaintext or
  reversible encryption.
- Output encoded per rendering context; no raw unescaped user content.
- Client-facing errors are generic; detailed errors logged server-side only.
- TLS enforced everywhere; no default credentials in any environment.
- Auth endpoints rate-limited with lockout/backoff; sessions invalidated
  on logout/password change, never in URLs.
- Server-side requests built from user input are allowlist-validated
  (SSRF); private IP ranges blocked by default.
- Untrusted data deserialized only via strict schema validation; never
  unsafe deserializers (pickle/eval) on external input.
- Auth/authz/validation failures logged with context, excluding secrets.
```

## Fragment: security review lens

```text
Review this code against the OWASP Top 10, category by category:
A01 access control — server-side ownership checks on every request?
A02 crypto — passwords hashed properly? TLS enforced? Sensitive data
   encrypted at rest?
A03 injection — any string-concatenated queries/commands?
A04 insecure design — do sensitive flows have a threat model?
A05 misconfiguration — default creds, verbose errors, open services?
A06 dependencies — known CVEs in use, scanning in CI?
A07 auth failures — brute-force protection, session invalidation, MFA?
A08 integrity — safe deserialization, verified CI artifacts?
A09 logging — auth/authz failures logged without leaking secrets?
A10 SSRF — user-influenced outbound requests allowlist-validated?
Report findings as CRITICAL for exploitable-by-anonymous-user issues,
HIGH for authenticated-user-exploitable, with the specific fix.
```

## One-liner

```text
OWASP Top 10: server-side authz always; parameterized queries always;
hashed passwords (bcrypt/argon2); encode output per context; generic
client errors; TLS everywhere; rate-limited auth; SSRF allowlisting;
safe deserialization; log security events without secrets.
```
