# Design Language — Pau Avila

## Anti-template stance

Every UI surface should look intentional and specific to the product — never a default Tailwind/shadcn template shipped unmodified, never a generic centered-hero-plus-gradient landing page. Before writing frontend code, pick a specific style direction (editorial, neo-brutalist, glassmorphic, bento, etc.) rather than defaulting to "clean minimal." See the [Refactoring UI pack](../../ux/refactoring-ui/README.md) for the systems to build that direction from, and the anti-template checklist below.

## Anti-template checklist (apply to every meaningful UI surface)

- [ ] Clear hierarchy through scale/weight/color contrast, not size alone
- [ ] Intentional spacing rhythm, not uniform padding everywhere
- [ ] Depth/layering (overlap, shadow, surfaces, or motion)
- [ ] Typography with a real pairing strategy, not a single default stack
- [ ] Color used semantically, not just decoratively
- [ ] Designed hover/focus/active states
- [ ] At least one deliberate grid-breaking or bento moment where it fits
- [ ] Motion that clarifies, not distracts

## Identity rules

- Personality lives in: color, type pairing, illustration/iconography style, motion flavor, copy voice, radius/shape family.
- Personality never overrides: [WCAG floor](../../ux/wcag/README.md), obviousness of primary actions ([Krug](../../ux/steve-krug/README.md)), or the four-states requirement.
- Default to picking a real style direction at project start, documented in one line (e.g. "dark luxury, sharp type, restrained accent") so every subsequent screen stays consistent with it.

## Practical defaults

- Prefer Tailwind as the styling engine, but tokenize the design system on top of it (see [design-systems pack](../../frontend/design-systems/README.md)) rather than shipping raw utility defaults.
- Dark mode is a deliberate choice per project, not an automatic default — decide based on what the product actually wants.
