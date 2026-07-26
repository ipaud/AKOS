# Engineering Rules — Auth Pack

Checkable in the artifact. A reviewer verifies each mechanically; a violation is a
finding. `★` marks floor rules that hold in every reasoning profile, Prototype
included — they are the safety floor, not a Production upgrade. Parenthetical codes
cite the principle in [principles.md](principles.md).

## Flow selection

- AU1 ★. Browser and mobile logins use the authorization code flow with PKCE
  (`code_challenge_method=S256`), for confidential clients as well as public ones. (P5)
- AU2 ★. The implicit flow is not used: no `response_type=token`, no access token
  arriving in a URL fragment. (P5)
- AU3 ★. The resource-owner password credentials grant is not used — the application
  never collects a third-party password in order to exchange it. (P5)
- AU4. `code_challenge_method` is `S256`; `plain` is neither sent nor accepted. (P5)
- AU5. The `code_verifier` is generated per authorization request from a CSPRNG, is at
  least 43 characters, and is never reused across requests. (P7)
- AU6. Machine-to-machine callers use the client credentials grant with a credential
  that belongs to no user, never a user token minted at signup. (P1)
- AU7. Authorization codes are exchanged exactly once; a second exchange of the same
  code fails and is logged as a security event. (P2)

## The round trip

- AU8 ★. Every authorization request sends `state`, and the callback rejects a response
  whose `state` is absent, unknown, or already consumed. (P7)
- AU9 ★. OIDC logins send `nonce`, and ID-token validation rejects a token whose `nonce`
  does not match the one stored for that request. (P7)
- AU10. `state` and `nonce` are bound to the initiating session server-side or in a
  signed `HttpOnly` cookie — not in `localStorage`, which any injected script reads. (P3)
- AU11. When the provider returns an `iss` parameter, the callback verifies it matches
  the authorization server the request was sent to (mix-up defense). (P8)

## Redirects

- AU12 ★. `redirect_uri` values are an allowlist compared by exact string. No prefix
  match, no suffix match, no wildcard host, no wildcard path segment. (P6)
- AU13 ★. Any post-login "return to" destination is validated against an allowlist of
  in-app paths, or is a path-only value with scheme and host supplied by the server —
  never a full URL taken from a query parameter. (P6)
- AU14. Loopback redirects for native clients accept a variable port but a fixed path,
  and the port is not templated from user input. (P6)

## Token validation

- AU15 ★. Every service acting on a token validates the signature against keys fetched
  from the issuer's JWKS endpoint, with the key selected by `kid`. (P8)
- AU16 ★. Validation checks `iss` against the expected issuer and `aud` against this
  service's own identifier; a token minted for another audience is rejected. (P2, P8)
- AU17 ★. Validation checks `exp`, plus `nbf`/`iat` where present, with a clock-skew
  allowance no larger than 60 seconds. (P2)
- AU18 ★. The signing algorithm is pinned to an expected asymmetric algorithm; `none` is
  rejected, and an algorithm named in the token header never selects the verification
  path by itself. (P8)
- AU19 ★. ID tokens authenticate; they never authorize an API call. Resource servers
  accept access tokens only. (P1)
- AU20. Authorization decisions read claims from a validated token, never from a request
  body, header, or query parameter the client controls (`?user_id=`, `X-User-Role`). (P3)
- AU21. JWKS responses are cached with a bounded TTL and re-fetched on an unknown `kid`,
  with the re-fetch itself rate-limited. (P8)
- AU22. Where the provider supports audience restriction or sender constraining (mTLS,
  DPoP), tokens for sensitive resource servers use it. (P2)

## Token storage and transport

- AU23 ★. Tokens travel in the `Authorization` header or an `HttpOnly` cookie — never in
  a query string, a URL path, or a fragment, all of which land in logs, referrers, and
  browser history. (P2)
- AU24 ★. Session cookies set `HttpOnly`, `Secure`, and `SameSite=Lax` or stricter, with
  `Path=/` and no `Domain` broader than the app needs. (P3)
- AU25. Browser clients do not hold refresh tokens in `localStorage` or
  `sessionStorage`; the refresh credential lives in an `HttpOnly` cookie or behind a
  backend-for-frontend. (P3, P11)
- AU26. Access-token lifetime is measured in minutes, and is set in config rather than
  left at a provider default nobody checked. (P2, P12)
- AU27. Tokens and authorization codes never appear in application logs, error
  reporting, or analytics payloads. (P2)
- AU28. TLS is required on every endpoint carrying a credential; there is no plaintext
  fallback path. (P2)

## Session lifecycle

- AU29 ★. The session identifier is regenerated on login and on any privilege elevation;
  a pre-login identifier is never carried into an authenticated session. (P9)
