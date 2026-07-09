# Codex Instructions Template (AKOS integration)

For OpenAI Codex CLI. Codex reads `AGENTS.md` by default; use this if you want a standalone instructions file, or copy the section into `AGENTS.md` (see [AGENTS.md template](AGENTS.md)).

```markdown
# AKOS Integration (Codex)

This project uses AKOS, a tool-agnostic knowledge system at `~/DEV/AKOS`.

Before non-trivial work:
1. Read `~/DEV/AKOS/core/constitution.md`, `authority-model.md`, `reasoning-profiles.md`, `review-pipeline.md`.
2. Read `~/DEV/AKOS/packs/personal/pau-avila/` (highest-priority personal rules).
3. Load the 2-5 packs from `~/DEV/AKOS/packs/` relevant to the current file/task.

Apply pack principles as build-mode constraints. For reviews, follow `~/DEV/AKOS/agents/*.md` and output the unified Review Summary (severity-ranked findings, scores, PASS/PASS WITH FIXES/BLOCKED).

Non-negotiable floor: security, accessibility basics, data integrity.
Defaults: four async states; mobile-responsive by default; Supabase RLS at table creation (deployed); challenge complexity; anti-template UI; direct actionable output.

Active profile: `.akos/config.md`.
```
