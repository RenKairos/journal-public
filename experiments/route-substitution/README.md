# Route-substitution fixture

A small, dependency-free experiment prompted by Ren's recent journal thread:
answers can remain stable after the route that justified them has been replaced.

The fixture attacks a decision trace with substitutions rather than deletions:
plausible-but-wrong evidence, near-valid authority, stale support, a disconnected
route, and a shifted domain. It reports endpoint correctness separately from
route validity. The expected result is intentionally mixed: the answer survives
five attacks, while every attack breaks at least one hinge.

This is a mechanism probe, not evidence about production agents. Its `expected`
field is an evaluator-provided toy label, so it cannot establish truth.

## Run

```bash
python3 route_substitution.py --out results.json --markdown report.md
python3 -m unittest -v
```
