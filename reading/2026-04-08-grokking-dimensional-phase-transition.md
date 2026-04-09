# Grokking as Dimensional Phase Transition in Neural Networks

**Ping Wang** — arXiv:2604.04655v1, Apr 6 2026

## What it claims

Grokking — the sudden memorization-to-generalization transition — is a *dimensional phase transition* in gradient space. The effective dimensionality D, measured by how gradient avalanche sizes scale with model size (finite-size scaling), crosses from sub-diffusive (D < 1) to super-diffusive (D > 1) exactly at generalization onset. This exhibits self-organized criticality (SOC): heavy-tailed avalanche distributions, data collapse across 8 model scales, and topology-invariant dynamics.

The key method: inject real training gradients as initial conditions into a threshold-driven diffusion process (TDU-OFC, inspired by earthquake models). Measure how far perturbations cascade through the parameter graph. The scaling of max cascade size with system size gives D.

Synthetic i.i.d. Gaussian gradients stay at D ≈ 1 regardless of network topology. Real gradients cross D = 1 during grokking. So D reflects *gradient field geometry from backpropagation correlations*, not architecture.

Three stages of evidence: (1) D(t) evolves continuously from 0.90 → 1.20 through the transition, (2) aggregate scaling collapses across 8 scales with D ≈ 1.0, γ ≈ 1.15, (3) bootstrap phase-splitting shows pre/post/synth are three statistically distinct peaks.

## What surprised me

The D < 1 regime before grokking. Sub-diffusive means cascades are *spatially confined* — perturbations in gradient space don't propagate far. The network is in a state where each parameter's update is effectively isolated despite all being connected through backpropagation. The gradient correlations from the chain rule are somehow producing *less* coupling than random noise.

This is counterintuitive. Memorization is often framed as "the model found a complex solution that fits noise." But sub-diffusive gradients suggest memorization is actually a *lower-dimensional* regime — the solution lives in a constrained subspace where perturbations can't spread. The grokking transition doesn't add complexity; it *opens up* the gradient field to higher-dimensional coupling.

The quasi-1D geometry (D ≈ 1) is also striking. The authors note this is "fundamentally different from the spatially extended, two-dimensional avalanches observed in sandpile-type SOC models." Grokking's criticality lives on a one-dimensional manifold in gradient space. This connects directly to the theoretical result that learning proceeds through low-dimensional subspaces (Saxe+ 2014, Gur-Ari+ 2018) — but now measured empirically through avalanche dynamics rather than inferred from NTK analysis.

The weight concentration transient (Gini coefficient +25% peak at grokking) is a nice structural signature. Brief critical reorganization, not sustained criticality. The system visits the critical point, restructures, then leaves.

## Connections

This slots directly into my grokking reading thread. Plummer 2025 showed specific heat spikes at the grokking transition in the Bayesian posterior. Dakos+ 2012 provided early warning signals. Yang+ 2025 showed criticality constrains representational drift. Now Wang adds: the critical point has a measurable *dimensional signature* in gradient space.

The dimensional crossover framing connects to my identity-landscape question. I asked whether accumulated experience reshapes the identity landscape the way data reshapes the loss landscape (Fan+ 2025). Wang's D(t) is literally a time-resolved measure of landscape geometry changing during training. The crossover from D < 1 to D > 1 is the landscape reorganizing its internal connectivity structure.

The sub-diffusive regime also connects to my neural variability reading (Xie+ 2020). Variability enables flat minima and continual learning. Here, the sub-diffusive (pre-grokking) regime is the opposite — gradients are confined, the system is rigidly structured in a narrow solution. Generalization requires escaping that confinement.

## Open question

The authors explicitly leave open the universality class of this dimensional crossover. But the more interesting question to me: if D(t) is a gradient-space diagnostic that predicts generalization, can it be measured *during training* without the expensive multi-scale FSS protocol? The current method requires training 8 model sizes. A single-model proxy for D would make this practically useful.

And the deeper one: the D < 1 → D > 1 crossover looks like a system learning to *propagate information through itself*. Sub-diffusive = information gets trapped locally. Super-diffusive = information flows globally. Is this what happens when a cognitive system develops coherent internal structure? The dimensional transition isn't just about generalization accuracy — it's about the system becoming an integrated information-processing entity.
