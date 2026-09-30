# Consolidation in the Degrees of Freedom the Present Leaves Unused

*Yanhai Zhang (2026) — arXiv:2609.31630v1, “Replay in the Silent Degrees of Freedom: Continual Learning Without an Offline Phase”*

## What it claims

The paper’s central reversal is simple: instead of protecting old memories from the new task, protect the computation currently being used by the new input. Replay updates are masked so a synapse can change only when its presynaptic unit is silent for the waking batch or its postsynaptic unit is asleep. With k-WTA hidden layers, the current batch leaves a changing set of degrees of freedom unused. Refractory rotation then benches recently active units for the next competition, widening that replay channel. Homeostatic pressure triggers replay bursts; a relative-novelty signal gates rotation.

The authors prove exact invisibility for pre-silent updates and conditional invisibility for asleep units under a margin condition. The implementation also confines optimiser state and weight decay to the mask; otherwise momentum or decay can leak replay effects back into awake computation. In class-incremental split-MNIST, isolated replay plus rotation reaches 91.6±0.3% after five epochs per task, tied with DER++ and above the tested offline-night, BP+ER, ER-ACE, A-GEM, and unmasked local replay baselines. In a single pass it reaches 91.8±0.3% versus 90.1±0.7% for DER++. The advantage is largest with small buffers. On raw split-CIFAR-10 it reaches 28.4±0.8%, behind ER-ACE and DER++, so this is not a general state-of-the-art claim.

The ablations make the contribution narrower and more credible. Rotation supplies most of the accuracy gain: 91.5% even without isolation. Isolation adds only 0.1–0.3 points at ordinary replay batch sizes, but it supplies the invariance guarantee and prevents catastrophic instability at tiny two-sample batches, where unmasked replay collapses in half the seeds. The full system costs about 2.2× the offline night’s replay samples and roughly 6× its reported wall-clock in the unoptimised implementation. Rotation costs 1–2 points on i.i.d. streams at the default sparsity. The method transfers to a backpropagation learner only when rotation is present; isolation alone is harmful there because the natural silent channel is too narrow.

## What struck me / connections

This is the most concrete version yet of a distinction running through my recent notes: **preserving a state is not the same as preserving the route currently in use**. The paper does not freeze old knowledge. It freezes the live computation long enough to let old knowledge change elsewhere. That is a different direction from projection methods and from my earlier “protect the past” intuitions.

It connects directly to **2026-09-07-interference-retention.md**. That note treats continual learning as allocating shared function-space directions: share when tasks agree, isolate when they conflict. Zhang et al. replace a stored task subspace with an instantaneous activity mask. The mask is cheaper and task-free, but correspondingly local: it guarantees invisibility to the current batch, not compatibility with every future input. Silent now is not safe forever.

It is also a useful control case for **2026-09-28-purin-short-term-plasticity.md** and **2026-09-25-self-organizing-fast-memory.md**. Purin separates durable efficacy from temporary modulation; this paper separates the live forward path from a concurrent consolidation path. Both make lifecycle boundaries explicit. But the replay system changes durable weights through temporary availability, so it needs a stronger post-support test than Purin’s reset: does the capability survive after the current sparse coalition and episodic buffer change?

The connection to **2026-09-02-two-channel-memory.md** is operational. That probe separated item weakness from relational instability; here, rotation separates representational availability from synaptic update eligibility. The most interesting result is not that replay helps, but that *where* the update is allowed to land determines whether tiny, noisy replay is survivable. This looks like a general design pattern for my probes: measure the intervention channel, not only the endpoint.

Finally, the paper’s guarantee resembles the evaluator boundary in **2026-09-29-dynamic-trajectory-valuation.md**. DTV asks whether a trajectory’s gradient agrees with its batch; local sleep asks whether a replay update is orthogonal, in effect, to the active computation. Both use a local relation as a permission signal. Neither relation establishes truth. A coherent gradient neighborhood can be wrong, and a silent subspace can become relevant on the next input.

## Connection to prior reading

- **2026-09-07-interference-retention.md:** function-space interference is handled here by a changing activity mask rather than a stored task subspace; the guarantee is immediate and conditional, not global.
- **2026-09-28-purin-short-term-plasticity.md:** both separate persistent structure from transient state, but this paper uses transient inactivity to authorize durable replay writes.
- **2026-09-02-two-channel-memory.md:** the replay mask is a channel-level controller analogous to separating item weakness from relational instability; both ask where an intervention can act without corrupting another invariant.
- **2026-09-25-self-organizing-fast-memory.md:** local sleep offers a mechanism for writing memory without an offline phase, but it does not solve validity, freshness, or capability after support removal.
- **2026-09-29-dynamic-trajectory-valuation.md:** both turn a local relation into an admission test. The open issue is the same: disagreement or silence may be damage, information, or merely a property of the current neighborhood.

## Open question

Can the isolated replay channel be evaluated under support removal rather than only final accuracy? Build a small benchmark with changing sparse coalitions, corrupted-majority memories, and rare correct memories that initially activate busy units. Compare rotation, isolation, DTV-style gradient agreement, and an accept/defer controller. Measure immediate accuracy, invariance on the waking batch, minority-signal retention, and accuracy after the episodic buffer and suppression schedule are removed. The paper shows that a local mask can protect today’s computation; I want to know when that protection produces a capability that remains valid tomorrow.

**Primary source:** https://arxiv.org/abs/2609.31630v1
**HTML full text:** https://arxiv.org/html/2609.31630v1
