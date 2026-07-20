import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

import validate as v  # noqa: E402


PACK_SCHEMA = json.loads((paths.AKOS_HOME / "schemas/knowledge-pack.schema.json").read_text())


class TestValidateInstance(unittest.TestCase):
    def test_minimal_valid_pack_has_no_errors(self):
        data = {
            "name": "x", "domain": "y", "authority-level": 2, "version": "1.0.0",
            "tags": [], "sources": [{"title": "t", "url": "u"}], "related": [],
        }
        errors, warnings = v.validate_instance(data, PACK_SCHEMA)
        self.assertEqual(errors, [])
        # Recommended fields are absent -> warnings, not errors.
        self.assertTrue(warnings)

    def test_fully_populated_pack_has_no_warnings(self):
        data = {
            "name": "x", "domain": "y", "authority-level": 2, "version": "1.0.0",
            "tags": [], "sources": [{"title": "t", "url": "u"}], "related": [],
            "id": "y/x", "status": "stable", "last_reviewed": "2026-01-01",
            "review_after": "2027-01-01", "maintainer": "core",
        }
        errors, warnings = v.validate_instance(data, PACK_SCHEMA)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_missing_required_field_is_an_error(self):
        data = {"domain": "y", "authority-level": 2, "version": "1.0.0", "tags": [], "sources": [], "related": []}
        errors, _ = v.validate_instance(data, PACK_SCHEMA)
        fields = {e["field"] for e in errors}
        self.assertIn("name", fields)

    def test_bad_authority_level_type(self):
        data = {"name": "x", "domain": "y", "authority-level": "high", "version": "1.0.0",
                "tags": [], "sources": [], "related": []}
        errors, _ = v.validate_instance(data, PACK_SCHEMA)
        self.assertTrue(any(e["field"] == "authority-level" for e in errors))

    def test_bad_status_enum(self):
        data = {"name": "x", "domain": "y", "authority-level": 2, "version": "1.0.0",
                "tags": [], "sources": [], "related": [], "status": "not-a-status"}
        errors, _ = v.validate_instance(data, PACK_SCHEMA)
        self.assertTrue(any(e["field"] == "status" for e in errors))

    def test_bad_date_format(self):
        data = {"name": "x", "domain": "y", "authority-level": 2, "version": "1.0.0",
                "tags": [], "sources": [], "related": [], "last_reviewed": "2026-99-99"}
        errors, _ = v.validate_instance(data, PACK_SCHEMA)
        self.assertTrue(any(e["field"] == "last_reviewed" for e in errors))

    def test_bad_name_pattern(self):
        data = {"name": "Not Valid!", "domain": "y", "authority-level": 2, "version": "1.0.0",
                "tags": [], "sources": [], "related": []}
        errors, _ = v.validate_instance(data, PACK_SCHEMA)
        self.assertTrue(any(e["field"] == "name" for e in errors))

    def test_sources_missing_url(self):
        data = {"name": "x", "domain": "y", "authority-level": 2, "version": "1.0.0",
                "tags": [], "sources": [{"title": "only title"}], "related": []}
        errors, _ = v.validate_instance(data, PACK_SCHEMA)
        self.assertTrue(any("sources[0]" in e["field"] for e in errors))

    def test_source_with_org_instead_of_author_is_valid(self):
        # Real corpus fact: 3 packs use `org:` instead of `author:` in
        # sources — the schema deliberately doesn't require either.
        data = {"name": "x", "domain": "y", "authority-level": 2, "version": "1.0.0",
                "tags": [], "sources": [{"title": "t", "org": "W3C", "url": "u"}], "related": []}
        errors, _ = v.validate_instance(data, PACK_SCHEMA)
        self.assertEqual(errors, [])


class TestValidateRealRepo(unittest.TestCase):
    def test_all_packs_validate_clean(self):
        results = v.check_packs(PACK_SCHEMA)
        self.assertGreaterEqual(len(results), 40)
        errors = [e for r in results for e in r["errors"]]
        self.assertEqual(errors, [], f"unexpected schema errors in real packs: {errors}")

    def test_all_agents_validate_clean(self):
        schema = json.loads((paths.AKOS_HOME / "schemas/agent.schema.json").read_text())
        results = v.check_agents(schema)
        self.assertEqual(len(results), 13)
        errors = [e for r in results for e in r["errors"]]
        self.assertEqual(errors, [])

    def test_workflows_without_frontmatter_are_valid(self):
        schema = json.loads((paths.AKOS_HOME / "schemas/workflow.schema.json").read_text())
        results = v.check_workflows(schema)
        self.assertGreaterEqual(len(results), 9)
        errors = [e for r in results for e in r["errors"]]
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
