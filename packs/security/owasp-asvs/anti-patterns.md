# Anti-Patterns — OWASP ASVS Pack

## No stated target level

A production app with no documented security bar — every review becomes a subjective argument about "is this secure enough" with no shared reference point. Fix: AV1 — state the target level explicitly.

## Scattered authorization logic

Twelve endpoints, twelve slightly different implementations of "check if user owns this resource," some subtly buggy. Fix: AS2, AV2 — one canonical mechanism.

## API-only access control

Authorization enforced at the API layer but the database is directly reachable (via a BI tool, a debug console, an admin script) with no equivalent row-level restriction — an alternate path bypasses the control entirely. Fix: AV5 — enforce at every layer capable of reaching the data.

## Denylist validation

Trying to enumerate "forbidden" characters/patterns for input validation, which is trivially bypassed by anything the list-writer didn't think of. Fix: AV6 — allowlist the valid shape instead.

## Undocumented crypto key handling

Encryption keys hardcoded, shared across environments, or nobody currently at the company knows how they're rotated (if ever). Fix: AV7 — documented key management.

## Sequence-blind checkout

A checkout API where `POST /confirm-payment` can be called before `POST /calculate-total`, using stale or attacker-supplied pricing data, because no server-side state machine enforces step order. Fix: AS9, AV9.

## "It worked in staging" configuration drift

Production accidentally running with debug mode on, verbose errors enabled, or a staging CORS wildcard — because configuration was never diffed against the intended environment-specific baseline. Fix: AV10.

## L3 cargo-culting

A small internal tool adopting L3-level ceremony (extensive formal threat modeling, advanced cryptographic key ceremonies) because "more security is always better," burning effort disproportionate to actual risk. Fix: decision-framework — match level to actual stakes.
