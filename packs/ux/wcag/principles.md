# Principles — WCAG Pack (POUR, operationalized)

Success criteria cited as (SC x.x.x). Working target: WCAG 2.2 AA.

## Perceivable — information must reach the user's senses

### P-1 Text alternatives (SC 1.1.1)
Every non-text content carries a text equivalent serving the same purpose: informative images get descriptive `alt`; decorative images get empty `alt=""` (silence, not noise); icon buttons get accessible names; charts get data tables or summaries.

### P-2 Semantic structure (SC 1.3.1, 1.3.2)
Structure expressed visually must exist programmatically: real headings in order, real lists, real tables with headers, real labels bound to inputs, landmark regions. Meaning conveyed by layout alone evaporates in the accessibility tree.

### P-3 Color independence (SC 1.4.1)
Color never carries meaning alone: errors also get icons/text; links in prose also get underlines; chart series also get patterns/labels; states also get shape or text.

### P-4 Contrast floors (SC 1.4.3, 1.4.11)
Text ≥ 4.5:1 against background (≥ 3:1 for large text ≥ 24px or 19px bold); UI component boundaries and meaningful graphics ≥ 3:1. Brand palettes adapt to the floor ([Ruling R1](../../../core/conflict-resolution.md)).

### P-5 Reflow and zoom (SC 1.4.4, 1.4.10)
Text resizes to 200% and pages reflow to 320px-equivalent without loss or 2D scrolling. This is the same discipline as mobile-first ([Krug P14](../steve-krug/principles.md)) — one design effort, two constituencies.

### P-6 Text spacing & content on hover (SC 1.4.12, 1.4.13)
Layouts survive user-adjusted text spacing; hover/focus-revealed content is dismissible, hoverable, persistent.

## Operable — every function must be reachable and drivable

### O-1 Keyboard completeness (SC 2.1.1, 2.1.2)
Everything doable with a mouse is doable with a keyboard; focus never gets trapped. This single principle catches most custom-widget failures.

### O-2 Visible focus, logical order (SC 2.4.3, 2.4.7, 2.4.11)
Focus indicator always visible (never `outline: none` without replacement), focus order follows reading/task order, focused elements not hidden behind sticky chrome.

### O-3 Skip and structure navigation (SC 2.4.1)
Skip-to-content link before repeated blocks; landmarks and headings make the page navigable by structure.

### O-4 Descriptive pages, headings, links (SC 2.4.2, 2.4.4, 2.4.6)
Page titles describe the page; headings describe their sections; link text describes its destination out of context (= [Krug ER16](../steve-krug/engineering-rules.md)).

### O-5 Timing and motion under user control (SC 2.2.1, 2.2.2, 2.3.1)
Time limits extendable; auto-moving content pausable; nothing flashes more than 3×/second. Respect `prefers-reduced-motion`.

### O-6 Input modality freedom (SC 2.5.1, 2.5.2, 2.5.7, 2.5.8)
Complex gestures have single-pointer alternatives; drag operations have non-drag alternatives; touch targets ≥ 24×24 CSS px minimum (44 remains the [usability bar](../steve-krug/engineering-rules.md)); down-events don't commit actions.

### O-7 Consistent help & authentication (SC 3.2.6, 3.3.8)
Help mechanisms appear in consistent locations; authentication never requires a cognitive test (transcription, puzzles) — allow paste, password managers, passkeys.

## Understandable — content and behavior must be predictable

### U-1 Language declared (SC 3.1.1, 3.1.2)
Page language set (`lang`); inline language changes marked.

### U-2 Predictable interface (SC 3.2.1–3.2.4)
Focus or input never triggers surprising context changes (no submit-on-focus, no navigate-on-select without warning); components consistent across the product (= [NN/g H4](../nielsen-norman-group/principles.md)).

### U-3 Labels, instructions, error identification (SC 3.3.1–3.3.3)
Every input has a visible, persistent, programmatically-bound label; required formats stated up front; errors identified in text, located at the field, with correction suggested where known (= [NN/g NG32-33](../nielsen-norman-group/engineering-rules.md)).

### U-4 Error prevention on consequences (SC 3.3.4)
Legal/financial/data-changing submissions are reversible, checked, or confirmable (= [Norman NR16](../don-norman/engineering-rules.md)).

### U-5 Redundant entry (SC 3.3.7)
Never re-ask information already provided in the same process — auto-populate or offer selection (= [Tesler LX10](../laws-of-ux/engineering-rules.md)).

## Robust — content must survive the technology stack

### R-1 Valid, complete name/role/value (SC 4.1.2)
Every UI component exposes its name, role, and state to the accessibility tree: native elements first; correct ARIA patterns (per the APG) for custom widgets; state changes (expanded, selected, checked) programmatically updated.

### R-2 Status messages (SC 4.1.3)
Status updates (saves, errors, async results, loading completions) announced via live regions without stealing focus.

## Meta-principles

- **MP1 — Native first.** Use the HTML element that exists (`button`, `a`, `select`, `dialog`, `details`) before rebuilding it with ARIA.
- **MP2 — Wrong ARIA < no ARIA.** ARIA promises behavior; unkept promises actively mislead. Follow the APG patterns completely or use native.
- **MP3 — Test the tree, not the pixels.** Review with keyboard walks and accessibility-tree inspection; automated scanners are the floor-finder, not the audit.
