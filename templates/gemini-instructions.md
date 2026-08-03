# Gemini Instructions Template (AKOS integration)

For Gemini CLI. Use as the project's `GEMINI.md`.

```markdown
# AKOS Integration (Gemini)

This project uses AKOS, a knowledge system at `~/DEV/AKOS`.

Before non-trivial work:
1. Read `~/DEV/AKOS/core/constitution.md`, `authority-model.md`, `reasoning-profiles.md`, `review-pipeline.md`.
2. Read `~/DEV/AKOS/packs/personal/<personal_profile>/` (highest-priority personal rules; `<personal_profile>` from this project's `.akos/config.md`, default `pau-avila`).
3. Load the 2-5 relevant packs from `~/DEV/AKOS/packs/`.

Apply pack principles as constraints while building. For reviews, follow `~/DEV/AKOS/agents/*.md` and produce the unified Review Summary (severity-ranked findings, scores, INCOMPLETE/PASS/PASS WITH FIXES/BLOCKED — INCOMPLETE if a required lens didn't run).

Non-negotiable floor: security, accessibility basics, data integrity.
Defaults: empty/loading/error/success states everywhere; mobile-responsive by default; Supabase RLS at table creation (deployed); challenge unnecessary complexity; anti-template UI; direct actionable output.

Active profile: `.akos/config.md`.
```
