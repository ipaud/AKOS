# Mental Models — QA Checklists Pack

- **The four states as a mandatory sweep:** empty/loading/error/success ([Krug ER25](../../ux/steve-krug/engineering-rules.md)) — every async surface gets checked against all four, not just the happy path.
- **Edge cases as a checklist, not inspiration:** zero items, one item, many items, maximum-length input, special characters, slow network, offline, concurrent edits — a fixed list applied systematically beats ad hoc "let me think of edge cases."
- **The device/browser matrix as risk-weighted, not exhaustive:** test the combinations real users actually use (per analytics), not every theoretical combination.
- **Exploratory testing as structured improvisation:** time-boxed sessions with a charter ("explore the checkout flow for data-loss risks") rather than unstructured poking, so findings are reproducible and reportable.
