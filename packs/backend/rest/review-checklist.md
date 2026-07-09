# Review Checklist — REST Pack

## High
- [ ] URLs are nouns; verbs expressed via HTTP method. (RR1)
- [ ] Status codes match actual outcome. (RR2)
- [ ] List endpoints paginated with max page size. (RR3)

## Medium
- [ ] Versioning strategy explicit for breaking changes. (RR4)
- [ ] Consistent response envelope across the API. (RR5)
- [ ] Error responses have machine-readable code + message. (RR6)

## Low
- [ ] GET has no side effects; PUT/DELETE idempotent. (RR7)
