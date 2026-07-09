# Decision Framework — NN/g Pack

## Which evaluation method, when?

| Situation | Method |
|-----------|--------|
| Design exists (mockup → production), budget ≈ zero | Heuristic pass (this pack), one heuristic at a time |
| Team disagrees about a specific flow | Think-aloud test, 3–5 users ([Krug planner fragment](../steve-krug/prompt-fragments.md)) |
| Nothing built yet | Heuristic-evaluate competitors; test their products |
| Post-launch, live traffic | Analytics for *where* (drop-offs, pogo-sticking), then testing for *why* |
| Redesign decision pending | Test the current version first — redesigns must beat a measured baseline, not a remembered one |

Heuristics find the known problem classes cheaply; users find the surprises. Never let either substitute for the other.

## Prioritizing findings

Severity (frequency × impact × persistence) ranks findings; then apply fix-cost:

1. High severity + low cost → fix now, this release.
2. High severity + high cost → schedule; interim mitigation now (copy change, default change).
3. Low severity + low cost → batch into polish passes.
4. Low severity + high cost → backlog honestly (most die there; that's correct).

Findings without severity ratings don't enter prioritization — rate or drop.

## Resolving inter-heuristic conflicts

- **Power vs simplicity (H7/H8):** progressive disclosure; default to the novice surface.
- **Status vs noise (H1/H8):** show status users act on; suppress status that's merely true.
- **Consistency vs local improvement (H4):** consistency wins locally; improvements migrate globally or not at all.
- **Prevention vs freedom (H5/H3):** constrain inputs, not goals — prevent malformed data, never trap users in flows.
- **Real-world match vs precision (H2):** user vocabulary in UI; precise terminology available in docs/tooltips for experts.

## When a heuristic itself shouldn't win

Heuristics measure usability. They yield when:

- **Accessibility hard requirements** conflict (rare; usually complementary) — WCAG is Level 1, this pack is Level 2.
- **Platform guidelines** prescribe a specific pattern on their platform ([R3](../../../core/conflict-resolution.md)).
- **Deliberate friction** is the product (confirmation of legal consent, game difficulty) — friction serving the *user's* interest is not a violation; friction serving only the org still is.
