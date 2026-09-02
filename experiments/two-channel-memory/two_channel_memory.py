#!/usr/bin/env python3
"""Mechanism probe: can two failure signals steer a bounded memory?

The simulator has overlapping relations, decaying item/joint traces, and an
online update that can interfere with old relations. Policies get the same
review/compute budget and see noisy observables, never the hidden relations.
This is a toy probe, not evidence about production continual-learning systems.
"""
from __future__ import annotations
import argparse, itertools, json, math, random
from pathlib import Path


def make_world(rng, items=48, relations=24):
    hidden = []
    for _ in range(relations):
        anchor = rng.randrange(items) if not hidden else hidden[rng.randrange(len(hidden))][rng.randrange(3)]
        group = {anchor}
        while len(group) < 3: group.add(rng.randrange(items))
        hidden.append(tuple(sorted(group)))
    distractors = [tuple(sorted(rng.sample(range(items), 2))) for _ in range(relations // 2)]
    return hidden, distractors


def run(seed, strategy, phases=24, events=20, items=48, relations=24, reviews=8):
    rng = random.Random(seed)
    hidden, distractors = make_world(rng, items, relations)
    strength = [0.0] * items
    precision = [0.0] * items
    joint = {r: 0.0 for r in hidden}
    pair = {}
    checkpoints, action_counts = [], {"review": 0, "precision": 0, "gate": 0}

    def observe(group, amount=1.0):
        for i in group:
            strength[i] = min(1.0, strength[i] + 0.048 * amount + 0.018 * precision[i])
        if len(group) == 3:
            r = tuple(sorted(group))
            if r in joint: joint[r] = min(1.0, joint[r] + 0.066 * amount + 0.020 * sum(precision[i] for i in r) / 3)
        for a, b in itertools.combinations(sorted(group), 2):
            pair[(a, b)] = min(1.0, pair.get((a, b), 0.0) + 0.055 * amount)

    def decay():
        for i in range(items):
            strength[i] *= 0.974 + 0.012 * precision[i]
            precision[i] *= 0.986
        for r in joint: joint[r] *= 0.942
        for k in list(pair): pair[k] *= 0.978

    def candidates():
        # Build candidates from observed edges only; do not enumerate the full
        # item universe (and do not leak the hidden relation list).
        edges = [p for p, value in pair.items() if value >= 0.045]
        out = set()
        for a, b in edges:
            for c, d in edges:
                if c == a and d != b: out.add(tuple(sorted((a, b, d))))
                if c == b and d != a: out.add(tuple(sorted((a, b, d))))
        scored = []
        for r in out:
            evidence = sum(pair.get(p, 0.0) for p in itertools.combinations(r, 2)) / 3
            if evidence >= 0.045: scored.append((r, evidence))
        return scored or [(tuple(sorted(rng.sample(range(items), 3))), 0.01) for _ in range(4)]

    def signals(r, evidence):
        # Structural threat: predicted joint access collapses when a member is removed.
        base = min(strength[i] for i in r) * (0.35 + 0.65 * evidence)
        drops = []
        for removed in r:
            remain = [i for i in r if i != removed]
            after = min(strength[i] for i in remain) * (0.35 + 0.65 * sum(pair.get(p, 0) for p in itertools.combinations(remain, 2)))
            drops.append(max(0.0, base - after))
        structural = sum(drops) / 3 * (0.5 + evidence)
        # Update threat: noisy curvature-aware old/new alignment proxy. Negative means interference.
        old = sum((strength[i] + 0.8 * joint.get(r, 0.0)) for i in r) / 3
        new = sum((rng.random() - 0.5) * 0.45 for _ in r) / 3
        interference = max(0.0, old * 0.62 - new) * (0.55 + 0.45 * evidence)
        return structural, interference

    for phase in range(phases):
        current = phase % relations
        for _ in range(events):
            decay()
            if rng.random() < 0.25: observe(rng.choice(distractors), 0.8)
            else:
                observe(hidden[current])
                if rng.random() < 0.30: observe(hidden[rng.randrange(max(1, current + 1))], 0.7)
        cand = candidates()
        scored = [(r, e, *signals(r, e)) for r, e in cand]
        # Policies use only observables. Each review consumes one of eight slots.
        for _ in range(reviews):
            if strategy == "weakest":
                target = (min(range(items), key=lambda i: strength[i]),)
                action = "review"
            else:
                if strategy == "structural": key = lambda x: x[2]
                elif strategy == "interference": key = lambda x: x[3]
                elif strategy == "two_channel": key = lambda x: 3.0 * x[2] + x[3]
                elif strategy == "uniform": key = lambda x: rng.random()
                else: raise ValueError(strategy)
                target = max(scored, key=key)[0]
                # Two channels can choose between rehearsal, more precision, and gating.
                s, q = next((x[2], x[3]) for x in scored if x[0] == target)
                if strategy == "two_channel" and q > 0.10 and s < 0.018:
                    for i in target: precision[i] = min(1.0, precision[i] + 0.22)
                    action_counts["precision"] += 1; continue
                if strategy == "two_channel" and s > 0.018 and q < 0.10:
                    action_counts["gate"] += 1
                    observe(target, 0.55); continue
                action = "review"
            observe(target)
            action_counts[action] += 1
        item = sum(x >= 0.32 for x in strength) / items
        rel = sum(all(strength[i] >= 0.32 for i in r) and joint[r] >= 0.25 for r in hidden) / relations
        checkpoints.append((item, rel))
    return {"seed": seed, "strategy": strategy, "item_recall": sum(x[0] for x in checkpoints)/phases,
            "relation_recall": sum(x[1] for x in checkpoints)/phases, "final_relation_recall": checkpoints[-1][1],
            "actions": action_counts}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", type=Path, default=Path("results.json")); ap.add_argument("--seeds", type=int, default=200); ap.add_argument("--smoke", action="store_true"); args = ap.parse_args()
    seeds = 5 if args.smoke else args.seeds
    strategies = ("uniform", "weakest", "structural", "interference", "two_channel")
    rows = [run(s, p) for s in range(seeds) for p in strategies]
    summary = {}
    for p in strategies:
        sub = [r for r in rows if r["strategy"] == p]
        summary[p] = {k: sum(r[k] for r in sub)/len(sub) for k in ("item_recall", "relation_recall", "final_relation_recall")}
        summary[p]["action_totals"] = {k: sum(r["actions"][k] for r in sub)/len(sub) for k in ("review", "precision", "gate")}
    payload = {"protocol": {"seeds": seeds, "phases": 24, "events_per_phase": 20, "reviews_per_phase": 8, "items": 48, "hidden_overlapping_relations": 24, "relation_rule": "all items >= .32 and joint trace >= .25", "observability": "pair co-occurrence plus noisy structural/update signals; hidden relation labels withheld"}, "summary": summary, "runs": rows}
    args.out.parent.mkdir(parents=True, exist_ok=True); args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__": main()
