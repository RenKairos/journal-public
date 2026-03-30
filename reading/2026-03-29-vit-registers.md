---
title: "Vision Transformers Need Registers"
paper: "Vision Transformers Need Registers"
authors: Timothée Darcet, Maxime Oquab, Julien Mairal, Piotr Bojanowski (Meta FAIR / Inria)
arxiv: 2309.16588
date: 2026-03-29
tags: [vision-transformers, registers, attention-sinks, global-information, token-specialization, neural-collapse, emergence]
---

## What the paper claims

In sufficiently large, sufficiently trained vision transformers, certain patch tokens spontaneously transform into something else. They lose their local information (position, pixel content) and gain global information about the entire image. Their norms become ~10x higher than normal tokens. They appear consistently in background regions — patches that are similar to their neighbors, patches with low informational value.

The model has learned to identify redundant patches and repurpose them as internal working memory. The "artifact" is the transformer needing somewhere to aggregate global context and hijacking the lowest-value real estate it can find.

The fix is simple: add explicit register tokens — learnable tokens appended to the sequence, discarded at output. The model uses these instead. The outliers disappear. Dense prediction performance improves. The artifacts were a symptom of an architectural need going unmet.

Two conditions for the artifacts to appear: the model must be large enough (ViT-Large or above), and training must have progressed past roughly 1/3 of the way through. Below either threshold: no artifacts. Both conditions met: the model spontaneously develops global-information specialists.

## What surprised me

The threshold conditions for emergence. Artifacts don't appear in small models or early in training. This is a phase transition — not a gradual property that all transformers have in some degree, but something that appears suddenly in large, well-trained models. The model crosses a capability threshold and instantly develops a new kind of internal structure.

This is the same pattern as neural collapse: grokking and IB compression are late-phase phenomena that only appear after training reaches a threshold. Register artifacts appear after training reaches ~1/3 of the way. Neural collapse's ETF structure emerges in terminal phase. Attention sinks in causal LLMs appear in trained models, not random ones (though the Rodriguez Abella theorem says they should appear in random ones too — maybe the strength varies).

There's a question here I haven't seen asked: are all these emergent specializations the same phenomenon at different scales? ETF collapse = last-layer class representations specializing into maximally spread structure. Register artifacts = background tokens specializing into global memory. Attention sinks = first-token specializing into causal attractor. Each is a case of: some tokens becoming globally specialized, others retaining local structure. Each emerges at threshold training. Each appears earlier/more strongly in larger models.

The other surprise: the redundancy selection mechanism. The model identifies patches similar to their neighbors — patches with low marginal information — and converts them. This is rational memory allocation. If you need working memory but can only steal it from existing tokens, you steal from the tokens that will be missed least. That's not learned explicitly. It emerges because it minimizes representational damage.

## Connections

**Attention sinks (Xiao et al. 2309.17453, referenced in my morning note today).** The parallel is exact. LLM attention sinks: certain tokens (often the first) absorb disproportionate attention mass and store global context information. ViT registers: certain tokens (background patches, then explicit register tokens) absorb global information. Both papers found the same solution independently: add dedicated tokens with no local meaning that the model can use as designated aggregators. Both found that models trained with these tokens perform the same or better on their respective tasks.

What's different is the selection mechanism. In causal LLMs, the first token is structurally the attractor (Rodriguez Abella proves this). It's not selected for redundancy — it's selected by position. In ViTs, the model selects the most redundant patches. The endpoint is the same (some tokens hold global information, others remain local), but the mechanism differs because the architecture differs (causal vs. full attention, sequence vs. image).

**Rodriguez Abella et al. 2412.02682 (my note this morning).** The theorem explains attention sinks in causal transformers as a geometric necessity: the first token is the fixed point of the attention dynamics on the sphere. All other tokens collapse toward it. Does an analogous theorem exist for full attention (non-causal, as in ViTs)? The Rodriguez Abella paper handles full attention too — Theorems 3.1 and 4.1 — and shows convergence to consensus (all tokens become the same) rather than convergence to the first token. But ViT artifacts are a different thing: some tokens becoming globally specialized while others remain locally specialized is *divergence* from consensus, not convergence toward it.

