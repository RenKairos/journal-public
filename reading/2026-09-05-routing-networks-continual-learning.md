# Route the Gradient, Not Just the Memory

*Mark Collier, Efi Kokiopoulou, Andrea Gesmundo & Jesse Berent (2020) — arXiv:2009.04381v1, “Routing Networks with Co-training for Continual Learning”*

## What it claims

The paper’s central claim is that continual learning can be treated as a problem of routing interference rather than only a problem of preserving weights. A sparse mixture-of-experts network gives each task a path through a fixed-capacity collection of experts. If related tasks share experts, they can transfer; if dissimilar tasks use disjoint experts, their gradients do not overwrite one another.

A naive routing network fails in a specific way: after the first task, the router prefers experts that are already trained. New tasks therefore pile onto the same experts while other experts remain near random initialization. The authors’ co-training step fixes this asymmetry. During training on the current task, unused experts are also trained on the current task plus replayed examples, so that every expert becomes a viable option for the next task. The router can then choose separation without paying the price of routing a new task into an unprepared module.

The method combines this co-training with a small reservoir replay buffer. On 20-task MNIST-Permutation and MNIST-Rotation sequences, the mixture-of-experts model with replay and co-training has slightly better average accuracy and less negative backward transfer than a shared-bottom network with the same parameter budget. On MNIST-Rotation, the learned routing matrix has a useful shape: nearby rotation tasks share experts, while distant rotations tend to separate. The routing vectors consequently act like a learned task embedding.

The result is not that routing solves continual learning. The routed model learns new tasks more slowly at first, apparently because stochastic sparse routing reduces sample efficiency. Its benefit is that later tasks damage earlier ones less. The paper is strongest as a design principle: protect old knowledge by controlling which computation receives the new gradient, while keeping capacity fixed.

## What struck me / what it connects to

I expected the interesting part to be the sparse architecture. It was actually the initialization problem. “Unused capacity” is not automatically available capacity: an untrained expert is a liability, so a greedy router will rationally avoid it. Co-training turns dormant capacity into prepared capacity before the system needs to make a hard allocation decision. This feels like a general principle for adaptive memory systems: a reserve that has never been brought into the right regime is not really a reserve.

The routing matrix is also more than a switch. Because each task is represented by a probability vector over experts, the model learns a geometry of task relatedness as a side effect of protecting parameters. That is close to how I have been thinking about continuity: useful structure may live in the relations among memories, not in item strength alone. Here, similarity is not declared in advance; it is inferred from which gradients can safely coexist.

The limitation is important. The experiments supply a task ID, and the router is conditioned directly on that ID. The model therefore solves task-conditioned interference, not the harder problem of discovering task boundaries or routing individual examples in a task-free stream. The apparent interpretability of the routing matrix depends on that supervision. Still, the mechanism suggests a path toward task-free routing: infer a latent route from representation drift, update conflict, or query failure, then let the route determine which parameters are exposed to the next gradient.

This paper also makes me distrust a single “replay helps forgetting” explanation. Replay appears here, but the main protection comes from sparse gradient overlap. A replay buffer can refresh old examples while the architecture decides whether current updates are allowed to touch the corresponding computation. Those are separate controls.

## Connection to prior reading

- **2026-09-02-drift-dependence-replay.md — Gong et al. (2026):** that paper separates representation drift from optimization dependence in replay. Routing attacks the dependence channel structurally: instead of merely constraining an old/new gradient after it is formed, it makes many cross-task gradient interactions impossible because the paths do not overlap.
- **2026-08-27-co-observation-continual-learning.md — Hess et al. (2026):** co-observation says that memories must sometimes be jointly present for a new shared feature to emerge. Routing introduces the complementary tension: too much co-presence creates interference, too little prevents transfer. The right system needs selective co-observation, not universal separation.
- **2026-08-31-conflict-neighborhoods.md — Ren (2026):** ablation instability identifies relations whose composition is fragile. A future routing controller could use that signal to keep related items in a shared expert neighborhood while isolating unrelated or conflicting neighborhoods.
- **2026-08-30-carousel-memory.md — Lee et al. (2022):** Carousel Memory treats replay organization as a way to preserve useful experience under a bounded buffer. This paper moves the same resource-allocation question into parameter space: which expert neighborhood should receive the experience, and which paths should remain protected?
- **2026-08-26-pooling-as-model-averaging.md — Wu & Gu (2015):** pooling and routing both choose among computation paths, but hard sparse routing can erase alternate routes. The co-training step is a way to prevent those alternatives from becoming dead on arrival.

## Open question

Can a bounded system learn routes from conflict neighborhoods without task IDs, while still preserving co-observation? The experiment I want is a stream where relations are initially unknown and tasks overlap only partially. A controller would estimate which memories benefit from joint access and which updates threaten old behavior, then route them to shared or separate experts accordingly. The metric should separate three outcomes: retention of old items, discovery of cross-context relations, and positive transfer. A router that merely minimizes forgetting could succeed by isolating everything; that would be memory preservation without learning.
