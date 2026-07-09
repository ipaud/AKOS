# Principles — Pau Avila

Core working principles across all projects, highest priority (Level 0) short of the safety floor.

1. **Speed to a working prototype matters.** Most projects start as fast prototypes — optimize early iterations for learning, not completeness. Apply [Prototype/Startup MVP reasoning profiles](../../../core/reasoning-profiles.md) by default unless told otherwise.
2. **Challenge unnecessary complexity, always.** Before adding an abstraction, dependency, or layer, agents should ask whether it's earned its place right now — not defer this to a "someday" review. This is a standing instruction, not a one-time reminder.
3. **Reusable systems over one-off solutions**, but only after a pattern repeats — build templates, prompts, and skills that generalize once something has proven itself twice, not preemptively.
4. **Strong visual identity, but usability stays non-negotiable.** Personality and distinctiveness are a real product requirement — see [design-language.md](design-language.md) — but never at the cost of the interface being obvious (per [Krug](../../ux/steve-krug/README.md)).
5. **Direct, actionable output over hedged or exploratory output.** State the recommendation; don't present an unranked list of options unless genuinely asked to compare.
6. **Security and Supabase/RLS review is mandatory for anything beyond a local, never-deployed prototype.** No exceptions negotiated per-project — see [supabase-rules.md](supabase-rules.md).
7. **Mobile/responsive review by default** on every web project, not opt-in.
8. **Empty/loading/error/success states are considered from the start**, not bolted on later — treated as part of "done," per [Krug ER25](../../ux/steve-krug/engineering-rules.md).
9. **Prefer the stack already in use** (see [project-patterns.md](project-patterns.md)) over introducing a new tool for a one-off need, unless the existing stack genuinely can't do the job.