- AU30 ★. Logout invalidates the session server-side — revoking the refresh token and
  clearing server state — not only deleting the client cookie. (P10)
- AU31 ★. Changing a password, changing an email, altering MFA enrollment, or an admin
  disabling the account invalidates that user's other active sessions. (P10)
- AU32 ★. Refresh tokens rotate on every use, and rotation invalidates the previous
  token. (P11)
- AU33 ★. Reuse of an already-rotated refresh token revokes the whole token family for
  that session and is logged as a security event. (P11)
- AU34. Sessions carry both an idle timeout and an absolute maximum lifetime, both set
  explicitly. (P12)
- AU35. Re-authentication is required before high-impact actions — changing the password,
  changing MFA enrollment, deleting the account, changing payout details — however fresh
  the session is. (P9)
- AU36. Users can list their active sessions and revoke them individually, wherever the
  product holds anything worth stealing. (P10)

## Passwords and recovery

- AU37 ★. Passwords are stored under a memory-hard hash (argon2id or scrypt; bcrypt
  where the platform offers nothing better), with a per-user salt and a calibrated work
  factor. No fast general-purpose hash, no reversible encryption, no plaintext. (P14)
- AU38 ★. Minimum password length is at least 8 characters, passwords of at least 64
  characters are accepted, and no character class is required. (P13)
- AU39. All printable characters including spaces and Unicode are accepted, input is not
  silently truncated, and Unicode is normalized consistently before hashing. (P13)
- AU40 ★. Candidate passwords are screened against a known-breached-password list at
  signup and at password change. (P13)
- AU41. Passwords do not expire on a schedule; a forced change follows evidence of
  compromise. (P13)
- AU42 ★. Password-reset tokens are single-use and high-entropy, expire within minutes to
  a small number of hours, and are invalidated when a new one is issued or the password
  changes. (P2, P10)
- AU43 ★. Password reset does not reveal whether an address exists: same response, same
  visible timing, either way. (P16)
- AU44. Knowledge-based recovery questions are not used as an authentication factor. (P15)

## Multi-factor

- AU45. Where MFA exists, enrollment and recovery are at least as strong as the factor
  itself; support-driven or email-only MFA reset is either documented as an accepted risk
  or removed. (P15)
- AU46. Recovery codes are single-use, hashed at rest, and regenerating them invalidates
  the previous set. (P15)
- AU47. TOTP verification accepts a bounded time-step window and rejects a code already
  used within it. (P2)
- AU48. Where SMS is offered it is labeled as the weaker factor, and it is not the only
  option for accounts with elevated privilege. (P15)

## Enumeration and abuse

- AU49 ★. Login, signup, password reset, and MFA verification are rate-limited per
  account *and* per source, with escalating backoff or lockout. (P16)
- AU50 ★. Failed login returns one message and one status code whether or not the account
  exists. (P16)
- AU51. Signup and "forgot password" disclose no existing accounts through response
  differences, status codes, or measurable timing. (P16)
- AU52. Authentication events — success, failure, lockout, MFA change, token reuse — are
  logged with actor, source, and timestamp, and without credentials or full personal
  data. (P4)
- AU53. When an anti-abuse control's own dependency is unavailable, the endpoint degrades
  to a challenge, never to an open endpoint. (P3)

## Supabase mapping

Rules for the default stack. They do not replace the ones above — they say where the
platform already satisfies one and where it does not.

- AU54 ★. Server-side code establishes identity with `getUser()`, which revalidates
  against the auth server, not with `getSession()`, which returns whatever the cookie or
  storage holds without verifying it. A server authorization decision made from
  `getSession()` is AU20 violated with extra steps. (P3, P8)
- AU55 ★. The service-role key exists only in server-side environments. It bypasses RLS
  entirely, so its presence in a client bundle, a public-prefixed environment variable,
  or a browser-reachable route is a CRITICAL finding. (P3)
- AU56 ★. Redirect URLs are enumerated in the project's Auth URL configuration, and the
  allowlist holds no broad wildcard standing in for "whatever preview deployment we
  get". (P6)
- AU57. PKCE is the configured flow for browser and SSR clients, and the cookie-based
  session helper is used rather than storing the session in `localStorage`. (P5, AU25)
- AU58. Leaked-password protection and a minimum password length are enabled in project
  settings — the platform provides both, and both are inert until switched on. (P13, AU40)
- AU59. Where MFA is enrolled, RLS policies gating sensitive tables assert the assurance
  level from the verified JWT rather than assuming any authenticated session is a
  second-factor session. (P1, P3)
- AU60. JWT lifetime is set deliberately in project settings, and refresh handling is
  exercised by a test rather than assumed from the client library's defaults. (P2, AU26)
