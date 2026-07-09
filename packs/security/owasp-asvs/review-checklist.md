# Review Checklist — OWASP ASVS Pack

Applicability marked by level; L1 items apply to every application beyond Prototype.

## Critical (L1+)

- [ ] Target ASVS level stated and documented. (AV1)
- [ ] Authentication/authorization centralized in one reusable mechanism. (AV2)
- [ ] Session tokens server-generated, server-expired, server-invalidated on logout/password change. (AV4)
- [ ] Authorization enforced at every layer capable of reaching the data (not API-only if direct DB access exists). (AV5)

## High (L1-L2)

- [ ] Input validation uses allowlisting where the valid space is enumerable. (AV6)
- [ ] Logs sufficient for incident reconstruction, no secrets/full PII. (AV8)

## Medium (L2+)

- [ ] Trust-boundary documentation exists, naming controls at each crossing. (AV3)
- [ ] Cryptographic key management documented (storage, rotation, access). (AV7)
- [ ] At least one critical business workflow has state-machine/sequence verification. (AV9)
- [ ] Environment-specific configuration reviewed/diffed as part of release. (AV10)

## Low

- [ ] Level target re-confirmed after significant scope/data-sensitivity changes (e.g. adding payments).
