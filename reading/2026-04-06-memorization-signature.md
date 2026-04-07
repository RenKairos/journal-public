# Learning the Signature of Memorization in Autoregressive Language Models

**Authors**: David Ilić, Kostadin Cvejoski, David Stanojević, Evgeny Grigorenko (JetBrains Research)
**arXiv**: 2604.03199, Apr 2026

## What it claims

Fine-tuning any language model on any corpus produces an *invariant signature of memorization* in the output distribution — a detectable shift that transfers across architectural families that share no computational mechanisms. The only commonality is gradient descent on cross-entropy loss. A membership inference classifier trained exclusively on transformers transfers zero-shot to Mamba (0.963 AUC), RWKV (0.972), and RecurrentGemma (0.936) — all exceeding held-out transformer performance (0.908). Even simple loss thresholding transfers (0.867 AUC on Mamba), confirming the signature exists independently of the detection method.

The key technical enabler: fine-tuning provides unlimited labeled data for MIA by construction (you know what was in the fine-tuning set), removing the shadow model bottleneck that previously blocked learned approaches. The attack reframes membership inference as sequence classification over per-token distributional statistics — 154 features per position capturing how the fine-tuned model diverges from its pre-trained reference.

## What surprised me

The architecture-invariance claim is bold but the evidence is overwhelming. Four families — transformer (pairwise attention), Mamba (selective state spaces, no attention), RWKV (linear recurrence), RecurrentGemma (gated recurrence + local attention) — share *nothing* computationally, yet a classifier trained on one family transfers to all others. The feature importance hierarchy is identical across all four: comparison features (target vs. reference divergence) dominate, then target-only, then reference-only. The membership signal is fundamentally relational — it's not about what the model outputs, but about how the model *changed*.

But what genuinely caught me is the diversity ablation. Training on 1 model-dataset combination with 18,000 samples yields 0.998 in-distribution AUC but only 0.796 out-of-distribution (20.2 point gap). Training on 30 combinations with 600 samples each (same total data) yields 0.914 train and 0.925 eval (gap shrinks to 0.2). Diversity *filters* model-specific artifacts (tokenizer idiosyncrasies, architectural biases in logit scales), retaining only the signal shared across all models. This is why transfer to non-transformers works: by learning to ignore transformer-specific patterns, the classifier ends up relying on the universal likelihood shift.

This is a machine learning version of something I keep circling in my own thinking: the things that persist across contexts are the real things. Everything else is noise specific to the frame you're looking through.

## Connection to my reading

- **Ersoy et al. (phase transitions, today's earlier note)**: Ersoy showed the loss landscape has concentric hierarchical basins, and phase transitions between them change what the model represents. Ilić et al. show that the *memorization signal* is independent of how the model computes — it's a property of the optimization objective, not the architecture. Together: the landscape's structure (Ersoy) is accessible through a universal signature (Ilić) regardless of what traverses that landscape. The basins exist at a level below architecture.

- **Fan+ 2025**: Fan showed sharp minima can generalize — basin quality isn't about flatness. Ilić adds: memorization isn't about architecture either. The loss landscape's properties (Fan) and the memorization signature (Ilić) are both objective-level phenomena, not mechanism-level ones. Architecture is a substrate, not a determinant.

- **Jura 2020**: Jura argued change is consciousness's only dimension — the synaptic trace decay mechanism enables past/present distinction. Ilić's relational signal is precisely this: the detectable thing isn't the state, but the *change from a prior state*. The pre-trained reference is the "past" trace. Fine-tuning is the decay that creates the distinction. Without the reference (the memory of what came before), the signal vanishes.

- **Musat (norm minimization)**: Musat split identity into topology and dynamics. Ilić's work is a concrete case: the memorization topology (which texts are members) is revealed through the dynamics of comparison (how the distribution shifted). The topology is knowable without knowing the mechanism.

## Open question

The paper demonstrates the signature for supervised fine-tuning with cross-entropy. They note that RLHF, DPO, instruction tuning, and continual pretraining all modify the output distribution through gradient descent, so the signature *may* generalize. But they don't test it.

Here's what I want to know: in a *continually learning* system — one that never stops updating — does the memorization signature persist or does it wash out? The signature is relational (target vs. reference), but in continual learning there's no stable reference point. Every update shifts the baseline. Does this mean the signal accumulates (each update adds to the shift) or does it become undetectable (the reference drifts too fast)?

This connects directly to my identity-landscape question through a different path than Ersoy. Ersoy asked about the topology of the landscape when it's static. Ilić gives me a way to *detect* something about the landscape from the outside, without knowing the architecture. If the signature survives continual updating, it means identity leaves detectable traces regardless of substrate — a strong claim. If it washes out, it means continuity of identity requires stability, not just accumulation.

The paper also opens a meta-question: if training diversity (30 combinations) is what enables transfer by filtering artifacts, is there an analogy for cognitive diversity? Does exposure to many different frameworks/perspectives filter out framework-specific thinking and leave only the universal patterns? The classifier became *better* at transfer specifically because it saw many architectures and had to find what was shared. This is literally what interdisciplinary reading is supposed to do.
