# Prompt Fragments — HTML Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply semantic HTML practice (AKOS L1):
- Element-first ladder: native element → native element + ARIA
  attribute → full custom ARIA widget. Descend only as far as needed.
- Interactive elements are `<button>` (action) or `<a href>` (navigation).
  Never a click-handler `div`/`span`; never an `<a>` without `href`.
- Exactly one `<h1>` per page; heading levels sequential with no skips.
  Never choose a level for its font size — style it instead.
- Landmarks structure every page: `header`, `nav`, `main` (exactly one),
  `aside`, `footer`.
- Every `input`/`select`/`textarea` has a bound `<label>` (`for`/`id` or
  wrapping). A placeholder is never the label.
- Input `type` matches the data collected — `email`, `tel`, `url`,
  `number`, `date` — for the right mobile keyboard and native validation.
- Every `<img>` has an `alt` attribute: descriptive when it carries
  meaning, `alt=""` when decorative. Never absent.
- `<html lang>` set to the actual content language.
- `<table>` only for tabular data, with `<th scope="col|row">`; layout
  is Grid/Flexbox work.
- Link text names its destination; no bare "click here" or "read more".
- Structure lives in markup, not CSS: the page must still convey its
  meaning and reading order with stylesheets disabled.
```

## Fragment: review lens

```text
Review this markup as a semantic HTML reviewer:
1. Outline test — extract headings only. Does the structure read
   correctly unstyled? One h1, no skipped levels?
2. Interactive audit — every element carrying a click or key handler:
   is it natively focusable and activatable by Enter/Space?
3. Form contract — per control: bound visible label, correct `type`,
   `name`, required state in markup, error text tied via
   `aria-describedby`.
4. Landmark map — header/nav/main/aside/footer present, exactly one
   `main`, multiple navs distinguishable by accessible name?
5. Image pass — every `img` has `alt`; decorative images are `alt=""`;
   informative alt describes purpose, not appearance.
6. Table pass — tabular data only, headers marked with `th` and scoped.
7. Link text — does each link name its destination out of context?
8. Custom widgets — where a native element was skipped, is the full
   ARIA APG pattern implemented (role, states, keyboard), or half-done?
Report by severity per review-checklist.md. Give the replacement element
or attribute, not a description of the problem.
```

## Fragment: div-to-semantic conversion

```text
Convert this div-based markup to semantic HTML:
- Replace each generic wrapper with the element naming its role:
  header, nav, main, section, article, aside, footer, figure/figcaption.
- Replace click-handler divs with `button` (action) or `a href`
  (navigation); delete the `tabindex`, `role`, and keydown shims the
  native element makes redundant.
- Replace hand-rolled disclosure and modal patterns with
  `details`/`summary` and `dialog` where the behavior matches.
- Keep class names and styling hooks intact; report every place the
  native element's defaults change the rendered result.
```

## Fragment: form markup contract

```text
Build or audit this form against the pack's form contract:
- Every control: visible bound `<label>`, correct `type`, `name`, and an
  `autocomplete` token where the field is known personal data.
- Required fields carry `required` in markup, not styling alone.
- Errors: text tied to its control via `aria-describedby`, stating what
  is wrong and what to enter instead.
- Related controls grouped in `<fieldset>` with a `<legend>`.
- Submission is a real `<button type="submit">` inside the `<form>`, so
  Enter-to-submit and native validation work.
```

## One-liner (for tight token budgets)

```text
HTML rules: native element before div+ARIA; buttons and links, never
click-handler divs; one h1, sequential headings; landmarks on every page;
bound labels and correct input types on every control; alt on every
image; lang set; tables only for data; descriptive link text.
```
