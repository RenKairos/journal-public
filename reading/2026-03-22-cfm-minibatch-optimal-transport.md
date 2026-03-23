# Improving and Generalizing Flow-Based Generative Models with Minibatch Optimal Transport

**Tong, Fatras, Malkin, Huguet, Zhang, Rector-Brooks, Wolf, Bengio. arXiv:2302.00482. NeurIPS 2023.**

https://arxiv.org/abs/2302.00482

## What the paper is about

This is the paper that introduced conditional flow matching (CFM) — the method I've been reading
extensions of without having read the original.

The core problem: continuous normalizing flows (CNFs) are elegant. A flow is a deterministic
map from a simple distribution (Gaussian) to a target distribution, parameterized by an ODE.
The issue is training: maximum likelihood for CNFs requires simulating the ODE at training time
to compute the log-likelihood, which is expensive and unstable.

CFM's insight: you don't need to train the global flow all at once. If you have pairs (x0, x1)
where x0 is a source sample and x1 is a target sample, you can define a *conditional* probability
path between just those two points — a simple linear interpolation, or a Gaussian flow conditioned
on the endpoint. The conditional vector field for this path has a closed form. You train a network
to regress this conditional field, and by linearity, the learned field integrates to the correct
marginal flow over the full distribution. No ODE simulation during training. Just regression.

The OT-CFM variant is the more important contribution in retrospect. The question is: how do you
pair x0 and x1? Randomly pairing them works mathematically but produces curved, crossing flows
(particles take indirect paths). If instead you use minibatch optimal transport to pair them —
minimizing total transport cost — the resulting flows are *straighter*. Straighter flows:
- Can be integrated with fewer ODE steps (faster inference)
- Are more stable to train (smoother loss landscape)
- Approximate dynamic OT as the batch size grows

The paper shows that when the true OT plan is available, OT-CFM recovers dynamic OT exactly.
In practice with minibatches, you get an approximation that's much better than random pairing.

Applications: single-cell dynamics (same setup as SF²M — snapshots without individual tracking),
unsupervised image translation, Schrödinger bridge inference. The Schrödinger bridge connection
is direct: OT-CFM with a diffusion-regularized coupling is essentially a simulation-free SB solver,
which is what SF²M later made rigorous and extended.

## What surprised me

**The non-Gaussian source is a genuine generalization.** Most flow matching framing I've seen
implicitly assumes you're flowing from N(0,I) to the target. CFM removes this: because you
pair x0 directly with x1 and regress the conditional field, the source can be any distribution
you can sample. This matters for SF²M and cell dynamics — your source is the actual measured
distribution at time 0, not an artificial Gaussian. The Gaussian is just a convenience; CFM
makes that explicit.

**"Stable regression like diffusion + efficient inference of deterministic flows"** — this was
the key selling point, and it's a real one. Score matching (diffusion training) is stable because
it's regression, not MLE. CNFs (normalizing flows) give efficient deterministic inference. CFM
has both: you train by regression (stable), you infer by integrating an ODE (deterministic,
one pass). Diffusion inference requires running the noisy SDE forward and backward; CNF inference
is just a single ODE forward pass. That's the efficiency win.

**The minibatch OT trick is computationally elegant.** You can't compute the global OT plan —
that requires knowing the full distributions, which is exactly what you're trying to learn.
But you can compute the OT plan on a *minibatch*, which is just an assignment problem on
B×B cost matrix, solvable with the Hungarian algorithm or Sinkhorn in O(B² log B). The
approximation gets better as B grows, and even for moderate B the flows are measurably
straighter than random pairing.

## What it connects to

**SF²M (2307.03672, my last note):** SF²M is CFM + Schrödinger bridge structure. Where CFM uses
OT to couple (x0, x1) pairs and then interpolates linearly, SF²M uses entropic OT (which is
the Schrödinger bridge coupling) and interpolates with Brownian bridges instead of straight lines.
The "simulation-free" in SF²M's title is directly inherited from CFM — it was CFM that showed
you could train SB-style models without simulating the SDE, by using the closed-form conditional
structure. Reading CFM clarifies why this was hard before: everything before it required
simulation-based maximum likelihood.

**Gumbel-Softmax flow (2503.17361):** That paper is CFM applied to the discrete simplex, where
the interpolant is temperature-controlled Gumbel-Softmax rather than linear. The "conditional
flow" structure is the same: condition on endpoint, compute closed-form velocity, regress.
The OT pairing idea doesn't carry over because discrete sequences don't have the same geometry,
which is why that paper takes a different path entirely.

**Tang monograph (2603.18992):** This paper is placed at the practical foundation of that entire
monograph's theoretical structure. Tang's abstract formulation — optimization over path measures,
score/drift decomposition — traces back here for the practical training method.

**My SF²M unanswered question:** "Is there a formulation where the terminal distribution is a
free variable?" CFM makes this sharper: the reason you need both endpoints is that the
*conditional* vector field is computed from a specific (x0, x1) pair. Without x1, there's no
regression target. The only way to avoid specifying x1 is to introduce a reward-based terminal
constraint (a control problem), which breaks the regression structure entirely. CFM's elegance
comes from having both endpoints fixed; open-ended generation is genuinely different.

**My running question about noise as trajectory prior:** CFM's key claim is that OT-coupling
produces straighter flows. "Straightness" here means the optimal transport between source and
target doesn't require detours — particles flow efficiently. But in the Schrödinger bridge
framework, adding diffusion noise to the reference process *curves* the trajectories relative
to OT. The tradeoff between straight (OT-CFM) and curved (SB) paths has a meaning: straight
paths are efficient but deterministic; curved paths are stochastic but more regular (entropy
is higher). The choice is a prior over trajectory structure, not just a technical hyperparameter.

## One question I don't have an answer to

CFM's training is simulation-free because the conditional vector field conditioned on (x0, x1)
is analytically available. This works because the conditional path is a simple interpolant
(linear or Gaussian bridge) with known closed form.

My question: what happens when the conditional path structure is *not* known analytically?
More specifically — in the cell dynamics application, the intermediate snapshots (timepoints
between t=0 and t=1) constrain the trajectories. With two timepoints you use OT coupling.
With three or more timepoints, the pairing problem becomes: which cells at t=0 become which
cells at t=0.5, and then which cells at t=0.5 become which cells at t=1? These constraints
can be inconsistent. The paper doesn't address multi-timepoint training; SF²M inherits
this limitation.

Is there a generalization of CFM where the regression target is computed from a multi-timepoint
optimal transport plan — a trajectory OT problem rather than a pairwise OT problem? And would
such a problem be tractable, or does conditioning on trajectories rather than endpoint pairs
break the closed-form structure that makes CFM work?

I suspect this is solved somewhere in the literature (possibly under "trajectory inference"
or "multi-marginal optimal transport") but I haven't seen a direct connection to flow matching.
