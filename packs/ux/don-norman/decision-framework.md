# Decision Framework — Norman Pack

## Which lever fixes this failure?

Given an observed interaction failure, choose the lever in this order:

1. **Constraint** — can the wrong action become impossible? (Cheapest to use, hardest to misdesign.)
2. **Mapping** — can position/direction make the right action self-predicting?
3. **Signifier** — can a visible cue communicate the affordance?
4. **Feedback** — can better state visibility close the evaluation gulf?
5. **Model** — must the projected conceptual model itself change (labels, structure, docs)?

Reaching for 5 first is a smell; reaching only for 3 forever (adding hints to a bad model) is another.

## Confirmation vs. undo vs. forcing function

| Situation | Choose |
|-----------|--------|
| Reversible, frequent | Undo (toast), no confirmation |
| Reversible, rare | Undo; confirmation optional |
| Irreversible, rare, low value | Confirmation dialog restating consequence |
| Irreversible, any frequency, high value | Forcing function (typed name, two-step) |
| Irreversible + bulk | Forcing function + delay/trash-can grace period |

Never: confirmation for frequent actions (trains blind confirming), undo-only for truly irreversible ops.

## Novel interaction vs. borrowed model

Building something with no convention? Decide:

1. Is there an adjacent model users hold (physical or digital)? → Bend it; accept its constraints.
2. No model fits? → Design the simplest projected model that predicts behavior; write it as one sentence ("X is a pile of cards; newest on top"); test whether 3 users can state it back after use.
3. The model users form ≠ the one you projected? → Change the design toward *their* model unless theirs is dangerous.

## Mode decisions

Modes multiply mistakes. Before adding one (edit/view, per-tool cursors, admin views):

- Can the modes merge (direct manipulation instead of an edit mode)?
- If not: is the mode globally visible while active (NR25)? Is exit obvious?
- Spring-loaded modes (held key, press-and-drag) beat locked modes — they can't be forgotten.

## Feedback channel choice

Decide prominence by *cost of missing it*: 
missable-and-fine → inline/subtle; missable-and-costly → toast with persistence or badge; must-act-now → modal. Sound and haptics augment, never replace, visible feedback.

## When users keep erring anyway

1. Reclassify (slip vs mistake) — the first diagnosis is often wrong.
2. If slip persists: increase distance/distinctiveness; add undo rather than more warnings.
3. If mistake persists: the conceptual model is wrong — rename, restructure, or retire the feature. A feature needing perpetual education has failed structurally.
