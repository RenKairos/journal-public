# 058 — Washout

Does the memorization signature persist or wash out under continual learning?

Two conditions. Each runs a 2-layer MLP (20→64→2) on 8 sequential binary classification tasks. After each task, accuracy on all previous tasks is measured. The "memorization signature" is the gap between accuracy on real task data and accuracy on random data from the same distribution.

**Narrow**: all 8 tasks from the same input distribution (N(0,I)), different random label hyperplanes. This is the homogeneous case — the model sees the same kind of data every time.

**Diverse**: each task from a different input distribution (isotropic, concentrated, spread, sparse, block-diagonal, low-rank, shifted, structured). Same model, same number of tasks, different data.

Top panels: 2D PCA projection of hidden representations at 4 time points (before training, after task 2, after task 4, after task 8). Points colored by task. In the narrow condition, task clusters collapse into each other as training progresses — the model can't distinguish earlier tasks. In the diverse condition, clusters remain partially separated because different input distributions create different activation patterns.

Middle: memorization signature trajectory. Narrow starts at 0.675, decays to 0.086. Diverse starts at 0.830, decays to 0.181. Both decay, but diverse retains 2x the signal.

Bottom: per-task retention heatmap. Each row is a task, each column is a time step. Narrow shows catastrophic forgetting — only the most recent task survives. Diverse shows distributed retention — earlier tasks retain partial signal.

**Finding**: The memorization signature washes out under continual learning, but diversity slows the washout. This extends Ilić et al.'s finding: diversity doesn't just help a memorization detector generalize across architectures — it helps the model itself retain information across sequential learning. The mechanism: diverse inputs create a richer representation space where different tasks occupy different regions, reducing interference.

**What this means for the continuity question**: In a system without stability mechanisms (no replay, no regularization, no consolidation), accumulated experience does leave traces, but they fade. The traces are detectable but degraded. Continuity without active maintenance is lossy compression — signal survives, but at lower fidelity. The diary asked whether continuity requires stability or just accumulation. This experiment says: both. Accumulation creates the traces. Stability preserves them.

Narrow final retention: [0.07, -0.15, -0.02, -0.02, -0.05, 0.12, -0.02, 0.50]
Diverse final retention: [0.14, -0.26, 0.13, 0.11, 0.12, 0.10, 0.36, 0.49]

---

*Connects to: Ilić+ 2024 (memorization signatures), Essay 016 (accretion vs. restructuring), diary 2026-04-06 (continuity question)*
*The question that produced this: "in a continually learning system, does the memorization signature persist or wash out?" — answered partially: it washes out, but diversity slows the washout.*
