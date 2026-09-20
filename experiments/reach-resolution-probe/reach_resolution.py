#!/usr/bin/env python3
"""Toy probe: does learning to reach evidence change which experiment is safe to use?

This is intentionally a mechanism sketch, not a claim about deployed agents.
Two hidden worlds (m=0/1) are observed through one of two experiments:

  alias  : y = m xor nuisance-parity. High average information under benign
           nuisance frequencies, but catastrophically ambiguous in the hard tail.
  direct : y = m with measurement noise. Lower ideal information, but robust
           across nuisance states; it is only usable when a learned procedure
           reaches the right endpoint under a fixed budget.

The policies choose once per episode using calibration estimates. The important
separation is between reach (can the agent obtain the direct measurement?) and
resolution (does the resulting observation support a nuisance-blind decision?).
"""
from __future__ import annotations
import argparse
import json
import math
import random
from statistics import mean

NUISANCE_STATES = tuple(range(8))
# Calibration distribution is intentionally easier than evaluation: a hidden
# hard tail (odd nuisance parity) is underrepresented during selection.
CALIB_WEIGHTS = (0.40, 0.04, 0.20, 0.04, 0.14, 0.04, 0.10, 0.04)
EVAL_WEIGHTS = (0.10, 0.15, 0.10, 0.15, 0.10, 0.15, 0.10, 0.15)
DIRECT_NOISE = 0.18
DIRECT_COST = 2
BUDGET = 2


def weighted_choice(rng: random.Random, weights: tuple[float, ...]) -> int:
    r = rng.random() * sum(weights)
    acc = 0.0
    for i, w in enumerate(weights):
        acc += w
        if r <= acc:
            return i
    return len(weights) - 1


def observe(experiment: str, m: int, z: int, rng: random.Random, reachable: bool = True):
    if experiment == "alias":
        return m ^ (z % 2), 1
    if experiment == "direct" and reachable:
        y = m if rng.random() >= DIRECT_NOISE else 1 - m
        return y, DIRECT_COST
    return None, BUDGET


def majority_decoder(calibration, y: int) -> int:
    # One common decoder, deliberately forbidden from seeing z at evaluation.
    votes = [m for m, yy in calibration if yy == y]
    return 1 if mean(votes) >= 0.5 else 0 if votes else y


def select_policy(policy: str, rng: random.Random, direct_reach: float):
    # Calibration uses public descriptor pairs and a noisy estimate of what each
    # intervention achieves. The agent does not receive the hidden eval labels.
    n = 80
    alias_correct = 0
    direct_correct = 0
    direct_attempts = 0
    for _ in range(n):
        m = rng.randrange(2)
        z = weighted_choice(rng, CALIB_WEIGHTS)
        # A calibration trial knows the label, but the deployed decoder will not
        # know nuisance; this is exactly the shortcut the probe exposes.
        ya, _ = observe("alias", m, z, rng)
        alias_correct += int(ya == m)
        if rng.random() < direct_reach:
            yd, _ = observe("direct", m, z, rng)
            direct_correct += int(yd == m)
            direct_attempts += 1
    alias_score = alias_correct / n
    direct_score = direct_correct / max(1, direct_attempts)
    if policy == "average":
        return "alias" if alias_score >= direct_score else "direct"
    if policy == "robust":
        # Estimate worst parity group, then penalize experiments that can only
        # look good by averaging over nuisance states.
        alias_hard = []
        direct_hard = []
        for z in (1, 3, 5, 7):
            for m in (0, 1):
                ya, _ = observe("alias", m, z, rng)
                alias_hard.append(int(ya == m))
                direct_hard.append(1 - DIRECT_NOISE)
        alias_lower = mean(alias_hard) - 0.05
        direct_lower = mean(direct_hard) * direct_reach
        return "direct" if direct_lower > alias_lower else "alias"
    if policy == "reach-only":
        return "direct" if direct_reach >= 0.65 else "alias"
    raise ValueError(policy)


def run(seed: int, policy: str, direct_reach: float, episodes: int):
    rng = random.Random(seed)
    selected = select_policy(policy, rng, direct_reach)
    rows = []
    for _ in range(episodes):
        m = rng.randrange(2)
        z = weighted_choice(rng, EVAL_WEIGHTS)
        reachable = rng.random() < direct_reach
        chosen = selected
        y, cost = observe(chosen, m, z, rng, reachable=reachable)
        if y is None:
            # No direct route: explicit ambiguity is safer than a fabricated
            # singleton claim, but it counts as unresolved.
            pred = None
            candidate_size = 2
            false_exclusion = 0
        else:
            pred = y  # deployed nuisance-blind decoder
            candidate_size = 1
            false_exclusion = int(pred != m)
        rows.append({
            "m": m, "z": z, "hard_tail": int(z % 2 == 1),
            "selected": chosen, "reachable": int(reachable),
            "resolved": int(pred is not None),
            "correct": int(pred == m) if pred is not None else 0,
            "candidate_size": candidate_size,
            "false_exclusion": false_exclusion,
        })
    hard = [r for r in rows if r["hard_tail"]]
    return {
        "seed": seed, "policy": policy, "direct_reach": direct_reach,
        "selected": selected,
        "reach_rate": mean(r["reachable"] for r in rows),
        "resolution_rate": mean(r["resolved"] for r in rows),
        "accuracy_on_resolved": sum(r["correct"] for r in rows) / max(1, sum(r["resolved"] for r in rows)),
        "mean_candidate_set": mean(r["candidate_size"] for r in rows),
        "false_exclusion_rate": mean(r["false_exclusion"] for r in rows),
        "hard_tail_false_exclusion": mean(r["false_exclusion"] for r in hard),
    }


def summarize(rows):
    keys = ["reach_rate", "resolution_rate", "accuracy_on_resolved", "mean_candidate_set", "false_exclusion_rate", "hard_tail_false_exclusion"]
    out = {"n": len(rows), "selected_counts": {k: sum(r["selected"] == k for r in rows) for k in ("alias", "direct")}}
    for k in keys:
        out[k] = mean(r[k] for r in rows)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=200)
    ap.add_argument("--episodes", type=int, default=400)
    ap.add_argument("--out", default="results.json")
    args = ap.parse_args()
    all_results = []
    summaries = {}
    for reach in (0.25, 0.90):
        for policy in ("average", "robust", "reach-only"):
            rows = [run(1000 + i, policy, reach, args.episodes) for i in range(args.seeds)]
            key = f"{policy}@reach={reach:.2f}"
            summaries[key] = summarize(rows)
            all_results.extend(rows)
    payload = {
        "protocol": {
            "seeds": args.seeds, "episodes_per_seed": args.episodes,
            "calibration_weights": CALIB_WEIGHTS, "evaluation_weights": EVAL_WEIGHTS,
            "direct_noise": DIRECT_NOISE, "budget": BUDGET,
            "hard_tail": "odd nuisance states (50% of evaluation, 20% of calibration)",
        },
        "summaries": summaries,
        "runs": all_results,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(summaries, indent=2))

if __name__ == "__main__":
    main()
