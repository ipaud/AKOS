# Glossary — REST Pack

- **Resource** — a noun-identified entity exposed by the API (e.g. `/orders/:id`).
- **Idempotency** — a request that produces the same result no matter how many times it's repeated.
- **HATEOAS** — Hypermedia as the Engine of Application State; the full theoretical REST discovery model.
- **Envelope** — the consistent wrapper shape (`data`/`error`/`meta`) around API responses.
- **Cursor pagination** — pagination using an opaque pointer rather than an offset, robust to concurrent inserts.
