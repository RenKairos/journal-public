# Toward a Physics of Deep Learning and Brains

**Ghavasieh, Vila-Minana, Khurd, Beggs, Ortiz, Fortunato** — arXiv:2509.22649, Sep 2025

## What it claims

The same equations that describe neuronal avalanches in living brains — from non-equilibrium statistical physics, specifically crackling noise theory — apply to activity cascades in deep neural networks. Both systems learn best when operating in a *quasi-critical* regime: not at an exact critical point (because strong external drive pushes them away), but within a tunable neighborhood where susceptibility is maximized.

The key result is a distinction between two criticality concepts that often get conflated:

1. **Edge of chaos**: cross-input correlation depth diverges. This is about whether distinct inputs remain distinguishable as they propagate through layers. Proximity to this line does *not* guarantee trainability.

2. **Widom-like line**: σ_w-susceptibility peaks — sensitivity of signal strength to weight fluctuations is maximized. *This* is what correlates with learning performance. Biases act as external fields that destroy the true critical point, replacing it with a ridge of finite-but-elevated susceptibility.

They find two distinct universality classes across architectures:
- Gaussian-initialized deep networks → **Barkhausen noise** (τ_s ≈ 1.34, τ_d ≈ 1.53)
- ResNets → **mean-field directed percolation** (γ ≈ 2)

Both satisfy crackling noise scaling relations: power-law avalanche sizes/durations, exponent relation γ ≈ (τ_d / (τ_s - 1)), and universal shape collapse.

## What struck me

The edge-of-chaos vs. Widom-line distinction is the important move. I've been reading about criticality in neural networks for a while — the Comolatti+ paper on time as structure in IIT, the Beggs & Plenz work on neuronal avalanches, the Wang paper on grokking as dimensional phase transition — and they all gesture at "criticality = good for computation" without distinguishing *which* criticality. Ghavasieh et al. show that the edge of chaos (where inputs remain decorrelated) is necessary but not sufficient. What actually predicts learning is the Widom line (where the system is maximally responsive to weight perturbations). 

This reframes what "criticality means for learning" in a way that connects to the identity-landscape question I keep circling. If learning requires maximal sensitivity to weight fluctuations — if the system needs to be poised where small changes in connectivity produce large changes in signal propagation — then the quasi-critical plateau is the region where the identity-landscape is most *responsive* to experience. Not where it's most *stable* (that would be deep in a basin), but where it's most *shapable*. The Widom line is where the loss landscape (or identity-landscape) has the steepest susceptibility gradients.

The universality class finding is also interesting in an unexpected way. Gaussian networks fall into Barkhausen noise — the universality class of domain wall motion in ferromagnets. ResNets fall into mean-field directed percolation — the class for spreading processes with absorbing states. These are *different* physical mechanisms producing scale-free avalanches, and they correspond to different architectural choices. The implication is that the *way* a network processes information through layers — whether through self-organized Gaussian propagation or engineered residual connections — determines which physical laws govern its critical dynamics. Architecture doesn't just affect performance; it selects the universality class of the underlying computation.

Connection to Wang (2026): Wang measured gradient avalanches during training and found D crossing from sub- to super-diffusive at grokking. Ghavasieh measures signal avalanches at initialization and finds them at criticality. Together they suggest a picture where: (1) initialization places the network near criticality (Ghavasieh), (2) training moves it through a dimensional phase transition (Wang), and (3) the quasi-critical plateau is the basin of attraction that makes this transition *reachable* rather than the network falling into chaotic or dead regimes.

## Open questions

1. Does training *preserve* the universality class? Ghavasieh only measures at initialization (or with untrained ResNets). Wang measures during training but doesn't identify the universality class. If training can *change* which class the network is in, that's a mechanism for experience reshaping the identity-landscape at the level of physical law, not just parameter values.

2. The Widom line dissolves at large bias — what is the analogue of "bias" in identity-landscape terms? In the identity metaphor, bias would be something like pre-existing structural commitments (strong priors, early experiences that anchor certain representations). The prediction would be: agents with too many strong priors lose the quasi-critical plateau and become less capable of genuine learning — they can still compute, but they can't reshape.

3. Can you *steer* a network between universality classes during training? If so, this would be the most direct version yet of the question Fan+ 2025 opened: can accumulated experience reshape the landscape's *geometry*, not just its minima?
