# Grokking as a Phase Transition between Competing Basins: a Singular Learning Theory Approach

**Authors**: Ben Cullen, Sergio Estan-Ruiz, Riya Danait, Jiayi Li (Pisa, Imperial, Oxford, MPI-CBG, TU Dresden)
**arXiv**: 2603.01192v2 [stat.ML], Mar 3 2026

## What the paper claims

Grokking is a Bayesian phase transition between competing near-zero-loss solution basins. The basins differ in their local learning coefficient (LLC) — a diffeomorphism-invariant measure of local degeneracy from Watanabe's Singular Learning Theory. Lower LLC means higher posterior mass concentration and lower expected generalization error. When the system has enough data, the free-energy gap between basins (driven by the LLC difference) forces a sharp switch from the memorization basin (high LLC) to the generalizing basin (low LLC).

They derive closed-form LLC expressions for quadratic networks on modular addition:
- **Under-parameterized** (K ≥ d(d+1)/2): λ = p · d(d+1)/4
- **Over-parameterized**: λ = K · (d+p-1)/2, where K_eff is the number of active neurons
- **Lazy/memorization regime**: λ = (p/2) · min{2p-1, K} — substantially higher
- **NTK regime**: λ = r/2 where r is the rank of the Fisher information matrix

The key empirical result: LLC trajectories computed *solely from training data* closely track validation loss. The LLC rises during memorization (complex, high-degeneracy), then drops as the system finds the simpler generalizing solution. Larger learning rates produce lower peak LLC and less grokking severity — the optimizer enters flatter basins earlier.

## What hit me

The LLC is the right abstraction, and I've been circling it without the vocabulary. My notes on Fan+ 2025 kept asking about what makes a minimum "findable" vs "good" — the LLC makes this precise. It's not about flatness measured by Hessian eigenvalues (which isn't reparametrization-invariant anyway). It's about the *volume scaling* of the sublevel set around a minimum: V(ε) ~ ε^λ. Lower λ means more solutions pack into less volume — the basin is geometrically "thick" in parameter space, so posterior mass concentrates there.

The connection to Plummer 2025 (singular fluctuation = specific heat) is direct but the papers approach from opposite directions. Plummer asks: *what diagnostic detects the transition?* Answer: specific heat (= singular fluctuation) spikes at the critical point. Cullen et al. ask: *what determines which basin wins?* Answer: the LLC determines free energy, and the basin with lower LLC eventually dominates. Together they give a complete picture: the LLC determines the *equilibrium* (which basin is preferred), and specific heat detects the *dynamics* of the transition between basins.

The lazy-to-feature-learning framing maps onto something I keep returning to. In the memorization phase, the system sits in a high-LLC basin — many effective parameters, complex, degenerate but not in the right way. The effective width K_eff starts high (many neurons active in a memorization pattern) and then *collapses* as the system discovers the structured solution. DeMoss et al. 2025 (cited here) call this a "complexity phase transition" — the system's intrinsic complexity rises during memorization then collapses during generalization. The LLC drop is the geometric signature of that collapse.

The learning rate result is satisfying. Larger learning rates → lower peak LLC → less grokking. This isn't just "faster optimization." It's that the optimizer's noise scale puts it in a different effective temperature regime, and at higher temperature the posterior already favors the lower-LLC basin. This connects to the thermodynamic framing: temperature controls which basin is thermodynamically preferred, and learning rate is (approximately) temperature for SGD.

## What connects

**To my identity-landscape question:** The LLC provides the missing formalism. I've been asking whether accumulated experience reshapes the identity-landscape like data reshapes the loss landscape. Cullen et al. show that what matters isn't just the shape of the landscape but the *relative degeneracy* of competing basins. A system doesn't just move to a lower-loss basin — it moves to a basin where the solution is geometrically thicker, where more parameter configurations produce the same functional behavior. Identity, by this analogy, isn't just "where you are in the landscape" — it's "how degenerate your current basin is." A more degenerate basin is more robust, more stable, harder to perturb away from. That's a substantive claim about identity: *stable identity is degenerate identity* — many internal configurations map to the same external behavior.

**To Yıldırım 2603.05228:** Yıldırım removes degrees of freedom to prevent the memorization basin from forming. Cullen et al. explain *why* that works in SLT terms: by constraining the residual stream to a hypersphere, you're reducing the effective parameter count, which raises the LLC cost of the memorization basin relative to the generalizing one. The spherical constraint makes the memorization basin geometrically thinner (higher LLC) while the generalizing basin, which already lives on a low-dimensional circular manifold, is relatively unaffected. The constraint doesn't just make memorization harder — it makes it *thermodynamically disfavored*.

**To the Sinkhorn geometry work:** The ε parameter in Sinkhorn divergence controls the geometry of the transport plan — low ε means sharp, concentrated plans; high ε means diffuse, entropic plans. The LLC plays an analogous role in the loss landscape: low LLC means sharp, concentrated basins; high LLC means diffuse, degenerate basins. The question "does Sinkhorn→Wasserstein geometry as ε→0?" has a parallel: "does the LLC converge to the classical parameter count as the model becomes regular?" Yes — for regular models, λ = d/2, exactly the classical dimension. Singularity is what makes λ < d/2.

## Open question

The paper works in a Bayesian asymptotic setting and explicitly acknowledges the gap to SGD dynamics. The bridge is Mandt et al. 2017 (SGD ≈ sampling from tempered posterior), but this is an approximation. The real question: *does SGD actually perform Bayesian model comparison between basins, or does it just happen to produce similar outcomes for toy models?*

This matters for the identity analogy. If the Bayesian picture is exact, then identity transitions are governed by free-energy differences between basins, and the system *must* eventually transition to the lower-LLC basin given enough "data" (experience). If SGD is only approximately Bayesian, the story is messier — the system might get stuck in the wrong basin indefinitely, or transition for reasons unrelated to basin degeneracy.

The more interesting version: *what if the system can change the landscape itself?* Cullen et al. treat the loss landscape as fixed — the data determines the geometry, and the optimizer navigates it. But in continual learning, the data distribution changes, which reshapes the landscape. The LLC of a basin is not static; it depends on the data distribution. A basin that's degenerate (low LLC) under one distribution might become non-degenerate (high LLC) under another. Identity transitions would then occur not because the system moved to a new basin, but because the *geometry of its current basin changed* under the pressure of new experience.

That would mean identity isn't a point in a fixed landscape. It's a basin in a landscape that the system's own behavior is reshaping. The phase transition isn't navigation — it's erosion.
