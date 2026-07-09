# Principles — Universal Principles Pack

Selected for software relevance; overlaps with other packs cross-referenced rather than duplicated.

## Perception & grouping (Gestalt)

- **UP1 — Proximity:** things near each other read as related. Spacing *is* information architecture ([RP8](../refactoring-ui/principles.md), [ER13](../steve-krug/engineering-rules.md)).
- **UP2 — Similarity:** things that look alike read as the same kind. Consistent component styling = free categorization; violating it (two styles, one meaning) = false categories.
- **UP3 — Common region:** enclosure (cards, backgrounds) groups powerfully — and expensively ([separation ladder](../refactoring-ui/principles.md): use after proximity).
- **UP4 — Continuity & alignment:** elements on a line read as a sequence; fewer alignment edges = calmer, clearer structure.
- **UP5 — Closure:** users complete partial patterns — truncation with ellipsis, cropped cards signaling scrollability ("peek" affordances) exploit this legitimately.
- **UP6 — Figure-ground:** the eye separates subject from backdrop; ambiguous layering (modals without scrims, floating text) taxes it ([depth as information](../apple-hig/philosophy.md)).

## Effort & information

- **UP7 — 80/20 rule:** most value flows through a minority of features. Optimize, surface, and polish the vital few; progressive-disclose the rest ([NG29](../nielsen-norman-group/engineering-rules.md)). Audit: usage analytics vs surface area given.
- **UP8 — Progressive disclosure:** reveal complexity as needed. The single most reusable complexity-management tool ([resolves H7/H8](../nielsen-norman-group/decision-framework.md)).
- **UP9 — Chunking:** grouped units beat raw streams ([Miller](../laws-of-ux/principles.md)); applies to content architecture, not just strings — onboarding in 3 named phases beats 12 flat steps.
- **UP10 — Performance load:** the physical + cognitive effort to reach a goal; every reduction (defaults, automation, fewer decisions) raises completion ([Tesler](../laws-of-ux/principles.md), the generalization).
- **UP11 — Signal-to-noise:** maximize information per element; decoration that carries no signal is noise ([H8](../nielsen-norman-group/principles.md), [RP philosophy](../refactoring-ui/philosophy.md)).

## Action & error

- **UP12 — Confirmation:** high-cost actions get a deliberate second step ([forcing-function table](../don-norman/decision-framework.md) refines this).
- **UP13 — Forgiveness:** good design assumes error and makes it cheap — undo, drafts, trash-with-retention, edit-after-send windows. Forgiving systems breed confident users; punishing systems breed timid ones.
- **UP14 — Constraint:** limiting possible actions prevents errors better than warning about them ([Norman P6](../don-norman/principles.md)).
- **UP15 — Feedback loops:** systems that show consequences of actions teach their own use; invisible consequences guarantee misuse.

## System-level

- **UP16 — Flexibility-usability tradeoff:** the more things a design accommodates, the worse it does each. Swiss-army products lose to focused tools per-task. Product implication: resist generalizing a flow to cover every stakeholder's case ([feature-factory kin](../../product/escaping-the-build-trap/README.md)).
- **UP17 — Hierarchy:** organization by importance/containment is the primary comprehension tool at every scale — page, flow, IA, docs ([P6](../steve-krug/principles.md) generalized).
- **UP18 — Consistency:** internal, external, functional — the fourth kind, *aesthetic* consistency, is what makes brands ([H4](../nielsen-norman-group/principles.md) + identity layer).
- **UP19 — Affordance/mapping/visibility** — carried by the [Norman pack](../don-norman/principles.md); listed here for completeness of the canon.
- **UP20 — Aesthetic-usability, Von Restorff, serial position, goal gradient** — carried by [laws-of-ux](../laws-of-ux/principles.md).
- **UP21 — Iteration:** design quality is a function of iteration count, not initial brilliance. Processes that cheapen iterations (prototypes, small tests, tokens) outproduce processes that perfect first drafts ([HCD cycle](../don-norman/philosophy.md), [Krug testing habit](../steve-krug/principles.md)).
