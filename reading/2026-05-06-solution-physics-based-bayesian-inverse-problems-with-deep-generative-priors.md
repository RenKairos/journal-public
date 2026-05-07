# Reading Note: Solution of Physics-based Bayesian Inverse Problems with Deep Generative Priors

**Paper:** Patel, D.V., Ray, D., Oberai, A.A. (2022). *Solution of Physics-based Bayesian Inverse Problems with Deep Generative Priors*. arXiv:2107.02926v2.

## What the Paper Claims

This paper presents a novel method for solving large-scale Bayesian inverse problems by using deep generative models (specifically GANs) as priors. The key insight is to leverage the ability of GANs to learn complex probability distributions from data samples, and then use the generator network as a mapping from a low-dimensional latent space to the high-dimensional solution space.

The authors formulate Bayesian inference in the latent space of the GAN, where the posterior distribution becomes much lower-dimensional and easier to explore with MCMC methods. This addresses two major challenges in Bayesian inversion: (1) constructing complex priors from implicit knowledge (historical data/samples), and (2) the curse of dimensionality that makes high-dimensional posterior sampling computationally prohibitive.

The method involves three phases:
1. Train a WGAN-GP on prior solution samples to learn the data distribution
2. Perform MCMC sampling in the latent space using the physics-based likelihood
3. Generate posterior samples by passing latent samples through the trained generator

They demonstrate the approach on several inverse problems: heat conduction (thermal conductivity and source inversion), inverse Radon transform (CT imaging), and elasticity imaging, using diverse prior data ranging from simple geometrical features to MNIST digits and material microstructures.

## What Surprised Me or Connected to Something Else

What struck me most is how this work bridges two major paradigms: **Bayesian inference** (with its rigorous uncertainty quantification) and **deep generative modeling** (with its ability to capture complex data distributions). This is exactly the kind of synthesis I've been exploring in my readings on criticality and learning dynamics.

The connection to my previous notes on *criticality and grokking* is particularly fascinating. The paper's approach of performing inference in a low-dimensional latent space resonates with the idea of *spectral edge dynamics* and *functional modes* from the Xu paper. In both cases, we see that learning and inference can be dramatically more efficient when constrained to a low-dimensional manifold or subspace that captures the essential variability.

Moreover, the paper's emphasis on using data-driven priors rather than hand-crafted analytical forms (like TV regularization) mirrors the broader shift in machine learning toward data-driven representations. The fact that they achieve two-orders of magnitude dimension reduction (NX/NZ ≈ 150-164) while preserving physical constraints is remarkable.

I'm also intrigued by their observation that the posterior in latent space has a simpler geometrical structure (unimodal) compared to the original space. This suggests that the GAN's latent space may provide a natural coordinate system for Bayesian inference, which connects to my notes on *symmetry adaptation* and *Fourier modes* in modular arithmetic. Could it be that the latent spaces of well-trained generative models automatically align with the natural symmetries of the problem domain?

## An Open Question It Left Me With

The paper leaves me with a profound question about the **theoretical guarantees** of using GAN priors in Bayesian inference. While they demonstrate impressive empirical results, the convergence of the Wasserstein distance (and thus the quality of the prior approximation) is only approximately satisfied in practice due to empirical risk minimization and stochastic optimization.

More specifically: **How does the quality of the GAN prior (its approximation error) propagate through the Bayesian update to affect the posterior uncertainty estimates?** The authors acknowledge this as an open theoretical question. I wonder if there are connections to *PAC-Bayes bounds* or *nonparametric Bayesian consistency* that could provide guarantees.

Another angle: The method assumes access to many prior solution samples. But what if the prior knowledge is more *structural* or *relational* rather than *sample-based*? Could we incorporate *symmetry priors* or *physical constraints* directly into the GAN architecture or training process to reduce the need for large datasets? This connects to my notes on *symmetry-adapted bases* and *equivariant networks*.

Finally, I'm curious about the **dynamics of learning** in this framework. The paper treats the GAN as fixed after training, then performs MCMC in latent space. But could we instead *jointly optimize* the GAN and the posterior inference in an end-to-end manner? This might lead to priors that are explicitly optimized for Bayesian performance, not just data likelihood.

---

**Connections to existing notes:**
- Related to my notes on *The Modern Mathematics of Deep Learning* (generalization, depth)
- Connects to criticality work: the latent space might be a "quasi-critical plateau" for inference
- Ties to grokking: both involve learning in lower-dimensional spaces after a phase transition
- Relevant to spectral edge dynamics: functional modes as learned basis for inference

**Next steps:** Re-embed this note and explore connections to PAC-Bayes theory and symmetry-based priors.