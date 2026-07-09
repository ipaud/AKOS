# Workflow: New Project

Bootstrapping a new app/site/tool from scratch with AKOS loaded.

## Steps

1. **Set the reasoning profile.** Pick from [reasoning-profiles](../core/reasoning-profiles.md): most of this owner's work is Prototype or Startup MVP. Record it in `.akos/config.md`.
2. **Load the personal layer.** [pau-avila principles](../packs/personal/pau-avila/principles.md), [project-patterns](../packs/personal/pau-avila/project-patterns.md), [design-language](../packs/personal/pau-avila/design-language.md) — these set stack, identity, and defaults.
3. **Reuse-first check.** Is there an existing AKOS template/prompt or prior pattern covering 80%+? Adapt over building net-new.
4. **Product framing** (skip for pure prototypes): what problem, what outcome? Light [product-reviewer](../agents/product-reviewer.md) pass.
5. **Pick a style direction** before any UI code ([design-language](../packs/personal/pau-avila/design-language.md)) — avoid generic template defaults.
6. **Scaffold with defaults:** React + Tailwind + Supabase (web), TypeScript strict, tokenized design system. Two-layer architecture until complexity demands more.
7. **Enable RLS at table creation** for any Supabase table with real user data ([supabase-rules](../packs/personal/pau-avila/supabase-rules.md)) — from the start, even in prototype if deployed.
8. **Wire the four states** into every async surface from the beginning.
9. **Run `akos install-project`** to write the integration files (CLAUDE.md, AGENTS.md, etc.).

## Profile adjustments

- **Prototype:** steps 4, 6-architecture, and formal testing relaxed; steps 2, 5, 7 (if deployed), 8 still apply.
- **Production:** full — add architecture planning, test setup, CI/CD, monitoring from the start.

## Exit criteria

A running skeleton with the chosen style direction visible, RLS on (if deployed), four states stubbed, and the integration files in place.
