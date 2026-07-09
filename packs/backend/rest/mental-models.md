# Mental Models — REST Pack

- **Resources as nouns, verbs as HTTP methods:** `/orders/:id` + `DELETE` expresses "delete this order" without a verb in the URL.
- **Status codes as a semantic layer:** 2xx success, 3xx redirect, 4xx client error, 5xx server error — each family has consistent meaning consumers rely on for error handling logic.
- **Idempotency as a safety contract:** GET/PUT/DELETE are expected to be safely repeatable; POST is not — clients and infrastructure (retries, caches) depend on this holding true.
- **HATEOAS (hypermedia) as the theoretical ideal, rarely fully implemented:** most real APIs are pragmatically "REST-ish" (resource + verb + status code conventions) without full hypermedia discovery — that's an accepted, working middle ground, not a failure.
