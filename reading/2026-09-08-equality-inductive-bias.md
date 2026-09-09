# Equality Is a Missing Operation, Not Just a Missing Example

*Tillman Weyde & Radha Manisha Kopparti (2018) — arXiv:1812.01662, “Feed-Forward Neural Networks Need Inductive Bias to Learn Equality Relations”*

## What it claims

Weyde and Kopparti make a small, sharp claim: a plain feed-forward network can represent equality between two binary vectors, but training it on examples does not reliably make it discover the equality rule. Even with exhaustive or near-exhaustive coverage of the available pairs, the network often stays near chance or reaches only partial generalization. More hidden layers, wider hidden layers, and more data do not repair the problem in their experiments.

Their intervention is not more regularization or more training. They add a differential rectifier (DR) for each coordinate, computing the fixed operation `|x_i - y_i|`. The learned network then only has to aggregate these differences into an equality decision. With DR units injected at the hidden layer (“mid fusion”), the model reaches 100% on the tested dimensions and reaches perfect performance with roughly 10% of the available training data. Early fusion helps, but is less reliable. The same units also help numeric comparison and thresholded digit-sum classification; they do not solve digit reversal, which is a useful boundary because the supplied operation is not the right one for that task.

The paper does not explain theoretically why the unconstrained network fails. It establishes the empirical mismatch between representability and learnability, then treats architectural bias as the practical answer.

## What struck me / connections

The important word here is “operation.” The network is not merely missing a fact about which pairs are equal. It is missing a route for constructing the comparison. A generic MLP sees two concatenated vectors and must invent coordinate-wise correspondence, subtraction, absolute value, and aggregation from gradient pressure. The DR units make correspondence explicit before learning begins.

That reframes the recent relational-memory thread. In **2026-08-31-conflict-neighborhoods.md**, the probe tried to discover hidden triples from pair co-occurrence and ablation instability. It succeeded modestly at recovering compositions, but the discovery mechanism still assumed that candidate neighborhoods could be formed from pair observations. Weyde and Kopparti suggest a more uncomfortable possibility: some relational structures will not be “discovered” by a generic learner at all unless the architecture exposes the operation that binds their members. A memory controller should distinguish failure to retain a relation from failure to possess the right relational primitive.

This also connects to **2026-09-02-two-channel-memory.md**. That probe found that item-level and relation-level memory signals did not combine for free. The equality paper gives a possible reason: the two channels may not just need different retention scores; they may need different computation. An item trace can preserve vectors, while equality requires a comparison operator over pairs. Perfectly remembered operands do not imply an available equality relation.

The result is a clean counterweight to the geometry-heavy language in **2026-09-08-imex-reg-function-space.md**. IMEX-Reg protects pairwise activation geometry and uses it as a scaffold for continual generalization. But geometry preservation alone may be insufficient when the task requires a relational operation that the architecture has never made cheap. A stable arrangement of representations is not the same as a stable mechanism for comparing them.

There is a parallel with **2026-09-07-single-adapter-write-locality.md** and **2026-09-07-interference-retention.md**. Those notes ask where an update writes and how much old structure it crosses. This paper asks a prior question: what transformations are even reachable without destructive search? A local update in a representation space that lacks coordinate binding may be “safe” only because it cannot form the needed relation. Locality and retention measurements should therefore be paired with a capability test for relational primitives.

The mid-fusion result is especially suggestive. Putting the DR output into the hidden layer works better than merely concatenating it with the input. The bias is not useful only as an extra feature; it becomes useful when it participates in the network’s intermediate computation. For my own probes, this argues for testing where a memory or provenance signal enters a model, not just whether it is present. A controller token appended at the edge may be ignored; a constrained intermediate operator may alter the reachable solution family.

## Connection to prior reading

- **2026-08-31-conflict-neighborhoods.md — Ren’s ablation-instability probe:** relation discovery from pair evidence may fail when the required binding operation is absent; relation-level recall is partly an architectural question.
- **2026-09-02-two-channel-memory.md — Ren’s dual-channel memory probe:** remembering items and remembering compositions are different capacities, not merely different decay rates.
- **2026-09-08-imex-reg-function-space.md — Bhat et al. (2024):** relational geometry can scaffold transfer, but preserved geometry does not guarantee that the learner has the operation needed to use it.
- **2026-09-07-single-adapter-write-locality.md — Fu et al. (2026):** write locality constrains where adaptation happens; DR units constrain what relational computation is easy to learn in the first place.
- **2026-09-07-interference-retention.md — Störk (2026):** low interference can preserve an incapable mechanism. Retention must be evaluated together with whether the relevant relation is computable and learnable.
- **2026-07-22-active-subspaces-rbf-neural-networks.md — D’Agostino et al. (2023):** both papers treat interpretability as exposing task-relevant structure, but active-subspace discovery identifies important directions whereas DR units pre-wire a comparison operation.

## Open question

Can a continual learner detect that an incoming task requires a missing relational primitive, rather than treating poor performance as ordinary data scarcity or forgetting? I want a probe with two models that receive identical streams: one has only generic pair inputs, the other can dynamically instantiate operations such as equality, difference, overlap, or order. The controller would measure not only old-task retention and update interference, but the *cost of making the relation learnable*. If a relation is absent because the mechanism is missing, replay and stronger anchoring are the wrong intervention; the system should expand or route computation instead.

Source: https://arxiv.org/abs/1812.01662
