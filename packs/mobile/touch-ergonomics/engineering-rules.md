# Engineering Rules — Touch Ergonomics Pack

Checkable in the artifact. A reviewer verifies each against the code and the rendered UI on a real device; violations are findings. `F` denotes the applicable target floor — 44px (Apple-leaning), 48px (Material-leaning), or 24px only where a documented WCAG 2.2 SC 2.5.8 exception genuinely applies.

## Target size

- TEE1. Every interactive element is at least 24×24 CSS px, or satisfies a named SC 2.5.8 exception (spacing, inline, equivalent, user-agent, essential). The exception is named in the review, not assumed.
- TEE2. Primary actions, destructive actions, and any control tapped more than once per task are at least 44×44 CSS px (48 on Material surfaces). The 24px floor is never used to justify these.
- TEE3. The measured size is the *hit* area, not the visual box: verified with the element's actual client rect (including padding and any hit-expanding pseudo-element), not from the design file.
- TEE4. Icon-only controls carry the floor through padding or an explicit expanded hit area; icon glyph size is decoupled from target size.
- TEE5. Row-level actions in tables, lists, and grids meet the same floor as standalone buttons. Density is not an exemption.
- TEE6. Checkbox and radio hit areas include their label; the label is a `<label>` with a `for`/wrapping association so the whole text is tappable.
- TEE7. Close, back, dismiss, and cancel controls meet the floor. A dismiss the user cannot hit is a trap.
- TEE8. Inline links inside body text are exempt from the size floor (SC 2.5.8 inline exception) but standalone links styled as actions are not.

## Spacing and non-overlap

