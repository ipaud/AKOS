# Principles — Krug Pack

Durable rules. Violating one requires an explicit tradeoff statement.

## P1 — The no-think principle

A user should never have to stop and think about the interface itself. Questions like "is that clickable?", "where am I?", "what does this word mean here?", "did that work?" are defects, not quirks.

## P2 — Self-evident first, self-explanatory as fallback

Design every element to be understood at a glance. When a concept is genuinely novel and glance-level clarity is impossible, minimal in-place explanation is the fallback — never a manual, never a tour that can be skipped and forgotten.

## P3 — Design for scanning

Assume the page will be scanned, not read. Consequences: clear visual hierarchy (importance = prominence), headings that summarize honestly, front-loaded sentences, one idea per paragraph, links whose text alone says where they go.

## P4 — Support satisficing

Make the first plausible choice the correct one, and make wrong choices cheap: instant back, preserved state, no punishment. Never rely on users comparing all options before acting.

## P5 — Conventions are borrowed clarity

A convention (logo top-left links home, cart icon top-right, underlined links, search field with magnifier) is instantly understood because thousands of other sites taught it. Innovate on your product's substance, not on solved interface problems. Break a convention only when the replacement is *so* clear it needs no learning, or the value is worth the learning cost — and you've tested that claim.

## P6 — Visual hierarchy must match logical hierarchy

The more important something is, the more prominent. Related things look related and sit together. Nesting shows containment. When visual hierarchy lies (a trivial banner dominating, the primary action visually equal to five secondary ones), users misread the page — and blame themselves.

## P7 — Clickability must be unambiguous

Everything clickable must look clickable; nothing unclickable should. Affordance ambiguity forces micro-experiments ("hover and see") that burn goodwill. Flat design is welcome to be flat *except* where it erases this distinction.

## P8 — Navigation is orientation, not just transport

Persistent navigation tells users where they are, what exists, and how to move — on every page, because users teleport in via deep links. Page names must match the link that led there, appear where the eye expects a title, and be marked in the nav ("you are here").

## P9 — The homepage answers four questions in seconds

What is this? What can I do here? Why should I be here instead of elsewhere? Where do I start? A first-time visitor who can't answer these within a few seconds of landing is already leaving. The tagline next to the logo is the hardest-working sentence in the product.

## P10 — Omit needless words

Half the words on most pages can go; then half of what remains. Happy talk (self-congratulatory intros), instructions (nobody reads them — make the thing self-explanatory instead), and redundant labels are the first cuts. Less text makes the useful text visible.

## P11 — Every page needs an obvious primary action

One thing should visually dominate as "what you do here". Multiple equal-weight actions means the design hasn't decided — so the user has to.

## P12 — Usability testing is a habit, not an event

One morning a month, three users, whatever's ready — live site, prototype, competitor's site. Watch them think aloud. Fix the worst observed problem before the next round. Debating what users will do is a smell; watching them is the cure.

## P13 — Do the least you can do (when fixing)

The cheapest fix that removes the observed confusion wins over the redesign. A tweak ships this week; a redesign spawns a project. Usability debt is paid down in small, continuous installments.

## P14 — Mobile is the priority filter

Small screens force honest prioritization. Design mobile to expose what matters; keep everything reachable (full functionality, even if layout differs); never require precision a thumb doesn't have; never rely on hover.

## P15 — Accessibility is usability, continued

The same moves that help everyone (clear hierarchy, real headings, honest labels, keyboard-reachable actions) are the foundation of accessibility. Treat WCAG basics as part of usability work, not a separate compliance chore. Details: [wcag pack](../wcag/principles.md).

## P16 — Goodwill is the budget

Every design decision is a deposit or withdrawal from the user's goodwill reserve. When arguing for a decision that costs the user effort for the product's benefit, name it as a withdrawal and justify it.
