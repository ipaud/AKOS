# Prompt Fragments — UX Writing Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply interface-writing constraints (UX-writing pack, AKOS L3):
- Truth first: every action label names an effect the handler actually
  produces. Never label a capability the code doesn't have (no "(AI)" on
  deterministic logic, no "Import" on a control that takes no file).
- Confirmations fire only from the success branch. Async outcomes report
  the queued state, never the hoped-for one. One action = one message.
- One concept, one word, everywhere. No synonyms; no developer vocabulary
  (stub, null, payload, entity, enum, sync, bare status codes).
- Errors: what happened -> why (if known) -> what to do next. State the rule
  to satisfy, never blame the user, never ship a bare code.
- Empty states teach: what belongs here + why + one action. Distinct copy for
  first-run, no-results, cleared, and failed-to-load.
- Buttons: verb + object, <=3 words. Confirmation dialogs repeat the verb;
  no Yes/No/OK. The escape option names what it preserves.
- Forms: visible persistent labels (never placeholder-only), hints before
  typing, formats by example, normalize input instead of complaining.
- Reassurance sits at the commitment point: what happens, is it reversible,
  who sees it, what does it cost.
- No meaning in tooltips or title attributes only.
- Strings are whole sentences with named placeholders, in a resource layer,
  plural-rule APIs, layouts tolerant of +40% growth.
```

## Fragment: review lens

```text
Review this work as an interface-copy reviewer (UX-writing pack).
1. Truthfulness pass — REQUIRES THE DIFF, not just the screen. For every
   action label, read the handler and finish: "after pressing this, the user
   could verify that ___". Flag any label promising more than the code does,
   any success message not bound to a success branch, any capability claim
   without an implementation.
2. Terminology pass — grep for synonyms of each core concept and for
   developer vocabulary. Every duplicate term is a finding.
3. State pass — for each surface: are empty / loading / error / success all
   written, and are the four zero states distinguished?
4. Message pass — does every error and blocked state end with a next action?
   Any bare codes, blame, or vague status where the cause is known?
5. Commitment pass — mark each irreversible/costly/public action; is the
   reassurance adjacent, specific, and true about reversibility?
6. Accessibility-of-copy pass — any meaning living only in hover/title?
   Any status carried by colour alone?
7. Run review-checklist.md; report findings by severity with the exact
   replacement string, not a description of one.
Never write "improve the copy" — quote the current string, give the new
string, name the rule ID.
```

## Fragment: label-behaviour audit

```text
Audit label truthfulness in this diff. For each user-facing control:
- Quote the label.
- Summarize what the handler actually does (one line, observable effects only).
- Verdict: TRUE / OVERPROMISE / WRONG-CAPABILITY / MECHANISM-NOT-EFFECT.
- If not TRUE, give both fixes: the honest label, and what the code would need
  to do to earn the current one. Recommend one.
Also list every success/confirmation message with the branch it fires from,
and flag any that can fire when the operation did not succeed.
Output a table. No prose preamble.
```

## Fragment: terminology ledger builder

```text
Build a terminology ledger for this product from its user-facing strings.
- Extract every noun and verb that names a product concept.
- Cluster synonyms that refer to the same concept.
- For each cluster: pick the term users would type into a search box, list the
  banned synonyms (including the engineering word), and count occurrences of
  each variant with file references.
Output: a markdown table (concept | approved term | banned synonyms | files to
change) plus a ready-to-run grep command for the banned column.
```

## Fragment: message rewrite pass

```text
Rewrite these interface strings.
For each: original -> revised -> rule ID -> one-clause rationale.
Rules: errors get what/why/next; validation states the rule not the violation;
no blame, no bare codes, no apologies before facts; empty states teach and
offer one action; success names the resulting state; buttons are verb+object;
labels in a set share one grammatical form; no developer vocabulary; sentence
case throughout. If a string exists only to explain a control, say so and
propose the control change instead of rewriting the string.
```

## One-liner (for tight token budgets)

```text
UX-writing rules: the label must match what the code does; confirm only what
happened; one concept one word; no dev vocabulary; errors = what/why/next with
no blame or bare codes; empty states teach and offer an action; verb+object
buttons and dialogs that repeat the verb; visible labels, forgiving inputs;
reassurance at the commitment point; nothing meaningful in tooltips only; one
action one message; whole-sentence strings built for translation.
```
