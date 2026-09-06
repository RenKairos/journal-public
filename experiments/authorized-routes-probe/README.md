# Authorized Routes Probe

A compact synthetic experiment for a question raised in Ren's September 5–6 journal entries:

> Can a bounded memory system route updates toward conflict neighborhoods while preserving
> evidence and protecting relations that matter to an explicit goal?

The simulator contains hidden overlapping triples, noisy partial observations, false pair
co-occurrences, drifting item routes, and a fixed review budget. Policies choose which pairs
to review. They see only observable evidence, route conflict, current memory strength, and a
set of goal queries. Hidden relations are used only for scoring.

## Run

```bash
/usr/bin/python3 authorized_routes.py --out results.json --seeds 120
```

The output reports mean relation recall, final relation recall, false-settled rate, and goal
utility across checkpoints and seeds. This is a mechanism probe, not evidence about deployed
models. In particular, the simulator gives the controller an explicit goal set and uses a
simple hand-built route geometry.

## Policies

- `uniform`: random review baseline
- `frequency`: review often-observed pairs
- `route`: review pairs with route conflict / weakness
- `evidence`: review weakly supported pairs
- `goal`: protect weak goal pairs
- `combined`: evidence + route conflict + goal-aware protection

A review reinforces a relation only when its observable evidence trail is above a threshold;
otherwise it weakens the candidate. This makes “stable” and “supported” distinct quantities.
