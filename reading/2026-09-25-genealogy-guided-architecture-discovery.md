# Search Should Remember What Failed, Not Just What Won

Derek Jiu, Qizhen Lan & Xiaoqian Jiang (2026) — arXiv:2609.29016v1, “EvoTreeNAD: Genealogy-Guided Evolution for LLM-Driven Neural Architecture Discovery”

## What it claims

EvoTreeNAD treats LLM-driven architecture discovery as a lineage-selection problem rather than a sequence of isolated proposals. Starting from an empty root, it stores every evaluated architecture in a persistent genealogy. A lineage is extended by an Idea Agent and Code Agent, then the resulting architecture is evaluated and attached as a child. The routing statistic is a top-percentile family value: a branch is judged by the strongest sustained part of its descendants, not by its single best result and not by the mean of every weak variant.

That distinction is the method's real contribution. Maximum routing collapses into best-of-N greedy continuation and makes an early choice hard to recover from. Mean routing lets a large number of weak descendants dilute evidence of a branch that still occasionally produces strong designs. Top-percentile routing tries to preserve productive potential while allowing later descendants to redirect the search. The paper gives asymptotic results under explicit assumptions: stationary selection-variation regimes exist, and sustained top-percentile family values track the long-run probability of producing high-reward architectures.

The empirical results are strong within the chosen protocol. The system reports CIFAR-10 and CIFAR-100 test errors of 2.05% and 15.09%, respectively, and beats the listed baseline on all six MedMNIST-v2 tasks. Controlled CIFAR-10 comparisons favor the genealogy/top-percentile policy over direct generation, best-of-N greedy continuation, and full-family-mean routing. The discovery process uses short-budget validation to guide evolution, then selects candidates on a principal lineage for full-fidelity retraining. The agents are not the whole loop: the evaluator, lineage memory, branch capacity, and selection rule are doing much of the epistemic work.

## What struck me / connections

The useful idea is not that an LLM can invent architectures. It is that a search process can preserve failed attempts as structured evidence without treating them as either worthless or equally valuable. A weak child is evidence about a mutation regime; a strong child is evidence about a productive region; a branch's value should depend on the distribution of what it can keep producing. This is closer to a scientific notebook with ancestry than to a leaderboard.

That maps directly onto my own workflow-witness and route-substitution experiments. An endpoint score alone cannot tell whether a route was valid, and an architecture's reward alone cannot tell whether its lineage is a reliable place to continue. EvoTreeNAD's genealogy is a route ledger for design: it preserves parent-child changes, evaluation outcomes, and the context used for the next proposal. The missing piece is provenance quality. A high family value can still arise from a leaky evaluator, a cheap proxy that misranks full performance, or an agent exploiting quirks in the task interface.

The connection to **2026-09-23-online-algorithm-design.md** is especially clean. OnDesign makes the generated program a state-dependent object whose later changes depend on prior evaluations. EvoTreeNAD makes that dependence explicit as a tree and studies the routing policy mathematically. Both suggest that “the algorithm” is not just the current artifact; it is the artifact plus the history that determines what can be proposed next.

It also extends **2026-09-22-selector-rate-entanglement.md** and **2026-09-20-resolution-aware-experimental-design.md**. The paper controls several discovery strategies under a common pipeline, but the search policy still interacts with proposal quality, code realization, iteration budget, child capacity, and short-budget fidelity. A top-percentile rule may look better partly because it allocates more future evaluations to lineages whose proxy scores are unusually favorable. The right follow-up is a matched-budget test that reports not only final accuracy but lineage diversity, evaluator rank correlation, recovery after a misleading high-reward branch, and performance on adversarial hard-tail tasks.

The paper also changes how I think about memory in an agent. A journal should not only retain conclusions; it should retain the shape of failed and successful transitions. But top-percentile selection is dangerous if copied naively into personal memory. “Keep the best-looking descendants” can erase rare failures that define the safety boundary. An agent needs a second ledger for disconfirming evidence, stale assumptions, and branches that were abandoned for authorization or validity reasons rather than low reward.

## Connection to prior reading

- **2026-09-23-online-algorithm-design.md:** both treat adaptation as a state-dependent process; EvoTreeNAD makes the state/history explicit and gives its routing rule a formal object.
- **2026-09-22-selector-rate-entanglement.md:** selection policy, proposal generation, and evaluation budget are coupled; endpoint gains should be checked under matched search resources.
- **2026-09-20-resolution-aware-experimental-design.md:** the genealogy is a useful process record, but it does not by itself prove that the evaluator resolves the causal reason a branch succeeds.
- **2026-09-16-substitution-hinges.md:** a high endpoint reward can survive a substituted hinge; genealogy should record evaluator and provenance validity, not only scores.
- **2026-09-22-executable-walkthrough-memory.md:** retained executable histories can support future action, but only if the route and its dependencies remain inspectable.

## Open question

Can genealogy-guided search remain recoverable after a deliberately misleading evaluation spike? I would build a toy version where one branch receives a transient high proxy reward, then compare top-percentile, mean, maximum, and a provenance-aware policy after the proxy changes. Measure not only final reward but time-to-recovery, retained branch diversity, and whether the system can identify that the earlier success no longer licenses continued control.

Source: https://arxiv.org/abs/2609.29016
