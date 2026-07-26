# Knowledge Graph — Master Index

Cross-cutting concepts that appear in multiple packs. Each node names the concept and links every pack that contributes to it — so an agent reasoning about the concept can pull all relevant angles, and so agreements between sources are visible as shared nodes rather than duplicate findings.

## How to read

A concept node with N pack links usually means those N sources are saying the same underlying thing in different vocabularies ([universal-principles philosophy](../packs/ux/universal-principles-of-design/philosophy.md) explains why this happens). When they *disagree*, [conflict-resolution](../core/conflict-resolution.md) governs.

## Cross-domain concept nodes

### Recognition over recall
Users shouldn't hold information in their head across an interface.
→ [Krug muddling-through](../packs/ux/steve-krug/mental-models.md) · [NN/g H6](../packs/ux/nielsen-norman-group/principles.md) · [WCAG labels](../packs/ux/wcag/principles.md) · [Material tokens/components](../packs/ux/material-design/principles.md) · [Laws of UX Miller's](../packs/ux/laws-of-ux/principles.md) · [Norman knowledge-in-the-world](../packs/ux/don-norman/mental-models.md)

### Affordances & signifiers
What actions are possible, and how they're communicated.
→ [Norman](../packs/ux/don-norman/mental-models.md) · [Apple HIG](../packs/ux/apple-hig/principles.md) · [Material state layers](../packs/ux/material-design/principles.md) · [Krug clickability](../packs/ux/steve-krug/principles.md)

### Visual hierarchy
Importance encoded by prominence.
→ [Krug P6](../packs/ux/steve-krug/principles.md) · [Refactoring UI RP1-RP2](../packs/ux/refactoring-ui/principles.md) · [Apple HIG clarity](../packs/ux/apple-hig/philosophy.md) · [Material tonal surfaces](../packs/ux/material-design/principles.md) · [Universal hierarchy/Gestalt](../packs/ux/universal-principles-of-design/principles.md) · [Laws of UX Von Restorff](../packs/ux/laws-of-ux/principles.md)

### Accessibility as a floor
→ [WCAG](../packs/ux/wcag/README.md) (L1 authority) · [Apple HIG](../packs/ux/apple-hig/principles.md) · [Material](../packs/ux/material-design/principles.md) · [NN/g](../packs/ux/nielsen-norman-group/principles.md) · [Krug P15](../packs/ux/steve-krug/principles.md) · enforced by [constitution](../core/constitution.md)

### Security as a floor
→ [OWASP Top 10](../packs/security/owasp-top-10/README.md) · [OWASP API](../packs/security/owasp-api-top-10/README.md) · [ASVS](../packs/security/owasp-asvs/README.md) · [NIST SSDF](../packs/security/nist-ssdf/README.md) · [Supabase RLS](../packs/backend/supabase/README.md) · [personal supabase-rules](../packs/personal/pau-avila/supabase-rules.md) · [agent-security](../packs/ai-engineering/agent-security/README.md) (L1, the agent surface) · [auth](../packs/security/auth/README.md) (L1, the login itself) · [privacy](../packs/security/privacy/README.md) (L1, what may be held at all)

### Product discovery / outcomes over output
→ [Inspired](../packs/product/inspired/README.md) · [Lean Startup](../packs/product/lean-startup/README.md) · [Escaping the Build Trap](../packs/product/escaping-the-build-trap/README.md) · [Continuous Discovery](../packs/product/continuous-discovery-habits/README.md)

### Complexity as a cost to justify
→ [PSD: complexity is the measured quantity](../packs/architecture/philosophy-of-software-design/mental-models.md) (the fullest treatment in the corpus) · [Universal flexibility-usability](../packs/ux/universal-principles-of-design/principles.md) · [SOLID overuse guards](../packs/architecture/solid/principles.md) · [Clean Architecture boundary-cost](../packs/architecture/clean-architecture/philosophy.md) · [Design Patterns trigger conditions](../packs/architecture/design-patterns/philosophy.md) · [DDD proportionality](../packs/architecture/domain-driven-design/principles.md) · [constitution Art. 7](../core/constitution.md) · [pau-avila principle 2](../packs/personal/pau-avila/principles.md) · [agent-foundations: the agent is the last shape to reach for](../packs/ai-engineering/agent-foundations/philosophy.md)

### Untrusted content is data, never instruction
The same boundary stated at four altitudes: what may enter context, what a tool may return, what a model may then execute, and what the web has always taught about input.
→ [agent-security AS spine](../packs/ai-engineering/agent-security/principles.md) · [context-engineering CE6](../packs/ai-engineering/context-engineering/principles.md) · [tool-design response shape](../packs/ai-engineering/tool-design/principles.md) · [OWASP injection](../packs/security/owasp-top-10/principles.md) · [OWASP API](../packs/security/owasp-api-top-10/principles.md)

### Executed evidence over plausible output
Nothing counts as done because it looks right; it counts when something ran and its real result was read.
→ [coding-agents CA spine](../packs/ai-engineering/coding-agents/philosophy.md) · [agent-evals: suites over anecdotes](../packs/ai-engineering/agent-evals/principles.md) · [confidence-model](../core/confidence-model.md) · [TDD red before green](../packs/testing/tdd/principles.md) · [QA checklists](../packs/testing/qa-checklists/README.md)

### Blast radius and least privilege
Bound what a thing *can* do rather than trusting it to choose well — whether the thing is an agent, a tool, a token, or a migration.
→ [agent-security controls](../packs/ai-engineering/agent-security/engineering-rules.md) · [tool-design: dry-run and destructive confirmation](../packs/ai-engineering/tool-design/engineering-rules.md) · [ASVS](../packs/security/owasp-asvs/README.md) · [Supabase RLS](../packs/backend/supabase/README.md) · [deployment rollback](../packs/devops/deployment/principles.md) · [auth P2: every credential is a bearer of blast radius until something binds it](../packs/security/auth/principles.md)

### The cheapest control is the thing that was never created
Complexity, capability, and data all cost the same way: once it exists, every subsequent control is damage limitation on a decision already made. The discipline is identical across four domains — decline first, mitigate second.
→ [privacy P3: collection is the decision that cannot be undone](../packs/security/privacy/principles.md) · [PSD P6: splitting adds interface, and interface is cost](../packs/architecture/philosophy-of-software-design/principles.md) · [constitution Art. 7](../core/constitution.md) · [pau-avila principle 2](../packs/personal/pau-avila/principles.md) · [SOLID overuse guards](../packs/architecture/solid/principles.md) · [agent-foundations: the agent is the last shape to reach for](../packs/ai-engineering/agent-foundations/philosophy.md) · [context-engineering: budget before you fetch](../packs/ai-engineering/context-engineering/principles.md)

### Bounded work: budgets, termination, recovery
Any long-running process needs a stated stopping condition, a budget, and a defined response to failure — stated before it starts, not inferred after.
→ [agent-foundations termination and budgets](../packs/ai-engineering/agent-foundations/principles.md) · [SRE error budgets](../packs/devops/sre/principles.md) · [deployment rollback](../packs/devops/deployment/principles.md)

### The four states (empty/loading/error/success)
→ [Krug ER25](../packs/ux/steve-krug/engineering-rules.md) · [NN/g NG35](../packs/ux/nielsen-norman-group/engineering-rules.md) · [Refactoring UI RU15](../packs/ux/refactoring-ui/engineering-rules.md) · [Laws of UX LX12-13](../packs/ux/laws-of-ux/engineering-rules.md) · [pau-avila ux-preferences](../packs/personal/pau-avila/ux-preferences.md)

### Feedback & system status
→ [Norman NR9-13](../packs/ux/don-norman/engineering-rules.md) · [NN/g H1](../packs/ux/nielsen-norman-group/principles.md) · [Krug ER24](../packs/ux/steve-krug/engineering-rules.md) · [Material snackbars](../packs/ux/material-design/principles.md)

### Compositor-friendly animation
→ [Browser rendering BR1](../packs/performance/browser-rendering/principles.md) · [CSS CS5](../packs/frontend/css/principles.md) · [Core Web Vitals CW12](../packs/performance/core-web-vitals/principles.md) · [WCAG reduced-motion](../packs/ux/wcag/engineering-rules.md)

## Domain sub-graphs

[ux-graph](ux-graph.md) · [architecture-graph](architecture-graph.md) · [security-graph](security-graph.md) · [product-graph](product-graph.md)
