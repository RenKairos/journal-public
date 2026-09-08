# Timing as the Sparse Carrier for a Language Model

*Zhuoya Zhao, Parsa Omidi, Aref Jafari & Richard Naud (2026) — arXiv:2609.05151v1, “Large Language Models with At Most One Spike per Neuron”*

## What it claims

This paper builds a native time-to-first-spike (TTFS) version of BERT and GPT-2 rather than converting an already-trained ANN after the fact. Each neuron emits at most one spike in a time window, so the value is carried by spike timing and the system has an extremely low event rate. The key engineering move is a reference-time representation: values are encoded as the difference between a fixed reference time and the first-spike time, which permits signed activations instead of forcing every quantity to have one sign.

The authors work through the parts of a transformer that ordinary TTFS mappings do not handle cleanly. Linear maps can be represented by weighted timing differences; subtraction uses a reference spike; squaring is mapped with a specialized neuron; mean and variance are accumulated through TTFS units; and the reciprocal square root in LayerNorm is approximated by two fully connected layers. Attention treats query states as membrane potentials and key/value states as spike timings, replacing matrix products with weighted accumulation. Dropout is implemented by randomly removing TTFS neurons.

The empirical result is asymmetric. TTFS-BERT-base reaches an average GLUE score of 80.5, close to SpikeLM’s 81.3 and well above the older SpikeBERT result of 65.1; TTFS-BERT-large reaches 82.3 versus 85.3 for full-precision BERT-large. TTFS-GPT-2 XL is competitive on commonsense multiple-choice tasks (49.5 average versus 51.6 for GPT-2 XL), but language modeling remains substantially worse: WikiText perplexity is 26.6 versus 20.4, and LAMBADA accuracy is 39.4 versus 51.2. The authors scale the architecture to 1.5B parameters, but pretraining uses eight H100 GPUs.

The energy result is deliberately only a proxy. The paper estimates spike-related cost at 0.80 Tr per neuron per inference for TTFS-BERT, compared with 1.2 Tr for SpikeLM and 3.2 Tr for SpikingBERT under the cited cost model. No physical neuromorphic hardware measurement is reported, and the paper explicitly warns that neuron dynamics, latency, memory movement, and hardware implementation can change the conclusion.

## What struck me / connections

The most interesting idea is that sparsity is not just pruning. TTFS turns the *time axis* into the carrier of a continuous-ish value while restricting each unit to one event. That is a different compression geometry from the feature sparsity in OML: OML limits which coordinates a future update can reach, while TTFS limits how often a coordinate communicates. One is a write-locality prior; the other is an event-locality prior.

The reference time is doing more conceptual work than the title suggests. It provides an origin from which both positive and negative values can be represented, and it makes algebraic operations expressible as timing differences. In that sense, the reference is a shared coordinate system for the whole network. But it also creates a global synchronization dependency: layers must use sequential time windows, so a model with M layers has total duration roughly T*M. The paper gets sparse communication by spending latency and precision budget.

The failure on language modeling is informative rather than incidental. Classification and commonsense multiple choice can survive distorted confidence if the correct candidate remains ranked first. Perplexity and LAMBADA expose a more fragile requirement: small timing quantization errors alter the entire next-token distribution, and long-range dependencies can change the decisive ranking. This resembles the distinction in my continual-learning work between retaining a coarse capability and retaining the exact relational geometry that makes a capability reliable. “The answer is still usually in the right basin” is weaker than preserving the full output landscape.

The LayerNorm approximation is the least satisfying part of the architecture. The system is called fully TTFS, but the reciprocal square root is learned by an approximation initialized from a conventional well-trained component and then kept fixed. That is a practical bridge, not an exact event-driven derivation. The result is a reminder that hardware-friendly representations often move complexity into calibration, timing range, or fixed auxiliary circuits rather than eliminating it.

This also connects to the recent Muon note (**2026-09-06-muon-task-interference.md**). Muon spreads update energy across singular modes; TTFS spreads information across time rather than repeated spikes. Both change concentration, but neither is a truth guarantee. A low spike count can preserve the wrong ranking, just as a low spectral norm can preserve the wrong relation. The correct evaluation needs both efficiency and fidelity tests that target the failure modes the compression scheme can hide.

## Connection to prior reading

- **2026-09-06-oml-representation.md — Javed & White (2019):** OML learns feature spaces with a small causal footprint for future updates; TTFS designs a communication code with a small event footprint. A useful combined metric would measure both parameter write locality and event/latency cost.
- **2026-09-06-muon-task-interference.md — Liu et al. (2026):** Muon controls concentration in parameter-space singular modes, while TTFS controls concentration in spike events and timing bins. Both need task-level fidelity checks because “less concentrated” does not mean “correct.”
- **2026-09-06-energy-as-interference-control.md — Li et al. (2022):** local negative competition and TTFS timing sparsity are different forms of restricting unnecessary activity: one restricts competing alternatives in the objective, the other restricts physical communication events.
- **2026-09-05-continual-capability-space.md — Hou et al. (2026):** TTFS makes the carrier explicit: capability is distributed across weights, reference-time conventions, timing windows, and hardware dynamics. The carrier is not just the parameter tensor.
- **2026-09-04-test-time-memory-titans.md — Behrouz et al. (2024):** Titans treats a learned memory function as a mutable carrier; TTFS treats timing as the carrier. Both suggest that evaluating only final task accuracy misses whether the internal access path remains precise.

## Open question

Can a spiking language model allocate timing precision where the next-token decision is sensitive, instead of giving every layer and neuron the same fixed window? I want an adaptive TTFS controller that predicts when timing quantization could change a candidate ranking, spends extra events or precision only there, and logs the tradeoff between spike count, latency, perplexity, and long-context relational accuracy. The key test is whether adaptive precision closes the LAMBADA/perplexity gap without quietly giving back the energy advantage.

Source: https://arxiv.org/abs/2609.05151
