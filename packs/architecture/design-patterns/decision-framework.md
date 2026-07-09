# Decision Framework — Design Patterns Pack

## Should I apply a pattern here?

1. Name the concrete pain in plain language (not "I should use Strategy" but "this if/else chain grows every time we add a payment method").
2. Does a GoF pattern's trigger condition match? (See [principles.md](principles.md).)
3. Does the language already solve this more simply (closures, first-class functions)? If yes, use that.
4. Does the trigger condition currently exist (≥2 real cases), or is it hypothetical? Hypothetical → defer (YAGNI; same rule as [SOLID OCP](../solid/decision-framework.md)).
5. Apply the named pattern, using its standard shape (so the name means something to the next reader) — don't invent a "pattern-ish" variant that shares the name but not the structure.

## Choosing between similar-looking patterns

- Need to add behavior to *individual instances* dynamically → Decorator. Need to add behavior to *all instances of a type* → subclass or just edit the method.
- Need to swap an *entire algorithm* → Strategy. Need to override *specific steps* of a shared algorithm → Template Method.
- Need object creation logic centralized for *one product line* → Factory Method. Need it for *families of related products* → Abstract Factory (rare; usually overkill below multi-product-line complexity).

## When NOT to reach for the catalog at all

Small scripts, prototypes, and low-complexity CRUD rarely benefit from named patterns — plain functions and straightforward classes communicate better to a small team than a Factory-Strategy-Observer assembly for three use cases.
