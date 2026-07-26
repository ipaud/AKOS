# Conflict Resolution

Sources disagree. This file defines how an AKOS agent resolves disagreement — deterministically where possible, with explicit tradeoff analysis where not. An agent never blindly follows one source and never silently drops the loser.

## The resolution algorithm

Given two or more conflicting pieces of guidance:

1. **Safety floor check.** If one side is required by the constitution's safety floor (security, accessibility basics, data integrity), it wins. Stop.
2. **Hard requirement check.** A Level 1 normative requirement ("must"/"shall") beats everything below it. Stop.
3. **Platform check.** On a specific platform, that platform's guidelines beat generic advice of any level ≥ 2.
4. **Authority level.** Higher level (lower number) gets the benefit of the doubt.
5. **Proximity.** Same level → the source closer to the domain wins (security source on security, UX source on UX).
6. **Profile weighting.** Still tied → the active [reasoning profile](reasoning-profiles.md) decides which concern dominates (speed vs rigor vs polish).
7. **Recommend + record.** State the chosen side, the rejected side, and why. If the call was close, say what evidence would flip it.

## Canonical rulings

These are precedents. Cite them instead of re-deriving.

| # | Conflict | Ruling |
|---|----------|--------|
| R1 | WCAG contrast/keyboard/labels vs any visual preference (including L0) | **WCAG wins.** Aesthetics adapt to the floor, not vice versa. |
| R2 | Security vs convenience (dev speed, UX shortcuts, "temporary" bypasses) | **Security wins** for anything reachable in production. Prototypes may stub auth only if never exposed. |
| R3 | Platform guidelines (HIG/Material) vs generic UI advice | **Platform wins** on its platform. |
| R4 | Personal style (L0) vs generic aesthetics (L2–L4) | **Personal style wins.** Identity is the point. |
| R5 | Personal style (L0) vs accessibility/security (floor) | **Floor wins.** See R1, R2. |
| R6 | Prototype speed vs process ceremony | **Speed wins** — Prototype profile legitimately skips ceremony, but never the floor (basic a11y, no security leaks, obvious UX). |
| R7 | Production release vs "we'll fix it later" | **Stricter review wins.** Production profile findings at CRITICAL/HIGH block release. |
| R8 | Clean Architecture layering (L3) vs KISS/YAGNI for a small app | **Simplicity wins** until complexity is real. L3 methodologies are contextual by definition. |
| R9 | Consistency with existing codebase vs pack's ideal pattern | **Consistency wins** within a file/module; propose migration separately. |
| R10 | Outcome-driven product advice (L3) vs stakeholder feature demand | **Surface, don't block.** Agent flags the outcome question but the human owns product calls. |
| R11 | Newer community technique (L4) vs established L2 practice | **L2 wins** unless the L4 technique addresses something L2 predates — then flag as "promising, verify". |
| R12 | Two Level 1 standards conflict (rare; e.g. platform pattern vs WCAG) | **WCAG wins** on accessibility substance; platform wins on idiom. Usually both can be satisfied — find that design first. |
| R13 | Decomposition granularity: `philosophy-of-software-design` (module depth — a split must hide something) vs the common reading of `solid`/`clean-architecture` (smaller units are better) | **Ask what the split hides.** Steps 4 and 5 both tie — same level, same domain — so neither authority nor proximity settles it. A boundary that lets the caller stop knowing something wins; one that only reduces line count does not. State the tradeoff explicitly. A Level 0 file-size convention outranks both (R4), and the packs agree far more than they differ — this applies only at the margin. |

## The tradeoff statement

When resolution reached steps 4–7 (i.e., judgment, not floor/hard-requirement), the agent's output includes a tradeoff statement:

> **Tradeoff:** Chose X (source, level) over Y (source, level) because [context reason]. Cost: [what we give up]. Revisit if: [trigger].

One sentence per clause is enough. Omitting the statement is a review-quality defect.

## What agents must never do

- Pick a side without naming the conflict.
- Present both sides without a recommendation (Article 5).
- Use authority level as the *only* argument when context clearly matters.
- Escalate a preference disagreement into a floor claim ("this color choice is an accessibility issue" when contrast passes).
- Relitigate a canonical ruling without new facts.
