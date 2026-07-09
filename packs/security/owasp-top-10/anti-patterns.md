# Anti-Patterns — OWASP Top 10 Pack

## Client-side-only authorization

Hiding an admin button in the UI for non-admins, but the backend endpoint accepts the request from anyone with a valid session regardless of role. Fix: OW1 — server-side check on every request.

## SQL string concatenation

`"SELECT * FROM users WHERE id = " + userId` — the textbook injection vector, still found in real codebases. Fix: OW3 — parameterized queries always.

## Roll-your-own crypto/auth

A hand-written password hashing scheme, a custom session-token format, a homemade "encryption" using XOR. Fix: OW2, established libraries — never invent cryptographic primitives.

## Verbose error pages in production

A stack trace with file paths and a database connection string fragment shown to users on a 500 error. Fix: OW8 — generic client-facing errors, detailed logs server-side only.

## Stale dependency drift

A production app running a web framework version with three publicly known critical CVEs, because "upgrading might break things." Fix: OW10 — CI-blocking vulnerability scanning, scheduled upgrade cadence.

## Fail-open permission checks

A permission check that defaults to `allow` if the role-lookup service times out or throws. Fix: fail-closed mental model — errors in security checks deny by default.

## SSRF via "fetch this URL" features

A link-preview or webhook feature that fetches any user-supplied URL server-side, including `http://169.254.169.254/` (cloud metadata endpoint) or internal service URLs. Fix: OW17 — allowlist validation, block private IP ranges.

## Logging secrets

Debug logs including full request bodies (with passwords, tokens, credit card numbers) "for troubleshooting," retained indefinitely. Fix: OW16 — structured logging that explicitly excludes secret fields.
