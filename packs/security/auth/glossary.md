# Glossary — Auth Pack

Terms this pack uses precisely. Where the industry uses one word for two things, the
entry says which one is meant here.

- **Authentication (authn)** — establishing *who* the requester is.
- **Authorization (authz)** — deciding *what* that requester may do. A separate decision,
  made from a separate token.
- **Access token** — a capability presented to a resource server. Scoped, short-lived,
  audience-restricted.
- **ID token** — an assertion that a login happened, issued to a specific client. Proof of
  authentication, never an API credential.
- **Refresh token** — a long-lived credential exchanged for new access tokens. The most
  valuable secret in the flow, and therefore the one that rotates.
- **Authorization code** — a single-use value returned to the redirect endpoint and
  exchanged, server-side, for tokens.
- **PKCE** — proof key for code exchange. The client commits to a secret (`code_verifier`)
  by sending its hash (`code_challenge`) up front, so a stolen code is useless without the
  original secret. Required for every client type, not only public ones.
- **`state`** — an opaque per-request value binding the callback to the browser session
  that started the flow. Defeats cross-site request forgery on the callback.
- **`nonce`** — an OIDC per-request value embedded in the ID token, binding that token to
  this authorization request. Defeats replay of a previously issued token.
- **Bearer token** — any credential that works for whoever holds it. Everything is a
  bearer token until something binds it.
- **Sender-constrained token** — a token bound to the client's key or connection (mTLS,
  DPoP), so possession alone is insufficient.
- **Audience (`aud`)** — the intended recipient of a token. Validating it stops a token
  minted for one service being replayed against another.
- **JWKS** — the issuer's published set of public keys, selected by `kid` at validation.
- **Session fixation** — an attacker fixes a session identifier before login so the
  victim's authenticated session lands on it. Defeated by regenerating at login.
- **Refresh-token reuse detection** — treating a second use of an already-rotated token as
  evidence of theft, and revoking the whole family.
- **Token family** — the chain of refresh tokens descended from one login. Revoked as a
  unit on reuse.
- **Idle timeout** — the session ends after inactivity. Bounds an unattended screen.
- **Absolute lifetime** — the session ends at a fixed age regardless of activity. Bounds a
  stolen token that stays warm.
- **Step-up authentication** — requiring a stronger or fresher proof before a specific
  action, independent of session age.
- **AAL (authenticator assurance level)** — how strongly the authentication event was
  proven. Relevant here because an authorization rule may need to assert it, not merely
  that *some* session exists.
- **Phishing-resistant factor** — one that cannot be relayed by a convincing fake site
  (typically origin-bound public-key credentials). SMS and TOTP are not.
- **Account enumeration** — inferring which identifiers are registered from differences in
  responses, status codes, or timing.
- **Backend-for-frontend (BFF)** — a thin server owned by the same team that holds the
  tokens so the browser holds only a session cookie.
- **Magic link** — authentication by a single-use, short-lived URL sent out of band.
  Removes password storage from the system; inherits the security of the mailbox.
- **Service-role key** — in Supabase, a key that bypasses row-level security entirely.
  Server-side only, always.
