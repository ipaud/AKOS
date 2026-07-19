# Anti-Patterns — GOV.UK Content Design Pack

Named failure modes. Detection cue → why it fails → fix.

## Org-chart content

**Detect:** navigation or page structure mirrors departments, teams, systems, or legal instruments. Section names are internal nouns. Completing one task requires visiting pages owned by three different groups.
**Why it fails:** transfers the organisation's internal complexity to a reader who has no map of it.
**Fix:** restructure by user task. Merge the fragments into one task page; keep internal ownership in metadata, not in the IA. (GC3)

## The question nobody asked

**Detect:** no user need statement, or one whose beneficiary is the organisation. Page exists because a launch, a policy change, or a senior request happened.
**Why it fails:** consumes search visibility and reader attention while meeting no need, and dilutes the pages that do.
**Fix:** delete or fold into a page that answers a real question. If the announcement matters internally, it belongs somewhere that is not the user's answer surface. (GC1, GCE1–GCE2)

## Happy talk preamble

**Detect:** the first paragraph welcomes, contextualises, congratulates, or explains why the organisation cares. The answer appears in paragraph two or later. Deleting the opening loses no information.
**Why it fails:** every reader pays for material that serves the author.
**Fix:** delete it. Start with the answer. (GC5, GCE10)

## The hidden actor

**Detect:** passive constructions in instructions, deadlines and consequences — "applications will be reviewed", "documents must be submitted", "payment will be processed". The reader cannot tell whether they must act.
**Why it fails:** it is a factual omission dressed as a style choice; readers miss obligations that were never assigned to them.
**Fix:** name who acts, in active voice: "we review applications within 10 working days", "you must send your documents by 14 March". (GC8, GCE8)

## Topic sprawl

**Detect:** page titled "X information" or "About X" that assembles everything known about a subject; multiple audiences addressed in alternating paragraphs; readers must extract their own case.
**Why it fails:** completeness for the author, extraction work for the reader — and the extraction is where people get it wrong.
**Fix:** split into task pages, each answering one question completely. (GC9)

## Jargon laundering

**Detect:** specialist terms replaced with vaguer near-synonyms while the underlying complexity is untouched. Reading age barely moves. Readers still cannot say what they must do.
**Why it fails:** treats plain language as a word-swap exercise rather than a restructuring of the explanation.
**Fix:** re-derive the content from the user need and say what the reader must do. Word choice comes last, not first. (GC4)

## Metaphor as explanation

**Detect:** journeys, umbrellas, roadmaps, unlocking, ecosystems, deep dives. The reader must solve an analogy before receiving a fact.
**Why it fails:** adds a decoding step, ages badly, and breaks on translation and for non-native readers.
**Fix:** state the literal fact. (GC11, GCE25)

## Formal filler

**Detect:** "in order to", "please note that", "it should be noted", "with regard to", "prior to", "endeavour to". Sentences long, information density low.
**Why it fails:** length with no content; pushes the answer down the page and past the scan.
**Fix:** mechanical deletion — most filler phrases delete to nothing or to one short word. (GCE26)

## Prose that should be a table or steps

**Detect:** a paragraph containing a sequence ("first… then… after that…"), or near-identical repeated paragraphs differing in two values, or nested conditionals ("if… unless… except where…").
**Why it fails:** forces readers to build the table or list mentally, which they do badly and inconsistently.
**Fix:** numbered steps, a table, or a question sequence. (GC7, GCE15–GCE16, GCE22)

## Zombie content

**Detect:** page past its review date, or with no review date and no owner. Prices, deadlines, screenshots or system names that no longer match reality. Still ranking in search, still confidently wrong.
**Why it fails:** fails silently — nothing errors, so nobody finds out until a user acts on it.
**Fix:** re-verify, revise, or retire with a redirect. Treat unreviewed content as suspect by default. (GC15, GCE38–GCE40)

## Duplicate answers

**Detect:** two or more pages answering the same question with different wording, and often different facts. Search returns both; support links to whichever one they remember.
**Why it fails:** guarantees drift; the two copies diverge, and readers cannot tell which is current.
**Fix:** merge into one, redirect the loser, and record the merge. (GCE4)

## The attachment dump

**Detect:** the actual answer lives in a PDF, spreadsheet or slide deck; the page is a download link with a sentence of context.
**Why it fails:** breaks on mobile, defeats search, degrades for assistive technology, and is never updated.
**Fix:** publish the actionable content as HTML; keep the attachment only for genuinely fixed-format artefacts. (GCE33)

## Link roulette

**Detect:** "click here", "read more", "this page", raw URLs. Link text that means nothing when read out of context or by a screen reader listing links.
**Fix:** front-loaded link text naming the destination. (GCE31–GCE32)

## Publish-and-forget

**Detect:** page never revised since publication; no post-launch look at search terms, bounces or support volume. Launch treated as completion.
**Why it fails:** first publication is a hypothesis; without iteration the hypothesis is never tested.
**Fix:** scheduled review at 1 month with real data; fix the highest-volume failure. (GC16)

## FAQ as landfill

**Detect:** an FAQ page absorbing questions that arise because the main content does not answer them, or because the interface is confusing.
**Why it fails:** each entry documents a failure elsewhere, and the answer ends up somewhere nobody looks.
**Fix:** move each answer into the page or interface where the question occurs, then delete the entry. See also the [steve-krug](../../ux/steve-krug/anti-patterns.md) treatment of the same smell.

## Content organised for search engines, not readers

**Detect:** repeated keyword phrases, bloated introductions to hit a word count, headings written for crawlers.
**Why it fails:** worsens the thing readers came for, and the answer that genuinely satisfies the query is the version that ranks anyway.
**Fix:** answer the question in the reader's words, once, first. (GC2, GC12)
