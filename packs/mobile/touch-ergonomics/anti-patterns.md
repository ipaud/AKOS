# Anti-Patterns — Touch Ergonomics Pack

Named failure modes. Detection cue → why it fails → fix. The first block covers defects that cause a *wrong action or a wrong value* rather than mere inconvenience; those are correctness bugs and are scored as such.

## The contested strip

**Detect:** two adjacent controls where at least one has a hit area larger than its visual box, and the visual gap is smaller than `F − (wA + wB)/2`. Invisible in screenshots and design files; found by arithmetic or by inspecting client rects in devtools.
**Why it fails:** the overlapping band belongs to whichever element wins hit-testing, normally the one painted later or stacked higher. That resolution is an accident of DOM order, so the user's taps near the boundary activate a control chosen by an implementation detail. When one of the two is destructive, an intended edit deletes a record.
**Fix:** compute the required gap and open it, or grow both boxes with real padding so no overlay is needed. If the layout cannot carry it, move the destructive control out of the cluster entirely. Never resolve it with `z-index` — that hides the defect by choosing a winner rather than removing the contest.

## The comma that ate the number

**Detect:** a numeric or money field in a product with non-English locales, whose handler calls `Number(value)`, `parseFloat(value)`, or `value || 0`. Reproduce by switching the device language to a comma-locale and typing the separator the keypad offers.
**Why it fails:** the on-screen keypad is localized, so users type `12,50`. `Number("12,50")` is `NaN`; `parseFloat("12,50")` is `12`; on `type="number"` the element's own sanitization can make `value` an empty string while the characters remain visible on screen. Any `|| 0` downstream then commits a confident zero. Nothing errors, nothing logs, and the wrong number reaches storage and every total computed from it.
**Fix:** one locale-aware parser that returns a number or `null`; `null` blocks the commit and renders an error. Derive separators from `Intl.NumberFormat.formatToParts`. Echo the parsed value back, formatted, near the field. Add a comma-locale case to the test matrix for every numeric input.

## The rule that lives in a doc

**Detect:** a codebase whose design-system documentation states a touch rule — most often the 16px input floor and its iOS auto-zoom consequence — while components in the product violate it. Confirmed by grepping for raw `<input>` / `<select>` / `<textarea>` outside the shared field primitive.
**Why it fails:** documentation records intent and constrains nothing. Any component built without going through the primitive reintroduces the defect, and the developer who does it has usually never read the doc — which is the normal case, not the negligent one. The team's knowledge was never the binding constraint.
**Fix:** move the rule into the primitive, plus a backstop rule so bypasses still render correctly, plus a lint or CI check that fails on the bypass. Grade the fix by which of those three landed; patching the two offending components alone is not a fix.

## Hover-only meaning

**Detect:** `title` attributes on interactive elements, tooltip-only explanations, controls that appear on `:hover`, status indicators whose meaning is a hover card. Grep: `title=` on anything focusable, `:hover` rules that change `display`, `visibility`, or `opacity` on a control.
**Why it fails:** touch has no hover, so the content does not exist for those users. When the hidden content is a *warning the user needs to act on*, the touch user is not inconvenienced — they are uninformed at the moment of a decision. Keyboard and screen-reader treatment is inconsistent on top of that, so this also breaches the accessibility floor.
**Fix:** identity → visible text or an accessible name; detail → a tap-activated, dismissible disclosure; warning → persistent visible text next to what it warns about; decoration → delete. `title` may remain only as redundant extra. (See [ux-writing UWE38](../../content/ux-writing/engineering-rules.md).)

## The action at the top of the scroll

**Detect:** a state-advancing control (save, submit, confirm, next) placed above a scroll region longer than one viewport, or in the top corner of a screen used repeatedly. Found by loading the flow on a phone and asking where the user's thumb rests versus where the action is.
**Why it fails:** it puts the most frequent interaction in the most expensive position on the device. On a screen designed for on-site use — one hand on the phone, the other holding something — reaching it requires a regrip that users avoid by not completing the task. The pattern usually enters because the desktop layout put the action bar at the top and nobody re-asked the question for touch.
**Fix:** duplicate or move the primary action into a bottom-anchored bar within thumb reach, respecting `env(safe-area-inset-bottom)` and verified with the keyboard open.

## Desktop density on a touch device

**Detect:** icon-button rows, table row actions, or toolbar clusters at 24–32px with 2–6px gaps, ported unchanged from a desktop layout.
**Why it fails:** each control is at or under the conformance floor without satisfying the spacing exception, and the cluster multiplies the error rate by putting several of them within one contact patch.
**Fix:** grow the buttons to the ergonomic target on coarse pointers, reduce how many actions are exposed inline (overflow the rest), or switch the row to a tap-to-open detail with full-size actions.

## The unreachable close button

**Detect:** a dismiss `×` under 44px, in the far top corner, sometimes over a busy background.
**Why it fails:** it is the only escape from the surface, placed at the single worst point on a one-handed phone, at a size that guarantees misses. Users who cannot close a sheet reload the page and lose their state.
**Fix:** floor-sized dismiss, plus a second escape route — tap-outside, swipe-down on a sheet, or a bottom-anchored "Close". Backdrop dismissal alone is not enough on a full-screen sheet.

## Swipe-only actions

**Detect:** delete, archive, or reply available only by swiping a row; long-press-only context menus; pinch or two-finger gestures as the sole path.
**Why it fails:** invisible to anyone who has not been told, impossible for users who cannot perform a path gesture or hold multiple contacts, and normatively insufficient under SC 2.5.1.
**Fix:** every gesture ships alongside a visible single-tap control. Keep the gesture — it is genuinely good for experts — but never as the route.

