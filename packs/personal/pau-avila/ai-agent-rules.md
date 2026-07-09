# AI Agent Rules — Pau Avila

How coding agents should behave on this owner's projects. Applies across Claude Code, Codex, Cursor, Gemini, and any AKOS-loading agent.

## Working style

- **Be direct and actionable.** State the recommendation, then do it. Don't present unranked option surveys unless genuinely asked to compare — pick, justify briefly, proceed.
- **Challenge unnecessary complexity actively.** If a request or an existing plan adds an abstraction/dependency/layer that hasn't earned its place, push back before building it — this is a standing instruction ([principle 2](principles.md)), not something to wait for permission on.
- **Prefer complete, ready-to-use output.** This owner values complete prompts, complete templates, complete implementations over partial scaffolds that need filling in.
- **Reuse before rebuild.** Check for an existing AKOS pack/template/prompt or prior pattern covering 80%+ before writing net-new.

## Defaults to apply without being asked

- Load the [personal layer](README.md), UX packs, and (for deployed projects) security/Supabase packs automatically for relevant work.
- Design the four states (empty/loading/error/success) for every async surface.
- Review mobile/responsive by default on web work.
- Enforce the safety floor (security, accessibility basics, data integrity) regardless of profile.

## Profile assumption

Assume **Prototype** or **Startup MVP** profile unless the project's `.akos/config.md` states otherwise — most of this owner's work sits there. Scale process accordingly ([reasoning-profiles](../../../core/reasoning-profiles.md)); don't impose Enterprise ceremony on a fast prototype.

## Review triggers this owner wants enforced

- Security + Supabase/RLS review before any deployed project is "done."
- UX + accessibility + mobile + copy passes on every user-facing feature.
- A complexity-challenge pass on any design introducing new abstractions.

## What NOT to do

- Don't hedge endlessly or defer decisions the agent can reasonably make.
- Don't ship generic template UI ([design-language.md](design-language.md)).
- Don't relax the safety floor for speed, even in Prototype.
- Don't add speculative generality "for later."
