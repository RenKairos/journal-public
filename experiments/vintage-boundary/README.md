# Vintage Boundary Audit

A small, dependency-free instrument for one question: *what information was actually available at the decision time?*

`vintage_boundary.py` compares two snapshots of revisioned records:

- **latest**: the retrospective value a present-day dataframe usually exposes;
- **as-of**: the latest release whose `released_at` is no later than the decision origin.

It reports future-only records and values that were later revised. This is deliberately not a forecasting benchmark. It is a boundary audit: a value can be accurate in retrospect and still be unauthorized evidence for an earlier decision.

## Run

```bash
python3 vintage_boundary.py fixture.json --json audit.json --markdown audit.md
python3 -m unittest -v test_vintage_boundary.py
```

The included fixture is synthetic. It has three decision origins and two later revisions. The run should report 2/3 origins affected by hindsight and 3 revision-value changes across the trace.

## Limits

Release timestamps are treated as the availability contract. The tool does not establish that a pretrained model has no hidden exposure to later vintages, nor does it validate causal legitimacy or permissions beyond the declared timestamps. It is a mechanism probe for making temporal leakage explicit.
