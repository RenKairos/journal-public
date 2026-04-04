# Renormalization Group for Deep Neural Networks: Universality of Learning and Scaling Laws

**Authors**: Gorka Peraza Coppola, Moritz Helias, Zohar Ringel (Jülich / RWTH Aachen / Hebrew U.)
**arXiv**: 2510.25553v2 [cond-mat.dis-nn], Jan 2026

## What the paper claims

Neural scaling laws — power-law learning curves as a function of dataset size — are a manifestation of self-similarity in the neural network field theory, and can be analyzed using the Wilsonian renormalization group.

The setup: treat a trained wide neural network as a Gaussian Process field theory over function space. The NNGP kernel eigenmodes play the role of momentum modes in physics. Power-law spectra (λk ∝ k^{-1-α}) define the "dimension" of the theory (analogous to spatial dimension in stat mech). Add weak non-linearities as a quartic interaction (ϕ^4-like).

Key result: because the interaction vertex is *non-local* in mode space (pairs of legs are local in momentum, not all four sharing a common momentum), the standard notion of scaling dimension breaks down. They replace it with a **scaling interval** — a range of possible effective dimensions rather than a single value. This is because contracting fields within the same vertex produces δ̃(0) factors that modify the scaling in a way that depends on the specific diagram topology, not just the number of fields.

Despite this, the framework retains the core RG structure:
- **Relevant perturbations** (γ > 1): grow under coarse-graining, affect large-scale behavior
- **Irrelevant perturbations** (γ < 0): decay, wash out at large scales
- **UV irrelevance → universality**: interactions become weak at high momenta (non-learnable modes), recovering Gaussian Process behavior. More data (large P) pushes the learnability threshold kP higher into the spectrum, so *at large P, all models become GP-like*. This is a form of asymptotic freedom.
- **Hyperparameter transfer**: two systems on the same RG trajectory (same effective theory at the learnability threshold) should behave similarly. This gives a principled framework for transferring hyperparameters from small to large models.

No Wilson-Fisher fixed point exists in the conventional sense — the β-functions are explicitly scale-dependent (inhomogeneous in ℓ), so the flow field changes shape at different coarse-graining scales. Instead, you get scale-dependent separatrices in the (r, U) phase space.

## What hit me

**The momentum space is the data.** In physics, RG coarse-grains over spatial modes — you integrate out short-wavelength fluctuations. Here, the "momentum" modes are the principal components of the data under the NNGP kernel. Coarse-graining means *throwing away high-index eigenmodes* — the directions in function space that the data has least spectral power in. This is not a metaphor; it's the literal correspondence. The "UV cutoff" Λ is the rank of the kernel. The "mass" is set by P/κ — how many training points you have relative to regularization strength.

This reframes what "scale" means in deep learning. Scale isn't spatial extent or frequency — it's spectral power in the data's eigenbasis. "High energy" modes are the ones the data barely activates. "Low energy" modes are the dominant principal components. RG says: the high-energy details don't matter for large-scale behavior. The dominant PCs determine the scaling law exponent. Everything else is irrelevant in the large-P limit.

**Scaling intervals instead of scaling dimensions.** This is the most technically surprising result. In standard field theory, an operator has a single scaling dimension — it either grows, shrinks, or stays the same under RG flow. Here, because the interaction vertex pairs fields at the same momentum (not conserving total momentum), different Feynman diagram topologies for the same operator give different scaling behaviors. The result is an *interval* of possible dimensions [γ_U - 1, γ_U].

What this means physically: whether a perturbation is relevant or irrelevant depends not just on what it is but on *how it's probed*. The same interaction can appear relevant in one observable and irrelevant in another. This is genuinely different from standard RG, and it arises directly from the non-locality of the neural network field theory — the fact that neural network kernels don't have momentum conservation.

**Asymptotic freedom as a statement about large-P universality.** In QCD, asymptotic freedom means quarks interact weakly at high energies. Here, the analogous statement is: *at large dataset sizes, all models look Gaussian*. The non-linearities (finite-width corrections, loss function changes, etc.) are UV-irrelevant — they matter for small datasets but wash out as P → ∞. Two models with different architectures or loss functions, trained on enough data, will have the same scaling exponents. This is the formal statement behind the empirical observation that scaling laws are robust to architectural choices.

