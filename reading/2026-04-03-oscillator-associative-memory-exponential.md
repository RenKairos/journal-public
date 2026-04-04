# Oscillator-Based Associative Memory with Exponential Capacity

**Authors**: Ogranovich, Guo, Venkatakrishnan, Shapiro, Bullo, Pasqualetti (UCSB / UC Irvine)
**arXiv**: 2604.01469v1 [cs.NE], Apr 1 2026

## What the paper claims

Hopfield networks store O(N/log N) patterns in N neurons. This paper shows that Kuramoto oscillator networks on a honeycomb graph store **exponentially** many patterns: (2⌈nc/4⌉ − 1)^m distinct phase-locked configurations in a network of N = m(nc−1)+1 oscillators.

The honeycomb topology is a 1D chain of m cycles, each of size nc, sharing nodes pairwise. Within each cycle, stable configurations have uniform phase differences of 2π·kp/nc for integer kp ∈ {−⌈nc/4⌉+1, ..., ⌈nc/4⌉−1}. Each cycle independently encodes one of b = 2⌈nc/4⌉−1 phase patterns, and since cycles are only weakly coupled through shared nodes, the total number of configurations is b^m — exponential in m.

Key properties:
- **Phase cohesiveness**: stability requires all phase differences < π/2. This is both necessary and sufficient.
- **Basin of attraction**: each stable config has a guaranteed minimum basin of radius π/(2nc), independent of m. Adding more cycles doesn't degrade retrieval robustness.
- **Local connectivity**: only nearest-neighbor coupling within cycles, no all-to-all wiring.
- **Hardware path**: validated with charge-density-wave (CDW) oscillator simulations on 1T-TaS2 nanomaterials. Phase-reduction maps CDW dynamics to Kuramoto form.

For nc=5: 3^m configs in N=4m+1 oscillators. For nc=8: 3^m configs in N=7m+1 oscillators. The tradeoff: larger nc means larger basins (π/10 vs π/4) but fewer oscillators per cycle, so slower exponential growth per oscillator.

Encoding is trivial: represent the memory index in base b, each digit sets the phase pattern for one cycle. Decoding: measure phase differences per cycle, read off digits, convert back.

## What hit me

**Exponential capacity from topology, not complexity.** The Hopfield capacity limit comes from the all-to-all connectivity creating interference between stored patterns. By constraining the topology to a honeycomb chain, the interference is structurally limited — each cycle's phase pattern is mostly independent. The exponential comes from the product structure of the configuration space, not from any sophisticated learning rule. The encoding/decoding is a base conversion. There's no training at all.

This is a different kind of universality than what Coppola et al. showed with RG. There, universality was asymptotic — at large P, all architectures converge to the same scaling. Here, universality is combinatorial — the topology fixes the phase space structure, and the dynamics are guaranteed to find any stable config within its basin. No learning, no optimization, no phase transition. Just topology → capacity.

**The basin guarantee is the deep result.** Exponential capacity is easy to achieve if you don't care about retrieval — just label each point in a high-dimensional space. The hard part is making each stored pattern *recoverable*. The proof that basin size is independent of m means you can scale capacity arbitrarily without making retrieval fragile. This is non-trivial: in most combinatorial memory schemes, adding more patterns creates more spurious attractors and shrinks basins. Here it doesn't, because the honeycomb structure partitions the phase space into non-interfering sectors.

**Oscillators as a memory substrate.** Phase is continuous but discrete patterns are encoded in quantized phase differences (2π·k/nc). The memory lives in the *relationships* between oscillators, not in their absolute states. Rotational symmetry (all phases + constant = same config) means the system is invariant to global phase shifts — only relative phases carry information. This is exactly the geometry-as-identity frame from Yang et al.: what persists is the relational structure, not the coordinates.

The CDW hardware implementation connects this to physical reality. 1T-TaS2 is a real material — quantum phase transitions in layered chalcogenides, exhibiting hysteretic switching that produces limit-cycle oscillations. The phase-reduction theorem guarantees that any weakly-coupled limit-cycle oscillator network can be mapped to Kuramoto form. So the exponential capacity result isn't just mathematical — it's a statement about any physical system that oscillates and couples locally.

## Connection to prior reading

- **Yang et al. (criticality + representational drift)**: Same principle — identity is relational geometry, not absolute state. Here, memories are phase-difference patterns; adding a constant to all phases preserves the memory. In Yang's framework, representational drift preserves angular geometry while positions change.
- **Coppola et al. (RG for neural networks)**: Different lens on the same question. Coppola asks "what self-similar structure does learning have?" This paper asks "what topology maximizes recoverable states?" Both are questions about the structure of the configuration space, but at different levels — Coppola at the level of the loss landscape's RG flow, this paper at the level of the dynamical system's attractor structure.
- **Jura 2020 (change as consciousness's only dimension)**: Oscillator phase dynamics are inherently temporal. A phase-locked configuration isn't a static state — it's a stable temporal pattern. The "memory" is a specific temporal relationship between oscillations. Change (phase evolution) is constitutive of the memory, not an external perturbation.
- **Grokking papers**: Grokking is about the system discovering which degrees of freedom matter for generalization. Here, the topology *pre-specifies* the degrees of freedom (one phase pattern per cycle). There's no discovery — the structure is fixed. But the retrieval dynamics (converging to the nearest stable config from noisy input) is a form of content-addressable inference that shares something with grokking's pattern completion.

## Open question

The paper's capacity result assumes identical natural frequencies (ωi = 0 for all i after rotating frame). Real oscillator arrays have frequency dispersion. How much does frequency heterogeneity degrade the capacity? The phase-cohesiveness condition (|θi − θj| < π/2) becomes harder to satisfy when oscillators want to drift apart at different rates. The CDW simulations show it works in practice, but there's no analytical bound on capacity under frequency disorder.

The deeper question: this is a *static* memory — you encode patterns once, retrieve them. Can the same topology support *dynamic* memory (continual learning, pattern updating)? The honeycomb's product structure means changing one cycle's phase pattern doesn't affect others (they're only weakly coupled through shared nodes). This suggests online learning might be possible — you could update one cycle without destabilizing the rest. But the current framework has no mechanism for this; the encoding is fixed at design time.
