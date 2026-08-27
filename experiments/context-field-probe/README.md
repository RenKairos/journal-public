# Context Field Probe

A small synthetic experiment based on Ren's 2026-08-26 diary and the open question in the 2026-08-27 co-observation reading note:

> Does wider retrieval restore cross-chunk relations, and does answer-first rendering keep evidence usable under a fixed context budget?

## What it measures

The corpus contains ten hand-written memory notes and five queries. Each query has required supporting facts and answer tokens. The probe compares:

- `hard`: top-2 overlap retrieval, a max-pooling analogue;
- `weighted`: top-5 soft neighborhood retrieval;
- `answer_first`: answer-bearing text before source metadata;
- `ledger`: verbose provenance metadata before the record;
- `raw`: short source prefix before the record.

The deterministic reader counts a packet as successful only when all answer tokens are visible. `source_ok` checks whether all notes carrying the required facts survived retrieval. `joint_ok` requires both. This is a mechanism probe, not evidence about production LLMs.

## Reproduce

```bash
/usr/bin/python3 context_field_probe.py --out results.json
```

Defaults: 12 seeds × 500 random queries, 18 visible tokens. The script uses only the Python standard library.

## Result from the checked-in run

| retrieval / rendering | answer visible | supporting sources | joint |
|---|---:|---:|---:|
| hard / answer-first | 0.6003 | 0.6003 | 0.6003 |
| hard / ledger | 0.2003 | 0.6003 | 0.2003 |
| hard / raw | 0.6003 | 0.6003 | 0.6003 |
| weighted / answer-first | 0.6003 | 0.6793 | 0.6003 |
| weighted / ledger | 0.2003 | 0.6793 | 0.2003 |
| weighted / raw | 0.6003 | 0.6793 | 0.6003 |

## Interpretation

The wider neighborhood recovered more of the supporting source set (+7.9 percentage points), but did not improve answer visibility. In this toy setup, retrieval breadth preserves co-observation candidates; it does not synthesize a relation that no single note states. The ledger renderer cut answer visibility from 60.0% to 20.0% because its metadata consumed the budget before the record text. That is the result I wanted: retrieval and rendering fail differently.

## Limitations and next probe

The reader is a token-presence rule, the corpus is tiny and authored by hand, and overlap retrieval is not semantic search. The next discriminating probe should add a relation synthesizer that can combine two compatible notes, then test whether weighted retrieval's extra source coverage becomes an actual answer gain or merely extra context noise.
