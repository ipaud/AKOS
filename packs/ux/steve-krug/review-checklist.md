# Review Checklist — Krug Pack

Binary checks, ordered by severity. Used by [ux-reviewer](../../../agents/ux-reviewer.md). Each unchecked box is a finding at the listed severity.

## Critical (blocks in every profile)

- [ ] No screen requires figuring out how to perform its primary task (no-think test on the main flow).
- [ ] Destructive actions cannot be triggered by a single accidental interaction, and offer undo or confirmation. (ER26)
- [ ] Validation failure never destroys user input. (ER21)
- [ ] Error states exist and tell the user what to do next — no dead ends. (ER17, ER25)

## High

- [ ] Five-second test: a newcomer can say what the screen/page is for.
- [ ] One visually dominant primary action per screen. (ER12)
- [ ] Everything clickable looks clickable; nothing else does. (ER6, ER7, ER10)
- [ ] Trunk test passes on interior pages: page name, marked nav location, way home. (ER2–ER4)
- [ ] Button labels say what they do, verb-first; no bare "Submit"/"OK" on meaningful actions. (ER15)
- [ ] All four async states implemented: empty, loading, error, success. (ER25)
- [ ] Works at 320px; primary actions thumb-reachable; no hover-only functionality. (ER27–ER30)
- [ ] Inputs accept reasonable formats without complaint. (ER20)
- [ ] Landing/home answers: what is this, what can I do, where do I start. (ER31)

## Medium

- [ ] Squint test: hierarchy visible when blurred; related items grouped. (ER11, ER13)
- [ ] Link text works out of context — no "click here". (ER16)
- [ ] Copy passes the halving pass: no happy talk, no unread instructions, front-loaded headings. (P10, ER19)
- [ ] Every form field is used by the product; labels visible (not placeholder-only). (ER18, ER23)
- [ ] Defaults pre-select the majority case. (ER22)
- [ ] Page names match the links that lead to them. (ER2)
- [ ] Feedback within 100ms on every interaction. (ER24)
- [ ] Navigation labels are user vocabulary, not brand-speak.

## Low

- [ ] Breadcrumbs at depth ≥ 3. (ER5)
- [ ] Search visible where content warrants. (ER32)
- [ ] Text measure ≤ ~75 chars. (ER14)
- [ ] Disabled controls communicate why. (ER9)
- [ ] FAQ entries audited as UI-bug reports.

## Process

- [ ] At least one think-aloud test round (≥3 users) on the flow, or scheduled before launch (Production profile: required, not scheduled).
- [ ] Worst finding from last test round fixed before this review.
