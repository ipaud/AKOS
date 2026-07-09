# Mental Models — WCAG Pack

## The accessibility tree

Parallel to the DOM, the browser builds an accessibility tree: nodes with **role** (what it is), **name** (what it's called), **state/value** (what it holds), and **relationships** (what it belongs to). Assistive technology reads *only this tree*. Everything visual — layout, color, iconography — must have a representative in the tree or it doesn't exist for AT users. Debugging accessibility = debugging this tree (browser devtools expose it).

## Name, role, value — the component contract

Every interactive element answers three questions to the tree: What is it (role: button, checkbox, tab)? What's it called (name: computed from content, label, aria-label)? What state is it in (checked, expanded, disabled, 40%)? Native HTML answers all three automatically. Custom widgets must answer manually — and keep answers current as state changes. A custom dropdown that looks perfect but reports `<div> "" (no role)` is a mute button on the interface's API.

## The curb-cut effect

Curb cuts were built for wheelchairs; they serve strollers, luggage, carts, bikes. Accessibility features follow the same economics: captions (deaf users → gyms, offices, language learners), keyboard paths (motor impairments → power users), contrast (low vision → sunlight), reflow (magnification → mobile). Frame accessibility investments by their full beneficiary set.

## Situational, temporary, permanent

One arm: permanent (amputation), temporary (fracture), situational (holding a baby). Vision, hearing, cognition, motor control all have this triple. Design for the permanent case and the other two come free — and the other two include *every user sometimes*.

## Assistive tech is a modality, not a device list

Screen readers (VoiceOver, NVDA, JAWS, TalkBack), magnifiers, voice control, switch access, keyboard-only, high-contrast modes, reduced motion. Don't design for specific products; design for the modality contract: everything perceivable without vision, operable without pointer, understandable without guessing, robust in the tree — then the whole category works.

## Automated vs manual detection split

Automated scanners (axe, Lighthouse) reliably catch: contrast failures, missing names/alt, missing labels, invalid ARIA, missing lang, duplicate IDs. They cannot catch: whether alt text is *useful*, whether focus order makes *sense*, whether keyboard flows *complete tasks*, whether announcements are *meaningful*. Rule of thumb: scanners find ~a third of failures. The manual third-pass: keyboard walk, screen-reader walk, zoom/reflow walk.

## The two audits

- **Build-time contract:** engineering rules enforced in component library + linting (one-time cost, product-wide payoff). Accessible component libraries make the accessible path the lazy path.
- **Surface audit:** per-screen review walking the checklist. Without the first, the second finds the same failures forever.
