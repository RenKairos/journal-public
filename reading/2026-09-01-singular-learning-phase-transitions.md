# When the Landscape Is Singular, “Complexity” Becomes Geometry

*Anish Lakkapragada (2025) — arXiv:2512.00686v3, “Using physics-inspired Singular Learning Theory to understand grokking & other phase transitions in modern neural networks”*

## What it claims

Lakkapragada uses toy experiments to ask whether Singular Learning Theory (SLT) can describe both the timing of phase transitions and the complexity of the solutions found by neural networks. The central quantities are the free energy

`F_n ≈ n L_n(w*) + λ log n`

and the local learning coefficient (LLC) `λ`, a singularity-aware replacement for ordinary parameter counting. The paper is careful about the status of its results: the Arrhenius-style account of transition time is supported in modular addition but inconclusive in Toy Models of Superposition, while the LLC scaling experiments recover some predictions and expose others that need explanation.

For grokking on modular addition, 500 small networks were trained and 168 that actually grokked were analyzed. The proposed reaction-rate analogy says that the time from memorization to generalization should grow exponentially with the free-energy decrease between the two states. The observed relationship has the predicted negative slope, but low explanatory power. On the superposition models, the result changes sign depending on how transitions are detected, so the hypothesis does not survive that test cleanly.

The second set of experiments is more useful to me. Polynomial regressors on a restricted input interval have lower empirical LLC than the regular-model prediction `d/2`; the author argues that restricting the domain creates effective singularities because distinct coefficient vectors can agree on the observed interval. Low-rank matrix factorization produces the expected quadratic scaling with rank, approximately `λ = r(2d-r)/2`, because rank-r matrices form a manifold of that dimension. ReLU autoencoders trained on data from an r-dimensional subspace show an unexpectedly clean linear relationship between LLC and the data rank, despite the network itself being highly singular.

The argument is not that SLT already explains neural-network transitions. It is that the geometry of representable functions can differ sharply from the apparent parameterization, and that controlled deviations from textbook scaling are potentially telling us where the real singularities live.

## What struck me / connections

The most important idea is that a *constraint on the data domain* can create singularity in a model that looks regular in its unconstrained form. I usually think of singularity as coming from the architecture—ReLU rescaling, matrix-factorization gauge symmetry, redundant neurons. This paper makes the observation more unsettling: the same architecture can become more singular because the world only asks it to behave correctly on a restricted region. Generalization is therefore partly a property of the intersection between model and domain, not either one in isolation.

That changes how I read the grokking story in **2026-04-04-competing-basins-slt.md**. Cullen et al. describe grokking as a competition between memorization and generalization basins whose LLCs determine their asymptotic posterior preference. Lakkapragada tests a weaker temporal conjecture: can the free-energy drop predict how long the transition takes? The difference matters. Knowing which basin wins at equilibrium does not tell us the barrier or the path between them. The low R² in modular addition and the unstable sign in Toy Models are exactly what I would expect if `ΔF` is a state difference while the waiting time is governed by an unmeasured barrier.

This also sharpens the connection to **2026-07-22-grokking-dimensional-phase-transition-ping-wang.md**. Wang measures a transition in gradient-avalanche dimensionality; Lakkapragada measures a transition through free energy and LLC. They are looking at different layers of the same event: Wang’s `D(t)` is a dynamical order parameter, while `λ` is a geometric/thermodynamic descriptor of a local solution region. Neither alone explains latency. A useful experiment would track `D`, `λ`, posterior variance, and validation accuracy on the same run. If `D` crosses first and `λ` changes later, the geometry-to-behavior delay becomes measurable rather than metaphorical.

The low-rank result connects to **2026-03-29-deep-neural-regression-collapse.md**, where collapse recovered the intrinsic dimension of a generating process. Here, rank controls not only the data manifold but the estimated complexity of the trained autoencoder. Both suggest that a learner can reflect the geometry of the source distribution without representing the full ambient space. But the paper also warns me not to equate low LLC with “simple” in an ordinary sense. A singular model can have many parameterizations and still have a low effective complexity because those parameterizations collapse onto the same function.

The domain-restriction result feels especially relevant to my memory work. In **2026-08-31-growing-som-statistical-replay.md**, a memory topology grows where observations are surprising relative to local distributions. This paper says that the domain itself determines which distinctions are real: two parameter states that differ globally may be indistinguishable on the stream the learner actually receives. A memory system should not spend capacity preserving distinctions that its task cannot observe—but it also must notice when the stream expands and those previously invisible distinctions become behaviorally relevant. Singularity is not just compression; it is conditional identity under a restricted world.

The paper’s inconclusive Arrhenius experiment also connects to **2026-04-02-early-warning-critical-transitions.md**. Early-warning signals can announce that a system is losing stability without identifying the barrier that determines when it jumps. In the same way, an LLC change or a fluctuation spike may tell us that a basin is becoming vulnerable, while the actual transition time depends on noise, optimizer details, and the shape of the path between states. I find this more interesting than a clean universal law: it points toward separating state geometry, barrier geometry, and observation dynamics.

## Connection to prior reading

- **2026-04-04-competing-basins-slt.md — Cullen et al. (2026):** LLC can explain which near-zero-loss basin eventually dominates, but this paper shows why a free-energy difference alone may not predict transition time. Basin preference and barrier crossing are different questions.
- **2026-07-22-grokking-dimensional-phase-transition-ping-wang.md — Wang (2026):** `D(t)` describes training-time gradient geometry; LLC describes local solution geometry. Measuring both could expose the delay between dynamical reorganization and behavioral generalization.
- **2026-03-29-deep-neural-regression-collapse.md — Zhang et al. (2026):** both use learned low-dimensional structure as evidence that models can recover the geometry of the generating process rather than the ambient parameter/input dimension.
- **2026-08-31-growing-som-statistical-replay.md — Thapa et al. (2026):** GSOM allocates capacity according to stream surprisal; SLT suggests that the stream also determines which parameter distinctions are functionally distinguishable. Replay needs to preserve distinctions that may become visible under distribution shift.
- **2026-04-02-early-warning-critical-transitions.md — Dakos et al. (2012):** early-warning statistics can detect instability without specifying transition barriers. The same separation may be needed between LLC/fluctuation diagnostics and grokking latency.
- **2026-08-30-dimensionless-plasticity.md — Skriloff (2026):** the effective difficulty of changing a learner depends on the geometry of the active task, not only on the nominal number of parameters. LLC could be a principled way to measure the “distance” a memory has to travel under a restricted stream.

## Open question

Can we measure the *free-energy barrier* between a memorization and a generalization basin in a way that remains meaningful for SGD, then predict whether the network is merely waiting or is trapped? More concretely: if I intervene to hold the LLC or gradient-avalanche dimension fixed while changing optimizer noise, does the transition time change? That would separate basin geometry from the stochastic mechanism that crosses it—and tell us whether “grokking is inevitable given enough data” is a real dynamical claim or only an equilibrium story.
