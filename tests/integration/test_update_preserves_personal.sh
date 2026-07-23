#!/usr/bin/env bash
# update.sh must never lose or silently change packs/personal/ content — not
# even after a REAL, successful `git pull --ff-only` that legitimately
# updates tracked personal-layer files upstream. That is what makes the
# personal layer "personal": update.sh treats ANY drift from the pre-update
# snapshot, even from a real upstream commit, as something to detect and
# restore, not adopt.
#
# Builds a real local git remote — a bare clone of AKOS_HOME — so the
# git-pull-SUCCESS branch actually executes, not just "not a git repository"
# (which a prior version of this test only covered). Everything is local
# filesystem access; no network is used anywhere in this file.
set -euo pipefail

AKOS_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

pass() { printf '  ok - %s\n' "$1"; }
fail() { printf '  FAIL - %s\n' "$1"; exit 1; }

export HOME="$TMP/home"
mkdir -p "$HOME"

# The remote must reflect the CURRENT WORKING TREE under test (including any
# uncommitted changes to update.sh/personal_layer_integrity.py themselves),
# not whatever AKOS_HOME's last git commit happened to be — `git clone`
# alone would silently test a stale, already-committed version of this very
# script. Snapshot the working tree into a fresh baseline repo, then bare it.
BASELINE="$TMP/baseline"
mkdir -p "$BASELINE"
( cd "$AKOS_HOME" && tar -c --exclude='.git' --exclude='.akos-update.lock' . ) | ( cd "$BASELINE" && tar -x )
git -C "$BASELINE" init -q
git -C "$BASELINE" config user.email "test@test.com"
git -C "$BASELINE" config user.name "test"
git -C "$BASELINE" add -A
git -C "$BASELINE" commit -q -m "baseline: current working tree under test"
DEFAULT_BRANCH="$(git -C "$BASELINE" symbolic-ref --short HEAD)"

fresh_origin() {
  # Each case gets its OWN bare origin, freshly cloned from the pristine
  # $BASELINE — sharing one origin across cases would let one case's pushed
  # commit (e.g. deleting a personal-layer file) leak into every later
  # case's clone, contaminating scenarios that never touched that file.
  # mktemp for uniqueness, not an incrementing counter: this function is
  # invoked via command substitution, which forks a subshell — any counter
  # increment inside it is invisible to the caller, so every call would
  # otherwise compute the same "next" name and collide.
  local origin; origin="$(mktemp -u "$TMP/origin-XXXXXX").git"
  git clone --bare -q "$BASELINE" "$origin"
  echo "$origin"
}

new_clone() {
  # $1 = destination, $2 = origin. Fresh working clone.
  git clone -q "$2" "$1"
  git -C "$1" config user.email "test@test.com"
  git -C "$1" config user.name "test"
}

push_from_editor_copy() {
  # $1 = a scratch dir to clone into and mutate, $2 = mutate_fn, $3 = origin.
  local editor="$1" mutate_fn="$2" origin="$3"
  new_clone "$editor" "$origin"
  "$mutate_fn" "$editor"
  git -C "$editor" add -A
  git -C "$editor" commit -q -m "upstream test commit"
  git -C "$editor" push -q origin "HEAD:$DEFAULT_BRANCH"
}

# ============================================================
# Case 1: a real pull that MODIFIES a personal-layer file
# ============================================================
ORIGIN1="$(fresh_origin)"
CLONE1="$TMP/clone1"
new_clone "$CLONE1" "$ORIGIN1"
ORIGINAL_1="$(cat "$CLONE1/packs/personal/pau-avila/principles.md")"

_mutate_modify() { echo "UPSTREAM TAMPERED WITH THIS FILE" >> "$1/packs/personal/pau-avila/principles.md"; }
push_from_editor_copy "$TMP/editor1" _mutate_modify "$ORIGIN1"

OUT1="$TMP/out1"
rc=0
bash "$CLONE1/update.sh" >"$OUT1" 2>&1 || rc=$?
[ "$rc" -eq 0 ] || fail "expected exit 0 on successful pull + successful restore, got $rc: $(tail -25 "$OUT1")"
grep -q "personal layer drifted" "$OUT1" || fail "expected update.sh to detect the drift introduced by the pull"
grep -q "personal layer restored and verified" "$OUT1" || fail "expected a successful-restore message"
grep -q "Update complete and verified" "$OUT1" || fail "expected the final success message"
current_1="$(cat "$CLONE1/packs/personal/pau-avila/principles.md")"
[ "$current_1" = "$ORIGINAL_1" ] || fail "principles.md was not restored to its pre-pull content"
pass "update_restores_file_modified_by_pull"
pass "update_success_prints_verified_only_after_compare"

