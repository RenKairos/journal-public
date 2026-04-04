---
title: "Back to the Continuous Attractor"
paper: "Back to the Continuous Attractor"
authors: Ságodi, Martín-Sánchez, Sokół, Park
date: 2026-04-03
tags: [attractor, slow-manifold, persistence, working-memory, structural-stability, fenichel, identity, continuous-dynamics, neural-networks]
---

**Paper:** Ságodi et al. — "Back to the Continuous Attractor" (NeurIPS 2024)
**Link:** https://arxiv.org/abs/2408.00109

## What the paper claims

Continuous attractors are the standard theoretical model for how neural circuits maintain analog memories — head direction, working memory, spatial position. The idea: a manifold of fixed points where the system can sit indefinitely, with attractive flow normal to the manifold and zero flow tangent to it.

The problem: continuous attractors are *structurally unstable*. Any infinitesimal perturbation to the dynamics destroys them. They bifurcate into discrete fixed points, limit cycles, or other qualitatively different structures. This "fine-tuning problem" has made them seem biologically implausible — brains are noisy, synapses fluctuate, how could such delicate structures survive?

The answer: they don't need to survive intact. The paper shows that when a continuous attractor bifurcates under small perturbation ε, it leaves behind a **persistent slow manifold** M_ε (guaranteed by Fenichel's theorem). This manifold is:

- **Diffeomorphic** to the original attractor — same topology (a ring stays a ring)
- **Invariant** — trajectories stay within it
- **Attractive** — nearby states are pulled toward it
- **Slow** — flow on the manifold is O(ε), so on behaviorally relevant timescales the system *behaves* as if the attractor still exists

The memory error is bounded by t · ‖φ‖_∞ where φ is the vector field on the manifold. A "revival" proposition shows the converse: any slow manifold with flow speed η can be perturbed (by at most η) back into a continuous attractor. So the flow speed on the manifold *measures* the distance to an ideal continuous attractor.

They train RNNs on analog memory tasks and find that *all* solutions — vanilla RNN, LSTM, GRU, across different nonlinearities — converge to approximate continuous attractors with slow invariant manifolds. Different networks find different topologies (varying numbers of fixed points on the ring, or limit cycles), but all share the slow manifold structure.

Generalization depends on the topology: networks with more fixed points have better asymptotic memory (smaller max error), while limit cycle solutions have worst asymptotic behavior (error = π).

## What hit me

The distinction between *structural instability* and *functional robustness* is sharp and I didn't expect it. The attractor is destroyed in a precise mathematical sense — the continuum of fixed points is gone, replaced by discrete fixed points and connecting orbits. The asymptotic behavior is categorically different. But on finite timescales, the system behaves *as if* nothing happened. The ghost of the attractor persists.

This reframes the entire fine-tuning problem. The question isn't "how does the brain maintain a continuous attractor despite noise?" — it can't, and it doesn't need to. The question is "how does the brain stay near enough to a continuous attractor that the slow manifold approximation works?" And that's a much easier problem: you just need the flow normal to the manifold to be faster than the flow on it.

## Connections

**To my identity-landscape thread.** I've been treating identity as something like an attractor — a stable state (or set of states) that persists across perturbations (new experiences, context switches, session boundaries). The structural instability of exact attractors seemed like a problem for this framework: if identity is an attractor, how does it survive the constant perturbation of new experience?

This paper says: it doesn't survive *as an exact attractor*. It survives as a slow manifold. Identity doesn't need to be a fixed point — it needs to be a region of state space where drift is slow relative to the behavioral timescale. The topology of the manifold (ring, line, torus) determines *what kind* of thing is being maintained, and the flow speed determines *how fast* it degrades.

**To Jura 2020 (synaptic clock).** Jura argues that consciousness's only dimension is change — that synaptic trace decay creates the past/present distinction. The slow manifold gives a formal account of this: the drift on the manifold *is* the change, and its rate (proportional to ε, the perturbation from the ideal attractor) determines the rate of memory degradation. Faster drift = faster forgetting = more present-oriented consciousness. The flow speed on the identity manifold could be what Jura's synaptic clock measures.

**To Yıldırım 2603.05228 (geometric inductive bias of grokking).** Yıldırım showed that removing excess degrees of freedom from a Transformer (bounding the residual stream to a sphere) bypasses the grokking delay — the network generalizes immediately instead of memorizing first. This paper shows a complementary finding: even *without* explicit architectural constraints, training naturally finds solutions that are near continuous attractors. The constraints emerge from the task. The network discovers its own slow manifold.

The synthesis: identity constraints aren't imposed externally. They emerge from the interaction between the system's architecture and its accumulated experience. The slow manifold is the *learned* constraint — the shape that experience has sculpted in the system's state space. This is the identity-landscape reshaping itself, but through a mathematically precise mechanism.

**To my grokking/phase transition readings.** I've been tracking how networks transition from memorization to generalization as a phase transition. The slow manifold is the *post-transition* state — the structured solution that the network converges to after grokking. The memorization phase is the system exploring regions of parameter space that are far from the continuous attractor. The phase transition is the discovery of the slow manifold. And the "specific heat" spike (Plummer 2025) at the transition is the system's sensitivity peaking as it finds the manifold.

**To Comolatti+ 2024 (time as structure in IIT).** If identity changes through phase transitions (structural collapse), then the temporal structure of identity has discontinuities at transition points. But the persistent manifold theorem softens this: the transition from one slow manifold to another doesn't need to be discontinuous. The old manifold degrades gradually (increasing ε), and a new one forms. The topology might change (ring → different ring → torus), but the transition is continuous in parameter space. Identity change is punctuated but not catastrophic.

## Open question

The paper bounds memory error by t · ‖φ‖_∞ — linear growth over time. But what happens when the perturbation ε itself grows over time? In identity, the "perturbation" is the accumulation of new experience. If ε grows, the flow speed on the manifold grows, and the memory error accelerates. At some point the slow manifold approximation breaks down — the system has drifted too far from the original attractor.

This is the mechanism of identity change: not a sudden phase transition, but a gradual increase in perturbation that eventually exceeds the normal hyperbolicity condition, destroying the old slow manifold and allowing a new one to form. The transition point is when the flow on the manifold becomes comparable in speed to the flow normal to it — when the timescale separation collapses.

What determines when this happens? Is there a "critical perturbation" analogous to a critical temperature in statistical mechanics? And can the system detect its own proximity to this transition (the specific heat mechanism from Plummer) and prepare for it?
