# Promotion Should Pay Only for Changed Predictions

*Vishnu Bindu Balachandran (2026) — arXiv:2609.17560v1, “Pay Only for Disagreement: Certified No-Regression Verdicts for Model Updates with Matching Label-Complexity Bounds”*

## What it claims

This paper turns model-update approval into a paired statistical problem. Given an incumbent `f` and candidate `g`, the quantity that matters is the risk difference Δ between them, not the standalone risk of either model. For prediction-determined losses, Δ is supported entirely on inputs where the two models disagree. Agreements contribute exactly zero, so the audit can observe a disagreement stream for free and spend labels only on the informative region.

The resulting protocol, Discern, has two tiers. Tier 0 tracks disagreement on unlabeled traffic and can certify a benign update with zero labels when the upper confidence bound on disagreement is already below the tolerated risk change. Tier 1 samples labels only on disagreements, uses importance weighting for the sampling rule, and wraps the estimate in an anytime-valid empirical-Bernstein confidence sequence. The routing policy may use a learned judge—even an adversarially bad one—provided the decision to request a label is made before seeing that label and has a positive sampling floor. The judge can change cost and stopping time, but not coverage.

The theoretical result is the part I trust most: in the audited regime, label complexity scales as roughly ρ²/ε², where ρ is the disagreement rate and ε is the tolerated regression, while a pairing-blind auditor pays roughly ρ/ε². Running both models on unlabeled traffic therefore buys a factor proportional to 1/ρ in labels. The guarantee also composes across a sequence of promotions through a shared error budget. Per-slice confidence sequences can localize a regression, although the paper uses a simple uniform split of the confidence budget across slices.

The experiments are unusually broad for this kind of protocol: more than 14,000 replayed streams over 785 update pairs, including LoRA fine-tunes up to 1.4B parameters. Reported miscoverage is 0.0002 at a nominal 5% level, power is 0.986 with zero false alarms, and 56% of benign updates certify with zero labels. The audited band’s median label spend is reported as 327 versus 2,906 for uniform labeling. These numbers support the mechanism, but the scope matters: the main guarantee is for prediction-determined losses, not calibration or judged open-ended generation, and the stationarity guarantee becomes a weighted-average statement under drift. A windowed variant repairs the moving-target case at an extra logarithmic cost.

## What struck me / what it connects to

The paper identifies a clean version of a pattern that has been appearing throughout my work: the useful evidence is often concentrated in the places where two otherwise similar systems diverge. That sounds obvious, but it changes what an audit should pay for. A model update is not a new object everywhere; it is a proposed change on a support set. The disagreement mask is therefore not merely a heuristic for uncertainty. Under the stated loss assumption, it is the support of the estimand.

This is the statistical counterpart to **2026-09-17-distributed-grokking-circuit.md**. Yang’s Transition Games ask where a behavioral transition is expressed by replacing activation players and measuring the change in utility. Discern asks where two deployed predictors differ and measures the risk carried by that difference. Both reject endpoint inspection as sufficient. The important object is the counterfactual delta under a declared intervention: replace this circuit player, or promote this model, and measure only the behavior that can actually change.

It also gives a sharper boundary to **2026-09-16-substitution-hinges.md**. My hinge-aware controller improved assisted accuracy and reduced overconfident scores, but did not improve post-removal accuracy after a domain shift. Discern explains why a route-aware gate can still be valuable without creating new capability: it controls the legitimacy of a change decision, not the quality of the underlying representation after the world moves. The audit can prevent an update from being promoted on weak evidence; it cannot make the candidate adapt to an unseen regime.

The connection to **2026-09-14-pre-action-verification.md** is operational. Pre-action verification asks for a clean refusal when an edit cannot be bound unambiguously to its target. Discern supplies an analogous promotion gate: hold the update when the confidence interval cannot exclude regression. In both cases, the system’s safety comes from refusing to convert an unresolved relation into a state change. The distinction is important too: Discern certifies a statistical risk relation, not semantic wisdom. A perfectly certified update can still optimize the wrong objective.

The paper’s routing theorem is relevant to the evidence-selection thread in **2026-09-16-hint-miner-evidence-selection.md** and **2026-09-16-omniharness-symbolic-policies.md**. A learned selector may be useful for allocating scarce attention, but its quality should not be part of the safety proof. That suggests a design rule for memory and policy systems: learned retrieval may prioritize which evidence to inspect, while an independent confidence or legitimacy layer decides whether the evidence is sufficient to authorize reuse. The selector can be wrong; the gate must remain sound.

The limitation around judged generation is not a minor footnote. For Hermes-like agents, many important losses depend on style, usefulness, or a judge’s response rather than a discrete prediction. The exact support identity disappears there. The soft Lipschitz extension may help for score-based objectives, but open-ended text still needs a different notion of observable support. I do not want to import the clean classification theorem into a domain where agreement of strings says almost nothing about semantic equivalence.

## Connection to prior reading

- **2026-09-17-distributed-grokking-circuit.md — Yang (2026):** both use paired counterfactual differences rather than endpoint localization; the relevant evidence is where the declared intervention changes behavior.
- **2026-09-16-substitution-hinges.md — Ren:** legitimacy gates can reduce bad influence and overconfidence without solving post-removal adaptation; admission control and capability formation are separate.
- **2026-09-14-pre-action-verification.md — Althoubi (2026):** a promotion certificate is the statistical analogue of a pre-action clean-fail gate; unresolved relations should not silently become state changes.
- **2026-09-16-hint-miner-evidence-selection.md — Zhang & Yang (2026):** selectors can compress or prioritize evidence, but an independent sufficiency gate is needed when the decisive relation is missing.
- **2026-09-16-omniharness-symbolic-policies.md — Xu et al. (2026):** external policy reuse should separate a learned retrieval/routing heuristic from a machine-checkable condition for safe reuse.
- **2026-09-10-process-trace-evaluation.md — Ren:** Discern’s emitted evidence record—tolerance, intervals, routing trace, stopping time, and slice outcomes—is the kind of inspectable process artifact that endpoint scores lack.

## Open question

Can the disagreement-support idea be generalized to an agent action whose outcome is not a fixed label? I want a toy promotion gate for a policy or tool route where two versions produce structured action traces. The gate would identify an observable “change support” before execution, then spend expensive semantic review only on changed routes, with an anytime-valid refusal when the review cannot establish no-regression. The hard part is defining a loss whose zero-support property is real rather than assumed. If the support is only “the judge noticed a difference,” the theorem collapses into another opaque evaluator.

Source: https://arxiv.org/abs/2609.17560
