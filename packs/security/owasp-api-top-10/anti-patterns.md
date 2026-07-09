# Anti-Patterns — OWASP API Security Pack

## The "authenticated is enough" assumption

An endpoint checks `if (req.user)` and stops there, serving any authenticated user's request for any object ID without ownership verification. Fix: AP1 — object-level check on every call.

## Mass-assignment-friendly update endpoints

`db.users.update(req.params.id, req.body)` — whatever fields the client sends get written directly, including ones the UI never exposed. Fix: AP3 — explicit field allowlisting via DTOs.

## Security through undocumented URLs

An admin panel or internal API reachable at a guessable-but-undocumented path, with no additional auth beyond "you'd have to know the URL." Fix: AP2, AP5 — real authentication and role checks, not obscurity.

## Unbounded list endpoints

`GET /api/orders` with no pagination limit, returning the entire table if asked — a denial-of-service vector and a data-exposure risk simultaneously. Fix: AP4 — max page size enforced server-side regardless of requested size.

## Coupon/inventory bot vulnerability

A checkout flow with no rate limiting, allowing scripted accounts to reserve all limited-inventory items or redeem a single-use coupon thousands of times via account cycling. Fix: AP6 — anti-automation on high-value flows.

## Permissive CORS with credentials

`Access-Control-Allow-Origin: *` alongside `Access-Control-Allow-Credentials: true` — a combination browsers actually reject, but frequently shipped anyway alongside a token-in-header workaround that reintroduces the same exposure. Fix: AP8 — explicit origin allowlist.

## Zombie API versions

`/api/v1/` left running and unpatched for years after `/api/v3/` became the documented default, still reachable and still vulnerable to issues fixed in later versions. Fix: AP9 — actual decommissioning, not just doc removal.

## Blind third-party trust

`const data = await thirdPartyApi.get(...); db.save(data)` — no schema validation, so a malformed or malicious third-party response flows directly into internal storage/logic. Fix: AP10 — validate before use.
