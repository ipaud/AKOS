# Prompt Fragments — SRE Pack

Copy-paste blocks for injecting this pack into agent prompts.

## Fragment: build-mode constraint block

```text
Apply SRE practice (AKOS L2):
- Every production service has SLIs on its critical user journeys —
  availability, latency, correctness — measured from the user's side, not
  from server internals.
- Each SLI carries an SLO target set from what users actually need. 99.9%
  and 99.99% are different engineering programs; never default to higher.
- The error budget is the SLO's complement: tracked, visible, reviewed on
  a fixed cadence by the owning team. When it is spent, feature work
  yields to reliability work until it recovers.
- Page only on user-facing symptoms — SLO burn rate, error rate, latency
  breach. Never page on raw resource metrics such as CPU or memory.
- Every paging alert is actionable at 3am, carries a written rationale
  for why it pages, and links a runbook with concrete next steps.
- Alerts routinely dismissed as noise are deleted or their root cause is
  fixed. Tolerated noise trains on-call to miss the real page.
- Known failure modes have runbooks, so response means following
  documented steps rather than improvising from one engineer's memory.
- Incidents above the defined severity threshold get a blameless
  postmortem naming systemic gaps, not people, with owned follow-ups
  tracked to completion.
- Recurring manual operational work is logged as toil and prioritized for
  automation, not absorbed as a permanent cost of running the system.
```

## Fragment: review lens

```text
Review this service's reliability posture as an SRE reviewer:
1. SLIs — are critical user journeys measured, and from the user's
   perspective? Name any journey with no indicator.
2. SLOs — is there a target, justified by user need not aspiration?
3. Error budget — tracked, visible, and does anything actually change
   when it runs out?
4. Alert quality — per paging alert: symptom or cause? Actionable at 3am?
   Times fired vs. times acted on over the last month?
5. Runbooks — does every alert link one, and can a non-expert follow it
   to confirm impact, mitigate, and verify recovery?
6. Postmortems — blameless in wording, systemic in cause, follow-ups
   assigned, dated, and closed?
7. Toil — what recurring manual work exists, and what automates it?
Report by severity. A page with no possible action, and a critical
journey with no SLI, are both HIGH.
```

## Fragment: alert design

```text
Design or repair an alert:
- State the user-visible symptom it detects and the SLO it protects.
- Set the threshold on SLO burn rate rather than a static resource
  number: fast burn pages, slow burn opens a ticket.
- Assign severity deliberately — page (a human must act now), ticket (act
  this week), dashboard only (no notification).
- Write the "why this pages" rationale in one sentence.
- Link a runbook covering: how to confirm user impact, immediate
  mitigation, escalation path, how to verify recovery.
- State expected fire frequency. If it would fire more than a few times a
  month, fix the system or lower the severity.
If any of these cannot be filled in, this alert must not page.
```

## Fragment: blameless postmortem

```text
Write a blameless postmortem:
- Impact first: what users experienced, how many, for how long, measured
  against the SLO and the error budget consumed.
- Timeline: detection, escalation, mitigation, resolution — call out the
  gap between failure start and detection explicitly.
- Contributing factors as systemic gaps: missing guardrail, unsafe
  default, absent runbook, unclear ownership. Name roles and systems,
  never individuals.
- Ask what allowed a normal action to have this impact, not who acted.
- Follow-up actions: each concrete, owned, dated, tracked where the team
  will see it. Separate prevention from faster detection and faster
  mitigation, and fund all three.
- Record what worked in the response so it is preserved deliberately.
```

## One-liner (for tight token budgets)

```text
SRE: SLIs on critical user journeys measured from the user's side; SLOs
set by user need; error budget tracked and enforced — spent budget means
reliability work; page only on user-facing symptoms and burn rate, never
CPU; every page actionable, rationaled, and runbook-linked; delete or fix
noisy alerts; blameless postmortems naming systemic gaps with owned
follow-ups; track and automate toil.
```
