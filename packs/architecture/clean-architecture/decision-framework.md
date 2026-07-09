# Decision Framework — Clean Architecture Pack

## When to apply full ring separation

| Signal | Apply |
|--------|-------|
| Multiple delivery mechanisms (REST + CLI + worker) share logic | Yes — one core, multiple thin adapters |
| Persistence technology likely to change or needs swapping (multi-tenant, migration planned) | Yes — repository interfaces |
| Small internal tool, single delivery mechanism, unlikely to change | No — two-layer (domain + everything) is enough |
| Prototype / Startup MVP profile | No — YAGNI; note the tripwire, don't build the ring |
| Production / Enterprise profile, core logic complex and long-lived | Yes |

## When NOT to over-apply

- CRUD screens with no business rules beyond validation don't need a use-case layer — a thin service or even direct repository call is honest.
- Don't add a repository interface for a database you will never swap; add it when a second implementation is actually planned or testability demands a fake.
- Don't let ring-count become a code-review ritual ("where's your use-case layer?") on a feature that's three lines of logic.

## Choosing rings vs hexagonal vocabulary

Use whichever the team already speaks fluently; they're isomorphic. Don't introduce a second vocabulary for the same idea mid-codebase.

## Retrofitting into a tangled codebase

1. Identify the highest-value business rule currently entangled with framework/DB code.
2. Extract it behind an interface; write the humble wrapper around the existing entangled call.
3. Test the extracted logic in isolation; leave the rest tangled until it needs to change.
4. Repeat opportunistically — don't schedule a big-bang rewrite ([R9 conflict ruling](../../../core/conflict-resolution.md): consistency migrates globally or not at all, but migration can be incremental per-module).
