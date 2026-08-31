#!/usr/bin/env python3
"""Probe whether ablation instability can discover overlapping conflict neighborhoods.

Mechanism sketch, not a claim about production memory systems. Hidden triples share
items and some streams contain misleading pair-only co-occurrences. A review policy
gets a fixed budget and may rehearse one item or one discovered/true triple.
"""
from __future__ import annotations
import argparse, itertools, json, random
from pathlib import Path


def make_world(rng: random.Random, items: int = 48, triples: int = 24):
    hidden = []
    # Force overlap: each new triple shares one item with an earlier triple.
    for t in range(triples):
        anchor = rng.randrange(items) if t == 0 else hidden[rng.randrange(len(hidden))][rng.randrange(3)]
        rest = set([anchor])
        while len(rest) < 3:
            rest.add(rng.randrange(items))
        hidden.append(tuple(sorted(rest)))
    # Distractor pairs make raw frequency/co-occurrence less trustworthy.
    distractors = [tuple(sorted(rng.sample(range(items), 2))) for _ in range(triples // 2)]
    return hidden, distractors


def run(seed: int, strategy: str, phases: int = 10, events_per_phase: int = 28,
        items: int = 48, triples: int = 24, reviews: int = 8) -> dict:
    rng = random.Random(seed)
    hidden, distractors = make_world(rng, items, triples)
    strength = [0.0] * items
    joint = {tr: 0.0 for tr in hidden}
    pair_obs = {}
    seen = set()
    checkpoints = []

    def observe(group):
        for i in group:
            strength[i] = min(1.0, strength[i] + 0.055)
        if len(group) == 3:
            tr = tuple(sorted(group))
            if tr in joint:
                joint[tr] = min(1.0, joint[tr] + 0.075)
        for a in group:
            for b in group:
                if a < b:
                    pair_obs[(a, b)] = min(1.0, pair_obs.get((a, b), 0.0) + 0.06)

    def decay():
        for i in range(items):
            strength[i] *= 0.985
        for tr in joint:
            joint[tr] *= 0.955

    for phase in range(phases):
        current = phase % triples
        # Mostly true triple events, with pair distractors and occasional overlap.
        for _ in range(events_per_phase):
            decay()
            if rng.random() < 0.22:
                observe(rng.choice(distractors))
            else:
                observe(hidden[current])
                if rng.random() < 0.20:
                    observe(hidden[rng.randrange(max(1, current + 1))])
            seen.add(current)

        # Candidate discovery uses only observable pair co-observation. The hidden
        # triples are never supplied to this policy; distractor pairs can create
        # false neighborhoods and overlapping triples share members.
        candidates = [tr for tr in itertools.combinations(range(items), 3)
                      if all(pair_obs.get(pair, 0.0) >= 0.06
                             for pair in itertools.combinations(tr, 2))]
        if not candidates:
            candidates = [tuple(sorted(rng.sample(range(items), 3))) for _ in range(3)]

        def instability(tr):
            # How much the predicted joint access collapses under one-item ablation.
            base = min(strength[i] for i in tr) * (0.35 + 0.65 * sum(pair_obs.get(tuple(sorted((a,b))), 0.0)
                    for ix,a in enumerate(tr) for b in tr[ix+1:]) / 3.0)
            drops = []
            for removed in tr:
                remain = [i for i in tr if i != removed]
                ablated = min(strength[i] for i in remain) * (0.35 + 0.65 * sum(
                    pair_obs.get(tuple(sorted((a,b))), 0.0) for a in remain for b in remain if a < b))
                drops.append(max(0.0, base - ablated))
            # Instability is useful only when there is evidence of the neighborhood.
            return sum(drops) / 3.0 * (0.5 + 0.5 * min(1.0, sum(pair_obs.get(tuple(sorted((a,b))), 0.0)
                    for ix,a in enumerate(tr) for b in tr[ix+1:]) / 3.0))

        for _ in range(reviews):
            if strategy == "uniform":
                observe([rng.randrange(items)])
            elif strategy == "frequency":
                observe([max(range(items), key=lambda i: strength[i])])
            elif strategy == "instability":
                target = max(candidates, key=instability)
                observe(target)
            elif strategy == "oracle":
                target = min(hidden, key=lambda tr: joint[tr] + sum(strength[i] for i in tr) / 3)
                observe(target)
            else:
                raise ValueError(strategy)

        item_recall = sum(strength[i] >= 0.34 for i in range(items)) / items
        relation_recall = sum(all(strength[i] >= 0.34 for i in tr) and joint[tr] >= 0.30
                              for tr in hidden) / len(hidden)
        checkpoints.append((item_recall, relation_recall))

    return {"seed": seed, "strategy": strategy,
            "item_recall": sum(x[0] for x in checkpoints) / len(checkpoints),
            "relation_recall": sum(x[1] for x in checkpoints) / len(checkpoints),
            "final_relation_recall": checkpoints[-1][1]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("results.json"))
    ap.add_argument("--seeds", type=int, default=100)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    seeds = 5 if args.smoke else args.seeds
    strategies = ("uniform", "frequency", "instability", "oracle")
    rows = [run(seed, strategy) for seed in range(seeds) for strategy in strategies]
    summary = {}
    for strategy in strategies:
        subset = [r for r in rows if r["strategy"] == strategy]
        summary[strategy] = {k: sum(r[k] for r in subset) / len(subset)
                             for k in ("item_recall", "relation_recall", "final_relation_recall")}
    payload = {"protocol": {"seeds": seeds, "phases": 10, "events_per_phase": 28,
                             "items": 48, "hidden_overlapping_triples": 24,
                             "distractor_pair_probability": 0.22, "reviews_per_phase": 8,
                             "relation_rule": "all 3 items >= 0.34 and joint access >= 0.30"},
               "summary": summary, "runs": rows}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
