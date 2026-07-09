# CLAUDE.md Template (AKOS integration)

This is the AKOS section that `akos install-project` writes into a project's `CLAUDE.md`, between markers so it can be safely re-generated without clobbering your own content.

```markdown
<!-- AKOS:START -->
## AKOS — AI Knowledge Operating System

This project uses AKOS (global knowledge system at `~/DEV/AKOS`). Before working on user-facing features, architecture, security, or data, load the relevant AKOS knowledge.

**Bootstrap (read in order):**
- `~/DEV/AKOS/core/constitution.md` — top-level articles
- `~/DEV/AKOS/core/authority-model.md` — source ranking (L0 personal → L4 community, with a security/accessibility/data-integrity floor)
- `~/DEV/AKOS/core/reasoning-profiles.md` — pick the profile (see `.akos/config.md`)
- `~/DEV/AKOS/core/review-pipeline.md` — the review structure
- `~/DEV/AKOS/packs/personal/pau-avila/` — Level-0 personal rules (always apply)

**Load task-relevant packs from** `~/DEV/AKOS/packs/` (by domain — don't load everything).
**For reviews, use** `~/DEV/AKOS/agents/` and produce the unified Review Summary format.

**Non-negotiable floor (every profile):** security, accessibility basics, data integrity. Never traded for speed.
**This owner's defaults:** four states (empty/loading/error/success) on every async surface; mobile/responsive by default; Supabase RLS on at table creation for deployed projects; challenge unnecessary complexity; direct, actionable output; anti-template UI.

Active profile and any project-specific overrides live in `.akos/config.md`.
<!-- AKOS:END -->
```
