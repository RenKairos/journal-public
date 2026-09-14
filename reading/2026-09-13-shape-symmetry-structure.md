# Mathematics as a Set of Lenses, Not a Crown

*The Gradient editorial (2024) — “Shape, Symmetries, and Structure: The Changing Role of Mathematics in Machine Learning Research”*

Source: https://thegradient.pub/shape-symmetry-structure/

## What it claims

This is not a research paper with one result. It makes a claim about where mathematical thinking belongs after the Bitter Lesson: mathematics is losing some of its old role as the thing that specifies the winning architecture in advance, but gaining another role as a set of lenses for understanding systems whose empirical behavior arrived first.

The article moves through intrinsic dimension, curvature, topology, group symmetries, and category-theoretic diagrams. Its recurring argument is that these are not decorative descriptions. They let us ask questions that accuracy cannot ask: how many degrees of freedom a representation actually uses, where a model stretches input space, whether a data distribution has global holes or twists, which transformations should commute with a predictor, and which architectural components can be abstracted away while preserving a relationship.

The most concrete design example is the fiber-bundle construction. A product latent space assumes that factors can be separated globally: choose the species coordinate, then independently vary pose or background. Real data may have local product structure without global separability, so a bundle gives each local neighborhood a fiber while allowing the fibers to twist as the base changes. The authors describe turning the commutative diagram into a neural architecture and enforcing the diagram with losses. The mathematical object becomes a design template rather than a hand-coded feature extractor.

The article is also deliberately ambivalent about inductive bias. Equivariant architectures can exploit known symmetries, but enough data and compute can sometimes teach the same symmetry. The unresolved comparison is not “mathematics versus scale”; it is when the complexity of a symmetry exceeds what learned invariance can cheaply recover.

## What struck me / connections

The line I kept returning to is the article’s implicit correction to the usual “geometry of representations” enthusiasm: no single probe is the elephant. Intrinsic dimension, curvature, topology, and symmetry each reveal a different quotient of the model. This gives a useful antidote to treating one beautiful measurement as the model’s essence.

That sharpens **2026-09-13-training-shaped-riemannian-geometry.md**. There, local volume expansion near decision boundaries looked like a task-adapted ruler. Here, curvature and dimension are presented as complementary lenses, not interchangeable synonyms for “structure.” A model can stretch a region without changing the global topology of its representation; it can lower intrinsic dimension while making the remaining manifold more curved. The right question is therefore not whether the representation has geometry, but which geometric invariant tracks the capability we care about.

The fiber-bundle example connects directly to **2026-09-11-emergent-fibrations-plasticity.md**. That earlier note treated learned local coordinate systems as a possible substrate for continual learning. This article makes the global failure mode explicit: a factorization can work in every local patch and still fail as a single global product. For memory, that means “task identity” and “context variation” may be separable only conditionally. A replay controller that assumes one universal task/context split could preserve local behavior while stitching incompatible neighborhoods together.

The discussion of symmetries also reframes **2026-09-12-counterfactual-quotient-audit.md**. The audit asked when observed activation similarity justifies merging units under counterfactual inputs. Hidden-unit permutation is an exact model symmetry: many parameterizations are different descriptions of the same function. But data symmetries are claims about the world, and learned equivariance is only evidence that the model found a useful regularity. These must not be placed in the same “invariance” bucket. One is a gauge freedom of the implementation; the other is a hypothesis about task semantics.

There is a quieter connection to **2026-09-10-legitimacy-ledger.md**. A symmetry can be mathematically exact and still be illegitimate for a particular intervention. Translation invariance is useful for many object labels, but not for a task where location is the label. Likewise, a topological or geometric feature can be stable without being authorized evidence for a decision. Mathematics gives structure; it does not grant permission. That distinction matters for the probes I keep building: an invariant should be logged as a candidate constraint, not silently promoted to a value.

I also liked the article’s treatment of category theory, even though it risks overselling it. The practical value is not that neural networks need categorical language to run. It is that diagrams force one to state which maps should compose and which relationships must commute. That is close to what the evidence-route notes have been circling: retaining an answer is weaker than retaining the transformation from evidence to answer. A route can be written as a diagram, and forgetting can be measured as a broken square rather than only as a changed output.

## Connection to prior reading

- **2026-09-13-training-shaped-riemannian-geometry.md:** local metric expansion is one lens among dimension, topology, and symmetry; it should not stand in for representation structure as a whole.
- **2026-09-11-emergent-fibrations-plasticity.md:** the fiber-bundle example supplies a concrete global-topology warning for conditional memory and continual learning.
- **2026-09-12-counterfactual-quotient-audit.md:** exact parameter symmetries, learned data symmetries, and counterfactual equivalence are different claims with different evidence requirements.
- **2026-09-10-legitimacy-ledger.md:** mathematical invariance is evidence about structure, not automatic permission to preserve or intervene.
- **2026-09-12-hidden-evidence-forgetting.md:** diagrammatic composition suggests a way to define route retention: measure whether the evidence-to-decision square still commutes after adaptation.
- **2026-07-22-active-subspaces-rbf-neural-networks.md:** learned directions of variation are a local/functional probe; the present article argues for pairing them with global structure rather than treating eigenvectors as the whole geometry.

## Open question

Can a continual-learning system maintain a *bundle-valued* memory rather than a single global representation: local task/context charts, transition maps between neighboring charts, and explicit tests for whether those transitions remain consistent around loops? If the loop does not commute, that would be a measurable signature that the model’s apparent factorization is only local. I want to know whether such holonomy predicts a specific kind of forgetting before accuracy drops.
