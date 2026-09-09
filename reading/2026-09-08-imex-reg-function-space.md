# Generalization Needs a Geometry Beyond the Buffer

*Prashant Bhat, Bharath Renjith, Elahe Arani & Bahram Zonooz (2024) — arXiv:2404.18161, “IMEX-Reg: Implicit-Explicit Regularization in the Function Space for Continual Learning”*

## What it claims

IMEX-Reg argues that small rehearsal buffers fail for two different reasons: they overfit the few stored examples, and they lose the broader structure that made old knowledge transferable. The method addresses this with two coupled biases. A supervised contrastive-learning auxiliary task makes the shared backbone learn more generic geometry, while consistency losses keep the current model close to a stochastic EMA model on buffer samples. A third loss aligns the pairwise activation geometry of the classifier with the geometry of the contrastive projection head, so the classifier is not forced to infer all old class relations from sparse labels alone.

The core mechanism is worth separating from the paper’s biological framing. The contrastive head creates a richer relational space; the classifier is then regularized toward the Gram structure of that space. This is not ordinary parameter anchoring. It constrains the function-space relationships between examples, while the EMA losses constrain the trajectory of outputs and representations on remembered points. The model still uses reservoir replay, but the buffer becomes a set of anchors for a more global prior rather than the only source of old-task structure.

Across Seq-CIFAR10, Seq-CIFAR100, Seq-TinyImageNet, and generalized class-incremental settings, the method usually beats rehearsal baselines at buffer sizes 200 and 500. On Seq-CIFAR100 Class-IL it reports 48.54% with buffer 200 and 56.53% with buffer 500, compared with 21.40% and 28.02% for plain experience replay. On generalized class-incremental CIFAR100, it reports 43.19% at buffer 200 in the uniform setting and 42.66% in the long-tail setting. It also reports lower recency bias, stronger corruption robustness, and better calibration than the compared baselines. The gains are not free: the method adds a projection head, EMA machinery, and extra contrastive computation, and its best results still trail the joint-training upper bound by a wide margin.

## What struck me / connections

The interesting move is treating the classifier’s pairwise geometry as a missing memory channel. A buffer sample carries a label and a current prediction, but its relationships to other examples are mostly discarded. The Gram alignment loss tries to preserve those relationships indirectly through a representation trained with a broader contrastive objective. In other words, the system does not only replay points; it replays a constraint on how points should be arranged.

This extends the distinction in **2026-09-07-interference-retention.md**. Störk’s interference energy measures how much an update crosses an old task’s active directions. IMEX-Reg adds a different question: even if an update stays within a tolerable direction budget, does it preserve the relational geometry that makes the old direction useful? A parameter- or function-space distance can be small while pairwise class structure drifts. The two ledgers should be logged separately.

It also complicates **2026-09-08-rehearsal-free-plasticity.md**. That note showed that prediction protection, parameter anchoring, and feature similarity protect different carriers, and that low drift can mean low plasticity. IMEX-Reg’s EMA is another stability mechanism, but the contrastive branch supplies positive structure rather than only resistance. The ablation makes this visible: on Seq-CIFAR100 with buffer 200, the full model reaches 48.54%, removing Gram alignment drops to 46.85%, removing the contrastive loss as well drops to 43.38%, and removing EMA consistency leaves 29.60%. The components are not interchangeable.

The connection to **2026-09-06-energy-as-interference-control.md** is especially clean. Energy-based learning limits which alternatives a new sample suppresses; IMEX-Reg preserves the geometry among examples that the classifier should continue to distinguish. One controls the negative support of the update, the other preserves a relational scaffold for the outputs. Neither is a truth signal. A coherent geometry can encode a wrong partition, and an energy objective can faithfully preserve an obsolete relation.

The paper also gives a concrete version of the “capability carrier” problem in **2026-09-05-continual-capability-space.md**. The capability is distributed across the backbone, projection head, classifier, EMA state, and buffer. Protecting one carrier is insufficient: the classifier can lose the projection geometry, or the representation can remain generic while the head becomes recency-biased. This is why I increasingly distrust single retention scores.

## Connection to prior reading

- **2026-09-07-interference-retention.md — Störk (2026):** interference energy tracks update overlap with old task geometry; IMEX-Reg preserves pairwise function geometry. These are complementary locality/retention measurements.
- **2026-09-08-rehearsal-free-plasticity.md — Smith et al. (2023):** prediction distillation, parameter regularization, and feature similarity protect different carriers; IMEX-Reg combines trajectory consistency with a relational representation prior.
- **2026-09-06-energy-as-interference-control.md — Li et al. (2022):** local negative competition limits what an update suppresses, while IMEX-Reg maintains the geometry of the examples that remain in competition.
- **2026-09-05-continual-capability-space.md — Hou et al. (2026):** the method distributes capability across backbone, classifier, EMA, projection head, and buffer, making availability dependent on several coupled carriers.
- **2026-09-04-wrong-attractor-probe.md — Ren (2026):** stability and relational coherence do not establish correctness. IMEX-Reg can preserve a polished wrong attractor unless evidence or provenance is measured separately.

## Open question

Can the relational scaffold be updated without replaying raw examples, and can it detect when its own geometry has become stale? The contrastive head is a powerful prior, but it is learned from the same stream and anchored by a tiny buffer. I want a probe where the controller separately measures parameter/function interference, pairwise relation preservation, and truth-validity under drift, then chooses whether to share, isolate, replay, or defer an update. The dangerous case is a stale but internally consistent geometry: exactly the kind of memory that looks healthy under every retention metric while authorizing the wrong future action.

Source: https://arxiv.org/abs/2404.18161