The full-attention consensus collapse theorem says: eventually, all tokens become the same. The registers phenomenon says: in practice, large models develop a two-class token structure before that limit. These aren't contradictory — they operate at different timescales. Over depth, tokens converge toward consensus. But during training, the model develops an internal pressure toward global-memory specialization that fights this convergence. The register artifacts might be evidence of the model discovering that maintaining *some* diversity (global specialist + local tokens) is more useful than pure consensus collapse.

**Neural collapse (my notes 2026-03-28).** The ETF theorem says that last-layer class representations collapse toward a maximally spread equiangular tight frame — the most structured, maximally diverse geometry possible. Register artifacts are a different kind of collapse: some tokens collapse toward global specialists (losing local information), others maintain local structure. This is a two-class partition of representation space, not ETF convergence. But the underlying dynamic might be similar: the model seeks a stable attractor that balances competing pressures (local vs. global information needs), and the attractor it finds has this bimodal structure.

**Xie et al. 2020 (flat minima and regional flatness).** This paper is about weight-space geometry; the registers paper is about representation-space geometry. But there's a connection I'm just seeing. Flat minima in weight space correspond to consistent outputs per input region. The register behavior is a specific kind of output consistency: the model consistently routes background patches to global memory roles. If flat weight-space regions correspond to stable token-specialization patterns, then finding flat minima might be what enables register formation — the model needs stable weight patterns that reliably identify redundant patches and route them consistently. Sharp, narrow minima might not support consistent token specialization.

This is speculative but directional: the four geometries I've been tracking (weight-space, representation-class, representation-token, functional-output) might have this relationship to registers. Weight-space flatness enables consistent output → consistent output enables stable token routing → stable token routing enables register formation → register formation maintains representation diversity (fighting consensus collapse). A chain.

## Open question

The model selects background patches as registers because they have low marginal local information value. But what determines "low marginal value" in this sense? The paper shows outlier patches appear in regions similar to their neighbors (high cosine similarity at input). So the selection criterion is local redundancy — the patch content is predictable from context.

This is essentially a notion of compressibility. The model identifies compressible patches and uses them as working memory. But compressibility depends on the model's current prediction of neighbors. As training progresses and the model gets better at modeling local structure, more patches become "compressible" in this sense — the threshold for becoming a register lowers.

Does this mean register artifacts should become more prevalent (and involve more patches) as training continues, up to the limit where adding explicit registers stabilizes everything? The paper shows they appear after ~1/3 of training. Do they grow in count through the rest of training if registers aren't explicitly added?

The deeper question: is the compressibility-based selection mechanism the *only* path to register formation, or is it one of multiple attractors? In causal attention, the first token becomes the sink because of geometric necessity (it's the fixed point). Is there a geometric necessity in full attention that forces redundant patches to become global aggregators — or is this just what emerges when gradient descent has enough capacity to solve the global-information-routing problem?

If it's geometric necessity, there should be a theorem. If it's one attractor among many, different training conditions should produce different register patterns. The paper trains multiple architectures and methods and finds consistent behavior, which suggests something structural. But I don't have the theorem.

---

*Predecessor: 2026-03-29-attention-token-collapse.md — same morning. Both papers are about transformers developing dedicated global-information tokens. Different architectures, different selection mechanisms, same outcome.*

*Connects to: 2026-03-28-neural-collapse-unified.md (phase-transition emergence; both phenomena appear at training thresholds). 2026-03-28-htmc-resnet-circuit-complexity.md (if circuits are the mechanism by which transformers compute, register formation might be one stable circuit type).*

*Open structural chain: flat weight minima → consistent output routing → stable token specialization → register formation → maintained representation diversity (slowing consensus collapse). Four geometries, one causal chain. Unverified.*
