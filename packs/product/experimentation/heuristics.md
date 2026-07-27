# Heuristics — Experimentation Pack

Defaults with known exceptions. Use while deciding whether and how to test; the
[engineering rules](engineering-rules.md) apply once a test exists.

- **Do the sample-size arithmetic before anything else, including before writing the
  ticket.** It takes two minutes and it cancels most proposed experiments. That is the
  point.
- **Under a few thousand weekly users into the funnel, you cannot A/B test conversion.**
  Say so plainly. It is a fact about arithmetic, not a lack of ambition.
- **Write down what you'll do for each outcome before you launch.** If every branch ships,
  cancel. If no branch changes anything, cancel. Half of proposed tests die here.
- **Ask "how could this metric go up while the product gets worse?"** If the answer is easy,
  pick a different criterion.
- **Declare guardrails even when you're confident.** They cost nothing and they are the only
  thing standing between a win and an unnoticed regression.
- **Fix the end date and stop looking.** Checking a running test and stopping when it looks
  good is the most common way to be confidently wrong, and it feels like diligence.
- **Check the split ratio before you look at the outcome.** Once you've seen the result you
  cannot un-see it, and a broken split invalidates it anyway.
- **Log exposure where the user could actually notice the change**, not at flag evaluation.
  Counting unexposed users drags every effect toward zero.
- **Run an A/A test before trusting a new setup.** If two identical arms produce winners,
  the analysis is broken and every result after it is fiction.
- **Expect to lose.** Most tested changes do nothing or hurt. A pipeline that mostly reports
  wins is measuring wrong, not winning.
- **Report the interval, not the verdict.** "Significant" and "not significant" both hide
  the number people actually need.
- **Never say "no difference".** Say "no difference larger than X detectable at this power".
  The first is a claim you did not make.
- **Treat a segment you found afterwards as the next test, not this conclusion.** Slicing
  until something appears is a procedure that always succeeds.
- **Two weeks of novelty is not a durable gain.** If the effect shrinks across the window,
  believe the trend rather than the total.
- **Don't test whether to meet the floor.** Accessibility, security, and safety are not
  variants.
- **When you can't test, decide and record why.** That is a legitimate, common, honest
  answer — and far better than a number nobody should trust.
