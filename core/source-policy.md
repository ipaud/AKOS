# Source Policy

AKOS distills knowledge; it never reproduces it. This policy binds everyone (human or agent) who writes or extends packs.

## Hard rules

1. **No copied paragraphs.** Not one. Rewriting must happen at the idea level, not the sentence level — "paraphrase by synonym" is still copying.
2. **No long quotes.** If a short phrase is quoted (a named law, a term of art), it's a term, not a passage: "recognition over recall" is fine; a quoted paragraph is not.
3. **No chapter reconstruction.** A pack must not mirror a book's table of contents or recreate its structure section-by-section. Organize by the AKOS file contract instead — that reorganization *is* the transformation.
4. **Original examples only.** Invent examples; never lift the source's case studies, screenshots, or sample copy.
5. **Attribution by pointer.** `references.md` and `metadata.yaml` cite title, author, organization, and official URL. Nothing else from the source appears.
6. **Facts and ideas are free; expression is not.** Distilling "users satisfice rather than optimize" into an operational rule is legitimate use of an idea. Copying the author's explanation of it is not.

## Source intake gate

Answered in the PR **before** `akos create-pack` runs. The hard rules above govern
what a pack may do with a source; this gate governs whether the source earns a pack
at all.

**A pack is doctrine, not reference.** It is justified when the source holds a
*position* that distills into checkable engineering rules and binary checklist items.
An encyclopedic reference — an API changelog, MDN, a language spec read as lookup —
has no position to distill, and an agent can already look it up. Those enter as a
`sources[]` entry inside an existing pack, or not at all.

1. **What position does this source hold that yields 10+ checkable rules?** If the
   honest answer is "it explains how X works", it's reference — no pack.
2. **What gap does it close that no existing pack closes?** Back it with a grep across
   `packs/`, not intuition. More than half overlapping an existing pack → extend that
   pack instead.
3. **What authority level, and why?** Per [authority-model.md](authority-model.md):
   standards body or platform owner → 1; broad multi-decade acceptance → 2; a book or
   named methodology → 3.
4. **If Level 3 (a paper) or Level 4 (web, blog): what corroborates it?** A paper alone
   doesn't earn Level 3 — corroborated adoption does. **A Level 4 source may never be a
   pack's primary source**; it enters only alongside a higher-level one, per the
   Community sources rule below.

Two consequences worth stating, because both are asked repeatedly:

- **Papers become sources inside packs, never packs themselves.** The corpus already
  works this way: the agent packs cite ReAct-class papers under a "methodology papers,
  applied as decision frameworks" heading in `references.md`. No pack is named after a
  paper.
- **A website earns a pack only when it is the platform owner's normative
  documentation.** Every web-sourced pack in the corpus meets that bar. Third-party
  product docs cap at Level 2.

## What distillation looks like

The transformation pipeline for any source idea:

```
source idea → why it's true (philosophy) → durable rule (principle)
→ default with exceptions (heuristic) → checkable rule (engineering rule)
→ pass/fail item (checklist) → invented example → prompt fragment
```

If a pack file could only have been written by someone holding the book open, it fails this policy. If it could have been written by an expert who internalized the ideas years ago, it passes.

## Trademark & naming

Pack names may reference authors/works for identification (`packs/ux/steve-krug/`) — that's nominative use. Packs must state they are independent distillations, not endorsed by or affiliated with the source. Every pack `README.md` carries a line opening with **"Independent distillation"** and pointing at `references.md`. `doctor.sh` checks for it.

The canonical long form, for a pack distilling a book or an author's body of work:

> Independent distillation for personal engineering use. Not affiliated with or endorsed by the source authors. See `references.md` for the originals — buy/read them; this pack is a lossy operational index, not a substitute.

A terse variant is acceptable where the long form doesn't fit the source — a standards body has no "originals to buy" — as long as it opens the same way and links `references.md`:

> Independent distillation; not affiliated with or endorsed by OWASP. See `references.md`.

What is *not* acceptable is omitting it. The requirement is the claim of independence, not the exact sentence.

## Standards documents

Open standards (WCAG, OWASP, RFCs) permit broader reuse, but the policy stays the same for consistency: restate requirements operationally, link the normative text. Success criterion numbers (e.g. "WCAG 1.4.3") are identifiers — always cite them so the normative source is one click away.

## Community sources (Level 4)

Same rules. Additionally: a Level 4 idea enters a pack only after it's been verified against practice or a higher-level source — packs must not launder blog speculation into system knowledge.
