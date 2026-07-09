# Pack: Twelve-Factor App

**Domain:** Architecture/Deployment · **Authority:** Level 2 (widely-adopted industry methodology, originating from Heroku engineering practice) · **Version:** 1.0.0

Operationalizes the twelve-factor methodology for building deployable, scalable, portable services: config via environment, stateless processes, explicit dependency declaration, disposability, dev/prod parity, and more.

Independent distillation; not affiliated with or endorsed by the source organization. See [references.md](references.md).

## When to load

- Structuring any backend service intended for real deployment (not a one-off script).
- Reviewing config/secrets handling, process design, and deployment scripts.
- Diagnosing "works on my machine" / environment-drift problems.
- Container/cloud-native service design.

## Related packs

[clean-architecture](../clean-architecture/README.md) · [devops/ci-cd](../../devops/ci-cd/README.md) · [devops/deployment](../../devops/deployment/README.md) · [security/nist-ssdf](../../security/nist-ssdf/README.md)
