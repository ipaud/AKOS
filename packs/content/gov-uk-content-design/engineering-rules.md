# Engineering Rules — GOV.UK Content Design Pack

Checkable in the artefact. Each rule can be verified by a reviewer, and most by a script. Violations are findings.

## Need and justification

- GCE1. Every published page has a recorded user need statement in the form *as a [user] I need to [action] so that [outcome]*. Missing statement = finding.
- GCE2. The need statement names a user outside the organisation. Needs whose beneficiary is the organisation ("so that we can communicate the change") fail.
- GCE3. Every page has a named individual owner and a review date, both stored as page metadata, not tribal knowledge.
- GCE4. No two live pages answer the same user question. Duplicates are merged and one is redirected.

## Readability targets

- GCE5. General-audience content scores at or below a Flesch–Kincaid grade level of **6** (approximately a reading age of 9). Specialist-audience content: grade level **9** maximum, and only with the audience recorded.
- GCE6. No sentence exceeds **25 words**. Mean sentence length across the page is **≤ 20 words**.
- GCE7. No paragraph exceeds **5 lines** as rendered at 320px width, and each paragraph carries one idea.
- GCE8. Passive constructions are **≤ 10%** of sentences, and **0** in instructions, obligations, deadlines, eligibility conditions, and consequences.
- GCE9. No sentence contains more than one subordinate clause.

## Front-loading

- GCE10. The first sentence of the page states the answer or the action, not the context. Word count of any preamble before the answer: **0**.
- GCE11. The first **three words** of every heading and link carry the distinguishing meaning. Headings beginning with "Information", "About", "Overview", "Introduction", "Further", "Additional" fail.
- GCE12. Every section's first sentence states that section's point.
- GCE13. Page title is **≤ 65 characters**, front-loaded, verb-led where the page describes a task, and does not repeat the site or section name.
- GCE14. Meta description, where used, is **≤ 160 characters** and restates the answer, not the organisation.

## Structure and format

- GCE15. Any sequence of **3 or more ordered actions** is rendered as a numbered list, not prose.
- GCE16. Any comparison of **2 or more items across 2 or more attributes** is rendered as a table with a header row using `<th>` and `scope`.
- GCE17. Bullet lists: each item is **≤ 2 sentences**; items share a grammatical form; the list is introduced by a lead-in line ending in a colon.
- GCE18. Bullet lists contain **≤ 8 items**. Longer lists are grouped under subheadings or converted to a table.
- GCE19. Headings are semantic (`h2`/`h3`), sequential without skipping levels, and never styling-only. Exactly one `h1` per page.
- GCE20. Any page longer than **~3 screens** at 320px has subheadings at least every **300 words**.
- GCE21. A page exceeding **800 words** is either split by task or justified in the page record. Above **1,500 words**, splitting is mandatory unless the content is a single indivisible legal text.
- GCE22. Conditional eligibility with **3 or more branching conditions** is presented as a question sequence, a table, or separate pages — never as nested prose conditionals.

## Vocabulary

- GCE23. No specialist term appears without a plain-language definition at first use on that page. Definitions do not rely on the reader having visited another page.
- GCE24. Acronyms are expanded at first use on every page, written without full stops, and are not used at all if used fewer than **3 times** on the page.
- GCE25. No metaphor, idiom, or figurative language in instructional content. Detection: journey, unlock, empower, roadmap, umbrella, landscape, ecosystem, seamless, deep dive, reach out.
- GCE26. Formal filler is absent. Detection list: "in order to", "prior to", "in the event that", "with regard to", "it should be noted", "please note", "please be advised", "utilise", "facilitate", "commence", "endeavour", "in respect of".
- GCE27. The words "simply", "just", "easy", "obviously" do not appear in instructions.
- GCE28. Latin abbreviations (e.g., i.e., etc., NB, via) are replaced with plain equivalents ("for example", "that is", "and so on", "through").
- GCE29. The reader is addressed as "you". The organisation is named or called "we", and only when it performs an action the reader needs to know about.
- GCE30. Where user vocabulary and official vocabulary differ, the user term appears first and the official term in brackets on first mention.

## Links and references

- GCE31. Link text describes its destination and works out of context. Banned link text: "here", "this", "this page", "click here", "read more", "learn more", "more information", bare URLs.
- GCE32. Link text is front-loaded and **≤ 8 words**.
- GCE33. No content is delivered only as an attachment (PDF, DOCX, spreadsheet) when it can be an HTML page. Attachments that remain have an HTML summary of the actionable content.
- GCE34. Every outbound reference to a volatile fact (price, threshold, date, system name) either restates the fact with a review date or links to the authoritative page rather than copying it.

## Numbers, dates and typography

- GCE35. Numbers are written as numerals except where a single word reads naturally at the start of a sentence; thousands use a comma separator; percentages use `%`.
- GCE36. Dates are written with the month spelled out (`14 March 2026`), no ordinal suffixes, and ranges use the word "to", not a dash.
- GCE37. Bold, italics, ALL CAPS and underline are not used for emphasis in body content; underline is reserved for links.

## Lifecycle

- GCE38. Every page carries a **review date ≤ 12 months** ahead. Content containing prices, legal thresholds, deadlines or system names: **≤ 6 months**.
- GCE39. Any page past its review date is flagged as stale and is either re-verified, revised, or retired within the review cycle. A stale page on a task-critical path is a blocking finding.
- GCE40. Retirement is executed as a redirect to the nearest correct answer, never as a 404 and never as a silent orphan. Retirement decisions are recorded with the reason.
