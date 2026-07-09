# Prompt Fragments — Laws of UX Pack

## Fragment: build-mode constraint block

```text
Apply cognitive-law constraints (Laws of UX, AKOS L2):
- Hick: ≤5 undifferentiated options per decision point; group, default,
  or progressively disclose beyond that; recommend one option.
- Fitts: frequent actions = large + near (thumb zone on mobile); 44px/8px
  touch minimums; destructive actions never largest/nearest/default.
- Jakob: platform convention for all standard objects; novelty only on
  the product's differentiator.
- Miller: never require recall across screens; restate context; chunk
  displayed identifiers.
- Tesler: infer what the system can know (locale, timezone, card type),
  with visible override; every user-facing field/instruction must justify
  why the system couldn't absorb it.
- Goal-Gradient: honest progress on flows ≥3 steps; named sub-goals ≥6.
- Peak-End: design the completion state of every journey (result +
  location + next step); design waiting and error moments deliberately.
- Von Restorff: one isolated primary element per screen; accent budget
  ≤10% of elements; distinctiveness never color-only.
- Serial Position: first and last nav slots carry the priorities.
```

## Fragment: flow cost audit

```text
Audit this flow step by step, tallying four user costs per step:
decision cost (options count/ambiguity — Hick), motor cost (target
size/distance — Fitts), memory cost (context carried in the head —
Miller), learning cost (convention deviations — Jakob). Then identify
complexity that could move into the system (Tesler): inferable inputs,
absorbing defaults, format normalization. Output a table: step × costs ×
proposed reduction, plus the flow's peak and ending assessment (Peak-End)
and progress visibility (Goal-Gradient).
```

## Fragment: law-citation reviewer guard

```text
When citing a psychological law in a finding, verify its boundary
conditions first: Miller's is about working memory, not menu length
(use Hick for choice sets); Hick's weakens for practiced experts; Peak-End
doesn't excuse broken middles; Aesthetic-Usability means praise is
contaminated evidence, not that polish replaces usability. Reject or
reclassify findings that cite a law outside its mechanism.
```

## One-liner

```text
Laws: cut/group/default choices (Hick); big-near frequent targets, never
destructive (Fitts); convention everywhere but the differentiator (Jakob);
no cross-screen recall, chunk ids (Miller); system absorbs complexity with
override (Tesler); design peaks/endings/waits (Peak-End); firsts+lasts carry
priority (Serial Position); one accent per screen (Von Restorff); measure
behavior not praise (Aesthetic-Usability); honest visible progress
(Goal-Gradient).
```
