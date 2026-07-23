# Review Pipeline

Every user-facing feature passes through twelve review lenses before it's considered done. The active [reasoning profile](reasoning-profiles.md) decides which steps are strict, light, or skipped — the pipeline order never changes.

## The twelve steps

| # | Lens | Agent | Core question |
|---|------|-------|---------------|
| 1 | Product clarity | [product-reviewer](../agents/product-reviewer.md) | Does this solve a real user problem? Is the outcome defined? |
| 2 | UX clarity | [ux-reviewer](../agents/ux-reviewer.md) | Can a first-time user accomplish the task without thinking? |
| 3 | Accessibility | [accessibility-reviewer](../agents/accessibility-reviewer.md) | Keyboard, contrast, names, focus, semantics — does it pass? |
| 4 | Mobile/responsive | [mobile-reviewer](../agents/mobile-reviewer.md) | Does it work at 320px, with touch, on slow networks? |
| 5 | Copywriting | [copy-reviewer](../agents/copy-reviewer.md) | Is every word earning its place? Are labels honest and obvious? |
| 6 | Frontend quality | [frontend-reviewer](../agents/frontend-reviewer.md) | Semantic HTML, state handling, component hygiene, visual polish? |
| 7 | Architecture | [architecture-reviewer](../agents/architecture-reviewer.md) | Right-sized structure? Dependencies point the right way? |
| 8 | Security | [security-reviewer](../agents/security-reviewer.md) | AuthN/AuthZ, injection, secrets, RLS, OWASP pass? |
| 9 | Performance | [performance-reviewer](../agents/performance-reviewer.md) | Web Vitals / frame budget within target? Payloads sane? |
| 10 | Testing | [testing-reviewer](../agents/testing-reviewer.md) | Are the critical paths tested at the right level of the pyramid? |
| 11 | Personal rules | (all agents) | Do `packs/personal/` conventions hold — states, stack, identity? |
| 12 | Release readiness | [release-reviewer](../agents/release-reviewer.md) | Migrations, rollback, monitoring, docs — can this ship and unship? |

## Profile configuration

Strictness per step comes from the profile weight table in [reasoning-profiles.md](reasoning-profiles.md):

- **Weight 3** — full checklist, findings can block.
- **Weight 2** — standard checklist, CRITICAL blocks, HIGH becomes fix-soon.
- **Weight 1** — quick pass on the agent's top-5 checks only.
- **Weight 0** — skipped; noted in the report as skipped-by-profile.

Steps 2, 3, 8 never drop below weight 1 in any profile (the safety floor plus "obvious UX").

## Running the pipeline

**Full run** (pre-release, new feature done): execute steps in order. Later steps assume earlier findings are addressed or accepted.

**Targeted run**: any single step can run alone via its agent file or `prompts/run-*.md`.

**Full frontend/UI run**: for “full frontend review” or “UI screen review,”
run [ui-screen-review](../workflows/ui-screen-review.md): UX → Accessibility →
Mobile/responsive → Copywriting → Frontend quality. This is a five-lens workflow,
not an alias for the single Frontend quality lens.

**Lightweight loop** (during development): steps 2, 5, 6 after each UI iteration; steps 3, 4 before calling a screen done; the rest at feature completion.

## Unified report format

Every agent, every step, same output:

```markdown
# Review Summary

## Context
## Strengths
## Critical Issues
## High Priority Fixes
## Medium Priority Fixes
## Low Priority Improvements
## Tradeoffs
## Relevant Knowledge Packs Used
## Coverage
- Inspected:
- Not inspected / out of scope:
- Confidence basis:
## Scores
- UX:
- Accessibility:
- Mobile:
- Architecture:
- Security:
- Performance:
- Product:
- Maintainability:
- Overall:
## Recommended Next Iteration
## Final Decision
PASS / PASS WITH FIXES / BLOCKED
```

Scoring rules: [scoring-model.md](scoring-model.md). Agents fill only the score lines they can honestly assess; others get `n/a`.

Every finding carries an inline confidence tag — `(Confidence: Certain|High|Moderate|Low)`, per [confidence-model.md](confidence-model.md) — structuring what severity-gating already required implicitly. **Coverage** states what was actually inspected, so a score never implies more certainty than the review earned; it is a reporting addition and does not change the decision semantics below — a CRITICAL blocks regardless of coverage, and low coverage is never a reason to soften a finding actually made. See [docs/scoring/evidence-confidence-coverage.md](../docs/scoring/evidence-confidence-coverage.md).

## Pre-report gate

Before a finding is written into Critical/High/Medium/Low, it clears four checks — fail one and the finding is downgraded or dropped, never reported as-is:

1. **Cited** — exact file:line, or exact screen/state, not a paraphrase of where.
2. **Concrete** — the actual failure mode (what breaks, for whom, under what input), not a restated best practice.
3. **Contextualized** — the surrounding function/component/markup was actually read, not just the matched line.
4. **Severity-defensible** — the assigned severity matches this lens's own Severity levels, not inflated for effect or softened to dodge a hard conversation.

This operationalizes [confidence-model.md](confidence-model.md) rule 2 ("verify before asserting") as a mechanical step at the moment of reporting, not just a standing principle. A finding that fails the gate isn't silently dropped without a trace when it's still worth a note — demote it to Low Priority or Tradeoffs, labeled; otherwise it doesn't survive into the report at all.

## Severity levels

- **CRITICAL** — safety floor violation or data loss risk. Always blocks, every profile.
- **HIGH** — real user harm or defect likely. Blocks at weight 3; fix-soon at weight 2.
- **MEDIUM** — maintainability or quality concern. Scheduled, not blocking.
- **LOW** — polish. Optional.

## Decision semantics

- **PASS** — no CRITICAL/HIGH open.
- **PASS WITH FIXES** — HIGH findings exist, are enumerated, and the profile permits shipping with a fix commitment.
- **BLOCKED** — CRITICAL open, or HIGH open at weight 3.

A multi-step run's final decision is the worst individual decision.
