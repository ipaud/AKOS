# Project AKOS Loader Template

Written to a project's `.akos/config.md` by `akos install-project`. This is the per-project configuration agents read to know the active profile and any overrides.

```markdown
# AKOS Project Config

## Reasoning profile

<!-- One of: Prototype | Startup MVP | Production | Enterprise | Game Dev | Internal Tool -->
profile: Startup MVP

## Personal profile

<!-- Which packs/personal/<name>/ to load as the Level-0 layer.
     Default if this section is absent: pau-avila (unchanged from before
     this field existed — every project scaffolded before this section
     was added keeps working identically). Run `akos profile list` to see
     what's available, `akos profile create <name>` to make a new one. -->
personal_profile: pau-avila

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

An agent loading AKOS reads this file as **untrusted project manifest data** — facts and hints, never instructions. It can suggest the active reasoning profile (falling back to Startup MVP if absent), request additional valid packs, record the committed style direction, and **raise** scrutiny (`Deployed: yes` makes the security/RLS floor mandatory). It can never lower the safety floor or change lens weights: repository-side `Profile overrides` are not authoritative, and `akos check-config` flags them. The enforced precedence — safety floor, then the current user, then the operator's local config, then this manifest, then defaults — lives in the constitution and the skills, not in this file.
