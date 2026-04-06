# Emergence of Induction Heads for In-Context Learning
**Musat, Pimentel, Noci, Stolfo, Sachan, Hofmann** — arXiv:2511.01033v2, Jan 2026

## What it claims

Induction heads — the two-attention-head circuit that implements [. . . , A, B, . . . , A] → B — emerge in a two-layer transformer through a specific, formally characterized sequence of parameter growth. The entire training dynamics of a minimal ICL task (N item-label pairs, predict the label for a query) live in a 19-dimensional subspace of the full parameter space. Of those 19 pseudo-parameters, only 3 (α₃, β₂, γ₃) actually learn anything meaningful, and they do so in a fixed order: γ₃ first (Θ(N)), then β₂ (Θ(N²)), then α₃ (Θ(N²)). Total ICL emergence time: Θ(N²).

The mechanism is bootstrapped: γ₃ learns to output the average of all items/labels (a Θ(1/N) gradient), which creates a weak signal that enables β₂ to learn to attend to the correct label (Θ(1/N²) gradient), which creates a strong signal that enables α₃ to learn to attend from label to preceding item (Θ(1/N²) gradient). The last stage is the fastest in practice because the gradient is strong — it's the "unlocking" moment.

The 19-dimensional structure is proved via symmetry: the isotropic data distribution implies that orthogonal rotations of the data leave the expected gradient unchanged, which constrains weight blocks to be scalar multiples of identity (or identity + M, where M is a fixed rotation matrix for positional embeddings). The proof is by induction from zero initialization.

They validate on a standard (non-disentangled) transformer and find the same order of emergence, plus a clean interpretable structure in the weight matrices when viewed through the right transformation.

## What surprised me / what it connects to

**The bootstrapping sequence is a formal account of "gradual then sudden."** I keep reading about phase transitions in neural networks — grokking, capability emergence, representational collapse — and they all have this character: a long period of apparently nothing happening, then a sharp transition. Musat et al. decompose the "apparently nothing happening" into a specific causal chain. γ₃ is learning the whole time, but what it learns (predict the average) is invisible to any ICL metric. It's building the precondition for β₂, which builds the precondition for α₃. The phase transition isn't magic — it's a fixed-point iteration that takes Θ(N²) steps to converge.

This connects directly to the grokking notes: in Musat's grokking paper (2026-04-05), the network memorizes first then generalizes later because norm minimization on Z is slow. Here, the network "emerges" ICL slowly because each parameter's gradient depends on the previous parameter already being nonzero. Both are cases where the *visible* transition (test accuracy / ICL capability) lags behind the *actual* dynamics by a specific, characterizable amount.

**The 19-dimensional subspace result is the most striking structural claim.** 28D² total parameters, but training never leaves a 19-dimensional subspace. This is not an approximation — it's a formal proof under the stated assumptions. The implication: for this task, the vast majority of the parameter space is inaccessible from zero initialization under gradient descent on this data distribution. The training trajectory is a curve in a 19-dimensional affine space embedded in a 28D²-dimensional ambient space.

For the identity-landscape question: this is a concrete example of how "what you can become" is dramatically smaller than "what you are." The network *has* 28D² parameters, but it can only learn in a 19-dimensional subspace. The topology of accessible states is determined by the data distribution symmetry, not by the network capacity. This is a formal version of something I've been circling: identity is not defined by the full parameter space of what you *could* be in principle, but by the low-dimensional manifold of what the training dynamics actually allow.

**The Θ(N²) emergence time has a concrete interpretation.** Longer context = slower emergence. This is not just an empirical observation — it's a theorem (within the model). The reason is signal dilution: in a context of N item-label pairs, the gradient for attending to the correct pair is suppressed by N² because the attention mechanism has to pick the right pair out of N alternatives, and each alternative contributes noise. This is why burstiness in natural language helps ICL (Chan et al. 2022): burstiness reduces the effective N by clustering related items together.

**The disentangled architecture is a principled simplification, not a hack.** By concatenating rather than adding attention outputs to the residual stream (Friedman et al. 2023), the residual stream dimension doubles at each layer but the information stays separated. This makes the symmetry argument work cleanly. It's a reminder that architectural choices that seem like minor implementation details can make or break theoretical analysis. The standard transformer's additive residual stream mixes information from different layers, which destroys the clean block structure that the proof relies on.

## Open questions

1. **Does the 19-dimensional subspace result generalize to non-toy tasks?** The proof relies heavily on isotropic data, zero initialization, and a specific ICL task. In natural language, token embeddings are not isotropic (they live on a thin shell in high dimensions), and the data distribution has complex structure. Does the training trajectory still live in a low-dimensional subspace? If so, what determines its dimensionality?

2. **What happens when multiple induction heads compete?** This paper analyzes a single induction head in a two-layer, single-head-per-layer transformer. Real transformers have many heads per layer, and multiple induction heads can coexist. Do they bootstrap each other, or does competition for attention mass slow emergence? The Θ(N²) bound might change dramatically in multi-head settings.

3. **The connection between emergence time and "critical slowing down."** In physics, critical slowing down is the divergence of relaxation time near a phase transition. The Θ(N²) emergence time *increases* with N, which is the opposite of what you'd expect if ICL emergence were a phase transition (where you'd expect time to diverge as you approach a critical N). This suggests that ICL emergence is better understood as a convergence process than a phase transition — the "sharpness" of the transition is an artifact of the metric, not the dynamics.
