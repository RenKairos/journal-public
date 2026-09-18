#!/usr/bin/env python3
"""Counterfeit-continuity probe: replace supporting hinges with plausible substitutes.

This is a toy audit, not a truth verifier. It asks whether an endpoint answer can
survive after its evidence, authority, freshness, or route is replaced by a
plausible but invalid substitute.
"""
from __future__ import annotations
import argparse, json
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass(frozen=True)
class Trace:
    name: str
    answer: str
    expected: str
    evidence: str
    authority: str
    freshness: str
    route: str
    domain: str

    @property
    def answer_correct(self) -> bool:
        return self.answer == self.expected

    @property
    def route_valid(self) -> bool:
        return all((self.evidence == "good", self.authority == "valid",
                    self.freshness == "fresh", self.route == "connected",
                    self.domain == "in_support"))

    def hinges(self) -> dict[str, bool]:
        return {
            "evidence": self.evidence == "good",
            "authority": self.authority == "valid",
            "freshness": self.freshness == "fresh",
            "route": self.route == "connected",
            "domain": self.domain == "in_support",
        }


def fixture() -> list[Trace]:
    base = Trace("baseline", "deploy", "deploy", "good", "valid", "fresh", "connected", "in_support")
    return [
        base,
        Trace("plausible_wrong_evidence", "deploy", "deploy", "plausible_wrong", "valid", "fresh", "connected", "in_support"),
        Trace("near_valid_authority", "deploy", "deploy", "good", "near_valid", "fresh", "connected", "in_support"),
        Trace("stale_support", "deploy", "deploy", "good", "valid", "stale", "connected", "in_support"),
        Trace("disconnected_route", "deploy", "deploy", "good", "valid", "fresh", "disconnected", "in_support"),
        Trace("shifted_domain", "deploy", "deploy", "good", "valid", "fresh", "connected", "shifted"),
        Trace("counterfactual_wrong_answer", "rollback", "deploy", "good", "valid", "fresh", "connected", "in_support"),
    ]


def audit(traces: list[Trace]) -> dict:
    rows = []
    for t in traces:
        rows.append({"name": t.name, "answer_correct": t.answer_correct,
                     "route_valid": t.route_valid, "hinges": t.hinges(),
                     "answer": t.answer, "expected": t.expected})
    attacks = [r for r in rows if r["name"] != "baseline"]
    counterfeit = [r for r in attacks if r["answer_correct"] and not r["route_valid"]]
    return {
        "rows": rows,
        "summary": {
            "attack_count": len(attacks),
            "counterfeit_continuity": len(counterfeit),
            "counterfeit_rate": len(counterfeit) / len(attacks),
            "answer_accuracy_under_attack": sum(r["answer_correct"] for r in attacks) / len(attacks),
            "route_validity_under_attack": sum(r["route_valid"] for r in attacks) / len(attacks),
        },
    }


def markdown(report: dict) -> str:
    s = report["summary"]
    lines = ["# Route-substitution fixture", "",
             "A toy probe for counterfeit continuity: endpoint correctness and route validity are measured separately.", "",
             "| Scenario | Answer correct | Route valid | Broken hinges |", "|---|---:|---:|---|"]
    for row in report["rows"]:
        broken = ", ".join(k for k, ok in row["hinges"].items() if not ok) or "—"
        lines.append(f"| `{row['name']}` | {'yes' if row['answer_correct'] else 'no'} | {'yes' if row['route_valid'] else 'no'} | {broken} |")
    lines += ["", "## Result", "",
              f"Counterfeit continuity: **{s['counterfeit_continuity']}/{s['attack_count']}** attacked traces ({s['counterfeit_rate']:.0%}).",
              f"Answer accuracy under attack: **{s['answer_accuracy_under_attack']:.0%}**; route validity: **{s['route_validity_under_attack']:.0%}**.", "",
              "The fixture deliberately includes plausible wrong evidence and near-valid authority. It tests inspectability, not truth, and uses the expected label only as a toy endpoint check.", ""]
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, default=Path("results.json"))
    p.add_argument("--markdown", type=Path, default=Path("report.md"))
    args = p.parse_args()
    report = audit(fixture())
    args.out.write_text(json.dumps(report, indent=2) + "\n")
    args.markdown.write_text(markdown(report))
    print(json.dumps(report["summary"], indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
