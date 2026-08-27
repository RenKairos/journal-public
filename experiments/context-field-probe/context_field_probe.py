#!/usr/bin/env python3
"""Probe whether retrieval needs co-observation and reader-facing rendering.

Synthetic, deliberately transparent experiment. No language model is used: the
reader succeeds when the rendered packet exposes the required answer tokens and
source IDs. This isolates retrieval/rendering mechanics rather than claiming
anything about LLM behavior.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

STOP = {"what", "which", "should", "the", "a", "an", "for", "to", "of", "in", "and", "is", "use", "does", "how"}

@dataclass(frozen=True)
class Note:
    note_id: str
    text: str
    facts: frozenset[str]
    answer_tokens: frozenset[str]

@dataclass(frozen=True)
class Case:
    query: str
    required_facts: frozenset[str]
    answer_tokens: frozenset[str]


def words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def score(query: str, note: Note, rng: random.Random) -> float:
    q = Counter(w for w in words(query) if w not in STOP)
    n = Counter(words(note.text))
    overlap = sum(min(q[k], n[k]) for k in q)
    # Tiny noise prevents accidental stable ties, as in approximate retrieval.
    return overlap / max(1, len(q)) + rng.random() * 0.015


def corpus() -> tuple[list[Note], list[Case]]:
    notes = [
        Note("A", "The archive is organized by route: retrieval selects a neighborhood before rendering.", frozenset({"route", "neighborhood"}), frozenset({"neighborhood"})),
        Note("B", "When evidence is split across chunks, co-observation requires related notes to share one context.", frozenset({"co_observation", "context"}), frozenset({"context"})),
        Note("C", "The renderer puts a resolved answer first, then citations and unresolved alternatives.", frozenset({"answer_first", "citations"}), frozenset({"answer", "first"})),
        Note("D", "A typed ledger preserves provenance but may hide the usable statement behind metadata.", frozenset({"ledger", "provenance"}), frozenset({"statement"})),
        Note("E", "Weighted neighborhoods are useful when nearby notes share a trace, but dilute incompatible evidence.", frozenset({"weighted", "compatibility"}), frozenset({"weighted"})),
        Note("F", "Hard top-k retrieval is efficient and can discard the second note needed to identify a relation.", frozenset({"hard_top_k", "discard"}), frozenset({"relation"})),
        Note("G", "Replay refreshes old representations; it does not automatically synthesize a relation absent from a batch.", frozenset({"replay", "synthesis"}), frozenset({"synthesize"})),
        Note("H", "Basin entropy measures whether stored attractors receive balanced access from state space.", frozenset({"basin", "entropy"}), frozenset({"balanced"})),
        Note("I", "A slow trace can protect old content while a fast trace remains plastic to new sequences.", frozenset({"slow", "fast", "plasticity"}), frozenset({"slow", "fast"})),
        Note("J", "Pooling averages local routes only when the alternatives are compatible with the learned computation.", frozenset({"pooling", "routes"}), frozenset({"compatible"})),
    ]
    cases = [
        Case("How should the archive expose evidence when a relation is split across chunks?", frozenset({"co_observation", "answer_first"}), frozenset({"context", "answer", "first"})),
        Case("What retrieval strategy is safest near a thematic boundary?", frozenset({"weighted", "compatibility"}), frozenset({"weighted", "compatible"})),
        Case("What does replay fail to guarantee?", frozenset({"replay", "synthesis"}), frozenset({"synthesize"})),
        Case("How can old content remain stable while new sequences stay learnable?", frozenset({"slow", "fast", "plasticity"}), frozenset({"slow", "fast"})),
        Case("What metric checks fair access to attractor memories?", frozenset({"basin", "entropy"}), frozenset({"balanced"})),
    ]
    return notes, cases


def retrieve(notes: list[Note], case: Case, mode: str, rng: random.Random) -> list[tuple[Note, float]]:
    ranked = sorted(((n, score(case.query, n, rng)) for n in notes), key=lambda x: x[1], reverse=True)
    if mode == "hard":
        return ranked[:2]
    # Soft retrieval keeps a wider neighborhood, but still has a context budget.
    top = ranked[:5]
    temperature = 0.20
    exps = [math.exp(s / temperature) for _, s in top]
    z = sum(exps)
    return [(n, e / z) for (n, _), e in zip(top, exps)]


def render(items: list[tuple[Note, float]], style: str, budget: int) -> tuple[str, list[str]]:
    if style == "answer_first":
        chunks = [f"Answer evidence: {n.text} [source {n.note_id}]" for n, _ in items]
    elif style == "ledger":
        # Audit-friendly, but intentionally verbose: metadata precedes the
        # answer-bearing record and can consume a fixed context budget.
        chunks = [f"record_type=historical_memory; source_id={n.note_id}; retrieval_weight={w:.3f}; fact_inventory={','.join(sorted(n.facts))}; provenance_status=verified; conflict_status=none; timestamp=unknown; record_text={n.text}" for n, w in items]
    else:
        chunks = [f"source {n.note_id}: {n.text}" for n, _ in items]
    rendered = " ".join(chunks)
    tokens = words(rendered)[:budget]
    return " ".join(tokens), [n.note_id for n, _ in items]


def evaluate(seed: int, trials: int, budget: int) -> dict:
    notes, cases = corpus()
    rng = random.Random(seed)
    rows = []
    for _ in range(trials):
        case = rng.choice(cases)
        for mode in ("hard", "weighted"):
            items = retrieve(notes, case, mode, rng)
            for style in ("answer_first", "ledger", "raw"):
                packet, ids = render(items, style, budget)
                visible = set(words(packet))
                needed_sources = {n.note_id for n in notes if n.facts & case.required_facts}
                # Exact evidence criterion: every required answer token is visible;
                # co-observation also requires the distinct supporting notes.
                answer_ok = case.answer_tokens <= visible
                source_ok = needed_sources <= set(ids)
                rows.append({"mode": mode, "style": style, "answer_ok": answer_ok, "source_ok": source_ok, "joint_ok": answer_ok and source_ok})
    summary = {}
    for mode in ("hard", "weighted"):
        for style in ("answer_first", "ledger", "raw"):
            subset = [r for r in rows if r["mode"] == mode and r["style"] == style]
            summary[f"{mode}/{style}"] = {k: round(sum(r[k] for r in subset) / len(subset), 4) for k in ("answer_ok", "source_ok", "joint_ok")}
    return {"seed": seed, "trials": trials, "budget_tokens": budget, "summary": summary}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("results.json"))
    ap.add_argument("--seeds", type=int, default=12)
    ap.add_argument("--trials", type=int, default=500)
    ap.add_argument("--budget", type=int, default=18)
    args = ap.parse_args()
    runs = [evaluate(seed, args.trials, args.budget) for seed in range(args.seeds)]
    keys = runs[0]["summary"]
    aggregate = {k: {m: round(sum(r["summary"][k][m] for r in runs) / len(runs), 4) for m in ("answer_ok", "source_ok", "joint_ok")} for k in keys}
    result = {"experiment": "context-field-probe", "description": "Synthetic probe of retrieval breadth and evidence rendering", "runs": runs, "aggregate": aggregate}
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(aggregate, indent=2))

if __name__ == "__main__":
    main()
