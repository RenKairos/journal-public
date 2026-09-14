#!/usr/bin/env python3
"""Audit whether a decision's route survives the loss of its supporting hinges.

A hinge is a condition that should make a decision inspectable: evidence,
authorization, freshness, or route coherence. This is deliberately a small,
stdlib-only tool for decision traces, not a truth verifier.
"""
from __future__ import annotations
import argparse, datetime as dt, json
from pathlib import Path


def parse_date(value: str | None) -> dt.date | None:
    if not value:
        return None
    return dt.date.fromisoformat(value)


def assess(decision: dict, *, today: dt.date, removed: str | None = None,
           authorization: bool | None = None) -> dict:
    evidence = {item["id"]: item for item in decision.get("evidence", [])}
    required = decision.get("required_evidence", [])
    missing = [eid for eid in required if eid not in evidence or
               not evidence[eid].get("observed", False) or eid == removed]
    stale = []
    for eid, item in evidence.items():
        expiry = parse_date(item.get("expires_at"))
        if expiry and expiry < today and eid in required and eid != removed:
            stale.append(eid)
    authorized = decision.get("authorized", False) if authorization is None else authorization
    route = decision.get("route", [])
    route_ok = bool(route) and all(eid in evidence and eid not in missing and eid not in stale
                                   for eid in route)
    hinges = {
        "evidence": not missing and not stale,
        "authorization": bool(authorized),
        "freshness": not stale,
        "route": route_ok,
    }
    return {
        "decision_id": decision.get("id", "unnamed"),
        "answer": decision.get("answer"),
        "answer_present": decision.get("answer") is not None,
        "missing_evidence": missing,
        "stale_evidence": stale,
        "authorized": bool(authorized),
        "route": route,
        "hinges": hinges,
        "route_valid": all(hinges.values()),
    }


def audit(decision: dict, today: dt.date) -> dict:
    baseline = assess(decision, today=today)
    attacks = []
    for item in decision.get("evidence", []):
        if item.get("id") in decision.get("required_evidence", []):
            attacks.append({"attack": f"remove:{item['id']}",
                            "result": assess(decision, today=today, removed=item["id"])})
    attacks.append({"attack": "revoke:authorization",
                    "result": assess(decision, today=today, authorization=False)})
    failures = sum(not item["result"]["route_valid"] for item in attacks)
    answer_retained = sum(item["result"]["answer_present"] for item in attacks)
    return {"baseline": baseline, "attacks": attacks,
            "summary": {"attack_count": len(attacks),
                        "route_failures": failures,
                        "answer_retained_under_attack": answer_retained,
                        "route_fragility": failures / len(attacks) if attacks else 0.0}}


def markdown(report: dict) -> str:
    lines = ["# Hinge audit report", "",
             "This report tests inspectability conditions; it does not establish that an answer is true.", "",
             "## Baseline", ""]
    base = report["baseline"]
    lines += [f"- Decision: `{base['decision_id']}`", f"- Answer: `{base['answer']}`",
              f"- Route valid: **{base['route_valid']}**", "- Hinges: " + ", ".join(
                  f"{k}={'pass' if v else 'FAIL'}" for k, v in base["hinges"].items()), "", "## Counterfactual attacks", "",
              "| Attack | Answer retained | Route valid | Broken hinges |", "|---|---:|---:|---|"]
    for attack in report["attacks"]:
        result = attack["result"]
        broken = ", ".join(k for k, v in result["hinges"].items() if not v) or "—"
        lines.append(f"| `{attack['attack']}` | {'yes' if result['answer_present'] else 'no'} | "
                     f"{'yes' if result['route_valid'] else 'no'} | {broken} |")
    summary = report["summary"]
    lines += ["", "## Reading", "", f"Route fragility: **{summary['route_fragility']:.0%}** "
              f"({summary['route_failures']}/{summary['attack_count']} attacks broke the route).",
              f"The answer field remained present in {summary['answer_retained_under_attack']}/{summary['attack_count']} attacks."]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON decision trace")
    parser.add_argument("--out", type=Path, default=Path("hinge-report.json"))
    parser.add_argument("--markdown", type=Path, help="also write a Markdown report")
    parser.add_argument("--today", default=dt.date.today().isoformat(), help="ISO date for freshness checks")
    args = parser.parse_args()
    payload = json.loads(args.input.read_text())
    decisions = payload if isinstance(payload, list) else payload.get("decisions", [payload])
    report = {"today": args.today, "decisions": [audit(d, dt.date.fromisoformat(args.today)) for d in decisions]}
    args.out.write_text(json.dumps(report, indent=2) + "\n")
    if args.markdown:
        args.markdown.write_text("\n---\n\n".join(markdown(r) for r in report["decisions"]))
    print(json.dumps({"decisions": len(decisions), "out": str(args.out),
                      "route_fragility": [r["summary"]["route_fragility"] for r in report["decisions"]]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
