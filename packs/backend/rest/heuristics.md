# Heuristics — REST Pack

- URL with a verb (`/createOrder`, `/getUserById`) → refactor to noun + method (`POST /orders`, `GET /users/:id`).
- Endpoint always returning `200` even on failure with an error field in the body → fix status codes, clients shouldn't have to parse the body to know if it failed.
- Unbounded list endpoint → add pagination before it becomes a production incident.
- Inconsistent response shape across endpoints (`{data: ...}` here, raw object there) → standardize the envelope.
