# Glossary — DDD Pack

- **Ubiquitous language** — one vocabulary shared by domain experts and code within a bounded context.
- **Bounded context** — an explicit boundary within which a model and its terms are consistent.
- **Context map** — documentation of how bounded contexts relate and translate.
- **Entity** — object defined by persistent identity, not attributes.
- **Value object** — immutable object defined entirely by its attributes.
- **Aggregate** — a consistency boundary cluster of entities/value objects with one root.
- **Aggregate root** — the sole external entry point into an aggregate.
- **Domain event** — a named, past-tense fact about something that happened in the domain.
- **Anti-corruption layer** — a translation boundary preventing an external model from leaking into the domain.
- **Core / supporting / generic subdomain** — Evans's classification by strategic importance, guiding how much modeling investment each deserves.
- **Repository** — persistence abstraction operating at aggregate-root granularity.
