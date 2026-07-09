# Mental Models — Apple HIG Pack

## Navigation as a physical grammar

iOS navigation is spatial: hierarchical push/pop (drill in, edge-swipe back), modal sheets (temporary contexts that slide up and must resolve), tab bars (parallel top-level worlds that preserve their own stacks). Users hold this physics innately; violating it (a push that behaves like a modal, tabs that reset stacks) breaks their spatial model. Choose the *grammar element* that matches the content relationship, and the rest of the behavior is prescribed.

## Size classes, not screens

Layouts respond to compact/regular width-height combinations, not device names. iPhone landscape, iPad split view, Stage Manager windows — all are size-class puzzles. Designing per-device is designing for a hardware catalog that will change.

## Dynamic Type as the real type system

Text styles (Large Title, Title 1–3, Headline, Body, Callout, Subhead, Footnote, Caption) are semantic slots that scale with user preference. Adopting them = typography + accessibility + future-proofing in one move. Fixed pixel fonts opt out of all three.

## The 44pt world

Touch targets ≥44×44pt is the ergonomic constant everything else arranges around ([Fitts](../laws-of-ux/principles.md), [Krug ER8](../steve-krug/engineering-rules.md)). Thumb zones: bottom of iPhone screens is prime; top corners are reach-cost. Hence tab bars, bottom sheets, and large-title-collapsing patterns.

## Feedback trio: visual, haptic, audio

The platform offers three coordinated channels; native-feeling apps use system haptics semantically (success, warning, selection ticks) alongside visual state — sparingly enough that each still means something ([Norman feedback calibration](../don-norman/heuristics.md)).

## SF Symbols as vocabulary

The system icon family with weights/scales aligned to text styles. Using it (or matching its optical rules) buys consistency with the OS-wide iconographic language users already read.