# ============================================================
# Case 2: a real pull that DELETES a personal-layer file, and a real pull
# that ADDS a new one — both must be reverted by the full-tree restore.
# ============================================================
ORIGIN2="$(fresh_origin)"
CLONE2="$TMP/clone2"
new_clone "$CLONE2" "$ORIGIN2"
[ -f "$CLONE2/packs/personal/pau-avila/design-language.md" ] || fail "fixture assumption failed: design-language.md should exist"

_mutate_nested() {
  rm "$1/packs/personal/pau-avila/design-language.md"
  echo "new upstream file" > "$1/packs/personal/pau-avila/new-upstream-file.md"
}
push_from_editor_copy "$TMP/editor2" _mutate_nested "$ORIGIN2"

OUT2="$TMP/out2"
rc=0
bash "$CLONE2/update.sh" >"$OUT2" 2>&1 || rc=$?
[ "$rc" -eq 0 ] || fail "expected exit 0, got $rc: $(tail -25 "$OUT2")"
[ -f "$CLONE2/packs/personal/pau-avila/design-language.md" ] \
  || fail "a file deleted by the pull must be restored"
[ ! -f "$CLONE2/packs/personal/pau-avila/new-upstream-file.md" ] \
  || fail "a file ADDED by the pull must be reverted too — the personal layer restores to the FULL pre-update snapshot, not a partial fill"
pass "update_restores_nested_new_and_removed_entries"

# ============================================================
# Case 3: an untracked symlink in the personal layer survives, unfollowed
# ============================================================
ORIGIN3="$(fresh_origin)"
CLONE3="$TMP/clone3"
new_clone "$CLONE3" "$ORIGIN3"
ln -s "/nonexistent-target-$$" "$CLONE3/packs/personal/pau-avila/my-link"

_mutate_noop_unrelated() { echo "irrelevant" >> "$1/README.md"; }
push_from_editor_copy "$TMP/editor3" _mutate_noop_unrelated "$ORIGIN3"

OUT3="$TMP/out3"
rc=0
bash "$CLONE3/update.sh" >"$OUT3" 2>&1 || rc=$?
[ "$rc" -eq 0 ] || fail "expected exit 0, got $rc: $(tail -25 "$OUT3")"
[ -L "$CLONE3/packs/personal/pau-avila/my-link" ] || fail "the symlink must survive as a symlink"
[ "$(readlink "$CLONE3/packs/personal/pau-avila/my-link")" = "/nonexistent-target-$$" ] \
  || fail "the symlink's target string must be preserved exactly, never followed or resolved"
pass "update_preserves_symlink_without_following_target"

# ============================================================
# Case 4: git pull failure (diverged/dirty tree) must return non-zero
# ============================================================
ORIGIN4="$(fresh_origin)"
CLONE4="$TMP/clone4"
new_clone "$CLONE4" "$ORIGIN4"
_mutate_diverge() { echo "diverges" >> "$1/README.md"; }
push_from_editor_copy "$TMP/editor4" _mutate_diverge "$ORIGIN4"
# Make CLONE4 diverge locally (a real, uncommitted local change) so
# --ff-only refuses.
echo "local uncommitted change" >> "$CLONE4/README.md"

OUT4="$TMP/out4"
rc=0
bash "$CLONE4/update.sh" >"$OUT4" 2>&1 || rc=$?
[ "$rc" -ne 0 ] || fail "expected non-zero exit when git pull fails"
grep -qi "git pull failed" "$OUT4" || fail "expected the git-pull-failed warning"
grep -q "did NOT complete" "$OUT4" || fail "expected the script to say it did not complete cleanly"
pass "update_pull_failure_returns_nonzero"

# ============================================================
# Case 5: not a git repository at all — must not claim "complete"
# ============================================================
CLONE5="$TMP/clone5-nogit"
cp -R "$AKOS_HOME" "$CLONE5"
rm -rf "$CLONE5/.git"
MARKER5="MARKER-$$"
echo "$MARKER5" >> "$CLONE5/packs/personal/pau-avila/principles.md"

OUT5="$TMP/out5"
# Snapshot existing backup dirs BEFORE this run — cases 1-4 already created
# their own under the same shared $HOME/.akos-backups, so "the first match"
# would pick up an earlier case's backup, not this one's. Diff, don't guess.
backups_before5="$(find "$HOME/.akos-backups" -maxdepth 1 -type d -name 'personal-*' 2>/dev/null | sort)"
bash "$CLONE5/update.sh" >"$OUT5" 2>&1 || true
grep -q "Not a git repository" "$OUT5" || fail "expected the no-git warning branch"
if grep -q "Update complete and verified" "$OUT5"; then
  fail "a non-git checkout must not claim 'Update complete and verified'"
