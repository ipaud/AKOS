# Philosophy — Clean Architecture Pack

## The database and the framework are details

Business rules are why the software exists; the database, the web framework, the UI toolkit are how it's currently delivered. Details change more often and more cheaply than rules should. Architecture that lets frameworks dictate structure inverts the relationship of what should depend on what — the important thing (rules) ends up depending on the unimportant thing (delivery), and every framework upgrade or migration becomes a rewrite.

## Dependencies point inward, toward policy

The dependency rule: source code dependencies point only inward, toward higher-level policy. Inner circles (entities, use cases) know nothing about outer circles (controllers, databases, UI). Outer circles depend on interfaces the inner circles define — dependency inversion, not just layering. This is what makes the core testable without a database, a browser, or a network.

## Testability is the tell, not the goal

The practical signal that the dependency rule holds: can the business rules be tested with plain objects, no framework, no I/O, in milliseconds? If testing a use case requires spinning up a database or mocking a web framework, the rule has already been broken — the fix is architectural, not "write better mocks".

## Screaming architecture

A codebase's top-level structure should announce what the system *does* (place-order, manage-inventory) not what framework it's built with (controllers/, models/, views/). Frameworks are visible in the outer ring; the system's purpose is visible at a glance from folder names — the opposite of most generated-scaffold layouts.

## Boundaries cost, so cross them deliberately

Every architectural boundary (interface, layer, indirection) buys isolation at the price of complexity. Clean Architecture is not "always use four rings" — it's "know where your boundaries are, and put them where change actually happens or testability actually matters". Applying it uniformly to every CRUD screen in a small app is the methodology's most common misuse.
