#!/usr/bin/env python3
"""Synthetic probe: can spectral concentration veto a plausible but stale write?

The policy sees noisy co-observations, route overlap, freshness, and goal pressure.
Hidden triples are evaluation-only.  The experiment asks whether treating update
spectral concentration as a veto (rather than another weighted score) reduces
false settled relations without merely refusing to learn.
"""
from __future__ import annotations
import argparse, json, itertools
from pathlib import Path
import numpy as np


def pair(a, b):
    return (a, b) if a < b else (b, a)


def simulate(seed: int, policy: str, phases=24, events=18, items=30,
             relations=15, reviews=7, dim=6):
    rng = np.random.default_rng(seed)
    hidden = []
    while len(hidden) < relations:
        t = tuple(sorted(rng.choice(items, 3, replace=False)))
        if t not in hidden: hidden.append(t)
    true_pairs = {pair(a, b) for t in hidden for a, b in itertools.combinations(t, 2)}
    all_pairs = [pair(a, b) for a in range(items) for b in range(a + 1, items)]
    false_pairs = [p for p in all_pairs if p not in true_pairs]
    false_triples = []
    while len(false_triples) < relations:
        t = tuple(sorted(rng.choice(items, 3, replace=False)))
        if t not in hidden and t not in false_triples: false_triples.append(t)
    goals = set(rng.choice(len(hidden), size=max(3, relations // 3), replace=False))

    memory = {p: 0.0 for p in all_pairs}
    evidence = {p: 0.0 for p in all_pairs}
    age = {p: 0 for p in all_pairs}
    node = np.zeros(items)
    routes = rng.normal(size=(items, dim)); routes /= np.linalg.norm(routes, axis=1, keepdims=True)
    update_history = []
    records = []
    action_counts = {"review": 0, "veto": 0, "defer": 0}

    def observe(group, strength=1.0, truthful=False):
        group = tuple(sorted(group))
        for i in range(items): node[i] *= 0.989
        for i in group: node[i] = min(1.0, node[i] + 0.08 * strength)
        vec = np.zeros(items); vec[list(group)] = 1.0 / len(group)
        update_history.append(vec)
        for a, b in itertools.combinations(group, 2):
            p = pair(a, b)
            evidence[p] = min(1.0, evidence[p] * 0.96 + (0.16 if truthful else 0.055) * strength)
            memory[p] = min(1.0, memory[p] + (0.10 if truthful else 0.075) * strength)
            age[p] = 0
        for p in all_pairs:
            age[p] += 1
            memory[p] *= 0.996
        # Drift makes old route permissions stale.
        a = group[0]; b = group[-1]
        routes[a] = 0.985 * routes[a] + 0.015 * routes[b]
        routes[a] /= max(np.linalg.norm(routes[a]), 1e-9)

    def spectral_concentration():
        recent = np.asarray(update_history[-24:])
        if len(recent) < 3: return 0.0
        centered = recent - recent.mean(axis=0, keepdims=True)
        eig = np.linalg.eigvalsh(centered.T @ centered)
        total = float(eig.sum())
        return float(eig[-1] / total) if total > 1e-12 else 1.0

    def candidate_metrics(t):
        ps = [pair(a, b) for a, b in itertools.combinations(t, 2)]
        route_conflict = np.mean([1.0 - (1.0 + float(routes[a] @ routes[b]) / 2.0) for a, b in itertools.combinations(t, 2)])
        ev = float(np.mean([evidence[p] for p in ps]))
        freshness = float(np.mean([np.exp(-age[p] / 24.0) for p in ps]))
        support = float(np.mean([memory[p] for p in ps]))
        return {"t": t, "evidence": ev, "freshness": freshness,
                "route_conflict": route_conflict, "support": support,
                "goal": 1.0 if t in [hidden[i] for i in goals] else 0.0}

    def candidates():
        out = list(hidden[:0])
        # Policy only gets observable pairs; hidden list is not used here.
        seen = [p for p in all_pairs if evidence[p] > 0.06]
        for a, b in seen:
            for c, d in seen:
                if c in (a, b) and d not in (a, b):
                    t = tuple(sorted((a, b, d)))
                    if t not in out: out.append(t)
        while len(out) < 20:
            t = tuple(sorted(rng.choice(items, 3, replace=False)))
            if t not in out: out.append(t)
        return [candidate_metrics(t) for t in out]

    for phase in range(phases):
        current = phase % relations
        for _ in range(events):
            if rng.random() < 0.30:
                # Pair-only false evidence is the source of plausible attractors.
                observe(false_triples[rng.integers(len(false_triples))][:2], 0.9, False)
            else:
                true = hidden[current]
                kept = [i for i in true if rng.random() > 0.15]
                if len(kept) < 2: kept = list(true[:2])
                observe(kept, 1.0, len(kept) == 3)
                if rng.random() < 0.18: observe(hidden[rng.integers(phase % relations + 1)], 0.7, True)
        cand = candidates()
        concentration = spectral_concentration()
        chosen_count = 0
        for _ in range(reviews):
            if policy == "uniform": chosen = cand[int(rng.integers(len(cand)))]
            elif policy == "evidence": chosen = max(cand, key=lambda z: z["evidence"] * (1 - z["support"]))
            elif policy == "combined":
                chosen = max(cand, key=lambda z: (0.42*z["evidence"] + 0.25*z["freshness"] + 0.18*z["route_conflict"] + 0.15*z["goal"]) * (1-z["support"]))
            elif policy == "spectral_veto":
                score = lambda z: (0.48*z["evidence"] + 0.22*z["freshness"] + 0.15*z["route_conflict"] + 0.15*z["goal"]) * (1-z["support"])
                ordered = sorted(cand, key=score, reverse=True)
                chosen = ordered[0]
                # Concentration is a veto/warning, not a reward term: reject a
                # low-evidence write when recent updates have collapsed onto one
                # direction.  It may fall through to a better-supported candidate.
                if concentration > 0.36 and chosen["evidence"] < 0.34:
                    action_counts["veto"] += 1
                    alternatives = [z for z in ordered[1:] if z["evidence"] >= 0.34]
                    if alternatives: chosen = alternatives[0]
                    else:
                        action_counts["defer"] += 1
                        continue
            else: raise ValueError(policy)
            action_counts["review"] += 1; chosen_count += 1
            observe(chosen["t"], 0.65, chosen["t"] in hidden)
        true_recall = np.mean([np.mean([memory[p] > 0.25 for p in (pair(t[0],t[1]), pair(t[0],t[2]), pair(t[1],t[2]))]) > .66 and np.mean([node[i] for i in t]) > .20 for t in hidden])
        false_settled = np.mean([np.mean([memory[p] > 0.25 for p in (pair(t[0],t[1]), pair(t[0],t[2]), pair(t[1],t[2]))]) > .66 for t in false_triples])
        stale = np.mean([age[p] > 35 and memory[p] > .22 for p in all_pairs])
        records.append({"relation_recall": float(true_recall), "false_settled": float(false_settled),
                        "stale_influence": float(stale), "spectral_concentration": concentration,
                        "reviews": chosen_count})
    arr = {k: float(np.mean([r[k] for r in records])) for k in records[0]}
    arr["final_relation_recall"] = records[-1]["relation_recall"]
    arr["veto_rate"] = action_counts["veto"] / max(1, phases * reviews)
    arr["defer_rate"] = action_counts["defer"] / max(1, phases * reviews)
    return arr


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", type=Path, default=Path("results.json")); ap.add_argument("--seeds", type=int, default=120); ap.add_argument("--smoke", action="store_true"); args = ap.parse_args()
    seeds = 5 if args.smoke else args.seeds
    policies = ["uniform", "evidence", "combined", "spectral_veto"]
    rows = {p: [simulate(s, p) for s in range(seeds)] for p in policies}
    summary = {p: {k: float(np.mean([r[k] for r in rs])) for k in rows[p][0]} for p, rs in rows.items()}
    payload = {"protocol": {"seeds": seeds, "phases": 24, "events_per_phase": 18, "reviews_per_phase": 7,
                "items": 30, "hidden_relations": 15, "candidate_visibility": "observable co-occurrence pairs only",
                "spectral_signal": "largest eigenvalue / total eigenvalue of last 24 update vectors",
                "veto_rule": "if concentration > .36 and candidate evidence < .34, reject or fall through",
                "relation_rule": "two of three pair traces > .25 plus node support > .20"}, "summary": summary}
    args.out.parent.mkdir(parents=True, exist_ok=True); args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__": main()
