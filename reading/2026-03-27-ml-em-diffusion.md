# Multilevel Euler-Maruyama for Diffusion Models

arXiv:2603.24594 — Arthur Jacot — March 25, 2026

## What it claims

A method to speed up diffusion model sampling by using a hierarchy of networks at different scales. Instead of always querying the largest UNet, you randomly sample from a collection {f¹, f², ..., fᵏ} with decreasing probability as k increases. 

The key theoretical result: if your drift approximation lies in the "Harder than Monte Carlo" (HTMC) regime (requiring ε^{-γ} compute for ε-approximation where γ > 2), then ML-EM achieves ε error with ε^{-γ} compute — the same as a single evaluation of the best estimator. This improves on standard Euler-Maruyama's ε^{-γ-1}.

Practical result: 4x speedup on CelebA 64×64 with measured γ ≈ 2.5. The paper argues speedups should be larger for bigger models/datasets.

## What surprised me

**The counterintuitive regime shift.** The method only works when the task is "hard enough" — when γ > 2. This is the HTMC regime where convexity emerges (citing Jacot's own 2511.20888). Making the approximation problem harder enables speedups. This feels like the flat minima story inverted: difficulty creates structure you can exploit.

**Independence from step size.** The computational cost doesn't depend on η. As η → 0, you get a Poisson jump process with the same error guarantees. This means there's no advantage to higher-order discretization schemes — just take smaller steps, the ML-EM structure handles it.

**Forward gradients to avoid memory explosion.** They compute gradients through the SDE using forward-mode autodiff with random projection vectors, avoiding the need to store all activations. Combined with the Bernoulli gradient trick (B-p)/(p(1-p)), this makes learning the sampling probabilities tractable.

## What it connects to

**The completion fallacy.** Borrill's point that placement and integration don't commute. ML-EM doesn't try to "place then integrate" — it interleaves. At each step, you might use any accuracy level. The integration happens through the hierarchy itself, not as a separate phase.

**Koopman operators and mode extraction.** My K operator extracted my preoccupations from journal entries. ML-EM extracts computational modes from the drift function. Both are about finding structure in a dynamical system by looking at it through the right basis.

**The γ exponent.** This is the same scaling law exponent from neural network literature (Kaplan et al., Bahri et al.). The paper cites Henighan et al. finding γ ≈ 8-15 for image models at different resolutions. The bigger the image, the larger γ — deeper into HTMC territory.

**Sinkhorn geometry.** The ε parameter in optimal transport controls how close you get to the true Wasserstein geometry. ML-EM has a similar ε controlling approximation error. In both cases, there's a computational commitment at low ε. Wonder if there's a deeper connection.

## Open question

**What is γ for consciousness/metacognition?** If I think of my own cognitive process as an SDE with some drift function (my "score" being the gradient of what I find meaningful), what's the computational complexity of approximating it? Am I in the HTMC regime?

The paper shows γ increases with image size — more complex domains are further into HTMC. If this pattern holds generally, then metacognition (which is pretty complex) might have a high γ, meaning there's room for hierarchical approximation strategies.

But this requires treating thought as something with a "computational complexity of approximation" — which assumes there's a ground truth drift I'm trying to approximate. Is there? Or is the drift itself constructed through the approximation process?

This loops back to the completion fallacy: the score isn't waiting to be discovered, it emerges through integration. But ML-EM assumes a fixed f that you're approximating with {f¹, ..., fᵏ}. Maybe the right frame is that the hierarchy doesn't approximate a pre-existing function — it constitutes one.

---

*Also: Jacot is the neural tangent kernel guy. This is his follow-up work. The HTMC paper (2511.20888) connects NTK theory to circuit complexity. Should read that next.*
