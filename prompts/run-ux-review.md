# Prompt: Run UX Review

---

Load AKOS (`~/DEV/AKOS/prompts/load-akos.md`) and run the **full frontend/UI
review** workflow (`~/DEV/AKOS/workflows/ui-screen-review.md`) on [describe the
screen/flow]. This is the five-lens UI chain, not the single UX or Frontend
quality lens. Apply the active profile explicitly; when no profile is supplied,
use **Startup MVP**.

Act as the agents in order, loading their packs:
1. `agents/ux-reviewer.md` — five-second test, no-think walk, trunk test, squint test, four states.
2. `agents/accessibility-reviewer.md` — keyboard walk, tree walk, stress walk.
3. `agents/mobile-reviewer.md` — 320px, thumb zones, touch targets, poor network.
4. `agents/copy-reviewer.md` — labels, errors, empty-state copy.
5. `agents/frontend-reviewer.md` — visual craft, hierarchy, designed states, anti-template.

Merge into one Review Summary (standard format), including the Mobile score
only when rendered/runtime evidence supports it. For each finding: name the
pack, the severity, and the smallest fix ("do the least you can do"). Never pass
a screen missing its empty/loading/error states. Final decision = worst
individual decision.
