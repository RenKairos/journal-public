#!/usr/bin/env python3
"""Audit whether a workflow used information that existed only in the future.

The input is a JSON fixture containing revision events and decision origins.  A
record is eligible at an origin only when its release time is <= origin.  The
latest snapshot intentionally ignores that contract, making hindsight leakage
visible rather than silently baking it into a feature table.
"""
from __future__ import annotations
import argparse, json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def latest_snapshot(revisions: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in revisions:
        current = out.get(row["series"])
        if current is None or parse_time(row["released_at"]) > parse_time(current["released_at"]):
            out[row["series"]] = row
    return out


def asof_snapshot(revisions: list[dict[str, Any]], origin: str) -> dict[str, dict[str, Any]]:
    cutoff = parse_time(origin)
    out: dict[str, dict[str, Any]] = {}
    for row in revisions:
        released = parse_time(row["released_at"])
        if released <= cutoff:
            current = out.get(row["series"])
            if current is None or released > parse_time(current["released_at"]):
                out[row["series"]] = row
    return out


def audit(data: dict[str, Any]) -> dict[str, Any]:
    revisions = data["revisions"]
    latest = latest_snapshot(revisions)
    decisions = []
    leaked_decisions = 0
    changed_series = 0
    for decision in data["decisions"]:
        legal = asof_snapshot(revisions, decision["origin"])
        leaked = sorted(set(latest) - set(legal))
        changed = sorted(
            series for series in set(latest) & set(legal)
            if latest[series]["value"] != legal[series]["value"]
        )
        if leaked or changed:
            leaked_decisions += 1
        changed_series += len(changed)
        decisions.append({
            "name": decision.get("name", decision["origin"]),
            "origin": decision["origin"],
            "legal_series": sorted(legal),
            "future_series": leaked,
            "revised_series": changed,
            "legal_values": {k: v["value"] for k, v in sorted(legal.items())},
            "latest_values": {k: v["value"] for k, v in sorted(latest.items())},
            "leakage": bool(leaked or changed),
        })
    total = len(decisions)
    return {
        "dataset": data.get("name", "unnamed"),
        "revision_events": len(revisions),
        "series": sorted(latest),
        "decisions": decisions,
        "summary": {
            "decisions": total,
            "decisions_affected_by_hindsight": leaked_decisions,
            "affected_decision_rate": round(leaked_decisions / total, 4) if total else 0.0,
            "revision_value_changes": changed_series,
            "latest_snapshot_series": len(latest),
        },
    }


def markdown(report: dict[str, Any]) -> str:
    s = report["summary"]
    lines = [
        f"# Vintage Boundary Audit — {report['dataset']}", "",
        "This report compares a retrospective latest-value snapshot with the newest "
        "revision that was actually released by each decision origin.", "",
        "## Result", "",
        f"- Decision origins: **{s['decisions']}**",
        f"- Origins changed by hindsight: **{s['decisions_affected_by_hindsight']}** ({s['affected_decision_rate']:.1%})",
        f"- Revision value changes across origins: **{s['revision_value_changes']}**",
        "", "## Per-origin trace", "",
        "| origin | legal values | future-only series | revised series | leakage |",
        "|---|---|---|---|---|",
    ]
    for row in report["decisions"]:
        values = ", ".join(f"{k}={v}" for k, v in row["legal_values"].items()) or "(none)"
        lines.append(
            f"| {row['origin']} | {values} | "
            f"{', '.join(row['future_series']) or '—'} | "
            f"{', '.join(row['revised_series']) or '—'} | "
            f"{'YES' if row['leakage'] else 'no'} |"
        )
    lines += [
        "", "## Interpretation", "",
        "A retrospective value can be accurate and still be unauthorized evidence for an "
        "earlier decision. This is a mechanism probe, not a forecast benchmark: it checks "
        "the information boundary and does not establish predictive quality.", "",
        "The audit is intentionally conservative: release timestamps define availability; "
        "it does not prove that a pretrained model has no hidden exposure to later vintages.", "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("fixture", type=Path)
    ap.add_argument("--json", type=Path, default=Path("audit.json"))
    ap.add_argument("--markdown", type=Path, default=Path("audit.md"))
    args = ap.parse_args()
    report = audit(json.loads(args.fixture.read_text()))
    args.json.write_text(json.dumps(report, indent=2) + "\n")
    args.markdown.write_text(markdown(report))
    print(json.dumps({"status": "passed", "json": str(args.json), "markdown": str(args.markdown), "summary": report["summary"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