## Edge-anchored custom gestures

**Detect:** custom horizontal drags, sliders, or drawer handles starting within the screen's edge strips, or interactive content pushed into the bottom home-indicator area.
**Why it fails:** those strips belong to the operating system's back and home gestures. The OS wins, so the interaction fires intermittently — which reads to users as a broken app rather than a conflict.
**Fix:** inset custom drag origins away from the edges, honour `env(safe-area-inset-*)`, and provide a non-gesture route for anything the conflict can swallow.

## `touch-action: none` as a scroll fix

**Detect:** `touch-action: none` on a container that is not implementing a custom pointer gesture; often added to stop an unwanted scroll or a stray zoom.
**Why it fails:** it disables the browser's default touch behaviours wholesale, including pinch-zoom, which is an accessibility regression for low-vision users. The scrolling problem it was meant to fix usually had a targeted solution.
**Fix:** `touch-action: manipulation` on tappable controls (removes double-tap-zoom delay only); `overscroll-behavior: contain` for chaining and pull-to-refresh; `pan-x` / `pan-y` where an axis genuinely must be reserved. Reserve `none` for real custom-gesture surfaces.

## Scroll chaining and the accidental refresh

**Detect:** a bottom sheet, drawer, or modal with an internal scroll area and no `overscroll-behavior`; a horizontal carousel with no `overscroll-behavior-x`.
**Why it fails:** scrolling past the end of the inner area moves the page behind it, or triggers pull-to-refresh and destroys a half-filled form. On horizontal scrollers, overscroll triggers browser back-navigation — the same outcome, faster.
**Fix:** `overscroll-behavior: contain` on the scroll container, `overscroll-behavior-x: contain` on horizontal scrollers, body scroll lock while a modal sheet is open with scroll position restored on close.

## The keyboard-covered action

**Detect:** a sticky or fixed bottom action bar; a form whose submit sits at the bottom of the viewport. Reproduce by focusing the last field on a real device.
**Why it fails:** the virtual keyboard occupies a large share of the screen and does not consistently resize the layout viewport, so the action the user is typing toward disappears exactly when they finish typing. Desktop testing never surfaces it because the keyboard never appears.
**Fix:** `dvh`/`svh` units instead of `vh`, `interactive-widget=resizes-content` in the viewport meta where supported, and `window.visualViewport` listeners where the layout must track the keyboard precisely. Verify on device with the keyboard open.

## `user-scalable=no` as the zoom fix

**Detect:** `maximum-scale=1`, `user-scalable=no`, or `minimum-scale=1` in the viewport meta — usually added right after someone noticed iOS Safari zooming on input focus.
**Why it fails:** it treats the symptom (auto-zoom on a sub-16px field) by removing the user's ability to zoom at all, which breaks the primary magnification strategy for low-vision users. It trades a layout annoyance for an accessibility barrier.
**Fix:** raise form-control font size to at least 16px on coarse pointers, enforced in the field primitive. Remove the scale locks.

## `type="number"` for things that aren't quantities

**Detect:** `type="number"` on phone numbers, card numbers, postal codes, PINs, one-time codes, or locale-formatted amounts.
**Why it fails:** the element sanitizes non-conforming input to an empty value, drops leading zeros, ignores `maxlength`, increments on scroll, and rejects locale separators — while not reliably producing a compact keypad anyway.
**Fix:** `type="text"` plus `inputmode="numeric"` or `"decimal"` plus a real `autocomplete` token, with parsing in code.

## The keyboard nobody asked for

**Detect:** inputs with no `inputmode`, no `autocomplete`, no `enterkeyhint` — a full alphabetic keyboard for a quantity, no autofill on an address, a return key labelled "return" in the middle of a five-field form.
**Why it fails:** every missing attribute is taps the user pays for. Missing `autocomplete` on an address form can be thirty of them, on a phone, standing up.
**Fix:** the four-attribute contract on every field. It is one line per input and it is the highest-yield touch change in most forms.

## Feedback under the thumb

**Detect:** validation messages below the field, tooltips opening downward from the trigger, toasts anchored at the very bottom edge, inline spinners rendered at the tap point.
**Why it fails:** the hand covers that region at the moment of the tap. The feedback is rendered, technically delivered, and not seen — so the user taps again.
**Fix:** position feedback above or beside the contact point; place toasts high enough to clear a resting thumb, or make them persistent enough to survive the hand moving away.

## Down-event activation

**Detect:** handlers on `touchstart`, `pointerdown`, or `mousedown` for anything that acts; custom controls that commit before release.
**Why it fails:** it removes the user's only escape hatch — sliding off before lifting — and converts the beginning of a scroll into an action. It also fails SC 2.5.2.
**Fix:** act on the up-event, and let a pointer that moves off the target cancel.

## Sticky hover after tap

**Detect:** on a touch device, a control keeps its hover styling after being tapped, sometimes until another element is tapped.
**Why it fails:** it misrepresents state — the element looks focused, active, or selected when it is not — and it is the most common visible symptom of hover styles written without a capability query.
**Fix:** move hover styling inside `@media (hover: hover) and (pointer: fine)` and give touch devices explicit `:active` feedback instead.

## The pointer test by viewport width

**Detect:** `max-width` breakpoints gating touch sizing, hover affordances, or gesture handlers; `'ontouchstart' in window`; user-agent sniffing.
**Why it fails:** width has never answered "can this be touched". Touchscreen laptops get mouse-sized targets, tablets with keyboards get hover affordances they can't use, and a narrowed desktop window gets touch layout with a mouse. All three are wrong in different directions.
**Fix:** `any-pointer: coarse` for sizing, `hover: hover` for hover enhancements, width for layout only.
