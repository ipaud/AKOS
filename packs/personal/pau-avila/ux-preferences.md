# UX Preferences — Pau Avila

UX defaults applied to every app automatically, without needing to be requested per-project.

## Always-on defaults

- **UX principles applied automatically** to all apps — agents load the [Krug](../../ux/steve-krug/README.md), [NN/g](../../ux/nielsen-norman-group/README.md), and [WCAG](../../ux/wcag/README.md) packs for any user-facing surface without being asked.
- **Obvious over clever.** Interface has personality (see [design-language.md](design-language.md)) but the primary action and navigation are always self-evident.
- **Four states by default** — empty/loading/error/success designed for every async surface, from the start, not as a later pass.
- **Mobile/responsive reviewed by default** — every web surface checked at 320px and for touch, not opt-in.
- **Accessibility basics are non-negotiable** — keyboard reachability, accessible names, contrast floors, visible focus — treated as part of "working," not polish.

## Interaction defaults

- Immediate visual feedback on every interaction (<100ms), even when the underlying operation is slower.
- Undo over confirmation for reversible actions; forcing functions (typed confirmation) for irreversible destructive ones.
- Forgiving inputs — accept any reasonable format, normalize in code, never lecture the user about format.
- Honest error messages: what happened, why, what to do next.

## Copy defaults

- Verb-first specific button labels ("Create account", not "Submit").
- No happy talk, no unread instruction blocks — cut aggressively ([Krug copy reduction](../../ux/steve-krug/heuristics.md)).
- Link text describes its destination out of context.

## Review defaults

Every user-facing feature gets, at minimum: UX clarity, accessibility, mobile/responsive, and copy passes — even in Prototype profile, at reduced depth. Production adds the full [review pipeline](../../../core/review-pipeline.md).
