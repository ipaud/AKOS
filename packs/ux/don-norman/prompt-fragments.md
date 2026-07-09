# Prompt Fragments — Norman Pack

## Fragment: build-mode constraint block

```text
Apply interaction-design constraints (Norman school, AKOS L2):
- Signify every affordance that matters: primary actions visibly cued;
  gestures/shortcuts only as accelerators over visible paths.
- Natural mapping: controls adjacent to what they affect; directions
  consistent; ordered controls mirror effect order; label similar controls.
- Feedback: acknowledge <100ms; progress >1s; cancelable >10s; state
  (account, mode, sync, unsaved) always visible; results say what+where.
- Constraints before validation: prevent invalid input via pickers,
  filtering, disabled-with-reason; every planned error message is a
  missing-constraint question first.
- Error design: undo over confirmation for reversible; forcing functions
  for irreversible; destructive actions distinct and distant; error copy =
  cause + next step, no blame.
- One conceptual model: one term per concept; no implementation vocabulary;
  no invisible modes — behavior-changing state shows a persistent indicator.
```

## Fragment: failure-diagnosis lens

```text
Diagnose the reported interaction failures using Norman's taxonomy:
1. For each failure, classify the gulf: execution (couldn't figure out how
   to act) or evaluation (couldn't tell what happened).
2. For each user error, classify slip (right intent, wrong motion) vs
   mistake (wrong model). State the evidence for your classification.
3. Prescribe the fix lever in priority order: constraint → mapping →
   signifier → feedback → conceptual model. Justify skipped levers.
4. Flag any slip being treated with a mistake remedy or vice versa
   (e.g. confirmation dialogs patching model failures).
```

## Fragment: state-visibility audit

```text
Audit state visibility: enumerate every piece of system state that changes
behavior or interpretation (auth account, workspace, mode, sync/offline,
unsaved changes, environment). For each: where is it visible? Is it
persistent while active? Could a user discover it only by acting? Report
invisible or test-to-discover state as HIGH; invisible modes as CRITICAL.
```

## One-liner

```text
Norman rules: signify affordances; map controls to effects; feedback <100ms
with visible state; constrain before validating; undo > confirm; distinct &
distant destructive actions; slips get mechanics, mistakes get better models;
one term per concept; no invisible modes.
```
