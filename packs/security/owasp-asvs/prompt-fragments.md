# Prompt Fragments — OWASP ASVS Pack

## Fragment: level-selection lens

```text
Determine the appropriate OWASP ASVS target level (AKOS L1) for this
application: consider data sensitivity (PII, payments, health data),
attacker motivation (opportunistic vs. skilled/motivated vs.
sophisticated/well-resourced), and regulatory context. Recommend L1, L2,
or L3 with a one-sentence justification, and map it to the AKOS
reasoning profile in use.
```

## Fragment: domain-by-domain review lens

```text
Review this application against OWASP ASVS, one domain at a time:
Architecture (trust boundaries documented?), Authentication, Session
Management (server-authoritative?), Access Control (checked at every
reachable layer?), Validation/Encoding (allowlist-based?), Cryptography
(key management documented?), Error Handling/Logging (sufficient for
incident reconstruction, no leaked secrets?), Business Logic (workflow
sequence/rate abuse prevented?), Configuration (environment-diffed at
release?). Report gaps per domain with the target level they apply to.
```

## One-liner

```text
ASVS: state a target level (L1/L2/L3) matched to data sensitivity and
attacker motivation; centralize auth/validation logic; enforce access
control at every reachable layer; allowlist validation; document trust
boundaries and key management at L2+; model business-logic workflows
against out-of-order/excessive-repetition abuse; diff config per environment.
```
