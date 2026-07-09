# Review Checklist — web.dev Practice Pack

## High

- [ ] Routes/major features code-split; initial bundle contains only first-view needs. (WE1)
- [ ] Images sized via srcset to actual rendered dimensions, modern formats used. (WE3)
- [ ] Static assets cached long-lived with content-hashed filenames. (WE5)
- [ ] Third-party scripts async/defer, not blocking main content. (WE8)

## Medium

- [ ] Below-the-fold images lazy-loaded; above-the-fold not. (WE2)
- [ ] Font families/weights limited to actually-used set. (WE4)
- [ ] Loading states use skeletons matching eventual layout for loads >500ms. (WE6)
- [ ] Dependencies reviewed for bundle-size impact before merge. (WE7)
- [ ] Bundle-size budget enforced in CI. (WE9)

## Low

- [ ] Hover/viewport-based prefetch used for high-confidence next navigations. (WE10)