- TEE9. No two hit areas overlap. Overlap resolved by paint order or `z-index` is a defect regardless of which element currently wins.
- TEE10. For adjacent controls with visual widths `wA` and `wB`, the visual gap satisfies `gap ≥ F − (wA + wB)/2`. Computed, not eyeballed; recorded in the review for every icon-button cluster.
- TEE11. Where either adjacent control is destructive, the required gap is doubled or the destructive control is moved out of the cluster.
- TEE12. Adjacent targets have at least 8px of visual separation even when both already meet the floor (Material's separation guidance; keeps the contact ellipse from straddling).
- TEE13. Hit-expanding pseudo-elements (`::after { position:absolute; inset:-Npx }`) are audited for intersection with siblings after every layout change; the bleed value is derived from the floor, not hardcoded independently.
- TEE14. Prefer real padding on the element over an expanding overlay. Overlays are used only where layout constraints forbid growing the box, and each use carries a comment stating the computed bleed and the checked neighbours.

## Hover, focus, and pointer capability

- TEE15. No `title` attribute carries meaning required to operate or understand a control. `title` is permitted only as redundant detail. (Safety floor; see [ux-writing UWE38](../../content/ux-writing/engineering-rules.md) and [wcag](../../ux/wcag/engineering-rules.md).)
- TEE16. No control appears only on hover. Row actions, edit affordances, delete buttons, and drag handles are persistently visible on coarse-pointer devices.
- TEE17. Tooltips are replaced by, or paired with, one of: persistent visible text, an accessible name, or a tap-activated disclosure (popover/details) that is dismissible and keyboard-reachable.
- TEE18. Hover-only enhancements are wrapped in `@media (hover: hover) and (pointer: fine)`; nothing inside that block is required to complete a task.
- TEE19. Sizing and spacing rules branch on `@media (any-pointer: coarse)`, never on `max-width`. No width breakpoint gates touch behaviour.
- TEE20. No code uses user-agent sniffing or `'ontouchstart' in window` to decide layout or affordances; capability is queried via media queries or `matchMedia`.
- TEE21. `:hover` styles do not persist after a tap on touch devices — verified, since sticky hover state on a tapped element is a common artefact.

## Placement and reach

- TEE22. On phone viewports, the primary action of a task screen is reachable in the bottom third of the viewport — as a sticky action bar, a bottom-anchored button, or a duplicated control.
- TEE23. No state-advancing action (save, submit, confirm, next) exists *only* above a scroll region longer than one viewport.
- TEE24. Destructive controls are not immediate neighbours of the primary action and are not placed in the bottom-third thumb zone of a repeated-use screen.
- TEE25. Bottom-anchored bars respect `env(safe-area-inset-bottom)` and do not overlap the home indicator area.
- TEE26. Fixed and sticky elements are verified with the virtual keyboard open; the primary action is not covered by it.
- TEE27. Viewport-height layouts use `dvh`/`svh` rather than `vh`, and any layout that must track the keyboard uses `window.visualViewport` rather than assuming a resize event.

## The virtual keyboard and input attributes

- TEE28. Every text input declares `type`, and declares `inputmode` wherever the desired keypad differs from the type's default.
- TEE29. Every input that maps to a known autofill category declares `autocomplete` with a valid token (`email`, `tel`, `name`, `street-address`, `postal-code`, `cc-number`, `one-time-code`, `current-password`, …). `autocomplete="off"` requires a stated reason.
- TEE30. Multi-field forms set `enterkeyhint` — `next` on intermediate fields, `done` or `send` on the last.
- TEE31. `type="number"` is used only for true quantities that tolerate spinner semantics. Phone numbers, card numbers, postal codes, PINs, and locale-formatted amounts use `type="text"` with `inputmode` set.
- TEE32. `inputmode` is never treated as validation. Every field validates and parses its value in code irrespective of the keyboard requested.
- TEE33. Codes and identifiers set `autocapitalize="off"`, `autocorrect="off"`, and `spellcheck="false"`; free text does not.
- TEE34. Text inputs, selects, and textareas render at a computed font size of at least 16px on coarse-pointer devices. Below 16px, iOS Safari zooms the page on focus, which strands the user at a zoom level the layout was not designed for.
- TEE35. The 16px floor is never bought with `user-scalable=no` or `maximum-scale=1` in the viewport meta. Suppressing zoom is an accessibility regression, not a fix.
- TEE36. The 16px floor is enforced at a single site — the shared field primitive plus a backstop rule — not documented and left to each component.
- TEE37. A lint or CI check fails on raw `<input>`, `<select>`, and `<textarea>` elements outside the field primitive, and on any `font-size` below 16px targeting a form control.
- TEE38. Native pickers (`date`, `time`, `datetime-local`, `select`) are preferred over custom dropdowns on touch unless the custom control demonstrably beats them; custom replacements meet every rule in this file on their own.

## Locale-safe input parsing

- TEE39. No user-entered numeric string reaches `Number()`, `parseFloat()`, or `parseInt()` without passing through an explicit locale-aware parser.
- TEE40. The parser returns a number or an explicit failure sentinel (`null`, a result type). `Number(x) || 0`, `?? 0`, and `isNaN(x) ? 0 : x` are banned in any path that writes a persisted value.
- TEE41. The parser handles: the locale decimal separator, the locale grouping separator, non-breaking and narrow no-break spaces used as grouping, leading and trailing whitespace, currency symbols, and an empty string. Separators are derived from `Intl.NumberFormat.formatToParts`, not from a hardcoded locale map.
- TEE42. On parse failure the field shows an error and the value is not committed. Silent substitution of `0` for unparseable input is treated as data loss, not as a default.
- TEE43. Money and quantity fields echo the parsed interpretation back to the user (formatted with `Intl.NumberFormat`) before or at the moment of commit, so a misread comma is visible rather than inferred later.
- TEE44. Values are stored in a canonical machine form (minor units or a decimal type) and formatted for display through locale APIs; the display string is never the stored value.
- TEE45. Automated tests cover the locale matrix for every numeric input: at minimum a dot-locale and a comma-locale, with the separator the on-screen keypad actually offers.

## Gestures, scrolling, and tap behaviour

- TEE46. Every gesture-triggered action has a visible single-tap equivalent reachable without the gesture (SC 2.5.1). Swipe-to-delete always ships with a visible delete control.
- TEE47. No action requires a path-based or multi-point gesture unless the gesture is essential to the function (drawing, map pinch).
- TEE48. Custom horizontal-drag and edge-drag interactions are kept clear of the screen edges reserved by system back/home gestures; content in those strips is non-interactive or duplicated elsewhere.
- TEE49. `touch-action: manipulation` is applied to tappable controls to remove double-tap-zoom delay. `touch-action: none` is used only on elements implementing custom pointer gestures, never as a scrolling workaround, and never on a container that would otherwise permit pinch-zoom.
- TEE50. Scrollable overlays (sheets, modals, drawers) set `overscroll-behavior: contain` so scrolling does not chain to the page or trigger pull-to-refresh.
- TEE51. Horizontal scrollers (carousels, scrollable tables) set `overscroll-behavior-x: contain` to avoid triggering browser back-navigation on overscroll.
- TEE52. Body scroll is locked while a modal sheet is open, and the scroll position is restored on close.

## Accidental activation and recovery

- TEE53. Actions fire on the up-event (`click` / `pointerup`), never on `pointerdown` or `touchstart`, and remain cancellable by moving off the target before release (SC 2.5.2).
- TEE54. Consequential actions provide undo with a stated window, rendered in the bottom third within thumb reach, persisting long enough to be noticed and acted on; confirmation dialogs are reserved for the genuinely irreversible, and their confirming button is not placed where the user's finger already is.
