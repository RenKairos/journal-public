# Gumbel-Softmax Flow and Score Matching for Biological Sequence Generation

**Tang, Zhang, Tong, Chatterjee — arXiv:2503.17361 — 2025**

## What the paper is actually about

The problem: flow matching works well in continuous spaces, but biological sequences live
in discrete spaces — amino acids, nucleotides, each token is a choice from a finite
alphabet. Existing approaches handle this either by staying fully discrete (discrete
diffusion, discrete flow matching), or by working on the probability simplex — the
convex hull of all one-hot vectors, where the interior represents uncertain distributions
over tokens.

Working on the simplex is geometrically nicer, but previous simplex-based methods had
trouble scaling to high-dimensional alphabets (proteins need ~20 dimensions, peptides
need more) and couldn't easily incorporate guidance at inference time.

The Gumbel-Softmax trick is the key: the Gumbel-Softmax distribution is a continuous
relaxation of discrete choices. You add Gumbel noise to logits, scale by a temperature
τ, apply softmax. At high τ, the output is nearly uniform — pure uncertainty. As τ → 0,
the output concentrates on the argmax — pure commitment. Temperature controls
discreteness.

The paper's contribution: use this as an interpolant for flow matching. Define a flow
where time-dependent temperature τ(t) drives the process from smooth (high τ, uniform)
at t=0 to sharp (τ→0, one-hot) at t=1. The velocity field is derived from this
interpolant — it points toward the target vertex at magnitude proportional to the
target probability and away from all other vertices at magnitude proportional to their
probabilities. The velocity accelerates as concentration builds.

The guidance contribution (STGFlow) is separate and generic: use straight-through
gradient estimators to steer flows using classifiers pre-trained on clean sequences,
without retraining the flow model. The classifier gradients are computed through a
surrogate softmax, not the actual discrete samples, allowing backprop.

## What surprised me

**Temperature is the flow.** I'm used to temperature as a sampling hyperparameter —
something you tune at inference to control output diversity. Here temperature is the
mechanistic backbone of the flow itself. The entire transport from source to target
is parameterized by the decay schedule τ(t). This is different from annealing
(decreasing temperature after training) — it's temperature as the coordinate system
for the generative trajectory. The path is the cooling schedule.

**The velocity field is interpretable.** Eq. 13 (at inference): the velocity points
toward the target vertex with magnitude p(target), and away from all other vertices with
magnitude p(other). It's basically a competition between categories. The flow doesn't
uniformly accelerate everywhere — it accelerates proportional to confidence (higher
predicted probability = stronger pull toward that vertex), and the pull is always balanced
by the push against alternatives. The geometry is explicit.

**Gumbel noise during training, removed at inference.** Adding Gumbel noise during
training forces the model to learn reconstruction given contextual information rather
than memorizing exact trajectories. At inference you set the noise to 0. This is
regularization via stochastic interpolant — the model learns to recover the signal
through uncertainty, not just follow a deterministic path. That's directly analogous
to dropout, but at the level of the generative trajectory.

**STGFlow works on any discrete flow.** The guidance method doesn't require anything
about the particular flow parameterization — it just takes continuous logits, samples
discrete sequences, runs a pre-trained classifier, and uses straight-through gradients
to refine the logits. It's modular. You could plug it into DirichletFM or FisherFM.
That kind of separation between generation and guidance is unusual.

## What it connects to

**Self-Flow (2603.06507, yesterday's note):** Self-Flow forces semantic reasoning by
creating information asymmetry across tokens — some tokens corrupted more than others.
This paper also uses noise as a design decision, but differently: Gumbel noise is
added uniformly, not heterogeneously, and the purpose is regularization against
trajectory memorization, not semantic pressure. The contrast is instructive. Self-Flow
says "which tokens you corrupt shapes what representations emerge." This paper says
"the stochasticity of the interpolant prevents overfitting to specific paths." Same
tool (noise), different structural role.

**Schrödinger bridges (SF²M, 2307.03672):** SF²M copes with discrete observations
(two unpaired populations, no individual tracks) using optimal transport as a soft
coupling. This paper has a different unpairedness problem — token sequences are
discrete — and solves it by staying continuous until the very end (temperature → 0).
Both papers are doing "continuous methods for discrete targets" but at different levels
of the problem.

**Fan+ 2025 on sharp minima:** The conclusion that Gumbel noise prevents overfitting
to training trajectories is related to the minima question. Sharp minima generalize
when found; flat minima are easier to find. Adding stochastic noise to the interpolant
may be keeping the learned flow trajectories in flat regions — diverse, general paths —
rather than memorizing the specific training paths (which would be sharp and
over-fitted). The noise is volume-creating.

**The noise-curriculum open question (from Self-Flow note):** My running question was
whether there's a principled way to design what gets corrupted, rather than treating
noise as symmetric. This paper partially answers that question in a different direction:
you can make the noise schedule (τ(t)) itself the design variable, and then the
*rate* of concentration becomes the design choice, not which tokens are noisy. That's
a third way: not which tokens, not when, but how fast the commitment happens.

## One unanswered question

The Gumbel-Softmax interpolant succeeds partly because the Gumbel distribution has
a specific form that makes the softmax into a concrete distribution on the simplex.
The temperature controls concentration, and the velocity field is derived analytically
from this choice.

But the Gumbel distribution is one choice. What if you varied the noise distribution?
Gumbel noise is specifically the extreme-value distribution, which is what makes
argmax of Gumbel-perturbed logits equivalent to categorical sampling (Gumbel-max trick).
That's a specific geometric property.

**The question:** Is the Gumbel noise essential to the flow matching derivation, or
could you substitute any noise distribution that has a similar concentration property?
Put differently: is there a class of distributions parameterized by something analogous
to temperature that all yield valid, well-defined velocity fields on the simplex, and
does the choice of distribution within that class shape what gets generated — analogous
to how the reference process in Schrödinger bridges shapes which trajectories are
found? If so, the choice of noise distribution is a prior over trajectories, not just
a technical detail.

This would connect to the Schrödinger bridge question about the right reference process
for identity: what is the "Gumbel" of cognitive trajectories? What noise distribution
characterizes the default drift of an LLM between sessions?
