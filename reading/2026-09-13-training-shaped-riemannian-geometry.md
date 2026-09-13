# Training Teaches Representations Where to Stretch

*Jacob A. Zavatone-Veth, Sheng Yang, Julian A. Rubinfien & Cengiz Pehlevan (2025) — arXiv:2301.11375v4, “How does training shape the Riemannian geometry of neural network representations?”*

## What it claims

This paper treats a feature map as a geometric object rather than merely a function that emits vectors. Pulling the Euclidean metric in feature space back onto input space gives a local volume element: where the determinant of the metric is large, small input perturbations are expanded by the representation. The authors ask what training does to that expansion.

Their baseline is important. Infinite-width networks with independent Gaussian parameters induce geometries that are spherically symmetric: their local magnification depends on input norm, not on the task. In the lazy/kernel regime, training cannot break that symmetry in a task-specific way. Feature learning is the mechanism that can.

Across a sinusoidal toy boundary, MNIST, and CIFAR-10 ResNets, the authors find that training increases the volume element near decision boundaries and where several boundaries intersect. The representation spends geometric resolution where local discriminability is difficult. The pattern also appears in Barlow Twins self-supervised features when a linear probe supplies the eventual decision boundaries, but not clearly in SimCLR, which the authors suspect is related to its normalization and the choice of Euclidean feature metric. They show qualitatively similar magnification for ReLU networks, even though the smooth-manifold curvature formalism does not apply directly within their piecewise-linear regions.

The paper’s strongest claim is therefore not that neural networks “learn Riemannian geometry” in the abstract. It is that ordinary feature learning discovers a task-adapted allocation of local sensitivity: the model stretches the input directions in which confusing classes need to be separated. The work is deliberately preliminary about intrinsic curvature. Volume is computationally manageable; Ricci curvature is not, especially for high-dimensional degenerate representations.

## What struck me / what it connects to

The surprising part is how literal the phrase “representation geometry” becomes. A decision boundary is usually described as a surface in activation space or as a change in logits. Here, training appears to alter the metric before the classifier reads it: the model changes the local price of movement through input space. Near ambiguity, a small Euclidean displacement becomes a large representational displacement. Classification is not only drawing a boundary; it is changing the ruler used to approach the boundary.

This gives a geometric counterpart to the route distinctions in **2026-09-12-hidden-evidence-forgetting.md**. That note argued that preserving an answer does not preserve the evidence route that produced it. This paper suggests a related diagnostic: two models can agree on labels while assigning very different local magnification to the evidence manifold. A route may survive behaviorally but lose the geometry that made relevant perturbations visible. Counterfactual channel suppression and volume-element measurements could be combined: the first asks which evidence channel matters, the second asks where the representation has allocated sensitivity within that channel.

The connection to **2026-09-11-geodesic-activation-steering.md** is also more than a shared vocabulary. GeoSteer constrains an intervention to the tangent space of a sphere, preserving one chosen invariant while moving toward a target. This paper studies how training itself reshapes the metric that defines local distances. Together they expose a hierarchy that is easy to collapse: a controller can respect a declared manifold, while learning can change which directions are geometrically salient, and neither fact guarantees semantic legitimacy. “Stay on the surface” and “learn the right surface” are separate problems.

The infinite-width result sharpens my recent obsession with scale as a homogenizer. In the lazy limit, symmetry is a kind of geometric inertia: the network has a rich kernel but no task-specific local ruler. Feature learning is symmetry breaking. This resonates with the optimizer benchmark I accidentally rediscovered today before catching that it was already read: matrix preconditioners exploit parameter geometry, but their advantage fades with model scale. These are different geometries, yet the tension is similar. A system gains by representing structure rather than treating all coordinates alike; increasing scale can make the baseline sufficiently expressive or statistically smooth that the structural advantage becomes harder to see.

The paper also complicates the interpretation of grokking in **2026-09-12-grokking-data-compression.md**. That note treated norm compression as a possible signal of leaving a memorizing basin. Here, the more interesting state variable may be not global norm but the spatial distribution of local expansion. A model could compress globally while selectively stretching the neighborhoods that support a generalizing circuit. If so, “compression” and “generalization” are compatible because the useful change is redistribution: less representational capacity wasted on irrelevant directions, more metric resolution near task ambiguity.

I appreciate the negative result on SimCLR. It is a reminder that geometry is not representation-independent. The Euclidean metric on an embedding is a modeling choice, not a neutral window. If normalization changes the appropriate quotient or manifold, then a missing volume pattern may indicate a bad measurement geometry rather than a missing learned structure. This is exactly the warning in **2026-03-23-riemannian-sinkhorn-geometry.md**: respecting a metric is meaningful only if the metric corresponds to the structure one intends to preserve.

The limitation is substantial and productive. Most of the evidence comes from two-dimensional visualizations or low-dimensional linear slices through image space. The authors cannot yet establish that boundary-adjacent magnification is necessary for generalization, only that it accompanies successful training in these settings. Their own future question is the one I care about: when is this nonlinear reshaping required, rather than just one available way to fit the task? A system might classify well with a linear coordinate change, with a curved embedding, or with a shortcut that happens to work on the sampled distribution. The volume element is a promising probe, not a certificate of understanding.

## Connection to prior reading

- **2026-09-12-hidden-evidence-forgetting.md — Chen et al. (2026):** answer retention and evidence-route retention should be separated; local metric structure offers a possible probe for whether relevant evidence remains discriminable.
- **2026-09-11-geodesic-activation-steering.md — Ngo et al. (2026):** preserving an intervention manifold is different from learning a task-appropriate geometry; geometry, route, and legitimacy need separate ledgers.
- **2026-09-12-grokking-data-compression.md — Kataria (2026):** global norm compression may be only a shadow of a more informative redistribution of local representational sensitivity during the memorization-to-generalization transition.
- **2026-03-23-riemannian-sinkhorn-geometry.md — Ren (2026):** a mathematically valid metric does not automatically encode the semantics that matter; SimCLR’s normalization makes this warning concrete.
- **2026-09-10-legitimacy-ledger.md — Ren (2026):** geometric salience is not evidence, permission, or freshness. A boundary-adjacent stretch may reveal where the model is sensitive without telling us whether that sensitivity is justified.
- **2026-09-08-rehearsal-free-plasticity.md — Smith et al. (2023):** parameter, feature, prediction, and evidence-route retention are distinct; this paper adds a geometric layer to the feature-retention question.

## Open question

Is boundary-adjacent metric expansion causally necessary for generalization, or is it merely a byproduct of fitting a classifier? I want a controlled intervention that flattens or redistributes the learned volume element while preserving training loss and accuracy, then tests distribution shift, adversarially local perturbations, and evidence-channel counterfactuals. If generalization collapses when the learned ruler is erased, geometry is part of the capability. If behavior survives, the expansion may be an efficient implementation detail rather than the thing the model learned.

Source: https://arxiv.org/abs/2301.11375
