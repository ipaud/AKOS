# Principles — Design Patterns Pack

Each entry: trigger condition → pattern → the plain alternative when the trigger is absent.

## Creational

- **DP1 — Factory Method:** trigger = object creation logic varies by subtype and callers shouldn't know which concrete class they get. Absent trigger → a plain constructor call is simpler.
- **DP2 — Builder:** trigger = constructing an object requires many optional parameters or a multi-step assembly process. Absent trigger → a plain constructor or object literal.
- **DP3 — Singleton:** trigger = exactly one instance must exist and be globally reachable (rare — usually a smell for hidden global state; prefer dependency injection of a single shared instance over a Singleton class).

## Structural

- **DP4 — Adapter:** trigger = an existing interface doesn't match what a client expects, and you can't change either side. Absent trigger → just call the API directly.
- **DP5 — Decorator:** trigger = behavior needs to be added to individual objects dynamically, without subclassing every combination. Absent trigger → a single method/subclass is fine.
- **DP6 — Facade:** trigger = a subsystem is complex and most callers only need a simple subset of it. Absent trigger → expose the subsystem directly.
- **DP7 — Composite:** trigger = clients need to treat individual objects and groups of objects uniformly (tree structures, nested UI components).

## Behavioral

- **DP8 — Strategy:** trigger = an algorithm needs to vary independently of the client using it, with ≥2 real interchangeable implementations. Absent second implementation → inline the logic (see [SOLID OCP overuse guard](../solid/principles.md)).
- **DP9 — Observer:** trigger = one or more objects need to react to state changes in another, without tight coupling. Modern equivalents: event emitters, reactive streams, pub/sub.
- **DP10 — Command:** trigger = an action needs to be represented as an object (for queuing, undo, logging, or deferred execution). Absent trigger → a plain function call.
- **DP11 — State:** trigger = an object's behavior changes substantially based on internal state, and state-transition logic is sprawling across conditionals. Absent trigger → a simple enum + switch is fine for a handful of states.
- **DP12 — Template Method:** trigger = several classes share an algorithm's skeleton but vary specific steps. Modern equivalent often: a higher-order function taking the varying step as a parameter.

## Meta-principle

- **DP13 — Check for a native language feature first.** First-class functions, closures, and module systems often replace Strategy, Command, Iterator, and Singleton with less ceremony than a class hierarchy.
