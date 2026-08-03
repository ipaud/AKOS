# Authoring a rule

`rules/README.md` has the quick version. This is the fuller walkthrough, with the reasoning behind each step, using `SUPABASE_RLS_DISABLED` as the worked example.

## 1. Decide Level A or B honestly

Ask: can a script answer this question correctly, or does it need to *understand* something (layout, intent, structure)? If a regex can only approximate the answer with real false positives either direction, it's Level B — cap it at MEDIUM and exclude it from CRITICAL-only exit gating in the registry. `A11Y_INPUT_NO_LABEL` is the worked counter-example: real label association is tree-structural, so it shipped as Level B on purpose, not as a compromise.

Don't round Level B up to Level A because the detector "usually works." The whole point of the level is honesty about the false-positive rate, not a badge.

## 2. Write the registry entry first

```yaml
# rules/security/supabase-rls-disabled.yaml
id: SUPABASE_RLS_DISABLED
title: Table created without Row Level Security enabled
domain: security
level: A
severity:
  default: CRITICAL
  profiles:
    Prototype: HIGH        # override per-profile only where the default is genuinely wrong for that context
confidence: Certain
related_packs:
  - backend/supabase
detector: rules/security/supabase-rls-disabled.py
applies_to:
  glob: ["**/*.sql"]
  target: project-source   # or akos-packs, for a rule that scans AKOS's own repo (see PACK_EXPIRED)
recommendation: One sentence, imperative, telling the fix.
version: 1
status: stable
```

Writing this before the detector forces the actual question: what severity, what confidence, which packs does this relate to. A detector without an honest registry entry is untrustworthy by construction — severity and confidence aren't afterthoughts to bolt on once the regex works.

## 3. Write the detector

```python
# rules/security/supabase-rls-disabled.py
def run(files: list[Path]) -> list[dict]:
    ...
    return [{"evidence": [{"path": str(path), "line_start": n, "line_end": n, "snippet": "..."}]}]
```

That's the whole contract: `run(files) -> list[dict]`, each dict at least `evidence`. Optional per-finding overrides: `severity_override`, `confidence_override`, `detail` (replaces the registry's `recommendation` just for this finding — used when the fix depends on what was actually found, e.g. the JWT role in `SECRET_IN_SOURCE`), and `blocking: True` to make a finding gate the exit code even when its severity is below CRITICAL (used for a realistic live credential that defaults to HIGH — see `SECRET_IN_SOURCE`). CRITICAL always blocks regardless. Don't reach for `blocking` to turn ordinary HIGH findings into gates; reserve it for a finding that must stop a ship on its own.

**Severity is not adjusted by path.** A real credential or a real destructive migration under `tests/`, `fixtures/`, or `docs/` is still real, so the runner never downgrades a finding for living in one of those directories. If AKOS's own synthetic corpus would otherwise trip a detector, keep the realistic value out of version control (a placeholder materialized into a temp copy at scan time — see `benchmarks/runners/run.py`), never a path exclusion.

**A detector that cannot run is an error, not a finding.** If `run` raises, the detector file is missing, or there is no `run()`, the runner records an `ExecutionError` and the scan reports status `error` (exit 1) — it never manufactures a placeholder finding and never reports clean. Let a genuinely unexpected input raise rather than swallowing it into an empty result.

**Suppression is centralized in the runner** (`rules/runner.py`'s `is_suppressed`), checking an `akos:allow RULE_ID` comment on or within a few lines before the evidence line. Don't reimplement suppression inside a detector.

## 4. Test the true positive AND the near-miss — before trusting either

This is the step every shipped detector's construction skipped at first, and every one of them had a real bug caught by doing it anyway:

- `SUPABASE_RLS_DISABLED` — scanning file-by-file instead of across all matched files together would have false-positived on the normal "table created in one migration, RLS added in a later one" pattern.
- `A11Y_INPUT_NO_LABEL` — only recognizing HTML's `for` attribute, not JSX's `htmlFor`, flagged every correctly-labeled React input.
- `SECRET_IN_SOURCE` — a naive substring check for "test" in a path matched `/tmp/secret-test/` (this very testing session's own scratch directory), silently skipping real secrets under any path merely containing the word.
- `DESTRUCTIVE_MIGRATION_NO_GUARD` — a fixed 3-line guard window let a comment meant for one statement suppress an unrelated destructive statement a few lines later.

None of these would have been caught by testing only the positive case. Write both, in the same sitting, before moving to the next rule.

## 5. Add a benchmark case

`benchmarks/README.md` has the mechanics. The short version: a case per true-positive/near-miss pair you tested by hand in step 4, so the next person's change to this detector (or a shared helper it depends on) gets caught by `akos benchmark run`, not rediscovered by hand.

## 6. Run `akos rules run` against something real, once

Fixtures prove the logic is internally consistent. Running the rule against an actual project (even a small one) is what proves the `applies_to.glob` is scoped sensibly and the detector doesn't choke on real file encodings, BOMs, or directory layouts fixtures don't happen to exercise.
