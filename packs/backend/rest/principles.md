# Principles — REST Pack

- **RS1** — URLs identify resources (nouns); actions are expressed via HTTP method, not verbs in the path.
- **RS2** — Status codes are used correctly and consistently: 200/201/204 success variants, 400/401/403/404/409/422 client errors, 500 server errors.
- **RS3** — GET/PUT/DELETE are truly idempotent; POST is used for non-idempotent creation/actions.
- **RS4** — List endpoints support pagination (cursor or offset) with sane default and maximum page sizes.
- **RS5** — Breaking changes are versioned (URL path or header-based), with old versions supported through a deprecation window.
- **RS6** — Response envelopes are consistent across the API (same success/error/pagination shape everywhere).
- **RS7** — Error responses include a machine-readable code and a human-readable message, not just a status code.
