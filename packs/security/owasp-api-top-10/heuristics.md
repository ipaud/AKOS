# Heuristics — OWASP API Security Pack

- **The ID-swap test:** for every endpoint accepting an object ID, authenticate as user A, then request user B's object ID — does it return B's data? (API1)
- **The mass-assignment test:** send an update request with an extra field the UI never exposes (`isAdmin`, `role`, `balance`) — does the server silently accept it? (API3)
- **The unbounded-list test:** call a list/search endpoint with no pagination params, or a huge `limit` — does it return everything, unbounded? (API4)
- **The admin-endpoint-as-regular-user test:** as a non-privileged user, directly call an admin-only endpoint URL — does it check role, or just check "is authenticated"? (API5)
- **The bot-economics test:** could this flow (signup, checkout, redemption) be automated at scale to extract value (inventory hoarding, spam accounts, coupon abuse) profitably? If yes and there's no rate limit/anti-automation, that's API6.
- **The CORS wildcard check:** grep for `Access-Control-Allow-Origin: *` combined with `Access-Control-Allow-Credentials: true` — that combination is almost always a misconfiguration. (API8)
- **The "what APIs do we actually have" audit:** compare the API gateway/router's registered routes against the official API documentation — undocumented live routes are shadow APIs. (API9)
- **The third-party trust check:** does code calling an external API validate the response shape before using it, or does it trust and directly deserialize into internal types? (API10)
