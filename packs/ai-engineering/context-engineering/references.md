# References — Context Engineering Pack

Attribution only. Nothing in this pack is copied from the source below; the pack is an original operational distillation, reorganized into the AKOS 17-file contract. Read the original — it carries the reasoning and the worked examples this pack compresses away.

## Primary source (Level 2)

- **Effective Context Engineering for AI Agents** — Anthropic. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

## Related AKOS core documents

This pack composes with, rather than restates, the following:

- [core/confidence-model.md](../../../core/confidence-model.md) — the confidence levels behind CE14/CEE53's verified-vs-assumed distinction.
- [core/source-policy.md](../../../core/source-policy.md) — distillation rules this pack itself follows, and the standard every AKOS pack's context is held to.
- [core/authority-model.md](../../../core/authority-model.md) — the general authority-level hierarchy that CE7's instruction hierarchy specializes for a single agent's context.
- [core/conflict-resolution.md](../../../core/conflict-resolution.md) — the general pattern behind resolving conflicting instruction layers (CE7, decision-framework.md).
- [skills/akos/SKILL.md](../../../skills/akos/SKILL.md) — a live, in-repo worked example of dynamic pack routing and progressive disclosure, critiqued directly in [decision-framework.md](decision-framework.md) and [examples.md](examples.md).

## Related AKOS packs

- [agent-foundations](../agent-foundations/README.md) — which architecture a task warrants and how it is bounded: shape selection, termination, budgets, escalation, as distinct from this pack's focus on context assembly.
- [tool-design](../tool-design/README.md) — the shape of the tools an agent calls; this pack's size-capping and pagination rules (an unbounded tool result is a context failure) meet that pack's response-shape rules there.
- [agent-evals](../agent-evals/README.md) — measuring whether an agent's behavior actually improved, including whether a context change helped or hurt.
- [agent-security](../agent-security/README.md) — the controls behind CE6's rule that retrieved content is data and never instruction; that pack carries the injection and exfiltration attack classes this one only bounds.
- [personal/pau-avila](../../personal/pau-avila/README.md) — the Level 0 layer this pack's "shared vs. task-specific context" principle (CE12) treats as the always-loaded case.
- [nielsen-norman-group](../../ux/nielsen-norman-group/README.md) — systematic heuristic evaluation; the same discipline of "does this actually serve the user in front of you" applied to an interface rather than to a model's context.
- [clean-architecture](../../architecture/clean-architecture/README.md) — dependency direction and layering in code; the closest architectural analogue to this pack's instruction-hierarchy and layering concerns, applied to context instead of to modules.
