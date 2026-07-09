# Examples — Apple HIG Pack

Invented cases.

## Container grammar

Task: user taps a recipe in a list, then wants to edit it.
- Wrong: recipe opens in a full-screen modal; Edit pushes onto the modal; dismissal ambiguity everywhere.
- Right: recipe **pushes** (parent→detail); Edit opens a **sheet** (scoped task) with Cancel/Save; saving pops the sheet back to the detail view.

## Permission flow (AP15)

- Bad: launch → notification prompt + location prompt + tracking prompt stacked.
- Good: first launch is fully usable. When the user taps "Remind me", an in-app screen explains "We'll send one reminder at your chosen time", *then* triggers the system prompt. Denial → feature shows in-app scheduling instead.

## Dynamic Type survival (AP2)

A card with title, subtitle, price, CTA at default size. At AX5 size:
- Bad: title truncates to one word, CTA half-covered, price overlaps image.
- Good: card switches to a vertical stack layout at accessibility sizes; all text wraps; CTA full-width. Layout rule, not layout picture.

## Dark mode tokens (AP8)

- Bad: `background: #FFFFFF; color: #111`.
- Good: `background: var(--bg-primary)` with dual definitions, or system colors (`systemBackground`, `label`) that adapt automatically — including elevated-surface variants in dark.

## Destructive placement (AH6)

Mail-style swipe: Archive (frequent) full-swipe right; Delete requires deliberate partial-swipe + tap on a red, spatially-separated button — never the full-swipe default on the same edge as archive.

## Mac-worthy port (AP17)

iPhone journaling app → macOS: adds File/Edit/Entry menus (⌘N new entry, ⌘F search), sidebar-list-detail layout in a resizable window, hover states, drag-in image support. Same brand, Mac grammar.
