# Glossary — Philosophy of Software Design Pack

Terms this pack uses precisely. Several are used loosely elsewhere in the industry; the
entry says which sense is meant here.

- **Complexity** — anything about a system's structure that makes it hard to understand or
  change. Not size, not cleverness, not file count.
- **Change amplification** — a conceptually small change requiring edits in many places.
  The most measurable complexity symptom: read the diff.
- **Cognitive load** — how much a developer must hold in mind to work in an area. Used here
  about *code*; `ux/laws-of-ux` uses the same phrase about interfaces, which is a different
  claim about a different reader.
- **Unknown unknowns** — when it isn't apparent what must change, or what a change will
  break. The most dangerous symptom, because the developer cannot know they are wrong.
- **Dependency** — code that cannot be understood or changed in isolation. Broader than an
  import: a shared format convention is a dependency.
- **Obscurity** — important information that isn't apparent from the code.
- **Module** — any unit with an interface and an implementation: a function, class, file,
  package, or service. The depth model applies at every scale.
- **Deep module** — simple interface, substantial hidden functionality. The goal.
- **Shallow module** — interface nearly as complex as the implementation it hides, so the
  caller pays the abstraction's cost and gains little.
- **Depth** — informally, functionality divided by interface. Makes decomposition a
  quantity to weigh rather than a virtue to maximize.
- **Classitis** — the belief that more, smaller classes are automatically better, producing
  many units that hide nothing while each looks admirably small.
- **Information hiding** — a module holding a design decision its callers don't need. The
  mechanism that makes modules deep.
- **Information leakage** — the same design decision known to two or more modules. Coupling
  without an import, and the single most useful thing to look for in review.
- **Temporal decomposition** — splitting modules by the order operations happen in (read,
  then transform, then write). Produces leakage by construction, because format knowledge
  lands in more than one stage.
- **Pull complexity downward** — the module implementer absorbs an awkward case so every
  caller doesn't. Complexity is movable, and where it sits decides what it costs.
- **Pass-through method** — a method that forwards to another, adding no abstraction.
- **Pass-through variable** — a value threaded through several frames purely to reach a
  distant consumer.
- **Define errors out of existence** — changing an operation's semantics so a condition is
  normal rather than exceptional. Exception count is a design variable, not a fact about the
  domain.
- **Somewhat general-purpose interface** — one operation covering a family of needs rather
  than a method per caller. "Somewhat" bounds it: generality without a present consumer is
  speculation.
- **Design it twice** — sketching a genuinely different second approach before committing.
  Applied proportionally, to decisions that are expensive to reverse.
- **Strategic programming** — done means the design is one you'd want to extend. A small
  continuous investment in every change.
- **Tactical programming** — done means it works. Correct for prototypes, corrosive as a
  default.
- **Tactical tornado** — the highest-output developer who raises everyone else's cost,
  hard to challenge because each individual change is defensible.
- **Obviousness** — a reader forms the correct impression quickly and without effort. A
  property of the reader, so the author cannot judge it; a reviewer's confusion is data.
- **Interface comment** — describes what a caller needs and deliberately excludes
  implementation detail, so it doesn't change when the implementation does.
- **Red flag** — a symptom worth investigating rather than a rule violation. Most of this
  pack's findings are red flags, which is why none of them block.
