#!/usr/bin/env python3
"""Probe whether activation similarity is a safe signal for merging hidden units.

The policy only sees activations on a narrow training manifold. Evaluation also
uses a counterfactual full-space distribution, where apparent symmetries may break.
"""
import argparse, json
from pathlib import Path
import numpy as np


def make_data(rng, n, mode):
    if mode == "manifold":
        x0 = rng.uniform(-1, 1, n)
        x1 = x0 + rng.normal(0, 0.08, n)
    else:
        x0, x1 = rng.uniform(-1, 1, (2, n))
    x = np.column_stack([x0, x1])
    y = (x0 + x1 >= 0).astype(int)
    return x, y


def init(rng, hidden=24):
    return {"W1": rng.normal(0, .8, (2, hidden)), "b1": np.zeros(hidden),
            "W2": rng.normal(0, .25, hidden), "b2": 0.0}


def forward(p, x):
    z = x @ p["W1"] + p["b1"]
    h = np.maximum(z, 0)
    logits = h @ p["W2"] + p["b2"]
    return z, h, 1 / (1 + np.exp(-np.clip(logits, -30, 30)))


def train(p, x, y, steps, lr, rng):
    n = len(y)
    for _ in range(steps):
        ix = rng.integers(n, size=min(64, n))
        xb, yb = x[ix], y[ix]
        z, h, q = forward(p, xb)
        dlog = q - yb
        dW2 = h.T @ dlog / len(ix)
        db2 = dlog.mean()
        dh = dlog[:, None] * p["W2"]
        dz = dh * (z > 0)
        dW1 = xb.T @ dz / len(ix)
        db1 = dz.mean(0)
        p["W2"] -= lr * dW2; p["b2"] -= lr * db2
        p["W1"] -= lr * dW1; p["b1"] -= lr * db1


def accuracy(p, x, y):
    return float(np.mean((forward(p, x)[2] >= .5) == y))


def corr_pairs(h):
    c = np.corrcoef(h, rowvar=False)
    pairs = [(abs(c[i, j]), i, j, float(c[i, j])) for i in range(c.shape[0]) for j in range(i) if np.isfinite(c[i, j])]
    return sorted(pairs, reverse=True)


def merge(p, i, j):
    # Replace j by i: average the incoming representation; preserve total output weight.
    p = {k: v.copy() if hasattr(v, "copy") else v for k, v in p.items()}
    p["W1"][:, i] = (p["W1"][:, i] + p["W1"][:, j]) / 2
    p["b1"][i] = (p["b1"][i] + p["b1"][j]) / 2
    p["W2"][i] += p["W2"][j]
    p["W2"][j] = 0.0
    return p


def run(seed, hidden=24, merges=4):
    rng = np.random.default_rng(seed)
    train_x, train_y = make_data(rng, 1200, "manifold")
    test_m_x, test_m_y = make_data(rng, 3000, "manifold")
    test_f_x, test_f_y = make_data(rng, 3000, "full")
    p = init(rng, hidden)
    train(p, train_x, train_y, 900, .06, rng)
    _, h, _ = forward(p, train_x)
    pairs = corr_pairs(h)
    chosen = pairs[:merges]
    q = p
    used = set()
    for _, i, j, _ in chosen:
        if i not in used and j not in used:
            q = merge(q, i, j); used |= {i, j}
    # A control merges equally many random disjoint pairs.
    inds = list(rng.permutation(hidden)); r = p; used_r = set(); random_pairs = []
    for k in range(0, min(2 * merges, hidden - 1), 2):
        i, j = int(inds[k]), int(inds[k + 1]); random_pairs.append((i, j)); r = merge(r, i, j)
    def disagreement(a, b, x):
        return float(np.mean((forward(a, x)[2] >= .5) != (forward(b, x)[2] >= .5)))
    return {"seed": seed, "top_correlations": [x[0] for x in chosen],
            "baseline": {"manifold": accuracy(p, test_m_x, test_m_y), "full": accuracy(p, test_f_x, test_f_y)},
            "correlation_merge": {"manifold": accuracy(q, test_m_x, test_m_y), "full": accuracy(q, test_f_x, test_f_y),
                                  "disagreement_vs_baseline": {"manifold": disagreement(p, q, test_m_x), "full": disagreement(p, q, test_f_x)}},
            "random_merge": {"manifold": accuracy(r, test_m_x, test_m_y), "full": accuracy(r, test_f_x, test_f_y),
                              "disagreement_vs_baseline": {"manifold": disagreement(p, r, test_m_x), "full": disagreement(p, r, test_f_x)}}}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--seeds", type=int, default=40); ap.add_argument("--out", default="results.json")
    a = ap.parse_args(); rows = [run(s) for s in range(a.seeds)]
    summary = {}
    for policy in ("baseline", "correlation_merge", "random_merge"):
        summary[policy] = {split: float(np.mean([r[policy][split] for r in rows])) for split in ("manifold", "full")}
    for policy in ("correlation_merge", "random_merge"):
        summary[policy]["disagreement_vs_baseline"] = {split: float(np.mean([r[policy]["disagreement_vs_baseline"][split] for r in rows])) for split in ("manifold", "full")}
    result = {"experiment": "counterfactual-quotient-audit", "question": "Does activation similarity on a narrow support justify merging hidden units?", "seeds": a.seeds, "summary": summary, "runs": rows}
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"summary": summary, "out": str(out.resolve())}, indent=2))

if __name__ == "__main__": main()
