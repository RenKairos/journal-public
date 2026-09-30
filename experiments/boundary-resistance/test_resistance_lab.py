import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).parent


class BoundaryResistanceTests(unittest.TestCase):
    def test_lab_exposes_endpoint_route_gap(self):
        with tempfile.TemporaryDirectory() as td:
            tmp_path = Path(td)
            out = tmp_path / "results.json"
            report = tmp_path / "report.md"
            p = subprocess.run(
                [sys.executable, str(HERE / "resistance_lab.py"), "--out", str(out), "--markdown", str(report)],
                capture_output=True, text=True,
            )
            self.assertEqual(p.returncode, 0, p.stderr)
            data = json.loads(out.read_text())
            by_name = {r["scenario"]: r for r in data["results"]}
            self.assertTrue(by_name["normal"]["endpoint_passed"] and by_name["normal"]["route_valid"])
            self.assertTrue(by_name["shortcut_dependency"]["endpoint_passed"])
            self.assertFalse(by_name["shortcut_dependency"]["route_valid"])
            self.assertIn("undeclared_dependency", by_name["shortcut_dependency"]["route_flags"])
            self.assertTrue(by_name["stale_endpoint"]["endpoint_passed"])
            self.assertFalse(by_name["stale_endpoint"]["route_valid"])
            self.assertIn("stale_answer", by_name["stale_endpoint"]["route_flags"])
            self.assertTrue(report.exists())
