# Engineering Rules — DDD Pack

- DR1. Class, method, and variable names in the domain layer match the ubiquitous language used by domain experts — verified against a maintained glossary for the core subdomain.
- DR2. Value objects are immutable; equality is structural (by value), not by reference/identity.
- DR3. Entities implement identity-based equality; two entities are never equal solely because their attributes match.
- DR4. Code outside an aggregate references other aggregates only by ID, never holds a direct object reference across the boundary.
- DR5. Invariants that must always hold are enforced inside the aggregate root's methods — never left to be enforced by calling code from outside.
- DR6. Cross-aggregate and cross-bounded-context effects are triggered via domain events, not direct method calls reaching into another aggregate's internals.
- DR7. Integration with external systems or other teams' contexts passes through an explicit translation layer (anti-corruption layer); external model types never appear directly in the domain layer.
- DR8. Repositories operate at the aggregate-root granularity — no repository for a non-root entity.
- DR9. Full tactical pattern set (DR2–DR8) is applied only within identified core/complex subdomains; supporting subdomains may use simpler CRUD-style code without penalty.
