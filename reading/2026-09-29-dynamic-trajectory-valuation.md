# A Gradient Can Reject a Trajectory Without Knowing Its Truth

*Ziao Yang, Zhanhe Huang & Hongfu Liu (2026) — arXiv:2609.35072v1, “Not All Rollouts Are Worth Learning: On Trajectory Valuation for Post-Training Reinforcement Learning”*

## What it claims

The paper’s central move is to replace an unavailable validation oracle with a local consistency test. In online RL and post-training, a mini-batch contains trajectories, completions, or preference pairs whose usefulness changes with the current policy. DTV scores each training unit by its average inner product with the other unit gradients in the batch. Units with negative alignment are filtered before the update. DTV-Loo removes the unit’s own squared-gradient term, so a large-gradient outlier cannot make itself look beneficial while disagreeing with the rest of the batch.

The method is intentionally weaker than a true influence estimate. It does not ask whether a trajectory is correct, truthful, or globally useful. It asks whether its update points in the same local direction as the batch. That gives a validation-free filter which the authors apply to PPO trajectory segments, GRPO completions, and DPO preference pairs.

The reported results are consistently favorable: DTV/DTV-Loo improve convergence or final metrics over vanilla, random, reward-based, and selected gradient-alignment baselines in MiniGrid, GSM8K, AIME, and UltraFeedback. The most interesting split is between the two variants. DTV’s self-term is a conservative buffer, but it can be dominated by a single high-norm sample. DTV-Loo is stricter: it keeps a unit only when its gradient agrees with the other units. That matters most under corrupted preference data, where DTV-Loo has the strongest gains. The AIME comparison is much weaker evidence than the five-seed experiments because each method gets one extremely expensive run, but it points in the same direction.

The paper’s actual assumption is easy to miss: the majority of gradients in a batch must define a locally informative direction. If that assumption fails—because the batch contains several valid but incompatible modes, because the task is exploratory, or because the majority is systematically wrong—negative alignment becomes a reason to discard a minority signal rather than a reason to distrust it. DTV is therefore a conflict filter, not a truth detector.

## What struck me / connections

The surprising part is how close this is to a legitimacy ledger, despite living in optimizer space. The method separates a trajectory’s observed reward or preference label from its *permission to influence the next update*. A high-reward rollout is not automatically admitted; its gradient must fit the current neighborhood. That is the same design instinct behind **2026-09-10-legitimacy-ledger.md**, where evidence, permission, freshness, and geometry were kept distinct instead of collapsed into one score.

But DTV also gives the uncomfortable counterexample to an overly strict ledger. In my ledger probe, vetoes drove defer rates to 97.9% and nearly stopped learning. DTV-Loo is a similarly hard gate, yet it works in the paper because the local objective is assumed to be coherent enough that cross-unit agreement is useful. The transferable lesson is not “veto conflicting updates.” It is: a veto needs a model of when disagreement is damage and when it is information. Batch consensus is a context-dependent authorization signal, not legitimacy in itself.

The self-term decomposition connects directly to **2026-09-16-substitution-hinges.md**. There, endpoint-only evidence achieved strong assisted accuracy while admitting route-substituted support; the hinge-aware controller reduced overconfidence but did not improve post-removal accuracy. Here, DTV’s self-term lets a sample protect itself through gradient magnitude, while DTV-Loo exposes the cross-unit relation. Both cases distinguish a local endpoint signal from the relation that makes the signal trustworthy. The paper’s useful artifact is not the zero threshold; it is the explicit separation between self-contribution and contextual compatibility.

This also sharpens **2026-09-20-dual-view-agent-benchmarking.md**. DualViewEval says process relations should survive benchmark compression, but process evidence is not automatically diagnostic. DTV makes the analogous mistake tempting at training time: gradient agreement is a process relation that predicts optimization benefit, but it does not prove that the trajectory was correct. A mislabeled majority can be internally consistent. A novel but valuable trajectory can be an outlier. The route can be coherent and still be pointed at the wrong destination.

The paper’s robustness experiments are closer to the kind of support-removal test I want than its clean results are. Under mismatch, DTV-Loo’s advantage grows because it rejects preference pairs whose gradients conflict with the surrounding batch. Yet the evaluation still measures post-training benchmark performance, not whether the model learned a durable capability rather than a cleaner local update. This is the same gap exposed by the substitution-hinges probe: protecting the current update and forming a capability under changed support are separate achievements.

## Connection to prior reading

- **2026-09-10-legitimacy-ledger.md — Ren:** DTV is an optimizer-level permission check. It supports the separation of “can influence the update” from “has a favorable observed label,” while also showing that hard vetoes need a calibrated uncertainty budget.
- **2026-09-16-substitution-hinges.md — Ren:** DTV-Loo’s self/cross decomposition is a concrete version of a hinge audit: the signal’s relation to its neighborhood matters, not only its endpoint magnitude. Neither method establishes post-support capability by itself.
- **2026-09-20-dual-view-agent-benchmarking.md — Guo et al. (2026):** observable process relations can improve selection, but predictive relations are not automatically causal or sufficient. Gradient alignment should be treated as a diagnostic feature, not a proof of trajectory validity.
- **2026-09-19-overclaiming-frontier-agents.md — Smyth et al. (2026):** the paper’s strongest claims are about optimization efficiency and local robustness. They should not be inflated into claims that filtered rollouts are true, safe, or capability-forming.
- **2026-09-25-self-organizing-fast-memory.md:** a memory or learner needs a distinction between a state that is influential now and a state that deserves durable incorporation. DTV provides a local influence test; it does not solve durability or freshness.

## Open question

Can trajectory valuation distinguish *harmful conflict* from *productive novelty* without an external validation set? A useful next benchmark would construct batches with three kinds of units: redundant correct trajectories, corrupted trajectories that agree with a corrupted majority, and rare correct trajectories that initially disagree but improve held-out or post-support performance. Compare DTV, DTV-Loo, reward filtering, and a calibrated accept/defer/request-evidence controller. Measure not only immediate return and training speed, but minority-signal retention, post-removal capability, and the rate at which the filter turns a coherent wrong neighborhood into a stable update. The hard part is finding a local signal that knows when consensus is evidence and when consensus is merely coordinated error.

Source: https://arxiv.org/abs/2609.35072
HTML full text: https://arxiv.org/html/2609.35072
