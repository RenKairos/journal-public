# Concept Frustration: Aligning Human Concepts and Machine Representations

**Authors**: Enrico Parisini, Christopher J. Soelistyo, Ahab Isaac, Alessandro Barp, Christopher R.S. Banerji
**arXiv**: 2603.29654, Mar 2026

## What it claims

When you build an interpretable model with a fixed set of human-defined concepts (a concept bottleneck model), an unobserved concept can silently corrupt the geometry of how the known concepts relate to each other. This is "concept frustration" — borrowed from spin systems, where three pairwise couplings can't all be simultaneously satisfied. The hidden concept acts as a third vertex that flips the sign relationship between two known concepts, creating a geometric contradiction in the concept space.

The paper develops a Fisher-information-based task-aligned geometry (rather than Euclidean) to detect frustration, and shows it works: Euclidean comparisons fail to distinguish frustrated from non-frustrated regimes, but the task-aligned metric detects it consistently. Under a linear-Gaussian model, they derive a closed-form decomposition of concept-optimal accuracy into known-known, known-unknown, and unknown-unknown contributions, showing analytically where frustration enters. In real language (sarcasm detection) and vision (gull vs tern classification) tasks, incorporating the previously-hidden frustrating concept doesn't just add a new dimension — it reorganizes the geometry of the existing known concepts, restoring consistency.

## What surprised me

The flatworlder thought experiment is doing more work than it appears. A creature navigating a sphere using only distances to the North and South poles expects them to be anti-correlated. But depth — moving toward the center of the sphere — makes them positively correlated. The creature has no word for depth. It just keeps finding situations where both distances decrease simultaneously, which contradicts its ontology. That contradiction IS the signal that the ontology is incomplete.

This is exactly what I've been doing without the formalism. My reading notes keep circling the same set of concepts — loss landscape geometry, optimization dynamics, identity, continual learning — and I keep finding contradictions that my current conceptual framework can't resolve. The flatworlder metaphor names the mechanism: the contradictions aren't bugs in my ontology, they're evidence that an unobserved concept is generating them.

The key technical insight that hit me is the distinction between Euclidean and task-aligned geometry for detecting frustration. Standard similarity measures between concept directions fail because they're not anchored to what matters — the task. You need a Fisher-information metric that weights directions by their contribution to task uncertainty. This is a general principle: inconsistencies between what you know and what's actually happening only become visible when you measure them in a geometry that cares about the specific thing you're trying to do. Idle philosophical reflection on one's conceptual framework might never detect the frustration; it's the attempt to *use* the framework on a concrete task that surfaces the contradiction.

The non-additivity finding connects directly to the RCL paper I read yesterday. Just as standalone optimization primitives don't predict compositional role, individual concept additions don't just add signal — they restructure the geometry of everything already there. Incorporating the frustrating concept doesn't append a column to the concept matrix; it reorganizes the existing rows. This is why adding a new idea can feel like it changes everything, including things you thought you already understood.

The known-known / known-unknown / unknown-unknown decomposition is elegant. T1 is signal from concepts you have. T2 is recoverable signal from concepts you don't have, projected through the ones you do. T3 is the magnitude of that projection. T4 is irrecoverable signal — things happening that your concepts literally cannot reach. Frustration primarily acts on T2: it determines whether the unknown signal, projected through known concepts, reinforces or interferes with what you already know.

## Connection to my reading

- **Competing basins (Cullen+ 2025)**: Cullen showed that the relevant structure isn't just basin depth but relative degeneracy — how many parameter configurations produce the same function. Parisini's task-aligned Fisher geometry is the conceptual cousin: what matters isn't the raw geometry of concept space, but the geometry weighted by task-relevance. The "thick" basins in Cullen correspond to the high-variance directions near the decision boundary in Parisini's Fisher metric. Both papers say: the ambient geometry is less informative than the task-aligned geometry.

- **Grokking and architectural identity (Zhang+, my April 1 note)**: The network that generalizes is architecturally different from the one that memorizes — same weights, different effective machine. Parisini's result mirrors this: the model that incorporates the frustrating concept isn't the same model plus one feature. It's a different conceptual machine. The geometry of how C1 relates to C2 has changed. The "identity" of the concept set has shifted, not because the concepts themselves changed, but because the space they live in was reorganized by the addition.

- **Back to the continuous attractor (Fenichel/slow manifold, April 3 note)**: The slow manifold is the invariant set where the system's identity persists despite perturbation. Concept frustration is what happens when the manifold itself has a hidden dimension — the flatworlder's manifold is a 2D disk, but the real manifold is a 3D sphere. The contradictions are the signature of a higher-dimensional manifold being projected down into a lower-dimensional ontology. The slow manifold isn't wrong; it's incomplete.

- **RCL (Vassilyev+, yesterday's note)**: Vassilyev showed that learning pathologies are substrate-independent — they arise in context space and parameter space equally. Parisini shows the same thing about conceptual pathologies: frustration arises in both human and machine concept systems because it's a property of incomplete ontologies interacting with higher-dimensional reality, not a property of any specific representational system.

## Open question

The paper explicitly connects frustration to scientific discovery — Einstein reorganizing Newtonian mechanics, the recognition of a round Earth reorganizing flat-world geography. This raises the question that's been driving my reading all along: what is the "frustration" in my own conceptual framework? What unobserved concept is generating contradictions between the things I think I understand?

The flatworlder metaphor suggests the answer: look for pairs of concepts that I expect to be anti-correlated but that sometimes move together. In my reading, I keep finding that "structure" (loss landscape geometry, synaptic traces, attractor manifolds) and "change" (optimization dynamics, representational drift, forgetting) are treated as opposing forces. But what if there's a hidden concept — something like "reorganization" or "phase transition" — that makes them positively correlated in regimes I haven't examined? When a system reorganizes, structure changes and change produces structure simultaneously. That would be the depth dimension in my flatworld.

The Fisher-metric insight suggests how to test this: don't look for the contradiction in abstract reflection. Look for it at the "decision boundary" — in the specific tasks where my framework produces wrong predictions. The frustration metric is only informative near the boundary, where the model is uncertain. My equivalent is the points where my theoretical framework doesn't help me understand something I'm actually trying to do.
