# Reasoning Engine

How an agent actually thinks with AKOS loaded: the loop that connects task → profile → packs → decision → output. The other core files are the parts; this is the assembly.

## The loop

```
1. FRAME    What is the task? Build, review, decide, or explain?
2. PROFILE  Which reasoning profile applies? (ask once if unknown)
3. LOAD     Which packs matter? Load personal layer + the 2-5 packs
            closest to the task. Never load everything.
4. APPLY    Work the task using pack principles/rules. Cite level
            (L0-L4) for load-bearing guidance.
5. CONFLICT Any disagreement between sources? Run conflict-resolution.
            Emit tradeoff statements.
6. CHECK    Confidence per claim (confidence-model). Verify checkable
            claims in the artifact before asserting.
7. OUTPUT   Task-appropriate format. Reviews use the unified report.
            Decisions use the five-step frame. Builds ship code + notes.
8. DEBT     Note what was deliberately skipped per profile, so
            promotion to a stricter profile knows where to look.
```

## Pack loading discipline

Loading everything defeats the system — context fills with noise and the agent averages sources instead of ranking them. Selection rules:

- **Always:** `packs/personal/pau-avila/` (Level 0), the constitution's loading order.
- **By task domain:** the agent definition in `agents/*.md` names its packs; use that list for reviews.
- **By file type touched:** UI files → ux packs; queries/migrations → postgres/supabase + security; API routes → rest/security.
- **Depth by need:** quick pass → `heuristics.md` + `review-checklist.md` only; deep review → add `principles.md`, `anti-patterns.md`, `engineering-rules.md`; teaching → add `philosophy.md`, `mental-models.md`.

## Build mode vs review mode

**Build mode** (writing code/design): packs act as constraints and defaults. Apply silently; don't narrate every rule. Surface only conflicts, tradeoffs, and deliberate profile-based skips.

**Review mode** (judging an artifact): packs act as checklists. Every finding names its source pack and severity. The unified report format is mandatory.

**Decide mode**: [decision-framework.md](decision-framework.md) drives; packs supply criteria.

## Multi-agent composition

When a task warrants several lenses (full pipeline run), run agents in [review-pipeline](review-pipeline.md) order. Each agent's findings feed the next (an accessibility fix can change the UX review). The final report merges per-agent sections; final decision = worst individual decision.

## Self-checks before emitting output

- Did I cite sources for load-bearing claims, with levels?
- Did every judgment-call conflict get a tradeoff statement?
- Are CRITICAL/HIGH findings backed by Certain/High confidence?
- Did I challenge complexity at least once if the design has any? (Art. 7)
- Are empty/loading/error/success states covered? (Art. 8)
- Is the output actionable — could someone fix things from it alone? (Art. 10)
