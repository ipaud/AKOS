# Principles — Norman Pack

## P1 — Discoverability precedes usability

Users must be able to determine, by inspection, what actions are possible and where they stand. A feature that can't be discovered doesn't exist for the user who needs it.

## P2 — Signify every affordance that matters

For each action the user might need: is there a perceivable cue that it's possible, where, and how? Actions without signifiers are Easter eggs; primary actions without signifiers are defects. (Gestures and keyboard shortcuts are accelerators — they may hide, but a visible path to the same result must exist.)

## P3 — Map controls to effects naturally

Arrange controls to mirror their effects (spatially, directionally, or by strong analogy). Where natural mapping is impossible, group and label; never rely on memorized arbitrary associations for more than a couple of controls.

## P4 — Close the evaluation gulf: state must be visible

Every action gets acknowledgment; every ongoing process shows progress; every completed change shows its result; current system state is inspectable without acting. If a user has to *do something* to find out what state they're in, feedback failed.

## P5 — Project one coherent conceptual model

Choose the simplified story the UI tells (e.g. "documents live in folders and save themselves") and make every screen, label, and error message consistent with it. Features that leak implementation details break the model — hide them or change the model.

## P6 — Constrain before you validate

Prefer making wrong actions impossible (disable, omit, physically constrain, filter input) over detecting them afterwards. Order: constraint > default > validation > error message. Every error message is a constraint that wasn't designed.

## P7 — Design for error as a certainty

People will slip and people will misunderstand. Ship: undo everywhere feasible; confirmation proportional to irreversibility; dangerous actions visually and spatially distinct; sensible recovery from every error state. An interaction reviewed without asking "what happens when this goes wrong?" isn't reviewed.

## P8 — Treat slips and mistakes with different medicine

Diagnose observed errors: attention failure (slip) → spacing, undo, distinctiveness; model failure (mistake) → labels, system image, conceptual model. Never patch a mistake with a confirmation dialog.

## P9 — Put knowledge in the world

Show options rather than requiring recall; label rather than assume; keep context visible during multi-step tasks (what am I ordering? which account is active?). Memory demands are a tax the interface can almost always pay on the user's behalf.

## P10 — Standardize when you can't map

When natural mapping and constraints run out, standardize (conventions, platform patterns) so learning transfers. Deviating from a standard demands the same justification as breaking a Krug convention ([decision framework](../steve-krug/decision-framework.md)).

## P11 — Attractive things work better — behavioral level first

Invest in visceral appeal and reflective meaning (identity, personality) — they buy error tolerance and satisfaction. But behavioral quality (responsive, learnable, effective) is the load-bearing level; polish on top of confusion is lipstick on a gulf.

## P12 — Errors are data about the system image

Recurring user errors, support questions, and FAQs map exactly to where the projected model diverges from the user's model. Treat them as free usability research pointing at specific screens and words.
