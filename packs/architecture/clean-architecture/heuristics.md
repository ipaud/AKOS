# Heuristics — Clean Architecture Pack

- **The import test:** open a use-case file; if it imports anything from a framework/ORM/HTTP library, that's a boundary violation — extract an interface.
- **The unplug test:** could business logic be tested by unplugging the database and web framework entirely, using in-memory fakes? If no, the dependency rule isn't holding yet.
- **The screaming test:** look at top-level folders; do they say "orders, billing, shipping" or "controllers, models, services"? The latter is framework-organized, not business-organized.
- **Start simpler than you think.** New project, small team → two layers (domain + everything else) beats four rings prematurely; add rings when a second delivery mechanism, a second persistence technology, or serious testability pain actually appears.
- **Boundary placement follows the volatility axis.** Put interfaces where things are likely to change independently (payment providers, notification channels) — not around stable, unlikely-to-change internals.
- **When in doubt, favor the simpler structure and a documented tripwire** ("add a repository interface here if we ever support a second database") over speculative abstraction today.
- **Watch for anemic use cases:** a use case that's just `repo.save(request)` with no rules is a sign the "rule" belongs in the entity, or that this operation didn't need a use-case layer at all.
