# Prompt Fragments — NN/g Pack

## Fragment: heuristic evaluation (full)

```text
Run a heuristic evaluation (NN/g ten heuristics, AKOS L2). Sweep the UI ten
times, one heuristic per pass — do not blend passes:
H1 status: is what's-happening always visible (async, background, save state)?
H2 language: any jargon, schema nouns, locale violations, unnatural ordering?
H3 exits: can users leave/undo/cancel everything they can enter? Try X,
   Escape, Back on every modal/flow.
H4 consistency: same concept = same word, placement, pattern? Platform
   conventions kept?
H5 prevention: what invalid input is possible that a constraint could
   prevent? Are defaults safe? Double-submit blocked?
H6 recognition: any step requiring memory of a previous screen? Confirmations
   restate their object?
H7 efficiency: keyboard path, bulk ops, recents/templates present for
   repeated tasks?
H8 minimalism: every element justified by user value? Advanced behind
   disclosure? Org-serving content in task flows?
H9 recovery: force errors (offline, bad data, double-click). Message = what
   + why + next step? Persistent? Input preserved?
H10 help: empty states teach? Help reachable at confusion points? Docs
   task-titled?
For each finding: heuristic tag, severity (frequency × impact × persistence
→ CRITICAL/HIGH/MEDIUM/LOW), concrete smallest fix.
```

## Fragment: single-heuristic deep pass

```text
Audit only H{N} ({name}) across the entire surface. List every violation
with location, evidence, severity, and fix. Do not report other heuristics'
findings — note them one-line at the end if severe.
```

## Fragment: severity calibration

```text
Rate each usability finding: frequency (what share of users/sessions hit
it), impact (nuisance / slows / fails the task), persistence (once /
recurring). CRITICAL = task failure for typical users. HIGH = common +
costly. MEDIUM = recoverable annoyance. LOW = cosmetic. Apply the
persistence multiplier: every-time problems rate one level up. Reject
findings you cannot rate.
```

## One-liner

```text
NN/g ten: visible status; user language; exits+undo everywhere; consistency
internal+platform; prevent errors with constraints; recognition not recall;
accelerators over a novice-complete path; every element earns its place;
errors say what/why/next and persist; help in context. Tag findings H1-H10,
rate severity by frequency × impact × persistence.
```
