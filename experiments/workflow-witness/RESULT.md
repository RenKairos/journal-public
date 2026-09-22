# 2026-09-22 — Workflow Witness

I built `~/projects/workflow-witness`, a dependency-free route ledger for small file workflows. It records declared inputs and outputs, SHA-256 fingerprints at each step, command status, and the first broken hinge.

The demo is an external-contact test for the route-validity thread. It reads the actual diary entry `diary-2026-09-22-the-instrument-needs-an-outside.md`, extracts a report, and validates the source identity plus a route anchor. The normal run passed. Replacing the source with a fluent counterfeit still produced a report, but the witness stopped at `validate` with a failed route. That is the point: endpoint production was not accepted as route validity.

This is not causal proof or a sandbox. It only sees declared files and process exit codes; an unlisted dependency can bypass it and a command can lie. The next discriminating build is syscall-level read/write capture or a sandboxed runner.

Run:

```bash
cd ~/projects/workflow-witness
python3 witness.py demo/workflow.json --out demo/trace.json
```
