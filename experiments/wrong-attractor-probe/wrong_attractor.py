#!/usr/bin/env python3
"""Synthetic probe: can an energy-like residual warn about wrong memories?

The controller sees noisy pair co-observations, not hidden triples. Updates are
asymmetric and decay, so a plausible neighborhood can become a stable but false
attractor. This is a mechanism sketch, not a claim about neural systems.
"""
from __future__ import annotations
import argparse, itertools, json, math, random
from pathlib import Path


def make_world(rng, items=36, relations=18):
    hidden = []
    for _ in range(relations):
        anchor = rng.randrange(items) if not hidden else hidden[rng.randrange(len(hidden))][rng.randrange(3)]
        g = {anchor}
        while len(g) < 3: g.add(rng.randrange(items))
        hidden.append(tuple(sorted(g)))
    false = []
    while len(false) < relations // 2:
        t = tuple(sorted(rng.sample(range(items), 3)))
        if t not in hidden and t not in false: false.append(t)
    return hidden, false


def run(seed, policy, phases=18, events=24, items=36, relations=18, reviews=6):
    rng = random.Random(seed)
    hidden, false = make_world(rng, items, relations)
    nodes = [0.0] * items
    W = [[0.0] * items for _ in range(items)]
    joint = {r: 0.0 for r in hidden}
    pair_seen = {}
    records = []

    def observe(group, strength=1.0, truthful=False):
        group = tuple(sorted(group))
        for i in group: nodes[i] = min(1.0, nodes[i] + 0.045 * strength)
        for a, b in itertools.permutations(group, 2):
            # asymmetric online write: direction-specific noise is intentional
            target = 0.075 * strength + rng.gauss(0, 0.010)
            W[a][b] = max(-0.2, min(1.0, 0.965 * W[a][b] + target))
        for a, b in itertools.combinations(group, 2):
            pair_seen[(a, b)] = min(1.0, pair_seen.get((a, b), 0) + 0.06 * strength)
        if truthful and len(group) == 3:
            joint[group] = min(1.0, joint[group] + 0.085 * strength)

    def drift():
        for i in range(items): nodes[i] *= 0.978
        for a in range(items):
            for b in range(items):
                W[a][b] *= 0.989
        for r in joint: joint[r] *= 0.945
        for p in list(pair_seen): pair_seen[p] *= 0.974

    def candidates():
        edges = [p for p, v in pair_seen.items() if v > 0.07]
        out = set()
        for a, b in edges:
            for c, d in edges:
                if c in (a, b) and d not in (a, b): out.add(tuple(sorted((a, b, d))))
        return list(out) or [tuple(sorted(rng.sample(range(items), 3))) for _ in range(5)]

    def metrics(t):
        # Candidate-only observable features. Retrieval uses an asymmetric rollout;
        # energy uses the symmetrized projection solely as a diagnostic.
        x = [0.0] * items
        x[t[0]] = 1.0
        residuals, energies = [], []
        for _ in range(7):
            y = [math.tanh(sum(W[i][j] * x[j] for j in range(items))) for i in range(items)]
            residuals.append(sum(abs(y[i] - x[i]) for i in t) / 3)
            sym = lambda a, b: (W[a][b] + W[b][a]) / 2
            energies.append(-sum(sym(a, b) * x[a] * x[b] for a, b in itertools.combinations(t, 2)))
            x = y
        coh = sum((W[a][b] + W[b][a]) / 2 for a, b in itertools.combinations(t, 2)) / 3
        residual = sum(residuals[-3:]) / 3
        descent = sum(abs(energies[i + 1] - energies[i]) for i in range(len(energies) - 1)) / 6
        return {"t": t, "coh": coh, "residual": residual, "descent": descent,
                "observable": sum(pair_seen.get(p, 0) for p in itertools.combinations(t, 2)) / 3}

    for phase in range(phases):
        current = phase % relations
        for _ in range(events):
            drift()
            if rng.random() < 0.28:
                # pair-only distractors are the source of false neighborhoods
                observe(rng.choice(false)[:2], 0.9, False)
            else:
                true = hidden[current]
                kept = [i for i in true if rng.random() > 0.13]
                if len(kept) < 2: kept = list(true[:2])
                observe(kept, 1.0, len(kept) == 3)
                if rng.random() < 0.22: observe(hidden[rng.randrange(current + 1)], 0.7, True)
        cand = [metrics(t) for t in candidates()]
        for _ in range(reviews):
            if policy == "uniform": chosen = rng.choice(cand)
            elif policy == "frequency": chosen = max(cand, key=lambda z: z["observable"])
            elif policy == "residual": chosen = max(cand, key=lambda z: z["residual"])
            elif policy == "calibrated":
                # Repair unstable routes, but refuse already-settled high-coherence basins.
                chosen = max(cand, key=lambda z: z["residual"] * (1.0 - max(0.0, z["coh"])))
            elif policy == "oracle":
                chosen = min(hidden, key=lambda r: joint[r])
                chosen = metrics(chosen)
            else: raise ValueError(policy)
            observe(chosen["t"], 0.75, chosen["t"] in joint)
        true_recall = sum(joint[r] > 0.27 and all(nodes[i] > 0.20 for i in r) for r in hidden) / len(hidden)
        false_settled = sum(m["t"] in false and m["coh"] > 0.15 and m["residual"] < 0.12 for m in cand) / max(1, len(cand))
        # Record whether low residual actually identifies truth; this is the warning test.
        labels = [m["t"] in hidden for m in cand]
        if len(set(labels)) > 1:
            order = sorted(cand, key=lambda m: m["residual"])
            low_truth = sum(m["t"] in hidden for m in order[:max(1, len(order)//3)]) / max(1, len(order)//3)
        else: low_truth = float("nan")
        records.append({"phase": phase, "relation_recall": true_recall,
                        "false_settled": false_settled, "low_residual_truth": low_truth})
    valid = [r["low_residual_truth"] for r in records if not math.isnan(r["low_residual_truth"])]
    return {"seed": seed, "policy": policy,
            "relation_recall": sum(r["relation_recall"] for r in records) / len(records),
            "final_relation_recall": records[-1]["relation_recall"],
            "false_settled": sum(r["false_settled"] for r in records) / len(records),
            "low_residual_truth": sum(valid) / len(valid) if valid else None}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", type=Path, default=Path("results.json")); ap.add_argument("--seeds", type=int, default=120); ap.add_argument("--smoke", action="store_true"); args = ap.parse_args()
    seeds = 5 if args.smoke else args.seeds
    policies = ("uniform", "frequency", "residual", "calibrated", "oracle")
    rows = [run(s, p) for s in range(seeds) for p in policies]
    summary = {}
    for p in policies:
        sub = [r for r in rows if r["policy"] == p]
        summary[p] = {k: sum(r[k] for r in sub if r[k] is not None) / sum(r[k] is not None for r in sub) for k in ("relation_recall", "final_relation_recall", "false_settled", "low_residual_truth")}
    payload = {"protocol": {"seeds": seeds, "phases": 18, "events_per_phase": 24, "reviews_per_phase": 6, "items": 36, "hidden_relations": 18, "false_pair_source": "9 non-hidden triples sampled as pair-only distractors", "updates": "decaying asymmetric directed Hebbian writes", "diagnostic": "symmetrized energy rollout plus asymmetric residual", "relation_rule": "joint trace > .27 and all node traces > .20"}, "summary": summary, "runs": rows}
    args.out.parent.mkdir(parents=True, exist_ok=True); args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__": main()
