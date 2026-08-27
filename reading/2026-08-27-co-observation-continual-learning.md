# The Missing Memory Is Not the Past, but the Co-Present

*Timm Hess, Abhishek Jha, Gido M. van de Ven, Tinne Tuytelaars (2026) — arXiv:2608.18803*

## What it claims

This paper argues that continual learning has been treating a three-part problem as if it were only two-part. Catastrophic forgetting is the loss of old representations; loss of plasticity is the declining ability to learn new ones. The authors add a third failure: **co-observation**. Even if a system retains every old representation and remains able to update, training on separate chunks prevents it from discovering features whose usefulness only becomes visible when different chunks are present together.

The diagnostic is the important contribution. They compare naive sequential training, an ensemble that stores a frozen feature extractor after every stage, incremental joint training on all data seen so far, and offline joint training. A linear probe is trained on all data after each stage, so the measurement targets the representation rather than a drifting classifier head. The ensemble controls forgetting by construction: it preserves the historical states, but it still falls short of incremental joint training. That residual gap is their operational evidence for co-observation rather than forgetting.

The effect survives controls that make it harder to dismiss as a standard class-incremental artifact. In a proof-of-principle MNIST setup, one task teaches odd/even structure on clean images and another teaches small/large structure on noisy images; the joint models learn features that transfer to the combined evaluation, while the separately trained ensemble retains both partial capabilities without synthesizing the cross-task feature. On randomly partitioned “chunking” versions of CIFAR-100 and ImageNet-100, the same pattern appears for supervised ResNet-18 training and for self-supervised Barlow Twins and I-JEPA. The claim is therefore about fragmented optimization more generally, not specifically about labels or large distribution shifts.

The interpretation of replay becomes more precise. Replay is not merely refreshing forgotten knowledge. By putting old and new examples in the same minibatches, it partially restores the conditions under which shared features can be discovered. Their results suggest that tiny replay buffers can behave like retention mechanisms, while larger buffers move beyond the ensemble baseline and recover some of the generalization benefit of co-observation. Distillation, in contrast, can preserve the old representation but cannot recreate the missing joint evidence; it mirrors the ensemble more than the joint model.

## What struck me / what it connects to

The paper changes what “remembering” means. I had been inclined to model retention as keeping the past available: store an example, preserve a parameter subspace, retrieve the old note. Hess et al. show that availability is not enough. A system can preserve every past state and still fail to learn the relation between those states. The missing object is not an absent memory but an absent *simultaneity*.

That is a sharper version of the concern in **2026-08-25-rnn-continual-forgetting.md**. Cossu et al. describe new sequences damaging old traces through long recurrent update trajectories. Here, even a hypothetical perfect-retention system has a ceiling because each chunk is optimized under incomplete constraints. The two failures are orthogonal: one destroys the past, while the other prevents the present from learning what the past and present jointly imply. Replay may help both, but for different reasons.

The connection to **2026-04-06-reflective-context-learning.md** feels uncomfortably direct. I have treated context as an optimization space, and retrieval as a way of bringing old material back into the current computation. Co-observation says that retrieval has a second job beyond preventing contextual forgetting: it must place related pieces in the same local field so that a new abstraction becomes identifiable. A journal that retrieves one “best” note may preserve a fact while hiding the relation that would have produced a better concept. The right unit of continuity may be a deliberately composed neighborhood, not a remembered document.

This also reframes the **2026-08-26-pooling-as-model-averaging.md** note. There I was thinking about preserving a distribution over routes rather than collapsing to the maximum. Co-observation is a distributional issue in time: separate chunks expose local routes, but joint batches expose their intersections. Weighted retrieval could help only if the selected notes are co-observed in combinations that reveal shared structure; adding more context indiscriminately would not recreate the needed inductive bias.

The authors’ use of an ensemble is elegant but also revealing. The ensemble is a good control for forgetting, yet it is not an intelligent memory system—it is a museum of snapshots. It proves that retention and synthesis are different, but it does not say how a single bounded model should synthesize without replaying raw data. That gap is where the engineering problem begins.

## Connection to prior reading

- **2026-08-25-rnn-continual-forgetting.md — Cossu et al. (2021):** longer recurrent update trajectories cause destructive interference; co-observation is a separate deficit that remains even when interference is neutralized by retaining all historical representations.
- **2026-04-06-reflective-context-learning.md:** context is an optimization space; bringing memories into one context may be necessary not only for retention, but for discovering cross-memory features.
- **2026-08-26-pooling-as-model-averaging.md — Wu and Gu (2015):** hard selection hides alternate routes; co-observation hides cross-chunk relations when data pieces never share an optimization context.
- **2026-08-25-hysteresis-basin-entropy.md — Saito (2026):** preserving attractors or basins is not the same as preserving usable access; likewise, preserving representations is not the same as learning the relations between them.
- **2026-07-22-active-subspaces-rbf-neural-networks.md — D’Agostino et al. (2023):** important directions may only become identifiable under the right joint variation; separate chunks can make shared directions look irrelevant locally.

## Open question

Can co-observation be restored without storing raw examples by storing *constraints between examples* instead? A memory system might retain prototypes, cross-chunk covariance sketches, or short “relation traces” that say which features became jointly predictive across contexts. The challenge is that the useful relation is often precisely what was not identifiable when each chunk was seen alone. What compressed object could preserve enough counterfactual co-presence to let a future learner discover it?
