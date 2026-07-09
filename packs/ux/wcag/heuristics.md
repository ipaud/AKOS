# Heuristics — WCAG Pack

Fast judgment rules for building and reviewing.

## Building

- **Reach for the native element first.** Ask "does HTML have this?" before writing a component. `dialog`, `details`, `datalist`, `progress`, `meter` cover more than teams remember.
- **If you wrote `onClick` on a div, stop.** Make it a `button` — you get keyboard, focus, role, and name mechanics free.
- **Name everything at birth.** Adding accessible names in a later "a11y pass" costs 5× writing them inline now.
- **Style states, don't erase them.** Focus rings, checked states, disabled looks: restyle to match the brand, never remove.
- **Design tokens carry the floor.** Bake 4.5:1 pairs into the palette tokens so no one picks failing combinations ad hoc.
- **Live regions are plumbing — install early.** One polite + one assertive region wired to the toast/status system covers most of SC 4.1.3 forever.

## Reviewing (the three walks)

- **Keyboard walk:** unplug the mouse; complete the screen's primary task. Log every stall: unreachable control, invisible focus, trap, weird order. This one walk finds the majority of Operable failures.
- **Tree walk:** open the accessibility tree; read the screen as AT sees it. Nameless buttons, div-soup, missing roles, stale states jump out.
- **Stress walk:** 200% zoom, 320px width, forced text spacing, reduced motion, grayscale filter (color-independence check). Layout survivors pass Perceivable's hard parts.

## Judgment shortcuts

- **Alt text:** describe the *purpose in context*, not the pixels ("Company logo — home" not "blue swirl graphic"). If removing the image loses nothing, `alt=""`.
- **aria-label sniff test:** if the visible text and the aria-label differ, voice-control users can't click it by saying what they see (SC 2.5.3). Name = visible label + optional suffix.
- **Contrast triage:** body text and primary actions first; check the *real* rendered pairs (text over images, gradients, hover states), not just the palette table.
- **Heading skeleton read:** extract only the headings; do they outline the page honestly? (Same artifact scanning uses — [Krug P3](../steve-krug/principles.md).)
- **The modal gauntlet:** open → focus inside? Escape → closes? Tab cycle → contained? Close → focus back on trigger? Four checks, most modals fail one.
- **Forms in one question:** "could a screen-reader user fix a submission error without sighted help?" — walks labels, error association, focus management at once.

## Prioritization

- Failures on the primary task path outrank failures on secondary surfaces at the same SC.
- Systemic component failures (every button in the app) are one finding at CRITICAL with a component fix, not N findings.
- When effort-constrained: keyboard completeness → names/labels → contrast → error handling → structure → polish. That order maximizes users-unblocked per hour.
