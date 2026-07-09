# Pack: Clean Architecture

**Domain:** Architecture · **Authority:** Level 3 (methodology) · **Version:** 1.0.0

Operationalizes the dependency-rule school of architecture: business logic isolated from frameworks, databases, and UI via dependency inversion, so the core is testable and the delivery mechanism is swappable. Distilled for pragmatic use — including when *not* to apply it.

Independent distillation; not affiliated with or endorsed by the source author. See [references.md](references.md).

## When to load

- Structuring a new backend/service of nontrivial complexity.
- Deciding where business logic should live vs. framework code.
- Reviewing whether domain logic has leaked into controllers/ORM models.
- Arguing against (or for) layering on a small app — this pack includes the "when NOT" case explicitly.

## Related packs

[solid](../solid/README.md) · [domain-driven-design](../domain-driven-design/README.md) · [martin-fowler-refactoring](../martin-fowler-refactoring/README.md) · [twelve-factor-app](../twelve-factor-app/README.md)
