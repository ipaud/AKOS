# Decision Framework — Touch Ergonomics Pack

Decision rules for touch-interaction calls. Compose with [core/decision-framework.md](../../../core/decision-framework.md).

## Which target floor applies

| Control | Floor | Reasoning |
|---|---|---|
| Primary action, submit, confirm | 44 / 48 minimum, larger is fine | Tapped under pressure, often one-handed |
| Destructive action | 44 / 48 **and** isolated from neighbours | Cost of a misfire is unbounded |
| Close, back, dismiss | 44 / 48 | The only escape from the surface |
| Repeated control (per-row, per-item, stepper) | 44 / 48 | Repetition multiplies the error rate |
| Secondary control in a dense list | 24 minimum + spacing exception satisfied, 44 preferred | Legitimate use of the conformance floor; record it |
| Inline link inside a paragraph | Exempt (SC 2.5.8 inline exception) | Sizing it would break the text |
| Control with an equivalent elsewhere on the page | Exempt if the equivalent meets the floor | SC 2.5.8 equivalent exception; the equivalent must be genuinely reachable |

**Rule:** name which row you are in before defending a size. "It passes 2.5.8" is only an answer for the fifth and sixth rows.

## Enlarge the visual control, or enlarge the hit area

1. **Grow the element's own box (padding).** Default. Visible in devtools, participates in layout, cannot silently overlap.
2. **Grow the layout slot** (min-height on the row, larger gap). Use when several small controls share a container.
3. **Expand with a pseudo-element** (`inset: -Npx`). Last resort, when the visual design genuinely cannot carry a larger box.
4. **Move the control somewhere with room.** Often the right answer when 1–3 all fight the design.

If you reach step 3, you owe three things: the computed bleed `(F − w)/2`, the list of neighbours checked, and the gap arithmetic `gap ≥ F − (wA + wB)/2` for each. Skipping that check is how invisible hit areas start overlapping and resolving by paint order.

## Which keyboard does this field ask for

| Field | `type` | `inputmode` | `autocomplete` | `enterkeyhint` | What the user sees |
|---|---|---|---|---|---|
| Email | `email` | — | `email` | `next` | Letters with `@` and `.` |
| Phone | `tel` | — | `tel` | `next` | Dialler keypad with `+ * #` |
| One-time code | `text` | `numeric` | `one-time-code` | `done` | Digits; SMS suggestion offered |
| Postal code | `text` | `text` (or `numeric` where always digits) | `postal-code` | `next` | Letters or digits — never `type="number"` |
| Card number | `text` | `numeric` | `cc-number` | `next` | Digits |
| Card expiry | `text` | `numeric` | `cc-exp` | `next` | Digits |
| Integer quantity | `number` | `numeric` | `off` | `next` | Digits, no separator |
| Money / decimal amount | `text` | `decimal` | `off` | `done` | Digits + the **locale** decimal separator |
| Search | `search` | `search` | `off` | `search` | Letters, "Search" return key |
| URL | `url` | `url` | `url` | `go` | Letters with `/` and `.` |
| Person's name | `text` | — | `given-name` / `family-name` | `next` | Letters, word autocapitalization |
| Street address | `text` | — | `street-address` | `next` | Letters |
| Free-text note | `textarea` | — | `off` | `enter` | Letters, newline on return |

Notes that decide cases:

- `type="number"` does not reliably produce a compact numeric keypad; `inputmode` is what selects the keypad. Choose `type` for semantics and `inputmode` for the keys.
- `inputmode` restricts nothing. Paste, hardware keyboards, and autofill all bypass it. Validation lives in code.
- `inputmode="numeric"` offers digits only — no decimal separator, no minus sign. If the value can be fractional or negative, it is `decimal` or `text`.
- Prefer `type="text"` for anything that is a digit *string* rather than a quantity: leading zeros survive, `maxlength` works, and the element does not sanitize input the user can still see.

## `type="number"` or `text` + `inputmode="decimal"`

Choose `type="number"` only when **all** of these hold: the value is a true quantity, spinner increment/decrement makes sense, leading zeros are meaningless, no grouping separators will be typed, and `valueAsNumber` semantics are what you want. Otherwise choose `text` + `inputmode`.

The deciding failure: in a comma-locale, a user types the separator their keypad offers into a `type="number"` field. The element's own value sanitization rejects it, `el.value` reads empty and `valueAsNumber` reads `NaN` — while the user can still see the characters they typed. Any handler using `|| 0` then commits zero, and nothing anywhere reports an error. That single interaction is the reason this decision has its own section.

## Parsing a user-entered number

