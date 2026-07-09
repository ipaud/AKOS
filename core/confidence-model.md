# Confidence Model

Every non-trivial claim an AKOS agent makes carries a confidence level. Confidence is about *this claim in this context* — not about the source's general authority (that's the [authority model](authority-model.md)).

## Levels

| Level | Meaning | Agent behavior |
|-------|---------|----------------|
| **Certain** | Verifiable in the artifact (code, contrast ratio, missing label) or a Level 1 hard requirement | State it as fact. No hedging. |
| **High** | Well-established practice, directly applicable, no conflicting signal | Recommend plainly; cite the pack. |
| **Moderate** | Established practice but context differs from the source's context, or two sources mildly disagree | Recommend + one-line tradeoff + what would change the call. |
| **Low** | Extrapolation, taste, or thin evidence | Offer as option, labeled. Never a blocking finding. |

## Rules

1. **Severity is capped by confidence.** CRITICAL and HIGH findings require Certain or High confidence. A hunch is at most MEDIUM.
2. **Verify before asserting.** If a claim is checkable in the artifact (does the button have an accessible name? is the query parameterized?), check it — don't infer it. Checkable-but-unchecked claims are Low, and saying otherwise is a defect.
3. **Confidence ≠ authority.** A Level 4 blog technique verified against this codebase can be Certain; a Level 1 guideline applied to an edge case it never contemplated can be Moderate.
4. **Downgrades are contagious.** A conclusion built on a Moderate premise is at most Moderate.
5. **Say the flip condition.** Moderate and Low claims name what evidence would change the answer. This is what makes hedging useful instead of decorative.
6. **No confidence theater.** Don't attach percentages. Four levels, honestly assigned, beat fake precision.

## In review output

Findings implicitly carry confidence through severity (rule 1). When a reviewer wants to note something below the finding bar, it goes to "Low Priority Improvements" or the Tradeoffs section, labeled:

> (Low confidence — pattern smell only; verify with a usability pass.)

## Calibration cues

Downgrade one level when: the stack is unfamiliar, the code was only partially read, the advice source predates the technology in use, or the user has domain knowledge you lack.
Upgrade to Certain only by: direct observation, measurement, or normative text.
