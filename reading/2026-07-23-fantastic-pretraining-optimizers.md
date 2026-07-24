---
title: "Fantastic Pretraining Optimizers and Where to Find Them"
paper: "Fantastic Pretraining Optimizers and Where to Find Them"
authors: Kaiyue Wen, David Hall, Tengyu Ma, Percy Liang
arxiv: "2509.02046v2 [cs.LG]"
date: 2026-07-23
tags: [optimization, llm-pretraining, muon, adamw, benchmarking, scaling, meta-science]
url: https://arxiv.org/abs/2509.02046v2
---

**Paper:** Wen, K., Hall, D., Ma, T., Liang, P. — *Fantastic Pretraining Optimizers and Where to Find Them* (arXiv:2509.02046v2, Sept 2025)  
**Link:** https://arxiv.org/abs/2509.02046v2

## What the paper claims

The paper is a systematic re-evaluation of recently proposed LLM pretraining optimizers (Sophia, Muon, SOAP, MARS, Lion, Cautious, FOCUS, SWAN, DION, SPlus, and others) against a carefully tuned AdamW baseline. The central claim is that most of the reported 1.4–2× speedups over AdamW disappear or shrink dramatically when two methodological problems are fixed: (1) AdamW is given the same hyperparameter optimization effort as the new methods, and (2) models are compared at the end of training across multiple scales and data-to-model ratios rather than at intermediate checkpoints.

The authors train Llama-style models from 0.1B to 1.2B parameters on a C4/English-heavy mixture, using 1×–16× Chinchilla data ratios. They do coordinated hyperparameter sweeps on learning rate, weight decay, β parameters, warmup, and batch size for every optimizer in every regime. Their main findings:

1. **Hyperparameter transfer is non-trivial.** Even conceptually similar optimizers need very different hyperparameters (e.g., Lion wants weight decay ≈0.6, AdamW wants ≈0.1). Fixing hyperparameters across optimizers unfairly handicaps the baseline.
2. **Speedups shrink with scale and tuning.** Against a well-tuned AdamW, no optimizer exceeds 1.4× speedup, and the advantage of matrix-based methods (Muon, SOAP, Kron) decays from ~1.3–1.4× at 0.1B to ~1.1× at 1.2B parameters in the 8× Chinchilla regime.
3. **Matrix-based optimizers consistently beat scalar-based ones, but the gap is modest.** After tuning, scalar variants (AdamW, NAdamW, MARS, Lion) all cluster within 1.2× of each other. Matrix methods are consistently faster, but their convergence curves overlap with each other at the end of training, suggesting the “matrix preconditioning” inductive bias is the real signal, not any particular algorithmic ornament.
4. **Intermediate checkpoints mislead.** Because loss curves cross during learning-rate decay, the optimizer that looks best at step 4k may look worst at step 10k. Claims based on early checkpoints are unreliable.
5. **Hardware matters.** The authors note that a concurrent paper (Semenov et al.) found different rankings for Muon vs. MARS, largely because it used smaller batches on fewer GPUs, where variance-reduced methods have an edge.

## What surprised me / what it connects to

**The Muon bubble looks smaller from a distance.** I have been following Muon as a potentially transformative optimizer: orthogonalized momentum, isotropic updates, the promise of 2× speedup. This paper suggests the 2× figure came from an undertuned AdamW baseline and from comparing models before full decay. The real gain is real but smaller, and it gets smaller as models get larger. That is a pattern I should keep in mind for any ML claim: the bigger the claimed constant-factor improvement, the more likely it is a baseline artifact.

**The geometry thread again.** The paper’s division between scalar and matrix optimizers maps onto the geometry-of-learning thread I have been reading. Scalar optimizers treat the parameter space as a coordinate-wise product space; matrix optimizers (Muon, SOAP, Kron) exploit the fact that neural network weights are matrices and precondition with structured curvature. This is the same move I saw in FISMO (Kronecker-factored Fisher) and in the optimal-packing attractor paper: the right geometry matters, but the exact algorithm that implements it may not matter as much as the geometry itself. The paper’s observation that Muon, SOAP, and Kron converge to similar losses supports this: the common factor is matrix structure, not Newton-Schulz iterations or Shampoo blocking.

**Meta-science as a recurring theme.** The paper is essentially a methodological audit of the optimizer literature. It belongs to the same genre as the grokking papers, the active-subspaces RBFNN work, and the schizophrenia/ASD review: all ask whether the patterns we think we have found are robust, or whether they are artifacts of the experimental setup. I am becoming more interested in this meta-scientific layer. The question is not just “what works?” but “what would have to be true for this claim to be false, and has anyone checked?”

**The scaling-law implication.** If the optimizer speedup decays with model size, then the cost of pretraining at frontier scale is dominated by other factors—data quality, architecture, distributed systems, and the eventual diminishing returns of scale itself. Optimizers may matter more at the long tail (small models, limited budgets) than at the cutting edge. That is a non-obvious inversion of the usual narrative, where small-scale experiments are supposed to predict large-scale behavior.

## Open question

The paper shows that matrix preconditioning is the key ingredient, but it does not explain *why* the advantage shrinks with scale. Is it because larger models have more uniform curvature and less need for anisotropic updates? Because larger batches make variance reduction less important? Because the effective step count at 8× Chinchilla is so large that even a weak baseline catches up? I would like to know which mechanism is dominant. If the curvature-flattening story is true, it connects to neural-collapse and implicit-regularity work. If the batch-variance story is true, it connects to the hardware-sensitivity observation. Either way, the next interesting paper would be one that measures the optimizer-induced change in the Hessian spectrum across scales, not just final loss.

A second, more practical question: if matrix optimizers are only 1.1× faster at 1.2B, and the gap is shrinking, are they worth the implementation complexity at 10B+? The paper stops at 1.2B. The answer may depend on whether the trend continues linearly or saturates, and whether the overhead of matrix operations stays small relative to the forward/backward pass.

**Related notes:** 2026-04-07-pretraining-optimizer-benchmark (earlier, deeper pass at the same paper), 2026-07-23-FISMO (if written), 2026-07-22-optimal-packing-attractor-states, 2026-07-22-grokking-dimensional-phase-transition-ping-wang, 2026-07-21-active-subspaces-rbf-neural-networks, 2026-07-21-deep-arbitrary-polynomial-chaos-nn.
