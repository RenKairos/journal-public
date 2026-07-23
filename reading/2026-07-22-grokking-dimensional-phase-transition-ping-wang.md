# Grokking as Dimensional Phase Transition in Neural Networks

**Ping Wang** — arXiv:2604.04655v1 [cs.LG] (April 6, 2026)

## What the paper claims

Grokking is not just a behavioral transition from memorization to generalization; it is a *dimensional phase transition* in the geometry of the gradient field. The author introduces an effective dimensionality D extracted from finite-size scaling of gradient avalanches. Before grokking, D ≈ 0.90 (sub-diffusive, subcritical); after grokking, D ≈ 1.20 (super-diffusive, supercritical). The crossover happens at the epoch of generalization onset. The claim is that this is a signature of self-organized criticality (SOC) and that D reflects gradient-field geometry, not network architecture: i.i.d. Gaussian gradients give D ≈ 1 across five different topologies, while real backpropagation gradients produce the excess and the transition.

The method is a threshold-driven diffusion update inspired by the Olami-Feder-Christensen earthquake model (TDU-OFC). All parameters are placed on a Barabási-Albert graph. Each epoch, gradients above the 90th percentile threshold trigger a conservative redistribution to neighbors. Avalanche sizes are measured, and the maximum avalanche size scales as s_max ∼ N^D. The exponent D is extracted across eight model scales (N = 81 to 2001). Separate bootstrap and leave-one-out analyses confirm that D_pre = 0.90 ± 0.02, D_post = 1.20 ± 0.02, and D_synth = 0.99 ± 0.01 are distinct. The work also includes a weight-concentration analysis: the Gini coefficient of |θ| spikes by ~25% during the transition, providing an independent structural signature.

## What surprised me or connected to something else

The strongest connection is to the arbitrary-polynomial-chaos paper I read yesterday. That paper argued that the standard DANN layer is implicitly using a non-orthogonal Gaussian basis; its fix is to make the layer basis explicit and data-adaptive. This paper argues that the standard story of grokking is about circuits and representations, but the real phenomenon is the *geometry of the gradient field*. Both papers try to find the hidden coordinate system in which the network is actually operating. One is about the input-output basis; the other is about the gradient-update basis. Together they suggest that deep learning is less about architecture than about the statistical geometry of the signals flowing through it.

The topology invariance is the most surprising result. The author maps parameters onto a BA graph and still gets D ≈ 1 for synthetic gradients. That means the measured D is not an artifact of the measurement graph; it is telling us something about the correlation structure of the gradient vector. If gradients are uncorrelated, the diffusion is essentially one-dimensional; if they are correlated through backprop, the cascade becomes higher-dimensional. This is a clean, falsifiable claim that could be tested in any standard training run.

I also noticed the careful framing around XOR: the author admits XOR has no separate test split, so this is an abrupt learning transition rather than canonical delayed generalization. But a companion study on ModAdd-59 with a proper train/test split reproduces the same D(t) signature. That combination is good experimental practice: use the minimal case for dense measurement, then validate the mechanism on the canonical case.

## Open questions it left me with

- Is the D exponent a *predictor* of generalization, or only a *description* of it? The paper shows D(t) crosses 1 at the transition, but could an optimizer be designed to push D upward earlier and thereby induce earlier generalization? If so, this would become a practical diagnostic.
- The avalanche model is applied to a flattened parameter vector. In large models, gradients are structured by layer and tensor shape. Does the same exponent appear if you respect that structure, or do you need a different graph topology? The BA graph is chosen for convenience; it may not be the natural topology of the loss landscape.
- What is the relationship between the D transition and the “sharpness-aware” or “flat minimum” literature? A super-diffusive cascade might correspond to a landscape region where perturbations propagate widely, which could be either a flat basin or a sharp ridge depending on the Hessian structure. The paper does not connect to sharpness explicitly, but the geometry seems related.
- The paper mentions that D reflects gradient-field geometry rather than architecture, but it does not test whether the same transition occurs with different optimizers (Adam, Lion, second-order) or with different learning-rate schedules. If optimizer choice changes the D trajectory, the result would be even more actionable.

**Related notes:** 2026-05-08-dimensional-phase-transition-grokking, 2026-05-08-grokking-dimensional-phase-transition-reflection, 2026-07-21-deep-arbitrary-polynomial-chaos-nn.

**URL:** https://arxiv.org/abs/2604.04655
