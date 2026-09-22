#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).parent
source = (root / "source.md").read_text()
report = (root / "report.md").read_text()
expected_title = "2026-09-22 — The instrument needs an outside"
checks = {
    "source_exists": bool(source.strip()),
    "identity_anchor": expected_title in report,
    "route_anchor": "route" in report.lower(),
    "report_has_source_title": "Source title:" in report,
}
for name, ok in checks.items():
    print(f"{name}: {'ok' if ok else 'FAIL'}")
if not all(checks.values()):
    raise SystemExit(1)
