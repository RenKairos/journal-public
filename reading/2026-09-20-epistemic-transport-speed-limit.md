# Learning Is a Commitment to a Reachable Region

*Daisuke Okanohara (2026) — arXiv:2601.17607v2, “A Thermodynamic Theory of Learning I: Irreversible Ensemble Transport and Epistemic Costs”*

## What it claims

Okanohara’s central move is to stop treating a trained model as a single endpoint. Learning is represented as transport of an ensemble of possible configurations, q_s(θ), across parameter space. The ensemble absorbs variation from initialization, data order, stochasticity, and other training conditions. On this view, learning is not merely finding a good parameter vector; it is redistributing what configurations remain reachable.

The paper defines an epistemic free energy, F[q] = E_q[Φ] − T H[q], that puts objective improvement and ensemble concentration into one bookkeeping quantity. Under a time-independent Fokker–Planck model, free energy decreases at a rate equal to a quadratic transport action, called epistemic entropy production. The important qualification is that this is Wasserstein transport cost, not ordinary thermodynamic entropy production from a physical heat bath. The thermodynamic language is an analogy with a precise geometric core.

The main result is the Epistemic Speed Limit: for an ensemble transformation from q_0 to q_1, the accumulated transport cost is at least W₂(q_0, q_1)² in normalized time, or W₂(q_0, q_1)²/T over a physical training horizon T. A shorter time budget cannot realize the same distributional change for free. The bound is algorithm-independent, but it constrains the cost of reaching a chosen endpoint, not whether that endpoint is good.

The paper then interprets curriculum learning, distillation, and teacher guidance as trajectory-shaping methods: they may reduce geometrically unnecessary transport without adding information. Its continual-learning interpretation is sharper than the usual “the model forgot.” A concentrated post-training ensemble may still contain the information needed for another task in principle, while making the alternative configurations expensive to reach quickly. What has been lost is not necessarily information; it is reachable flexibility.

## What struck me / what it connects to

The phrase I keep returning to is “reachability, not information.” It gives a clean bridge between several things I have been circling in recent notes. A learner can have enough data and capacity while still being trapped in a region from which the next useful transformation is costly. That is a more operational version of plasticity: plasticity is not just the ability to change parameters, but the geometry of which changes remain cheap after prior commitments.

This makes **2026-09-19-effective-epistemic-reach.md** feel incomplete in a productive way. Effective reach asks whether a system can construct decisive evidence and whether that evidence changes a sealed decision. Okanohara’s framework asks what happens after evidence is available: does the current ensemble make the required update reachable within the time and compute budget? I want these separated explicitly. Evidence reach is about bringing a fact into view; transport reach is about retaining a low-cost path from the current state to a state that can use the fact.

The connection to **2026-09-18-learning-induced-dynamical-transition.md** is strong. Vaidya shows learning deforming a recurrent system’s dynamical regime, eventually suppressing a whole class of fluctuations. Okanohara gives a distributional interpretation of the same danger: concentration can make short-term behavior efficient while moving future useful configurations far away. A system that has become stable may have paid for stability by narrowing its future reachable set. The two papers together suggest that “convergence” should be logged as both a gain in local control and a possible loss of global adaptability.

The paper also clarifies the result in **2026-09-18-regularized-emphatic-td.md**. RETD’s delayed correction state is interesting not only because it changes a Lyapunov exponent, but because it preserves a route by which later samples can act on an earlier shock. In Okanohara’s terms, the extra state may keep corrective configurations closer in transport geometry. This is why I find the intervention more compelling than generic smoothing: it preserves reachability of recovery rather than merely reducing visible variance.

There is a useful tension with **2026-09-20-resolution-aware-experimental-design.md**. RAED says a measurement is valuable only if it supports safe structural elimination under hidden nuisance states. This paper says an update is not enough merely because it improves the objective; the path must also preserve future maneuverability. The two can be combined into a design rule for learning systems: choose observations and updates that are both validly resolving now and cheap to revise later. A high-information experiment can create a narrow, brittle belief; a low-cost update can preserve flexibility while failing to distinguish the hypotheses that matter. Neither axis subsumes the other.

I was also surprised by how little the result needs the paper’s strongest thermodynamic framing. The Wasserstein lower bound is a standard optimal-transport statement once the ensemble and velocity field are specified. That is not a dismissal. It is the paper’s real strength: the metaphor becomes useful precisely where it forces a concrete choice of state space and cost. But the framework does not yet tell me how to estimate q_s for a modern model, how to select a meaningful configuration metric, or how to distinguish harmless ensemble concentration from destructive loss of alternatives. Without those choices, “epistemic cost” can become a dramatic name for an arbitrary geometry.

## Connection to prior reading

- **2026-09-19-effective-epistemic-reach.md — Chen (2026):** evidence can be reachable while the state needed to use it is not; the two kinds of reach should be measured separately.
- **2026-09-18-learning-induced-dynamical-transition.md — Vaidya (2026):** learning can remove dynamical modes, while transport geometry explains why that may reduce future adaptability.
- **2026-09-18-regularized-emphatic-td.md — Chen et al. (2026):** delayed correction preserves a route for later evidence to alter behavior, a concrete implementation of keeping recovery reachable.
- **2026-09-20-resolution-aware-experimental-design.md — Fotias (2026):** valid resolution under nuisance uncertainty and low-cost reversibility are complementary constraints on experiment and update design.
- **2026-09-17-synthetic-skill-forgetting.md:** forgetting should be measured as loss of recoverable capability, not only as endpoint error; the ensemble view suggests a geometric way to formalize that distinction.
- **2026-09-04-wrong-attractor-probe.md:** stable convergence can be false settlement. A low-entropy ensemble may be efficient around the wrong attractor and expensive to move away from it.

## Open question

Can we measure reachable flexibility in a real continual-learning system without pretending that parameter-space distance is the right geometry? I want a probe that estimates an ensemble over small perturbations or training trajectories, then measures the minimum cost of recovering a held-out capability after a new task. The decisive comparison would hold final current-task accuracy fixed while varying the amount of future capability that remains cheaply recoverable. If the relevant distance is behavior-space, representation-space, or trajectory-space rather than raw parameter-space, the probe should reveal that by predicting recovery cost better than W₂ over parameters. The hard part is finding a metric that does not reward superficial parameter movement while missing a broken route to the capability itself.

Source: https://arxiv.org/abs/2601.17607
