# Anti-Patterns — Auth Pack

Named failure modes, how to spot them, and what to do instead.

## The trusted client claim

**Detect:** an endpoint reads `user_id`, `role`, `tenant`, or `is_admin` from a request
body, query string, or custom header, and uses it in a data lookup.
**Why it fails:** the client is a delivery mechanism (P3). Whatever it sends, an attacker
can send too — with a different value.
**Fix:** derive identity from the validated token only. Where a client must *name* a
resource, the server still checks the token's subject owns it. (AU20)

## The unverified session read

**Detect:** server-side code calls a "get current session" helper that reads a cookie or
storage and returns a user object without a network round trip, then authorizes from it.
**Why it fails:** a decoded token is not a verified token. Anything that can write the
cookie can write the claims.
**Fix:** on the server, use the call that revalidates against the auth server. In
Supabase that is `getUser()`, not `getSession()`. (AU54)

## The wildcard redirect

**Detect:** a redirect allowlist entry containing `*`, a prefix comparison
(`startsWith`), or a rule like "any subdomain of ours".
**Why it fails:** subdomain takeover and open-redirect chains turn the login into a code
exfiltration endpoint, and the victim sees your real domain the whole time.
**Fix:** exact-string allowlist. Register preview deployments explicitly at deploy
time. (AU12, AU56)

## The open return-to

**Detect:** `?next=`, `?returnTo=`, or `?redirect=` accepted as a full URL and followed
after login.
**Why it fails:** it's an open redirector attached to a page users have been trained to
trust, and it survives every other control in the flow.
**Fix:** accept a path only, or match against an allowlist of in-app destinations. (AU13)

## The forever session

**Detect:** logout deletes a cookie and returns; no server-side revocation; no absolute
lifetime; a refresh token that never rotates.
**Why it fails:** a token stolen once works until it expires, and it was configured never
to expire. Logout on a shared machine does nothing for the copy already taken.
**Fix:** revoke server-side on logout, rotate refresh on every use, revoke the family on
reuse, and set both clocks. (AU30, AU32–AU34)

## The token in the URL

**Detect:** an access token, session identifier, reset token, or magic-link secret in a
query string or path.
**Why it fails:** it lands in server logs, proxy logs, browser history, and the `Referer`
sent to every third-party asset on the page.
**Fix:** headers or `HttpOnly` cookies. Where a link must carry a secret, make it
single-use and short-lived so the leak has a deadline. (AU23, AU42)

## The ID token used as a key

**Detect:** a resource server accepting an ID token, or a client sending one as its API
credential because "it has the user in it".
**Why it fails:** the ID token is a statement about a login event for a specific client
audience, not a capability for your API. Accepting it usually means audience validation
is absent too.
**Fix:** access tokens authorize; ID tokens authenticate. Validate `aud`. (AU16, AU19)

## The helpful login error

**Detect:** "No account with that email" versus "Incorrect password", different status
codes for the two cases, or a reset flow that only sends mail when the address exists.
**Why it fails:** the attacker now has a verified user list and can move to credential
stuffing with half the work done.
**Fix:** one message, one status code, one visible timing, on every one of login, signup,
and reset. Say what to do next instead of what went wrong. (AU43, AU50)

## The self-service MFA bypass

**Detect:** MFA can be removed via an emailed link, or support can clear it on request
with no verification stronger than the factor being cleared.
**Why it fails:** the account's real authentication strength is its weakest path, and
that path is now email.
**Fix:** recovery at least as strong as the factor — hashed single-use codes, a second
enrolled factor, or an identity-verified support process. (AU45, AU46)

## The rotation race excuse

**Detect:** a refresh-token reuse is treated as a benign concurrency artifact and
silently allowed, or reuse detection is disabled because it "caused logouts".
**Why it fails:** reuse is the signal that a token was copied. Suppressing the signal
keeps the symptom away and the attacker in.
**Fix:** revoke the family, log the event, and fix the client's concurrent-refresh
handling — which is the actual bug behind the false positives. (AU33)

## The default nobody read

**Detect:** no explicit configuration for token lifetime, breached-password screening,
redirect allowlist, or session limits — the answer to "what is it set to?" is "whatever
the platform does".
**Why it fails:** provider defaults optimize for onboarding friction, not for your
threat model, and several security features ship switched off.
**Fix:** state each value in config or infrastructure-as-code, and review it as part of
the change. (AU26, AU58, AU60)

## The prototype exemption

**Detect:** starred rules waived because the reasoning profile is Prototype, or a code
comment promising to fix auth before launch.
**Why it fails:** prototypes that meet users become products without a rewrite gate, and
the auth that shipped is the auth that stays.
**Fix:** the safety floor is never modulated by profile. Defer the polish, not the
floor. (P4)
