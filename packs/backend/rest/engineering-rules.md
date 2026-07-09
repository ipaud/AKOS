# Engineering Rules — REST Pack

- RR1. URLs contain nouns/resource identifiers only; actions are expressed via HTTP method.
- RR2. Status codes match outcome: 2xx only for actual success, error responses use appropriate 4xx/5xx.
- RR3. List endpoints are paginated with a maximum enforced page size (ties to [AP4](../../security/owasp-api-top-10/engineering-rules.md)).
- RR4. API versioning strategy is explicit (URL path `/v1/` or header-based); breaking changes bump version.
- RR5. Response envelope shape (success and error) is consistent across all endpoints in the API.
- RR6. Error responses include a stable machine-readable error code plus a human-readable message.
- RR7. GET requests have no side effects; PUT/DELETE are safely repeatable.
