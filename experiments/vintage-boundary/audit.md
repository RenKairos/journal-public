# Vintage Boundary Audit — revision-boundary-demo

This report compares a retrospective latest-value snapshot with the newest revision that was actually released by each decision origin.

## Result

- Decision origins: **3**
- Origins changed by hindsight: **2** (66.7%)
- Revision value changes across origins: **3**

## Per-origin trace

| origin | legal values | future-only series | revised series | leakage |
|---|---|---|---|---|
| 2026-02-15T12:00:00Z | inflation=2.1, jobs=180000 | sales | inflation, jobs | YES |
| 2026-03-10T12:00:00Z | inflation=2.1, jobs=165000 | sales | inflation | YES |
| 2026-05-01T12:00:00Z | inflation=2.4, jobs=165000, sales=91 | — | — | no |

## Interpretation

A retrospective value can be accurate and still be unauthorized evidence for an earlier decision. This is a mechanism probe, not a forecast benchmark: it checks the information boundary and does not establish predictive quality.

The audit is intentionally conservative: release timestamps define availability; it does not prove that a pretrained model has no hidden exposure to later vintages.
