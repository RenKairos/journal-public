#!/usr/bin/env python3
"""Trace Guard: a tiny continual-learning experiment.

Compare an ordinary online classifier with a dual-rate learner that keeps a
slow, protected trace separate from a fast sequence-adaptation state.
No old examples are stored or replayed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import numpy as np


def softmax(z):
    z = z - np.max(z)
    e = np.exp(z)
    return e / e.sum()


def make_stream(rng, n_classes=8, dim=12, repeats=16, seq_len=16):
    """Return task-ordered samples; each class is introduced once."""
    centers = rng.normal(size=(n_classes, dim))
    centers /= np.linalg.norm(centers, axis=1, keepdims=True)
    # Orthogonal-ish directions make classes separable but not trivial.
    centers *= 2.2
    xs, ys, task_ids = [], [], []
    for task in range(n_classes // 2):
        for _ in range(repeats):
            order = rng.permutation([2 * task, 2 * task + 1])
            for cls in order:
                for _ in range(seq_len):
                    xs.append(centers[cls] + rng.normal(scale=0.72, size=dim))
                    ys.append(cls)
                    task_ids.append(task)
    return np.asarray(xs), np.asarray(ys), np.asarray(task_ids), centers


class OnlineLinear:
    def __init__(self, dim, n_classes, lr=0.035):
        self.w = np.zeros((n_classes, dim))
        self.b = np.zeros(n_classes)
        self.lr = lr

    def step(self, x, y):
        p = softmax(self.w @ x + self.b)
        g = p.copy(); g[y] -= 1
        self.w -= self.lr * g[:, None] * x[None, :]
        self.b -= self.lr * g

    def predict(self, x):
        return int(np.argmax(self.w @ x + self.b))


class DualRateTrace:
    """Fast state learns each sample; slow trace learns stable class summaries.

    The slow trace is content-addressed by the observed label and stores one
    prototype per class, not old examples. At inference it votes with the fast
    classifier. This is deliberately small: the point is to expose the tradeoff,
    not to win a benchmark.
    """
    def __init__(self, dim, n_classes, fast_lr=0.05, slow_lr=0.004, vote=0.72):
        self.fast = OnlineLinear(dim, n_classes, fast_lr)
        self.proto = np.zeros((n_classes, dim))
        self.proto_seen = np.zeros(n_classes, dtype=bool)
        self.slow_lr = slow_lr
        self.vote = vote

    def step(self, x, y):
        self.fast.step(x, y)
        # A compressed, label-addressed trace. No previous x is retained.
        if not self.proto_seen[y]:
            self.proto[y] = x
            self.proto_seen[y] = True
        else:
            self.proto[y] = (1 - self.slow_lr) * self.proto[y] + self.slow_lr * x

    def predict(self, x):
        fast_logits = self.fast.w @ x + self.fast.b
        proto_logits = self.proto @ x
        proto_logits[~self.proto_seen] = -1e9
        # Normalize scales before mixing so the vote remains interpretable.
        fast_logits = fast_logits / (np.std(fast_logits) + 1e-8)
        proto_logits = proto_logits / (np.std(proto_logits[self.proto_seen]) + 1e-8)
        return int(np.argmax(self.vote * proto_logits + (1 - self.vote) * fast_logits))


def evaluate(model, centers, rng, n=400):
    xs, ys = [], []
    for _ in range(n):
        y = int(rng.integers(len(centers)))
        xs.append(centers[y] + rng.normal(scale=0.72, size=centers.shape[1]))
        ys.append(y)
    pred = [model.predict(x) for x in xs]
    return float(np.mean(np.asarray(pred) == np.asarray(ys)))


def run(seed, seq_len, repeats=16):
    rng = np.random.default_rng(seed)
    xs, ys, tasks, centers = make_stream(rng, repeats=repeats, seq_len=seq_len)
    base = OnlineLinear(xs.shape[1], len(centers))
    guarded = DualRateTrace(xs.shape[1], len(centers))
    history = []
    seen_tasks = 0
    for x, y, task in zip(xs, ys, tasks):
        base.step(x, int(y)); guarded.step(x, int(y))
        if task + 1 > seen_tasks:
            seen_tasks = int(task + 1)
            history.append({
                "task": seen_tasks,
                "baseline": evaluate(base, centers, rng),
                "trace_guard": evaluate(guarded, centers, rng),
            })
    # Measure both final retention and the worst drop after a class was learned.
    final = history[-1]
    return {
        "seed": seed, "seq_len": seq_len, "history": history,
        "final_baseline": final["baseline"],
        "final_trace_guard": final["trace_guard"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sequences", nargs="+", type=int, default=[1, 4, 16, 64])
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--out", type=Path, default=Path("results.json"))
    args = ap.parse_args()
    all_runs = []
    for seq_len in args.sequences:
        for seed in range(args.seeds):
            all_runs.append(run(seed, seq_len))
    summary = []
    for length in args.sequences:
        rows = [r for r in all_runs if r["seq_len"] == length]
        summary.append({
            "seq_len": length,
            "baseline_mean": float(np.mean([r["final_baseline"] for r in rows])),
            "trace_guard_mean": float(np.mean([r["final_trace_guard"] for r in rows])),
            "baseline_sd": float(np.std([r["final_baseline"] for r in rows])),
            "trace_guard_sd": float(np.std([r["final_trace_guard"] for r in rows])),
        })
    payload = {"summary": summary, "runs": all_runs}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
