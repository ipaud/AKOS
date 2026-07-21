#!/usr/bin/env bash
# install.sh writes 17+ symlinks into $HOME. Runs the REAL script against a
# scratch COPY of the repo with HOME pointed at a scratch directory, so the
# no-clobber guards — the branches that decide whether a user's real files
# survive — actually execute. Before this test existed, none of them ever had.
set -euo pipefail

AKOS_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

pass() { printf '  ok - %s\n' "$1"; }
fail() { printf '  FAIL - %s\n' "$1"; exit 1; }

cp -R "$AKOS_HOME" "$TMP/akos-copy"
COPY="$TMP/akos-copy"
export HOME="$TMP/home"
mkdir -p "$HOME"

# 1. Fresh install creates the expected symlinks.
bash "$COPY/install.sh" >"$TMP/out1" 2>&1 || fail "install.sh exited non-zero on a fresh HOME: $(tail -3 "$TMP/out1")"
[ "$(readlink "$HOME/bin/akos")" = "$COPY/bin/akos" ] || fail "~/bin/akos does not point at the installed copy"
[ "$(readlink "$HOME/.claude/skills/akos")" = "$COPY/skills/akos" ] || fail "Claude skill 'akos' not linked"
[ "$(readlink "$HOME/.agents/skills/akos-review")" = "$COPY/skills/akos-review" ] || fail "Codex skill 'akos-review' not linked"
agent_links="$(find "$HOME/.claude/agents" -type l -name 'akos-*.md' | wc -l | tr -d ' ')"
agent_srcs="$(find "$COPY/agents" -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')"
[ "$agent_links" = "$agent_srcs" ] || fail "expected $agent_srcs agent symlinks, found $agent_links"
pass "fresh install creates bin, skill and $agent_links agent symlinks"

# 2. Idempotent: a second run changes nothing.
bash "$COPY/install.sh" >"$TMP/out2" 2>&1 || fail "second install.sh run exited non-zero"
agent_links2="$(find "$HOME/.claude/agents" -type l -name 'akos-*.md' | wc -l | tr -d ' ')"
[ "$agent_links2" = "$agent_links" ] || fail "second run changed the agent link count ($agent_links -> $agent_links2)"
[ "$(readlink "$HOME/bin/akos")" = "$COPY/bin/akos" ] || fail "second run broke ~/bin/akos"
pass "install.sh is idempotent"

# 3. No-clobber: a REAL directory at a skill destination survives untouched.
rm "$HOME/.claude/skills/akos"
mkdir -p "$HOME/.claude/skills/akos"
echo "user content" > "$HOME/.claude/skills/akos/SKILL.md"
bash "$COPY/install.sh" >"$TMP/out3" 2>&1 || fail "install.sh exited non-zero with a real dir at a skill dest"
[ ! -L "$HOME/.claude/skills/akos" ] || fail "install.sh replaced a user's real directory with a symlink"
grep -q "user content" "$HOME/.claude/skills/akos/SKILL.md" || fail "user's file inside the real directory was lost"
grep -q "leaving it untouched" "$TMP/out3" || fail "expected the no-clobber warning in the output"
pass "a real directory at a skill destination survives with a warning"

# 4. No-clobber: a REAL file at an agent destination survives untouched.
first_agent="$(find "$COPY/agents" -maxdepth 1 -name '*.md' | head -1)"
agent_dest="$HOME/.claude/agents/akos-$(basename "$first_agent")"
rm "$agent_dest"
echo "user agent" > "$agent_dest"
bash "$COPY/install.sh" >"$TMP/out4" 2>&1 || fail "install.sh exited non-zero with a real file at an agent dest"
[ ! -L "$agent_dest" ] || fail "install.sh replaced a user's real agent file with a symlink"
grep -q "user agent" "$agent_dest" || fail "user's real agent file was overwritten"
pass "a real file at an agent destination survives"

# 5. A pre-existing real ~/DEV directory is left alone (no symlink through it).
#    (In this scratch HOME, ~/DEV was created as a real dir by nothing — make one.)
rm -rf "$HOME/DEV"
mkdir -p "$HOME/DEV"
bash "$COPY/install.sh" >"$TMP/out5" 2>&1 || fail "install.sh exited non-zero with a real ~/DEV"
[ ! -L "$HOME/DEV" ] || fail "install.sh replaced a real ~/DEV directory with a symlink"
pass "a real ~/DEV directory is left untouched"

echo "PASS: test_install_isolated.sh"
