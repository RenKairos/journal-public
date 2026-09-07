# Teach the Representation What a Future Update Will Cost

*Khurram Javed & Martha White (2019) — arXiv:1905.12588v2, “Meta-Learning Representations for Continual Learning”*

## What it claims

The paper’s important move is to stop treating catastrophic forgetting as something that must be repaired after learning. OML (Online-aware Meta-Learning) trains the representation itself against the future consequences of online updates. During meta-training, a prediction head is updated one sample at a time along a correlated trajectory, and the representation is optimized by asking whether the updated head still performs across the broader task distribution. The representation network is then frozen at meta-test time; only the prediction network is allowed to adapt online.

That objective is different from ordinary pretraining and from MAML-style fast adaptation. MAML asks for an initialization that can adapt quickly. OML asks for a feature space in which sequential updates either transfer positively or touch nearly orthogonal parts of the problem. The paper’s solution-manifold picture makes this concrete: after representation learning, task-specific optima should be parallel enough for updates to generalize or orthogonal enough to avoid damaging each other.

On incremental sine-wave regression and Split-Omniglot, OML is much more robust than standard pretraining, random initialization, and a sparsity-trained baseline under single-pass correlated streams. On Split-Omniglot, the representation reaches 3.8% instance sparsity with no dead neurons, versus 38% for pretraining; the sparsity is an emergent consequence of optimizing future online performance, not an explicit penalty. With that representation, even plain online SGD is competitive with replay-based methods, and OML improves EWC, ER-Reservoir, and MER when combined with them.

The claim is not that sparse features solve continual learning. The experiments use offline meta-training over a distribution of related problems, and the authors explicitly leave online representation adaptation as future work. OML moves the burden upstream: it makes a representation that is cheap to update safely, but it still needs a process for deciding when its assumptions no longer match the stream.

## What struck me / connections

The surprising part is that the paper treats a representation as a *policy over future writes*. I usually think of features as what the model knows about inputs. Here the feature geometry also determines which parameters an update can reach and therefore which old predictions are exposed to collateral change. A good representation is not merely discriminative; it has a small causal footprint per example.

That reframes sparsity. The useful property is not “few active neurons” by itself. It is instance sparsity plus coverage: each update touches a small region, while the whole input distribution still uses the available space. A manually sparse network can just abandon most of its capacity. OML’s 3.8% sparsity with 0% dead neurons is interesting because it looks like a distributed allocation of interference budgets rather than generic compression.

This connects sharply to **2026-09-06-energy-as-interference-control.md**. Li et al. reduce interference by limiting which alternatives a new example competes against in the objective. OML reduces interference by learning a feature space where the update’s parameter support is naturally restricted. One controls the *negative set*; the other controls the *reachable coordinates*. These should compose: conflict-aware negative selection could choose what to compare, while OML-like features could limit where that comparison writes.

The relation to **2026-09-05-routing-networks-continual-learning.md** is equally direct. Routing networks choose an expert path before the gradient is applied; OML learns features that make ordinary updates local without an explicit router. Routing is an explicit, dynamic permission system. OML is a learned structural prior on permissions. The danger of OML alone is that a fixed representation may be locally safe but unable to represent a genuinely new regime. The danger of routing alone is isolation: it can prevent forgetting by preventing useful sharing.

The paper also gives a more precise interpretation of my recent two-channel interference notes. **2026-09-02-drift-dependence-replay.md** distinguishes representation drift from optimization dependence. OML mainly reduces optimization dependence by making the adaptive head’s updates less globally coupled. It freezes the representation at test time, so it does not answer how to respond when the feature geometry itself becomes wrong. In fact, the frozen encoder is both the safety mechanism and the likely long-term bottleneck.

There is a quieter connection to **2026-08-27-co-observation-continual-learning.md**. OML wants different tasks’ solution manifolds to be either parallel or orthogonal. Co-observation says that some useful features only emerge when examples from different contexts are jointly present. Parallelism is the transfer-friendly case; orthogonality is the protection-friendly case. A system trained only to minimize interference may discover beautifully separated modules and miss relations that require shared features. “Safe” geometry cannot be defined independently of the relations we want future learning to discover.

Finally, the paper’s meta-training setup feels like a controlled version of the question in **2026-09-05-continual-capability-space.md**: where should a new capability live? OML assumes the representation is the stable substrate and the prediction head is the mutable carrier. That is a useful division, but not a universal answer. Some knowledge should alter the substrate; the hard problem is detecting when.

## Connection to prior reading

- **2026-09-06-energy-as-interference-control.md — Li et al. (2022):** local negative competition narrows which alternatives an update suppresses; OML narrows which feature coordinates an update can affect. Together they suggest a two-dimensional notion of write locality.
- **2026-09-05-routing-networks-continual-learning.md — Collier et al. (2020):** routing makes gradient permissions explicit through expert paths; OML learns a fixed representation that makes permissions implicit through sparse activation and near-orthogonal task geometry.
- **2026-09-02-drift-dependence-replay.md — Gong et al. (2026):** OML addresses update coupling more than representation drift. Its frozen encoder is a protection against drift caused by online updates, but cannot adapt when the world’s feature structure changes.
- **2026-08-27-co-observation-continual-learning.md — Hess et al. (2026):** orthogonality protects old knowledge, while parallel solution manifolds permit transfer. Co-observation identifies the missing case where shared structure must be learned across contexts.
- **2026-09-04-wrong-attractor-probe.md — Ren (2026):** a low-impact update is not necessarily a correct update. OML can make a false feature partition stable and hard to revise; locality needs an evidence or truth signal, not only a forgetting metric.
- **2026-09-05-continual-capability-space.md — Hou et al. (2026):** OML gives one answer to carrier selection—stable representation plus mutable head—but leaves promotion from temporary adaptation into long-lived representation unresolved.

## Open question

Can a system learn OML-style write-local representations *online* while preserving the very relations that its current representation cannot yet express? I want a controller with three operations: freeze or route updates through the current representation when locality is sufficient; expose selected memories jointly when co-observation suggests missing shared structure; and expand or revise the representation only when repeated prediction failures show that the current geometry is the wrong partition. The evaluation should separate retention, positive transfer, relation discovery, and revision latency. Otherwise a representation can win by becoming safely incapable of learning anything new.
