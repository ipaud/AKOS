# Philosophy — Refactoring UI Pack

## Design is decisions, and constraints make decisions cheap

The reason developer-built UIs look amateur isn't missing talent — it's unlimited choice. Any pixel value, any gray, any font size, chosen independently per element, guarantees inconsistency. The fix is systems: a spacing scale, a type scale, a fixed set of grays and accents, a shadow ladder. With a 10-value palette and an 8-step spacing scale, most decisions become "pick the nearest step" — fast, consistent, and composable. Constraint is not a limitation on design; it *is* design.

## Hierarchy is the whole game

A screen where everything speaks at equal volume communicates nothing. Almost every "this looks off" complaint is a hierarchy failure: labels shouting over data, borders louder than content, five competing font sizes. The craft is deliberately de-emphasizing the secondary — softer color, lighter weight, smaller-but-not-tiny — so the primary reads without effort. De-emphasis is more powerful and more forgotten than emphasis. (Quantified cousin: [Von Restorff budget](../laws-of-ux/principles.md).)

## Start from features, not layouts

Design the piece of UI the feature needs (a search field, a result card), not "the app shell". Work in low fidelity, decide details later, and don't build what you can't ship — every polished mockup detail is a promise. Iterate: design a little, build a little.

## Remove before you add

The amateur instinct for "make it pop" is addition: more borders, more colors, more boxes. The professional move is usually subtraction: separate with spacing instead of borders, use background shifts instead of boxes, let whitespace group things ([proximity](../universal-principles-of-design/principles.md)). A design's polish level correlates inversely with its visual noise.

## Personality is a system property too

Fonts, color, border radius, illustration style, and copy tone set personality (playful ↔ serious, warm ↔ technical). Choose the personality deliberately, encode it in the system tokens, and it applies itself consistently — which is exactly the AKOS Level-0 rule: strong identity, systematically applied, never at the cost of obviousness or floors.
