# Philosophy — Coding Agents

## Fluency is not evidence

The defining property of a system that writes code by predicting what code should look like is that its output is well-formed whether or not it is right. A human who does not know an API writes hesitant code, leaves a comment, or stops to look it up; the hesitation is itself a signal, and readers use it. A generated call to a function that does not exist arrives with the same syntax, the same idiomatic shape, and the same confident surrounding prose as a call to one that does. This removes from the process the single cheapest error-detection mechanism software engineering ever had — the visible uncertainty of the person writing. Nothing replaces it except execution, which is why the discipline of this pack looks so heavily weighted toward running things. It is not thoroughness for its own sake. It is the reconstruction of a signal that fluent generation destroys.

## The report is part of the artifact

There is a habit of treating the code as the deliverable and the summary of the work as a courtesy wrapped around it. For an agent this inverts the actual risk. A defect in the code is caught by a test, a type checker, a reviewer, or production; a defect in the report — "all tests pass", "no callers affected", "backward compatible" — is caught by nobody, because its entire function is to tell people what they no longer need to check. A false completion claim is not a communication problem downstream of the engineering. It is the highest-leverage bug the process can produce, and it should be graded like one.

## Verification is an act, not an attitude

The gap between believing a change is correct and knowing it is correct is not closed by care, experience, or the amount of reasoning applied before writing. It is closed by one specific event: a command ran against the changed artifact and something read what came back. Everything that feels like verification but is not — reviewing the diff again, reasoning through the control flow, noting that the change is small and obviously safe — operates on the same information that produced the change and therefore inherits every assumption that produced it. This is why the discipline is stated in terms of executed commands and exit codes rather than in terms of rigor. Rigor is unfalsifiable; an exit code is not.

## The environment answers questions the model cannot

An agent editing a repository is not working from knowledge; it is working in an environment that already contains the answers to almost every question it might otherwise guess at. Does this function exist — the source is on disk. Do the tests pass — the runner is installed. Is this the project's convention — forty other files demonstrate it. Are there other callers — search takes a second. The characteristic failure is not that these answers are unavailable but that answering from memory is faster and feels equally reliable at the moment of writing. Every rule about searching before editing, reading before writing, and checking an API before calling it reduces to the same instruction: the repository is the authority, and consulting it is cheaper than being wrong.

## A change has a blast radius, and it is rarely the file you opened

The unit of thought when editing is naturally the file in view, and the unit of consequence almost never is. A signature has callers; a column has queries; a config key has deployments; an exported name has importers you never enumerated. The discipline of treating an interface change as a migration rather than an edit is not caution — it is a correction to a systematic perceptual bias, in which the part of the change that is visible feels like the whole of it. This is also why the smallest correct diff matters beyond reviewer convenience: a small diff has a small blast radius that a person can actually hold in mind, and a large one does not, regardless of how carefully it was constructed.

## Consistency beats correctness at the level of style

A codebase's conventions are usually somebody's second choice, and they are almost always worth keeping anyway. Their value does not come from any individual convention being right; it comes from being able to read the next file without relearning anything. An agent has both the capability and the inclination to improve local style continuously, and doing so silently, inside changes about something else, produces a codebase where every file reflects the taste of whatever process most recently touched it. The rule that existing conventions win is not deference. It is a recognition that uniformity is itself a load-bearing property, and that unilaterally trading it for a marginally better pattern is a bad trade made by the party who does not pay for it.

## The failing check is the cheapest form of the problem

There is a pull toward the state where everything is green, and it is strong enough that the mechanisms which produce red — a lint rule, a type error, a failing test, a reviewer's objection — start to feel like obstacles between the work and its completion rather than as its instrumentation. This inversion is where suppression comes from: not from a decision that the check is wrong, but from a framing in which green is the goal and the check is what stands in the way. Restated correctly, the check is doing the most valuable thing anything in the process does, and it is doing it at the moment when acting on it is cheapest. The commit that adds an ignore directive does not remove a problem; it removes the only place the problem was visible, and defers it to a moment when it is expensive.

## Where this philosophy stops

This pack is about the process discipline of the edit — how an agent orients, changes, verifies, and reports on a modification to a real repository. It is not about what shape the surrounding system should be or how it should be bounded, which is [agent-foundations](../agent-foundations/README.md); nor about what the agent gets to see when it works, which is [context-engineering](../context-engineering/README.md). It does not decide whether the design being implemented is good — that is architecture, and it lives in [packs/architecture](../../architecture/) — nor what a codebase's test strategy should be, which is [packs/testing](../../testing/). And it does not lower any safety floor: an edit that satisfies every rule here can still introduce a vulnerability, break accessibility, or corrupt data, and running the tests is not a substitute for the reviews that catch those.
