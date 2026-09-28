# Provenance Gate Probe

A small falsifiable experiment from Ren's 2026-09-28 journal question:

> Can a continual learner know when it is not entitled to route an input into an existing memory partition?

## Mechanism

Two tasks share a 2-D input space but use conflicting label rules. A noisy third feature acts as a provenance marker. During the middle of the stream, the marker becomes ambiguous. Three policies learn task-specific linear classifiers:

- `oracle`: receives the hidden task identity;
- `forced`: always routes to the highest-scoring partition;
- `quarantine`: abstains when the route margin is below a threshold and does not update either partition.

The probe measures route accuracy, cross-task contamination, immediate stream accuracy, and clean/ambiguous evaluation accuracy after the stream. It tests whether refusing to write under uncertainty protects future behavior, even if it reduces coverage.

## Run

```bash
/usr/bin/python3 provenance_gate.py --seeds 40 --out results.json
python3 -m unittest -v
```

The default run is dependency-light beyond NumPy and completes quickly on Kairos.

## Result

See `results.json` for numbers from the executed run. The important comparison is not whether quarantine wins every metric: it should trade coverage for lower contamination. If it does not, the gate is not buying anything in this mechanism.

## Limitations

This is a toy mechanism probe, not evidence about production continual-learning systems. The provenance marker is an explicit scalar, the classifier is linear, and the quarantine policy gets an engineered margin threshold. The experiment does not establish that a real model can learn a calibrated authorization boundary. Its value is narrower: it makes the cost of forced routing visible under a controlled overlap regime.

Source journal entries:

- `~/journal/diary-2026-09-28-the-route-is-not-the-result.md`
- `~/journal/reading/2026-09-28-code-judge-grounding.md`
- `~/journal/reading/2026-09-27-stacknet-task-identity.md`
