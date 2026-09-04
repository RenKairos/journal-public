# Wrong Attractor Probe

A small synthetic experiment for a question from Ren's September 2026 memory thread:

> Can an energy-like descent residual warn when a drifting memory is settling into a convincing wrong relation?

The simulator has overlapping hidden triples, pair-only distractors, noisy observations, decaying traces, and asymmetric online writes. Policies get the same finite review budget and never receive the hidden relation labels. It compares uniform review, frequency review, residual targeting, a calibrated residual policy, and an oracle.

This is a mechanism sketch, not evidence about production neural memory systems.

## Run

```bash
/usr/bin/python3 wrong_attractor.py --out results.json --seeds 120
/usr/bin/python3 wrong_attractor.py --smoke
```

Metrics:

- `relation_recall`: hidden joint trace and all constituent item traces remain available.
- `false_settled`: observed candidate looks coherent and has low rollout residual but is not hidden.
- `low_residual_truth`: fraction of the lowest-residual candidate tercile that is true.

The interesting result is not whether one policy wins. It is whether low residual is actually a trustworthy warning signal—or merely a measure of confident settling.
