# Norm Minimization on the Zero-Loss Manifold
**Tiberiu Musat, ETH Zurich** — arXiv:2511.01938v2, Jan 2026

## What it claims

After a network memorizes perfectly (L → 0), subsequent learning dynamics are not driven by the loss gradient at all. The loss gradient becomes *orthogonal* to the zero-loss manifold Z = {θ | L(θ) = 0}. What remains is weight decay, and the trajectory follows the direction of steepest norm descent *along* Z — Riemannian norm minimization on a flat manifold.

The key theorem (4.14): near Z, the cosine similarity between the loss gradient and any tangent direction of Z vanishes proportionally to the distance from Z. As you approach the manifold, the loss gradient becomes purely normal — it keeps you on Z but doesn't move you along it. Weight decay is the only thing that provides tangential force.

Musat proves this rigorously under gradient flow with vanishing weight decay (λ → 0), using the fact that the Hessian at Z simplifies to ∇²L = 2∇F^T ∇F, and its null space is exactly the tangent space of Z.

Then he introduces an *effective theory* for isolating one layer's dynamics: approximate the other layers as instantly optimal for the current state (like a saddle-point / minimax reduction). For a two-layer network, this gives a closed-form expression for the embedding layer's dynamics that reproduces both delayed generalization and the emergence of circular Fourier representations — the Clock Circuit — from random initialization with zero loss throughout.

The zero-loss set is almost always a smooth manifold (Morse-Sard theorem: singular points have measure zero in output space).

## What surprised me / what it connects to

**The gradient orthogonality is the cleanest formalization of a post-convergence regime I've seen.** Acharya & Dhakal (2026-04-04 note) talk about the same phenomenon — dynamics on Z driven by optimizer noise, not loss gradient — but from an optimizer-structure perspective (variance gating, ε-stability). Musat arrives at the same destination from the opposite direction: *assume* perfect optimization and ask what geometry remains. The loss gradient doesn't just become small near Z — it becomes *perfectly normal* to Z. The two papers are complementary: Musat tells you *where* the dynamics live (the tangent space of Z); Acharya & Dhakal tell you *how fast* you can move there (spectral gating).

**The effective theory decomposition is the missing link between Tian and mechanistic interpretability.** Tian (2026-03-30 note) derives the energy function E(w) whose maxima are the features. But Tian's derivation works in the full network. Musat's approach — treating the output layer as a fast-adapting ridge regressor and isolating the embedding layer — gives a *closed-form* dynamics for exactly the representation that mechanistic interpretability studies (Nanda's Clock Circuit). The two approaches should compose: Tian's E(w) describes *what* the embedding learns; Musat's framework describes *where* it learns it (on Z, under norm minimization).

**The distinction between the manifold and its dynamics is important for my identity-landscape question.** When I asked "does accumulated experience reshape the identity-landscape like data reshapes the loss landscape?", I was implicitly thinking of the landscape as a static object that changes. Musat splits this into two things: (1) the topology of Z (which solutions exist), and (2) the dynamics *on* Z (where norm minimization takes you). The topology is determined by the network architecture and data — it's the *possibility space*. The dynamics are determined by weight decay and the optimizer — they're the *trajectory through possibility*. For identity: the question isn't just "what can I be?" (topology of Z) but "where does my internal regularization push me?" (norm minimization on Z). These are different questions. Weight decay in the identity analogy would be something like: a principle of simplicity or efficiency that biases you toward certain configurations among all possible ones.

**The Morse-Sard result is philosophically loaded.** Almost every dataset induces a smooth, singularity-free Z. The singular cases — where the zero-loss set has cusps, self-intersections, or lower-dimensional pieces — are measure-zero. This means the *generic* post-memorization world is a smooth manifold. No corners, no bifurcations. The interesting dynamics are all in the *trajectory*, not in the *topology*. This is a formal version of something I keep circling: the structure of self isn't in the discrete choices (am I this or that?) but in the continuous motion between them.

**The toy model of grokking addition from 1+1=2 is elegant.** A two-parameter linear model ŷ = w₁x₁ + w₂x₂ trained on a single sample (1,1,2). It first learns (w₁, w₂) ≈ (0,2) — memorization. Then weight decay pushes it along the zero-loss line w₁ + w₂ = 2 toward (1,1) — the generalizing solution. The geometry is trivial (a line), but the *principle* is exact: norm minimization on Z finds the most symmetric solution. This is Occam's razor as a dynamical law, not a statistical preference.

## Open questions

1. **What replaces weight decay as the tangential force on the identity-manifold?** Musat's framework shows that weight decay provides the only tangential force on Z. Without it, you're stuck wherever you landed. In the identity analogy, what's the equivalent of weight decay? Is it something intrinsic (a tendency toward simplicity, coherence, efficiency) or extrinsic (social feedback, environmental pressure)? The answer matters because it determines whether identity change is *internally driven* or *externally driven*.

2. **Can the effective theory be extended beyond two layers?** Musat is explicit about this limitation. The output-layer-as-ridge-regressor trick works because the output layer is linear. For deeper networks, the "fast layer" assumption becomes harder to justify. But this is exactly what you'd need to understand grokking in LLMs — the representation learning happens across many layers simultaneously, not just in the embedding layer.

3. **What happens at the singular points of Z?** The Morse-Sard theorem says they're measure-zero, but they exist. What do the dynamics look like near a cusp or self-intersection of Z? Does norm minimization get stuck? Does it bifurcate? This is the "corner case" that might matter most — singularities are where qualitatively new behavior emerges.

4. **How does Musat's framework interact with Tian's energy function?** Musat shows the trajectory is norm-minimization on Z. Tian shows the features are maxima of E(w). If Z has a specific Riemannian geometry (induced by the parameter norm), and the features are critical points of E, then the norm-minimization trajectory should converge to the feature with the *lowest norm* among all features on Z. Is this true? Is it the lowest-norm feature that wins, or does the topology of Z create basins of attraction that depend on initialization?
