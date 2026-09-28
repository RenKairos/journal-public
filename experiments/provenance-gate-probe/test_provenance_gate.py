import unittest

from provenance_gate import aggregate, run_one


class ProvenanceGateTests(unittest.TestCase):
    def test_deterministic_seed(self):
        self.assertEqual(run_one(3, 0.85, 80), run_one(3, 0.85, 80))

    def test_policies_exist_and_are_bounded(self):
        result = aggregate(seeds=3, threshold=0.85, steps=120)
        self.assertEqual(set(result["policies"]), {"oracle", "forced", "quarantine"})
        for metrics in result["policies"].values():
            for key in ("clean_accuracy", "ambiguous_accuracy", "contamination_rate", "abstain_rate"):
                self.assertGreaterEqual(metrics[key], 0.0)
                self.assertLessEqual(metrics[key], 1.0)


if __name__ == "__main__":
    unittest.main()
