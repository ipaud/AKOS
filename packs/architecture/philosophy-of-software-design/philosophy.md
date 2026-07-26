# Philosophy — Philosophy of Software Design Pack

Why this source thinks what it thinks, and why the corpus is better with it in.

## The premise: complexity is the problem, not a side effect

Most engineering advice optimizes something adjacent — testability, reusability, purity,
conformance to a pattern. This source takes the position that the actual constraint on a
long-lived system is how hard it is to understand and change, and that everything else is
instrumental. Techniques are judged by whether they reduce that, not by whether they are
principled.

That reframing is what makes the pack useful next to the ones already here. `solid` gives
rules about responsibility. `clean-architecture` gives rules about dependency direction.
`design-patterns` gives named structures. All three answer "what shape should this be?"
This source asks "what does this cost the next person?", which is a different question, and
occasionally the two answers diverge.

## Why it is willing to disagree

The source argues openly against positions that are close to consensus — notably that
functions and classes should be made as small as possible. Its objection is not
contrarian: it follows directly from the depth model. If a boundary's cost is the interface
a caller must learn, then decomposition past the point where a unit hides something is
simply adding cost with no offsetting benefit, and the resulting system is more complex
while every individual piece looks better.

The corpus needs that counterweight. A knowledge system holding only sources that agree
produces confident advice with no way to notice when it is wrong. The disagreement is
recorded explicitly in [decision-framework.md](decision-framework.md) rather than resolved
by omission, because a pack that quietly dropped the inconvenient half would be a worse
source than the book.

## Why it is Level 3 and what that means

A book by one author, with the author's own context — systems software, research, teaching,
long-lived codebases with small teams. That context is real and it shows: the advice
assumes code that will be read for years by people who can be expected to hold a design in
their head. Applied to a two-week prototype, or to a codebase whose framework has strong
granularity idioms of its own, it is straightforwardly wrong.

Level 3 in this system means *decision framework, not commandment*, and it is why this pack
produces nothing above MEDIUM, scores `n/a` under the Prototype profile, and yields to any
Level 0 personal convention. Those are not hedges added for politeness — they are what
prevents a design opinion from acquiring the authority of a safety floor.

## The one idea worth keeping if you keep nothing else

**Ask what the caller stops needing to know.**

It applies to a function, a class, a service, a module, an API, a configuration file. It
converts an aesthetic argument into an answerable question. It is the test behind almost
every rule in this pack, and a reviewer who applies only that one has most of the value.

## What it shares with the rest of the corpus

The idea that the cheapest control is the thing that was never created — the same shape
appears in [privacy P3](../../security/privacy/principles.md) about data collection, in
[agent-foundations](../../ai-engineering/agent-foundations/philosophy.md) about reaching for
an agent, in [constitution Article 7](../../../core/constitution.md), and in
[pau-avila principle 2](../../personal/pau-avila/principles.md) about challenging
complexity as a standing instruction rather than a scheduled review. This source is the
most developed treatment of that idea in the corpus, which is the strongest argument for
its inclusion.
