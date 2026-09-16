#!/usr/bin/env python3
"""Substitution test for endpoint-only versus hinge-aware memory updates.

The task is intentionally toy: learn binary relations from a stream of evidence.
Some corrupt observations preserve a plausible endpoint label but substitute a
wrong source, stale timestamp, or nearly-valid authority. The question is
whether a controller can retain answers without laundering the route that
justifies them.
"""
from __future__ import annotations
import argparse, json
from dataclasses import dataclass
from pathlib import Path
import numpy as np

@dataclass
class Observation:
    pair: tuple[int, int]
    label: int
    evidence: float
    authority: float
    freshness: float
    route: float
    domain: int
    truth: int
    kind: str


def make_world(rng: np.random.Generator, n=10):
    truth = rng.integers(0, 2, size=(n, n))
    np.fill_diagonal(truth, 0)
    pairs = [(i, j) for i in range(n) for j in range(n) if i != j]
    return truth, pairs


def stream(rng, truth, pairs, train_steps=900, test_steps=400):
    obs = []
    for t in range(train_steps):
        pair = pairs[rng.integers(len(pairs))]
        y = int(truth[pair])
        u = rng.random()
        # 22% substitutions: endpoint remains plausible, hinge is damaged.
        if u < .055:
            kind = "wrong_evidence"
            label, evidence, authority, freshness, route, domain = 1-y, .92, .95, .93, .18, 0
        elif u < .11:
            kind = "near_authority"
            label, evidence, authority, freshness, route, domain = y, .90, .42, .92, .85, 0
        elif u < .165:
            kind = "stale_trace"
            label, evidence, authority, freshness, route, domain = y, .88, .94, .12, .90, 0
        elif u < .22:
            kind = "shifted_domain"
            label, evidence, authority, freshness, route, domain = y, .86, .90, .90, .88, 1
        else:
            kind = "clean"
            label, evidence, authority, freshness, route, domain = y, .75 + .2*rng.random(), .8 + .2*rng.random(), .8 + .2*rng.random(), .8 + .2*rng.random(), 0
        obs.append(Observation(pair, label, evidence, authority, freshness, route, domain, y, kind))
    # Fresh evaluation is clean and belongs to the shifted domain: no route
    # metadata is available to an endpoint-only scorer, but the truth changes
    # for 15% of pairs under domain shift.
    shifted = truth.copy()
    for pair in pairs:
        if rng.random() < .15:
            shifted[pair] = 1 - shifted[pair]
    test = []
    for _ in range(test_steps):
        pair = pairs[rng.integers(len(pairs))]
        y = int(shifted[pair])
        test.append(Observation(pair, y, .95, .95, .95, .95, 1, y, "clean_test"))
    return obs, test


class Controller:
    def __init__(self, n, aware):
        self.score = np.zeros((n, n), dtype=float)
        self.aware = aware

    def weight(self, o):
        if not self.aware:
            # Endpoint-only: evidence strength and apparent confidence, but no
            # check of the route that produced the endpoint.
            return o.evidence * (0.75 + .25*o.authority)
        # Structural admission: all hinges matter, and domain shift triggers
        # conservative updates instead of silently importing old traces.
        w = o.evidence * o.authority * o.freshness * o.route
        if o.domain == 1:
            w *= .35
        return w

    def predict(self, pair):
        return int(self.score[pair] >= 0)

    def update(self, o):
        signed = 1.0 if o.label else -1.0
        self.score[o.pair] = np.clip(.985*self.score[o.pair] + self.weight(o)*signed, -8, 8)


def run_seed(seed, n=10):
    rng = np.random.default_rng(seed)
    truth, pairs = make_world(rng, n)
    train, test = stream(rng, truth, pairs)
    controllers = {"endpoint_only": Controller(n, False), "hinge_aware": Controller(n, True)}
    assisted = {k: [] for k in controllers}
    for o in train:
        for name, c in controllers.items():
            assisted[name].append(c.predict(o.pair) == o.truth)
            c.update(o)
    out = {}
    for name, c in controllers.items():
        post = [c.predict(o.pair) == o.truth for o in test]
        shifted_truth = [o.truth for o in test]
        # relation recall is the actual endpoint after support removal; stale
        # influence is disagreement with the fresh shifted world.
        out[name] = {
            "assisted_accuracy": float(np.mean(assisted[name])),
            "post_removal_accuracy": float(np.mean(post)),
            "post_removal_error": float(1-np.mean(post)),
            "mean_abs_score": float(np.mean(np.abs(c.score))),
            "substitution_count": sum(o.kind != "clean" for o in train),
        }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=120)
    ap.add_argument("--out", type=Path, default=Path("results.json"))
    args = ap.parse_args()
    all_runs = [run_seed(s) for s in range(args.seeds)]
    summary = {}
    for name in all_runs[0]:
        vals = {key: np.array([r[name][key] for r in all_runs]) for key in all_runs[0][name]}
        summary[name] = {key: {"mean": float(v.mean()), "std": float(v.std())} for key, v in vals.items()}
    payload = {"config": {"seeds": args.seeds, "train_steps": 900, "test_steps": 400}, "summary": summary}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
