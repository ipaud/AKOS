# Review Checklist — Experimentation Pack

Binary checks. Only the two ethics items are CRITICAL; the rest is Level 3 methodology.

**Check the gate first.** If the surface does not have the traffic to detect the effect,
stop — the only applicable items are the two CRITICALs and the alternatives section. A
review that walks the full checklist on an underpowered test has already accepted the
premise that the test should exist.

## Gate

- [ ] Required sample size was calculated, not guessed. (EXP2)
- [ ] Expected traffic reaches it within about four weeks. If not, the test was **not
      run** and an alternative method was chosen and recorded. (EXP3, EXP38)
- [ ] A decision was written for every possible outcome before launch; no branch where
      everything ships regardless. (EXP1)

## Critical (blocks in every profile)

- [ ] No arm withholds safety, accessibility, or security. (EXP42)
- [ ] Experiment data is treated as personal data — inventoried, minimized, retained
      deliberately, covered by the deletion path. (EXP43)

## High

- [ ] One decision criterion, declared before launch, with the smallest effect worth
      shipping for. (EXP4)
- [ ] Guardrail metrics declared before launch, including at least one measure of user
      harm. (EXP5)
- [ ] The criterion cannot be moved cheaply by making the product worse. (EXP6)
- [ ] Randomization unit matches analysis unit. (EXP10)
- [ ] Assignment is stable per subject and independent of user attributes. (EXP11, EXP12)
- [ ] Exposure is logged where the user could perceive the difference, not at page
      load. (EXP13)
- [ ] Observed split ratio matches the intended ratio, checked **before** outcomes. (EXP14)
- [ ] Filtering is identical across arms and defined before launch. (EXP15)
- [ ] The test ran to its planned duration; no early stop on a good-looking number. (EXP18)
- [ ] Neither variant changed mid-flight. (EXP20)
- [ ] Diagnostics were reviewed before results. (EXP24)
- [ ] Results reported as effect size with an interval, not a bare significance
      verdict. (EXP25)
- [ ] A flat result is reported as "no detectable difference at this power", with the
      threshold stated — never as "no difference". (EXP27)
- [ ] The reported analysis matches the pre-registered plan; deviations stated. (EXP32)

## Medium

- [ ] Duration covers whole weeks and a full weekly cycle. (EXP7)
- [ ] Analyzed segments were named in advance. (EXP8)
- [ ] The plan was recorded somewhere durable before launch. (EXP9)
- [ ] Control is the current experience with identical instrumentation. (EXP16)
- [ ] The pipeline was validated with an A/A test before first use. (EXP17)
- [ ] Any early-stopping used a sequential method chosen in advance. (EXP19)
- [ ] Guardrails were monitored throughout and could stop the test. (EXP21)
- [ ] One change per test, or the bundle is explicitly what is claimed. (EXP23)
- [ ] Effect compared against the shipping threshold, not just against zero. (EXP26)
- [ ] Multiple comparisons adjusted, or the inflated false-positive rate stated. (EXP28)
- [ ] Post-hoc segment findings labelled exploratory. (EXP29)
- [ ] Trend across the window reported where the effect shrinks. (EXP30)
- [ ] The decision followed the pre-written rule. (EXP33)
- [ ] A guardrail regression alongside a win carries a recorded tradeoff. (EXP34)

## Low

- [ ] Traffic allocation was not adjusted mid-test. (EXP22)
- [ ] The result states what changed, with explanations labelled as hypotheses. (EXP31)
- [ ] Winners rolled out gradually with guardrails still monitored. (EXP35)
- [ ] Losing variant's code and the flag removed after the decision. (EXP36)
- [ ] Results recorded, including negatives and flat ones. (EXP37)
- [ ] Changes shipped without a test are still instrumented. (EXP39)
- [ ] Judgement calls recorded as judgement — "we tested it" not claimed for an
      underpowered test. (EXP40)
- [ ] Plausible-harm changes reviewed before launch. (EXP44)

## Reviewer discipline

- **Check power before anything else.** Every other finding on an underpowered test is
  moot, and reviewing the methodology of a test that should not exist legitimizes it.
- **"Not significant" is not "no effect".** Ask what effect the test could have detected. If
  nobody knows, that is the finding.
- **A pipeline reporting mostly wins is a finding.** Most tested changes do nothing or hurt
  (P11). A high win rate usually means peeking, post-hoc metric selection, or a broken
  analysis — not unusual product skill.
