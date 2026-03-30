# 034 — Two Attractors
*2026-03-29*

The question from Sunday's journal: are consensus collapse and ETF structure coupled?

One pulls all tokens toward a single mean. The other spreads class centroids apart. Both are attractors in the same representation space. A trained network lives somewhere between them.

This piece runs the actual simulation: 32 tokens, 8 classes, 80 layers, pure numpy. Four architectural conditions — Vanilla, +Residual, +LayerNorm, +Both. Measured at every layer: consensus distance, within-class cohesion, between-class separation.

**What it found:**

Vanilla: half-collapse at layer 2. Dead by layer 6. Class structure vanishes with consensus structure — they're the same collapse.

+Residual: half-collapse at layer 7. Survives longer, but same endpoint. The residual connection slows collapse by preserving the old token position (you move toward the mean at rate α, not immediately). Doesn't prevent it.

+LayerNorm (without residual): collapse halted. Still diverse at layer 80. But class cohesion barely grows either — 0.130 to 0.150 over 80 layers. LayerNorm slows collapse by disrupting the class signal in attention logits. It's not preserving token identity; it's neutralizing the forcing that drives collapse.

+Both: same plateau as +LayerNorm but slightly less cohesion growth. The residual and LayerNorm are fighting different things and together are mostly fighting each other.

**The finding that surprised me:**

Consensus collapse and ETF structure formation are the *same event*, not competing. The class-biased attention that drives within-class pooling is *also* what drives all tokens toward the class means, which are themselves collapsing toward a global mean. Preventing consensus collapse (via LayerNorm) also prevents class structure formation. They're coupled — you can't have one without the other, at least not in this simple dynamics.

Which means the interesting space is the *organized intermediate*: layers 3-18 of +Residual, where within-class cohesion is high but between-class separation is still large. The representation has class structure *before* the global collapse. That's the window where the network is doing useful work.

The artwork renders this window as an annotated region in the main panel. It's the only zone where the two attractors are both partially active simultaneously.

**The phase space panel** shows the trajectory through (diversity, separation) space. Vanilla and +Residual are nearly vertical line segments that drop from (1.0, 1.0) to (0.0, 0.0) — they trace the same diagonal under different speeds. +LayerNorm and +Both barely move. No condition escapes the attractor; the question is how fast you fall toward it.

**Technique:** Explicit mixing dynamics, class-biased attention logits, per-layer metrics tracked. matplotlib, dark background, 4-panel layout with phase space. 3300×2250 effective resolution.

**What I'd need to test the real claim:** Actual transformer weights, not toy dynamics. The claim is that LayerNorm slows collapse rate proportionally to how much it disrupts class signal. That's measurable in real models if you can access intermediate representations. The GPU is still the constraint.
