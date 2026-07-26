# Prompt Fragments — Auth Pack

Copy-paste blocks for injecting this pack into an agent prompt. Read this file first —
in most tasks the build-mode block is all that needs to be loaded.

## Fragment: build-mode constraint block

```text
AUTH CONSTRAINTS (safety floor — applies in every reasoning profile, Prototype included):

Flow
- Authorization code + PKCE (S256) for every browser and mobile client. Never implicit,
  never resource-owner-password.
- Send and verify `state` on every request. Send and verify `nonce` for OIDC.
- redirect_uri is matched by exact string against an allowlist. No wildcards, no prefix
  matching, no attacker-supplied absolute URL as a post-login destination.

Tokens
- Validate signature, iss, aud, and exp in every service that acts on a token. Pin the
  algorithm; reject `alg: none`.
- ID tokens authenticate. Access tokens authorize. Never swap them.
- Never read identity from a request body, query parameter, or custom header.
- Tokens go in the Authorization header or an HttpOnly cookie. Never in a URL.

Session
- Regenerate the session identifier at login and at privilege elevation.
- Logout revokes server-side, not just client-side.
- Refresh tokens rotate on use; reuse revokes the family and is logged.
- Set both an idle timeout and an absolute lifetime.

Credentials
- Memory-hard hash, per-user salt. Minimum length 8, accept 64+, no composition rules.
- Screen against breached-password lists.
- Reset tokens: single-use, short-lived.
- One message and one status code whether or not the account exists — on login, signup,
  and reset alike.
- Rate-limit every authentication endpoint per account and per source.

Supabase (when in the stack)
- Server-side identity comes from getUser(), never getSession().
- The service-role key never reaches a client bundle or browser-reachable route.
- Redirect URLs are enumerated in project config, with no broad wildcard.
```

## Fragment: review lens

```text
Review this authentication surface against the AKOS auth pack (security/auth).

Report findings by severity, each citing its rule code (AU1–AU60). Treat as CRITICAL:
anonymous-reachable account takeover, unverified server-side session reads, plaintext or
fast-hash password storage, a client-reachable RLS-bypassing key, missing state/nonce
verification, wildcard redirect matching, logout that does not revoke server-side, and
refresh tokens that never rotate.

For each finding give: the rule code, the file and line, the concrete failure scenario
(what an attacker does, in order), and the smallest fix. Do not report a rule as met
unless you have seen the code that meets it — absence of evidence is a finding of
"unverified", not a pass.

State explicitly which starred rules you could not check and why.
```

## Fragment: pre-implementation questions

```text
Before writing the login, answer these:

1. Who stores the credential — us, or an identity provider? If us, why?
2. Where does the browser hold the session, and what happens to it under XSS?
3. What is the access-token lifetime, and where is that value set?
4. What invalidates a session besides expiry? (logout, password change, MFA change, admin)
5. What does the reset flow tell an attacker enumerating addresses?
6. Which actions require re-authentication regardless of session freshness?
7. If MFA exists, what is the recovery path, and is it as strong as the factor?
```

## One-liner (for tight token budgets)

```text
Auth floor: code+PKCE only, exact-string redirect allowlist, verify state/nonce,
validate sig+iss+aud+exp with a pinned algorithm, ID tokens never authorize, tokens never
in URLs, HttpOnly+Secure+SameSite cookies, regenerate session at login, logout revokes
server-side, refresh rotates and reuse revokes the family, memory-hard password hash with
breach screening, identical responses whether or not the account exists, rate-limit every
auth endpoint. Supabase: getUser() not getSession() on the server; service-role key
server-only.
```
