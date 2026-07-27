# Anti-Patterns — Experimentation Pack

Named failure modes, how to spot them, and what to do instead. The first and last are the
ones most likely to apply here.

## The underpowered test

**Detect:** an experiment on a product with a few thousand users a week; a result quoted
with no mention of what effect the test could detect; "it wasn't significant so we killed
it" on a two-week test with a few hundred conversions.
**Why it fails:** the test never had the power to detect the effect, so it reported noise —
and the noise got treated as evidence. Worse than not testing, because "we don't know"
became a number people now cite.
**Fix:** calculate the required sample before building anything. If traffic can't reach it
in about four weeks, don't run it — pick from the alternatives in
[decision-framework.md](decision-framework.md) and record the judgement as a judgement.
(EXP2, EXP3, EXP40)

## Peeking

**Detect:** a dashboard checked daily; "it hit significance on Thursday so we shipped it";
a test stopped early with a good number and no sequential method declared up front.
**Why it fails:** the significance threshold assumes one look. Repeated looks with the
option to stop guarantee you eventually cross it by chance, on a change that does nothing.
It is the most common failure and it feels like diligence.
**Fix:** fix the duration in advance and stop looking, or choose a sequential method with
corrected thresholds *before* launch. Harm is the only valid reason to stop early. (EXP18,
EXP19, EXP21)

## The metric chosen afterwards

**Detect:** a report leading with a metric that wasn't in the plan; twenty metrics tracked
and the one that moved presented as the outcome; "the primary metric was flat, but…".
**Why it fails:** with enough metrics something always moves. Choosing after the fact is a
procedure guaranteed to find a winner in a change that did nothing.
**Fix:** one criterion, declared before launch, with the smallest effect worth shipping
for. Everything else is secondary and reported as such. (EXP4, EXP28, EXP32)

## The invisible sample ratio mismatch

**Detect:** a 50/50 test where the arms differ by a few percent in size; nobody checked;
the result was read first and the split noticed later, if at all.
**Why it fails:** an unequal split means assignment, logging, or filtering is broken —
often in a way correlated with the outcome (a variant that errors sends fewer users
through). The comparison is invalid however clean the numbers look.
**Fix:** check the split before the outcome, every time. A meaningful mismatch voids the
test until explained. (EXP14, EXP24)

## Exposure logged at the wrong moment

**Detect:** assignment counted at page load or flag evaluation, while the change is in a
flow most users never reach.
**Why it fails:** the denominator fills with people who could not have been affected, and
every effect is dragged toward zero. Real wins get killed as flat.
**Fix:** log exposure at the point the difference becomes perceptible. (EXP13)

## Randomize by user, analyze by session

**Detect:** an analysis whose sample size is much larger than the user count.
**Why it fails:** sessions from the same user are correlated, so treating them as
independent shrinks the interval and manufactures significance.
**Fix:** analyze at the unit you randomized. (EXP10)

## Segment mining

**Detect:** "flat overall, but a significant win for new mobile users in Spain" — a segment
nobody named before launch, found by slicing until something appeared.
**Why it fails:** enough slices guarantee a finding. This is the multiple-comparisons
problem wearing a product insight's clothing, and it is convincing precisely because it
comes with a plausible story.
**Fix:** pre-register the segments that matter. Anything found afterwards is the next
test's hypothesis, labelled exploratory. (EXP8, EXP29)

## Optimizing the proxy

**Detect:** a criterion like session length, clicks, or notification opens; a winning
variant that raised it by making something harder to find or more annoying to dismiss.
**Why it fails:** a measure adopted as a target stops measuring what it did. The cheapest
way to move engagement is usually to degrade the product.
**Fix:** ask how the metric could rise while the product gets worse. If that is easy,
choose a different criterion and declare guardrails that would catch it. (EXP5, EXP6)

## The two-week novelty win

**Detect:** a visible change to an established interface, a strong early effect, a decision
made at day ten, and an effect shrinking across the window.
**Why it fails:** regular users react to change as change. The test measured the reaction,
not the steady state.
**Fix:** run whole weeks, watch the trend, and treat a decaying effect as the signal it is.
(EXP7, EXP30)

## The suspiciously successful program

**Detect:** most experiments reported as wins; a year of shipped winners with no
corresponding movement in the top-line metric.
**Why it fails:** across mature products the large majority of tested changes do nothing or
hurt. A high win rate almost always means peeking, post-hoc metric choice, or a broken
analysis — and the missing top-line movement is the tell.
**Fix:** run an A/A test. If two identical arms produce winners, everything reported since
the pipeline was built is fiction. (EXP17, EXP37)

## Testing the floor

**Detect:** an arm with the accessibility fix withheld, a variant without a security
control, a "does anyone actually use keyboard navigation" test.
**Why it fails:** it withholds a floor requirement from real people to generate data about
whether the floor is popular. The floor is not contingent on usage.
**Fix:** ship it. Measure adoption afterwards if you want the number. (EXP42)

## Experimentation theatre on a small product

**Detect:** a feature-flag platform, an experiment review process, and a metrics pipeline
built for a product with a few hundred weekly users; a "test" whose result would never have
been readable.
**Why it fails:** it spends the scarcest resource a small team has on machinery that cannot
produce a valid answer, and it lends the appearance of rigour to decisions that were
actually judgement calls.
**Fix:** do the arithmetic, accept that you cannot experiment yet, and use the cheaper
methods that genuinely work at that scale — usability testing, interviews, staged rollout
with instrumentation. Say "we decided" rather than "we tested". (EXP3, EXP38, EXP40)
