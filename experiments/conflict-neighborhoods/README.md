# Conflict Neighborhoods

A synthetic probe for a question from Ren's 2026-08-31 journal entry: can a continuity mechanism discover which overlapping neighborhoods deserve rehearsal, rather than receiving relation boundaries from an oracle?

The stream contains 48 items, 24 hidden overlapping triples, and distractor pair events. A fixed review budget is given to four policies:

- `uniform`: review one random item;
- `frequency`: review the currently strongest item;
- `instability`: construct candidate triples from observed pair co-occurrence only, then rehearse the triple whose joint access is most sensitive to one-item ablation;
- `oracle`: use the hidden triples and target the weakest one (an upper-bound-style reference, though its objective is not optimized for the measured relation metric).

Run:

```bash
/usr/bin/python3 conflict_neighborhoods.py --out results.json
/usr/bin/python3 conflict_neighborhoods.py --smoke --out smoke.json
```

The result is a mechanism probe, not evidence about neural memory or language models. In particular, the simulator gives every policy the same simple strength/joint-access dynamics, and candidate discovery is restricted to triples whose three pairs have been observed. It does not solve semantic relation discovery.
