# Hinge Audit

A tiny, dependency-free counterfactual auditor for decision traces.

Recent journal entries kept returning to one distinction: an answer can remain
stable after the route that justified it has been damaged. Hinge Audit makes
that failure visible by attacking required evidence and authorization, then
reporting the answer field and inspectability route separately.

## Run

```bash
python3 hinge_audit.py demo.json --today 2026-09-14 \
  --out results.json --markdown report.md
```

The input is JSON containing `decisions`. Each decision has an `answer`,
`authorized` flag, `required_evidence`, `route`, and evidence objects with
`id`, `observed`, and optional ISO `expires_at`.

## What it measures

- evidence presence and freshness;
- authorization;
- whether the declared route is still connected to valid evidence;
- whether the answer remains present during attacks;
- route fragility across generated attacks.

This is a mechanism probe, not a truth verifier. It assumes the trace's schema
is meaningful and does not judge evidence quality beyond the supplied flags.
The useful negative result is precisely when `answer_present` survives while
`route_valid` fails.

## Test

```bash
python3 -m unittest -v
```
