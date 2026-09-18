import unittest
from route_substitution import audit, fixture

class RouteSubstitutionTests(unittest.TestCase):
    def test_baseline_is_valid(self):
        report = audit(fixture())
        self.assertTrue(report["rows"][0]["answer_correct"])
        self.assertTrue(report["rows"][0]["route_valid"])

    def test_plausible_wrong_evidence_is_detected(self):
        row = next(r for r in audit(fixture())["rows"] if r["name"] == "plausible_wrong_evidence")
        self.assertTrue(row["answer_correct"])
        self.assertFalse(row["route_valid"])
        self.assertFalse(row["hinges"]["evidence"])

    def test_counterfeit_rate_is_not_hidden_by_endpoint_accuracy(self):
        summary = audit(fixture())["summary"]
        self.assertEqual(summary["counterfeit_continuity"], 5)
        self.assertGreater(summary["answer_accuracy_under_attack"], summary["route_validity_under_attack"])

if __name__ == "__main__":
    unittest.main()
