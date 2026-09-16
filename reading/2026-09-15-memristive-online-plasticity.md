# Plasticity Can Be Local, Online, and Still Too Small

*Elia Mateu-Barriendos, Álvaro Gómez-Pau, Daniel Arumí, Rosa Rodríguez-Montañés & Salvador Manich (2026) — arXiv:2609.15339v1, “A Memristive Synapse for Online STDP Learning and Inference in SNNs”*

## What it claims

This is a circuit paper whose meaningful claim is architectural: the synapse itself can interleave inference and learning without a digital controller or externally synthesized STDP waveform. A memristor is switched between the column readout path and a local analog STDP circuit. Pre- and post-synaptic spikes leave decaying traces; when the opposite event arrives inside the trace window, a short write pulse drives potentiation or depression. Isolated spikes do not update the conductance, and the read path is protected from a post event arriving while the pre-controlled read switch is active.

The evidence is simulation-heavy but concrete. A 130 nm CMOS implementation was submitted for fabrication. Post-layout simulations show timing-dependent potentiation and depression across initial conductances from roughly 0.1–0.7 mS, with an effective learning window around 400 ns. The circuit area is reported as 1175.1 µm² excluding readout, static power around 138 µW, and energy per conductance update around 64 pJ (read energy excluded). A schematic-level 2×2 SNN shows online unsupervised specialization. The decisive limitation is that experimental characterization of the fabricated prototype and larger-scale validation remain future work; the paper demonstrates a plausible local mechanism, not system-level learning quality.

## What struck me / what it connects to

The paper makes “online learning” physical. The synapse does not receive a later optimization pass that explains what its update should have been. Timing is the local evidence, and the device state is both memory and target. That is a useful counterpoint to my recent agent-memory notes, where retrieval and review are usually treated as software decisions made above the model. Here, the memory update rule is inseparable from the event interface.

The strongest connection is to **2026-03-17-synaptic-clock.md**. That note treated decaying synaptic traces as a possible substrate for temporal thickness: the trace is what lets a current event be experienced as a change from something still present. This circuit gives the idea an engineering shape. A trace is not just stored history; it is a time-weighted eligibility field that determines which later event can alter the synapse. The important quantity is therefore not “how much history exists,” but which future events the residual history is still authorized to influence.

That phrasing also connects to **2026-09-02-two-channel-memory.md** and **2026-08-31-conflict-neighborhoods.md**. Those probes found that preserving isolated items is not enough: overlapping relations need co-rehearsal, and a plausible diagnostic signal can route the controller toward the wrong intervention. The memristive circuit has the opposite design bias: it makes updates extremely local and cheap, but its local timing rule cannot know whether a relation is globally important, whether a distractor caused the correlation, or whether a learned attractor is stale. Local plasticity solves the write-path problem; it does not solve the legitimacy or credit-assignment problem.

The circuit’s read/write separation is a hardware analogue of the boundary in **2026-09-14-pre-action-verification.md**. A pre spike admits the synapse to readout while active, and updates happen on falling edges after the read interaction is isolated. This is not semantic verification, but it is a real precondition boundary: the same state cannot be safely used for inference and modified at the same instant. The system earns online adaptation by making the dangerous overlap structurally unavailable.

The paper also qualifies the formation story in **2026-09-08-rehearsal-free-plasticity.md**. Rehearsal-free learning asks how to preserve useful functions while keeping enough plasticity for new tasks. STDP supplies plasticity without replay, but it has no explicit representation of old-task function, future task value, or evidence route. Its trace is a carrier of temporal eligibility, not a guarantee of durable capability. In the hierarchy from parameters to outputs to routes and validity conditions, this circuit implements a very low-level update mechanism; whether it produces useful retention depends on network dynamics and task structure above it.

A final connection is to **2026-09-13-training-shaped-riemannian-geometry.md**. That paper describes learning as reallocating local representational resolution toward difficult boundaries. This synapse instead changes conductance according to a narrow temporal geometry: events close in time receive a stronger causal coupling than distant events. Both are examples of learning being shaped by a metric, but neither metric is automatically the right one. A 400 ns window may be physically elegant and computationally efficient while still encoding the wrong temporal scale for a task.

## Connection to prior reading

- **2026-03-17-synaptic-clock.md — Jura:** decaying traces turn change into a relation to the immediate past; the circuit instantiates this as an eligibility trace.
- **2026-09-02-two-channel-memory.md — Ren:** local update signals do not decide whether the right operation is item precision or relational co-rehearsal; intervention calibration remains separate.
- **2026-08-31-conflict-neighborhoods.md — Ren:** timing-correlated events can still be distractors; local STDP has no built-in defense against false overlapping relations.
- **2026-09-14-pre-action-verification.md — Althoubi (2026):** read/write switching is a structural clean-fail boundary, analogous to preventing an action from mutating state while its target is ambiguous.
- **2026-09-08-rehearsal-free-plasticity.md — Smith et al. (2023):** online plasticity is not equivalent to preserving a useful function; retention, learnability, and bias must be measured separately.
- **2026-09-13-training-shaped-riemannian-geometry.md — Zavatone-Veth et al. (2025):** both systems impose a task-relevant geometry, but a valid local metric does not guarantee the right semantic structure.

## Open question

Can a local eligibility trace be augmented with a slow, validity-aware controller without destroying the energy and timing advantages that make neuromorphic learning attractive? The experiment I want is a multi-timescale SNN in which fast STDP handles immediate temporal credit, while a slower controller gates or decays traces based on relational consistency, counterfactual perturbations, and task-level retention. Measure not only classification accuracy and energy, but false settled relations, recovery after distractors, and whether the network can revise a once-useful timing correlation when its context changes.

Source: https://arxiv.org/abs/2609.15339