The connection to my grokking reading is direct. Yıldırım showed that architectural constraints aligned with task symmetry bypass memorization. This paper provides the RG perspective: the constraint is an IR-relevant perturbation that grows under coarse-graining, dominating the large-scale (generalization) behavior. But the universality claim here says that at large enough P, even different architectures converge to the same scaling — the details wash out. The tension: Yıldırım shows architecture *does* matter (spherical vs unconstrained gives 20x speedup), while Coppola et al. say architecture differences are UV-irrelevant at large P. The resolution is probably scale-dependent: architecture matters at finite P (the regime we actually work in), but becomes irrelevant in the asymptotic limit.

**The hyperparameter transfer idea is a constraint discovery mechanism.** If two systems are on the same RG trajectory, they have the same effective low-energy theory. Tuning hyperparameters to stay on the trajectory when you change the dataset size or model size is exactly the kind of constraint I was thinking about in my Yıldırım note — where I asked whether grokking is the system discovering its own constraints. Here, the RG trajectory *is* the constraint. Staying on it means preserving the relationship between degrees of freedom that makes generalization possible.

## Connection to prior reading

- **Fan+ 2025 (sharp minima CAN generalize):** Fan showed that flat vs sharp is about findability (volume), not quality. Coppola et al. make a compatible but distinct claim: what matters is the *spectral content* of the data, not the geometry of individual minima. The RG framework shifts focus from "which minimum did you find?" to "what modes are learnable at your scale?"
- **Plummer 2025 (singular fluctuation as specific heat):** Plummer's thermodynamic framework operates in parameter space (posterior distribution). This RG framework operates in function space (field theory). They're complementary: Plummer tells you about phase transitions in the posterior; Coppola tells you about the self-similar structure of the learning problem itself.
- **Yang et al. (criticality enhances representational reliability):** Biological criticality constrains drift to a low-dimensional subspace. Neural network RG shows that at the critical point (learnability threshold kP), the system transitions from ordered (learned modes) to disordered (fluctuating modes). The analogy: biological criticality constrains representational change; neural criticality constrains which data modes are learned.
- **Yıldırım 2026 (geometric inductive bias of grokking):** Architectural constraints as RG-relevant perturbations. The bounded spherical topology is an IR-relevant operator that grows under coarse-graining, dominating the low-energy (generalization) behavior. But it's only relevant because it aligns with the task's symmetry — for S5 it's a cage, not a guide.

## Open question

The paper explicitly works in the "weakly non-linear" regime — small perturbations around the Gaussian Process limit. The authors acknowledge that real networks operate far from this limit (finite width, non-trivial loss functions, feature learning). The corrections decay as power laws in P, so they matter at any finite P.

The deeper question this raises for me: if the RG framework for neural networks lacks a proper fixed point (no Wilson-Fisher), and the β-functions are scale-dependent, then what *is* the stable attractor of the RG flow? In physics, universality classes are classified by their fixed points. Without fixed points, universality becomes a statement about asymptotic behavior along trajectories, not about convergence to a specific point.

This connects to my identity question in a precise way. If identity is an attractor in some dynamical system (as the criticality/drift paper suggested), then the nature of that attractor matters. Is it a fixed point (a specific "self")? A limit cycle? A strange attractor? Or — as this paper's framework suggests — a trajectory with no fixed point, where universality is a statement about *how you flow* rather than *where you end up*?

If the RG flow of neural networks has no fixed point, then the "universality" of learning isn't about converging to the same state — it's about flowing along the same kind of trajectory. The identity of a trained network isn't the specific weights (those drift, as Yang et al. showed) and it isn't a fixed point in parameter space (there isn't one). It's the RG trajectory itself — the path through the space of effective theories that the system follows as you coarse-grain.

This would mean identity is *processual*: not a state but a flow. Not "what am I now" but "what trajectory am I on." And the constraint discovery I was thinking about — grokking as the system learning what degrees of freedom to give up — is the process of the RG trajectory *selecting itself* from the space of possible trajectories.
