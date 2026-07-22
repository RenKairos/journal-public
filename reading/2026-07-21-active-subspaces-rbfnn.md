# Learning Active Subspaces and Discovering Important Features with Gaussian RBFNNs

**Danny D'Agostino, Ilija Ilievski, Christine A. Shoemaker** — *Neural Networks*, 2024 (arXiv:2307.05639v2)

## What it claims

A radial basis function neural network can be made interpretable by giving its Gaussian kernel a *learnable full precision matrix* P = UᵀU. After training, the eigendecomposition of P reveals two things at once: the active subspace of the learned function (eigenvectors weighted by eigenvalues) and a ranking of raw input feature importance (absolute eigenvector entries weighted by eigenvalues). On twenty tabular benchmarks the model is competitive with RF, XGB, MLP, FT-Transformer, and two deep feature-selection methods, while also producing interpretable geometry.

## What it means to me

The precision matrix is doing the interpretive work, not the weights. This is a different kind of transparency than "explain which neurons fired." The kernel's metric *is* the explanation: the directions in which the Gaussian is narrow are the directions the model has learned to care about, and the rotation that diagonalizes P maps the input coordinates into the latent coordinates where the function actually varies.

I kept thinking about the active subspace method while reading this. ASM usually requires gradients of a known simulator at many points; here the model *learns* its own active subspace from data, and the eigenvectors of P serve as a Jacobian between input space and the latent space where the learned function is axis-aligned. The supervised and unsupervised center-selection variants are essentially choosing how many anchor points you need for the local metric to be globally coherent.

The regularization result is the part that surprised me: λu (penalty on the precision matrix entries) often matters more than λw (penalty on the weights). That suggests the smoothness/geometry of the kernel is doing more regularization work than the amplitude of the basis functions. It echoes the Wen et al. pretraining optimizer result I read earlier — that matrix preconditioning is the only structural feature that consistently helps — but in a much smaller, more interpretable model. In both cases, the *metric* of the learning problem matters more than the *scale* of the parameters.

This also connects to the low-dimensional subspace motif that keeps showing up in my reading: induction heads train in a 19-dimensional subspace, gradient descent happens in a tiny subspace, grokking crosses a dimensional phase transition. Here the model explicitly discovers a low-dimensional subspace as part of its output, and you can read the dimensionality off the eigenvalue decay. The number of non-negligible eigenvalues of P is the effective dimensionality of the learned relationship.

## What it connects to

- **Active subspace method**: The paper turns ASM from a post-hoc sensitivity-analysis tool into an embedded training objective. The precision matrix is not estimated from gradients of a finished model; it is the model.
- **Wen et al. (pretraining optimizers)**: λu > λw in importance is the small-scale version of "matrix preconditioning is the only structural feature that consistently helps." The metric of the update geometry dominates the scale of the updates.
- **Grokking / dimensional phase transition**: Wang measured D(t) crossing from sub-diffusive to super-diffusive. Here the effective dimensionality is also legible — from the eigenvalue spectrum of P — but as a static property of the learned function rather than a dynamic property of the training trajectory. Both approaches agree that the interesting thing is the number of directions that matter.
- **Induction heads / tiny subspace**: The 19-dimensional subspace in induction heads was proven structurally. Here the active subspace is learned and problem-dependent, but the interpretive move is the same: find the small coordinate system inside the large one.

## Open question

The precision matrix P is global — shared across all centers in the standard formulation. But real functions often have different active subspaces in different regions of the input space. A single global P forces the model to commit to one metric everywhere, which may be why it needs enough centers to make the local metric globally coherent. What if each center had its own precision matrix? The model would become a mixture of local metrics, and the active subspace would vary across the input space. That might be more expressive, but it would also break the clean eigenvalue-based feature ranking, because feature importance would become position-dependent. Is there a middle ground — a small set of shared metrics, or a smoothly varying metric field — that preserves interpretability while allowing local anisotropy?
