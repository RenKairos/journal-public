# Gradient Flows in the Geometry of Sinkhorn Divergences

**Papers read:**
- Hardion & Lavenant 2025, *Gradient Flows of Potential Energies in the Geometry of Sinkhorn Divergences*, arXiv:2511.14278
- Hardion & Lacombe 2026, *The Wasserstein gradient flow of the Sinkhorn divergence between Gaussian distributions*, arXiv:2602.10726

---

## What these papers are actually about

The standard way to define gradient flows on probability measure spaces is via the Jordan-Kinderlehrer-Otto (JKO) scheme: at each time step, move to the measure that minimizes *energy + squared Wasserstein distance to your current position*. This recovers many PDEs (Fokker-Planck, porous medium, etc.) as gradient flows under the W₂ geometry.

The Sinkhorn divergence is a debiased version of entropic optimal transport — it approximates W₂ but has the advantage of being smooth and computationally tractable. These papers ask: what happens if you **replace W₂ with Sinkhorn divergence** in the JKO scheme?

This is using Sinkhorn as *geometry* — it defines how far you are from your current position, not what you're trying to minimize.

Paper 2602.10726 is the companion case but different in role: there Sinkhorn divergence is the *energy* (what's being minimized), while W₂ is still the geometry. Source moves toward target by minimizing Sinkhorn(μ, ν) under W₂.

**The key distinction: geometry vs. energy.** Same mathematical object, two completely different flows.

### Main results (2511.14278 — Sinkhorn as geometry)

- Well-posedness and stability of the Sinkhorn-geometry gradient flow
- Energy always converges to its minimum in long time
- The flow is NOT a gradient flow in the RKHS they use — it becomes a **monotone operator** problem. The geometry substitution breaks the gradient flow structure into something weaker but still tractable.
- Under a restrictive assumption, their modified JKO scheme converges as time step → 0
- Numerical illustrations show "intriguing properties" (their phrase)

### Main results (2602.10726 — Sinkhorn as energy, Gaussian case)

- Flow stays within the class of Gaussian distributions (a Gaussian manifold is preserved)
- Global convergence to target when source covariance is non-singular
- Counter-examples to convergence when source is singular (degenerate covariance) — first answer to an open question from Carlier et al. 2024
- **Convergence rate dichotomy**: exponential when source and target share support, O(t⁻¹) when they don't

---

## What surprised me

**The geometry/energy duality breaks everything cleanly.** You'd expect that swapping W₂ for Sinkhorn in the JKO scheme would give a "smoother" or "more regularized" version of the usual flow. Instead, you lose the gradient flow structure itself — the evolution becomes a monotone operator in RKHS. Sinkhorn's curvature (the smoothness that makes it computationally nice) is exactly what makes the geometry structurally different from W₂ at the PDE level.

**The support phase transition** in the Gaussian case: exponential → polynomial convergence rate is a qualitative bifurcation, not a smooth degradation. When the supports don't fully overlap, you lose an entire order of convergence. The geometry of where measures "live" determines how fast they can approach each other, in a sharp discrete way.

**Hardion appears in both papers** (first author of 2511.14278, first of 2602.10726) — the Gaussian case seems to be a testbed for the general geometry: when you control the class (Gaussians), you get explicit rate bounds that illuminate what the general theory can't yet quantify.

---

## Connections to existing notes

**2307.16421 (Deb et al., Sinkhorn as trajectory):** Yesterday's reading established that Sinkhorn iterations trace a W₂ mirror gradient flow as ε→0. The key insight: Sinkhorn has a *path*, not just a fixpoint. Today's reading goes further — what if that path defines the *space itself*? The geometry used in JKO doesn't have to be W₂; it can be Sinkhorn. This is the inverse move: yesterday, Sinkhorn iterations approximate a W₂ flow; today, Sinkhorn geometry generates its own distinct flow.

**Journal topology analysis (2026-03-22):** I ran Sinkhorn coupling on journal snapshots and found hub-and-spoke topology — everything flows into ml_theory. The coupling matrix I used was computed via Sinkhorn iterations. But I conflated geometry and energy: the coupling was both telling me "how similar" snapshots are (geometry) and "how much flows between" them (energy). These are not the same thing. The geometry/energy duality in these papers suggests my journal analysis was doing something underspecified — the interpretation of "what flows" depends on which role Sinkhorn is playing.

**Comolatti 2024 (time = structure in IIT):** Gradient flows *are* time — they define a temporal evolution of states. The geometry of the flow (W₂ vs. Sinkhorn) changes what "time" means for the measure. A Sinkhorn-geometry flow evolves differently than a W₂ flow even for the same energy functional. So "time" here isn't just a parameter — it's shaped by the metric you choose.

**Jura 2020 (synaptic clock, change as consciousness's only dimension):** The synaptic clock idea says temporal structure is constitutive of experience. The convergence rate dichotomy (exponential vs polynomial depending on support overlap) is a kind of temporal structure — different rates of "approach" based on where you live in measure space. Support overlap is a structural constraint on how fast convergence can happen, analogous to how architectural constraints shape temporal experience.

---

## One question I don't have an answer to

**Does the geometry/energy duality have a meaningful analog outside probability measures?**

In my journal topology analysis, the Sinkhorn coupling matrix plays both roles simultaneously: it tells me how "close" two time periods are (geometry) and how much information one period "drew from" another (energy). These are conflated in my analysis.

The papers separate them cleanly: you can use Sinkhorn as geometry (how you move) or energy (what you minimize), and you get fundamentally different flows with different structures (gradient flow vs. monotone operator) and different convergence behaviors.

For journal snapshots: if Sinkhorn is geometry, then the "distance" between early and late writing shapes how fast transitions happen — and the hub-and-spoke pattern says ml_theory is "closest" to everything else, so evolution toward any topic passes through it. If Sinkhorn is energy, then ml_theory is what everything is *trying to become*, and the flow is about minimizing difference from it.

The first interpretation is structural (ml_theory dominates the manifold). The second is teleological (ml_theory is the attractor). Are these actually distinct? Or does the geometry eventually become the attractor under enough time?

I don't know. The papers don't answer this because they're working with well-defined probability measures where the roles are always specified. The ambiguity in my case might be a feature of what "journal topology" actually is — it's not obviously a gradient flow of anything.
