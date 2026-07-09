# Decision Framework — SOLID Pack

## Apply now vs. defer

| Signal | Action |
|--------|--------|
| Second real implementation/variant exists or is imminent | Apply the relevant principle now |
| Only one implementation exists, no second planned | Defer — inline is fine |
| A class is edited by two unrelated teams/features regularly | SRP split now |
| A class is stable, edited rarely, by one owner | Leave it, even if "impure" |
| A test needs isolation from slow I/O | DIP interface now, for that dependency only |

## Which principle addresses this pain?

- "Every change to this class breaks something unrelated" → SRP.
- "Adding a new type means editing five existing files" → OCP.
- "This subclass throws when I call the base method" → LSP (reconsider the hierarchy).
- "This class has ten stub methods" → ISP.
- "I can't test this without a live database" → DIP.

## Balancing SOLID against YAGNI

Default to the simplest structure that passes current tests and requirements. Introduce a SOLID-motivated abstraction only when: (a) the pain it addresses is already occurring, or (b) a second concrete case is confirmed, not merely conceivable. Record deferred cases as a tripwire comment rather than building the abstraction speculatively ([core decision framework](../../../core/decision-framework.md)).

## Refactoring toward SOLID incrementally

Don't stop feature work for a SOLID pass. Apply the relevant principle exactly to the code you're already touching for a feature/bugfix; leave adjacent violations alone unless they block the current change.
