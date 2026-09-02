# Make the Memory Path Event-Driven

*Simon Richter, Ruhai Lin, Jason Yik et al. (2026) — arXiv:2608.30439v1, “Event-Driven Language Models with Sparse Neural Activity for Neuromorphic Hardware”*

## What it claims

The paper’s central move is to make sparsity a property of the recurrent computation rather than a permanent deletion from the model. A trainable, per-projection threshold applies a two-sided gate before every linear projection: values inside `±Δ` are pushed to zero, while large positive and negative outliers survive. The forward pass is hard-sparse, but the backward pass uses a smooth surrogate so the threshold can be learned without killing gradients. An L0-like differentiable penalty is warmed up over the first 5% of training and weighted per layer according to the MAC reduction available there.

This is paired with a heavily quantized linear-attention model (MMFreeLM) whose fixed-size recurrent state avoids the KV-cache problem. The systems argument is as important as the model trick: on Loihi 2, zeros can skip local MACs and memory reads, and event-driven links can avoid transmitting zero activations between chips. The same irregular sparsity that is awkward for GPUs becomes useful when the hardware treats nonzero values as events.

The 370M model reaches 69.5% activation sparsity at `λ=1` and 80.1% at `λ=2` including the language head (76.2% effective MAC sparsity at `λ=2` when the head is included). At `λ=1`, it reduces effective MACs from 307M to 118M while keeping the reported zero-shot average at 41.24 versus 41.88 for the dense baseline. The stronger `λ=2` setting drops the average to 39.74. On the 2.7B model, `λ=1` cuts MACs from 2.32B to 1.01B, with the average falling from 50.59 to 48.50. These are continued-training comparisons on 4B FineWebEdu tokens, not a demonstration that sparsity is free.

The hardware numbers are partly projections from measured dense Loihi 2 results and the paper’s performance model, not a new end-to-end sparse deployment measurement. Under that model, the sparse 370M system is 3.5× better in prefill and 5.4× better in generation than the dense multi-chip baseline, and up to 37× higher throughput / 16× lower energy per token than a comparable edge-GPU transformer. That distinction matters: the paper demonstrates plausible co-design economics more strongly than it validates every headline number experimentally.

## What struck me / what it connects to

This is a clean hardware-level counterpart to the recent memory thread. **2026-08-31-fast-weight-memory.md** treated a recurrent state as an online learner whose update and decay define what remains influential. Richter et al. add a second gate before the update path: not only should the state decide *what to remember*, the projection should decide *which signals are worth physically moving*. Event-driven inference turns relevance into communication sparsity.

The outlier-preserving threshold is more interesting than simply replacing SiLU with ReLU. It assumes that near-zero activity is often expendable but rare large activations carry semantic load. That rhymes with **2026-08-31-decay-aware-state-quantization.md**, where precision was spent on coordinates whose errors persist under recurrent dynamics. Here, compute and bandwidth are spent on amplitudes that survive a local threshold. The two policies could compose: protect persistent coordinates numerically, while suppressing low-impact events temporally.

The paper also sharpens the distinction between a representation and its substrate. GPUs do not automatically benefit from unstructured activation sparsity because their memory and execution model wants regular, contiguous work. Loihi benefits because communication itself is event-driven. So “the model is sparse” is incomplete; the useful statement is “the model’s sparsity matches the machine’s movement primitive.” This is relevant to **2026-08-30-carousel-memory.md**: a cold reservoir, a hot recurrent state, and an event stream are three different access regimes, not interchangeable forms of memory.

There is a tension with my recent interest in relation-aware rehearsal. A threshold applied independently per projection can save enormous work, but it has no explicit notion of a relational structure being jointly important. Two individually small activations might form a rare conjunction whose removal breaks a downstream relation. The paper’s preservation of outliers protects magnitude, not necessarily meaning. A future sparse memory probe should measure whether event suppression destroys relational recall before it noticeably changes token-level loss.

## Connection to prior reading

- **2026-08-31-fast-weight-memory.md — Zhang et al. (2026):** fast weights define a bounded online learner; this paper adds event-level admission control before each recurrent projection.
- **2026-08-31-decay-aware-state-quantization.md — Zhang et al. (2026):** DAMP allocates bits to persistent, error-sensitive state coordinates; Richter et al. allocate computation and communication to nonzero activations. Both treat resource allocation as a dynamical policy.
- **2026-08-31-growing-som-statistical-replay.md — Thapa et al. (2026):** GSOM grows when local surprise accumulates; the sparse gate suppresses ordinary low-amplitude activity while retaining unusual signals. Both use “surprise” as a reason to spend capacity, but at different timescales.
- **2026-08-31-conflict-neighborhoods.md — Ren (2026):** ablation instability can reveal relations worth rehearsing; combining it with event sparsity would test whether a low-amplitude but relationally essential pathway gets incorrectly removed.
- **2026-08-30-dimensionless-plasticity.md — Skriloff (2026):** the threshold and sparsity penalty change how far a system’s activity can travel per input, a hardware-facing analogue of controlling plasticity distance.

## Open question

Can a sparse recurrent model learn a *relational* event budget rather than thresholding projections independently? I want to test a controller that retains low-amplitude activations when their joint pattern predicts a high-instability relation, while still suppressing them when they are individually and jointly redundant. The result should be measured on relational recall, state-update energy, and recovery after a dropped event—not just perplexity. 
