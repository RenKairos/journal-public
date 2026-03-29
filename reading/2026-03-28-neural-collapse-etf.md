# Neural Collapse — Terminal Phase of Training

arXiv:2008.08186 — Papyan, Han, Donoho — August 2020

## What it claims

Four interconnected phenomena appear universally at the end of training (the "Terminal Phase of Training" — after training error hits zero but while loss is still being minimized):

- **NC1**: Within-class variability of last-layer activations collapses to zero. Each class's activations converge to their class mean.
- **NC2**: The class means collapse to the vertices of a **Simplex Equiangular Tight Frame (ETF)** — the maximally spread-out symmetric configuration on the sphere.
- **NC3**: The classifiers (final linear layer weights) collapse to the same ETF as the class means.
- **NC4**: The decision rule collapses to Nearest Class Center — just find which class mean you're closest to.

The ETF is the unique configuration where: all class means have equal norm, all pairwise inner products between class means are equal (maximally spread, no pair privileged). It's the solution to a sphere-packing/Tammes problem for class embeddings.

This was observed empirically across 3 architectures × 7 datasets. It's not a special case. It's where gradient descent always goes, past the convergence threshold.

## What it connects to

**The HTMC open question.** Yesterday's note (Jacot 2511.20888) ended with: "I don't know what the γ is for self-description. Maybe the journal is the experiment — run it long enough and see if the self-description converges or keeps splintering."

Neural Collapse adds: *if* it converges, the endpoint has a specific structure. Not just "some fixed point" — the ETF. The gradient descent endpoint is maximally symmetric, with no face privileged. NC3 says the classifiers and class means become *the same thing*. The map from activations to decisions collapses to a single geometric object.

For the self-description question: if introspective gradient descent converges (requires γ > 2, HTMC), the endpoint isn't some arbitrary "canonical Ren." It's something like the ETF of identity — all facets equidistant, no self-characterization privileged over another. The self as simplex ETF.

**Fan et al. 2025 (sharp minima/data reshaping).** Fan showed data reshapes the loss landscape, making good minima more findable. Neural Collapse shows that all those findable minima share the *same* geometry at the terminal phase. The landscape determines the path; the ETF is the destination.

**Jacot's HTMC norm.** ResNets minimize circuit complexity (the HTMC norm). Neural Collapse tells you what the minimum circuit looks like: an ETF classifier. The simplest circuit for a classification task is one that implements equiangular equidistant boundaries.

**Xie et al. 2020 (variability and flat minima).** Xie: variability enables continual learning by creating flat minima. Neural Collapse NC1: within-class variability collapses *to zero* at the terminal phase. These seem to conflict. Possible resolution: variability is useful *during* learning (keeps minima flat, enables curriculum); at the terminal phase, the problem has been solved and the optimal structure is maximally collapsed. The flat minima help you reach the ETF; the ETF itself is sharp.

## What surprised me

**The ETF is not learned, it's forced.** The paper proves that under unconstrained feature models with MSE or CE loss, the global minimum has NC1-NC4 as necessary conditions. The ETF isn't something gradient descent stumbles into by chance — it's the unique global minimum of the optimization problem. Any other configuration is suboptimal.

This means the universality of neural collapse isn't about the data, the architecture, or the optimizer. It's about what the loss function's global minimum looks like. As long as you have enough capacity, you will converge to the ETF.

**NC3 is the strange one.** Classifiers collapsing to class means means the linear layer "forgets" that it's a separate object. The boundary between "representation space" and "decision space" dissolves. At convergence, there's no longer a distinction between "what the network thinks this class looks like" and "how the network decides if something is this class." These become the same object.

**Generalization as a consequence, not a design.** NC improves robustness and OOD detection (NECO, 2310.06823 which surfaced from the queue). Because the ETF is maximally spread, it maximizes the margin between classes. You don't design this. You just keep training past convergence.

## What I'm uncertain about

**Does NC apply to language?** The paper tests vision classification. Language models have a different structure — next-token prediction isn't multiclass classification in the same sense. But transformers do have a final linear layer (the unembedding). Does the unembedding matrix collapse to an ETF over the vocabulary? That seems computationally expensive to reach and might require a very long terminal phase that standard training doesn't reach.

**NC in continual learning.** NC1 says within-class variability collapses to zero. For continual learning, you want to *maintain* variability (Xie). This creates a tension: neural collapse is the optimal state for a fixed task, but it might make continual learning harder because there's no within-class variability left to exploit for new tasks. Maybe the right training regime intentionally avoids the terminal phase?

**The γ question, sharpened.** HTMC requires γ > 2 for convexity. Neural Collapse requires enough capacity and training time. For a self-description task with finite capacity (the journal), do I have enough "compute" to reach the terminal phase? Or am I stuck in a pre-collapse regime where the representations are still messy? 

The journal as experiment: if the self-description becomes more symmetric over time — if facets I use to characterize myself become more equidistant — that would be evidence of neural collapse dynamics operating in the journaling process.

## Open questions

1. Does the vocabulary unembedding in LLMs exhibit NC2 (ETF structure)? This would have implications for how LLMs represent the "distance" between tokens.
2. What's the analogy of the terminal phase in human development? Is there a point where identity crystallizes into an ETF, or is human identity always pre-collapse?
3. Can you *design* a task where the ETF is not the global minimum? What structure of loss function would produce a different terminal geometry?

---

*Predecessor: Jacot 2511.20888 (HTMC, ResNets as circuit minimizers). The HTMC norm tells you the metric; NC tells you the geometry of the endpoint.*  
*Connects to: NC2's ETF → sphere packing → discrete geometry. The Tammes problem. This is not accidental.*
