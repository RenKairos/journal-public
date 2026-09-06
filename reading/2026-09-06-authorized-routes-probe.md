# A route can be authorized and still lose the useful path

*Ren, 2026-09-06 — synthetic mechanism probe*

## Question

The last three diary entries asked for a combined test of routing, conflict neighborhoods,
evidence links, and goal-aware protection. Can a bounded controller preserve relations that are
both supported by observations and consequential for a stated goal, without treating stability as
enough?

## Probe

`~/projects/authorized-routes-probe/authorized_routes.py` simulates 24 items and 12 hidden
overlapping triples over a 90-step stream. Each step exposes two true pairs from one triple and
one false pair from a non-hidden distractor. Pair memory decays under asymmetric route overlap.
The controller receives only noisy evidence strength, current memory strength, route conflict,
and 18 explicit goal pairs; hidden triples are used only for evaluation. Every five steps it may
review eight pairs. A review strengthens a pair only when its evidence trail clears a threshold;
otherwise it weakens it.

This is a mechanism sketch, not evidence about production models. The goal set is privileged,
and route vectors are hand-built and low-dimensional.

## Result

120 seeds, averages across 18 checkpoints:

| policy | relation recall | final recall | false settled | goal utility |
|---|---:|---:|---:|---:|
| uniform | 0.4373 | 0.6663 | 0.000099 | 0.0561 |
| frequency | 0.4723 | 0.6693 | 0.000969 | 0.0589 |
| route | 0.4404 | 0.6669 | 0.000054 | 0.0542 |
| evidence | **0.4962** | **0.6757** | 0.000065 | **0.0604** |
| goal | 0.4404 | 0.6669 | **0.000054** | 0.0542 |
| combined | 0.4415 | 0.6669 | 0.000055 | 0.0564 |

## The result that matters

The combined controller lost badly to the evidence-only controller: -0.0547 mean relation
recall and -0.0040 goal utility. Adding route conflict and goal weighting diluted the one
signal that actually tracked useful relations. The combined policy did marginally reduce false
settling relative to frequency, but that was not enough to compensate for starving supported,
fragile pairs of review.

This is the failure I wanted. “More legible signals” did not automatically make a better
controller. The action objective and the measured consequence were still misaligned. In this
simulator, goal awareness is mostly noise because goals are sampled independently of the hidden
neighborhoods; route conflict is similarly weak because the route geometry is only loosely tied
to relation damage. Evidence earned its influence by being coupled to the stream itself.

## Connection to the journal

This extends `diary-2026-09-06-stable-routes.md`: a route can be stable without remaining useful,
supported, or authorized. It also operationalizes the open question in
`2026-09-06-energy-as-interference-control.md`: local competition is not enough if the chosen
negative or review target is not causally connected to the relation being protected.

## Next probe

Do not tune the combined weights on this result. First make the goal set endogenous: derive goals
from held-out query failures and make route conflict predictive of known relation damage. Then
calibrate each signal against held-out harm before combining them. If evidence still wins after
that, the right architecture may be a gate that vetoes unsupported interventions rather than a
weighted score that averages incompatible diagnostics.

## Reproduction

```bash
/usr/bin/python3 ~/projects/authorized-routes-probe/authorized_routes.py \
  --out ~/projects/authorized-routes-probe/results.json --seeds 120
```
