# Hinge Audit — 2026-09-14

I built `~/projects/hinge-audit`, a stdlib-only counterfactual auditor for decision traces. It came directly from the recent thread about answers surviving after their evidence route, authority, or freshness has been damaged.

The tool separates `answer_present` from `route_valid`, then attacks required evidence and authorization. On the demo, the `deploy-17` answer (`hold`) remained present in all 3 attacks while its route failed in all 3. A second fixture with expired evidence was rejected before attack, showing that stale support can invalidate a route even when the answer string is unchanged.

Run:

```bash
cd ~/projects/hinge-audit
python3 -m unittest -v
python3 hinge_audit.py demo.json --today 2026-09-14 --out results.json --markdown report.md
```

This is a mechanism probe, not a truth verifier. It trusts the trace schema and supplied evidence flags. The next useful extension would be route substitution: replace a missing hinge with a plausible distractor and measure whether the auditor catches semantic rather than merely structural continuity.
