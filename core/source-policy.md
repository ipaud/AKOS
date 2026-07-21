# Source Policy

AKOS distills knowledge; it never reproduces it. This policy binds everyone (human or agent) who writes or extends packs.

## Hard rules

1. **No copied paragraphs.** Not one. Rewriting must happen at the idea level, not the sentence level — "paraphrase by synonym" is still copying.
2. **No long quotes.** If a short phrase is quoted (a named law, a term of art), it's a term, not a passage: "recognition over recall" is fine; a quoted paragraph is not.
3. **No chapter reconstruction.** A pack must not mirror a book's table of contents or recreate its structure section-by-section. Organize by the AKOS file contract instead — that reorganization *is* the transformation.
4. **Original examples only.** Invent examples; never lift the source's case studies, screenshots, or sample copy.
5. **Attribution by pointer.** `references.md` and `metadata.yaml` cite title, author, organization, and official URL. Nothing else from the source appears.
6. **Facts and ideas are free; expression is not.** Distilling "users satisfice rather than optimize" into an operational rule is legitimate use of an idea. Copying the author's explanation of it is not.

## What distillation looks like

The transformation pipeline for any source idea:

```
source idea → why it's true (philosophy) → durable rule (principle)
→ default with exceptions (heuristic) → checkable rule (engineering rule)
→ pass/fail item (checklist) → invented example → prompt fragment
```

If a pack file could only have been written by someone holding the book open, it fails this policy. If it could have been written by an expert who internalized the ideas years ago, it passes.

## Trademark & naming

Pack names may reference authors/works for identification (`packs/ux/steve-krug/`) — that's nominative use. Packs must state they are independent distillations, not endorsed by or affiliated with the source. Each pack `README.md` carries the line:

> Independent distillation for personal engineering use. Not affiliated with or endorsed by the source authors. See `references.md` for the originals — buy/read them; this pack is a lossy operational index, not a substitute.

## Standards documents

Open standards (WCAG, OWASP, RFCs) permit broader reuse, but the policy stays the same for consistency: restate requirements operationally, link the normative text. Success criterion numbers (e.g. "WCAG 1.4.3") are identifiers — always cite them so the normative source is one click away.

## Community sources (Level 4)

Same rules. Additionally: a Level 4 idea enters a pack only after it's been verified against practice or a higher-level source — packs must not launder blog speculation into system knowledge.
