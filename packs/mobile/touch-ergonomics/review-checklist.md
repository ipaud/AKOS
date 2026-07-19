# Review Checklist — Touch Ergonomics Pack

Binary checks, ordered by severity. Used by [mobile-reviewer](../../../agents/mobile-reviewer.md). Each unchecked box is a finding at the listed severity. Checks marked ★ are safety-floor items and block in every reasoning profile.

Reviewing touch means holding the device. A narrow desktop window has a mouse, hover, no virtual keyboard, and no hand covering the screen — it cannot detect most of what follows. Where a check needs the diff rather than the screen, it says so.

## Critical (blocks in every profile)

- [ ] ★ No interactive element is under 24×24 CSS px without a named, genuinely applicable SC 2.5.8 exception. (TEE1)
- [ ] ★ No two hit areas overlap; every icon-button cluster satisfies `gap ≥ F − (wA + wB)/2`. (TEE9, TEE10)
- [ ] ★ No hit area of any control overlaps a **destructive** control's hit area. (TEE11)
- [ ] ★ No meaning, control, or warning exists only in a hover state or `title` attribute. (TEE15, TEE16)
- [ ] ★ Every gesture-triggered action has a visible single-tap equivalent, unless the gesture is essential to the function. (TEE46, SC 2.5.1)
- [ ] ★ Actions fire on the up-event and are cancellable by moving off before release. (TEE53, SC 2.5.2)
- [ ] ★ **Diff check:** no user-entered numeric string reaches `Number()` / `parseFloat()` / `parseInt()` without a locale-aware parser. (TEE39)
- [ ] ★ **Diff check:** no `|| 0`, `?? 0`, or `isNaN(x) ? 0 : x` on a parsed user value in any path that persists data. (TEE40)
- [ ] ★ Unparseable numeric input produces an error and blocks the commit; it is never silently stored as `0`. (TEE42)
- [ ] ★ The viewport meta does not contain `user-scalable=no`, `maximum-scale=1`, or `minimum-scale=1`. (TEE35)

## High

- [ ] Primary, destructive, repeated, and dismiss controls are at least 44×44 (48 on Material surfaces). (TEE2, TEE7)
- [ ] Measured hit areas match the claim — verified from client rects, not from the design file. (TEE3)
- [ ] Row-level actions in tables, lists, and grids meet the same floor as standalone buttons. (TEE5)
- [ ] Form controls render at ≥16px computed font size on coarse-pointer devices. (TEE34)
- [ ] The 16px floor is enforced in the shared field primitive plus a backstop, not only documented. (TEE36)
- [ ] A lint or CI check fails on raw `<input>`/`<select>`/`<textarea>` outside the field primitive. (TEE37)
- [ ] Every input declares `type`, `inputmode` where it differs from the default, and a valid `autocomplete` token. (TEE28, TEE29)
- [ ] `type="number"` appears only on true quantities — not phones, cards, postal codes, PINs, or locale-formatted amounts. (TEE31)
- [ ] The primary action of a task screen is reachable in the bottom third on phone viewports. (TEE22)
- [ ] No state-advancing action exists only above a scroll region longer than one viewport. (TEE23)
- [ ] Destructive controls are not immediate neighbours of the primary action, and not in the bottom-third thumb zone of a repeated-use screen. (TEE24)
- [ ] Fixed/sticky elements verified with the virtual keyboard open; the primary action is not covered. (TEE26)
- [ ] Row actions, edit affordances, drag handles, and delete controls are persistently visible on coarse pointers. (TEE16)
- [ ] Sizing and spacing branch on `any-pointer: coarse`, never on `max-width`; no UA sniffing or `ontouchstart` checks. (TEE19, TEE20)
- [ ] Scrollable overlays set `overscroll-behavior: contain`; body scroll is locked while a modal sheet is open. (TEE50, TEE52)
- [ ] Consequential actions offer undo with a stated window, rendered within thumb reach. (TEE54)
- [ ] Numeric-input tests cover at least one dot-locale and one comma-locale. (TEE45)

## Medium

- [ ] Adjacent targets have ≥8px visual separation even when both meet the floor. (TEE12)
- [ ] Hit-expanding pseudo-elements derive their bleed from the floor and record the neighbours checked. (TEE13, TEE14)
- [ ] Checkbox and radio hit areas include their labels via a real `<label>` association. (TEE6)
- [ ] `enterkeyhint` is set across multi-field forms (`next` … `done`/`send`). (TEE30)
- [ ] Codes and identifiers set `autocapitalize="off"`, `autocorrect="off"`, `spellcheck="false"`. (TEE33)
- [ ] Money and quantity fields echo the parsed value back, locale-formatted, before commit. (TEE43)
- [ ] Values are stored canonically and formatted for display via locale APIs. (TEE44)
- [ ] Parsing handles grouping separators, non-breaking spaces, currency symbols, and empty input, with separators derived from `Intl`. (TEE41)
- [ ] `touch-action: manipulation` on tappable controls; `touch-action: none` only on real custom-gesture surfaces. (TEE49)
- [ ] Horizontal scrollers set `overscroll-behavior-x: contain`. (TEE51)
- [ ] Custom drag interactions are inset from system-gesture edge strips. (TEE48)
- [ ] Bottom-anchored bars respect `env(safe-area-inset-bottom)`. (TEE25)
- [ ] Viewport-height layouts use `dvh`/`svh`; keyboard-tracking layouts use `visualViewport`. (TEE27)
- [ ] Feedback (validation, tooltips, toasts) renders above or beside the contact point, not under the hand. (TE2)
- [ ] Hover styles sit inside `@media (hover: hover)`; no sticky hover state persists after a tap. (TEE18, TEE21)
- [ ] Confirming buttons in dialogs are not placed where the user's finger just landed. (TEE54)

## Low

- [ ] Icon glyph size is decoupled from target size; targets grew, glyphs didn't. (TEE4)
- [ ] Native pickers preferred over custom dropdowns, or the custom control meets every rule here on its own. (TEE38)
- [ ] Standalone action-styled links meet the floor; inline text links correctly claim the inline exception. (TEE8)
- [ ] Touch devices get explicit `:active` feedback in place of hover states. (TEE21)

## Process

- [ ] The flow was exercised on a real device, held in one hand, at the tallest supported size.
- [ ] The flow was exercised with the virtual keyboard open.
- [ ] The flow was exercised with the device language set to a comma-locale, re-entering every number.
- [ ] Every hit-area overlay in the diff had its gap arithmetic computed and recorded.
- [ ] For each finding fixed, the enforcement rung was recorded — primitive, lint, backstop, or instance-only. Instance-only fixes are reported as unfixed. (TE14)
