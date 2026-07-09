# Engineering Rules — Krug Pack

Checkable in the artifact. A reviewer can verify each rule mechanically; violations are findings.

## Identity & orientation

- ER1. Site/app logo appears top-left (LTR locales) on every screen and links to home.
- ER2. Every page has exactly one `<h1>`, and its text matches (or clearly contains) the label of the link/button that navigates there.
- ER3. Persistent navigation appears on every page except focused funnels (checkout, sign-up), which instead show a minimal header with an explicit way out.
- ER4. Current location is marked in navigation (`aria-current="page"` + visual state).
- ER5. Sections ≥ 3 levels deep show breadcrumbs.

## Clickability

- ER6. Links and buttons are visually distinct from body text and from each other (buttons act, links go).
- ER7. No interactive element relies on hover alone to reveal that it is interactive or what it does.
- ER8. Click/tap targets ≥ 44×44 CSS px, or padded to that effective size; interactive targets have ≥ 8px separation.
- ER9. Disabled states are visually distinct AND explain (or make discoverable) why they're disabled.
- ER10. Non-interactive elements do not use hand cursors, button styling, or link coloring.

## Hierarchy & scanning

- ER11. Heading levels are semantic and sequential (`h1 → h2 → h3`, no skips, no styling-only headings).
- ER12. The primary action on each screen is visually dominant: at most one primary-styled button per view.
- ER13. Related controls are visually grouped; group spacing exceeds within-group spacing.
- ER14. Body text columns ≤ ~75 characters; text is never justified into rivers.

## Copy

- ER15. Button labels are verb-first and specific ("Save changes", "Send invite" — not "OK", "Submit", "Continue" where the object is ambiguous).
- ER16. Link text describes its destination out of context — no "click here", "learn more" without an object.
- ER17. Error messages state what happened, why (if known), and the next action — in user language, no codes-only errors.
- ER18. Forms label every field visibly (placeholder ≠ label); required/optional is marked on the minority case.
- ER19. Instructional text, where unavoidable, is ≤ 2 short sentences and adjacent to the thing it explains.

## Forms & input

- ER20. Inputs accept all reasonable formats (whitespace, dashes, case) and normalize server-side; format errors the code could fix itself are never shown to users.
- ER21. Every form preserves entered data on validation failure and on back-navigation.
- ER22. Sensible defaults are pre-selected for the majority case; nothing destructive is a default.
- ER23. Field count is minimal: each field either changes behavior or is removed.

## Feedback & states

- ER24. Every interaction produces visible feedback within 100ms (pressed state, spinner, optimistic update).
- ER25. Every async surface implements all four states: empty (with guidance to first action), loading (skeleton/spinner), error (with retry), success/content.
- ER26. Destructive actions require confirmation proportional to cost (undo > confirm dialog > typed confirmation), never a bare instant delete for user data.

## Mobile/responsive

- ER27. Layouts function at 320px width with no horizontal scroll.
- ER28. Primary actions sit in thumb-reachable zones on mobile viewports.
- ER29. No functionality is desktop-only unless technically impossible on mobile; parity gaps are documented decisions.
- ER30. Hover-only interactions have touch equivalents.

## Home / landing

- ER31. The viewport-visible landing content answers: what is this, what can I do, where do I start. A tagline near the logo states the value proposition in plain words.
- ER32. Site search (where content warrants it) is a visible input, top-right or prominent, not buried behind an icon on desktop.
