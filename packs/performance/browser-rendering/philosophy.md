# Philosophy — Browser Rendering Pack

## Not all pixel changes cost the same

A common misconception treats "changing something on screen" as a single undifferentiated operation. In reality, the browser's rendering pipeline has distinct, increasingly expensive stages, and different CSS/JS changes trigger different subsets of them. Understanding the pipeline turns "why is this animation janky" from folklore into a mechanical diagnosis: which stage is this change forcing, and can it be moved to a cheaper one?

## The frame budget is the real constraint

Smooth motion requires a new frame roughly every 16.7ms (60fps) or 8.3ms (120fps on modern displays) — all the work to produce that frame (JavaScript, style calculation, layout, paint, composite) must fit inside that budget, or a frame is dropped and motion visibly stutters. This is a hard real-time constraint, not a soft guideline — the pipeline exists to help developers reason about what fits.

## The compositor thread is the escape hatch

Most rendering work happens on the browser's main thread, contending with JavaScript execution, style calculation, and layout — but transform and opacity changes can be handled entirely by the compositor thread, running independently of main-thread work and capable of staying smooth even while JavaScript is busy elsewhere. This is *the* mechanical reason "animate transform/opacity only" is such a durable, cross-framework, cross-decade rule.

## Reflow is the pipeline's most expensive event, and often invisible in the code

A layout-triggering change (reading `offsetHeight` after a style mutation, animating `width`) can force the browser to recompute geometry for large portions of the page — and because this happens inside the browser's internals, it's invisible in a code diff unless you know which properties/reads trigger it. This pack exists to make that invisible cost visible and predictable.
