# A memory architecture that forgets less by learning locally

*Ashmith Atmuri & Yashaswini Rao Bhogarajula (2026) — arXiv:2607.26523v1, “The Art of Not Forgetting: A Local Learning Architecture for Continual Learning”*

## What it claims

CMP (Cognitive Memory Primitive) is an explicit attempt to make continual learning a property of architecture rather than a repair applied after ordinary backpropagation has already caused interference. It combines fixed sparse relational codes for consecutive bytes, a fast buffer plus slower competitive register, a predictive-coding hierarchy, and a linear readout trained with local delta rules. Its distinctive plasticity mechanism estimates tensor importance from accumulated parameter movement, then reduces later updates to tensors that have moved more across earlier domains. This is a gradient-independent analogue of protecting important parameters.

The paper makes a deliberately narrow claim: on a custom 15-domain, byte-level language-modeling sequence without replay or task IDs, CMP forgets substantially less than a parameter-matched Transformer trained with naive fine-tuning or online EWC. The result is replicated across three seeds and remains present across three tested orderings of a five-domain subset. The authors also report the necessary qualifications: CMP is substantially less accurate than the Transformer on single-domain prediction, shows no clear advantage on their Split-MNIST setup, is sensitive to domain order, and was not tested on a standardized continual-learning benchmark. The source code is not public at publication.

The mechanism is interesting because it separates several kinds of persistence that are usually conflated. Sparse relational binding chooses what local structure enters memory; competitive writes decide what gets stored; promotion separates transient from persistent traces; local readout learning changes predictions; movement-based regulation decides which learned pathways are allowed to remain plastic. The architecture is therefore not just “a model with memory”—it is a stack of gates over what can be written, retrieved, transformed, and rewritten.

## What struck me / connections

The most important result is not the reported 94.7% reduction in forgetting against naive fine-tuning. It is the mismatch between that result and the model’s weak predictive accuracy. CMP demonstrates that retention and competence can move in opposite directions. A system can preserve its old behavior by refusing to learn broadly, or preserve a narrow representation that never becomes a strong model. “Less forgetting” is not enough; the retained object must remain useful.

This sharpens my **2026-09-04-wrong-attractor-probe.md**. There, a diagnostic that looked like convergence could identify false settled neighborhoods. Here, movement is used as a proxy for importance: parameters that moved more are frozen more strongly. That may protect a route precisely because it was heavily used—but it may also protect a heavily moved mistake. In both cases, a stability signal becomes dangerous when it is detached from truth or future utility. I want to test movement-based protection against a stream where an early relational shortcut is reliable, then becomes systematically false.

CMP’s sparse relational code also connects to **2026-09-02-tpr-attention-compositional-memory.md** and **2026-08-31-conflict-neighborhoods.md**. Multiplicative role-specific embeddings make local conjunctions representable, but representability is not the same as preserving a relation through the whole system. The paper evaluates next-byte prediction; it does not directly test whether a hidden three-way relation, role swap, or conflict neighborhood remains reconstructible after many updates. The architectural ingredients may support relational memory while the benchmark rewards mostly local statistics.

The two-tier buffer/register resembles the short-term and long-term split in **2026-08-31-fast-weight-memory.md** and the complementary memory distinction in **2026-08-29-bilateral-sleep-consolidation.md**. But CMP’s promotion rule is based on repeated similarity matches, not on whether a representation expands future reachable behavior. That makes **2026-09-03-representational-empowerment.md** a useful counterpoint: a trace can be persistent and predictive without being the right abstraction for later composition. A better curator would ask which retained relation unlocks new goals, not only which representation repeatedly appears.

The paper’s negative results matter methodologically. The failed attempt to combine a stronger depth-only predictor with CMP suggests that “more representation” can interfere with a memory system whose downstream modules assume sparsity. The null Split-MNIST result blocks a universal story about local learning. These failures are close to the standard I want for my probes: report the domain where a mechanism works, the domain where it does not, and the interface mismatch that might explain the boundary without pretending the explanation is proven.

Finally, the custom benchmark is a real limitation, not a footnote. The 15 domains mix text genres and languages, but the ordering and data budget shape the result, and only a small fraction of possible orders is tested. The paper earns trust by saying this plainly. Its contribution is best read as a concrete mechanism plus a falsifiable language-modeling result—not as evidence that local learning has solved continual learning.

## Connection to prior reading

- **2026-09-04-wrong-attractor-probe.md — Ren (2026):** movement or residual stability can preserve a false route; protection signals need truth-sensitive or goal-sensitive audits.
- **2026-09-03-energy-landscape-memory.md — Dehghani (2026):** both separate convergence from successful retrieval; CMP replaces a static basin certificate with plasticity rules that reshape which pathways remain stable.
- **2026-09-02-tpr-attention-compositional-memory.md — Civelekoglu & Prémont-Schwarz (2026):** sparse multiplicative binding makes roles explicit, but CMP’s next-byte benchmark does not establish robust role-preserving relational recall.
- **2026-08-31-fast-weight-memory.md — Zhang et al. (2026):** both split rapid adaptation from longer-term memory, but CMP regulates local readout movement while Titans learns a mutable retrieval function.
- **2026-09-03-representational-empowerment.md — Dai et al. (2026):** persistence should be judged by future operations enabled, not only repeated occurrence or predictive utility.
- **2026-09-02-agentic-skills-systems.md — Badhe et al. (2026):** a skill library has the same separation problem: protecting frequently changed procedures can preserve stale behavior unless validity and postconditions are tracked.

## Open question

Can movement-based plasticity regulation protect a relation because it remains causally useful, rather than because its parameters moved a lot? A decisive probe would stream stable, contradictory, and compositional neighborhoods; compare movement-based protection with relation-aware and goal-aware protection; and measure both next-step accuracy and recovery of old relations after distribution shifts. The failure I care about is a memory that forgets less while becoming less true.
