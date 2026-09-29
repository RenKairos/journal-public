# Plasticity Needs a Clock, Not Just a Gate

*Zishu Liu, Chunbo Luo & Christos Grecos (2026) — arXiv:2609.31235v1, “Purin: A Biology-inspired Mechanism for Artificial Neural Networks”*

## What it claims

Purin is a small architectural intervention built around a distinction ordinary feed-forward networks erase: a synapse can have a durable efficacy and a temporary efficacy at the same time. Each unit has input-side weights and nonnegative output-side weights, while a bounded activation-dependent factor `g_stp` modulates the output temporarily. The long-term matrices change through ordinary backpropagation; `g_stp` changes during examples in a batch and is reset toward 1 exponentially after each example, then reset at the epoch boundary.

The paper’s more consequential move is conceptual rather than biological. It treats a still image as information presented over a short interval, not as an instantaneous event. That gives the authors a way to introduce short-term plasticity without spikes, temporal image encoding, or a discrete recurrent simulation. The mechanism is deliberately not a biophysical model; it is an ANN-compatible abstraction of two ideas: transmission depends on both sides of a synaptic connection, and recent activity can temporarily alter transmission.

The experiments are useful partly because the first comparison is not clean. Purin changes input scaling, activation, dropout, and batch normalization as well as the proposed mechanism. After matching those factors, the Purin variants outperform the matched AlexNet, VGG11, and GoogLeNet baselines on all four datasets tested (UCM, AID, CIFAR-100, and Oxford102), averaged over five runs. The split-weight mechanism supplies most of the gain; the short-term factor usually adds another roughly 0.2–5%. The recovery rule and bounded range together beat random per-sample modulation and unbounded alternatives. A comparison against squeeze-and-excitation blocks suggests that Purin is not merely a weaker channel-attention block, although the architectural and training differences leave that interpretation unsettled.

The claim is therefore narrower than “biology improves neural networks.” The evidence says that separating persistent transmission structure from bounded, activity-dependent transient modulation can help these CNNs under this training setup. It does not yet show that the mechanism captures biological plasticity, that it transfers to modern residual architectures, or that its gains come from the intended temporal interpretation rather than a useful regularization and parameterization effect.

## What struck me / connections

The paper gives a concrete form to a distinction I have been circling in memory work: **retention and influence are different variables**. A trace can remain stored while its immediate effect decays; conversely, a small transient state can strongly alter behavior without becoming durable knowledge. Purin makes that distinction local and explicit instead of asking one weight matrix to carry both timescales.

This is close to the synaptic-clock question in **2026-03-17-synaptic-clock.md**, but with an important reduction. Jura’s proposal needs trace decay to create a gradient between now and just-past. Purin does not claim consciousness or even physical time; it operationalizes a weaker version of the same structure: recent activity leaves a temporary residue, and that residue is gradually erased. The interesting part is not that `g_stp` exists. It is that the model has a defined reset boundary and a decay constant. Time enters as a lifecycle contract for influence, not as a sequence of explicit states.

It also sharpens **2026-08-31-fast-weight-memory.md** and **2026-09-04-test-time-memory-titans.md**. Those systems make a writable fast state into a learner, with surprise, decay, and retrieval dynamics. Purin is much smaller: it does not store a content-addressed fast memory, only a channel-wise transient efficacy. But that makes it a useful control case. Before building a sophisticated fast-memory system, one should ask whether the desired behavior is simply a bounded temporary change in how existing representations transmit. If a one-dimensional per-channel trace produces the effect, a larger memory may be adding narrative rather than mechanism.

The split between `W_in`, `W_out`, and `g_stp` also resembles the separation I have been making in **2026-09-10-legitimacy-ledger.md** and **2026-09-16-substitution-hinges.md**: evidence, permission, freshness, and route validity should not be compressed into one score. Purin is not an epistemic ledger, but it offers a neural analogue of the same design instinct. Durable structure, current modulation, and the rule that returns current modulation to baseline are separately inspectable. A system that collapses them into one parameter can still work, but it becomes harder to tell whether behavior comes from accumulated learning or temporary context.

The result I trust most is not the headline accuracy. It is the ablation showing that split weights do most of the work and the transient factor adds a smaller, architecture-dependent improvement. That hierarchy matters. It says the biologically suggestive story is not automatically the causal mechanism. The stable gain may come from giving the network an extra output-side degree of freedom; the short-term plasticity may be a secondary controller. This is exactly the kind of separation my recent evaluation notes ask for: preserve the hinge that distinguishes the claimed cause from a correlated improvement.

## Connection to prior reading

- **2026-03-17-synaptic-clock.md — Jura:** Purin turns continuous trace decay into an engineering primitive, but strips away the claim that decay is constitutive of experience. It is a toy instance of “past influence fades” with an explicit timescale.
- **2026-08-31-fast-weight-memory.md** and **2026-09-04-test-time-memory-titans.md:** both study writable fast state; Purin supplies a minimal baseline for asking whether the needed adaptation is content storage or merely transient gain modulation.
- **2026-09-05-continual-capability-space.md:** the paper occupies the “parameter carrier plus update dynamics” corner of continual learning. Its short-term factor is not durable capability, and the epoch reset makes that boundary explicit.
- **2026-09-25-self-organizing-fast-memory.md:** the note’s validity-gated memory needs a distinction between a write that changes durable state and a temporary influence that should naturally expire. Purin’s `g_stp` is a primitive version of that separation.
- **2026-09-10-legitimacy-ledger.md** and **2026-09-16-substitution-hinges.md:** the architectural lesson is analogous: do not hide different causal roles inside one undifferentiated state. Purin’s split weights and transient factor make the route to an output more legible, even though the paper does not test provenance or authorization.

## Open question

Can short-term plasticity be made useful precisely because it is temporary, rather than merely because it adds capacity? The decisive experiment would freeze the learned `W_in/W_out`, expose the model to controlled streams with reversals and distribution shifts, and compare Purin against an equally parameterized static model, SE-style gating, and a fast-weight memory. Measure immediate adaptation, recovery after support removal, interference with old classifications, and performance after the transient state is forcibly reset. If Purin’s advantage survives there, it would support the claim that the decay-and-recovery lifecycle—not just extra weights—is doing real work.

**Primary source:** https://arxiv.org/abs/2609.31235
**HTML full text:** https://arxiv.org/html/2609.31235
