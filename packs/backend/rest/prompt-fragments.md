# Prompt Fragments — REST Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply REST API design practice (AKOS L2):
- URLs name resources, never actions: POST /orders and GET /orders/:id,
  not /createOrder or /getOrderById. The HTTP method is the verb.
- Status codes carry the outcome: 201 with the created resource, 204 for
  a successful delete with no body, 400 malformed, 401 unauthenticated,
  403 authenticated but forbidden, 404 absent, 409 conflict, 422
  semantically invalid, 5xx server fault. Never return 200 with an error
  body — clients must not parse a body to learn that a call failed.
- GET is side-effect free and safe to retry or cache. PUT and DELETE are
  idempotent: repeating them lands on the same final state. Reserve POST
  for non-idempotent creation and actions.
- Every list endpoint is paginated with a default page size and an
  enforced maximum. No endpoint may return an unbounded collection.
- One response envelope across the whole API: the same success shape, the
  same error shape, the same pagination fields on every endpoint.
- Errors carry a stable machine-readable code plus a human-readable
  message. The code is part of the contract; the message is not.
- Breaking changes bump an explicit version (URL path unless there is a
  reason otherwise). Serve the old version through a stated deprecation
  window with a published sunset date. Never reshape a live response.
```

## Fragment: review lens

```text
Review this API as a REST contract reviewer:
1. Resource modelling — list every route. Flag verbs in paths and any
   endpoint that is RPC wearing REST's clothes.
2. Status codes — for each endpoint, map every outcome to the code it
   actually returns. Flag always-200, 200-with-error-body, blanket 500s
   for client mistakes, and 404 used where 403 is meant.
3. Method semantics — any GET with side effects? Any PUT or DELETE that
   breaks or errors on a repeat call?
4. Pagination — any list route without pagination or without an enforced
   maximum page size? Name the collection that grows unbounded.
5. Envelope — diff the response shapes across endpoints. Flag every
   inconsistency (raw array here, {data} there, {results} elsewhere).
6. Errors — stable machine-readable code present, or only prose?
7. Versioning — is the strategy explicit, and does any recent change
   alter an existing response shape without a version bump?
Report by severity per review-checklist.md, naming the route, the method,
and the corrected contract.
```

## Fragment: new-endpoint design pass

```text
Before implementing an endpoint, state its contract:
- Resource and path (nouns only), method, and why that method.
- Request shape, with every field validated and its failure code named.
- Success status and response body, inside the API's standard envelope.
- Every error case, each mapped to a status code and a stable error code.
- If it returns a collection: pagination style (cursor for large or
  frequently-changing data, offset for small stable sets), default and
  maximum page size, and the sort that makes paging deterministic.
- Idempotency: is repeating this call safe? If not and retries are
  likely, accept an idempotency key.
- Authorization: who may call it, checked server-side per object.
Write the contract first; implement against it.
```

## Fragment: breaking-change triage

```text
Classify each proposed API change:
- Non-breaking — new optional request field, new response field, new
  endpoint, a relaxed validation rule. Ship it in place.
- Breaking — removed or renamed field, changed type or units, narrowed
  validation, changed status code, changed pagination or envelope shape.
For anything breaking: bump the version, serve old and new concurrently,
publish the sunset date, and mark the old version deprecated in docs and
in a response header. Silently reshaping a live response breaks every
consumer at once with no signal — it is never an acceptable path.
```

## One-liner (for tight token budgets)

```text
REST rules: resource nouns in URLs and HTTP methods as verbs; status
codes that match the real outcome, never 200-with-error-body; GET safe,
PUT/DELETE idempotent; every list paginated with an enforced max page
size; one envelope across the API; errors with a stable machine-readable
code plus a human message; breaking changes versioned and served through
a published deprecation window, never reshaped in place.
```
