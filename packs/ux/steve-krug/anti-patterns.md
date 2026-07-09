# Anti-Patterns — Krug Pack

Named failure modes. Detection cue → why it fails → fix.

## Mystery-meat navigation

**Detect:** icons or images as nav with no visible labels; users must hover/tap to learn what things are.
**Why it fails:** forces micro-experiments; invisible on touch; burns goodwill per hover.
**Fix:** visible text labels; icons may accompany, never replace. Exception: universally learned icons (search magnifier, cart) — few exist.

## Happy talk

**Detect:** opening paragraphs that welcome, congratulate, or describe passion; text that could appear on any site unchanged.
**Fix:** delete. Replace with the answer to "what can I do here?".

## Instructions as duct tape

**Detect:** paragraphs explaining how to use the form/screen below them.
**Why it fails:** nobody reads them; they mark a design that needs explanation.
**Fix:** redesign until instructions are unnecessary; keep at most one short adjacent hint.

## The sign-up wall

**Detect:** value hidden behind registration; "create an account to see results".
**Fix:** show value first, ask at the point of obvious benefit. If business demands the wall, record it as an explicit goodwill withdrawal (Ruling R10).

## Format tantrums

**Detect:** errors like "no spaces allowed", "enter phone as XXX-XXX-XXXX".
**Why it fails:** the machine lectures the human about a problem the machine can fix in one line of code.
**Fix:** accept everything reasonable, normalize server-side.

## The everything-is-important page

**Detect:** multiple primary buttons, banners competing with content, no visual resting point; squint test shows uniform noise.
**Fix:** pick the one thing; demote the rest. Hierarchy is choosing.

## Clever labels

**Detect:** navigation or buttons using brand-speak, puns, or invented nouns ("Ignite", "My Universe", "Solutions").
**Fix:** the word users would type when searching for it.

## You-are-nowhere pages

**Detect:** interior page fails the trunk test — no page name, no marked nav location, title doesn't match the clicked link.
**Fix:** page name where the eye expects it, `aria-current`, breadcrumbs at depth.

## Link roulette

**Detect:** "click here", "learn more", "read on" as link text; links whose destination is a surprise.
**Fix:** noun-bearing links that describe the destination.

## Hover-only interfaces

**Detect:** actions/affordances appearing only on mouse-over (row actions, card buttons).
**Why it fails:** invisible on touch; undiscoverable for everyone.
**Fix:** persistent affordances, or an explicit "⋯" menu — visible always.

## Carousel as decision-avoidance

**Detect:** homepage hero carousel rotating 3–7 messages.
**Why it fails:** motion draws attention while rotation guarantees nobody sees any message; it's the org chart refusing to prioritize.
**Fix:** one message. Stakeholder conflicts get resolved in meetings, not in the hero.

## Redesign reflex

**Detect:** response to a usability finding is a redesign project scheduled next quarter.
**Fix:** smallest change that removes the observed confusion, shipped now ("do the least you can do"); redesign only after small fixes demonstrably fail.

## FAQ as landfill

**Detect:** FAQ page answering questions the interface itself raises ("How do I change my email?").
**Why it fails:** each FAQ entry documents a place the UI failed.
**Fix:** treat FAQ entries as a bug list; fix the UI, delete the entry.

## The kitchen-sink homepage

**Detect:** every department's link "above the fold"; no tagline; pull-quote carousel; 40+ links.
**Fix:** value proposition + start-here paths for the top 2–3 user goals; everything else into ranked navigation.

## Desktop-crippled mobile

**Detect:** mobile version missing features "for simplicity", with no path to them; or "view desktop site" as the workaround.
**Fix:** full functionality, reprioritized layout. Cutting scope ≠ cutting layout noise.
