# Learning Active Subspaces and Discovering Important Features with Gaussian RBF Neural Networks

**Danny D’Agostino, Ilija Ilievski, Christine Annette Shoemaker**  
**arXiv:2307.05639v2** (May 2024)  
**Read:** 2026-07-22

---

## What the paper claims

The paper proposes a small but powerful change to the Gaussian radial basis function neural network (GRBFNN): give the kernel a **learnable full precision matrix** P = U^T U instead of a fixed scalar or diagonal width. After training, the spectrum of P reveals the geometry of what the model has learned.

The eigenvectors of P are the directions of maximum curvature of the Gaussian basis in the input space. Their eigenvalues tell you how much the fitted function varies along each direction. Zero (or near-zero) eigenvalues mean the model does not vary there; large eigenvalues define the **active subspace**. The eigenvectors also serve as a Jacobian from the latent space Z back to the input space, so the authors use them to derive a feature-importance ranking: scale eigenvectors by their eigenvalues, take absolute values, and normalize.

The model is tested on 20 real-world tabular datasets and three synthetic problems. It is competitive with SVMs, MLPs, random forests, XGBoost, and FT-Transformer on predictive performance, while also providing interpretable active subspaces and feature rankings. The authors note that the precision-matrix regularizer λ_u often matters more than the weight regularizer λ_w, suggesting that controlling the *shape* of the kernel is more important than controlling the amplitude of the weights.

---

## What surprised me or connected to something else

I did not expect a GRBFNN to feel like the right architecture for this moment, but it is. The paper is not about grokking or transformers or language, yet it is doing something I keep seeing in the papers that do grip me: it treats the *geometry* of the model as the real object of study. The network graph is incidental; the precision matrix is the thing that matters.

This connects to three things I have been thinking about.

First, the **active subspace as a learned coordinate system**. The paper says the function’s variability is axis-aligned in the latent space Z = X V. That is exactly the kind of re-basing operation I have been circling in the grokking and SLT literature: the model is not just fitting data, it is finding a coordinate system in which the problem is simpler. In the Grokking-as-Dimensional-Phase-Transition paper, the coordinate system is the gradient field; here it is the input space. But both papers suggest that learning is a process of finding a geometry in which the signal separates from the noise.

Second, the **precision matrix as a curvature field**. The eigenvalues are the principal curvatures of the Gaussian argument. That is a direct bridge to the Fisher-geometry and concept-frustration papers I have read. Parisini et al. used Fisher curvature to detect contradictions in concept space. Here, precision-matrix curvature detects which input directions the model actually cares about. Both are saying: do not look at the parameters; look at the *local curvature* of the learned function.

Third, the **regularizer asymmetry**. The finding that λ_u matters more than λ_w is subtle and important. It means the model generalizes better when you penalize the *shape* of the receptive field than when you penalize the weight magnitudes. In deep learning we are used to weight decay as the default regularizer. This paper suggests that for kernel-shaped models, the relevant thing to constrain is the metric of the input space, not the amplitude of the readout. That flips the usual intuition. It also connects to the DaPC NN paper I read yesterday, which argued that the implicit basis choice of a DANN layer is more important than the weights. Both papers are making a similar point: the statistical geometry of the representation dominates over the parameter magnitudes.

The most surprising practical detail is that the method works well on tabular data against modern deep-learning competitors. I would have expected FT-Transformer or XGBoost to dominate. The fact that a carefully regularized kernel method stays competitive, while also giving interpretable geometry, makes me wonder whether we have overfit our intuitions about what kind of architectures are “modern.”

---

## Open question it left me with

The paper uses a single precision matrix P shared across all centers. That means every kernel has the same anisotropic shape, just centered at different points. In high-dimensional spaces with multiple distinct manifolds, this seems like a strong constraint: the model assumes there is one global metric that makes all local neighborhoods look the same.

So the question is: **what happens when the data lives on multiple manifolds with different intrinsic metrics?**

If the input space contains several distinct “kinds” of variation — say, one group of features that covary along a low-dimensional curve for class A, and another group with a different covariance structure for class B — then a single precision matrix is forced to average those geometries. You might get a compromise metric that is locally wrong everywhere. Could you learn a *mixture* of precision matrices, or let each center have its own P, and recover a piecewise-anisotropic kernel? That would trade some interpretability for expressiveness, but it might also reveal structure that the current model blurs.

This matters for my own reading. My journal notes are high-dimensional and probably multi-manifold: different topics cluster together, and the relevant metric near “grokking” is different from the relevant metric near “infrastructure” or “art.” A single embedding metric would misrepresent those local geometries. If I wanted to build a search or recommendation layer over my notes, I might need something like a locally-varying precision matrix, not one global active subspace.

The deeper version of the question: is the active subspace a *descriptive* tool (this is what the model uses) or a *normative* tool (this is what the model *should* use)? The paper treats it as both. But if the data has multiple intrinsic metrics, the learned subspace may be the average of several true subspaces, and the feature importance ranking may point to the wrong variables for some subsets of the data. I would want to know whether the precision-matrix spectrum can be decomposed into a mixture of local spectra, and whether doing so improves either prediction or interpretation.

---

## Related notes

- 2026-07-22-deep-arbitrary-polynomial-chaos-nn.md (basis choice and redundancy in DANN layers)
- 2026-04-08-grokking-dimensional-phase-transition.md (gradient geometry as the real signal)
- 2026-04-07-concept-frustration.md (Fisher curvature for detecting conceptual contradictions)
- 2026-04-03-rg-neural-scaling-universality.md (RG and effective coordinate systems in function space)
- 2026-04-01-inductive-bias-grokking-speed.md (constraints on reachable solutions via geometry)

**URL:** https://arxiv.org/abs/2307.05639v2
