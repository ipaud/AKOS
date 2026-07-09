# Mental Models — OWASP API Security Pack

## Object-level vs. function-level vs. property-level authorization

Three independent authorization checks an API must make, often confused with each other: **object-level** (can this user access *this specific record*, e.g. order #4471?), **function-level** (can this user call *this endpoint at all*, e.g. `DELETE /admin/users`?), **property-level** (can this user read/write *this specific field* on a record they can otherwise access, e.g. `isAdmin` on their own user profile?). Passing one check says nothing about the others — a user might legitimately access their own order (object ✓) but shouldn't be able to set its `status` field directly (property ✗).

## Mass assignment

Binding an entire request body directly to a data model/ORM entity without specifying which fields are actually allowed to be set. If a `User` model has an `isAdmin` field, and the update endpoint blindly applies the whole request body, an attacker can add `"isAdmin": true` to an unrelated profile-update request and gain a field they were never shown a UI control for.

## Rate limiting as a security control, not just a performance one

Beyond protecting infrastructure from load, rate limits bound the blast radius of credential stuffing, enumeration attacks, and scraping — each of which is only economically viable for an attacker at scale, so a request-per-minute/hour cap changes the attacker's cost-benefit calculation entirely, independent of any application logic bug.

## The API surface is bigger than the documented API

Shadow APIs (undocumented endpoints from feature flags, internal tools, deprecated versions still deployed) and zombie APIs (old versions kept "just in case") both count as live attack surface even though nobody's actively maintaining or securing them. An API inventory (what's deployed, what version, what's actually documented) is a prerequisite for claiming any endpoint is secured — you can't secure what you don't know is running.

## Third-party API responses are untrusted input too

A trust-boundary crossing happens not just when *your* API receives external input, but when *you* call someone else's API and consume its response — that response is still untrusted data from the perspective of your system and needs the same validation discipline as user input (API10).
