# Prompt Fragments — WCAG Pack

## Fragment: build-mode constraint block

```text
Apply WCAG 2.2 AA constraints (AKOS L1 — non-negotiable floor):
- Native HTML first: button/a/input/select/dialog/details; never click-divs.
  Custom widgets = complete ARIA APG pattern (roles + states + keyboard map).
- Names: every interactive element has an accessible name matching its
  visible label; every input has a visible bound <label> (placeholder ≠ label).
- Keyboard: all functionality keyboard-operable; visible :focus-visible ring
  ≥3:1; modals trap + Escape + restore focus; no positive tabindex.
- Visual: text contrast ≥4.5:1 (3:1 large); UI boundaries ≥3:1; color never
  the sole signal; survives 200% zoom + 320px reflow; respect
  prefers-reduced-motion.
- Errors: identified in text at the field, aria-describedby association,
  focus to first error, suggestion where known; async status via aria-live.
- Semantics: one h1, sequential headings, landmarks, skip link, lang, unique
  titles (SPA route changes update title).
- Inputs: autocomplete attributes; ≥24px targets (design to 44px); gesture
  and drag alternatives; commit on up-event; no redundant re-entry.
```

## Fragment: accessibility audit lens

```text
Audit this UI against WCAG 2.2 AA using the three walks:
1. KEYBOARD WALK: complete the primary task mouse-free. Log unreachable
   controls, invisible focus, traps, illogical order, obscured focus.
2. TREE WALK: read the accessibility tree. Log nameless/roleless
   interactives, placeholder-only labels, stale ARIA states, missing
   landmarks/heading structure.
3. STRESS WALK: 200% zoom, 320px reflow, text-spacing overrides,
   grayscale (color-independence), reduced-motion.
Then verify: contrast pairs as rendered (incl. hover/dark variants), error
flow (submit invalid → identified/associated/focused/announced), modal
gauntlet, live regions.
Report per finding: SC number, severity (★floor violations = CRITICAL),
location, and concrete fix. Systemic component failures = one finding +
component fix. Automated-scanner cleanliness is the entry ticket, not the
conclusion.
```

## Fragment: contrast & palette check

```text
For every text/background and component/background pair in this palette
(including hover, focus, disabled, dark-mode variants): compute the
contrast ratio; flag text <4.5:1 (normal) / <3:1 (large), non-text <3:1.
For failures, propose the minimal token change (darken/lighten/invert
roles) that passes while staying nearest the brand hue. Output the
corrected token table.
```

## One-liner

```text
WCAG floor: native elements or full ARIA patterns; visible bound labels +
accessible names; full keyboard + visible focus + no traps; 4.5:1 text /
3:1 UI contrast; never color-only; errors located+associated+focused+
announced; 200%/320px survives; reduced-motion respected; 24px targets.
```
