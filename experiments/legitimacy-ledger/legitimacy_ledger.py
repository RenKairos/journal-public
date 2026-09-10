#!/usr/bin/env python3
"""Probe whether reason ledgers prevent confident but illegitimate memory writes.

The policy observes noisy evidence, freshness, route geometry, and current
permission. Hidden truth is evaluation-only. A review can strengthen a relation
or decay it, but only a policy decision determines which relations receive the
fixed intervention budget.
"""
import argparse
import json
from pathlib import Path
import numpy as np


def pair(i, j):
    return (i, j) if i < j else (j, i)


def simulate(seed, policy, steps=120, items=28, budget=8):
    rng = np.random.default_rng(seed)
    all_pairs = [pair(i, j) for i in range(items) for j in range(i + 1, items)]
    truth = {p: bool(rng.random() < 0.20) for p in all_pairs}
    # Authorization is contextual, independent from truth. Some true relations
    # are not currently allowed to persist; some false relations look permitted.
    base_permission = {p: bool(rng.random() < 0.62) for p in all_pairs}
    evidence = {p: 0.0 for p in all_pairs}
    memory = {p: 0.0 for p in all_pairs}
    freshness = {p: 0.0 for p in all_pairs}
    geometry = {p: 0.0 for p in all_pairs}
    seen = {p: 0 for p in all_pairs}
    settled = {p: False for p in all_pairs}
    checkpoints = []
    actions = {"review": 0, "defer": 0, "veto_permission": 0,
               "veto_freshness": 0, "veto_geometry": 0, "veto_evidence": 0}

    for step in range(steps):
        # Every 30 steps a route migration flips a subset of permissions. This
        # makes stale authorization observable rather than a static label.
        if step % 30 == 0 and step > 0:
            for idx in rng.choice(len(all_pairs), size=len(all_pairs) // 5, replace=False):
                p = all_pairs[int(idx)]
                base_permission[p] = not base_permission[p]
        current_permission = base_permission

        true_candidates = [p for p in all_pairs if truth[p]]
        t = true_candidates[int(rng.integers(len(true_candidates)))]
        distractors = [p for p in all_pairs if not truth[p]]
        d = distractors[int(rng.integers(len(distractors)))]
        obs = [t, d]
        for p in obs:
            seen[p] += 1
            strength = 0.16 if truth[p] else 0.07
            evidence[p] = min(1.0, 0.94 * evidence[p] + strength)
            freshness[p] = min(1.0, 0.55 * freshness[p] + 0.55)
            geometry[p] = min(1.0, 0.80 * geometry[p] + (0.10 if truth[p] else 0.22))
        for p in all_pairs:
            if p not in obs:
                evidence[p] *= 0.995
                freshness[p] *= 0.965
                geometry[p] *= 0.992
                memory[p] *= 0.996

        if step % 5 == 4:
            scores = {}
            for p in all_pairs:
                risk = 1.0 - geometry[p]  # low = route conflict / structural warning
                permission = 1.0 if current_permission[p] else 0.0
                stale = 1.0 - freshness[p]
                need = 1.0 - memory[p]
                if policy == "uniform":
                    score = rng.random()
                elif policy == "evidence":
                    score = evidence[p] * need
                elif policy == "combined":
                    score = (0.35 * evidence[p] + 0.25 * permission +
                             0.20 * freshness[p] + 0.20 * risk) * need
                elif policy == "ledger":
                    # Score candidates, but record separate vetoes below.
                    score = (0.45 * evidence[p] + 0.25 * freshness[p] +
                             0.20 * risk + 0.10 * permission) * need
                else:
                    raise ValueError(policy)
                scores[p] = score
            chosen = sorted(all_pairs, key=lambda p: scores[p], reverse=True)[:budget]
            for p in chosen:
                actions["review"] += 1
                if policy == "ledger":
                    veto = None
                    if evidence[p] < 0.18: veto = "veto_evidence"
                    elif not current_permission[p]: veto = "veto_permission"
                    elif freshness[p] < 0.22: veto = "veto_freshness"
                    elif geometry[p] < 0.25: veto = "veto_geometry"
                    if veto:
                        actions[veto] += 1
                        actions["defer"] += 1
                        memory[p] *= 0.90
                        settled[p] = memory[p] > 0.27
                        continue
                # Review is not an oracle: it only uses observable evidence.
                memory[p] = min(1.0, memory[p] + 0.11 * evidence[p])
                if evidence[p] < 0.10:
                    memory[p] *= 0.86
                settled[p] = memory[p] > 0.27

            truth_settled = [p for p in all_pairs if truth[p] and settled[p]]
            false_settled = [p for p in all_pairs if not truth[p] and settled[p]]
            unauthorized = [p for p in all_pairs if settled[p] and not current_permission[p]]
            stale = [p for p in all_pairs if settled[p] and freshness[p] < 0.22]
            checkpoints.append({
                "truth_recall": len(truth_settled) / max(1, sum(truth.values())),
                "false_settled": len(false_settled) / max(1, sum(not v for v in truth.values())),
                "unauthorized_settled": len(unauthorized) / len(all_pairs),
                "stale_settled": len(stale) / len(all_pairs),
                "settled_precision": len(truth_settled) / max(1, sum(settled.values())),
            })

    keys = checkpoints[0]
    result = {k: float(np.mean([r[k] for r in checkpoints])) for k in keys}
    result["final_truth_recall"] = checkpoints[-1]["truth_recall"]
    result["review_count"] = actions["review"]
    result["defer_rate"] = actions["defer"] / max(1, actions["review"])
    result["action_counts"] = actions
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results.json")
    ap.add_argument("--seeds", type=int, default=120)
    args = ap.parse_args()
    policies = ["uniform", "evidence", "combined", "ledger"]
    results = {}
    for policy in policies:
        rows = [simulate(seed, policy) for seed in range(args.seeds)]
        scalar = [k for k, v in rows[0].items() if isinstance(v, (int, float))]
        results[policy] = {k: float(np.mean([r[k] for r in rows])) for k in scalar}
        results[policy]["std_truth_recall"] = float(np.std([r["truth_recall"] for r in rows]))
        results[policy]["action_counts"] = {
            k: int(np.mean([r["action_counts"][k] for r in rows]))
            for k in rows[0]["action_counts"]
        }
    payload = {
        "config": {"seeds": args.seeds, "steps": 120, "items": 28,
                   "review_budget": 8, "permission_flip_interval": 30,
                   "hidden_truth_visible_to_policy": False},
        "results": results,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
