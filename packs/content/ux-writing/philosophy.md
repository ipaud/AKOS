# Philosophy — Interface Writing

## Words are the part of the interface that makes claims

Layout arranges, colour emphasizes, motion directs — none of them assert anything. Words do. A button that reads `Send` asserts that pressing it sends something. An empty state that reads `No results` asserts that a search ran and found nothing. Every string is a claim about the system's state or behaviour, and users act on those claims without verifying them, because verifying is the product's job.

That makes interface copy the only layer of a product that can be *false*. A misaligned card is ugly; a mislabelled button is a lie the user acts on. This pack treats copy defects as behaviour defects, because to the user they are indistinguishable.

## Copy is the cheapest lever and the last resort

Changing a word costs minutes and can rescue a flow that a redesign would have taken weeks to fix. That cheapness is why writing is the right first move when users hesitate — and exactly why it gets abused. Text gets added to explain a control that should have been redesigned, to soften a workflow that should have been shortened, to warn about a consequence that should have been made reversible. Copy used as a patch hides the defect while making the screen heavier.

So the discipline runs in both directions: reach for words before reaching for a redesign, and reach for deletion before reaching for more words. The best microcopy on most screens is the sentence that turned out to be unnecessary once the control was named properly.

## The writer is the last honest reader of the code

Someone has to ask what the handler actually does before the label is written. If a control sets a status field, the label cannot say it sent an email. If nothing is imported and no model is called, the feature is not "Import (AI)". If the operation can fail, the success message cannot fire before the result is known. This is not pedantry about wording — it is the point at which a product's marketing to itself collides with what it built, and copy is where that collision becomes visible to users.

Teams drift here without malice. A feature gets named during planning, the implementation gets descoped, the label survives. Interface writing is the routine check that the words still describe the software.

## Consistency beats variety, always

Prose rewards synonyms; interfaces punish them. A reader enjoys "swap", "substitute" and "exchange" in a paragraph; a user reading them on one screen concludes there are three features. Every synonym is a new concept to someone learning the product, and users are always learning the product. Interface vocabulary is closer to an API than to writing: names are identifiers, and renaming one instance without the others is a breaking change.

## Tone is a response, not a personality trait

A product has one voice — that part is fixed, and it belongs to the brand. Tone is what the voice does when the user's circumstances change. The same product should sound different when someone is exploring than when their payment failed, and the difference is not decoration: playfulness at a moment of loss or cost reads as contempt. Writing well under stress means reading the user's emotional state off the situation — stakes, reversibility, whether they caused it, whether they're in a hurry — and adjusting warmth, brevity and formality accordingly. The voice stays recognizable; the register moves.

## Anxiety concentrates at commitment points

Users are calm while browsing and tense at the moment of irreversibility: paying, deleting, publishing, sharing, submitting something that reaches other people. The words placed within a few pixels of that moment do more work than any other copy in the product, and they answer the unspoken questions: what exactly happens, can I undo it, who sees it, what does it cost, when does it end. A reassurance located on a policy page reaches nobody. Proximity is the whole mechanism.

## Text is data, not decoration

Strings are shipped artifacts: they get versioned, translated, read aloud by screen readers, truncated by narrow viewports, and surfaced on lock screens far from their original context. Writing that only works when assembled by string concatenation, only fits at English length, or only makes sense with the surrounding screen visible is writing that breaks the moment the product leaves its home conditions. Compose whole sentences, expect them to grow, and assume they will be read alone.

## Where this philosophy stops

This lens is the words attached to controls and states. It does not cover long-form content strategy, plain-language rewriting or content lifecycle — see [gov-uk-content-design](../gov-uk-content-design/philosophy.md). It does not decide whether the screen or feature should exist — see [steve-krug](../../ux/steve-krug/philosophy.md) and the product lens. And it never overrides the safety floor: copy that carries meaning no keyboard or screen-reader user can reach is a defect regardless of how well it reads.
