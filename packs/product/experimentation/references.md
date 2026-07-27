# References — Experimentation Pack

Attribution only. Nothing here is copied from the source; the pack is an original
operational distillation, organized by the AKOS file contract rather than by the book's
structure.

- **Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing** — Ron Kohavi, Diane Tang, Ya Xu. Cambridge University Press. https://experimentguide.com/

## On the arithmetic in this pack

The sample-size approximation in [decision-framework.md](decision-framework.md) —
`n ≈ 16·p·(1−p)/δ²` per arm — is the standard rule of thumb for comparing two proportions
at 5% significance and 80% power. It is an approximation, deliberately: the point is that
the requirement scales with the inverse square of the effect, so halving the effect
quadruples the sample. Anything relying on a precise number should use a proper power
calculation rather than this pack.

## Level 3, and what that means here

A book by practitioners, carrying its own context: large-scale consumer products with
traffic most teams do not have. That context is the reason this pack's first section is
about *not* running experiments — applying the methodology at a scale it was not written
for is the specific failure mode a Level 3 source invites, and
[authority-model](../../../core/authority-model.md) is explicit that methodologies encode
the setting they came from.

## Related AKOS packs

[product/lean-startup](../lean-startup/README.md) — the hypothesis loop this supplies the
statistics for · [product/inspired](../inspired/README.md) — deciding what to build ·
[product/continuous-discovery-habits](../continuous-discovery-habits/README.md) — the
qualitative half an experiment cannot supply ·
[devops/observability](../../devops/observability/README.md) — the instrumentation the
numbers come from · [ai-engineering/agent-evals](../../ai-engineering/agent-evals/README.md)
— the same discipline for non-deterministic model output ·
[security/privacy](../../security/privacy/README.md) — what the measurement data itself
obliges you to
