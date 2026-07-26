# Principles — Philosophy of Software Design Pack

Durable rules for treating complexity as the thing being managed, rather than a
by-product to apologize for. Level 3: these are decision frameworks, not commandments —
see [decision-framework.md](decision-framework.md) for when they don't apply. The `PSD*`
codes in [engineering-rules.md](engineering-rules.md) derive from these.

## What complexity is

- **P1 — Complexity is whatever makes a system hard to understand or change.** Not line
  count, not cleverness, not the number of files. If a competent newcomer can't work out
  where to make a change and what it will break, the system is complex — regardless of
  how tidy it looks.
- **P2 — Complexity shows up as three symptoms, and each is diagnosable.** *Change
  amplification*: a conceptually small change touches many places. *Cognitive load*: how
  much a developer must hold in their head to work here. *Unknown unknowns*: it isn't
  even clear what must be changed, which is the worst of the three because no amount of
  reading the call site reveals it.
- **P3 — Complexity has exactly two causes: dependencies and obscurity.** A dependency is
  when code cannot be understood or changed in isolation. Obscurity is when important
  information isn't apparent. Every technique in this pack reduces one or the other, and
  a technique that reduces neither is decoration.
- **P4 — Complexity is incremental, which is why it wins.** No single change makes a
  system unmaintainable; a thousand small acceptable ones do. It follows that there is no
  threshold below which a mess is too small to matter — the tolerance itself is the
  mechanism.

## Modules

- **P5 — A module's value is its functionality divided by its interface.** *Deep*: simple
  interface, substantial behavior behind it. *Shallow*: an interface nearly as complicated
  as the implementation it hides, so the caller pays the full cost of the abstraction and
  receives almost nothing.
- **P6 — Splitting something in two adds interface, and interface is cost.** Decomposition
  is not free and not automatically good. More, smaller units means more boundaries to
  learn, more call chains to trace, and more places for information to leak. The question
  is never "is this big?" but "does the split hide something?"
- **P7 — Interfaces should be simpler than implementations, and the implementer is the one
  who should suffer.** Pull complexity downward: a single module maintainer absorbing an
  awkward special case is cheaper than every caller handling it. A configuration
  parameter is often complexity pushed upward onto people less equipped to decide.
- **P8 — Information hiding is the mechanism; information leakage is the failure.** When
  the same design knowledge — a file format, an encoding, a protocol detail — appears in
  two modules, they are coupled whether or not they call each other. Leakage is the single
  most useful thing to look for in a review, because it predicts change amplification.
- **P9 — Decompose by knowledge, not by chronology.** Splitting modules along the order
  operations happen in (read, then process, then write) guarantees leakage, because the
  same format knowledge lives in the reader and the writer. Group by what a unit knows,
  not by when it runs.
- **P10 — A somewhat general-purpose interface is usually deeper than a special-purpose
  one.** Designing for the single caller you have today tends to produce a narrow method
  per use case; designing one slightly more general operation often produces fewer, deeper
  methods and less total code. "Somewhat" is load-bearing — this is not a licence to build
  frameworks nobody asked for.
- **P11 — Each layer should offer a different abstraction.** When adjacent layers say
  nearly the same thing, the layer is paying its cost without earning it: a method that
  only forwards to another, a variable threaded through five frames to reach the one place
  that reads it, a wrapper that renames its arguments.

## Errors and special cases

- **P12 — The best way to handle an exception is to remove the situation that raises
  it.** Define errors out of existence: make the operation's semantics absorb the edge
  case so there is nothing to signal. Fewer places where things can go wrong beats more
  places that handle it correctly, because the second still costs every caller a branch.
- **P13 — Special cases belong inside the normal case, not beside it.** Every `if` that
  exists because "this one time is different" is a permanent tax on reading the code.
  Design the normal path so the special input is simply an instance of it.

## Working

- **P14 — Design the thing twice before building it once.** The first structure that comes
  to mind is a sample of one. Sketching a genuinely different second approach — not a
  variation — reliably produces a better third. This is cheap compared to discovering the
  problem after the code exists.
- **P15 — Strategic beats tactical, and the difference is what "done" means.** Tactical
  work stops when the feature works. Strategic work stops when the design is one you'd
  want to extend. The investment is small and continuous — a fraction of the time, every
  change — not a rewrite scheduled for later.
- **P16 — Comments exist to record what the code cannot say.** Not what it does; what a
  reader cannot recover from reading it — intent, invariants, units, why the obvious
  approach was rejected. A comment restating the next line is noise, and its presence is
  usually a sign the naming failed.
- **P17 — Write the interface comment before the implementation.** Doing so is a design
  test, not documentation work: if the description of what a unit does is long, awkward,
  or full of conditions, the abstraction is wrong and no amount of implementation will fix
  it. This is the cheapest design review available.
- **P18 — Naming is precision work, and vagueness in a name is a design smell.** A name
  that could describe two different things means the thing itself probably is two things.
  Consistency matters more than elegance: the same concept keeps the same word everywhere.
- **P19 — Obviousness is a property of the reader, not the author.** "Obvious" means a
  reader forms the correct impression quickly and without effort. Since the author cannot
  judge this about their own code, it is measured by asking someone else, and their
  confusion is data rather than an objection.

## Scope

This pack is about the cost of understanding and changing code: module depth, information
hiding, abstraction boundaries, error design, comments, and naming. It does not cover
which dependency points where ([clean-architecture](../clean-architecture/README.md)),
class-level responsibility rules ([solid](../solid/README.md)), named structural solutions
([design-patterns](../design-patterns/README.md)), the mechanics of restructuring
([martin-fowler-refactoring](../martin-fowler-refactoring/README.md)), or modeling a
complex domain ([domain-driven-design](../domain-driven-design/README.md)).

It also **partially disagrees** with the common reading of `solid` and
`clean-architecture` on how small units should be. That disagreement is deliberate and
resolved explicitly in [decision-framework.md](decision-framework.md) — do not paper over
it, and do not treat this pack as licence to write large tangled units.
