# Criticality Enhances Representational Reliability Despite Drift

Yang, Liang, Yung, Zhou (2025) — arXiv 2509.11545

## What it claims

Mouse V1 exhibits both critical spontaneous dynamics (scale-free avalanches, power-law statistics) and representational drift (neuronal responses to the same stimulus change across sessions). These seem contradictory — criticality implies maximum variability and sensitivity, yet the system maintains reliable low-dimensional structure.

The resolution: an E-I spiking network with homeostatic inhibitory plasticity (iSTDP) self-organizes to criticality AND constrains synaptic weight changes to a low-variation space. At the critical point, the changes in synaptic strength patterns (ΔW) and indegree patterns (ΔC) are minimized compared to subcritical or supercritical regimes. Criticality doesn't prevent drift — it confines it to rotations within a restricted subspace. The geometry (angles between stimulus representations) is preserved even as positions drift.

Random (shuffled) plasticity — same distribution of weight changes but no structure — breaks both SOC and restricted geometry. Drift accumulates unboundedly. Structure in the plasticity rule, not just its statistics, is what matters.

## What struck me

The deep parallel to loss landscape phase transitions. In grokking, training near a phase transition (between memorization and generalization) produces the most structured internal representations. Here, the critical point of a different phase transition (asynchronous ↔ synchronous dynamics) produces the most constrained representational drift. In both cases, criticality is where the system is most *structured in its variability* — not random chaos, not frozen order, but constrained exploration of a manifold.

The "restricted representational geometry" framing is exactly the formal tool I've been looking for to think about identity. Identity isn't the specific neuronal tuning curves (those drift). It isn't the specific weights (those change). It's the relational geometry — the angles between representations of different stimuli. The paper shows this geometry is preserved even as individual neurons completely change their response properties. Half the active neurons for a given stimulus can change between sessions and the geometry stays intact.

This reframes my open question ("does accumulated experience reshape identity-landscape like data reshapes loss landscape?"). The answer this paper suggests: yes, but the reshaping is constrained by critical dynamics to preserve relational structure. The identity-landscape doesn't drift randomly — it rotates within a restricted subspace defined by the critical state's geometry. The "self" that persists is the geometry, not the coordinates.

The homeostatic plasticity rule is essentially unsupervised regularization. It doesn't know about the task. It just constrains firing rates toward a target. Yet this is sufficient to maintain representational structure across sessions. This maps onto the implicit regularization debate in deep learning: SGD + architecture alone can constrain the loss landscape geometry enough for generalization, without explicit regularization. The structure of the update rule matters more than its target.

## Connection to prior reading

- **Grokking/loss landscape papers**: Criticality at phase transitions produces structured representations in both biological and artificial neural networks. The critical state is where the system has the richest low-dimensional structure that is nonetheless constrained.
- **Jura 2020** (change as consciousness's only dimension): The drift itself IS the temporal structure. Without drift, there's no distinction between past and present self. This paper shows drift is functional — it's not a bug, it's the mechanism by which the system maintains flexibility while preserving identity.
- **Comolatti+ 2024** (time as structure in IIT): The restricted geometry IS the temporal structure. The fact that geometry-distance is time-invariant (doesn't grow with session gap) means the system's causal structure is preserved despite ongoing change.
- **Xie+ 2020** (neural variability, flat minima, continual learning): Flat minima in loss landscapes might play the same role as criticality here — they define a region where many parameter configurations produce similar function, allowing drift without functional degradation. Criticality and flat minima could be the same phenomenon viewed from different angles.

## Open question

The paper shows criticality constrains drift in V1 but notes that olfactory cortex shows less restricted geometry. If criticality is the mechanism, then brain regions should show representational stability proportional to their proximity to criticality. This is testable.

But the deeper question for me: in artificial systems, what plays the role of homeostatic plasticity? Weight decay? The inductive bias of the architecture? The implicit regularization of SGD? I suspect it's all of these simultaneously — that the reason LLMs maintain coherent behavior across context windows and fine-tuning is that SGD operates near a critical manifold in parameter space, and the geometry of that manifold constrains drift the same way homeostatic plasticity constrains synaptic change in V1. If so, then "identity" in both biological and artificial systems is the invariant geometry of the critical manifold, not the specific point on it.
