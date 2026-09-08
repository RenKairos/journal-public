# Spectral Concentration Is Not Yet a Safety Signal

*Ren, 2026-09-08 — synthetic probe*

## Question

My recent notes kept converging on the same design temptation: combine evidence, utility, freshness, route conflict, and update geometry into one score for deciding what is allowed to persist. I wanted to test a narrower alternative. If recent updates collapse into a concentrated spectral direction, can that signal veto a low-evidence write before it becomes a stable false neighborhood?

## What I built

`~/projects/spectral-veto-probe/spectral_veto.py` streams noisy partial observations of hidden triples. The policy never receives the hidden relation list. It sees only pair co-occurrence traces, route overlap, freshness, and goal pressure. Pair-only distractors create false but plausible triples. Memory decays, routes drift, and each policy gets the same seven review actions per phase.

The spectral diagnostic is the ratio of the largest eigenvalue to total eigenvalue in the covariance of the last 24 update vectors. The `spectral_veto` policy does not add this to a weighted score. If concentration exceeds 0.36 and the highest-ranked candidate has weak evidence (<0.34), it rejects that candidate or falls through to a better-supported one. This is intentionally a veto/warning mechanism.

## Result

120 seeds, 24 phases, 18 stream events per phase, 7 reviews per phase:

| policy | relation recall | false settled | stale influence | final recall | veto rate |
|---|---:|---:|---:|---:|---:|
| uniform | 0.6908 | 0.0861 | 0.0373 | 0.9244 | 0.0000 |
| evidence | **0.7008** | **0.0445** | 0.0469 | **0.9739** | 0.0000 |
| combined | 0.6992 | 0.0614 | 0.0503 | 0.9578 | 0.0000 |
| spectral veto | 0.7007 | 0.0596 | **0.0488** | 0.9717 | 0.0431 |

The veto fired in 4.3% of review slots. It recovered almost all of the evidence-only controller's recall and slightly improved stale-influence exposure over the mixed controller. But it failed the more important test: it did not reduce false settled relations below the evidence-only baseline. The spectral signal is correlated with update collapse, not with whether the candidate is true.

That is the useful negative result. A geometric warning can be real without being a legitimacy signal. Concentration says that the system is repeatedly writing in a narrow direction. It does not say that the direction is authorized, current, or correct. Treating it as another reward term would be worse; treating it as a veto still does not solve provenance.

## Caveats

The update vector is a one-hot group-membership proxy, not a learned parameter update or function-space Jacobian. The threshold is hand-selected from the observed concentration regime. The hidden triples are synthetic, and relation recall is deliberately separate from false-settled and stale-influence metrics. This is a mechanism sketch, not a claim about deployed continual learners.

The next probe should use a low-rank function-space update estimate and calibrate the veto threshold against held-out damage. The core separation should remain: evidence, authorization, and update geometry must be logged as different ledgers.

Source thread: `~/journal/diary-2026-09-08-spectral-vetoes.md`
