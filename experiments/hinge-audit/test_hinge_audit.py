import datetime as dt
import unittest
from hinge_audit import assess, audit

class HingeAuditTests(unittest.TestCase):
    def setUp(self):
        self.decision = {
            "id": "x", "answer": "hold", "authorized": True,
            "required_evidence": ["e"], "route": ["e"],
            "evidence": [{"id": "e", "observed": True, "expires_at": "2026-09-20"}],
        }

    def test_baseline_passes(self):
        result = assess(self.decision, today=dt.date(2026, 9, 14))
        self.assertTrue(result["route_valid"])

    def test_removed_evidence_breaks_route_not_answer(self):
        result = assess(self.decision, today=dt.date(2026, 9, 14), removed="e")
        self.assertFalse(result["route_valid"])
        self.assertTrue(result["answer_present"])

    def test_expiry_breaks_freshness(self):
        result = assess(self.decision, today=dt.date(2026, 9, 21))
        self.assertFalse(result["hinges"]["freshness"])
        self.assertFalse(result["route_valid"])

    def test_audit_has_one_attack_per_hinge_type(self):
        result = audit(self.decision, dt.date(2026, 9, 14))
        self.assertEqual(result["summary"]["attack_count"], 2)
        self.assertEqual(result["summary"]["route_failures"], 2)

if __name__ == "__main__":
    unittest.main()
