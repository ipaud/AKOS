# Project AKOS Loader Template

Written to a project's `.akos/config.md` by `akos install-project`. This is the per-project configuration agents read to know the active profile and any overrides.

```markdown
# AKOS Project Config

## Reasoning profile

<!-- One of: Prototype | Startup MVP | Production | Enterprise | Game Dev | Internal Tool -->
profile: Startup MVP

## Project context

- **Stack:** <!-- e.g. React + Tailwind + Supabase; Godot; etc. -->
- **Deployed:** <!-- yes/no — determines whether security/RLS floor applies -->
- **Primary surface:** <!-- web app / mobile / game / internal tool -->

## Profile overrides

<!-- Any deviation from the profile's default weights, with a reason.
     Example: "Elevate performance to weight 3 — this is a latency-sensitive
     trading UI even though it's still MVP." -->

## Packs to always load for this project

<!-- Beyond the personal layer and core. Example:
     - packs/frontend/react
     - packs/backend/supabase
     - packs/ux/wcag -->

## Style direction

<!-- The one-line design direction chosen for this project, so every screen
     stays consistent. Example: "Dark luxury, sharp serif headings,
     restrained single accent." -->

## Notes

<!-- Anything project-specific an agent should know. -->
```

## How agents use it

An agent loading AKOS reads this file to determine the active reasoning profile (falling back to Startup MVP if absent), which packs to always load, whether the security/RLS floor is active (deployed projects), and the committed style direction. Overrides here take precedence over profile defaults but never over the safety floor.
