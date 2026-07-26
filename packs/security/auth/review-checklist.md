# Review Checklist — Auth Pack

Binary checks. Each cites the engineering rule it enforces. Critical items block in
every reasoning profile, Prototype included.

## Critical (blocks in every profile)

- [ ] Browser/mobile login uses authorization code + PKCE with `S256`; no implicit flow,
      no password grant. (AU1–AU3)
- [ ] `redirect_uri` matching is exact-string against an allowlist — no wildcard host,
      prefix, or path. (AU12)
- [ ] Post-login "return to" targets cannot be an attacker-supplied absolute URL. (AU13)
- [ ] `state` is sent and verified on the callback. (AU8)
- [ ] `nonce` is sent and verified for OIDC logins. (AU9)
- [ ] Token signature, `iss`, `aud`, and `exp` are validated by every service acting on
      the token. (AU15–AU17)
- [ ] The verification path pins the algorithm; `alg: none` and header-selected
      algorithms are rejected. (AU18)
- [ ] ID tokens are not accepted as API authorization. (AU19)
- [ ] No token appears in a URL query string, path, or fragment. (AU23)
- [ ] Session cookies are `HttpOnly` + `Secure` + `SameSite=Lax` or stricter. (AU24)
- [ ] Session identifier is regenerated at login and at privilege elevation. (AU29)
- [ ] Logout revokes server-side, not only client-side. (AU30)
- [ ] Password change / email change / MFA change invalidates other sessions. (AU31)
- [ ] Refresh tokens rotate on use, and reuse revokes the family. (AU32, AU33)
- [ ] Passwords are stored under a memory-hard, per-user-salted hash. (AU37)
- [ ] Password minimum length ≥ 8, ≥ 64 accepted, no composition rules. (AU38)
- [ ] Breached-password screening runs at signup and password change. (AU40)
- [ ] Reset tokens are single-use and short-lived. (AU42)
- [ ] Reset and failed login do not disclose whether the account exists. (AU43, AU50)
- [ ] Authentication endpoints are rate-limited per account and per source. (AU49)
- [ ] Supabase: server-side identity comes from `getUser()`, never `getSession()`. (AU54)
- [ ] Supabase: the service-role key is absent from every client-reachable surface. (AU55)
- [ ] Supabase: the redirect-URL allowlist contains no broad wildcard. (AU56)

## High

- [ ] `state`/`nonce` are stored server-side or in a signed `HttpOnly` cookie, not
      `localStorage`. (AU10)
- [ ] `iss` in the callback is verified when the provider returns it. (AU11)
- [ ] Refresh tokens are not held in browser `localStorage`/`sessionStorage`. (AU25)
- [ ] Access-token lifetime is explicitly configured and measured in minutes. (AU26)
- [ ] Authorization decisions never read a client-supplied identity header or
      parameter. (AU20)
- [ ] Sessions have both an idle timeout and an absolute lifetime. (AU34)
- [ ] Re-authentication gates high-impact actions. (AU35)
- [ ] MFA recovery is no weaker than the factor it recovers. (AU45)
- [ ] Recovery codes are single-use and hashed at rest. (AU46)
- [ ] Authorization codes are single-use and a replay is rejected. (AU7)
- [ ] Supabase: PKCE is the configured flow and the session lives in cookies. (AU57)
- [ ] Supabase: leaked-password protection is switched on. (AU58)

## Medium

- [ ] JWKS is cached with a bounded TTL and re-fetch is rate-limited. (AU21)
- [ ] `code_verifier` is per-request, CSPRNG-generated, ≥ 43 characters. (AU5)
- [ ] Unicode and spaces are accepted in passwords without silent truncation. (AU39)
- [ ] No scheduled password expiry. (AU41)
- [ ] TOTP rejects a code already used in its window. (AU47)
- [ ] SMS is not the only second factor for privileged accounts. (AU48)
- [ ] Users can view and revoke their active sessions. (AU36)
- [ ] Machine-to-machine access uses client credentials, not a user token. (AU6)
- [ ] Supabase: RLS on sensitive tables asserts assurance level where MFA exists. (AU59)

## Low

- [ ] Sender-constrained or audience-restricted tokens where the provider supports
      them. (AU22)
- [ ] Loopback redirects vary only the port. (AU14)
- [ ] Knowledge-based recovery questions are absent. (AU44)
- [ ] Supabase: JWT lifetime is set deliberately and refresh is covered by a test. (AU60)

## Process

- [ ] Authentication events are logged with actor/source/timestamp and no
      credentials. (AU52)
- [ ] Tokens and codes are absent from logs, error reports, and analytics. (AU27)
- [ ] TLS is required on every credential-carrying endpoint. (AU28)
- [ ] Anti-abuse controls fail to a challenge, not to an open endpoint. (AU53)
