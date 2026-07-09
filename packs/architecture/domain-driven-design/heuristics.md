# Heuristics — DDD Pack

- **The glossary test:** ask a domain expert and a developer to independently define five core terms; mismatches point straight at translation-loss bugs waiting to happen.
- **The "and" boundary test:** if describing a context requires "and" for unrelated concerns (Sales *and* Support *and* Billing all as one "Customer" model), that's likely 2-3 bounded contexts wearing one name.
- **Primitive obsession scan:** grep for raw strings/numbers doing a value object's job (email as `string` validated in six different places) — candidates for DD4.
- **Aggregate size check:** if a transaction commonly loads/locks far more than it needs to enforce one invariant, the aggregate is too big; if two aggregates are always updated together in the same transaction, they might be one aggregate.
- **Reach for full tactical DDD only in the core, complex subdomain** — the one the business actually differentiates on. Supporting subdomains (user profile settings, admin tooling) rarely earn it.
- **Context-map before microservices.** If a team can't draw bounded contexts on a whiteboard, splitting into services will just distribute the confusion over a network.
- **New feature naming friction is a modeling signal**, not a bikeshed — when a name doesn't fit, the model (not just the word) is usually slightly wrong.
