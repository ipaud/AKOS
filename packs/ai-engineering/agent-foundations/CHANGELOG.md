# Changelog — agent-foundations

## [1.0.1] — 2026-07-26

### Changed

- **Promoted from `draft` to `stable`.** Assessed against the draft→stable criterion
  now recorded in [core/knowledge-schema.md](../../../core/knowledge-schema.md): no
  placeholder content in any required file, every cited rule code defined in this pack,
  every `metadata.yaml` source grounded verbatim in `references.md`, the `AFE`
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
- Principles AF1–AF18, each with an operational corollary, covering the agent as the last shape to reach for, the predictability-for-adaptability trade, encoding a knowable path, the agency spectrum, multiplicative complexity in multi-agent topologies, routing as classification, parallelism buying latency or confidence but never correctness, dynamic decomposition only for non-enumerable subtasks, critique loops needing external criteria, a plan's declared status, defining "done" before the loop, limits as separate from success conditions, exhaustion as a reported result, the three error classes, escalation conditions as design-time artifacts, idempotency under at-least-once execution, budget as an input to shape selection, and observability as the precondition for every other rule.
- Engineering rules AFE1–AFE72, grouped into shape selection, routing, parallelization, orchestrator-worker, evaluator-optimizer, planning and replanning, termination conditions, limits and budgets, error recovery, escalation, idempotency and side effects, and observability.
- The shape spectrum as a decision table — single call → prompt chain → routing → parallelization → fixed workflow → orchestrator-worker → evaluator-optimizer → agent → multi-agent — ordered by who chooses the path, with a stated "why not the next one down" for every row (`mental-models.md`, `decision-framework.md`).
- The path-knowability test (enumerate the step sequences across twenty real inputs; few and stable → workflow with a router, patternless → the agent is earned) as the operational form of the pack's core claim.
- The three-outcome return contract — success / error / exhausted — with exhaustion carrying which limit fired, what completed, and what did not, so a caller can distinguish truncated work from finished work without inspecting its content.
- The retry / replan / escalate classification table, keyed to transient, approach-level, and terminal failures, with the cost of each misclassification stated.
- Anti-patterns derived from the pack's own principles: the silent truncation, the double-charged retry, the agent that should have been a function, the unbounded loop, the deterministic retry spiral, the vanity fan-out, the dependent parallel, the self-approving loop, the eternal refinement, the plan that was never revisited, the replan thrash, the multi-agent org chart, the orchestrator that already knew, the swallowed step, the escalation that never fires, the escalation that always fires, budget as an afterthought, and the untraceable run.
- Review checklist and scoring rubric that treat truncated work returned as complete, a side effect applicable more than once, and an action taken outside a stated authority boundary as correctness defects, with a hard cap at 59 for any open CRITICAL, a cap at 69 for a loop lacking both a success condition and a hard limit, a cap at 79 for an unwarranted agent or multi-agent shape, and no credit for instance-only fixes.
- Sources cited: Anthropic's "Building Effective Agents" and OpenAI's "A Practical Guide to Building Agents" (Level 2, published engineering practice), plus ReAct (Yao et al.) and Reflexion (Shinn et al.) as Level 3 methodology papers applied as decision frameworks. The pack is organized around the AKOS 17-file contract rather than any source's structure.
- A shape-selection worksheet, a loop-boundedness audit, and a failure-and-recovery trace as injectable prompt fragments, alongside the standard build-mode constraint block, review lens, and tight-budget one-liner.
- Scope boundary recorded against `packs/ai-engineering/context-engineering` (what the agent sees, as distinct from what shape it is and how it is bounded), and against a future sibling covering repository-editing discipline, which is deliberately out of scope here.
- Cross-links recorded to `core/authority-model.md` and `core/decision-framework.md` (the general patterns this pack specializes), `core/source-policy.md` (its own distillation discipline), `core/scoring-model.md` (scoring bands), and to the `architecture/design-patterns`, `devops/sre`, and `testing/testing-pyramid` packs — SRE in particular as the older, operational home of the retry, backoff, budget, timeout, and idempotency concerns this pack restates in agent-shaped form.
