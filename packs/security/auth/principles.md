# Principles — Auth Pack

Durable rules for designing the login itself: who the user is, how that claim is
proven, and how the resulting session stays bound to them. Violating one requires an
explicit tradeoff statement. The `AU*` codes in
[engineering-rules.md](engineering-rules.md) derive from these.

## The spine

- **P1 — Authentication answers *who*, authorization answers *what*. Separate decisions,
  separate tokens.** An ID token is proof of a login event; an access token is a
  capability. Using an ID token to authorize an API call, or deriving permissions from a
  client-held identity claim, collapses two decisions that must be able to fail
  independently.
- **P2 — Every credential is a bearer of blast radius until something binds it.** A token
  that works for anyone holding it works for whoever steals it. Binding — audience,
  issuer, sender, expiry, single use — is what turns a secret into a scoped one.
- **P3 — The client is a delivery mechanism, never the decision point.** Browser and
  mobile code can be read, modified, and replayed. A check that only runs there has not
  run. The authorization server and the resource server each decide for themselves.
- **P4 — Identity flows fail at the seams, not in the primitives.** The cryptography is
  rarely what breaks. What breaks is the redirect that wasn't matched exactly, the state
  that wasn't checked, the session that wasn't regenerated, the token that outlived the
  logout. Review belongs at the transitions.

## The flow

- **P5 — There is one correct browser flow: authorization code with PKCE.** For every
  client type, public and confidential alike. Implicit and resource-owner-password are
  not simpler alternatives, they are withdrawn options. A design reaching for either has
  misread the problem it is solving.
- **P6 — Redirect targets are an allowlist compared by exact string.** Anything admitting
  a prefix, a suffix, a wildcard host, or a user-supplied path is an open redirector
  wearing a login form — and it exfiltrates authorization codes, not merely attention.
- **P7 — Every leg of the round trip carries a value the other leg can check.** PKCE
  binds the code to the client that started the flow; `state` binds the callback to the
  session that started it; `nonce` binds the ID token to that same request. Each defeats
  a different attack, so having one is not having the others.
- **P8 — A token is validated by whoever acts on it, every time.** Signature, issuer,
  audience, expiry, and for an ID token the nonce. Trusting a token because the transport
  delivered it, or because a client library returned it from local storage without a
  network round trip, is not validation.

## The session

- **P9 — The session identifier changes the moment privilege changes.** Issuing a login
  onto an attacker-chosen identifier is session fixation; regeneration at login and at
  elevation is the entire defense.
- **P10 — Logout is a server-side event.** Clearing a cookie ends the client's
  cooperation, not the session. Whatever a stolen token still opens afterward was never
  logged out.
- **P11 — Refresh capability is the most valuable secret in the system, so it is the one
  that rotates.** A refresh token is a long-lived license to mint credentials. Rotate it
  on every use, and treat a reuse as what it almost always is — a theft already in
  progress, not a race to tolerate.
- **P12 — Sessions expire on two clocks.** Idle timeout bounds an unattended screen;
  absolute lifetime bounds a stolen token that stays warm. Only one of them is no bound
  at all.

## The credential

- **P13 — Length is the password requirement that survives contact with users;
  composition rules are not.** Forced character classes and scheduled expiry push people
  toward predictable mutations. Screening against known-breached passwords accomplishes
  more than every composition rule combined.
- **P14 — Store passwords only under a memory-hard hash, salted per user.** A fast
  general-purpose hash is an accelerator for the attacker who already has the dump.
- **P15 — A second factor is only as strong as its weakest recovery path.** Account
  recovery that bypasses MFA *is* the authentication strength of the account.
  Phishing-resistant factors are the target; SMS is a stopgap and must be named as one.
- **P16 — Account enumeration is an authentication defect, not a copy detail.**
  Responses, status codes, and timing that distinguish "no such account" from "wrong
  password" hand over half the credential for free. This is the one screen where the
  vaguer message is the correct message — see
  [content/ux-writing](../../content/ux-writing/README.md) for writing it without being
  useless.

## Scope

This pack covers designing and reviewing the authentication flow. It does not cover
authorization models beyond token validation: row-level rules live in
[backend/supabase](../../backend/supabase/README.md), API object-level checks in
[owasp-api-top-10](../owasp-api-top-10/README.md), and stated verification levels in
[owasp-asvs](../owasp-asvs/README.md).
