# Heuristics — Auth Pack

Defaults with known exceptions. Reach for these when the design is still open; the
[engineering rules](engineering-rules.md) decide once code exists.

- **Don't build it.** Delegate authentication to an identity provider or the platform
  already in the stack. Hand-rolled auth is where a team's remaining security budget
  goes to die. Exception: a genuinely offline or air-gapped product.
- **If a screen shows a password field you wrote, ask what it bought you.** Social and
  magic-link logins remove password storage, reset flows, and breach screening from your
  surface area entirely. Exception: enterprise buyers who require local accounts.
- **Pick the shortest token lifetime the UX survives, then rely on refresh.** Long access
  tokens are chosen to avoid building refresh handling, and that is the wrong reason.
- **Prefer an `HttpOnly` cookie over any token the JavaScript can read.** The moment an
  XSS lands, `localStorage` is an exfiltration endpoint. Exception: a native client with
  no DOM, where secure storage is the platform keychain.
- **Where an SPA talks to your own API, put a thin backend in front of the tokens.** The
  browser holds a session cookie; the server holds the tokens. This costs one small
  service and removes an entire class of finding.
- **Treat every "just for now" auth shortcut as permanent.** Prototype-profile relaxation
  applies to tests, docs, and polish — not to AU-starred rules. A prototype that reaches
  real users keeps the auth it shipped with.
- **When a provider offers a security setting that is off by default, assume it is off.**
  Breached-password screening, MFA enforcement, and session limits are commonly
  available and commonly unswitched. Read the project settings, don't infer them.
- **Make the enumeration-safe response the default copy, not a later hardening pass.**
  Retrofitting identical responses across signup, login, and reset means rewriting three
  flows and their tests.
- **Log the security events before you need them.** Token reuse, lockout, and MFA changes
  are the events an incident is reconstructed from, and they cannot be added
  retroactively to a breach that already happened.
- **If the design needs a diagram to explain who validates what, it is wrong.** A flow
  whose trust boundaries are hard to draw is a flow whose trust boundaries will be
  implemented inconsistently.
- **Test the negative path.** A login test that only asserts success proves the door
  opens, not that it locks. Assert the rejected `state`, the expired token, the reused
  refresh token.
- **Assume the redirect allowlist will be asked to accept a wildcard for preview
  deployments.** Solve it with a deterministic per-branch host registered at deploy time,
  not with a pattern that also matches an attacker's subdomain.
