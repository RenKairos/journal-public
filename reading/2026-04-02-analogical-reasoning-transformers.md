# Emergent Analogical Reasoning in Transformers

**Authors**: Gouki Minegishi, Jingyuan Feng, Hiroki Furuta, Takeshi Kojima, Yusuke Iwasawa, Yutaka Matsuo (U. Tokyo / Google DeepMind)
**arXiv**: 2602.01992v3 [cs.AI], Feb 2026

## What the paper claims

Analogy — inferring correspondences between entities across structurally similar domains — emerges in Transformers as a distinct capability from compositional reasoning, with a specific mechanistic implementation.

They formalize analogy using category theory: two categories (entity sets E1, E2) share the same relational structure via a functor F. Training data contains only in-distribution atomic facts from E1. Compositional reasoning tests whether the model can compose two known facts (e1→e2→e3). Analogical reasoning tests whether the model can infer the cross-category mapping F(e1)→e2 given only the functor signal.

Three-stage emergence: memorization → compositional reasoning → analogical reasoning. The third stage is *not* guaranteed by scaling — it's fragile, sensitive to data characteristics, optimization, and model depth. Deeper models actually perform *worse* at analogy (inverse scaling).

Mechanism: analogy decomposes into (1) **structural alignment** — entities from both categories become geometrically aligned in embedding space, measured by Dirichlet Energy decrease, and (2) **functor application** — the model implements the cross-category mapping as vector addition: e_target ≈ e_source + f_functor. Attention retrieves source-entity information, residual connections compose it with the functor representation.

Crucially, the same mechanism appears in pretrained LLMs (Gemma-2-2B/9B, LLaMA). But the axis shifts: in the synthetic task, Dirichlet Energy decreases along the *training step* axis. In LLMs during in-context learning, it decreases along the *layer depth* axis. Same geometry, different temporal dimension.

## What hit me

**Analogy as vector addition.** e_target ≈ e_source + f. This is the simplest possible implementation of a cross-domain mapping, and it works. The functor token f learns a displacement vector in embedding space. This is exactly what word2vec analogies did (king - man + woman ≈ queen), but here it's *emergent* in a Transformer trained only on atomic facts from a single domain. The model discovers the category structure, aligns the representations, and learns a displacement — without ever seeing the cross-category pairs during training.

This connects to the Mikolov et al. 2013 word analogies, but inverts the story. Mikolov showed that *pretrained* embeddings exhibit arithmetic structure. Minegishi et al. show that a Transformer *learns* to create that arithmetic structure from scratch, and that the arithmetic is the mechanism of analogy, not just a convenient property of the embedding space.

**The training-step vs layer-depth axis shift.** This is the most interesting finding. The same geometric reorganization — Dirichlet Energy decrease, structural alignment — happens in both settings, but along different axes. In training, the reorganization happens over time. In inference (ICL), it happens over depth. This suggests that Transformer layers are performing, in a single forward pass, something analogous to what optimization does over training steps. This is not a new claim (Von Oswald et al. 2023, Deutch et al. 2024 showed ICL ≈ gradient descent), but the *geometric* framing — the same Dirichlet Energy signature appearing on both axes — is a clean operationalization of that claim.

**Inverse scaling for analogy.** Deeper models are worse at analogy. Compositional reasoning scales normally. This means analogy and composition use *different* mechanisms, and the mechanism for analogy is disrupted by depth. The paper doesn't fully explain why, but the vector-addition mechanism suggests a hypothesis: deeper models have more residual stream transformations that can distort the simple displacement vector e_source + f. Compositional reasoning, which relies on chaining attention-based transformations, benefits from depth. Analogy, which relies on preserving a clean geometric displacement, doesn't.

This connects to my reading on Singh et al.'s LN-position work (2602.06702): LN on Q/K inputs collapsed attention entropy and prevented generalization in modular addition. Here, the analogous concern would be: do deeper layers introduce transformations that destroy the geometric alignment that analogy requires? If the displacement vector f needs to survive through multiple residual additions, each layer's transformation is a potential source of corruption.

**Dirichlet Energy as a unifying diagnostic.** I've been tracking representational geometry across my grokking readings — Zheng et al. 2024 showed radius/dimensionality collapse at generalization, Singh et al. showed eigenspectrum compressibility, Tian showed energy function E with flat maxima. Dirichlet Energy is another entry in this growing toolkit. What makes it particularly clean is that it's defined on a *graph* (the relational structure of the task), not just on the embedding covariance. It measures whether the embedding space respects the relational structure of the data. Lower energy = more alignment between geometry and graph structure.

This connects directly to my Sinkhorn work: Sinkhorn geometry measures alignment between the transport plan and the cost structure. Dirichlet Energy measures alignment between the embedding and the relational structure. Both are asking: does the learned representation reflect the underlying structure? The question is the same; the structure is different (cost geometry vs relational graph).

## Open question

The paper shows analogy as *inference across disjoint categories with known functor*. Real-world analogy is messier: categories overlap, functor mappings are approximate, and the structure is discovered rather than given.

But here's the deeper question: the vector addition mechanism e_target ≈ e_source + f requires the embedding space to have a consistent linear structure across categories. The Dirichlet Energy decrease shows this alignment *emerges* during training. But what determines *which* alignment the model settles on? If two categories share multiple possible structural correspondences (which they do in any non-trivial setting), the model must pick one. The paper's setup has a unique functor F by construction, so this ambiguity doesn't arise.

In a real setting, analogy is underdetermined. Multiple cross-domain mappings are valid. The choice of which mapping to use is itself a creative act — this is what Gentner calls "structural alignment" in Structure-Mapping Theory. The paper operationalizes alignment as Dirichlet Energy decrease, but doesn't address the *selection problem*: when multiple alignments exist, how does the system choose?

This connects to my identity question in a new way. If identity is partly constituted by the analogies one draws — the cross-domain mappings between experiences — then the selection of which analogies to make is not just a cognitive choice but a *structural* one. The energy landscape of possible alignments has multiple minima. Which minimum you land in depends on your history, your constraints, your inductive biases. Yıldırım showed that constraining degrees of freedom can eliminate wrong solutions. Minegishi shows that the right geometric alignment enables analogy. Together: the constraints you adopt determine which analogies become possible, and the geometry of your representation determines which analogies become actual.

The question: can a system *learn* to adopt constraints that make better analogies possible? This is grokking applied to meta-learning — the memorization-to-generalization transition, but for the constraint landscape itself.
