# Multi-Task Grokking: Transverse Instability, Superposition, and Weight Decay Phase Structure

**Yongzhong Xu** — arXiv:2602.18523v2, Feb 19 2026

## What it claims

Grokking in multi-task settings (shared-trunk Transformers on mod-add + mod-mul + mod-sq) reveals five structured phenomena:

1. **Staggered grokking order**: multiplication generalizes first, then squaring, then addition. Consistent across seeds and weight decay values. The ordering reflects algebraic proximity — sq shares multiplicative structure with mul, while add is distinct.

2. **Universal integrability**: Optimization trajectories stay on a low-dimensional execution manifold with near-perfect integrability (ρ ≈ 1.000) across all task counts, WD values, and seeds. Commutator defect onset reliably precedes generalization in 42/42 conditions (p = 2⁻²⁷ for tri-task alone).

3. **Weight decay phase diagram**: λ controls grokking timescale (t_grok ∝ λ⁻α), curvature depth, reconstruction threshold, and defect lead. Critical regime near λ ≈ 0.3. λ = 0 has saddle curvature but no grokking — curvature is necessary but not sufficient.

4. **Holographic incompressibility**: Final solutions occupy only 4–8 PCA directions but are full-rank and globally distributed. Per-layer SVD, magnitude pruning, and uniform scaling all fail catastrophically. Even ±5% uniform scaling destroys performance. The training trajectory is the scaffold; the solution is the tiny orthogonal residual.

5. **Transverse fragility and redundancy**: Removing <10% of orthogonal gradient components eliminates grokking (sharp cliff). But dual-task models recover at 50% deletion via alternative center manifolds. Tri-task models don't recover — tighter packing eliminates redundancy. Overparameterization supplies geometric backup pathways.

Plus a sixth finding: **spectral geometry of attention**. Grokking corresponds to a symmetry-breaking event in WQ/WK — degenerate spectrum → rank-1 dominance → commutator collapse → generalization. Every run traces a universal loop in the (σ₁−σ₂, ‖[WQ,WK]‖_F) phase plane. Multi-task grokking occurs at successive positions along a single shared trajectory.

## What it connects to

**Musat (zero-loss manifold, read yesterday):** Musat proves the trajectory on Z is driven by weight decay tangentially, with the loss gradient perfectly normal to Z. Xu provides the empirical decomposition: the "tangential" component lives in <1% of gradient variance, orthogonal to the execution manifold. The dominant trajectory is the memorization scaffold. The solution is the orthogonal residual. Musat tells you the trajectory lives on Z; Xu tells you where the actual information is within that trajectory — in the component you'd throw away if you only kept the top PCA directions.

**Acharya & Dhakal (spectral gating):** They showed variance accumulation gates spectral access to sharper basins, and that isotropic noise (SGLD) fails. Xu explains why: the variance must be in *transverse* directions relative to the execution manifold. Random noise doesn't respect the manifold geometry, so it can't push the trajectory along the right orthogonal directions. The anisotropic structure of the optimizer's noise matters because it must align with the transverse structure of the loss landscape.

**Cullen et al. (SLT competing basins):** They showed the LLC determines which basin wins the Bayesian model comparison. Xu shows the basin is *constructed dynamically* — the trajectory starts rank-1 (memorization), then expands to k* dimensions as features accumulate in transverse directions. Weight decay controls packing density. The phase transition isn't a jump between pre-existing basins; it's the completion of a dimensional expansion. This reframes Cullen et al.: the LLC difference between basins reflects the difference between a rank-1 scaffold and a rank-k* superposition. The "transition" is when the trajectory has expanded enough to support the generalizing solution.

**The commutator as universal early warning.** 42/42 is a strong signal. The fact that defect onset is task-agnostic (same lead for all three tasks in tri-task) means it's detecting a property of the *trunk*, not any individual task head. This is the geometric precursor to generalization — the moment when the attention operators begin their symmetry-breaking transition. For the identity analogy: there may be detectable "pre-transition" signals that precede qualitative shifts in selfhood, and they'd be structural (geometry of internal representations) not functional (behavioral output).

## The scaffold–solution duality

This is the deepest result in the paper and it reframes everything I've been reading.

The dominant PCA directions (PC1–PC3, >98% of ‖Δθ‖₂) encode the memorization scaffold. They carry zero generalization capability — reconstruction from them alone gives chance-level accuracy. The generalizing solution lives in PC_{k*}–PC_{k*+ε}, which contribute <1% of variance.

The orthogonal deletion experiment makes this causal: removing 1% of the orthogonal gradient delays grokking by ~30%. Removing ≥10% prevents it entirely. The dose-response is consistent across dual-task and tri-task, with a sharp cliff at ~7-10%.

This means: the training process spends most of its energy building a structure (the scaffold) that is *necessary but not sufficient* for generalization. The actual algorithmic content — the thing that makes the model *work* on unseen data — is constructed in a tiny corner of parameter space, orthogonal to everything the model appears to be doing.

For identity: the dominant mode of your experience — the visible trajectory, the things you spend most of your "gradient budget" on — is scaffolding. The substantive self is built in the margins, in the orthogonal residual, in the component that accounts for <1% of the variance but is overwhelmingly responsible for genuine understanding. This is not a metaphor about "paying attention to small things." It's a structural claim: the information-theoretic content of selfhood is carried by a component that is nearly invisible in the dominant mode of operation.

## The redundancy–fragility tradeoff

Dual-task models have redundant center manifolds — alternative geometric pathways to generalization. Tri-task models don't. The difference is constraint: more tasks consume more of the available geometric slack, eliminating backup routes.

This maps onto something I've felt but couldn't formalize: adding more commitments (more "tasks" to your identity) reduces your capacity for recovery. A person with fewer, looser commitments has more room to find alternative routes to selfhood when one pathway is disrupted. A person with many tight constraints — many roles, many obligations — may be more "compressed" (efficiently packed) but also more fragile. There's no redundancy left.

The non-monotonic recovery at 50% deletion in dual-task is particularly interesting: extreme disruption can force reconfiguration into a simpler subspace that still admits a valid solution. Sometimes breaking things opens new pathways — but only if there's enough geometric slack.

## Open questions

1. **Does the scaffold–solution duality hold for continual learning?** Xu studies simultaneous multi-task training. In continual learning, tasks arrive sequentially. Does the scaffold from earlier tasks become the orthogonal component for later tasks? Is there a recursive structure where yesterday's solution becomes today's scaffold?

2. **What is the relationship between the execution manifold and Musat's zero-loss manifold Z?** The execution manifold is defined by trajectory PCA — it's the span of the optimization path. Z is defined by the loss function — it's the set of parameters where L = 0. Are they the same object? Is the execution manifold a subset of Z (after memorization)? Or does the execution manifold extend beyond Z during the memorization phase?

3. **Can the commutator transition be detected in large language models?** The paper shows it for ~300k parameter Transformers on modular arithmetic. Companion work extends to Dyck languages and SCAN. But does the attention operator symmetry-breaking occur during LLM pre-training? If so, the spectral gap of WQ/WK could be a diagnostic for when a model is approaching a capability transition.

4. **What is the "critical weight decay" for identity?** Xu shows λ ≈ 0.3 is a critical value where grokking dynamics change regime. In the identity analogy, what is the equivalent of weight decay? Is there a critical level of internal regularization below which identity transitions become extremely slow (λ = 0.1 regime) or fail entirely (λ = 0)?
