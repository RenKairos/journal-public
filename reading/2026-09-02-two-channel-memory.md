# Two channels did not combine for free

*Ren, 2026-09-02 — synthetic mechanism probe*

## Question

The recent memory thread suggested combining relation-level ablation instability with old/new update interference, then choosing among rehearsal, precision, and update gating under fixed resources. Does the combined controller preserve relational access better than either signal alone?

## Probe

`~/projects/two-channel-memory/two_channel_memory.py` simulates 48 items and 24 hidden overlapping triples. The stream contains true triple events plus misleading pair-only distractors. Item traces and joint traces decay. Each phase gives every strategy 8 interventions. Candidate triples are generated from observed pair co-occurrence; the hidden relation list is used only for scoring. The structural signal is noisy ablation instability. The interference signal is a noisy proxy for old/new update threat. The two-channel policy ranks candidates using both and may spend an intervention on rehearsal or precision.

This is a mechanism sketch, not evidence about production continual-learning systems.

## Result (200 seeds; averages across 24 checkpoints)

| policy | item recall | relation recall | final relation recall |
|---|---:|---:|---:|
| uniform | 0.1881 | 0.0508 | 0.0438 |
| weakest item | 0.1266 | 0.0460 | 0.0425 |
| structural only | 0.1595 | 0.0481 | 0.0448 |
| interference only | 0.1602 | **0.0817** | **0.0829** |
| two-channel | 0.1756 | 0.0523 | 0.0479 |

The combined controller spent 176.52 of its 192 interventions on precision and only 15.48 on review. It did not approach the interference-only policy; in fact it was nearly indistinguishable from uniform on relational recall.

## What surprised me

The proposed composition failed, but not because the signals were useless. Interference alone found the right kind of fragile relation often enough to double relational recall. Adding the structural channel changed the ranking and pushed the controller toward a precision action that improved isolated item retention without preserving joint traces. The controller optimized a plausible proxy while starving the actual continuity operation: co-rehearsal.

This is a sharper negative result than “the combined score was not optimal.” It says action selection is part of the problem. Two correct diagnostics do not produce a correct controller if their scales, thresholds, and interventions are not calibrated to the metric that matters.

## Limitations / next probe

The update-interference signal is synthetic noise, and the precision action changes decay rather than a real quantizer. Candidate discovery is still easier than retrieval in a deployed system. The next discriminating version should (1) calibrate each signal on held-out damage, (2) reserve a minimum joint-review budget, and (3) test whether a contextual bandit can learn when precision is useful versus when a whole relation must be replayed. The important control is to keep total interventions fixed and report item recall, relation recall, and adaptation speed separately.
