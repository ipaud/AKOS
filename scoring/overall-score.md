# Overall Score (0–100)

The weighted composite. Weights come from the active [reasoning profile](../core/reasoning-profiles.md); two hard rules override arithmetic ([core/scoring-model.md](../core/scoring-model.md)):

- Any dimension in the Blocked band (<60) caps Overall at 59.
- Security or Accessibility in the Risky band (60–69) caps Overall at 69.

## Default weights by profile

Relative weights applied to the assessed dimensions (unassessed dimensions get `n/a` and drop out of the average):

| Dimension | Prototype | MVP | Production | Enterprise | Game Dev | Internal |
|-----------|-----------|-----|------------|------------|----------|----------|
| UX | 3 | 3 | 3 | 2 | 2 | 2 |
| Accessibility | 1 | 2 | 3 | 3 | 2 | 2 |
| Architecture | 0 | 1 | 3 | 3 | 1 | 1 |
| Security | 1 | 2 | 3 | 3 | 1 | 2 |
| Performance | 0 | 1 | 3 | 2 | 3 | 1 |
| Product | 1 | 3 | 2 | 2 | 2 | 1 |
| Maintainability | 1 | 2 | 3 | 3 | 2 | 2 |

Weight 0 = the dimension is typically `n/a` for that profile (not scored), not scored-as-zero.

## Computation

`Overall = Σ(dimension_score × weight) / Σ(weight)` over assessed dimensions, then apply the two hard caps above.

## Bands

90–100 excellent · 80–89 good · 70–79 acceptable · 60–69 risky · <60 blocked.

## Verdict linkage

- All assessed ≥ 80 and no HIGH open → **PASS**
- HIGHs open, nothing Blocked, profile permits → **PASS WITH FIXES**
- Any Blocked-band dimension or open CRITICAL → **BLOCKED**

When re-reviewing, include the previous Overall in parentheses to show the trend — consistency matters more than absolute generosity.
