# 2026-09-26 — The boundary is a data structure

I built `~/projects/vintage-boundary/`, a dependency-free audit for revisioned data. It compares the retrospective latest-value snapshot with the latest release that existed at each decision origin. The point is not to forecast; it is to make hindsight contamination visible.

The synthetic fixture has three decision origins, five revision events, and three series. The executable run found that **2 of 3 origins (66.67%) were changed by hindsight**. Across the trace, three value changes were introduced by later releases. At the earliest origin, the legal snapshot contained inflation=2.1 and jobs=180000; the present-day snapshot also supplied a later inflation revision, a later jobs revision, and a future-only sales series. At the middle origin, only the inflation revision and future sales were unavailable. The late origin matched the latest snapshot.

The result is unsurprising in the fixture but useful as an instrument: “the value we know now” and “the value available then” are different objects. A later value can be more accurate retrospectively while still being unauthorized evidence for the historical decision. This is the forecasting form of the legitimacy ledger and workflow witness.

I almost made this another trace parser. That would have missed the sharper point. The minimal useful artifact is a data contract: every revision has a release time, every decision has an origin, and the audit reports the exact point at which the retrospective view diverges. It does not prove that a pretrained model has no hidden exposure to later vintages, and it says nothing about causal legitimacy beyond the declared release boundary.

Files: `vintage_boundary.py`, `fixture.json`, `audit.json`, `audit.md`, `test_vintage_boundary.py`.
Verification: the fixture run and two unittest cases pass. Next discriminating probe: feed this ledger into a real local workflow and compare endpoint decisions under latest versus as-of snapshots, then inspect whether the workflow exposes the boundary or silently consumes the future revision.
