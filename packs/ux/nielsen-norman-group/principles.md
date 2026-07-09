# Principles — NN/g Pack: The Ten Heuristics, Operationalized

Each heuristic: what it demands, what satisfies it, and its classic violations.

## H1 — Visibility of system status

The system keeps users informed about what is going on, through appropriate feedback within reasonable time.
**Demands:** every action acknowledged; ongoing processes show progress; current state (where am I, what's selected, what mode, saved or not) readable at a glance.
**Satisfied by:** pressed states, progress bars, "Saved just now", active-nav markers, selection counts, sync indicators.
**Classic violations:** silent saves, spinners with no context, background jobs with no status surface, pagination without position.

## H2 — Match between system and the real world

Speak the users' language; follow real-world conventions; make information appear in natural, logical order.
**Demands:** domain vocabulary of the *user*, not the org or schema; metaphors users already hold; formats matching locale expectations (dates, currency, units).
**Classic violations:** internal jargon ("entities", "instances"), error codes, engineering units, alphabetical ordering where workflow ordering is natural.

## H3 — User control and freedom

Users perform actions by mistake and need a clearly marked emergency exit — undo, redo, cancel — without an extended process.
**Demands:** undo for mutations; cancel for ongoing processes; back that works and preserves state; exit from every flow, wizard, and modal; no roach motels (easy in, impossible out — subscriptions included).
**Classic violations:** modal without close, wizard without back, actions that commit instantly and irreversibly, cancellation flows designed to fail.

## H4 — Consistency and standards

Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform and industry conventions.
**Demands:** internal consistency (one term, one pattern, one placement per concept) and external consistency (platform conventions, Jakob's Law).
**Classic violations:** three button styles for the same action class, "Delete" here / "Remove" there for the same operation, custom controls where platform ones exist.

## H5 — Error prevention

Better than good error messages is a careful design that prevents problems from occurring — eliminating error-prone conditions or checking and confirming before commitment.
**Demands:** constraints over validation ([Norman P6](../don-norman/principles.md)); good defaults; confirmation for high-cost commitments; slip-proofing (spacing, distinctiveness) and mistake-proofing (clear model, honest labels).
**Classic violations:** free-text where a picker fits, destructive defaults, format-sensitive inputs, adjacent opposite-meaning buttons.

## H6 — Recognition rather than recall

Minimize memory load by making elements, actions, and options visible. Users should not have to remember information from one part of the interface to another.
**Demands:** visible options over memorized commands; context carried forward (show the item being edited/ordered/deleted); recently-used surfaced; field help in place.
**Classic violations:** confirmation screens that don't restate what's being confirmed, search requiring exact names, multi-step flows hiding earlier choices, icon-only toolbars for non-universal icons.

## H7 — Flexibility and efficiency of use

Accelerators — unseen by the novice — speed up interaction for the expert, so the design caters to both. Allow users to tailor frequent actions.
**Demands:** keyboard shortcuts, bulk operations, recent/pinned items, templates/defaults, deep links — all layered *over* a fully usable novice path (Norman NR1).
**Classic violations:** expert-only UI (bare command line for everyone), or novice-only UI (five clicks for the hundredth repetition), no bulk select, no keyboard path through forms.

## H8 — Aesthetic and minimalist design

Interfaces should not contain irrelevant or rarely needed information; every extra unit of information competes with the relevant units.
**Demands:** each element justified by user value; progressive disclosure for the rare; visual noise treated as a usability cost, not a style issue.
**Classic violations:** dashboards of everything, promo banners inside task flows, settings pages of 60 unranked toggles.
**Note:** minimalist ≠ signifier-free; cutting affordance cues violates H1/H6 ([Norman anti-pattern](../don-norman/anti-patterns.md)).

## H9 — Help users recognize, diagnose, and recover from errors

Error messages in plain language (no codes), precisely indicating the problem and constructively suggesting a solution.
**Demands:** visible error (user notices it happened), located (which field/what object), explained (why), actionable (what now), and non-destructive (input preserved).
**Classic violations:** toast errors vanishing before reading, "Something went wrong", validation summaries far from fields, error pages without a way forward.

## H10 — Help and documentation

Best if the system needs no explanation; when needed, help should be easy to search, focused on the user's task, listing concrete steps, and not too large.
**Demands:** in-context help first (adjacent hints, empty states that teach); searchable task-oriented docs second; help reachable from where the confusion happens.
**Classic violations:** manual-as-onboarding, help centers organized by feature instead of task, tooltips explaining what a redesign should make obvious (see [Krug decision framework](../steve-krug/decision-framework.md): cut before explaining).

## Meta-principles

- **M1 — Heuristics are lenses, not laws.** Two can conflict (H7 accelerators vs H8 minimalism); resolve with the [decision framework](decision-framework.md) and profile.
- **M2 — Tag findings.** Every UX finding cites its heuristic — the tag carries justification and speeds triage.
- **M3 — Severity = frequency × impact × persistence.** Rate every finding; unrated findings don't prioritize.
