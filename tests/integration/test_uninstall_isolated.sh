#!/usr/bin/env bash
# uninstall.sh ends in `rm -rf "$AKOS_HOME"` behind a typed confirmation.
# Runs the REAL script against a scratch COPY with a scratch HOME, covering
# the branches that decide whether user data survives: foreign files left
# alone, declining keeps everything, confirming backs up BEFORE deleting,
# and — the data-loss bug this file exists to lock down — a failed backup
# must ABORT, not print "preserved" and delete anyway.
set -euo pipefail

AKOS_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TMP="$(mktemp -d)"
trap 'chmod -R +w "$TMP" 2>/dev/null || true; rm -rf "$TMP"' EXIT

pass() { printf '  ok - %s\n' "$1"; }
fail() { printf '  FAIL - %s\n' "$1"; exit 1; }

fresh_copy() {
  rm -rf "$TMP/akos-copy" "$TMP/home"
  cp -R "$AKOS_HOME" "$TMP/akos-copy"
  rm -rf "$TMP/akos-copy/.git"
  export HOME="$TMP/home"
  mkdir -p "$HOME"
}

# 1. A foreign ~/bin/akos (regular file, not our symlink) survives.
fresh_copy
mkdir -p "$HOME/bin"
echo "someone else's script" > "$HOME/bin/akos"
printf '' | bash "$TMP/akos-copy/uninstall.sh" >"$TMP/out1" 2>&1 || fail "uninstall exited non-zero: $(tail -3 "$TMP/out1")"
grep -q "someone else's script" "$HOME/bin/akos" || fail "a foreign ~/bin/akos regular file was removed"
pass "foreign ~/bin/akos regular file survives"

# 2. A skill symlink pointing somewhere ELSE survives (readlink guard).
fresh_copy
mkdir -p "$HOME/.claude/skills" "$TMP/elsewhere"
ln -s "$TMP/elsewhere" "$HOME/.claude/skills/akos"
printf '' | bash "$TMP/akos-copy/uninstall.sh" >"$TMP/out2" 2>&1 || fail "uninstall exited non-zero"
[ -L "$HOME/.claude/skills/akos" ] || fail "a foreign skill symlink was removed"
pass "foreign skill symlink survives"

# 3. Declining deletion (empty stdin) keeps all content.
fresh_copy
printf '' | bash "$TMP/akos-copy/uninstall.sh" >"$TMP/out3" 2>&1 || fail "uninstall exited non-zero"
[ -f "$TMP/akos-copy/VERSION" ] || fail "declining deletion still removed content"
grep -q "Nothing deleted" "$TMP/out3" || fail "expected the 'Nothing deleted' confirmation"
pass "declining deletion keeps everything"

# 4. Typed confirmation backs up ALL of packs/ (not just personal/) before deleting.
fresh_copy
mkdir -p "$TMP/akos-copy/packs/ux/my-own-pack"
echo "user-authored" > "$TMP/akos-copy/packs/ux/my-own-pack/README.md"
printf 'DELETE AKOS\n' | bash "$TMP/akos-copy/uninstall.sh" >"$TMP/out4" 2>&1 || fail "confirmed uninstall exited non-zero: $(tail -3 "$TMP/out4")"
[ ! -d "$TMP/akos-copy" ] || fail "content was not deleted after typed confirmation"
backup="$(find "$HOME" -maxdepth 1 -type d -name 'akos-packs-backup-*' | head -1)"
[ -n "$backup" ] || fail "no backup directory was created before deletion"
[ -f "$backup/personal/pau-avila/principles.md" ] || fail "personal layer missing from the backup"
grep -q "user-authored" "$backup/ux/my-own-pack/README.md" || fail "a user-authored non-personal pack missing from the backup"
pass "typed confirmation backs up all of packs/ before deleting"

# 5. When the backup cannot be written, deletion ABORTS and content survives.
fresh_copy
chmod -w "$HOME"
set +e
printf 'DELETE AKOS\n' | bash "$TMP/akos-copy/uninstall.sh" >"$TMP/out5" 2>&1
rc=$?
set -e
chmod +w "$HOME"
[ "$rc" -ne 0 ] || fail "uninstall exited 0 even though the backup could not be written"
[ -f "$TMP/akos-copy/VERSION" ] || fail "content was deleted despite the backup failing — the data-loss bug is back"
grep -q "aborting" "$TMP/out5" || fail "expected an explicit abort message when the backup fails"
pass "failed backup aborts the deletion — nothing lost"

echo "PASS: test_uninstall_isolated.sh"
