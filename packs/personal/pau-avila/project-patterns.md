# Project Patterns — Pau Avila

Recurring architecture and stack choices across this owner's projects. These are defaults, not mandates — deviate with a stated reason.

## Default stacks

- **Web apps / webapps:** React + Tailwind + Supabase. TypeScript strict mode ([typescript pack](../../frontend/typescript/README.md)). Deployed on a platform with built-in CDN/CI (Vercel/Netlify-class).
- **Games:** Godot.
- **Tooling/scripts:** whatever's fastest to ship — often a small Node/Bash script; no ceremony.
- **Prototypes:** the above, minus the process (skip exhaustive tests, formal architecture) but never the safety floor.

## Architectural defaults

- Start simple: two effective layers (domain + everything) over four-ring Clean Architecture until complexity genuinely demands more ([clean-architecture decision framework](../../architecture/clean-architecture/decision-framework.md)).
- Supabase RLS is the primary authorization layer, not an app-server check ([supabase-rules.md](supabase-rules.md)).
- Prefer server components / SSR for content-heavy, LCP-sensitive pages ([react pack](../../frontend/react/README.md)); client components only where interactivity is needed.
- Reusable prompts, templates, and skills are built once a pattern repeats — the AKOS system itself is an instance of this preference.

## Profile mapping

- Personal experiment / never-deployed → **Prototype** profile.
- Real users, early product → **Startup MVP**.
- Paying users or real user data at scale → **Production**.

Most of this owner's projects sit in Prototype or Startup MVP; agents should assume that unless a project's `.akos/config.md` says otherwise.

## Reuse-first workflow

Before building something new, check: is there an existing AKOS pack, template, prompt, or a prior project pattern that covers 80%+? Prefer adapting it over net-new — matches the [reuse-first development workflow](../../../core/reasoning-engine.md).
