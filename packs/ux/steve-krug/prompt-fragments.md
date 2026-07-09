# Prompt Fragments — Krug Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply web-usability constraints (Krug school, AKOS L2):
- Self-evident first: no element may require figuring out. If a label needs
  explanation, change the label or the design, not add a tooltip.
- Design for scanning: semantic heading hierarchy, front-loaded headings,
  one visually dominant primary action per screen.
- Follow conventions: logo top-left → home, standard icons, buttons look
  like buttons, links look like links, nothing clickable-looking that isn't.
- Copy: verb-first specific button labels; no "click here"; no happy talk;
  cut every word that doesn't help the user act.
- Forms: visible labels (never placeholder-only), accept any reasonable
  input format, preserve input on errors, minimal fields, smart defaults.
- States: implement empty / loading / error / success for every async surface.
  Error messages: what happened → why → what to do next.
- Mobile: works at 320px, tap targets ≥44px, no hover-only affordances,
  primary actions thumb-reachable.
```

## Fragment: review-mode lens

```text
Review this UI as a Krug-school usability reviewer. For each screen:
1. Five-second test — can a newcomer say what it's for?
2. No-think walk — list every point a first-time user would hesitate
   ("is that clickable?", "which of these?", "did it work?", "where am I?").
3. Trunk test on interior pages (page name, nav location, way home).
4. Squint test — does visual prominence match importance?
5. Copy pass — flag happy talk, instructions, vague labels, "click here".
6. Run the pack checklist (review-checklist.md); report findings by severity
   with the concrete smallest fix ("do the least you can do").
Never say "improve the UX" — name the element, the confusion, and the fix.
```

## Fragment: copy-cutting pass

```text
Perform a Krug copy reduction on the following UI text:
- Delete happy talk and self-description.
- Delete instructions; if the design needs them, flag the design instead.
- Halve the word count, then halve again where meaning survives.
- Make every button label verb-first and specific; every link text
  destination-bearing; every heading front-loaded.
Output: table of original → revised → rationale (one clause).
```

## Fragment: usability-test planner

```text
Plan a lightweight think-aloud usability test (Krug style):
- 3 participants, ~1h total, loose recruiting (domain expertise not required
  unless the product is expert-only).
- Tasks: the 2-3 things the product must let anyone do, phrased as goals
  ("you want to stop paying for tools you don't use"), never as click paths.
- Facilitator rules: ask them to think aloud, answer questions with
  questions, never help, never explain.
- Output: the 3 worst observed problems, each with the smallest fix.
```

## One-liner (for tight token budgets)

```text
Krug rules: self-evident UI; users scan and satisfice — obvious beats clever;
follow conventions; one dominant action/screen; visible labels; forgiving
inputs; verb-first buttons; no happy talk; four async states; 320px + thumbs
+ no hover-only; test with 3 users and fix the worst thing.
```
