# Tests

## Unit (`tests/unit/`, Python stdlib `unittest`)

No pytest, no new dependency — matches this project's own constraint (`python3` is the one accepted external tool). Run:

```bash
python3 -m unittest discover -s tests/unit -p 'test_*.py' -v
```

Roughly 315 tests (run the command above for the exact count — CI is the source of truth) across the YAML parser, the schema validator and registry, the metadata migration, the marked-section parser, the Python-version-floor helper, draft-pack routing, the personal-layer integrity/manifest helper, all 8 rule detectors, freshness banding, review history, markdown link integrity, and the Review Summary template. A recurring pattern worth naming: **every detector's test file locks down the specific bug that detector's own construction found** — e.g. `test_a11y_input_no_label` asserts `htmlFor` (not just `for`) is recognized, because that was a real false-positive this session hit before shipping. A test that only asserts the happy path wouldn't have caught any of these; the near-miss case is the one that matters.

Notable additions: `test_marked_sections.py` includes a deliberate sabotage test — reverting the parser to "grab the first START and first END" (the exact bug it replaces) must fail at least one case. `test_pack_lifecycle_routing.py` derives its expectations by reading the real corpus's `metadata.yaml` `status` fields at test time, never a hardcoded list of draft pack names, so a future promotion/demotion can't silently make the test stale.

## Integration (`tests/integration/`, bash)

```bash
for t in tests/integration/test_*.sh; do bash "$t"; done
```

Each script uses `mktemp -d` and never writes outside it — except `test_end_to_end_project.sh`, which necessarily calls `akos profile create` (there is no "scratch AKOS repo" mode for that command) and cleans up via a `trap` on any exit path, not just success.

- `test_marker_replace.sh` — the exact scenario that caught `write_marked_section`'s BSD-awk bug (M4): install-project twice, with a real content change in between, confirming the rerun actually updates rather than silently no-op-ing. Also covers the shared parser's adversarial guarantees end to end: `install-project` preflights all 4 managed files and refuses (writing none of them) when one has an ambiguous marker structure; `profile use` rejects a malformed `.akos/config.md` instead of treating it as absent; a project path containing spaces still works.
- `test_python_required.sh` — `install.sh`/`update.sh`/every operational `akos` subcommand refuse to run (zero mutation) without a valid Python 3.10+, simulated deterministically via `AKOS_PYTHON_BIN` pointing at a trivial fixture script (never by altering the real interpreter); `doctor.sh` reports a missing/old Python as a build failure, not a warning; `help`/`doctor` are confirmed to still work without Python; `create-pack`'s date computation fails loudly rather than silently substituting today's date; the resolved interpreter is confirmed to be the one actually used (via a logging wrapper), not a second `python3` found on PATH.
- `test_update_preserves_personal.sh` — builds a real local git remote (a bare clone of the current working tree, no network) so the git-pull-**success** branch actually executes, not just "not a git repository." Covers: a real pull that modifies a personal-layer file (restored), one that deletes a file and adds a new one (both reverted — restore is a full-tree snapshot, not a partial fill), an untracked symlink surviving unfollowed, a failing pull, a non-git checkout, a concurrent run being rejected by the lock, a simulated restore failure (via an `AKOS_PYTHON_BIN` wrapper that fails only the `restore` subcommand — no fragile fs-permission tricks, no root-avoidance assumptions) reporting failure honestly, and a broken tree failing the final `doctor.sh` gate.
- `test_install_isolated.sh` — `install.sh` against a scratch `$HOME`: the symlinks it creates, idempotence, and the no-clobber guards that leave a user's real skill dir / agent file / `~/DEV` untouched.
- `test_uninstall_isolated.sh` — `uninstall.sh` against a scratch `$HOME`: foreign files left alone, declining keeps everything, typed confirmation backs up all of `packs/` before deleting, and a failed backup aborts rather than deleting.
- `test_end_to_end_project.sh` — doctor, validate, benchmark, profile create/use, create-pack (scaffolds `schema_version: 1` and validates clean), history record/list, all invoked for real through `bin/akos` in one run.
- `test_path_with_spaces.sh` — a project directory with spaces in its path; would break first on any unquoted path in `bin/akos` or the Python tooling.
- `test_doctor_self_scan.sh`, `test_gitignore_reviews.sh`, `test_version_freshness.sh` — plant a defect, assert the relevant gate fires, then assert recovery.

## Both run in CI

See `.github/workflows/ci.yml` — unit tests via `unittest discover`, integration tests by iterating `tests/integration/test_*.sh`.
