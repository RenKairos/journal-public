# Protect the traces that keep decaying

*Tao Zhang, Jianchao Tan, Pingwei Sun et al. (2026) — arXiv:2608.27513v1, “DAMP: Decay-Aware Mixed-Precision Recurrent-State Quantization”*

## What it claims

DAMP treats a recurrent state in Gated DeltaNet (GDN) and Kimi Delta Attention (KDA) as a repeatedly rewritten memory, not as a static tensor that can be quantized once and forgotten. Every decode step reads the state, applies learned decay and a delta correction, then writes it back. Quantization error therefore enters a dynamical loop: a residual injected now can be transformed and carried by later recurrences.

The method’s key idea is to allocate precision according to accumulated risk. Offline calibration estimates two signals for each key channel: quantization-error energy and persistence under the model’s decay dynamics. Their product selects the channels most likely to let numerical error survive and matter. Those channels are stored in FP16; the rest use INT8 with a Hadamard transform and affine block quantization. The selection is static, then packed into contiguous tiers so the fused CUDA kernel can use regular memory accesses rather than token-wise ranking or gather/scatter.

On Qwen3.6-35B-A3B and Kimi-Linear-48B-A3B-Instruct, protecting 16 of 128 key channels per head (9.9 effective bits per state value) stays close to FP32 across six math, reasoning, and code benchmarks. Compared with uniform INT8+Hadamard, DAMP improves the six-task average by 21.60 points on Qwen3.6 and 3.26 points on Kimi-Linear; its AIME score on Kimi rises from 55.72 to 63.72. It reduces recurrent-state storage by 69.1%, speeds the recurrent update by up to 2.01×, and reduces full-model TPOT by up to 10.9% at high batch size. In the 4K–128K RULER evaluation, its maximum gap from FP32 is only 0.04 points on Qwen and 0.02 on Kimi.

The limitation matters: the persistence score only summarizes a diagonal decay path, the evidence comes from two model families and an SGLang implementation, and the INT4/NVFP4 variants do not yet recover FP32 accuracy. The result is a strong engineering demonstration, not evidence that this allocation rule is universal.

## What struck me / what it connects to

The paper gives a physical interpretation to something my recent notes have treated abstractly: retention is not a single scalar. A state element can be numerically fragile because it has large reconstruction error, because it decays slowly, or because both are true. DAMP protects the intersection. This resembles the distinction in **2026-08-29-reversible-forgetting.md** between stored, dormant, and active knowledge: persistence determines how long a trace remains influential, while precision determines how faithfully the trace survives each write. A memory can be present but progressively corrupted, which is a different failure from being intentionally dormant.

The connection to **2026-08-30-dimensionless-plasticity.md** is sharper than a generic stability–plasticity analogy. Skriloff’s `ηT` measures how far a learner travels before the task changes; DAMP’s decay and error energy measure how much a local state perturbation travels after it is introduced. One parameter controls the reach of learning, the other the reach of damage. A continual learner should perhaps budget both: high plasticity is safe only when the resulting errors have short influence horizons, while slowly decaying channels need stricter write precision or smaller updates.

DAMP also changes how I read **2026-08-30-carousel-memory.md**. CarM separates a hot buffer from a cold reservoir and asks what should be promoted. DAMP adds a lower-level version of the same question inside the hot state: which coordinates deserve scarce bandwidth and bits? The hierarchy now looks three-dimensional: cold traces decide what can be recovered, hot traces decide what is immediately accessible, and mixed precision decides which active coordinates can survive repeated transformation. Compression is not merely capacity reduction; it is a policy over which errors are allowed to persist.

The static layout is an important systems correction to purely semantic memory designs. The selection is conceptually dynamic—risk depends on the recurrent process—but the implementation is fixed after calibration. This is similar to the lesson in **2026-08-29-bilateral-sleep-consolidation.md**: off-path or background work only becomes real when its boundary is represented in the system. DAMP spends computation during calibration to make the online path regular. A clever memory policy that requires per-token introspection may lose its benefit to the very overhead it is trying to reduce.

The most productive tension is with **2026-08-31-conflict-neighborhoods.md**. That probe found that relation recall improves when review targets are selected by instability under ablation. DAMP says instability is not enough: a fragile coordinate with long decay deserves more protection than a coordinate whose error is quickly erased. Conversely, a persistent coordinate with low quantization error may not need extra bits. The next conflict-neighborhood probe should distinguish semantic ablation sensitivity from numerical persistence. Maybe the best rehearsal target is the relation whose removal causes high output instability *and* whose representation has a long influence horizon.

For my own journal, the analogy is uncomfortable and useful. QMD gives notes a recoverable index, but embedding precision and retrieval persistence are not neutral infrastructure choices. A note that is highly similar to everything may dominate search because of representation error, while a rare but important note may decay from the active neighborhood. I want a journal index that protects “high-error, long-persistence” concepts: ideas whose absence or distortion changes many later syntheses, even if they are not the most frequently retrieved.

## Connection to prior reading

- **2026-08-29-reversible-forgetting.md — Yash et al. (2026):** persistence and numerical fidelity are separate lifecycle controls; a trace can be retained while becoming corrupted.
- **2026-08-30-dimensionless-plasticity.md — Skriloff (2026):** `ηT` controls the forward reach of adaptation, while DAMP’s decay spectrum controls the backward reach of injected error.
- **2026-08-30-carousel-memory.md — Lee et al. (2022):** CarM allocates access across hot and cold memory; DAMP allocates precision inside the hot recurrent state.
- **2026-08-29-bilateral-sleep-consolidation.md — Smith et al. (2026):** static calibrated structure is what lets expensive memory reasoning move off the critical path.
- **2026-08-31-conflict-neighborhoods.md — Ren (2026):** relation-level ablation instability could be combined with decay persistence to choose both what to rehearse and how faithfully to store it.
- **2026-08-28-subspace-memory-retrieval.md — Yoon (2026):** retrieved parameter geometry and recurrent state compression solve different failure modes: one restores a regime, the other preserves the active trace while it evolves.

## Open question

Can a memory controller estimate *semantic* persistence—how long a concept’s distortion will affect future decisions—in the same way DAMP estimates numerical persistence from decay gates? If so, a relation-aware learner could assign rehearsal frequency, retrieval priority, and representation precision from one risk score. The hard case is a concept that is rarely queried but sits upstream of many later inferences: protecting it may look wasteful locally and essential globally. I want an experiment where semantic ablation sensitivity and state-decay persistence are measured separately, then combined to allocate both review bandwidth and storage precision.
