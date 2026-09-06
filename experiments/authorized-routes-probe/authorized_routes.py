#!/usr/bin/env python3
"""Small probe: can a memory controller protect what is supported and consequential?

The policy never sees hidden relations. It sees noisy evidence, route conflict, and
query goals. Reviews move pair weights toward the evidence-backed state.
"""
import argparse, json
from pathlib import Path
import numpy as np


def pair(i, j):
    return (i, j) if i < j else (j, i)


def simulate(seed, policy, steps=90, items=24, triples=12, budget=8):
    rng = np.random.default_rng(seed)
    hidden = []
    for _ in range(triples):
        t = tuple(sorted(rng.choice(items, 3, replace=False)))
        if t not in hidden: hidden.append(t)
    true_pairs = {pair(a, b) for t in hidden for i, a in enumerate(t) for b in t[i + 1:]}
    all_pairs = [pair(i, j) for i in range(items) for j in range(i + 1, items)]
    false_pairs = [p for p in all_pairs if p not in true_pairs]
    goals = set(rng.choice(len(all_pairs), min(18, len(all_pairs)), replace=False))
    goal_pairs = {all_pairs[i] for i in goals}

    w = {p: 0.0 for p in all_pairs}          # current relational memory
    evidence = {p: 0.0 for p in all_pairs}   # observable support, not truth
    seen = {p: 0 for p in all_pairs}
    route = rng.normal(0, 1, (items, 4))
    route /= np.linalg.norm(route, axis=1, keepdims=True)
    checkpoints = []

    for step in range(steps):
        t = hidden[int(rng.integers(len(hidden)))]
        # Partial observation of a true neighborhood plus a non-hidden distractor.
        obs = [pair(t[0], t[1]), pair(t[1], t[2])]
        d = false_pairs[int(rng.integers(len(false_pairs)))]
        obs.append(d)
        for p in obs:
            seen[p] += 1
            evidence[p] = min(1.0, evidence[p] * 0.94 + (0.14 if p in true_pairs else 0.055))
            w[p] = min(1.0, w[p] + (0.12 if p in true_pairs else 0.075))
        # New writes interfere most when item routes overlap, but never symmetrically.
        active = set(obs)
        for p in all_pairs:
            if p in active: continue
            overlap = (1 + float(np.dot(route[p[0]], route[t[0]]))) / 2
            w[p] *= 0.997 - 0.004 * overlap
        # A route update follows observed co-occurrence, allowing neighborhood drift.
        route[t[0]] = 0.98 * route[t[0]] + 0.02 * route[t[1]]
        route[t[0]] /= np.linalg.norm(route[t[0]])

        if step % 5 == 4:
            scores = {}
            for p in all_pairs:
                freq = min(1.0, seen[p] / 8)
                route_conflict = 1.0 - (1 + float(np.dot(route[p[0]], route[p[1]]))) / 2
                # A high conflict means this relation is vulnerable to route separation.
                goal = 1.0 if p in goal_pairs else 0.0
                if policy == "uniform": s = rng.random()
                elif policy == "frequency": s = freq * (1 - w[p])
                elif policy == "route": s = route_conflict * (1 - w[p])
                elif policy == "evidence": s = evidence[p] * (1 - w[p])
                elif policy == "goal": s = goal * (1 - w[p]) + 0.15 * evidence[p] * (1 - w[p])
                elif policy == "combined":
                    s = (0.35 * evidence[p] + 0.30 * route_conflict + 0.25 * goal + 0.10) * (1 - w[p])
                else: raise ValueError(policy)
                scores[p] = s
            chosen = sorted(all_pairs, key=lambda p: scores[p], reverse=True)[:budget]
            for p in chosen:
                # Review does not reveal truth; it checks the current evidence trail.
                if evidence[p] > 0.10:
                    w[p] = min(1.0, w[p] + 0.10 * evidence[p])
                else:
                    w[p] *= 0.88
            true_recall = np.mean([w[p] > 0.25 for p in true_pairs])
            false_settled = np.mean([w[p] > 0.25 for p in false_pairs])
            goal_utility = np.mean([w[p] > 0.25 for p in goal_pairs])
            checkpoints.append((true_recall, false_settled, goal_utility))

    a = np.array(checkpoints)
    return {"relation_recall": float(a[:, 0].mean()),
            "final_relation_recall": float(a[-1, 0]),
            "false_settled": float(a[:, 1].mean()),
            "goal_utility": float(a[:, 2].mean())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results.json")
    ap.add_argument("--seeds", type=int, default=120)
    args = ap.parse_args()
    policies = ["uniform", "frequency", "route", "evidence", "goal", "combined"]
    result = {p: {} for p in policies}
    for p in policies:
        rows = [simulate(s, p) for s in range(args.seeds)]
        result[p] = {k: float(np.mean([r[k] for r in rows])) for k in rows[0]}
        result[p]["std_relation_recall"] = float(np.std([r["relation_recall"] for r in rows]))
    payload = {"config": {"seeds": args.seeds, "steps": 90, "items": 24, "hidden_triples": 12, "review_budget": 8}, "results": result}
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__": main()
