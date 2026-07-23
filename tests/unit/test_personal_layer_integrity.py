import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

import personal_layer_integrity as pli  # noqa: E402


class TestManifest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "tree"
        self.root.mkdir()
        (self.root / "sub").mkdir()
        (self.root / "a.txt").write_text("hello")
        (self.root / "sub" / "b.txt").write_text("world")

    def tearDown(self):
        self._tmp.cleanup()

    def test_manifest_is_deterministic(self):
        m1 = pli.build_manifest(self.root)
        m2 = pli.build_manifest(self.root)
        self.assertEqual(m1["entries"], m2["entries"])
        paths_in_order = [e["path"] for e in m1["entries"]]
        self.assertEqual(paths_in_order, sorted(paths_in_order))

    def test_manifest_detects_modified_file(self):
        manifest = pli.build_manifest(self.root)
        (self.root / "a.txt").write_text("changed")
        diff = pli.diff_manifest(manifest, self.root)
        self.assertEqual(diff["changed"], ["a.txt"])
        self.assertEqual(diff["missing"], [])

    def test_manifest_detects_missing_file(self):
        manifest = pli.build_manifest(self.root)
        (self.root / "sub" / "b.txt").unlink()
        diff = pli.diff_manifest(manifest, self.root)
        self.assertEqual(diff["missing"], ["sub/b.txt"])

    def test_manifest_detects_extra_file(self):
        manifest = pli.build_manifest(self.root)
        (self.root / "c.txt").write_text("new")
        diff = pli.diff_manifest(manifest, self.root)
        self.assertEqual(diff["added"], ["c.txt"])
        # An added file is never a failure signal on its own.
        self.assertEqual(diff["missing"], [])
        self.assertEqual(diff["changed"], [])

    def test_manifest_detects_changed_symlink_target(self):
        link = self.root / "link"
        os.symlink("/original/target", link)
        manifest = pli.build_manifest(self.root)
        link.unlink()
        os.symlink("/different/target", link)
        diff = pli.diff_manifest(manifest, self.root)
        self.assertIn("link", diff["changed"])

    def test_manifest_does_not_follow_external_symlink(self):
        # A symlink pointing OUTSIDE the tree, even to a real directory with
        # real content, must be recorded as a symlink entry (hashing its
        # target string) — never traversed into and never read as if its
        # target's content were part of this tree.
        external = Path(self._tmp.name) / "external"
        external.mkdir()
        (external / "secret.txt").write_text("should never be read")
        os.symlink(str(external), self.root / "link-to-external")

        manifest = pli.build_manifest(self.root)
        entry = next(e for e in manifest["entries"] if e["path"] == "link-to-external")
        self.assertEqual(entry["type"], "symlink")
        self.assertEqual(entry["symlink_target"], str(external))
        paths_seen = {e["path"] for e in manifest["entries"]}
        self.assertNotIn("link-to-external/secret.txt", paths_seen)

    def test_manifest_handles_dangling_symlink(self):
        os.symlink("/nonexistent/nowhere", self.root / "dangling")
        manifest = pli.build_manifest(self.root)  # must not raise
        entry = next(e for e in manifest["entries"] if e["path"] == "dangling")
        self.assertEqual(entry["symlink_target"], "/nonexistent/nowhere")
        diff = pli.diff_manifest(manifest, self.root)
        self.assertEqual(diff["changed"], [])
        self.assertEqual(diff["missing"], [])


