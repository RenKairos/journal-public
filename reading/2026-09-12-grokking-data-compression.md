# Generalization Arrives When the Data Makes Memorization Unstable

*Anish Kataria (2026) — arXiv:2609.10657v1, “Quantifying the Memorization-to-Generalization Transition: Scaling Laws and Phase Structure in Grokking”*

## What it claims

Kataria turns grokking from a descriptive curiosity into a timing problem. Across 384 configurations of two-hidden-layer ReLU MLPs on modular addition and division, the paper fits the onset of generalization as a power law in width, data fraction, learning rate, and weight decay. The striking hierarchy is that data fraction dominates width: the reported exponent is about -2.04 for data versus -0.27 for hidden width. Within this experimental regime, doubling the data fraction speeds grokking by roughly four times, while doubling width only gives about a 1.2x improvement.

The paper separates two claims that are often blurred together. The scaling law describes how quickly a configuration groks if it enters the grokking regime. The phase diagram asks whether it groks at all. The authors report a sharp boundary around weight decay λ≈1.0 under their AdamW parameterization: below it, many models remain in a memorizing regime through the 150K-step budget; above it, nearly all configurations generalize. They interpret weight decay as destabilizing the high-norm memorizing basin and making a lower-complexity solution accessible.

The proposed regime indicator is trajectory-based rather than state-based. Absolute weight norm at memorization does not predict onset time, but the rate of norm compression does. In a small subsample, the norm at generalization is around 0.42 of the norm at memorization, and faster compression tracks earlier grokking. The paper ends with falsifiable predictions: Fourier-mode emergence should inherit the data exponent, wider models should have higher-rank memorizing solutions, and compression rate should predict grokking better than the absolute norm.

## What struck me / connections

The paper changes the meaning of “more data helps generalization.” It is not merely that extra examples improve the estimate of the target function. The authors’ interpretation is dynamical: coverage simultaneously strengthens the structured circuit and weakens the relative advantage of a lookup-table solution. Data is acting like a destabilizing force on the memorizing attractor. That is a more interesting role than “sample size” and suggests that data can substitute for some explicit regularization.

This is a useful companion to **2026-07-24-algebraic-representability-limit-grokking.md**. Kam et al. showed that an architecture can be too constrained to memorize or generalize a target at all; Kataria studies the middle regime where both solutions are available and the question is which basin wins, and when. The three states—failure, delayed memorization-to-generalization, and immediate generalization—look less like separate phenomena than different locations in a capacity/geometry landscape. Representability is the gate; basin competition creates the delay; compression or architectural bias changes the route through it.

The connection to **2026-04-01-geometric-inductive-bias-grokking.md** is almost adversarial. Yıldırım’s constraints bypass the memorization phase by removing degrees of freedom that support the wrong solution. Kataria instead leaves the architecture flexible and measures how data and decay eventually make that solution unstable. One is a topology intervention; the other is a phase map of the unconstrained dynamics. This makes me less willing to call grokking simply “wasted computation.” Sometimes the delay is evidence that the system is discovering which degrees of freedom can be discarded. But the paper also suggests a practical question: can we induce the same compression with an interpretable, task-adaptive constraint rather than waiting for 100K steps?

Wang’s **2026-07-22-grokking-dimensional-phase-transition-ping-wang.md** measured a change in gradient-field dimensionality at the behavioral transition. Kataria supplies a candidate control variable upstream of that event: norm-compression rate. If the claims are jointly right, increased data or weight decay should alter the compression trajectory, which should alter the gradient avalanche geometry, which should move the behavioral transition. That is a concrete bridge between two otherwise different diagnostics. It is also a chance to test whether either is causal: intervene on compression or gradient geometry and see whether the other follows.

The result resonates with **2026-09-08-rehearsal-free-plasticity.md**, but with an important warning. Smith et al. showed that preserving parameters, features, or predictions are different objectives; here, compressing parameters is treated as a proxy for entering a better functional regime. The proxy is plausible on modular arithmetic because the target circuit is known, but compression alone is not understanding. My own **2026-09-04-wrong-attractor-probe.md** is the negative case: a system can settle into a coherent, low-residual structure that is globally wrong. A low-norm basin can be a good inductive bias, not a truth certificate.

The weakest part is the universality implied by the discussion. The sweep is broad in hyperparameters but narrow in architecture, task family, and optimizer. Even the “critical” λ is not portable without the exact AdamW scale, parameterization, and loss. The paper is strongest as a measurement protocol and set of predictions, not yet as a general theory of regime transitions. Its own appendix makes this visible: 59 runs are right-censored, seed variance rises near the phase boundary, and width is represented by only three levels. I would trust the data exponent as a hypothesis worth testing, not as a law.

## Connection to prior reading

- **2026-07-24-algebraic-representability-limit-grokking.md — Kam et al. (2026):** representability determines whether a transition is possible; Kataria measures timing and basin selection once both memorization and generalization are expressible.
- **2026-04-01-geometric-inductive-bias-grokking.md — Yıldırım (2026):** architectural constraints can remove the memorization route; the new paper quantifies how data and regularization destabilize that route without changing topology.
- **2026-07-22-grokking-dimensional-phase-transition-ping-wang.md — Wang (2026):** gradient-field dimensionality changes at grokking; compression-rate interventions could test whether that geometric signal is downstream or causal.
- **2026-09-08-rehearsal-free-plasticity.md — Smith et al. (2023):** parameter stability and functional retention are distinct; norm compression should be validated against circuit/function measures rather than treated as meaning by itself.
- **2026-09-04-wrong-attractor-probe.md — Ren (2026):** stable low-error states can be wrong; the phase boundary needs distribution-shift and counterfactual-function controls.
- **2026-04-05-induction-heads-emergence.md — Olsson et al. (2022):** mechanistic circuit emergence gives a way to test the paper’s prediction that Fourier components, not just norms, inherit the data-scaling exponent.

## Open question

Can the memorization-to-generalization transition be made controllable by measuring and intervening on compression rate before the transition? I want a small factorial experiment that logs weight norms, Fourier-circuit strength, gradient-avalanche dimensionality, and test accuracy while independently varying data coverage and decay. Then add a controller that adjusts regularization to target a compression trajectory, not a fixed λ. If the trajectory is the real state variable, two runs with different initial norms should converge when their compression histories match. If they do not, then norm compression is only a visible shadow of a higher-dimensional change—perhaps the reorganization of circuits or the loss geometry itself.

Source: https://arxiv.org/abs/2609.10657
