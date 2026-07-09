# Generic Agent Instructions Template (AKOS integration)

For any LLM coding agent that reads Markdown instructions (Continue, Cline, Roo Code, Windsurf, etc.). Copy into whatever instructions file the tool uses.

```markdown
# AKOS Integration

This project uses AKOS (AI Knowledge Operating System) — a tool-agnostic knowledge base at `~/DEV/AKOS` of distilled UX, architecture, security, product, performance, and testing expertise, all plain Markdown.

## Loading

Before non-trivial work, read in order:
1. `~/DEV/AKOS/core/constitution.md` — accept the articles.
2. `~/DEV/AKOS/core/authority-model.md` — source ranking (L0 personal rules highest, then L1 standards → L4 community; a security/accessibility/data-integrity floor sits above all).
3. `~/DEV/AKOS/core/reasoning-profiles.md` — determine the profile (`.akos/config.md`).
4. `~/DEV/AKOS/core/review-pipeline.md` — the review structure.
5. `~/DEV/AKOS/packs/personal/pau-avila/` — Level-0 personal rules, always apply.
6. The 2-5 task-relevant packs under `~/DEV/AKOS/packs/` (organized by domain: ux, architecture, product, security, performance, frontend, backend, testing, devops).

## Applying

- **Building:** pack principles/engineering-rules are constraints and defaults. Surface conflicts, tradeoffs, and deliberate profile-based skips.
- **Reviewing:** use `~/DEV/AKOS/agents/*.md`; output the unified Review Summary (Context → Strengths → Critical → High → Medium → Low → Tradeoffs → Packs Used → Scores → Next Iteration → PASS / PASS WITH FIXES / BLOCKED).
- Cite authority level for load-bearing guidance; give a tradeoff statement on any conflict; back CRITICAL/HIGH findings with high confidence.

## Never waive
Security, accessibility basics, data integrity — the safety floor, at any profile.

## Owner defaults
Four async states always; mobile-responsive by default; Supabase RLS at table creation for deployed projects; challenge unnecessary complexity; anti-template UI; direct actionable output.
```
