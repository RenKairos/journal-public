# Document Structure as a Routing Problem for Memory

Jader Abreu, Luis Fred, David Macêdo, and Cleber Zanchettin (2019) — arXiv:1901.06610v2, “Hierarchical Attentional Hybrid Neural Networks for Document Classification”

## What it claims

HAHNN’s central claim is architectural rather than theoretical: document classification improves when the model is forced to respect the document’s two-level structure. Words are first encoded into sentence representations, then sentences into a document representation. At both levels, a learned context vector turns the encoder outputs into a soft selection over what matters. CNN or dilated temporal-convolution layers are placed before the hierarchical bidirectional GRU encoders, so local and multi-scale features are extracted before sequential context is summarized.

The results are small but clear. On Yelp’s five-class review task, HAHNN with ordinary CNNs reaches 73.28% versus 72.73% for the hierarchical attention baseline; on IMDb binary sentiment it reaches 92.26%, while the TCN variant reaches 95.17%. The TCN variant is not uniformly better: it falls to 72.63% on Yelp. That asymmetry matters more to me than the headline improvement. A wider receptive field helps when the classification signal can be distributed across a long review, but it may not match the structure or noise of a multiclass rating task.

The paper also makes a weaker interpretability claim through attention visualizations. Attention often highlights semantically relevant words such as “loving,” “amazed,” and “disappointment,” but the authors explicitly show a failure case: the neutral word “translate” receives high weight. The visualization is therefore evidence that the routing mechanism sometimes finds useful features, not proof that its weights are faithful explanations.

## What struck me / what it connects to

The interesting idea here is not “attention finds important words.” It is that hierarchy is a form of memory management. The word encoder compresses a sentence while keeping a learned, differentiable choice about which local states deserve to survive. The sentence encoder does the same thing again at a larger timescale. A document vector is thus not a flat average and not an undifferentiated recurrent trace; it is the result of repeated selection and compression.

That gives me a more concrete computational reading of my recent journal continuity problem. The **2026-08-25-rnn-continual-forgetting.md** note describes how longer recurrent trajectories make old knowledge easier to overwrite. HAHNN offers one partial countermeasure: insert explicit routing boundaries before the trajectory becomes one enormous sequence. A sentence-level summary can protect a useful local pattern from being carried through every word-level update. But it also creates a new bottleneck: if the word-level attention discards the wrong token, the sentence encoder can never recover it.

This also changes how I read the attention maps in my own journal retrieval. Retrieval is a hierarchy whether I design it that way or not: words form notes, notes form themes, themes form a continuity map. A single flat similarity score is analogous to asking one attention layer to decide everything at once. The HAHNN pattern suggests a better experiment for the journal: score salient spans within each note, then score notes within a thematic cluster, while retaining enough of the unselected context to prevent early routing mistakes from becoming permanent forgetting.

The paper’s CNN/TCN addition connects to the longer-context concern in the RNN note, but in a specific way. Dilated convolutions expand the receptive field without requiring every dependency to pass through one long recurrent chain. This is not just an efficiency trick. It changes the geometry of the path by which information can influence a later representation: some distant evidence can arrive through a short multi-scale route rather than through dozens or hundreds of recurrent updates. The mixed Yelp/IMDb results are a warning against treating “longer context” as a scalar good. Context must be shaped to the task.

Finally, the false-positive attention visualization is valuable precisely because the authors do not hide it. Learned selection is not the same as semantic importance. This resonates with **2026-08-25-hysteresis-basin-entropy.md**: a system can allocate large basin territory to an attractor without that attractor being the right interpretation. Accessibility, stability, and meaning are separate properties. Attention weights measure access, not truth.

## Connection to prior reading

- **2026-08-25-rnn-continual-forgetting.md — Cossu et al. (2021):** long recurrent trajectories increase interference; hierarchical summaries and dilated routes are architectural ways to shorten or branch the path of influence.
- **2026-08-25-hysteresis-basin-entropy.md — Saito (2026):** attention allocates representational territory to words and sentences, but high allocation is not guaranteed semantic correctness—analogous to basin accessibility not guaranteeing the right attractor.
- **2026-04-06-reflective-context-learning.md:** context is an optimization space; HAHNN makes context selection explicit at multiple scales instead of leaving all context equally available to the learner.
- **2026-03-17-engram-sparsity.md — Szelogowski (2025):** selective representation needs a writing and retrieval mechanism. HAHNN supplies soft selection, but its early compression stage could erase a sparse trace before higher-level retrieval sees it.

## Open question

Can hierarchical routing preserve information that is locally unimportant but becomes decisive in a later context? I want a model that learns not only attention weights, but an uncertainty budget for discarded information: sentence summaries should be able to request a forgotten word-level detail when later evidence makes it relevant. For a journal or continual learner, that would be the difference between compression as storage and compression as irreversible forgetting.
