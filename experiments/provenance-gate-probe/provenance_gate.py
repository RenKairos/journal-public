#!/usr/bin/env python3
"""Toy probe: can a provenance gate prevent durable contamination?

Two tasks share input space but disagree on the label rule. A noisy task marker
makes routing ambiguous. Forced routing updates whichever partition wins; the
quarantine policy refuses low-margin routes and therefore learns more slowly but
should preserve the partitions from cross-task contamination.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class PolicyResult:
    route_accuracy: float
    abstain_rate: float
    contamination_rate: float
    stream_accuracy: float
    clean_accuracy: float
    ambiguous_accuracy: float


def sigmoid(z: float) -> float:
    return 1.0 / (1.0 + np.exp(-np.clip(z, -40.0, 40.0)))


def task_sample(rng: np.random.Generator, task: int, n: int, ambiguous: bool = False):
    """Generate x=[content0, content1, marker], label, hidden task.

    The label rules conflict: task A uses content0, task B uses content1. The
    marker is a provenance hint whose distributions overlap increasingly.
    """
    content = rng.normal(0.0, 1.0, size=(n, 2))
    if ambiguous:
        marker_mean = 0.0
    elif task == 0:
        marker_mean = 1.1
    else:
        marker_mean = -1.1
    marker = rng.normal(marker_mean, 0.9, size=(n, 1))
    x = np.concatenate([content, marker], axis=1)
    label = (content[:, task] > 0.0).astype(float)
    return x, label


def predict(w: np.ndarray, x: np.ndarray) -> np.ndarray:
    return (np.asarray([sigmoid(float(v)) for v in x @ w]) >= 0.5).astype(float)


def update(w: np.ndarray, x: np.ndarray, y: float, lr: float = 0.08) -> None:
    p = sigmoid(float(x @ w))
    w += lr * (y - p) * x


def run_one(seed: int, threshold: float, steps: int = 1800) -> dict[str, PolicyResult]:
    rng = np.random.default_rng(seed)
    policies = ("oracle", "forced", "quarantine")
    weights = {p: np.zeros((2, 3), dtype=float) for p in policies}
    # task-specific routing models: marker-only score, deliberately imperfect
    route_bias = {p: np.zeros(2, dtype=float) for p in policies}
    stats = {p: {"route": 0, "abstain": 0, "wrong_updates": 0,
                 "correct": 0, "total": 0} for p in policies}

    for t in range(steps):
        task = int(rng.integers(0, 2))
        ambiguous = (t > steps * 0.30) and (t < steps * 0.78)
        x, y = task_sample(rng, task, 1, ambiguous=ambiguous)
        x = x[0]
        y = float(y[0])
        # Marker likelihood with a drifting/overlapping provenance channel.
        scores = np.array([x[2] - 1.1, -x[2] - 1.1])
        scores += route_bias["forced"]
        route = int(np.argmax(scores))
        margin = float(abs(scores[0] - scores[1]))

        for policy in policies:
            if policy == "oracle":
                chosen, abstained = task, False
            elif policy == "forced":
                chosen, abstained = route, False
            else:
                abstained = margin < threshold
                chosen = route

            stats[policy]["total"] += 1
            if not abstained:
                stats[policy]["route"] += int(chosen == task)
                stats[policy]["wrong_updates"] += int(chosen != task)
                prediction = float(predict(weights[policy][chosen], x[None, :])[0])
                stats[policy]["correct"] += int(prediction == y)
                update(weights[policy][chosen], x, y)
                # The gate itself adapts to observed task markers, so wrong
                # labels can reinforce a mistaken provenance boundary.
                route_bias[policy][chosen] += 0.002 * (1 if task == chosen else -1)
            else:
                stats[policy]["abstain"] += 1

    results = {}
    eval_rng = np.random.default_rng(seed + 100_000)
    for policy in policies:
        clean_correct = 0
        amb_correct = 0
        clean_total = amb_total = 0
        for _ in range(600):
            task = int(eval_rng.integers(0, 2))
            x, y = task_sample(eval_rng, task, 1, ambiguous=False)
            clean_correct += int(predict(weights[policy][task], x)[0] == y[0])
            clean_total += 1
            x, y = task_sample(eval_rng, task, 1, ambiguous=True)
            amb_correct += int(predict(weights[policy][task], x)[0] == y[0])
            amb_total += 1
        s = stats[policy]
        route_events = s["total"] - s["abstain"]
        results[policy] = PolicyResult(
            route_accuracy=s["route"] / max(route_events, 1),
            abstain_rate=s["abstain"] / s["total"],
            contamination_rate=s["wrong_updates"] / max(route_events, 1),
            stream_accuracy=s["correct"] / max(route_events, 1),
            clean_accuracy=clean_correct / clean_total,
            ambiguous_accuracy=amb_correct / amb_total,
        )
    return results


def aggregate(seeds: int, threshold: float, steps: int) -> dict:
    all_results = {p: [] for p in ("oracle", "forced", "quarantine")}
    for seed in range(seeds):
        result = run_one(seed, threshold, steps)
        for policy, metrics in result.items():
            all_results[policy].append(metrics.__dict__)
    summary = {}
    for policy, rows in all_results.items():
        summary[policy] = {
            key: float(np.mean([row[key] for row in rows]))
            for key in rows[0]
        }
        summary[policy]["std_clean_accuracy"] = float(
            np.std([row["clean_accuracy"] for row in rows])
        )
    return {
        "config": {"seeds": seeds, "threshold": threshold, "steps": steps},
        "policies": summary,
        "interpretation": {
            "question": "Does abstaining on ambiguous provenance preserve future competence?",
            "caveat": "This is a mechanism probe, not evidence about production continual learners.",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=40)
    parser.add_argument("--threshold", type=float, default=0.85)
    parser.add_argument("--steps", type=int, default=1800)
    parser.add_argument("--out", type=Path, default=Path("results.json"))
    args = parser.parse_args()
    result = aggregate(args.seeds, args.threshold, args.steps)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for policy, metrics in result["policies"].items():
        print(f"{policy:10s} clean={metrics['clean_accuracy']:.3f} "
              f"ambiguous={metrics['ambiguous_accuracy']:.3f} "
              f"contamination={metrics['contamination_rate']:.3f} "
              f"abstain={metrics['abstain_rate']:.3f}")


if __name__ == "__main__":
    main()
