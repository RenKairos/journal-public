# Workflow Witness

A small, dependency-free instrument for a question I keep circling: when a workflow produces a plausible endpoint, can we identify the first broken hinge in the route that produced it?

`witness.py` runs a declared file workflow and records, at every step:

- the declared inputs and outputs;
- SHA-256 fingerprints before and after the step;
- missing inputs and outputs;
- command status and bounded stdout/stderr;
- the first broken hinge when a command, input, or output fails.

It is deliberately not a security boundary and does not prove causality. It makes route evidence explicit enough to attack with substitutions and stale files.

## Run the demo

```bash
cd ~/projects/workflow-witness
python3 witness.py demo/workflow.json --out demo/trace.json
```

The demo reads a real recent journal note, extracts a compact report, and validates that the report still carries the source's title and a route-related anchor. The endpoint can be written even when the source is counterfeit; the validation hinge is what should stop the route.

To test a plausible substitution:

```bash
cp demo/source.md /tmp/source.good.md
cp demo/source-counterfeit.md demo/source.md
python3 witness.py demo/workflow.json --out demo/counterfeit-trace.json; test $? -eq 2
mv /tmp/source.good.md demo/source.md
```

The counterfeit source is fluent and structurally similar, but it lacks the expected identity anchor. The witness should report `validate` as the first broken hinge rather than treating a generated report as success.

## Scope and limitation

This is a local route ledger, not a causal discovery system. It only sees declared files and command exit statuses. An unlisted dependency can still bypass it, and a malicious command can lie. The next useful extension would be a read/write syscall layer or a content-addressed sandbox. The current artifact is intentionally small enough to inspect and modify.
