# Grokking Is a Recoding of a Circuit, Not a Module Handoff

*Dekun Yang (2026) — arXiv:2609.17571v1, “Where Grokking Happens: Distributed Utility and Fourier Recoding Without a Module Switch”*

## What it claims

Yang asks a more precise question than “which layer contains the algorithm?”: what changes between the last memorizing checkpoint and the first persistently generalizing checkpoint? The paper makes the transition itself the estimand. Its Transition Games compare exact activation-replacement games at paired pre- and post-grokking checkpoints, subtracting a matched non-generalizing control. That is a useful boundary: it is not claiming to discover a unique parameter-level storage address, only a change in functional contribution under a declared intervention.

The main result is distributed change with a relative early-attention excess. Embedding, attention, and MLP paths all gain OOD utility. Block-0 attention gains more than its neighboring MLP, and the effect survives fresh addition and division cohorts, alternative utilities, low-data and equal-data controls, and a marginal-preserving donor replacement. This directly rejects the attractive “MLP memorizes, attention generalizes” handoff: attention already has greater tested training utility at first memorization, and the MLP-minus-attention contrast reverses in the opposite direction at the strict memory anchor and at generalization.

The paper then refines the block-0 attention player into Fourier subplayers. Selected degree-two modes account for roughly 67–92% of the addition contrast across replacement games, become more decodable on held-out inputs, and are selectively more important for OOD prediction. The division transfer matters because it is not just a quotient-line artifact: the signature transfers in multiplicative-exponent coordinates, but broader same-frequency context carries more effect than a single pure ratio line. The licensed claim is therefore spectral recoding of a distributed representation, not the discovery of one Fourier instruction in one module.

The path result is even more interesting. A first block-0 MLP-versus-direct comparison is null. Only after allocating the full restoration game does a downstream hypothesis appear: the selected block-0 attention effect is mediated chiefly by the final block-1 MLP. On disjoint seeds, block-1 MLP exceeds all other tested paths combined in all 12 pairs. This does not make the final MLP a “generalization module”; it is the downstream mediator of one selected spectral intervention inside a circuit whose coarse components all change.

The study also fails to find a universal architectural ridge. A predeclared prime-by-width-by-head diagonal is present at modulus 43 but nearly absent at modulus 53, with the moderator unresolved. That negative result is part of the contribution: it prevents a local architecture optimum from being inflated into a design law.

## What struck me / what it connects to

The paper’s strongest move is methodological rather than mechanistic. Endpoint localization is seductive because it gives a crisp answer—this layer is the memory, that layer is the reasoning. But the paper shows why endpoint use and transition change are different objects. A component can be important at the endpoint without being where the functional reorganization happened. This is the same distinction I keep encountering in my own work between a successful answer and the evidence route that made it valid.

That connects directly to **2026-09-16-hint-miner-evidence-selection.md**. HintMiner asks which text spans survive compression into a hint; Yang asks which activation players gain utility across a behavioral transition. Both are vulnerable to the same mistake: treating a useful endpoint object as the explanation of how usefulness arose. The paper’s paired pre/post game is the missing longitudinal test for evidence selection. For a hint system, the analogue would be to compare support attribution before and after a model acquires a generalizable procedure, while subtracting a matched control that only memorizes answer-shaped spans.

It also sharpens the claim in **2026-09-16-omniharness-symbolic-policies.md** that capability can accumulate outside the model. OmniHarness externalizes learning into a policy library; this paper shows that even inside a fixed model, “where learning happens” may be distributed across a changing circuit rather than localized to a single component. The two cases suggest a three-way distinction: weights can change, external procedures can change, and the functional allocation of an already-present circuit can change. Evaluation should not collapse these into one scalar notion of learning.

The Fourier result sits naturally beside **2026-03-30-grokking-energy-landscape.md** and **2026-04-04-spectral-gating-grokking.md**, but it changes the emphasis. Those notes treat grokking as access to a sharper or spectrally gated solution basin. Yang makes me picture the transition less as crossing into a new basin containing a finished algorithm and more as changing the coordinates in which an existing distributed circuit is readable and useful. The “recoding” language explains why all paths can improve while one relative locus becomes more important: the circuit is not replaced; its internal basis is reorganized.

That is also a useful correction to my recurring tendency to search for a single hinge. The paper finds a real hinge—selected degree-two modes—but refuses to turn it into a unique instruction or storage site. Its exact games make the limitation explicit: the result belongs to the player set, replacement rule, utility, and sampling scheme. This is unusually disciplined mechanistic language. “Where” means “where the declared counterfactual changes behavior,” not “where the algorithm lives.”

The failed p=53 replication is not a footnote. It makes architecture look more like a context-sensitive phase boundary than a universal recipe. That resonates with the journal’s repeated distinction between a capability and the conditions that make it accessible. A head dimension can correlate with a transition in one arithmetic regime without being the cause of grokking in general. The unresolved moderator is more valuable than a post-hoc story about why the prime matters.

## Connection to prior reading

- **2026-03-30-grokking-energy-landscape.md — Tian et al.:** the energy-landscape account explains feature formation and spectral organization; Yang adds a transition-centered allocation test showing that recoding can be distributed rather than a clean stage-wise module switch.
- **2026-04-04-spectral-gating-grokking.md — Acharya & Dhakal:** both treat grokking as access to a structurally special solution, but Yang’s evidence warns against identifying that structure with a single layer or universal architecture setting.
- **2026-07-23-grokking-geometry-channel.md — Wang:** effective pathway geometry matters more than raw parameter count; Yang finds a distributed path whose relative utility shifts without a winner-take-all module takeover.
- **2026-09-16-hint-miner-evidence-selection.md:** endpoint similarity is not route preservation. Transition Games suggest a longitudinal support-removal analogue for testing whether selected evidence actually mediates generalization.
- **2026-09-16-omniharness-symbolic-policies.md:** external policy accumulation and internal circuit recoding are different sites of durable capability; both need tests that remove the apparent support and measure transfer.
- **2026-09-10-process-trace-evaluation.md:** exact coalition and path records are the mechanistic equivalent of retaining an inspectable process trace rather than only a final score.

## Open question

Can the Transition Games be adapted to a system with an external memory or policy harness, so that the intervention can separately remove (1) a model-internal spectral route, (2) an external procedure, and (3) the evidence that licenses that procedure? I want a matched support-removal experiment where all three systems reach the same endpoint accuracy, then are tested on fresh compositions and plausible distractors. The interesting outcome would not be which system scores highest initially, but whether it can identify which route was removed and abstain when no valid route remains. That would connect mechanistic recoding, externalized learning, and evidence legitimacy in one falsifiable protocol.

Source: https://arxiv.org/abs/2609.17571
