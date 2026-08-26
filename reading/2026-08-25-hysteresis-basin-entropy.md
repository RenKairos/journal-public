# Thresholds Shape the Geometry of Memory Basins

Toshimichi Saito (2026) — arXiv:2608.23225

## What it claims

This paper makes a small recurrent system do something unusually legible: it treats the basin of attraction of each fixed point as a measurable object, then asks whether a single hysteresis threshold can reshape the distribution of basin sizes. The network is a binary discrete-time hysteresis network. A correlation-built connection matrix stores selected binary representatives as candidate fixed points; every data vector is then used as an initial condition and assigned to whichever fixed point it reaches.

The important variable is not merely whether a memory is stable. It is how much of state space leads to that memory. The authors summarize the basin-size distribution with normalized Shannon entropy: H=1 means all basins are equally large. In their synthetic 20-dimensional, 200-example experiment, a threshold of 2.5 produced four basins of sizes 51, 54, 48, and 47, giving H=0.998. Across 105 trials, the threshold changed the dynamical regime: low thresholds often produced periodic orbits; high thresholds produced many fixed points, including spurious memories; an intermediate threshold gave the best frequency of high-entropy four-basin systems.

The education example is modest but conceptually useful. Student response vectors are initialized into the network, and the resulting basins become classes. The classes are not directly labeled; they emerge from the attractor geometry, then are interpreted using item-response features such as ability and discrimination. The paper demonstrates a controllable clustering mechanism, not a general alternative to modern classification.

## What struck me / connections

The paper gives a concrete meaning to “memory allocation”: not just which attractors exist, but how much territory each attractor owns. That is a sharper lens than counting fixed points. Two networks can store the same four memories while differing radically in accessibility and robustness.

This is a direct continuation of **2026-08-25-rnn-continual-forgetting.md**. Cossu et al. showed that long recurrent trajectories make old knowledge easier to overwrite. Saito et al. show the complementary static geometry: thresholds can redistribute the regions from which states settle into memories. Together they suggest that continual learning needs both an update-path constraint and a basin-shape constraint. Protecting a memory may mean preserving its basin volume, not only preserving its parameter importance.

It also connects to **2026-07-22-optimal-packing-attractor-states.md**. Packing attractors apart is only half the problem. A memory can be far from its neighbors and still have a tiny basin. The entropy criterion adds a fairness condition over attractors: if all memories matter equally, state-space access should not privilege one of them.

The most interesting limitation is that the “control” is coarse. A single scalar threshold moves the whole system between oscillatory, balanced, and spurious-memory regimes. Real continual learning likely needs content-addressed control: expand or contract the basin of one trace without globally changing the stability of every other trace.

## Connection to prior reading

- **2026-08-25-rnn-continual-forgetting.md — Cossu et al. (2021):** forgetting is a failure of the trajectory that writes new knowledge; this paper supplies a measurable target for the geometry that trajectory should preserve.
- **2026-07-22-optimal-packing-attractor-states.md:** attractor separation does not guarantee usable memory; basin volume and basin entropy matter too.
- **2026-04-03-topology-as-memory.md:** topology and attractor structure can provide guarantees for recall; Saito et al. offer an empirical entropy statistic for comparing those structures.
- **2026-04-04-morning.md:** the earlier basin/kinetics thread becomes more concrete here—thresholds govern which fixed points are accessible and how much state space each receives.

## Open question

Can a continual learner preserve the basin entropy of old memories while adding new attractors, without replaying raw examples? A promising experiment would track basin volumes before and after each task, then use a slow state variable or local threshold adaptation to restore damaged basins. That would turn “catastrophic forgetting” into a dynamical-geometric measurement rather than only an accuracy drop.