fi
grep -q "$MARKER5" "$CLONE5/packs/personal/pau-avila/principles.md" \
  || fail "personal layer content was lost even in the no-git branch"
backups_after5="$(find "$HOME/.akos-backups" -maxdepth 1 -type d -name 'personal-*' 2>/dev/null | sort)"
backup_dir5="$(comm -13 <(echo "$backups_before5") <(echo "$backups_after5") | head -1)"
[ -n "$backup_dir5" ] || fail "no NEW durable backup was created under \$HOME/.akos-backups by this run"
grep -q "$MARKER5" "$backup_dir5/pau-avila/principles.md" \
  || fail "the durable backup does not contain the personal content"
pass "update_no_git_does_not_claim_complete"
pass "update_creates_verified_durable_backup"

# ============================================================
# Case 6: concurrent run is rejected — a held lock blocks a second run
# ============================================================
ORIGIN6="$(fresh_origin)"
CLONE6="$TMP/clone6"
new_clone "$CLONE6" "$ORIGIN6"
mkdir "$CLONE6/.akos-update.lock"
OUT6="$TMP/out6"
rc=0
bash "$CLONE6/update.sh" >"$OUT6" 2>&1 || rc=$?
rmdir "$CLONE6/.akos-update.lock"
[ "$rc" -ne 0 ] || fail "expected non-zero exit when the lock is already held"
grep -qi "already running" "$OUT6" || fail "expected the lock-held message"
pass "update_concurrent_run_is_rejected"

# ============================================================
# Case 7: restore failure — non-zero, and no false "preserved"/"restored"
# message. Uses AKOS_PYTHON_BIN to deterministically fail ONLY the
# `restore` subcommand of personal_layer_integrity.py, real python
# otherwise — no fragile fs-permission tricks, no dependency on not
# running as root.
# ============================================================
ORIGIN7="$(fresh_origin)"
CLONE7="$TMP/clone7"
new_clone "$CLONE7" "$ORIGIN7"
_mutate_modify7() { echo "drift again" >> "$1/packs/personal/pau-avila/principles.md"; }
push_from_editor_copy "$TMP/editor7" _mutate_modify7 "$ORIGIN7"

REAL_PYTHON="$(command -v python3)"
WRAPPER="$TMP/python3-restore-fails"
cat > "$WRAPPER" <<EOF
#!/usr/bin/env bash
is_restore=0
for arg in "\$@"; do
  case "\$arg" in
    *personal_layer_integrity.py) is_pli=1 ;;
    restore) [ "\${is_pli:-0}" = "1" ] && is_restore=1 ;;
  esac
done
if [ "\$is_restore" = "1" ]; then
  echo "error: simulated restore failure for test" >&2
  exit 1
fi
exec "$REAL_PYTHON" "\$@"
EOF
chmod +x "$WRAPPER"

OUT7="$TMP/out7"
rc=0
AKOS_PYTHON_BIN="$WRAPPER" bash "$CLONE7/update.sh" >"$OUT7" 2>&1 || rc=$?
[ "$rc" -ne 0 ] || fail "expected non-zero exit when restore fails"
grep -q "restore FAILED" "$OUT7" || fail "expected the restore-failure message"
if grep -q "personal layer restored and verified" "$OUT7"; then
  fail "must never print a success message when restore actually failed"
fi
if grep -q "Update complete and verified" "$OUT7"; then
  fail "must never claim overall completion when restore failed"
fi
pass "update_restore_failure_returns_nonzero"
pass "update_restore_failure_does_not_print_preserved"

# ============================================================
# Case 8: a broken tree makes the FINAL doctor.sh check fail — update.sh
# must reflect that in its own exit code, even though backup/pull/restore
# all succeeded on their own.
# ============================================================
ORIGIN8="$(fresh_origin)"
CLONE8="$TMP/clone8"
new_clone "$CLONE8" "$ORIGIN8"
rm "$CLONE8/core/constitution.md"  # local, uncommitted deletion — a no-op pull won't restore it

OUT8="$TMP/out8"
rc=0
bash "$CLONE8/update.sh" >"$OUT8" 2>&1 || rc=$?
[ "$rc" -ne 0 ] || fail "expected non-zero exit when the final doctor.sh check fails"
grep -q "doctor.sh reported failures" "$OUT8" || fail "expected update.sh to name the final doctor.sh failure"
pass "update_final_doctor_failure_is_nonzero"

echo "PASS: test_update_preserves_personal.sh"
