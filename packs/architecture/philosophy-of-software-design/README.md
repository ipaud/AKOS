# Pack: Philosophy of Software Design — Complexity as the Thing Being Managed

**Domain:** Architecture · **Authority:** Level 3 (book) · **Version:** 1.0.0

Treats complexity — how hard a system is to understand and change — as the quantity being
managed, and gives it a vocabulary precise enough to review against: module depth,
information leakage, change amplification, and the cost of an interface.

Independent distillation for personal engineering use. Not affiliated with or endorsed by
the author. See [references.md](references.md) for the original — buy and read it; this
pack is a lossy operational index, not a substitute.

## When to load this pack

- A module boundary, schema, or public interface is being designed — decisions expensive
  to reverse.
- A change touched many files for one conceptual reason and you want to know why.
- Code works but resists change, and "it's messy" needs to become something actionable.
- Reviewing a design where the question is what it costs the next reader.

**When not to load it:** Prototype profile (tactical is correct there), or when the
question is dependency direction, class responsibility, a named structure, or a domain
model — see the routing table in [decision-framework.md](decision-framework.md).

## What's inside

| File | Highlights |
|------|-----------|
| [principles.md](principles.md) | P1–P19. What complexity is, modules, errors, working method. |
| [engineering-rules.md](engineering-rules.md) | PSD1–PSD36. Deliberately unstarred — nothing here is a safety floor. |
| [mental-models.md](mental-models.md) | Module depth, the three symptoms, the two causes, pulling complexity down, design it twice. |
| [philosophy.md](philosophy.md) | Why this source disagrees with consensus, and why the corpus is better for holding the disagreement. |
| [decision-framework.md](decision-framework.md) | Should this be split, deep-or-shallow signals, the `solid` conflict, **when NOT to use this pack**. |
| [review-checklist.md](review-checklist.md) | MEDIUM and LOW only, plus the reviewer discipline rule. |
| [anti-patterns.md](anti-patterns.md) | Shallow module, temporal decomposition, pass-through layer, tactical tornado, classitis — and two failure modes of *applying* this pack. |
| [scoring-rubric.md](scoring-rubric.md) | Shallow deductions, no CRITICAL band, `n/a` under Prototype. |
| [prompt-fragments.md](prompt-fragments.md) | Build-mode block, review lens, the split test. |
| [glossary.md](glossary.md) | Terms used precisely, including where they collide with other packs. |
| [heuristics.md](heuristics.md) | Defaults while the design is still open. |

## Core claim, one line

Splitting something in two always adds an interface, and an interface is a cost — so
decomposition pays only when the new boundary lets the caller stop knowing something.

## The one question

**What does the caller stop needing to know?** It works on a function, a class, a service,
an API, a config file. It turns an aesthetic argument into an answerable one, and it is the
test behind almost every rule here.

## It disagrees with the neighbours, on purpose

This pack disputes the common reading of `solid` and `clean-architecture` on how small
units should be — Level 3 against Level 3, both architecture sources, so neither authority
nor proximity settles it. The disagreement is stated and resolved in
[decision-framework.md](decision-framework.md) rather than smoothed over, and a Level 0
personal file-size convention outranks both.

Read it as being about **interface** depth, not file length. That reading is both the
accurate one and the one that dissolves most of the conflict.

## Related packs

[solid](../solid/README.md) · [clean-architecture](../clean-architecture/README.md) ·
[design-patterns](../design-patterns/README.md) ·
[martin-fowler-refactoring](../martin-fowler-refactoring/README.md) ·
[domain-driven-design](../domain-driven-design/README.md)
