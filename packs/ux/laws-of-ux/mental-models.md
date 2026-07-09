# Mental Models — Laws of UX Pack

## The cost model of interaction

Every interaction charges the user in four currencies: **decision cost** (Hick), **motor cost** (Fitts), **memory cost** (Miller), and **learning cost** (Jakob). Total task cost is the sum across steps. Design optimization = shifting these costs onto the system (Tesler) until only irreducible cost remains. Reviews can literally walk a flow and tally the four costs per step.

## Memory as sampler, not recorder

Users don't remember experiences; they remember samples — peaks, endings, firsts, lasts, oddballs (Peak-End, Serial Position, Von Restorff). Consequence: perceived quality is designable somewhat independently of average quality. Ethical line: use sampling to *represent* the experience honestly at its best, not to hide what it is.

## Attention as a scarcity economy

Distinctiveness (Von Restorff) is zero-sum: each highlighted element taxes all others. Think of accent color, motion, size, and isolation as a fixed budget per screen. The squint test ([Krug](../steve-krug/heuristics.md)) is this model's audit tool.

## Motivation as gradient

Users are not uniformly motivated through a flow; motivation rises with visible proximity to the goal (Goal-Gradient) and collapses at perceived dead ends. Progress indicators, sub-goals, and completion moments are motivation engineering. Drop-off analytics along a funnel = a gradient map showing where perceived distance spiked.

## Perception colors judgment

Users cannot separately evaluate "how it looks" and "how it works" (Aesthetic-Usability). Their trust, patience, and even bug reporting are filtered through visceral response. Two practical readings: polish is not optional garnish (it changes measured behavior), and user *praise* is contaminated evidence (watch success rates, not smiles).

## Complexity conservation

For any task the user wants done, a fixed quantum of complexity exists (Tesler). UI simplicity claims must answer: where did it go? Good answers: defaults, inference, automation, the dev team's code. Bad answers: it's now the user's memory burden, an error message, or a support ticket.
