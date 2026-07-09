# Philosophy — Design Patterns Pack

## Patterns are vocabulary, not virtue

A pattern's value is shared naming for a recurring problem-solution shape, so a team can say "make it a Strategy" instead of drawing the diagram every time. That's a communication win, not a quality guarantee. Applying a pattern where the underlying problem doesn't exist buys the pattern's complexity (extra classes, indirection, an interface to maintain) for zero payoff — this is the single most common misuse of this entire catalog, and it's why every pattern in this pack is framed by its trigger condition first.

## The problem is the unit, not the pattern

The Gang of Four catalog is organized around recurring problems: "I need to create objects without specifying the exact class" (Factory), "I need interchangeable algorithms" (Strategy), "I need to notify dependents of a change" (Observer). Reach for a pattern by first naming the problem in plain language; if the problem doesn't exist yet, neither should the pattern.

## Language and platform features absorb many patterns

Many classic patterns exist to work around limitations of 1990s statically-typed OOP languages. Modern languages often provide the same power natively: first-class functions absorb much of Strategy and Command; language-level iterators absorb Iterator; module systems and closures absorb parts of Singleton and Factory. Before reaching for a class-based pattern implementation, check whether the language already has a simpler native form.

## Composition over inheritance, almost always

The catalog's most durable meta-lesson: prefer composing small, focused objects/functions over building inheritance hierarchies for variation. Strategy, Decorator, and Composite exist specifically because inheritance-based variation (subclass explosion, fragile base classes) breaks down at moderate complexity, and object composition doesn't.
