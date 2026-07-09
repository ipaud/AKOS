# Review Checklist — WCAG Pack

Floor items (★) block in every profile. Full list = AA review for Production.

## Critical ★

- [ ] Primary task completable by keyboard alone; no traps. (WC10, WC11)
- [ ] All interactive elements are native or complete ARIA patterns — no click-divs on task paths. (WC1)
- [ ] Every interactive element and input has an accessible name / bound visible label. (WC2, WC3)
- [ ] Focus visible everywhere. (WC12)
- [ ] Errors identified in text, associated with fields, focus moved to first error. (WC29)
- [ ] Body text and primary controls meet contrast floors. (WC16, WC17)
- [ ] Color never the sole carrier of meaning. (WC18)
- [ ] Nothing flashes >3×/s. (WC35)

## High

- [ ] Modal gauntlet passes (focus in / Escape / contained / restored). (WC11, WC15)
- [ ] Headings real, sequential, honest; one h1; landmarks + skip link. (WC5, WC6)
- [ ] 200% zoom and 320px reflow lose nothing. (WC19)
- [ ] Async status announced via live regions. (WC31)
- [ ] Images alt-treated by purpose (informative/decorative/complex). (WC4)
- [ ] Focus/input never auto-triggers context change. (WC33)
- [ ] Destructive/legal/financial submissions reversible-checked-or-confirmed. (WC30)
- [ ] Touch targets ≥24px floor (44px design bar); gestures and drags have alternatives. (WC23, WC24)

## Medium

- [ ] DOM = focus = visual order; no positive tabindex. (WC13)
- [ ] Sticky chrome never fully obscures focus. (WC14)
- [ ] `lang` set; titles unique and descriptive (SPA route changes included). (WC8, WC9)
- [ ] Autocomplete attributes on personal fields; no redundant re-entry in flows. (WC26, WC28)
- [ ] Auth allows paste/managers/passkeys. (WC27)
- [ ] Tooltips dismissible/hoverable/persistent. (WC21)
- [ ] `prefers-reduced-motion` respected. (WC22)
- [ ] Time limits extendable; auto-updating content pausable. (WC32)
- [ ] Text-spacing overrides don't break layout. (WC20)

## Low

- [ ] Tables use th/scope. (WC7)
- [ ] Help mechanisms in consistent locations. (WC34)
- [ ] Link text descriptive out of context. (O-4)

## Process

- [ ] Automated scan clean (axe/Lighthouse) — entry ticket. (WC36)
- [ ] Three walks performed: keyboard, tree, stress (zoom/reflow/spacing/grayscale).
- [ ] Systemic component failures reported once with component-level fix.
