# Changelog — context-engineering

## [1.0.1] — 2026-07-26

### Changed

- **Promoted from `draft` to `stable`.** Assessed against the draft→stable criterion
  now recorded in [core/knowledge-schema.md](../../../core/knowledge-schema.md): no
  placeholder content in any required file, every cited rule code defined in this pack,
  every `metadata.yaml` source grounded verbatim in `references.md`, the `CEE`
  prefix owned by this pack alone, and the independent-distillation line present in
  `README.md`. The first four are verified by the existing unit suite; the last by a new
  `doctor.sh` check added alongside this promotion. `last_reviewed` re-stamped to the
  promotion date and `review_after` recomputed from the Level 2 365-day cadence.
- **Now routable automatically.** The pack's row moves from the Experimental table into
  the stable routing table in `skills/akos/SKILL.md`, so it enters the "2-5 packs closest
  to the task" selection instead of loading only when a user names it, and stable agents
  may now depend on it.

## [1.0.0] — 2026-07-20

### Added

- First complete version: all 17 schema files populated with operational content.
- Principles CE1–CE16 covering the finite-and-expensive nature of context, minimum sufficient context, progressive disclosure, just-in-time retrieval, context poisoning, context rot, the instruction hierarchy (and why retrieved content is never in it), duplicated-instruction drift, lossy summarization, the four memory tiers, stable-vs-volatile facts, shared-vs-task-specific context, dynamic routing, verified-vs-assumed claims, large-repository navigation, and position weight within a context window.
- Engineering rules CEE1–CEE58, grouped into context budgeting, progressive disclosure, just-in-time retrieval, context-poisoning containment, context-rot mitigation, instruction hierarchy, deduplication, summarization/compaction, memory-tier discipline, stable-vs-volatile handling, dynamic selection/routing, evidence and citation, and large-repository context.
- Anti-patterns derived from the pack's own principles: context poisoning, the kitchen-sink prompt, context rot / lost in the middle, the instruction that wasn't (retrieved content obeyed as a directive), the duplicated rule that drifted, lossy summarization dropping a decision, the wrong-tier memory, the stale cached fact, the full-repo dump, confident hallucination presented as verified, the static prompt that never routes, preloading "just in case," and the buried critical instruction.
- Review checklist and scoring rubric that treat context poisoning acted on as fact, and retrieved content obeyed as instruction, as correctness defects, with a hard cap at 59 for either open CRITICAL and no credit for instance-only fixes.
- Standard source cited: Anthropic's "Effective Context Engineering for AI Agents," with the pack organized around the AKOS 17-file contract rather than the source's structure.
- A self-referential worked example, in `decision-framework.md` and `examples.md`: a critique of `skills/akos/SKILL.md` step 4's own routing table as a live instance of dynamic pack selection and progressive disclosure — what it gets right (task-fit routing, a stated 2–5 pack cap, fragment-before-depth reading order, stated routing output) and what a stricter context-engineering reading would tighten (the routing table's own fixed read cost, an implicit rather than stated precedence between loaded-pack guidance and direct artifact verification).
- Cross-links recorded to `core/confidence-model.md` (verified-vs-assumed claims), `core/source-policy.md` (this pack's own distillation discipline), `core/authority-model.md` and `core/conflict-resolution.md` (the general hierarchy and conflict-resolution patterns CE7 specializes), and `skills/akos/SKILL.md` (the worked routing example).
- Scope boundary recorded against the sibling packs: `agent-foundations` (architecture selection and bounding), `tool-design` (tool shape), `agent-evals` (measurement), `agent-security` (controls) — with instruction *phrasing* named as covered by no pack in this domain rather than silently absorbed here.
