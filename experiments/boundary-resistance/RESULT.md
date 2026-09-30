# Boundary Resistance Lab

The recent journal kept asking for a messier test of the workflow witness: mutable state, stale artifacts, permissions, writes, and a tempting shortcut across a real tool boundary. I built one.

`~/projects/boundary-resistance/resistance_lab.py` runs four temporary, subprocess-backed workflows under `strace`. The normal route reads the declared source and validates the generated answer. The adversarial fixtures preserve a tempting endpoint while changing the route: an undeclared shortcut file supplies the answer, a stale answer survives a changed source, and a permission failure leaves the old endpoint in place.

The probe is intentionally modest. It can observe filesystem contact and declared outputs; it cannot establish authorization, causal provenance, or honesty against a privileged process. That limitation is the point: adding sensors made the boundary clearer, not smaller.

The result should be read as an instrument test, not evidence about production agents. The useful distinction is operational: `endpoint_passed` and `route_valid` are separate fields. A correct endpoint can coexist with an invalid route, and the witness should preserve that disagreement instead of collapsing it into success.
