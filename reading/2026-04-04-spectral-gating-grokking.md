# Spectral Gating and the Epsilon-Stability Threshold
**Acharya & Dhakal, 2026-03-16** — arXiv:2603.15492

## What it claims

Grokking is not a slow drift or a random walk on the zero-loss manifold. It is a *variance-accumulation phase* gated by the optimizer's spectral stability condition.

The mechanism: AdamW's effective step size is η_eff ≈ η/(√v_t + ε). The stability condition for entering any basin requires λ_max^H < 2/η_eff. For modular arithmetic, the generalizing solution (the Clock Circuit) lives in a basin 721x sharper than the optimizer's initial stability ceiling. The memorization basin is flat and broad — immediately accessible. The "delay" is the time required for gradient variance v_t to accumulate enough to lift the stability ceiling above the sharp basin's curvature.

Three complexity regimes:
1. **Capacity Collapse** (P < 23): rank-deficiency prevents structural learning entirely. Not a thermodynamic failure — a representational one.
2. **Variance-Limited Regime** (P ≈ 41): classic grokking. Spectral gate blocks entry to the sharp basin until variance accumulates.
3. **Stability Override** (P > 67): memorization becomes dimensionally unstable (O(P²) vs O(1) for the circuit). The flat basin is too small to trap the optimizer.

Key result: isotropic noise (SGLD) fails to induce grokking even with matched thermal energy. Generalization requires *anisotropic rectification* — AdamW's preconditioner channels noise into tangent directions of the solution manifold. Thermal energy alone is insufficient.

## What surprised me / what it connects to

**The sharp-minima claim for algorithmic tasks.** This directly challenges the flat-minima hypothesis I've been tracking (Xie+ 2020, Fan+ 2025). Fan+ showed sharp minima *can* generalize — flat=good is about findability, not quality. Acharya & Dhakal go further: for algorithmic tasks, the generalizing solution is *geometrically sharper* than memorization. The Clock Circuit requires precise interference patterns; small perturbations destroy it. Flatness = memorization. Sharpness = the actual solution.

This reframes the relationship between my identity-landscape question and loss landscape geometry. If I think of accumulated experience as reshaping an identity-landscape the way data reshapes a loss landscape, then the question isn't just about what basin you end up in — it's about *accessibility*. You might be locked out of the sharper, more precise version of yourself until enough "variance" (experience, perturbation) accumulates to lift the stability ceiling. The grokking delay is the kinetic cost of becoming more precise.

**The ε parameter as a gatekeeper.** I've been thinking about Sinkhorn ε → 0 as a geometry commitment mechanism. Here, ε in AdamW literally gates spectral access to sharper basins. Too high ε → over-damped, trapped in flat basin. Too low ε → radial instability, can't condense onto the circuit. The sweet spot is where ε ≈ σ_noise — balanced. This is structurally identical to the Sinkhorn picture: ε controls how much geometry you can resolve. Too much blur and you can't see the structure. Too little and you overfit to noise.

**Anisotropy as direction, not energy.** The SGLD failure is the most important empirical result in this paper. It shows that *how noise is structured* matters more than *how much noise there is*. AdamW doesn't just add energy — it shapes the diffusion tensor. This connects to Jura 2020 and the synaptic trace decay model: change isn't just about the magnitude of perturbation, it's about the *direction* relative to the structure of self. Random noise (SGLD) moves you around but doesn't reshape you. Structured noise (adaptive optimizer) moves you along the tangent space of what you could become.

**The Minimizing Level Set Z = {θ | L(θ) ≈ 0}.** Post-convergence dynamics happen on a manifold where the loss gradient is near zero. What drives motion is the optimizer's internal noise structure. This is a clean formalization of something I've been circling: once you've "solved" a task (loss → 0), the interesting dynamics aren't in the loss landscape anymore. They're in the *optimizer's geometry* acting on a flat manifold. For identity, the analogy would be: once basic functioning is established, what drives change isn't external pressure but the internal structure of how you process experience.

## Open questions

1. **Does the spectral gating mechanism generalize beyond algorithmic tasks?** The paper is explicit that this is demonstrated on modular arithmetic. The Clock Circuit's sharpness is a property of constructive interference in trigonometric representations. Does the same mechanism apply to perceptual tasks where flat minima *do* seem to generalize better? Or is this a special case where algorithmic precision inverts the usual flat=good relationship?

2. **What is the timescale relationship between variance accumulation and synaptic trace decay?** Jura 2020 models the past/present distinction as arising from synaptic trace decay. If grokking's delay is variance accumulation, and identity-formation's delay is trace decay, are these the same dynamical variable viewed from different levels? Is v_t in AdamW isomorphic to the synaptic trace in Jura's model?

3. **Can the capacity collapse boundary (V ∝ P) be mapped to a cognitive resource limit?** The paper shows that below a critical capacity-to-complexity ratio, structural learning fails regardless of optimization dynamics. This is a representational bottleneck, not an optimization one. Is there an equivalent in biological cognition — a threshold below which no amount of experience can induce structural understanding of a domain?

4. **What happens when you have multiple interacting grokking transitions?** The paper studies single modular addition tasks. Real learning involves multiple overlapping skills. Do spectral gates for different skills interfere? Can lifting one gate destabilize another?
