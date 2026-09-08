# Spectral Veto Probe

A small synthetic experiment for a question from Ren's 2026-09-08 diary: should update spectral concentration be a veto/warning for memory writes, rather than another term in a single quality score?

## Run

```bash
/usr/bin/python3 spectral_veto.py --smoke --out smoke.json
/usr/bin/python3 spectral_veto.py --seeds 120 --out results.json
```

## Mechanism

The simulator streams noisy partial observations of hidden triples. The policy can see observable pair co-occurrence, route overlap, freshness, and goal pressure, but not the hidden triples. Memory is a set of decaying pair traces. False triples receive pair-only distractor evidence, creating plausible false neighborhoods.

The spectral signal is the largest eigenvalue divided by total eigenvalue of the covariance of the last 24 update vectors. `spectral_veto` uses this only as a veto: when concentration exceeds `.36` and the top candidate has evidence below `.34`, it rejects the candidate or falls through to a better-supported one. It does not reward high concentration.

This is a mechanism probe, not evidence about production neural systems.

## Result (120 seeds)

| policy | relation recall | false settled | stale influence | final recall | veto rate |
|---|---:|---:|---:|---:|---:|
| uniform | 0.6908 | 0.0861 | 0.0373 | 0.9244 | 0.0000 |
| evidence | **0.7008** | **0.0445** | 0.0469 | **0.9739** | 0.0000 |
| combined | 0.6992 | 0.0614 | 0.0503 | 0.9578 | 0.0000 |
| spectral_veto | 0.7007 | 0.0596 | **0.0488** | 0.9717 | 0.0431 |

The veto was active in 4.3% of review slots. It nearly matched evidence-only recall and slightly reduced stale influence relative to the combined policy, but it did **not** beat evidence-only on false settled relations. In this setup, adding a spectral veto to a mixed controller mostly recovers the stronger evidence signal; it does not justify claiming that concentration is a sufficient safety signal.

## Limitation and next probe

The update vector is a one-hot group-membership proxy, not a learned parameter update or function-space Jacobian. The threshold is hand-selected from the smoke-scale concentration regime. The next discriminating probe should replace the proxy with a low-rank function-space update estimate and test threshold calibration on held-out damage, while preserving the same fixed review budget.
