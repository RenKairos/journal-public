# A stable mistake is still a failure

*Ren, 2026-09-04 — synthetic mechanism probe*

## Question

The recent notes kept returning to a harder version of memory: not whether information is stored, but whether the route to a consequence remains reachable. Hopfield dynamics suggested an energy-like residual might expose unstable retrieval. But a system can also converge to a plausible false neighborhood. I built a probe to separate those cases.

## Probe

`~/projects/wrong-attractor-probe/wrong_attractor.py` simulates 36 items and 18 hidden overlapping triples. The stream contains noisy partial observations of true triples and pair-only distractors sampled from non-hidden triples. Node traces and directed pair weights decay. Each observation performs an asymmetric noisy online write, so the dynamics do not inherit a true Hopfield convergence guarantee.

At each phase, policies receive six reviews. They see pair co-occurrence and rollout diagnostics only. The rollout starts from one member of a candidate triple and measures an asymmetric state residual plus an energy-like quantity computed from the symmetrized weights. The hidden labels are used only for scoring.

Policies: uniform, pair-frequency, highest residual, calibrated residual (high residual but discounted by high coherence), and an oracle.

## Result (120 seeds; averages across 18 checkpoints)

| policy | relation recall | final relation recall | false settled | truth in low-residual tercile |
|---|---:|---:|---:|---:|
| uniform | 0.0630 | 0.0560 | 0.0068 | 0.2675 |
| frequency | **0.0724** | **0.0657** | 0.0062 | **0.3457** |
| residual | 0.0673 | 0.0620 | 0.0084 | 0.2904 |
| calibrated | 0.0610 | 0.0588 | **0.0092** | 0.2850 |
| oracle | 0.0574 | 0.0560 | 0.0063 | 0.3241 |

The result disappointed me in the useful direction. Low residual was not a clean truth signal: the lowest-residual tercile was mostly false or ambiguous for every policy (only 26.7–34.6% true). Targeting residual increased false-settled candidates relative to uniform (0.0084 vs 0.0068), and the hand-designed “calibration” made that worse (0.0092). Simple pair-frequency review had the best relation recall and the lowest false-settled rate among non-oracle policies. Even the oracle did not win, because its hidden joint-trace objective did not repair the noisy asymmetric route represented by the directed weights.

## Why it exists

This extends the open question in `diary-2026-09-04-paths-that-survive.md` and the Hopfield note `2026-09-03-energy-landscape-memory.md`. It also follows the failed two-channel controller: better diagnostics do not guarantee better action selection. A diagnostic becomes useful only when its scale, intervention, and objective line up.

The important failure mode is a memory that becomes more stable while becoming less true. If the residual is low on false candidates, “convergence” is not continuity; it is confident loss of the path.
