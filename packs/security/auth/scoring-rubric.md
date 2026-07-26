# Scoring Rubric — Auth Pack

Primary input to [scoring/security-score.md](../../../scoring/security-score.md), for
the authentication dimension specifically. Where a finding is also an OWASP Top 10
finding, score it once — this rubric refines it, it does not stack with the other pack.

## Deductions (from 100)

| Finding | Deduction |
|---------|-----------|
| Account takeover reachable by an anonymous attacker (wildcard/prefix redirect matching, missing signature or `aud` validation, `alg: none` accepted, tokens minted from client-supplied claims) | −40 each (CRITICAL — caps at Blocked band) |
| Plaintext, reversible, or fast-hash password storage | −40 (CRITICAL) |
| Server authorization decided from an unverified session read (decoded, never revalidated) | −25 (CRITICAL) |
| Service-role / RLS-bypassing key reachable from a client bundle or browser route | −40 (CRITICAL) |
| Implicit or password-grant flow in a browser client | −25 (CRITICAL) |
| Missing `state` or `nonce` verification | −25 (CRITICAL) |
| ID token accepted as API authorization | −25 (CRITICAL) |
| Logout that does not revoke server-side; sessions surviving a password change | −25 (CRITICAL) |
| Refresh tokens that never rotate, or reuse detection absent/disabled | −25 (CRITICAL) |
| Open post-login `returnTo` accepting an absolute URL | −25 (CRITICAL) |
| Tokens in URLs, or session cookies missing `HttpOnly`/`Secure`/`SameSite` | −10 (HIGH) |
| No rate limiting or lockout on authentication endpoints | −10 (HIGH) |
| Account enumeration through message, status code, or timing | −10 (HIGH) |
| Refresh token in browser `localStorage`/`sessionStorage` | −10 (HIGH) |
| No breached-password screening | −10 (HIGH) |
| Reset tokens reusable or long-lived | −10 (HIGH) |
| Session identifier not regenerated at login | −10 (HIGH) |
| No absolute session lifetime, or no idle timeout | −6 (MEDIUM) |
| No re-authentication before high-impact actions | −6 (MEDIUM) |
| MFA recovery weaker than the factor it recovers | −6 (MEDIUM) |
| Composition rules or scheduled expiry imposed on passwords | −4 (MEDIUM) |
| Access-token lifetime left at an unexamined provider default | −4 (MEDIUM) |
| Missing authentication event logging | −4 (MEDIUM) |
| No session listing/revocation for users | −2 (LOW) |
| No sender-constraining where the provider supports it | −2 (LOW) |

## Hard caps

- Any CRITICAL finding: score ≤ 59 (Blocked band), per
  [core/scoring-model.md](../../../core/scoring-model.md).
- Authentication implemented by hand with no identity provider *and* any starred rule
  unmet: cap 49 — the combination is how takeovers happen, not two separate concerns.
- No test exercises a rejected credential (expired token, bad `state`, reused refresh):
  cap 79. A login suite that only asserts success has verified the door opens, not that
  it locks.
- Findings claimed as fixed without an executed check: cap 69, per
  [core/confidence-model.md](../../../core/confidence-model.md).

## Anchors

- **95** — delegated identity, correct flow, both session clocks set, rotation with reuse
  detection, enumeration-safe copy, negative paths tested.
- **85** — the floor holds everywhere; MEDIUM items (session listing, re-auth gates)
  scheduled.
- **72** — floor holds, several HIGH gaps: no rate limiting, enumeration leaks, refresh in
  web storage. Acceptable pre-PMF with a named owner.
- **55** — a starred rule is unmet. Not shippable to real accounts.
- **≤ 40** — an account-takeover path exists today.
