# Legitimacy Ledger Probe

A small continual-memory probe for the question: can a controller preserve truth, freshness, geometry, and permission as separate ledgers, or does authorization checking simply stop learning?

## Run

```bash
/usr/bin/python3 legitimacy_ledger.py --seeds 120 --out results.json
```

The policy cannot see hidden truth labels. It observes noisy evidence, freshness, route geometry, and a permission bit that changes every 30 steps. Every policy receives 8 review slots at each 5-step checkpoint. A review strengthens memory from observable evidence; it does not reveal truth.

Policies:

- `uniform`: random review baseline.
- `evidence`: review by evidence strength.
- `combined`: rank evidence, permission, freshness, and geometry into one score.
- `ledger`: rank candidates, then separately veto low evidence, denied permission, stale evidence, or geometry warnings.

The output reports truth recall separately from false, unauthorized, and stale settled relations. `action_counts` records why the ledger deferred a write.

This is a mechanism probe, not evidence about production memory systems. The permission bit is synthetic, and geometry is only a noisy warning signal.
