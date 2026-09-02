# Two-channel memory controller probe

A small, reproducible mechanism probe for a question from Ren's September 2026 journal: can a bounded memory controller act on both (1) relation-level structural fragility and (2) old/new update interference, rather than optimizing item weakness alone?

The simulator hides overlapping triples, adds misleading pair observations, and gives every policy the same eight interventions per phase. Policies see noisy pair evidence and derived signals, not hidden labels. The two-channel policy can spend an intervention on relation rehearsal, precision, or a conservative gate. It is intentionally synthetic: the result is a probe of mechanism, not evidence about production continual-learning systems.

## Run

```bash
/usr/bin/python3 two_channel_memory.py --out results.json --seeds 200
/usr/bin/python3 two_channel_memory.py --smoke --out smoke.json
```

`results.json` contains the protocol, per-seed runs, and averages over checkpoints. The key metrics are item recall and relational recall; the latter requires both individually present items and a surviving joint trace.
