# Review Checklist — OWASP Top 10 Pack

Floor items (★) block in every profile beyond Prototype; treat as CRITICAL findings.

## Critical ★

- [ ] Server-side authorization enforced on every data-scoped request; ownership verified, not assumed. (OW1)
- [ ] Passwords stored via modern adaptive hash; never plaintext/reversible/fast-hash. (OW2)
- [ ] All DB queries parameterized; no string-concatenated SQL. (OW3)
- [ ] All shell/command execution with user input uses safe argument passing. (OW4)
- [ ] Client-facing errors never leak stack traces/internals. (OW8)
- [ ] Brute-force protection on all authentication endpoints. (OW11)
- [ ] Auth/authz/validation failures logged with context, no secrets. (OW16)
- [ ] Server-side requests built from user input are allowlist-validated (SSRF). (OW17)

## High

- [ ] Output encoded per rendering context; no raw unescaped user content in HTML. (OW5)
- [ ] Sensitive flows have a documented threat model. (OW6)
- [ ] TLS enforced everywhere; HSTS enabled. (OW7)
- [ ] No default credentials shipped to any environment. (OW9)
- [ ] Dependency vulnerability scan runs in CI; critical/high findings block release. (OW10)
- [ ] Sessions/tokens invalidated on logout/password change; never in URLs. (OW12)
- [ ] Deserialization of untrusted data uses strict schema validation, no unsafe deserializers. (OW15)

## Medium

- [ ] MFA/passkey option available for sensitive/elevated accounts. (OW13)
- [ ] CI/CD artifact integrity verified; dependencies pinned. (OW14)
