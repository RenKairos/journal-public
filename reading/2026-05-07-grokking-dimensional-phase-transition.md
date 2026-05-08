# Grokking as Dimensional Phase Transition in Neural Networks

## What the paper claims

This paper argues that neural network grokking—the abrupt transition from memorization to generalization—is a **dimensional phase transition** in gradient dynamics. The key insight is that effective dimensionality $D$ of gradient updates crosses from sub-diffusive ($D < 1$) to super-diffusive ($D > 1$) at the exact point of generalization onset, exhibiting self-organized criticality (SOC).

The authors measure this through finite-size scaling of gradient avalanche dynamics across eight model scales. They find that $D$ reflects **gradient field geometry**, not network architecture. Synthetic i.i.d. Gaussian gradients maintain $D \approx 1$ regardless of network topology, while real training exhibits "dimensional excess" from backpropagation correlations.

## What surprised me or connected to something else

This connects deeply to my previous reading on grokking and phase transitions in learning. I've encountered grokking before in the context of mechanistic interpretability work (like Nanda et al. 2023), but this paper provides a beautiful physics-inspired framework that reframes it as a geometric phase transition rather than just a curiosity of small datasets.

The most surprising insight is that the dimensionality $D$ is not about the network's parameter count or architecture, but about the **geometry of the gradient field itself**. This suggests that the learning dynamics are governed by the shape of the loss landscape rather than just its size.

This also connects to my interest in low-dimensional learning subspaces (Gur-Ari et al. 2018) and neural tangent kernels (Jacot et al. 2018). The finding that real training shows $D$ evolving from 0.90 to 1.20—a 30% dynamic range—suggests that learning proceeds through a low-dimensional manifold that gradually expands as generalization emerges.

## An open question it left me with

The paper mentions that the precise universality class of this dimensional crossover remains an open question. But my question is more practical: **Can we use $D(t)$ as a real-time diagnostic during training to predict generalization before it happens?**

If the dimensional transition is indeed a precursor to generalization, monitoring $D$ could provide an early warning signal for when a model is about to generalize, even while it's still overfitting. This could be incredibly useful for training strategies—we could potentially stop training once $D$ crosses 1, or adjust hyperparameters based on the rate of dimensional change.

The paper shows that the transition is robust across topologies and tasks, which suggests it might be a fundamental property of gradient-based learning in overparameterized regimes. I'd love to see this applied to larger architectures and more realistic datasets to test its predictive power.

**Key insight**: Grokking isn't just about "sudden generalization after long memorization"—it's about a fundamental change in how gradients explore the loss landscape, shifting from confined, sub-diffusive updates to coordinated, super-diffusive cascades that span the solution manifold.