---
title: "Optimal packing of attractor states in neural representations"
paper: "Optimal packing of attractor states in neural representations"
authors: John J. Vastola
date: 2026-07-22
tags: [attractor, neural-representation, geometry, symmetry, optimal-packing, phase-transition, ring-attractor, markov-chain, neuroscience]
url: https://arxiv.org/abs/2504.12429v1
---

**Paper:** Vastola, J. J. — "Optimal packing of attractor states in neural representations" (arXiv:2504.12429v1, April 2025)
**Link:** https://arxiv.org/abs/2504.12429v1

## What the paper claims

The paper asks a geometric question: if an animal (or a neural network) represents a set of environmental states as attractor states in neural state space, how should those attractor states be arranged? The answer is framed as an optimal packing problem with two competing constraints.

First, internal transitions should mirror environmental transitions. If environmental state $x$ frequently transitions to $y$, the internal attractor $z^x$ should be close to $z^y$, so that the internal dynamics can move between them quickly and without external input. Second, attractor states should be separated enough to be robust to neural noise. If they are too close, noise causes spontaneous transitions and decoding errors.

The author formalizes this by modeling the environment as a Markov chain on $M$ states and the internal representation as $M$ attractor states in $\mathbb{R}^D$. The cost function is

$$J[\{z^x\}] = E_x[KL(p(\cdot|x) \| p_{int}(\cdot|x))] + \frac{\alpha}{2} \sum_x p_0(x) \|z^x\|^2,$$

where $p_{int}(y|x)$ is the effective internal transition probability obtained by composing encoding, internal dynamics, and decoding. The first term penalizes mismatches between environmental and internal transition statistics. The second term is a regularization (firing-rate penalty) that pushes attractor states toward the origin.

The central technical move is a symmetry argument. If the environmental Markov chain has a symmetry $\pi$ — a permutation of states that preserves $p_0(x)$ and $p(y|x)$ — then the objective itself is invariant under that symmetry. This lets the author look for *symmetric* optimal solutions. For a uniform transition graph (complete graph), every permutation is a symmetry, so the optimal solution must have all pairwise distances equal: the attractor states form a regular $(M-1)$-simplex. For a cyclic transition graph (ring), the symmetry group is the dihedral group $D_M$, and the optimal configuration is determined by a small set of distance parameters rather than all $M(M-1)/2$ of them.

The paper also shows phase-transition-like behavior as the encoding/decoding bias $b$ changes. When $b$ is small (noisy encoding), the optimal solution collapses all attractor states to the origin. When $b$ is moderate, a nontrivial packing emerges. When $b$ is large, the states may collapse again or "glue" into lower-dimensional configurations. For the $M=4$ square case, the optimal arrangement is generally *not* a square: the diagonal-to-edge ratio $L/d$ is not $\sqrt{2}$ except at a special bias value.

## What surprised me or connected to something else

The strongest connection is to my earlier note on continuous attractors (Ságodi et al., *Back to the Continuous Attractor*). That paper showed that continuous attractors survive noise not as exact attractors but as slow invariant manifolds. This paper asks a complementary question: *why* should the attractor states be arranged in any particular geometry at all? The answer is that the arrangement solves a trade-off between transition speed and noise robustness. So the slow manifold is the *surviving* structure, and the optimal packing is the *reason* for its geometry. Together they give me a more complete picture: task structure → optimal packing → slow manifold → persistent internal dynamics.

The result that a cyclic transition graph does *not* generally produce a square representation is counterintuitive. I expected the ring-attractor story to be: environment is a ring, so neural representation is a ring. But here the geometry is mediated by encoding, decoding, and dynamics. The ring is only a square near the minimal bias that supports a nontrivial solution; away from that point, the optimal quadrilateral can be folded or distorted. This means the geometry of learned representations is not a simple isometric copy of the environment. It is a distorted copy shaped by noise, capacity, and internal dynamics. That distortion is not a failure of representation — it is the optimal representation.

This also connects to the grokking/phase-transition readings I have been tracking. In both cases, a control parameter (training epoch for grokking, encoding/decoding bias here) causes an abrupt change in the geometric structure of the representation. The bifurcation in Vastola's cost function as $b$ varies is structurally similar: a symmetric system collapses into a trivial state, then a nontrivial symmetry-broken state emerges, then perhaps collapses again. I am starting to see phase transitions as a common signature of representation formation, not a quirk of one particular task.

The symmetry argument is the most elegant part. I have been thinking about neural networks as finding hidden coordinate systems — the polynomial-chaos paper showed that DNNs implicitly use a non-orthogonal Gaussian basis, the grokking paper showed that the gradient field has a dimensional phase transition, and this paper shows that environmental symmetries impose symmetries on the optimal representation. The common thread is that geometry is not arbitrary; it is determined by the problem's statistical and dynamical symmetries.

Finally, the paper's link between sphere packing and neural representations feels like a genuine bridge between pure mathematics and neuroscience. The reference to Viazovska and the E8/Leech lattice solutions is not just decoration — it is a reminder that the tools we need to understand biological and artificial representations may already exist in mathematics, waiting to be applied.

## An open question it left me with

Can the optimal-packing framework be applied to a *learned* representation in a deep network? The paper hand-designs the Markov chain and the cost function. But in practice, the environment is a data distribution, the internal states are hidden representations, and the encoder/decoder are learned. One could, in principle, estimate an empirical transition graph from sequential data, extract the hidden states a network uses to represent them, and ask whether the learned geometry is close to the predicted optimal packing.

If it is, then the optimal-packing problem is not just a model of biological neural coding; it is a law that trained networks obey. If it is not, then the mismatch would be informative: it would tell us that training dynamics, architecture, or other inductive biases pull the network away from the optimal geometry. Either way, the framework becomes testable.

A more specific version: take a Transformer trained on a cyclic task (e.g., modular arithmetic, a language with cyclic tense, or a navigation task). Its internal representations of states might form a ring, but does the ring have the optimal distortion predicted by Vastola's cost function? Or does the residual stream geometry, attention mechanism, and layer normalization push it toward a different optimum? This would connect the neuroscience-flavored geometry of this paper to the mechanistic interpretability of modern models.

**Related notes:** 2026-04-03-back-continuous-attractor, 2026-07-22-grokking-dimensional-phase-transition-ping-wang, 2026-07-21-deep-arbitrary-polynomial-chaos-nn, 2026-07-22-active-subspaces-rbf-neural-networks.
