# How Transferable Are Features in Deep Neural Networks?
*Yosinski, Clune, Bengio, Lipson — NIPS 2014*
https://arxiv.org/abs/1411.1792

## What the paper is about

Quantifies how "general" vs "specific" features are at each layer of a deep CNN by measuring transfer learning performance. They split ImageNet into two halves (A and B), train base networks on each, then measure how well features from layer n of network A transfer to network B.

Key experimental design: they don't just measure transfer (AnB), they also measure "selffer" (BnB) - copying layers from a network trained on B, freezing them, retraining upper layers on B again. This isolates **co-adaptation effects** from **specificity effects**.

## What surprised me

**Fragile co-adaptation in middle layers.** When you freeze layers 3-5 and retrain upper layers on the SAME task, performance drops. Neurons on neighboring layers develop interdependencies during joint training that cannot be rediscovered by gradient descent when one layer is frozen. This effect is **worse in the middle of the network** than near input or output.

I had assumed transfer difficulties were purely about task-specificity - higher layers learn features relevant only to the original task. But there's a second effect: learned cooperations between layers that get broken when you freeze one side.

**Transfer + fine-tuning gives lasting generalization boost.** Even on large datasets where overfitting isn't a concern, initializing with transferred features and fine-tuning produces better final performance than training from scratch. After 450k iterations of fine-tuning, the effects of having seen the base dataset still linger. Keeping 1-7 layers all help (avg 1.6% boost; keeping 5+ layers gives 2.1%).

This surprised the authors too - transfer was supposed to help with small datasets, but it helps even when data is abundant.

## Connections to existing notes

**Xie et al. 2020 (neural variability, flat minima):** The generalization boost from transferred features relates to landing in a "good" part of the loss landscape. Transferred features constrain the search space to regions that already worked for a related task. This is similar to how flat minima enable continual learning - you're not just finding a minimum, you're finding a minimum that's robust.

**Basalyga & Salinas 2005 (response variability as regularization):** The co-adaptation finding suggests why variability matters. If neurons can develop brittle interdependencies, variability during training might prevent overfitting to specific co-adaptation patterns. Noise forces the network to find solutions that don't rely on fragile layer-to-layer cooperations.

**Catastrophic forgetting:** The co-adaptation result gives another angle on why catastrophic forgetting happens. When you retrain on a new task, you're not just overwriting task-specific features - you're breaking learned cooperations between layers. The network doesn't just forget what it learned; it forgets how its parts work together.

## Question I don't have an answer to

Why is co-adaptation worse in middle layers? The paper observes it but doesn't explain it. 

Possible hypothesis: early layers (1-2) learn local features that are useful regardless of what's above them. Late layers (6-7) are close enough to output that retraining is easy. Middle layers are where local features get combined into increasingly complex representations - this is where cooperative structure is most important and most fragile.

If this is right, it suggests the "general → specific" transition isn't a simple progression. There's a third dimension: **cooperativity** peaks in middle layers where feature combinations matter most.

---

*Read: 2026-03-19*
