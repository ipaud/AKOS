# Engineering Rules — Philosophy of Software Design Pack

Checkable in the artifact. A reviewer verifies each by reading the code, not by running a
linter — these are design properties, and most of them can only be judged against what the
module claims to hide. Parenthetical codes cite the principle in
[principles.md](principles.md).

No rule here is starred. This is a Level 3 pack: none of it is a safety floor, and every
rule yields to the constitution, to a Level 0 personal convention, and to
[R9](../../../core/conflict-resolution.md) consistency with the surrounding code.

## Module depth

- PSD1. Every module or class can be described in one sentence naming what it hides. If
  the sentence needs "and", it is probably two things. (P5, P8)
- PSD2. A public interface exposing nearly as many concepts as its implementation contains
  is flagged as shallow: the caller pays the abstraction's cost and gets little back. (P5)
- PSD3. A new class or module introduced during a change states what it hides that the
  caller no longer needs to know. "It was getting long" is not an answer. (P6)
- PSD4. Methods that only forward to another method, adding no abstraction, are removed
  and the caller talks to the real thing. (P11)
- PSD5. A variable passed through more than two frames purely to reach a distant consumer
  is a design signal: hoist it into shared context, pass the object that needs it, or move
  the consumer. (P11)
- PSD6. Adjacent layers offer different abstractions — if a layer's method names and
  signatures largely mirror the layer below, the layer is deleted or given a real job. (P11)
- PSD7. A wrapper that exists only to rename or reorder arguments is not a layer. (P11)

## Information hiding

- PSD8. The same design decision — a file format, wire encoding, retry policy, storage key
  layout — is known to exactly one module. Two modules encoding the same knowledge is
  leakage, whether or not they reference each other. (P8)
- PSD9. Modules are decomposed by what they know, not by the order in which work happens.
  A reader and a writer for the same format live together. (P9)
- PSD10. A public field, getter, or setter that exposes an implementation choice (a data
  structure, an index, a cache) is flagged; the interface should expose the operation, not
  the storage. (P8)
- PSD11. A caller that must call two methods in a fixed order to get a correct result is a
  leaked invariant: the module offers one operation that maintains it. (P8, P12)
- PSD12. Configuration parameters are justified individually. Each one asks a caller to
  decide something the module is better placed to decide, and defaults that nobody ever
  changes are complexity with no benefit. (P7)

## Interfaces

- PSD13. Interfaces are designed from what callers need to accomplish, not from what the
  implementation happens to make easy. (P7)
- PSD14. Where several call sites want narrow variants of the same operation, prefer one
  slightly more general operation over one method per variant — then verify the general
  one is genuinely simpler to describe. (P10)
- PSD15. Generality is bounded by present need: an extension point with no second consumer
  today is speculative, and is removed unless the second consumer is already scheduled.
  (P10)
- PSD16. When behavior must differ, prefer a parameter with a stated meaning over a
  boolean flag whose meaning is only recoverable at the call site. (P19)

## Errors and special cases

- PSD17. Before adding an exception or error return, the design is checked for a way to
  make the condition impossible or benign — a semantic that absorbs it rather than
  reports it. (P12)
- PSD18. Operations that are already in the desired state succeed rather than raising:
  deleting what does not exist, cancelling what has stopped, closing what is closed. (P12)
- PSD19. An exception that every caller handles identically is handled once, lower down,
  instead of at every call site. (P7, P12)
- PSD20. Special-case branches are counted during review; each one is either folded into
  the normal path or given a comment stating why it cannot be. (P13)
- PSD21. Error handling that aggregates upward — one handler for a class of failures at a
  boundary — is preferred to per-call recovery, unless recovery genuinely differs. (P12)

## Naming

- PSD22. A name is precise enough that a reader can predict what the thing does not do.
  Names like `data`, `info`, `handle`, `process`, `manager` are flagged unless the
  surrounding context genuinely supplies the missing precision. (P18)
- PSD23. One concept keeps one word across the codebase; two different concepts never
  share a word. Discovering a rename is required is a finding, not a chore to defer. (P18)
- PSD24. A name that needs a comment to be understood is changed instead of commented,
  unless the comment carries information a name could not (units, ranges, invariants). (P16)
- PSD25. Loop and block variables in non-trivial scopes are named for what they hold, not
  for their position. (P18)

## Comments

- PSD26. Interface comments describe what a caller needs — behavior, arguments, return,
  errors, invariants — and deliberately exclude implementation detail, so the comment does
  not have to change when the implementation does. (P16)
- PSD27. Comments that restate the code they sit above are deleted. (P16)
- PSD28. Non-obvious *why* is written down: why this approach over the obvious one, what
  breaks if the order changes, what external constraint forced this. (P16)
- PSD29. Units, ranges, ownership, and null/empty semantics are stated where a reader would
  otherwise guess. (P16)
- PSD30. Comments live next to what they describe, and duplicated documentation has one
  home with the others pointing at it. (P16)
- PSD31. For any non-trivial new unit, the interface comment is written before the
  implementation and treated as a design check: if it is hard to write, the abstraction is
  reconsidered rather than the comment shortened. (P17)

## Working method

- PSD32. Any design decision expensive to reverse — a schema, a public interface, a
  module boundary — is sketched two genuinely different ways before one is chosen, with
  the rejected one recorded in a sentence. (P14)
- PSD33. Every change leaves the design slightly better than it found it, or states why
  not. A change that works but degrades the structure is incomplete. (P15)
- PSD34. A change that touches many files for one conceptual reason is reported as change
  amplification, with the missing abstraction named. (P2)
- PSD35. Where a reader could not tell what a piece of code does without tracing it
  elsewhere, that is recorded as an obscurity finding, not dismissed as familiarity. (P19)
- PSD36. "Nobody understands this part" is treated as a defect with an owner, not as a
  property of the code. (P2, P19)
