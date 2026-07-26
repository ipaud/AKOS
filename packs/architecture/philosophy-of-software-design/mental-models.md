# Mental Models — Philosophy of Software Design Pack

The named models this source contributes. Reach for these when reasoning about a design;
the [engineering rules](engineering-rules.md) are what these models produce once code
exists.

## Module depth

Picture a module as a rectangle: width is the interface a caller must learn, height is the
functionality hidden behind it. **Deep** is tall and narrow — a lot of behavior reached
through a small opening. **Shallow** is short and wide — you learn nearly as much to use it
as you would to write it.

The value of the model is that it makes decomposition a *quantity* rather than a virtue.
Splitting always adds width; it only pays when it adds more height than width. This is why
"is this file too long?" is the wrong question and "what does this hide?" is the right one.

## The three symptoms

How complexity announces itself, in increasing order of danger:

1. **Change amplification** — a small conceptual change requires edits in many places. The
   cheapest to measure: the diff tells you.
2. **Cognitive load** — how much a developer must hold in mind to work here. Measured by
   watching someone new, not by introspection.
3. **Unknown unknowns** — it isn't clear what needs changing, or what will break. The worst
   because reading the call site does not reveal it, and the developer cannot know they are
   about to be wrong.

Use this as a triage vocabulary in review: naming which symptom a finding produces is what
turns "this feels messy" into something actionable.

## The two causes

Everything reduces to **dependencies** (code that cannot be understood or changed in
isolation) and **obscurity** (important information not apparent). A proposed improvement
that removes neither is decoration — a useful filter for design debates that have gone on
too long.

## Complexity as sediment

No single commit makes a system unmaintainable. Each one adds a thin layer that looked
acceptable in isolation, and the accumulation is the whole story. Two consequences worth
holding: there is no "too small to matter" threshold, and the cause of today's mess is
distributed across a year of individually defensible decisions, so looking for the commit
that broke it is wasted effort.

## Pulling complexity down

Complexity in a system is not conserved — it can be *moved*, and where it sits determines
what it costs. A module absorbing an awkward case pays once; the same case pushed to
callers is paid N times, by people with less context. Configuration parameters, thrown
exceptions, and required call ordering are all complexity travelling upward.

Asymmetry is the point: the implementer suffers so the callers don't. A design that makes
the implementation elegant and the calling code careful has it backwards.

## Defining errors out of existence

Three ways to reduce error-handling cost, in order of preference:

1. **Redefine the semantics** so the condition is normal — deleting an absent file
   succeeds, closing a closed handle succeeds.
2. **Mask it** in the module where it occurs, so callers never learn of it.
3. **Aggregate** handling at one boundary, where many failures share one recovery.

Only after all three fail does a caller-visible exception earn its place. The insight is
that exception *count* is a design variable, not a fact about the domain.

## Design it twice

The first design that comes to mind is a sample of size one, and its main property is that
it was first. Producing a second, genuinely different option — not a variation — reliably
improves the third, and often reveals that the first was shaped by an accident of how the
problem was described.

Applies proportionally: to schemas, public interfaces, and module boundaries, not to
helper functions.

## Strategic vs tactical

**Tactical**: done means it works. **Strategic**: done means the design is one you'd want
to extend. The difference is not effort in a single sitting — it is a small, continuous
fraction of every change, which is why "we'll clean it up later" is structurally different
and does not work.

The *tactical tornado* is the person producing the most visible output while raising
everyone else's cost, and the reason they're hard to challenge is that each individual
change is defensible.

## Comments as a design tool

Writing the interface comment *first* tests the abstraction before any code exists. A
description that is long, conditional, or awkward is evidence the boundary is wrong — and
it is the cheapest such evidence available, since the alternative is discovering it after
the implementation.

The corollary: comments record what code cannot express. If a comment could be replaced by
a better name, replace it with the better name.
