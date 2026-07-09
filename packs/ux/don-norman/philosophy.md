# Philosophy — Norman Pack

## Human error is design error

When a person pushes a door that should be pulled, the door failed, not the person. This inversion is the pack's foundation: designers control discoverability, understanding, and feedback; users control only their goals. Blaming users ("read the manual", "be careful") is the designer resigning from the job. In review terms: every user error observed in testing is assigned to a design cause until proven otherwise.

## Design is communication through objects

An interface is a one-way conversation held in advance. The designer can't be present, so the artifact itself must communicate what's possible (affordances made visible by signifiers), how controls relate to effects (mapping), what state things are in (feedback), and how the whole thing works (a projected conceptual model). Every usability failure is a failed utterance in this conversation.

## Two gulfs separate intent from success

Users stand before a **gulf of execution** ("what do I do to achieve my goal?") and, after acting, a **gulf of evaluation** ("did it work? what state is it in now?"). All interaction design is bridge-building over these two gulfs. The seven-stage action cycle (goal → plan → specify → perform → perceive → interpret → compare) names exactly where a bridge is out.

## The system image is all the user gets

Designers hold a rich mental model of the product. Users never see it — they see only the **system image**: the UI, the labels, the docs, the error messages. Users construct their own model from that image alone. If the system image is incoherent, users build a wrong model and the design fails in ways that look like "user error" (see above).

## Human-centered design is iterative by necessity

Since designers can't reason their way into users' heads, HCD works by cycle: observe → ideate → prototype → test → repeat. Requirements discovered by watching real behavior outrank requirements stated in meetings. This aligns with Krug's testing habit and product discovery packs ([continuous-discovery-habits](../../product/continuous-discovery-habits/README.md)).

## Emotion is part of function

Attractive things work better — not as decoration, but because positive affect broadens thinking and increases error tolerance, while anxiety narrows it. Visceral, behavioral, and reflective levels of processing all matter. This is the principled hook for AKOS's Level-0 "personality with obviousness" rule: identity is a functional investment, provided the behavioral level (usability) stays sound.

## Where this philosophy stops

Norman explains interaction mechanics and psychology; he is thinner on visual craft (see [refactoring-ui](../refactoring-ui/README.md)) and on business/product strategy (see product packs). Applying gulf analysis to every trivial button is over-tooling — reach for this pack when the *why* of a failure isn't obvious.
