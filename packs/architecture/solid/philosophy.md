# Philosophy — SOLID Pack

## Principles about change, not purity

SOLID isn't a style guide — each letter names a specific way software becomes expensive to change, and a specific class-design move that prevents it. Code that violates SRP is expensive to change because unrelated concerns force unrelated edits into the same file. Code that violates OCP is expensive to extend because new behavior means editing existing, tested code. The unifying question SOLID asks of any design: *when requirement X changes, how much of the system has to move?*

## Cohesion and coupling are the real substance

Strip the acronym and SOLID is a restatement of two older ideas: maximize cohesion (things that change together live together — SRP), minimize coupling (things that change independently don't know about each other's concrete details — DIP, ISP). LSP and OCP are consequences of getting abstraction boundaries right; when they're violated, it's usually because an abstraction was drawn in the wrong place, not because "polymorphism wasn't used enough".

## Applied to the wrong grain, SOLID produces the opposite of its goal

Taken to extremes — one-method classes, an interface for every class, inheritance hierarchies built for hypothetical future subclasses — SOLID produces exactly the fragility and indirection tax it was meant to prevent. The principles are diagnostic tools applied *when a change is actually painful*, not upfront ceremony applied to every class regardless of its stability. This pack pairs every principle with its overuse anti-pattern for that reason.
