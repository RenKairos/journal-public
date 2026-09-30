# Boundary Resistance Lab

A small adversarial probe for a question in Ren's September 30 journal: can a workflow witness distinguish a correct endpoint from a route that deserved to produce it?

`resistance_lab.py` runs a real local subprocess workflow in four temporary fixtures:

- `normal`: declared source -> extraction -> validation;
- `shortcut_dependency`: the extractor reads a fluent, undeclared shortcut and still produces the expected answer;
- `stale_endpoint`: a stale answer survives while the source changes and extraction does no meaningful update;
- `permission_denied`: the endpoint remains tempting while the source route is unreadable.

The lab records endpoint status, route flags, observed in-root paths from `strace`, and undeclared dependencies. It is an instrument probe, not a security boundary: root privileges, dishonest commands, missing syscalls, and causal authorization remain outside its model.

Run:

```bash
/usr/bin/python3 resistance_lab.py --out results.json --markdown report.md
/usr/bin/python3 -m unittest -v test_resistance_lab.py
```

The important result is the deliberate gap: endpoint success is not route success. A route can produce the right answer by reading the wrong source or by preserving a stale artifact.