class TestBackupAndVerify(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.source = Path(self._tmp.name) / "source"
        self.source.mkdir()
        (self.source / "principles.md").write_text("my principles")
        self.dest = Path(self._tmp.name) / "backups" / "snap"

    def tearDown(self):
        self._tmp.cleanup()

    def test_backup_is_verified_before_publish(self):
        # The realistic caller sequence: backup(), then immediately diff the
        # result against its own manifest — this must be clean for a real
        # copy, and must be exactly what would catch a silently-truncated one.
        manifest = pli.backup(self.source, self.dest)
        diff = pli.diff_manifest(manifest, self.dest)
        self.assertEqual(diff["missing"], [])
        self.assertEqual(diff["changed"], [])

    def test_backup_refuses_to_overwrite_existing_destination(self):
        self.dest.mkdir(parents=True)
        with self.assertRaises(FileExistsError):
            pli.backup(self.source, self.dest)

    def test_backup_failure_leaves_no_false_success_state(self):
        with mock.patch.object(pli.shutil, "copytree", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                pli.backup(self.source, self.dest)
        self.assertFalse(self.dest.exists(), "a failed backup must not leave a partial destination behind")


class TestRestore(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.backup_dir = Path(self._tmp.name) / "backup"
        self.backup_dir.mkdir()
        (self.backup_dir / "principles.md").write_text("original content")
        self.manifest = pli.build_manifest(self.backup_dir)
        self.dest = Path(self._tmp.name) / "personal"
        self.dest.mkdir()
        (self.dest / "principles.md").write_text("corrupted content")

    def tearDown(self):
        self._tmp.cleanup()

    def test_successful_restore_matches_manifest(self):
        pli.restore(self.backup_dir, self.dest, self.manifest)
        self.assertEqual((self.dest / "principles.md").read_text(), "original content")
        diff = pli.diff_manifest(self.manifest, self.dest)
        self.assertEqual(diff["missing"], [])
        self.assertEqual(diff["changed"], [])

    def test_restore_staging_is_verified_before_swap(self):
        # If the staged copy of the backup doesn't match the manifest, the
        # live `dest` must be left completely untouched — the corruption is
        # in the backup, not something a swap should ever propagate.
        original = (self.dest / "principles.md").read_text()
        real_copytree = pli.shutil.copytree

        def corrupt_first_copy(src, dst, **kwargs):
            real_copytree(src, dst, **kwargs)
            (Path(dst) / "principles.md").write_text("corrupted during staging")

        with mock.patch.object(pli.shutil, "copytree", side_effect=corrupt_first_copy):
            with self.assertRaises(pli.RestoreError):
                pli.restore(self.backup_dir, self.dest, self.manifest)
        self.assertEqual((self.dest / "principles.md").read_text(), original,
                         "dest must be untouched when the staged copy fails its own manifest check")

    def test_restore_failure_rolls_back_or_preserves_recovery(self):
        original = (self.dest / "principles.md").read_text()
        with mock.patch.object(pli.os, "replace", side_effect=OSError("permission denied")):
            with self.assertRaises(pli.RestoreError):
                pli.restore(self.backup_dir, self.dest, self.manifest)
        # Either dest still exists with its original content (rolled back),
        # or it's gone but recoverable — never silently empty/missing with
        # no trace and never silently "succeeded".
        self.assertTrue(self.dest.exists(), "dest must not vanish with no recovery trace")
        self.assertEqual((self.dest / "principles.md").read_text(), original)

    def test_failed_operation_leaves_no_false_success_state(self):
        with mock.patch.object(pli.os, "replace", side_effect=OSError("boom")):
            with self.assertRaises(pli.RestoreError) as cm:
                pli.restore(self.backup_dir, self.dest, self.manifest)
        # The exception message must be informative enough to act on — not
        # a bare "failed" with no path to recover from.
        self.assertIn(str(self.dest), str(cm.exception))


class TestCLI(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_cli_backup_then_verify_then_restore_round_trip(self):
        source = self.root / "source"
        source.mkdir()
        (source / "f.md").write_text("v1")
        dest = self.root / "backups" / "snap1"

        rc = pli.main(["backup", "--source", str(source), "--dest", str(dest)])
        self.assertEqual(rc, 0)
        manifest_path = dest.parent / "snap1.manifest.json"
        self.assertTrue(manifest_path.is_file())

        rc = pli.main(["verify", "--manifest", str(manifest_path), "--against", str(source)])
        self.assertEqual(rc, 0)

        (source / "f.md").write_text("v2 — corrupted")
        rc = pli.main(["verify", "--manifest", str(manifest_path), "--against", str(source)])
        self.assertEqual(rc, 2)

        rc = pli.main(["restore", "--backup", str(dest), "--manifest", str(manifest_path), "--dest", str(source)])
        self.assertEqual(rc, 0)
        self.assertEqual((source / "f.md").read_text(), "v1")

    def test_cli_verify_unknown_manifest_version_is_error(self):
        against = self.root / "dir"
        against.mkdir()
        manifest_path = self.root / "bad.manifest.json"
        manifest_path.write_text(json.dumps({"manifest_version": 99, "entries": []}))
        rc = pli.main(["verify", "--manifest", str(manifest_path), "--against", str(against)])
        self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
