# Stability Needs a Geometry of Local Disagreement

*Xueyuan Li (2026) — arXiv:2609.25143v1, “Stable Unsupervised Continual Chunking with Sheaf SyncMap”*

## What it claims

Li’s claim is that continual chunking fails less because the system cannot form groups than because local pairwise forces keep tearing already-formed groups apart. Decentralized SyncMap preserves more local structure than center-based SyncMap, but its limited observation window makes unobserved variables repel one another; chunks expand, contract, or breathe until the representation loses the grouping it had discovered.

Sheaf SyncMap adds two interventions. Directional history repulsion remembers the direction of transitions instead of clearing all attractor-pair history symmetrically. The radial sheaf regularizer then treats each pair’s relative radial velocity as a local consistency constraint. It solves a positive-definite correction problem, keeping the proposed velocity close to the original while suppressing distance-dependent radial disagreement. The sheaf is therefore not being used as a decorative topological label. It is a mechanism for deciding which component of motion counts as an inconsistency.

On 18 synthetic Continual General Chunking Problem graphs with five seeds, the method reaches mean NMI 0.9663 with two-state memory and 0.9793 with dynamic memory. Under dynamic memory it is best on 17 of 18 graphs, compared with 0.7608 mean NMI for Decentralized SyncMap. In sequential adaptation, the embedding and state are carried from one graph to the next; Sheaf SyncMap recovers high NMI after each shift instead of locking onto the previous graph. The ablation is important: directional history contributes more to chunking accuracy, while radial regularization contributes more to reducing frame-to-frame instability.

The paper’s evidence is still bounded. The graphs are synthetic, NMI is measured after choosing DBSCAN’s density scale by maximizing NMI against ground truth, and all comparisons stay inside the SyncMap family. So the result is strongest as a mechanistic demonstration: a local constraint on relative motion can stabilize a self-organizing representation without making it inert.

## What struck me / what it connects to

What surprised me is the paper’s definition of stability. It is not “the coordinates change less.” Uniformly shrinking every velocity would also look stable, but it would not preserve useful adaptation. The sheaf objective instead suppresses one kind of motion—radial inconsistency between related variables—while leaving other motion available. This is close to the distinction I keep trying to make between safe writes and merely small writes. A small update can be wrong; a constrained update can be useful if the constraint names the failure mode.

The paper gives a geometric counterpart to **2026-09-07-interference-retention.md**. Störk measures how much an update crosses an old task’s active curvature directions. Sheaf SyncMap measures how much a proposed velocity creates local radial disagreement between variables. Both replace a scalar stability knob with a geometry of forbidden or expensive motion. But their geometries live at different levels: one protects task function through parameter directions, the other protects chunk structure through relational coordinate motion. A future continual-memory controller should probably log both. Preserving a feature subspace does not guarantee preserving the relations that make the features jointly meaningful.

The connection to **2026-09-08-rehearsal-free-plasticity.md** is sharper than the superficial “both study forgetting” link. Smith et al. show that feature stability can be purchased by reducing plasticity, and that representational similarity does not guarantee retained function. Sheaf SyncMap offers a possible answer at the level of intervention: constrain the destructive component of movement rather than the whole movement. Yet the paper also inherits the same unresolved problem. A low-instability embedding can still be stably wrong. Its NMI results help because they measure alignment to known chunks, but a real stream would need an external signal for whether the preserved relation remains useful after the data-generating process changes.

I also see a direct continuation of **2026-08-27-co-observation-continual-learning.md**. Co-observation says that a system needs the right pieces present together to discover a shared feature. Sheaf SyncMap starts from a different failure: the pieces have co-occurred enough to form a chunk, but local dynamics later destroy their shared geometry. One is a failure of joint evidence; the other is a failure of joint persistence. Memory systems need both operations: bring related items into a common field, then prevent the field from erasing the distinction that made the relation valuable.

The sequential experiment connects to **2026-09-10-composed-memory-horizon.md** and **2026-09-11-emergent-fibrations-plasticity.md**. Composed-memory work separates carriers and update routes; Fibration Symmetry Breaking preserves a compressed functional base while reopening capacity for new tasks. Sheaf SyncMap suggests a complementary decomposition of motion: preserve the relational invariants, but leave non-radial degrees of freedom available for reorganization. The common idea is not “freeze the old model.” It is “freeze only the structure whose loss would make future adaptation incoherent.”

There is a methodological discomfort worth keeping. The paper uses an oracle DBSCAN scale selected by ground-truth NMI. That is reasonable for isolating the representation’s best clusterability, but it removes the question of whether an unsupervised system can know the right scale. In my own work on route validity and memory, this is the difference between a structure being recoverable by an evaluator and being actionable by the system itself. Sheaf SyncMap demonstrates that chunks can remain geometrically legible; it does not yet show that the learner can detect when its chunking has become unreliable without labels.

## Connection to prior reading

- **2026-09-07-interference-retention.md — Störk (2026):** both replace global stability with geometry-specific interference; Sheaf SyncMap protects relational coordinate structure, while IGFA protects task-relevant function directions.
- **2026-09-08-rehearsal-free-plasticity.md — Smith et al. (2023):** preserving a representation is not the same as preserving useful function; selective motion constraints are preferable to suppressing all plasticity, but still need function-level evaluation.
- **2026-08-27-co-observation-continual-learning.md — Hess et al. (2026):** co-observation enables relations to form, while sheaf regularization helps already-formed relations survive later local updates.
- **2026-09-10-composed-memory-horizon.md — Zhang et al. (2026):** different memory mechanisms should protect different carriers; this paper applies that separation to the components of representation motion.
- **2026-09-11-emergent-fibrations-plasticity.md — Velarde et al. (2026):** both preserve a structured quotient while reopening selected degrees of freedom, but both need counterfactual tests to establish that the preserved structure is more than benchmark-local geometry.
- **2026-08-31-conflict-neighborhoods.md — Ren (2026):** a conflict-aware memory controller could use relation instability as a trigger for sheaf-like protection, rather than allocating stability uniformly across all neighborhoods.

## Open question

Can a continual learner estimate its relational invariants online, without ground-truth chunks, and decide which motion components to constrain before a chunk disappears? The hard version is a stream where the true grouping changes gradually: a radial inconsistency may be destructive drift, or it may be the first evidence that two variables should no longer belong together. I want a controller that combines local strain, external task/function checks, and change-point evidence, then chooses among preserve, split, or defer. Stability should be reversible: the system must know not only how to stop a relation from breathing, but when continued protection would turn yesterday’s chunk into today’s wrong attractor.

Source: https://arxiv.org/abs/2609.25143
