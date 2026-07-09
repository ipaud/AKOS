# Workflow: Pre-Release Review

The full twelve-step [review pipeline](../core/review-pipeline.md) before a production release.

## The twelve steps

Run each agent in order; strictness per the active profile's [weight table](../core/reasoning-profiles.md):

1. Product clarity — [product-reviewer](../agents/product-reviewer.md)
2. UX clarity — [ux-reviewer](../agents/ux-reviewer.md)
3. Accessibility — [accessibility-reviewer](../agents/accessibility-reviewer.md)
4. Mobile/responsive — [mobile-reviewer](../agents/mobile-reviewer.md)
5. Copywriting — [copy-reviewer](../agents/copy-reviewer.md)
6. Frontend quality — [frontend-reviewer](../agents/frontend-reviewer.md)
7. Architecture — [architecture-reviewer](../agents/architecture-reviewer.md)
8. Security — [security-reviewer](../agents/security-reviewer.md)
9. Performance — [performance-reviewer](../agents/performance-reviewer.md)
10. Testing — [testing-reviewer](../agents/testing-reviewer.md)
11. Personal rules — all agents apply [pau-avila layer](../packs/personal/pau-avila/README.md)
12. Release readiness — [release-reviewer](../agents/release-reviewer.md)

## Merge

One aggregate Review Summary. Final decision = the worst individual step's decision. Any open CRITICAL → BLOCKED.

## Profile adjustments

- **Prototype:** steps at weight 0 skipped (noted as skipped-by-profile); floor steps (2, 3, 8) never below weight 1.
- **Production:** all steps at full weight; CRITICAL and HIGH block.
- **Enterprise:** adds compliance/observability/documentation depth.

## Exit criteria

Aggregate summary; BLOCKED if any CRITICAL open or any HIGH open at weight 3. For this owner: security + Supabase/RLS review is mandatory before "done" on any deployed project.
