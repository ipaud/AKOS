# AGENTS.md Template (AKOS integration)

Written into a project's `AGENTS.md` (read by Codex and other agents) between markers.

```markdown
<!-- AKOS:START -->
## AKOS Knowledge System

This project integrates AKOS at `~/DEV/AKOS` — a tool-agnostic knowledge system of distilled UX, architecture, security, product, performance, and testing expertise.

**Before non-trivial work, load:**
1. `~/DEV/AKOS/core/constitution.md`, `authority-model.md`, `reasoning-profiles.md`, `review-pipeline.md`
2. `~/DEV/AKOS/packs/personal/pau-avila/` — highest-priority personal rules
3. The 2-5 task-relevant packs under `~/DEV/AKOS/packs/`

**For reviews:** use the role definitions in `~/DEV/AKOS/agents/` and the unified Review Summary format (severity-ranked findings + scores + PASS/PASS WITH FIXES/BLOCKED).

**Safety floor (never waived):** security, accessibility basics, data integrity.
**Defaults:** four async states always; mobile-responsive by default; Supabase RLS at table creation (deployed); challenge complexity; anti-template UI; direct actionable output.

Profile: see `.akos/config.md`.
<!-- AKOS:END -->
```