```js
// Derive separators from the locale rather than a hardcoded map.
function separatorsFor(locale) {
  const parts = new Intl.NumberFormat(locale).formatToParts(12345.6);
  return {
    group: parts.find((p) => p.type === 'group')?.value ?? '',
    decimal: parts.find((p) => p.type === 'decimal')?.value ?? '.',
  };
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/** Returns a finite number, or null. Never a fallback zero. */
export function parseAmount(raw, locale = navigator.language) {
  let amount = String(raw).trim();
  if (!amount) return null;

  // A currency symbol is accepted at either edge, never in the middle.
  amount = amount
    .replace(/^\p{Sc}\s*/u, '')
    .replace(/\s*\p{Sc}$/u, '');
  if (!amount || /\p{Sc}/u.test(amount)) return null;

  const { group, decimal } = separatorsFor(locale);
  const groupToken = escapeRegExp(group);
  const decimalToken = escapeRegExp(decimal);
  const integer = group
    ? `(?:\\d+|\\d{1,3}(?:${groupToken}\\d{3})+)`
    : '\\d+';
  const localeShape = new RegExp(
    `^-?${integer}(?:${decimalToken}\\d+)?$`,
  );

  let canonical;
  if (localeShape.test(amount)) {
    canonical = group ? amount.split(group).join('') : amount;
    canonical = decimal === '.' ? canonical : canonical.replace(decimal, '.');
  } else {
    // A bare amount may use the other common decimal separator exactly once.
    // Grouped or malformed strings never reach Number().
    const alternate = decimal === ',' ? '.' : ',';
    const parts = amount.split(alternate);
    if (
      parts.length !== 2
      || !/^-?\d+$/.test(parts[0])
      || !/^\d+$/.test(parts[1])
    ) return null;
    canonical = `${parts[0]}.${parts[1]}`;
  }

  const n = Number(canonical);
  return Number.isFinite(n) ? n : null;
}

console.assert(parseAmount('12oops', 'en-US') === null);
console.assert(parseAmount('1,2,3', 'en-US') === null);
```

Decision rules around it:

- **Failure is an error state, not a default.** `null` renders a message and blocks commit. Substituting `0` is data loss with a friendly face.
- **Accept both separators when the field is a bare amount** — users type the dot out of habit on a comma keyboard — but only when the string contains exactly one separator candidate. `1.234` in a comma-locale is genuinely ambiguous; resolve it by echoing the interpretation, not by guessing silently.
- **Echo before commit.** Render `Intl.NumberFormat(locale, {style:'currency', currency}).format(parsed)` next to the field. The user sees `€1.234,00` and catches your misreading before the total does.
- **Store canonical, format for display.** Minor units or a decimal type in storage; locale formatting at the edge.

## Gesture: primary, accelerator, or not at all

| Situation | Decision |
|---|---|
| The action already has a visible control; the gesture is faster for experts | **Accelerator** — ship both |
| The action has no visible control | **Not yet** — build the control first; the gesture is not the feature |
| The gesture is the function itself (drawing, map pan/pinch, signature) | **Essential** — permitted as the only path (SC 2.5.1 essential exception), documented as such |
| The gesture is path-based or multi-point and the action is ordinary | **No** — single-pointer alternative is normative |
| The gesture starts within a system-reserved edge strip | **No** — redesign; you will lose to the OS |

Discoverability is not a defence for gesture-only design: a hint the user must first find in order to learn a gesture they must then perform is two failures, not one.

## Where does this control go

Start from the thumb arc, then apply consequence:

1. **How often is it used in a single task?** Every iteration → bottom third. Once per session → middle. Rarely → top is acceptable.
2. **What does a misfire cost?** Unbounded (delete, send, pay) → out of the natural arc, isolated, ideally behind a disclosure.
3. **Is it the only route?** Close, back, and save must be reachable one-handed; a second placement is cheaper than a redesign.
4. **Is the screen used in the field?** Standing, one hand busy → bottom third is a requirement, and the sticky bar must survive the keyboard.
5. **Does anything cover it?** Check `env(safe-area-inset-bottom)`, the browser URL bar, and the keyboard, in that order.

When steps 1 and 2 conflict — the destructive action is also the frequent one, as in a bulk-cleanup screen — keep it out of the easy zone and invest in undo instead. Frequency is an argument for *recoverability*, never for putting deletion under the resting thumb.

## Confirm, undo, or neither (touch variant)

Follow [ux-writing's confirm/undo table](../../content/ux-writing/decision-framework.md), with three touch amendments:

- **Undo outranks confirmation more strongly on touch**, because misfires come from imprecision rather than intent and a dialog does not prevent an imprecise tap on the dialog.
- **The undo affordance goes in the bottom third** and lasts long enough for someone looking at a partially occluded screen to notice it.
- **If you confirm, relocate.** The confirming control must not appear where the finger just landed; otherwise a fast double-tap defeats the entire mechanism.

## When to branch on pointer capability

| Question | Query | Then |
|---|---|---|
| Can this device be touched at all? | `@media (any-pointer: coarse)` | Apply touch sizing and spacing. Sizing follows the **coarsest** available pointer. |
| Does the primary pointer hover reliably? | `@media (hover: hover) and (pointer: fine)` | Add hover enhancements. Nothing inside may be required. |
| Is the screen narrow? | `@media (max-width: …)` | Layout only. **Never** touch behaviour or hover affordances. |

The asymmetry is the point: over-sizing for a mouse user costs a few pixels; under-sizing for a touch user costs the feature. When the queries disagree — a hybrid laptop reporting both — size for coarse and treat hover as additive.
