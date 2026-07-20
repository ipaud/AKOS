import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "helpers"))
import paths  # noqa: F401,E402

import freshness  # noqa: E402


class TestBandBoundaries(unittest.TestCase):
    """Exact boundary conditions — this is where the real --fail-on severity
    inversion bug lived (M7), so the boundaries themselves get direct
    coverage, not just a couple of representative dates."""

    def setUp(self):
        self.today = date(2026, 7, 20)

    def test_no_review_after_is_unknown(self):
        band, days = freshness.band_for(None, self.today)
        self.assertEqual(band, "unknown")
        self.assertIsNone(days)

    def test_unparseable_date_is_unknown(self):
        band, _ = freshness.band_for("not-a-date", self.today)
        self.assertEqual(band, "unknown")

    def test_one_day_past_is_expired(self):
        d = (self.today - timedelta(days=1)).isoformat()
        band, days = freshness.band_for(d, self.today)
        self.assertEqual(band, "expired")
        self.assertEqual(days, -1)

    def test_exactly_today_is_review_due(self):
        band, _ = freshness.band_for(self.today.isoformat(), self.today)
        self.assertEqual(band, "review-due")

    def test_exactly_30_days_out_is_review_due(self):
        d = (self.today + timedelta(days=30)).isoformat()
        band, _ = freshness.band_for(d, self.today)
        self.assertEqual(band, "review-due")

    def test_31_days_out_is_review_due_soon(self):
        d = (self.today + timedelta(days=31)).isoformat()
        band, _ = freshness.band_for(d, self.today)
        self.assertEqual(band, "review-due-soon")

    def test_exactly_90_days_out_is_review_due_soon(self):
        d = (self.today + timedelta(days=90)).isoformat()
        band, _ = freshness.band_for(d, self.today)
        self.assertEqual(band, "review-due-soon")

    def test_91_days_out_is_fresh(self):
        d = (self.today + timedelta(days=91)).isoformat()
        band, _ = freshness.band_for(d, self.today)
        self.assertEqual(band, "fresh")


class TestFailOnSeverityDirection(unittest.TestCase):
    """The exact bug M7 found: --fail-on's severity comparison was inverted,
    so `--fail-on expired` matched everything except unknown. Locking the
    correct direction down explicitly so it can't silently flip back."""

    def test_severity_order_worst_to_best(self):
        self.assertLess(freshness.BAND_SEVERITY["fresh"], freshness.BAND_SEVERITY["review-due-soon"])
        self.assertLess(freshness.BAND_SEVERITY["review-due-soon"], freshness.BAND_SEVERITY["review-due"])
        self.assertLess(freshness.BAND_SEVERITY["review-due"], freshness.BAND_SEVERITY["expired"])
        self.assertLess(freshness.BAND_SEVERITY["expired"], freshness.BAND_SEVERITY["unknown"])

    def test_fail_on_expired_does_not_match_fresh(self):
        rows = [{"pack": "x", "band": "fresh", "review_after": "2099-01-01", "days": 9999}]
        threshold = freshness.BAND_SEVERITY["expired"]
        matched = any(freshness.BAND_SEVERITY[r["band"]] >= threshold for r in rows)
        self.assertFalse(matched, "an all-fresh corpus must not trigger --fail-on expired")

    def test_fail_on_expired_matches_expired(self):
        rows = [{"pack": "x", "band": "expired", "review_after": "2020-01-01", "days": -2000}]
        threshold = freshness.BAND_SEVERITY["expired"]
        matched = any(freshness.BAND_SEVERITY[r["band"]] >= threshold for r in rows)
        self.assertTrue(matched)


class TestRealRepoAllFresh(unittest.TestCase):
    def test_no_pack_is_currently_expired(self):
        rows = freshness.collect(None)
        self.assertGreaterEqual(len(rows), 40)
        expired = [r for r in rows if r["band"] == "expired"]
        self.assertEqual(expired, [], f"unexpected expired packs: {expired}")


if __name__ == "__main__":
    unittest.main()


class TestUnmatchedPackFilterIsAnError(unittest.TestCase):
    """`--pack no/such --fail-on expired` used to exit 0: collect() returned
    an empty list, no row was at the failing band, and the gate passed. A
    typo in a CI invocation therefore produced a check that could never
    fire. An unmatched filter must fail, not report clean."""

    def test_unmatched_pack_exits_1(self):
        self.assertEqual(freshness.main(["--pack", "no/such-pack"]), 1)

    def test_unmatched_pack_with_fail_on_does_not_pass_silently(self):
        self.assertNotEqual(freshness.main(["--pack", "no/such", "--fail-on", "expired"]), 0)

    def test_real_pack_still_works(self):
        self.assertEqual(freshness.main(["--pack", "ux/wcag"]), 0)
