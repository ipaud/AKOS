# Prompt Fragments — Philosophy of Software Design Pack

Copy-paste blocks for injecting this pack into an agent prompt. Read this file first — in
most tasks the build-mode block is all that needs loading.

## Fragment: build-mode constraint block

```text
DESIGN CONSTRAINTS (Level 3 — decision framework, not a floor; skip entirely in Prototype
profile, and yield to any Level 0 personal convention):

Boundaries
- Before splitting anything, say what the new unit hides from its caller. "It was getting
  long" is not an answer.
- Prefer one longer unit with a clear interface over several short ones sharing state.
  Exception: a testing seam, or a piece with a different reason to change.
- Interfaces must be simpler to describe than the implementations they hide.
- Adjacent layers offer different abstractions. No pass-through methods, no wrappers that
  only rename arguments.

Knowledge
- One design decision — format, encoding, key layout, ordering rule — is known to exactly
  one module. The same knowledge in two places is coupling even without an import.
- Group modules by what they know, not by the order operations happen in.
- Don't expose implementation choices (data structure, index, cache) through the interface.

Errors
- Before adding an exception, try to make the condition normal: deleting what's absent,
  closing what's closed, cancelling what stopped should all succeed.
- An exception every caller handles identically is handled once, lower down.
- Fold special cases into the normal path, or say why they can't be.

Naming and comments
- Names let a reader predict what the thing does NOT do. One concept, one word.
- If a comment explains a name, fix the name instead.
- Write the interface comment BEFORE the implementation — if it's awkward to write, the
  boundary is wrong.
- Comments carry what code can't: intent, units, invariants, the rejected alternative.
  Never a restatement of the line below.

Cost
- Pull complexity downward: the implementer absorbs the awkward case so callers don't.
- Each config parameter asks a caller to decide something the module knows better. Justify
  it individually.
```

## Fragment: review lens

```text
Review this code against the AKOS philosophy-of-software-design pack
(architecture/philosophy-of-software-design).

Report findings citing rule codes (PSD1–PSD36). MEDIUM is the maximum severity this pack
produces — nothing here blocks, and nothing here is a safety floor.

Prioritize, in order: information leakage (the same design decision known to two modules),
temporal decomposition, leaked invariants (callers required to call in a fixed order),
change amplification visible in the diff, then shallow modules, then comments and naming.

MANDATORY for every finding: name what a caller or the next reader would stop having to
know if it were fixed. If you cannot write that sentence, drop the finding — an
unfalsifiable design objection is worse than the problem it names.

Do not report a file for being long. Report an interface for being wide. Where a Level 0
personal convention (packs/personal/<profile>/coding-preferences.md) covers file size or
decomposition, that convention wins and code following it is not a finding.
```

## Fragment: the split test

```text
Before splitting this into separate units, answer:

1. What will the new unit hide that its caller currently has to know?
2. Will the two halves change for different reasons — and can you name them?
3. Would the same knowledge (a format, an ordering, an encoding) now live on both sides?
4. Write the new unit's interface comment. Is it simpler to describe than the code it
   hides?

If 1 and 4 both fail, don't split. One longer unit with a clean interface is the correct
answer even when it feels untidy.
```

## One-liner (for tight token budgets)

```text
Design floor (L3, advisory, skip in Prototype): a split must hide something — say what the
caller stops needing to know or don't split; interfaces simpler than implementations; one
design decision known to one module; group by knowledge not by stage; no pass-through
layers; define errors out of existence before handling them; pull complexity down into the
module rather than out to callers; names predict what a thing doesn't do; write the
interface comment first as a design test; comments carry intent, never restatement. Never
report a finding without naming who stops needing to know what.
```
