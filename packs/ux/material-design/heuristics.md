# Heuristics — Material Design Pack

## Component selection

- One filled button per surface; everything else steps down the emphasis ladder (tonal/outlined/text).
- FAB only for *the* signature action of a screen (compose, add) — one, bottom-right (LTR), never a menu-opener; no FAB on screens without a dominant action.
- Snackbar for transient feedback (with optional single action like Undo); dialog for decisions; banner for persistent conditions. Never stack snackbars into a notification system ([feedback calibration](../don-norman/heuristics.md)).
- Chips for compact choices/filters/inputs; don't rebuild them as tiny buttons.
- Bottom sheet (modal) for mobile contextual actions; side sheet for supplementary content on large canvases.

## Fast checks

- Grep for raw hex/dp values in components → pyramid holes (MD5).
- Toggle dark theme: tonal surfaces shifting correctly? Hardcoded whites glaring?
- Enable dynamic color (or simulate a hue swap): brand survive? contrast pairs hold?
- Keyboard/TalkBack pass: focus indicators from state layers visible? semantics intact after theming?
- Resize to tablet width: does navigation morph (bar→rail) and does the layout adopt a canonical pattern, or is it a stretched phone?

## Theming judgment

- Start theming from color scheme (seed color → tonal palettes), then type ramp, then shape scale — that order covers most brand distance cheaply.
- Shape: pick a family (M3 has small/medium/large component radii) and adjust the family, not individual components ([radius roulette](../refactoring-ui/anti-patterns.md)).
- If the design goal fights a component's anatomy (e.g. "buttons with no state feedback"), the goal loses — states are load-bearing (MD4).

## Cross-platform

- Material on Android + web is coherent; Material on iOS is foreign grammar — swap the navigation/control layer per platform, keep tokens/brand shared ([HIG cross-platform](../apple-hig/heuristics.md)).
- Component libraries (MUI, Flutter Material): pin versions to a Material version; mixing M2 and M3 idioms in one app reads as two apps.
