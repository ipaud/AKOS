# Personal Layer — Pau Avila

**Authority: Level 0** — highest priority in AKOS, overridden only by the safety floor (security, accessibility basics, data integrity — see [core/constitution.md](../../../core/constitution.md)) and hard legal/standards requirements.

This is not a distillation of an external source — it's the owner's own conventions, preferences, and patterns, recorded so every AKOS-loaded agent applies them automatically without being asked each time.

## File map

| File | Covers |
|------|--------|
| [principles.md](principles.md) | Core working principles across all projects |
| [design-language.md](design-language.md) | Visual identity defaults and anti-template stance |
| [project-patterns.md](project-patterns.md) | Recurring architecture/stack patterns |
| [coding-preferences.md](coding-preferences.md) | Code style and tooling defaults |
| [ux-preferences.md](ux-preferences.md) | UX defaults applied to every app |
| [supabase-rules.md](supabase-rules.md) | Supabase/RLS conventions for this owner's projects |
| [ai-agent-rules.md](ai-agent-rules.md) | How coding agents should behave on this owner's projects |

## How to use

Every AKOS-loading agent reads this directory as part of its [bootstrap loading order](../../../core/constitution.md#loading-order) — always, regardless of task. When a rule here conflicts with a generic pack recommendation, this layer wins (Ruling R4, [core/conflict-resolution.md](../../../core/conflict-resolution.md)) — unless the generic recommendation is enforcing the safety floor, in which case the floor wins (Ruling R5).
