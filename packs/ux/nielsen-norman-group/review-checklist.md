# Review Checklist — NN/g Pack

Run one heuristic at a time. NG-rule references: [engineering-rules.md](engineering-rules.md).

## Critical

- [ ] No roach motels: every enrollable thing is exitable; every flow has an exit. (H3, NG9, NG11)
- [ ] Actionable errors cannot be missed (persist until handled) and never destroy input. (H9, NG31)
- [ ] High-cost commitments restate their object and consequences before commit. (H5/H6, NG19, NG20)

## High

- [ ] All async operations show status; background work has a revisitable surface. (H1, NG1–NG4)
- [ ] Modals close via X/Escape; multi-step flows have state-preserving Back. (H3, NG8, NG9)
- [ ] One component set; identical actions labeled and placed identically. (H4, NG12, NG13)
- [ ] Known-value inputs are constrained controls, not free text. (H5, NG16)
- [ ] Double-submit mechanically prevented. (H5, NG18)
- [ ] Error copy: what + why + next step; field errors adjacent + focused. (H9, NG32, NG33)
- [ ] Keyboard path exists through all primary flows. (H7, NG24)
- [ ] No jargon/schema vocabulary in user-facing text. (H2, NG5)

## Medium

- [ ] Locale-correct dates/numbers/currency; workflow-logical option ordering. (H2, NG6, NG7)
- [ ] Undo for content mutations; cancel for long operations. (H3, NG10)
- [ ] Platform controls and shortcuts standard. (H4, NG14)
- [ ] Safe, most-likely defaults; Enter never destroys. (H5, NG17)
- [ ] Prior choices visible in multi-step flows; icon-only limited to universal icons. (H6, NG21, NG22)
- [ ] Bulk operations for repeatable actions; recents/templates for frequent inputs. (H7, NG25, NG26)
- [ ] Task screens free of org-serving content; advanced options progressively disclosed. (H8, NG28, NG29)
- [ ] Empty states teach; help reachable at points of confusion. (H10, NG35, NG36)

## Low

- [ ] Deep links reflect app state. (H7, NG27)
- [ ] Data displays default to decision-relevant subset. (H8, NG30)
- [ ] 404/500 pages offer home/back/search/support. (H9, NG34)
- [ ] Docs task-titled and linked from relevant UI. (H10, NG37)
- [ ] Relative times carry absolute tooltips. (H2, NG6)

## Process

- [ ] Every finding tagged with its heuristic (H1–H10).
- [ ] Every finding severity-rated via frequency × impact × persistence.
- [ ] Pass run heuristic-by-heuristic, not blended.
