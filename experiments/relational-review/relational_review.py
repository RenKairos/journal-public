#!/usr/bin/env python3
"""Synthetic probe: can relation-level review preserve what item-level review misses?

This is a mechanism sketch, not a model of neural training. A relation is a triple of
co-dependent notes. Individual note strength decays under stream interference, while
joint relation access is separately strengthened by co-observation.
"""
from __future__ import annotations
import argparse, json, random
from pathlib import Path


def run(seed: int, strategy: str, relations: int = 24, phases: int = 8,
        phase_steps: int = 18, reviews: int = 6) -> dict:
    rng = random.Random(seed)
    # Every relation owns three notes. New stream events are unrelated singleton noise.
    strength = [[0.0, 0.0, 0.0] for _ in range(relations)]
    coobs = [0.0] * relations
    learned = [False] * relations
    checkpoint_item, checkpoint_relation = [], []
    for phase in range(phases):
        current = phase % relations
        # Learn the current relation from a handful of co-observations.
        for _ in range(phase_steps):
            for j in range(relations):
                strength[j] = [max(0.0, x - 0.006) for x in strength[j]]
                coobs[j] = max(0.0, coobs[j] - 0.018)
            strength[current] = [min(1.0, x + 0.085) for x in strength[current]]
            coobs[current] = min(1.0, coobs[current] + 0.11)
            learned[current] = True
            # Interference is strongest for facts not currently rehearsed.
            strength[current] = [min(1.0, x + rng.uniform(-.008, .008)) for x in strength[current]]

        # Fixed review budget: only policy differs.
        for _ in range(reviews):
            if strategy == "uniform":
                selected = rng.choice([r for r in range(relations) if learned[r]])
            elif strategy == "difficulty":
                # Item-level difficulty: fix the weakest individual note.
                flat = [(strength[r][n], r) for r in range(relations) if learned[r] for n in range(3)]
                selected = min(flat)[1]
            elif strategy == "relation":
                # Relation-level difficulty: target the weakest joint neighborhood.
                selected = min((r for r in range(relations) if learned[r]),
                                key=lambda r: (sum(strength[r]) / 3 + coobs[r]) / 2)
            else:
                raise ValueError(strategy)
            if strategy == "relation":
                strength[selected] = [min(1.0, x + 0.105) for x in strength[selected]]
                coobs[selected] = min(1.0, coobs[selected] + 0.16)
            else:
                n = rng.randrange(3)
                strength[selected][n] = min(1.0, strength[selected][n] + 0.16)
                # Item review gives only a small chance of re-forming the relation.
                coobs[selected] = min(1.0, coobs[selected] + 0.025)

        known = [r for r in range(relations) if learned[r]]
        checkpoint_item.append(sum(sum(x >= .35 for x in strength[r]) for r in known) / (len(known) * 3))
        checkpoint_relation.append(sum(all(x >= .35 for x in strength[r]) and coobs[r] >= .28
                                      for r in known) / len(known))

    item_recall = sum(checkpoint_item) / len(checkpoint_item)
    relation_recall = sum(checkpoint_relation) / len(checkpoint_relation)
    return {"seed": seed, "strategy": strategy, "item_recall": item_recall,
            "relation_recall": relation_recall, "mean_coobservation": sum(coobs) / relations}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("results.json"))
    ap.add_argument("--seeds", type=int, default=200)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    seeds = 5 if args.smoke else args.seeds
    rows = [run(seed, strategy) for seed in range(seeds) for strategy in ("uniform", "difficulty", "relation")]
    summary = {}
    for strategy in ("uniform", "difficulty", "relation"):
        subset = [r for r in rows if r["strategy"] == strategy]
        summary[strategy] = {k: sum(r[k] for r in subset) / len(subset)
                             for k in ("item_recall", "relation_recall", "mean_coobservation")}
    payload = {"protocol": {"seeds": seeds, "relations": 24, "phases": 8,
                             "phase_steps": 18, "reviews_per_phase": 6,
                             "relation_recall_rule": "all 3 notes >= 0.35 and co-observation >= 0.28"},
               "summary": summary, "runs": rows}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
