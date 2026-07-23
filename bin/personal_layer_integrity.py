#!/usr/bin/env python3
"""Manifest-backed backup/verify/restore for AKOS's personal layer
(`packs/personal/`) — the operator's own Level-0 customization, which must
never silently change out from under them via `update.sh`, even from a
legitimate upstream commit to the shipped default profile.

Before this existed, `update.sh` backed up the personal layer with a plain
`cp -R`, and "restored" it with `cp -Rn ... || true` — a best-effort fill of
files that happened to be MISSING, with no verification the result actually
matched the pre-update snapshot, and no detection of a file that was merely
CHANGED rather than removed. A failed or partial restore printed the exact
same "personal layer preserved" as a real one.

Manifest format (manifest_version 1): a sorted list of every file/dir/symlink
under the tracked root, each with its path, type, POSIX mode (files/dirs
only), size and sha256 (files only), and symlink target STRING (symlinks
only — the target is hashed as text and never followed/resolved, so even a
dangling symlink round-trips and verifies).

Usage:
    python3 bin/personal_layer_integrity.py backup --source DIR --dest DIR
    python3 bin/personal_layer_integrity.py verify --manifest PATH --against DIR
    python3 bin/personal_layer_integrity.py restore --backup DIR --manifest PATH --dest DIR

Exit codes (this command's own 0/1/2 convention, per docs/cli/exit-codes.md):
    0 - backup/restore succeeded, or verify found no mismatch
    1 - usage/setup error, or backup/restore failed outright
    2 - verify found a missing or changed entry (added-only is not a failure)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

MANIFEST_VERSION = 1


class RestoreError(Exception):
    """A restore could not complete safely. The caller must NOT report
    success, and must preserve whatever backup/recovery paths still exist
    for manual inspection — never delete evidence on the way out."""


def _mode_str(p: Path) -> str:
    return format(p.stat().st_mode & 0o777, "o")


def _akos_version() -> str:
    version_path = Path(__file__).resolve().parent.parent / "VERSION"
    try:
        return version_path.read_text(encoding="utf-8").strip()
    except OSError:
        return ""


def build_manifest(root: Path) -> dict:
    """Walks `root` depth-first, sorted, never descending into a symlinked
    directory (followlinks=False) — a symlink itself is recorded as an
    entry, its target is never read as if it were part of this tree."""
    entries = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirpath_p = Path(dirpath)
        for name in sorted(dirnames) + sorted(filenames):
            p = dirpath_p / name
            rel = p.relative_to(root).as_posix()
            if p.is_symlink():
                target = os.readlink(p)
                entries.append({
                    "path": rel, "type": "symlink", "mode": None, "size": None,
                    "sha256": hashlib.sha256(target.encode("utf-8")).hexdigest(),
                    "symlink_target": target,
                })
            elif p.is_dir():
                entries.append({
                    "path": rel, "type": "dir", "mode": _mode_str(p),
                    "size": None, "sha256": None, "symlink_target": None,
                })
            else:
                data = p.read_bytes()
                entries.append({
                    "path": rel, "type": "file", "mode": _mode_str(p),
                    "size": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                    "symlink_target": None,
                })
    entries.sort(key=lambda e: e["path"])
    return {
        "manifest_version": MANIFEST_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "source": str(root),
        "akos_version": _akos_version(),
        "entries": entries,
    }


def diff_manifest(manifest: dict, against: Path) -> dict:
    """Recomputes a manifest for `against` and diffs against the stored one.
    `added` (present now, absent from the manifest) is never a failure —
    files created after the snapshot was taken are legitimate."""
    current = build_manifest(against)
    old_by_path = {e["path"]: e for e in manifest["entries"]}
    new_by_path = {e["path"]: e for e in current["entries"]}

    missing = sorted(set(old_by_path) - set(new_by_path))
    added = sorted(set(new_by_path) - set(old_by_path))
    changed = []
    for path in sorted(set(old_by_path) & set(new_by_path)):
        old, new = old_by_path[path], new_by_path[path]
        if (old["type"], old["sha256"], old.get("mode")) != (new["type"], new["sha256"], new.get("mode")):
            changed.append(path)
    return {"missing": missing, "changed": changed, "added": added}


def backup(source: Path, dest: Path) -> dict:
    """Copies `source` to `dest` (symlinks preserved, never followed), then
    builds the manifest from what was ACTUALLY WRITTEN at `dest` — not
    assumed from `source` — so a silently-truncated copy is caught by the
    caller's own immediate post-backup verify, not trusted blind."""
    if dest.exists():
        raise FileExistsError(f"backup destination already exists: {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, dest, symlinks=True)
    return build_manifest(dest)


def restore(backup_dir: Path, dest: Path, manifest: dict) -> None:
    """Full-tree staging + swap of `dest`, verified before AND after the
    swap. On any failure, the original `dest` (if moved aside) and the
    staging/recovery directories are preserved — never silently cleaned up —
    so the exact paths remain available for manual recovery."""
    parent = dest.parent
    parent.mkdir(parents=True, exist_ok=True)

    staging = Path(tempfile.mkdtemp(dir=parent, prefix=f".{dest.name}.staging-"))
    staging.rmdir()  # copytree requires the destination not exist yet
    try:
        shutil.copytree(backup_dir, staging, symlinks=True)
    except OSError as e:
        shutil.rmtree(staging, ignore_errors=True)
        raise RestoreError(f"failed to stage backup copy from {backup_dir}: {e}") from e

    staging_diff = diff_manifest(manifest, staging)
    if staging_diff["missing"] or staging_diff["changed"]:
        shutil.rmtree(staging, ignore_errors=True)
        raise RestoreError(
            f"staged copy of {backup_dir} does not match its own manifest before swap "
            f"(missing={staging_diff['missing']}, changed={staging_diff['changed']}) — "
            f"the backup itself may be corrupt; dest was not touched"
        )

    recovery = Path(tempfile.mkdtemp(dir=parent, prefix=f".{dest.name}.recovery-"))
    recovery.rmdir()
    moved_dest_aside = False
    try:
        if dest.exists():
            os.replace(dest, recovery)
            moved_dest_aside = True
        os.replace(staging, dest)
    except OSError as e:
        if moved_dest_aside and not dest.exists():
            os.replace(recovery, dest)  # best-effort: put the original back
        else:
            shutil.rmtree(staging, ignore_errors=True)
        raise RestoreError(f"failed to publish the restored tree to {dest}: {e}") from e

    final_diff = diff_manifest(manifest, dest)
    if final_diff["missing"] or final_diff["changed"]:
        raise RestoreError(
            f"restored tree at {dest} does not match the manifest after swap "
            f"(missing={final_diff['missing']}, changed={final_diff['changed']}) — "
            f"dest left as published, previous content preserved at {recovery} for manual recovery"
        )

    if recovery.exists():
        shutil.rmtree(recovery, ignore_errors=True)


# --- CLI ----------------------------------------------------------------------


def cmd_backup(args) -> int:
    source, dest = Path(args.source), Path(args.dest)
    if not source.is_dir():
        print(f"error: --source {source} is not a directory", file=sys.stderr)
        return 1
    try:
        manifest = backup(source, dest)
    except (FileExistsError, OSError) as e:
        print(f"error: backup failed: {e}", file=sys.stderr)
        return 1
    manifest_path = dest.parent / f"{dest.name}.manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"backed up {source} to {dest}")
    print(f"manifest: {manifest_path} ({len(manifest['entries'])} entries)")
    return 0


def cmd_verify(args) -> int:
    manifest_path, against = Path(args.manifest), Path(args.against)
    if not manifest_path.is_file():
        print(f"error: --manifest {manifest_path} not found", file=sys.stderr)
        return 1
    if not against.is_dir():
        print(f"error: --against {against} is not a directory", file=sys.stderr)
        return 1
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"error: could not read manifest: {e}", file=sys.stderr)
        return 1
    if manifest.get("manifest_version") != MANIFEST_VERSION:
        print(f"error: unknown manifest_version {manifest.get('manifest_version')!r} "
              f"(expected {MANIFEST_VERSION})", file=sys.stderr)
        return 1

    diff = diff_manifest(manifest, against)
    if diff["missing"] or diff["changed"]:
        for p in diff["missing"]:
            print(f"\033[31m✗\033[0m missing: {p}")
        for p in diff["changed"]:
            print(f"\033[31m✗\033[0m changed: {p}")
        for p in diff["added"]:
            print(f"  added (fine): {p}")
        return 2
    print(f"\033[32m✓\033[0m {against} matches the manifest ({len(diff['added'])} new file(s) since, if any)")
    return 0


