# Mental Models — Touch Ergonomics Pack

Named models this pack contributes. Use them as diagnostic lenses while building and reviewing.

## The contact patch

A tap is not a point; it is a contact ellipse roughly the size of a fingertip pad, from which the system derives a single coordinate. The user cannot see the ellipse, cannot see the derived point, and cannot correct either before committing — the correction opportunity that a mouse gives you (move, look, then click) does not exist. Design consequence: the target must be large enough that the derived point lands inside it even when the ellipse is offset, and far enough from neighbours that an offset lands on nothing rather than on the wrong thing.

**Diagnostic:** for each interactive element, ask "if the contact point lands 6px off in the worst direction, what gets activated?" If the answer is a different control, the layout is wrong. If the answer is a *destructive* control, it is a critical finding.

## The two floors

There are two different numbers and conflating them causes arguments that never resolve.

| | Number | Status | What it means |
|---|---|---|---|
| **Legal floor** | 24×24 CSS px | WCAG 2.2 SC 2.5.8, Level AA, with exceptions | The point below which the interface fails an accessibility conformance claim |
| **Ergonomic target** | 44×44 pt (Apple) / 48×48 dp (Material) | Platform guidance, Level 1 on their platform | The size at which people actually hit things reliably, one-handed, in motion |

The legal floor is a compliance boundary with documented escapes (spacing, inline, equivalent, essential, user-agent). The ergonomic target is what the design should aim at. A 24px control that passes 2.5.8 via the spacing exception is *conformant* and still a bad button. Design to 44/48; use 24-with-spacing only where the layout genuinely cannot carry the larger box, and record it.

**Diagnostic:** when someone defends a small target, ask which number they are invoking. If they are invoking 24 to justify a primary action, they are using a floor as a goal.

## The contested strip

Enlarging a hit area beyond the visible control creates invisible geometry. When two enlarged areas overlap, the overlapping band belongs to whichever element wins hit-testing — normally the one painted later or stacked higher. Nothing about that resolution is a design decision; it is an accident of DOM order and stacking context, and it is invisible in every screenshot and every design file.

The band has a size you can compute. For two adjacent controls with visual widths `wA` and `wB` and a target floor `F`, the visual gap needed to avoid a contested strip is:

```
gap ≥ (F − wA)/2 + (F − wB)/2      →      gap ≥ F − (wA + wB)/2
```

**Diagnostic:** run the arithmetic on every icon-button cluster. A negative result means slack; a positive result larger than the actual gap is the width of the contested strip, and whichever control paints later owns it. If either control is destructive, treat the finding as critical regardless of the width.

## The occlusion cone

The hand hides a region of the screen around and below the contact point, biased toward the side the hand comes from. Feedback rendered inside that region is not delivered. This is why the desktop instinct — put the tooltip under the trigger, put the validation message under the field, anchor the toast to the bottom edge — inverts on touch.

**Diagnostic:** cover the lower-right third of the screen with your palm and re-read the screen. Anything you now can't see is feedback the user may not receive at the moment they need it.

## The thumb arc

A phone held in one hand gives the thumb a sweep — a rough arc pivoting from the base of the thumb, comfortable in the lower and inner part of the screen, straining at the top, effectively unreachable in the far top corner opposite the holding hand. Reach is therefore not uniform, and screen position encodes an implicit cost.

| Band (portrait phone) | Cost | Belongs here | Never here |
|---|---|---|---|
| Bottom third | Free — thumb rests here | Primary action, submit/next, main nav, the control used on every iteration | Destructive actions |
| Middle | Small shift of grip | Content, form fields, secondary controls | — |
| Top quarter | Regrip or second hand | Title, status, settings, rarely-used escapes | Primary action on a repeated task |
| Far top corner (opposite the grip) | Worst point on the screen | Nothing that matters | The only route to close, back, or save |

The arc also explains the destructive-action rule: the thumb's resting sweep should never cross a destructive control on its way to the primary one. Placing "Delete" adjacent to "Save" in the easy zone puts the most expensive mistake in the cheapest position.

**Diagnostic:** hold the device one-handed and reach for the primary action without regripping. Note every interactive element the thumb passes over on the way. Each one is a candidate misfire, and any destructive element among them is a finding.

## The keyboard contract

The markup on a text field is a contract in three parts, each addressed to a different party:

1. **`type`** — tells the browser what the value *is* (validation, autofill category, native pickers). Also constrains what the element will hand back to the code.
2. **`inputmode`** — tells the on-screen keyboard which keys to show. Purely presentational; it restricts nothing.
3. **`autocomplete`** — tells the platform's autofill which stored value belongs here, converting thirty taps into one.

Plus `enterkeyhint` for the return key's label, and `autocapitalize` / `autocorrect` / `spellcheck` for text handling. The contract is not enforcement: `inputmode="numeric"` shows a digit keypad and still accepts a pasted essay. Every field validates and parses on the code side regardless of what keyboard it asked for.

**Diagnostic:** for each field, name the keyboard the user will actually see and the exact character set they can produce with it. If the parser was not written against that character set, you have found a defect.

## Silent-coercion risk

Every input that reaches a number, date, or currency passes through a conversion. Conversions in JavaScript fail quietly: `Number("12,50")` is `NaN`, `parseFloat("12,50")` is `12`, `Number("")` is `0`, and the idiom `Number(x) || 0` turns every one of those failures into a confident zero. On a locale keypad that offers a comma, the failing input is not an edge case — it is what the keyboard hands you by default for half the world.

The model: draw the path from *keystroke* → *element value* → *parsed value* → *persisted value*, and mark every point where a bad input can become a plausible number instead of an error. Each unmarked point is where money quietly changes.

**Diagnostic:** type the locale's decimal separator into the field and check what is committed. If the answer is `0`, `NaN`, or an empty field with no error, the defect is present.

## Enforcement surface

For any rule in this pack, ask where it physically lives. Ranked by how much it actually binds:

1. **Impossible** — the primitive is the only way to build the thing, and it carries the rule.
2. **Caught at build** — lint rule, type constraint, or CI check fails the violation.
3. **Caught at runtime** — a backstop stylesheet or wrapper corrects bypasses that slipped through.
4. **Caught in review** — a human has to notice.
5. **Written down** — a doc explains the rule and its consequence.

Rung 5 alone is the state most teams are in when the audit finds the defect. The finding is never "they didn't know"; it is "knowing wasn't binding". Fixes are graded by which rung they install, not by whether they patch the instance.

**Diagnostic:** after fixing a violation, ask whether the same violation can be reintroduced by a developer who never reads the fix. If yes, the fix was rung 4.

## Pointer capability, not device class

The platform answers two independent questions, and neither is "how wide is the screen":

- `(any-pointer: coarse)` — *can* this device be touched at all? Governs sizing. Hybrid laptops answer yes.
- `(hover: hover)` — does the *primary* pointer hover reliably? Governs whether hover may add anything.

Sizing follows the coarsest available pointer; hover affordances follow the primary pointer and must always be supplementary. A width breakpoint answers neither question, and a desktop browser narrowed to 380px will lie to it in both directions.

**Diagnostic:** grep the codebase for width-based branches that gate touch behaviour or hover behaviour. Every hit is a capability question asked in the wrong language.
