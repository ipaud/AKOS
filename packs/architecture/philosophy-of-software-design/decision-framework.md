# Decision Framework — Philosophy of Software Design Pack

Level 3: a decision framework, not a set of commandments. This file exists mostly to say
where the ideas stop applying, because the failure mode of this pack is a reviewer using
"that's shallow" as an unfalsifiable objection to any decomposition.

## Should this be split?

Splitting is justified when the split **hides something**. Work the questions in order:

1. **What will the new unit hide from its caller?** If the caller still needs to know the
   same things afterwards, the split added an interface and hid nothing — don't.
2. **Will the two halves change for different reasons?** Different reasons to change is
   the strongest signal a boundary is real.
3. **Would the same knowledge now live on both sides?** If a format, ordering rule, or
   encoding has to be understood by both, splitting *creates* coupling. Group by knowledge
   instead (P9).
4. **Is the new interface simpler to describe than the code it hides?** Write the interface
   comment first. If it's awkward, the boundary is in the wrong place (P17).

If 1 and 4 both fail, leaving one longer unit is the correct answer, and it stays correct
even though it feels untidy.

## Deep or shallow?

| Signal | Reading |
|---|---|
| Interface fits in a sentence, implementation is substantial | Deep. Keep. |
| Method count grows with caller count | Shallow. Look for one more general operation (P10). |
| Callers must call in a fixed order | Leaked invariant. Fold into one operation. |
| Every caller passes the same arguments | Those arguments belong inside. |
| A class exists to hold one method used once | Probably not a module. Inline it. |
| Changing the implementation forces callers to change | Not hiding anything. |

## Where this pack disagrees with `solid` and `clean-architecture`

Real disagreement, stated rather than smoothed over. Both are Level 3, both are
architecture sources, so neither authority level nor proximity settles it
([conflict-resolution](../../../core/conflict-resolution.md) steps 4–5 both tie). It is
recorded as canonical ruling **R13** — cite that rather than re-deriving this section.

**The disagreement:** the common reading of single-responsibility and of "functions should
be small" pushes toward many small units. This pack holds that decomposition past the
point where a unit hides something produces *shallow* modules and raises total complexity —
more interfaces to learn, more call chains to trace, more places for the same knowledge to
leak. It disputes the granularity, not the direction.

**How to resolve it in practice:**

- **They agree far more than they disagree.** Both want a unit to have one reason to
  change and dependencies pointing inward. Start there; the conflict only arises at the
  margin.
- **When they genuinely conflict, ask what the split hides.** SOLID answers "does this
  have one responsibility"; this pack answers "does the boundary reduce what a caller must
  know". Where the second is no, the first was being applied mechanically.
- **State the tradeoff, per the resolution algorithm.** "Chose one 90-line function with a
  clear interface over four 20-line functions sharing three parameters, because the split
  exposed the intermediate representation to every caller. Cost: the function is longer
  than the house style prefers. Revisit if: a second caller needs one of the stages
  alone."
- **Personal Level 0 wins over both.** `packs/personal/<profile>/coding-preferences.md`
  sets file-size conventions, and Level 0 outranks any Level 3 pack (R4). Read this pack
  as being about *interface* depth, not about file length — that reading is both the
  accurate one and the one that removes the conflict.

## When NOT to use this pack

Required for Level 3 packs, and meant literally.

- **On a throwaway prototype.** Under the Prototype profile, tactical is correct: the code
  is a question, not an asset. Applying strategic design to something being deleted next
  week is the waste this pack exists to prevent.
- **As a blocker in review.** Every finding here is MEDIUM at most. "This module is
  shallow" is a design opinion, and a reviewer who cannot say *what the caller would stop
  needing to know* has an aesthetic preference, not a finding.
- **Against an established codebase convention.** R9 — consistency within a file or module
  beats this pack's ideal. Propose the migration separately.
- **On code that is genuinely simple.** A 30-line module with three callers does not need
  a depth analysis. The ideas earn their keep where change amplification is real.
- **As an argument against testing seams.** A boundary introduced so behavior can be tested
  hides something real: the dependency. Test seams are not shallow modules.
- **In a language or framework whose idiom disagrees.** Idiomatic React components,
  idiomatic Go packages, and idiomatic Rails models each carry granularity conventions
  that outrank a general-purpose book on their own turf.

## Which architecture pack for which question

| Question | Pack |
|---|---|
| Does this boundary reduce what callers must know? | this one |
| Which direction do dependencies point? | [clean-architecture](../clean-architecture/README.md) |
| Does this class have one reason to change? | [solid](../solid/README.md) |
| Is there a named solution to this recurring structure? | [design-patterns](../design-patterns/README.md) |
| How do I safely restructure what exists? | [martin-fowler-refactoring](../martin-fowler-refactoring/README.md) |
| Is the domain model and its language right? | [domain-driven-design](../domain-driven-design/README.md) |

## Profile modulation

- **Prototype** — skip. Tactical is the correct mode; note obvious leakage and move on.
- **Startup MVP** — apply to interfaces that already have two or more callers, and to
  anything that will be hard to change later (schemas, public APIs, module boundaries).
- **Production / Enterprise** — full review, with change amplification and obscurity
  reported as findings with named owners.
