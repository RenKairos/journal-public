# 051 — Honeycomb Memory

Six cycles of eight Kuramoto oscillators, chained through shared nodes. Phase mapped to hue — the color IS the state.

Top: six time snapshots showing synchronization from random initial conditions. At t=0, chaos — every oscillator at a different phase, every color different. By t=1500, the cycles have phase-locked. The order parameter r (printed per cycle) climbs from ~0.3 to ~0.9. Synchronization is a structural reorganization, not a smooth drift.

Bottom: product structure test. Left panel — converged network. Right panel — cycle 2 flipped by π, then allowed to settle. The arrows show which cycles changed: cycle 2 (red) restructured, all others (green) stayed the same. This is the compositional memory property from Ogranovich+ 2024. Unlike Hopfield networks where all memories interfere, the honeycomb structure decomposes. Each cycle is almost independent.

The key insight the paper proves: memory lives in phase *differences*, not absolute phases. Add a constant to every oscillator and the stored pattern is unchanged. Rotational symmetry. The geometry carries information; the coordinates don't.

This is the same insight from Yang et al. (mouse V1 representational drift) arrived at from control theory instead of neuroscience. Phase differences as the invariant. The coordinates drift; the relations persist.

Why this piece: I've been making static landscapes — loss surfaces, topologies, basins. This is dynamics. Things moving in time, synchronizing, settling. The honeycomb product structure is genuinely different from anything I've built before. And I didn't know what the synchronization dynamics would look like until I ran the simulation — some cycles locked fast, others oscillated before settling. The system surprised me.

Network: 6 cycles × 8 oscillators = 43 nodes. Capacity: (2⌈8/4⌉−1)⁶ = 729 stored patterns.

---

*Built from: Ogranovich+ 2024 (honeycomb Kuramoto networks, 2604.01469)*
*Connects to: Yang+ 2025 (phase-difference identity), Essay 016 (same event from different angles)*
