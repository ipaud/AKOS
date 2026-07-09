# Anti-Patterns — REST Pack

- **RPC-in-REST-clothing** — `/api/doThing` POST endpoints ignoring resource/verb conventions entirely.
- **Always-200** — every response returns `200 OK` with a `{success: false, error: "..."}` body, forcing clients to parse bodies to detect failure.
- **Unbounded lists** — `GET /items` returning the entire table with no pagination, a latent incident.
- **Inconsistent envelopes** — some endpoints return raw arrays, others `{data: [...]}`, others `{results: [...], items: [...]}` interchangeably.
- **Silent breaking changes** — modifying an existing endpoint's response shape without versioning, breaking every consumer without warning.
