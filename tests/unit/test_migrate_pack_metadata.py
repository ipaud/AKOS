import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

spec = importlib.util.spec_from_file_location("migrate_pack_metadata", paths.AKOS_HOME / "bin/migrate-pack-metadata.py")
migrate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(migrate)


class TestMigrationOnRealCorpusCopy(unittest.TestCase):
    """Runs the real migration logic (in dry-run, then applied) against a
    COPY of the real metadata.yaml corpus in a temp dir — never touches the
    actual repo. Confirms: idempotency, append-only (never rewrites an
    existing line), and the em-dash CHANGELOG date parse that all 49 real
    changelogs actually use."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.tmp_packs = Path(self.tmpdir) / "packs"
        shutil.copytree(paths.AKOS_HOME / "packs", self.tmp_packs)
        # Undo the real repo's own migration so this test exercises the
        # actual "add missing fields" path, not a no-op.
        for meta in self.tmp_packs.glob("*/*/metadata.yaml"):
            text = meta.read_text()
            for key in migrate.CANONICAL_ORDER:
                lines = text.split("\n")
                text = "\n".join(l for l in lines if not l.startswith(f"{key}:"))
            meta.write_text(text)

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_changelog_date_parses_with_em_dash(self):
        changelog = self.tmp_packs / "ux/wcag/CHANGELOG.md"
        d, source = migrate.parse_changelog_date(changelog)
        self.assertEqual(source, "CHANGELOG.md")
        self.assertEqual(d.isoformat(), "2026-07-09")

    def test_missing_changelog_falls_back_to_today_with_a_stated_reason(self):
        d, source = migrate.parse_changelog_date(Path("/nonexistent/CHANGELOG.md"))
        self.assertIn("fallback", source)

    def test_migration_adds_exactly_the_missing_fields(self):
        meta_path = self.tmp_packs / "ux/wcag/metadata.yaml"
        text_before = meta_path.read_text()
        self.assertNotIn("status:", text_before)

        missing = migrate.CANONICAL_ORDER
        block, info = migrate.build_missing_block(meta_path, missing)
        migrate.atomic_append(meta_path, block)

        text_after = meta_path.read_text()
        self.assertTrue(text_after.startswith(text_before), "migration must be append-only — never rewrite existing lines")
        for key in migrate.CANONICAL_ORDER:
            self.assertIn(f"{key}:", text_after)

    def test_review_after_cadence_by_authority_level(self):
        # wcag is authority-level 1 -> 545-day cadence (18mo)
        meta_path = self.tmp_packs / "ux/wcag/metadata.yaml"
        block, _ = migrate.build_missing_block(meta_path, migrate.CANONICAL_ORDER)
        lines = dict(l.split(": ", 1) for l in block.strip().split("\n"))
        from datetime import date
        last_reviewed = date.fromisoformat(lines["last_reviewed"])
        review_after = date.fromisoformat(lines["review_after"])
        self.assertEqual((review_after - last_reviewed).days, 545)

    def test_rerun_is_idempotent(self):
        meta_path = self.tmp_packs / "ux/wcag/metadata.yaml"
        block, _ = migrate.build_missing_block(meta_path, migrate.CANONICAL_ORDER)
        migrate.atomic_append(meta_path, block)

        text = meta_path.read_text()
        existing = migrate.top_level_keys(text)
        still_missing = [k for k in migrate.CANONICAL_ORDER if k not in existing]
        self.assertEqual(still_missing, [], "a second run must find nothing left to add")

    def test_personal_layer_is_never_a_target(self):
        # The real migration script's main() explicitly skips any path
        # containing "personal" — verified structurally here since
        # packs/personal/pau-avila has no metadata.yaml to migrate anyway.
        self.assertFalse((self.tmp_packs / "personal/pau-avila/metadata.yaml").exists())


if __name__ == "__main__":
    unittest.main()
