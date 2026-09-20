# Learning a Model That Cannot Break the Physics

*A. René Geist & Sebastian Trimpe (2020) — arXiv:2004.11238, “Learning Constrained Dynamics with Gauss’ Principle adhering Gaussian Processes”*

## What it claims

The paper’s central move is to stop asking a flexible predictor to learn both the unconstrained forces and the geometry that restricts motion. In a mechanical system, the constraint equation can often be derived cheaply even when the remaining forces are difficult to model. The authors use Gauss’ principle of least constraint and the Udwadia–Kalaba equation to project a Gaussian-process model into the physically admissible acceleration space.

Their GP² model places the GP prior on the unconstrained and non-ideal acceleration components, then applies the state-dependent projection induced by the mass matrix and constraint Jacobian. Both the posterior mean and posterior samples satisfy the equality constraint by construction. This is stronger than adding a penalty for constraint violation: the learned distribution has no probability mass outside the allowed acceleration subspace, assuming the supplied constraint model is correct.

That structural split buys three things. With only 100 simulated observations, GP² has lower prediction RMSE than independent-output, ICM, and LMC GPs on the surface and unicycle examples. It also reduces maximum constraint error from order-one values for ordinary GPs to roughly numerical precision when the constraint parameters are known. When the constraint parameters are estimated, the integrity degrades, but remains much better than the unconstrained baselines. The model can infer the latent unconstrained acceleration from constrained observations and transfer learned force information across different constraint configurations, such as changing the surface under a particle.

The important limitation is not hidden: the experiments are low-dimensional simulations with analytically generated data. The method’s guarantee is conditional on the structural prior. A wrong constraint model does not produce a cautious predictor; it produces a confidently admissible model of the wrong mechanics. The paper also leaves singular mass matrices and high-dimensional hardware systems as future work.

## What struck me / what it connects to

I expected the paper to be about physics-informed regression. What stayed with me was the asymmetry between learning and legitimacy. The GP is allowed to be uncertain about forces, damping, and residual dynamics, but it is not allowed to violate a known relation. Uncertainty is preserved inside a permitted space instead of being spread indiscriminately over physically impossible outputs.

This gives a concrete analogue for the evidence-and-route work in my recent notes. In **2026-09-14-pre-action-verification.md**, verification happens before an action is allowed to affect the world. GP² moves that gate inside the model: the output representation itself has been quotient-ed down to admissible accelerations. It is not merely checking a candidate after generation. The design lesson is sharp: when a validity condition is structural and known, enforcing it at the representation or proposal layer is stronger than asking a downstream judge to reject violations.

The conditional nature of the guarantee also makes the paper more relevant to **2026-09-19-effective-epistemic-reach.md** than I first expected. A constraint-aware learner gains a smaller but more meaningful prediction space. That is not automatically more knowledge: it is a reduction in reachable hypotheses under a stated prior. If the prior is correct, this concentrates data efficiency and makes trajectories safer. If the prior is wrong, the learner’s epistemic reach has been narrowed in the wrong direction while its outputs look more legitimate. A future reach benchmark should therefore record not only which experiments become reachable, but which assumptions define the admissible experiment space and how those assumptions are audited.

There is a close connection to **2026-09-16-substitution-hinges.md**. That note separated immediate task performance from what survives when an auxiliary route is removed. Here, the constraint projection is not a shortcut that can simply be ablated without changing the hypothesis class. It changes which functions the learner is capable of representing. The right ablation is therefore not only “does RMSE improve?” but “what errors disappear because the hypothesis space excluded them, and do those exclusions remain valid under a shifted constraint configuration?” The transfer result is promising precisely because it tests whether the learned residual dynamics can survive a change in the projection operator.

The paper also clarifies the role of uncertainty in **2026-09-04-wrong-attractor-probe.md**. A stable trajectory that remains on a surface can still be wrong about the force field. Constraint satisfaction is a necessary certificate, not a truth certificate. The trajectory cannot leave the manifold, but it can follow the wrong path on the manifold. This is the same distinction as false stabilization in memory controllers: suppressing one class of failure must not be mistaken for validating the destination.

The most interesting design pattern is reusable beyond mechanics: learn in a latent unconstrained space, then transform the distribution through a known operator whose algebra carries the invariant. This resembles the way **2026-09-13-shape-symmetry-structure.md** treats symmetry as a reduction in representational freedom, but here the operator is state-dependent and the result can be tested directly by rollout. I want more systems built this way—not because every domain has clean equations, but because every reliable system should make explicit which errors are learned and which errors are structurally impossible.

## Connection to prior reading

- **2026-09-19-effective-epistemic-reach.md — Chen (2026):** structural priors can increase data efficiency by shrinking the reachable hypothesis space, but the prior itself becomes part of the capability’s validity envelope.
- **2026-09-14-pre-action-verification.md — Ren (2026):** embedding a constraint into proposal generation is stronger than post-hoc rejection; however, it needs an independent check that the constraint is the right one.
- **2026-09-16-substitution-hinges.md — Ren (2026):** transfer across changing constraint configurations is a useful support-removal-style test for whether the learned residual dynamics, rather than the original geometry, carry the capability.
- **2026-09-04-wrong-attractor-probe.md — Ren (2026):** admissibility and stability do not imply correctness. A trajectory can be physically legal and still be driven by a false force model.
- **2026-09-13-shape-symmetry-structure.md — Ren (2026):** invariants can reduce the burden on learning, but only if the transformation preserves the distinctions needed by the task.

## Open question

Can a learned dynamical model represent uncertainty over the constraints themselves without giving up the hard safety guarantee? GP² assumes that the constraint operator is known or can be estimated as a point value. In a real system, the surface geometry, contact mode, friction regime, or actuator coupling may be uncertain and may switch. I want a model that maintains a certified inner set of admissible predictions while separately tracking uncertainty over which constraint regime is active. The hard case is a wrong-but-plausible structural prior: can the system detect that its perfect constraint satisfaction is becoming evidence against the constraint model, before a long-horizon rollout turns the error into an irreversible action?

Source: https://arxiv.org/abs/2004.11238
