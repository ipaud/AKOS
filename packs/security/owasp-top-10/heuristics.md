# Heuristics — OWASP Top 10 Pack

- **The "what if the frontend lied" test:** for every request, ask what happens if an attacker sends it directly (bypassing your UI) with modified IDs, roles, or amounts. If the server trusts the client's claim about who it is or what it owns, that's A01.
- **The string-concatenation grep:** search for SQL/shell/command strings built via concatenation or template literals with variables — nearly always A03 if the variable comes from user input.
- **The "guess the ID" test:** change a numeric/UUID ID in a request to another user's resource ID — does the server return their data? That's IDOR (A01).
- **The error-message test:** trigger a 500 error deliberately — does the response leak a stack trace, file path, or internal library version to the client? A05.
- **The dependency-audit reflex:** run `npm audit`/`pip-audit`/equivalent before every release; treat critical/high CVEs in production dependencies as release blockers, not backlog items.
- **The "logged in as who" test:** after logout, is the old session/token still valid? A07.
- **The SSRF smell:** any feature accepting a URL from a user and having the server fetch it (webhooks, image-by-URL, link previews) is an SSRF candidate until proven allowlisted.
- **The secrets-in-logs check:** grep logs for password/token/API-key fields — if present even in debug logs, that's A09 (and potentially A02).
