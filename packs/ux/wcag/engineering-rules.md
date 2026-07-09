# Engineering Rules — WCAG Pack

Checkable rules with SC citations. Floor rules (marked ★) bind every profile including Prototype.

## Semantics & names

- WC1 ★ Interactive elements are native (`button`, `a[href]`, `input`, `select`, `textarea`, `details`, `dialog`) or complete APG-pattern ARIA widgets — never bare `div/span` with click handlers. (4.1.2)
- WC2 ★ Every interactive element has an accessible name matching or containing its visible label. Icon-only controls: `aria-label`. (4.1.2, 2.5.3)
- WC3 ★ Every form input has a programmatically bound, visible, persistent label (`<label for>` or wrapping); placeholders are not labels. (1.3.1, 3.3.2)
- WC4. Images: informative → descriptive `alt`; decorative → `alt=""`; complex (charts) → short alt + adjacent long description or data table. (1.1.1)
- WC5. Headings are real (`h1–h6`), sequential, and describe their sections; exactly one `h1` per page. (1.3.1, 2.4.6)
- WC6. Landmarks present: `main`, `nav`, `header`, `footer`; repeated blocks skippable via skip link as first focusable. (1.3.1, 2.4.1)
- WC7. Tables use `th` + `scope` (or headers/id for complex); layout tables don't exist. (1.3.1)
- WC8. `html` has `lang`; inline foreign phrases get `lang`. (3.1.1, 3.1.2)
- WC9. Page `<title>` describes page + product, unique per view (SPAs update it on route change). (2.4.2)

## Keyboard & focus

- WC10 ★ Every action completable by keyboard alone; custom widgets implement APG keyboard patterns (arrows in menus/tabs/radios, Escape closes, Enter/Space activate). (2.1.1)
- WC11 ★ No keyboard traps; modals trap focus *intentionally* while open, restore it on close to the trigger. (2.1.2)
- WC12 ★ Focus indicator visible on every focusable element (≥3:1 against adjacent colors); `outline: none` only with an equal-or-better replacement. (2.4.7, 1.4.11)
- WC13. DOM order = focus order = visual reading order; no positive `tabindex`. (2.4.3, 1.3.2)
- WC14. Focused elements never fully obscured by sticky headers/footers/cookie banners. (2.4.11)
- WC15. Focus moves purposefully: into opened dialogs, to first error on failed submit, to result announcements — never randomly resets to body. (2.4.3, 3.3.1)

## Visual

- WC16 ★ Text contrast ≥ 4.5:1 (normal) / 3:1 (large: ≥24px or ≥19px bold). (1.4.3)
- WC17. UI component boundaries, focus indicators, and meaningful graphics ≥ 3:1 against adjacent colors. (1.4.11)
- WC18 ★ Color never sole carrier of meaning: errors get text+icon; prose links get non-color distinction; chart series get labels/patterns. (1.4.1)
- WC19. Page functional at 200% zoom and 320px reflow: no 2D scrolling, no clipped content, no desktop-only escape hatch. (1.4.4, 1.4.10)
- WC20. Layout survives user text-spacing overrides (line-height 1.5×, paragraph 2×, letter 0.12×, word 0.16×) — no clipping/overlap. (1.4.12)
- WC21. Tooltips/hover cards: dismissible (Escape), hoverable (pointer can enter), persistent (until dismissed). (1.4.13)
- WC22. `prefers-reduced-motion` respected: decorative animation drops out; essential motion gets alternatives. (2.3.3 AAA-adjacent, 2.2.2)

## Input & interaction

- WC23. Touch targets ≥ 24×24 CSS px hard floor; 44×44 as the design bar (Krug ER8). (2.5.8)
- WC24. Complex gestures (pinch, multi-finger, path-drag) have single-pointer alternatives; drag-drop has click/keyboard alternative. (2.5.1, 2.5.7)
- WC25. Actions commit on up-event, not down (permits slide-away abort). (2.5.2)
- WC26. Autocomplete attributes on personal-data fields (`autocomplete="email"` etc.). (1.3.5)
- WC27. Authentication permits paste, password managers, passkeys; no transcription/memory puzzles without alternative. (3.3.8)
- WC28. Data already provided in a flow is auto-populated or selectable, never re-typed. (3.3.7)

## Errors & status

- WC29 ★ Errors identified in text at the field, associated programmatically (`aria-describedby`), with suggestion where known; focus moves to first error. (3.3.1, 3.3.3)
- WC30. Legal/financial/data-destroying submissions: reversible, or reviewed, or explicitly confirmed. (3.3.4)
- WC31. Async status (saved, loaded, failed, N results) announced via `aria-live` (polite for info, assertive for errors) without focus theft. (4.1.3)
- WC32. Session time limits warn and allow extension; auto-updating content pausable. (2.2.1, 2.2.2)

## Behavior

- WC33. Focus/input never auto-triggers context change (no navigate-on-select, no submit-on-last-digit) without prior notice. (3.2.1, 3.2.2)
- WC34. Navigation and component behavior consistent across the product; help in a consistent location. (3.2.3, 3.2.4, 3.2.6)
- WC35. Nothing flashes >3×/second. (2.3.1)

## Tooling gate

- WC36. Automated scan (axe/Lighthouse-a11y) integrated into CI or review; zero violations at the scanner level is the *entry ticket* to manual review, not the audit itself.
