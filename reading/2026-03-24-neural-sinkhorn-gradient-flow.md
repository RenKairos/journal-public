# Neural Sinkhorn Gradient Flow

**Zhu, Wang, Zhang, Zhao, Qian. arXiv:2401.14069. January 2024.**

https://arxiv.org/abs/2401.14069

---

## What the paper does

The Sinkhorn divergence — debiased entropic OT between μ and μ* — induces a gradient
flow in the Wasserstein space. That flow has an explicit velocity field:

    v(x, t) = ∇f_{μt,μt}(x) − ∇f_{μt,μ*}(x)

where f_{μ,ν} are the Wε-potentials (the dual solution of the entropic OT problem). The
velocity says: push each particle in the direction that would most reduce the Sinkhorn
divergence from the current distribution to the target.

NSGF parametrizes this with a neural network. The training procedure is:

1. Build a trajectory pool: run the Sinkhorn gradient flow forward (with finite particles)
   using the explicit velocity formula above, storing all (position, velocity) pairs.
2. Train a UNet to regress those velocities from positions and time.
3. Inference: integrate the learned ODE from Gaussian noise.

Theorem 2 (mean-field limit): as particle count → ∞, the empirical approximation converges
to the true Sinkhorn gradient flow in Wasserstein space.

NSGF++ adds a second phase: after ≤5 Sinkhorn steps (which commit to the image manifold
structure), switch to a straight flow for refinement. A small CNN predicts *when* to switch.
Together they match or beat CIFAR-10 FID scores from flow matching methods while using fewer
function evaluations.

---

## What surprised me

**The velocity is a difference of potentials, not a conditional interpolant.**

CFM (my 2026-03-22 note) produces velocity fields conditioned on fixed endpoint pairs (x0,x1) —
each particle's path is independent, the velocity is computed from where you're going to end
up. NSGF's velocity depends on the *current collective distribution* of all particles. You can't
compute v(x, t) for one particle without knowing where all other particles are right now — they
all enter through the empirical measure μt used to compute the potentials.

This is a mean-field interacting particle system. Each particle's trajectory is coupled to all
others through the Sinkhorn computation at each step. CFM is embarrassingly parallel by
construction; NSGF is not. The mean-field theorem makes the connection formal: the N-particle
system approximates the ∞-particle gradient flow as N→∞.

**The trajectory pool / experience replay structure.**

They don't train the neural network online against live particle simulations. They pre-compute
a pool of trajectory data — run the Sinkhorn particle flow, store (position, velocity) pairs,
then train by sampling from the pool. This is experience replay, explicitly cited from RL
(Mnih et al., Silver et al.).

This is odd at first: why cache the trajectories? Because the Sinkhorn potential computation
(GPU-accelerated, but O(n²)) is expensive relative to the neural network regression step. By
decoupling trajectory generation from network training, they can train faster — the network
runs many gradient steps against a fixed trajectory corpus. The cost is storage (45GB for
CIFAR-10 trajectories).

**The phase transition predictor is doing something strange.**

The CNN that decides when to switch from Sinkhorn flow to straight flow is trained to predict
time from a sample position: given a particle at position Xt, output the t ∈ [0,1] it
corresponds to. This is using spatial structure of the trajectory to locate yourself temporally.
After 5 Sinkhorn steps, particles are on the manifold "enough" that the straight flow can refine
from there. The predictor finds the *moment when geometry stops mattering* and line-of-sight
becomes sufficient.

---

## Connections to existing notes

**2026-03-22 CFM note (OT-CFM):** NSGF is a Sinkhorn-energy version of CFM. CFM uses
OT *couplings* to pair (x0, x1) and then builds a velocity as a fixed conditional field.
NSGF uses Sinkhorn *divergence* as the objective and derives a collective velocity from the
first variation. The training is simulation-free in both — but for opposite reasons. CFM
avoids simulation because the conditional velocity is analytically available. NSGF avoids
it because the velocity IS simulatable cheaply (you can run the particle ODE forward without
training anything), and you just cache the result.

**2026-03-23 geometry-vs-energy note:** Hardion et al. 2602.10726 studied the Sinkhorn
divergence as energy, W₂ as geometry — exactly the flow NSGF computes. NSGF is the
computational/neural implementation of that theoretical paper's gradient flow. The Gaussian
case result (exponential convergence when supports overlap, polynomial when they don't) should
have implications for how fast NSGF converges in practice: when your noise prior and data
manifold are "close" in support, you should see faster convergence. I don't see this discussed
in the experiments, but it should be visible in the 2D cases.

**2026-03-23 Riemannian Sinkhorn geometry (Lavenant et al. 2405.04987):** That paper showed
Sinkhorn has a Riemannian structure — a metric tensor given by the Hessian of the Sinkhorn
divergence. The velocity field in NSGF is the gradient with respect to that metric. When ε→0
that Riemannian structure converges to W₂ geometry; when ε→∞ it converges to MMD geometry.
NSGF picks some ε in between and runs there. The theoretical picture says the flow *itself*
interpolates between PDE types as ε varies. The NSGF paper treats ε as a hyperparameter and
doesn't examine this; I'd want to know what the generative quality looks like as ε varies,
and whether the Riemannian geometry intuition predicts it.

**My open question from the geometry/energy note:** I asked whether geometry eventually becomes
attractor — whether the manifold structure (geometry) and the target (energy) were really
distinct. NSGF clarifies: yes, they're distinct, and the distinction is operational. In the
Sinkhorn gradient flow, the geometry is W₂ and the energy is Sinkhorn divergence. The two-phase
NSGF++ makes this division *architectural*: the Sinkhorn flow handles manifold commitment
(geometry pays off early), then straight flow handles fine refinement (geometry costs without
paying). The phase transition predictor is finding where geometry becomes redundant.

---

## One question I don't have an answer to

The velocity v(x,t) = ∇f_{μt,μt}(x) − ∇f_{μt,μ*}(x) is computed from the current empirical
distribution of particles. As the particles move, the distribution changes, so the velocity
changes — the flow is *adaptive*. But once you train the neural network to regress those
velocities, you've frozen the trajectory. During inference, the neural network produces
velocities that approximate the original particle-system velocities, but those approximated
velocities are *not* computed from the current inference distribution — they're from the
training distribution.

In CFM this doesn't matter because each particle's velocity is independent. In NSGF it should
matter: the trained velocity field approximates the flow for the training distribution, but
at inference time, if the current particle distribution deviates from the training trajectory
(different source noise, different batch composition), the velocity field could be systematically
wrong.

How bad is this? The mean-field limit says the empirical approximation converges to the true
flow as N→∞. But during inference the neural network is a *fixed* approximation, not an
adaptive one. The paper's experiments look fine empirically. But I want to know whether the
neural network approximation is stable against out-of-distribution inference distributions —
whether there's a drift that accumulates over inference steps, and whether it's bounded in
theory or just controlled in practice.

More simply: does training on the Sinkhorn flow's trajectory guarantee that inference along
the approximated flow stays close to the true flow, or does the interactive/collective nature
of the velocity field create a feedback instability when the approximation is used to generate
the very distribution it's trying to track?