def cmd_restore(args) -> int:
    backup_dir, manifest_path, dest = Path(args.backup), Path(args.manifest), Path(args.dest)
    if not backup_dir.is_dir():
        print(f"error: --backup {backup_dir} is not a directory", file=sys.stderr)
        return 1
    if not manifest_path.is_file():
        print(f"error: --manifest {manifest_path} not found", file=sys.stderr)
        return 1
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"error: could not read manifest: {e}", file=sys.stderr)
        return 1
    if manifest.get("manifest_version") != MANIFEST_VERSION:
        print(f"error: unknown manifest_version {manifest.get('manifest_version')!r} "
              f"(expected {MANIFEST_VERSION})", file=sys.stderr)
        return 1

    try:
        restore(backup_dir, dest, manifest)
    except RestoreError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(f"restored {dest} from {backup_dir}, verified against {manifest_path}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_backup = sub.add_parser("backup")
    p_backup.add_argument("--source", required=True)
    p_backup.add_argument("--dest", required=True)

    p_verify = sub.add_parser("verify")
    p_verify.add_argument("--manifest", required=True)
    p_verify.add_argument("--against", required=True)

    p_restore = sub.add_parser("restore")
    p_restore.add_argument("--backup", required=True)
    p_restore.add_argument("--manifest", required=True)
    p_restore.add_argument("--dest", required=True)

    args = ap.parse_args(argv)
    return {"backup": cmd_backup, "verify": cmd_verify, "restore": cmd_restore}[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
