# Philosophy — OWASP API Security Pack

## APIs expose the data model directly — that's the risk surface

A traditional web app mediates data access through server-rendered views that only ever show what the developer chose to render. An API exposes the underlying data model's shape directly to any client that can send a request — which means every object, every field, and every function the API can touch is a potential exposure point, reachable by anyone who can construct a valid request, not just by clicking through a UI a developer designed. This is why authorization has to be checked at the *object* and *field* level, not just "is this user logged in."

## The UI is not a security control

API endpoints are frequently more permissive than the UI that "normally" calls them, because the UI hides buttons/fields the backend still accepts. Attackers don't use your UI — they read your API responses, guess or enumerate your endpoint patterns, and send requests your UI never would. Every API security control must assume a client that ignores the UI's constraints entirely.

## Automation changes the threat model

Because APIs are built to be called programmatically, business-flow abuse (buying up all inventory via bots, mass account creation, credential-stuffing at API scale) is a first-class API risk category (API6) that a traditional web-focused threat model under-weights. Rate limiting and anti-automation aren't just performance controls — they're security controls specific to APIs.

## Inventory is a security property

An API you don't know exists (an old version left running, a debug/internal endpoint accidentally exposed, staging infrastructure indexed by search engines) is unpatched by definition — nobody is applying fixes to something nobody's tracking. API9's inclusion reflects that discovery of forgotten endpoints is one of the most common real-world API breach vectors, entirely preventable by inventory discipline rather than code-level fixes.
