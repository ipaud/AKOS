# Personal Layer — <your name>

**Authority: Level 0** — highest priority in AKOS, overridden only by the safety floor (security, accessibility basics, data integrity — see [core/constitution.md](../../../core/constitution.md)) and hard legal/standards requirements.

This is not a distillation of an external source — it's your own conventions, preferences, and patterns, recorded so every AKOS-loaded agent applies them automatically without being asked each time.

## Files

- `principles.md` — durable working principles. Write this first.
- `ai-agent-rules.md` — how you want an agent to behave (tone, defaults, what NOT to do).
- `coding-preferences.md` — stack, style, and pattern preferences.
- `ux-preferences.md` — UX/copy defaults you want applied without being asked.
- `design-language.md` — visual identity, if you have projects with UI.
- `project-patterns.md` — recurring structural choices across your projects.
- `supabase-rules.md` — only relevant if you use Supabase; delete if not.

## Activating this profile

```bash
akos profile use <your name>
```

writes `personal_profile: <your name>` into the current project's `.akos/config.md`.
