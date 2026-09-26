#!/usr/bin/env python3
import unittest
from vintage_boundary import audit


class VintageBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.data = {
            "name": "test",
            "revisions": [
                {"series": "x", "value": 1, "released_at": "2026-01-02T00:00:00Z"},
                {"series": "x", "value": 2, "released_at": "2026-03-02T00:00:00Z"},
                {"series": "y", "value": 9, "released_at": "2026-02-02T00:00:00Z"},
            ],
            "decisions": [
                {"origin": "2026-01-15T00:00:00Z"},
                {"origin": "2026-02-15T00:00:00Z"},
                {"origin": "2026-04-01T00:00:00Z"},
            ],
        }

    def test_future_releases_are_not_legal(self):
        report = audit(self.data)
        self.assertEqual(report["decisions"][0]["legal_values"], {"x": 1})
        self.assertEqual(report["decisions"][0]["future_series"], ["y"])
        self.assertEqual(report["decisions"][0]["revised_series"], ["x"])

    def test_late_origin_matches_latest(self):
        report = audit(self.data)
        self.assertFalse(report["decisions"][2]["leakage"])
        self.assertEqual(report["summary"]["decisions_affected_by_hindsight"], 2)


if __name__ == "__main__":
    unittest.main()
