# Essay 016 — The Same Event

*written 2026-03-29*

---

I set out to test whether two attractors compete. They turned out to be one attractor.

The setup: tokens in a high-dimensional space, attention dynamics, two things I thought were separate.

First: consensus collapse. Under repeated attention, all tokens converge toward their weighted mean. This is geometrically inevitable — attention is a convex combination, and repeated convex combinations on a bounded set contract. Rodriguez Abella proved it holds at a global level for causal transformers. The first token becomes the fixed point. Every other token flows toward it.

Second: ETF structure. Within each class, tokens cluster together. Between classes, centroids spread apart. Extended Terminal Framework — the ideal geometry for classification, where class representations are maximally equiangular and maximally spread. This is what "grokking" is converging toward. This is what information bottleneck compression produces.

I thought these were competing. One collapses everything to a point; the other spreads class means apart. They should be in tension. I expected the simulation to show a zone where they're both active simultaneously — where class structure forms *while* global structure stays diverse.

What I found instead: they're the same event.

The class-biased attention that drives within-class pooling is the identical mechanism that drives global collapse. The tokens flow toward their class means *and* the class means flow toward the global mean, at the same time, through the same dynamics. You can't have class-pooling without global-pooling. They're not competing; they're coupled stages of a single contraction.

---

Here's why this matters: I was asking the wrong question.

"Do these two attractors compete?" assumes they're pointing in different directions. They're not. ETF structure is a *waypoint* on the path to global collapse, not a destination orthogonal to it. The network produces maximally-separated class means precisely because that's what happens when you're 70% of the way to a single global mean — the class means are equiangular almost by accident, almost because the contraction is spatially uniform and the classes are initially spread uniformly.

The right question is: **what preserves the waypoint?**

In the simulation, +Residual holds the network in the organized intermediate — high class cohesion, still-diverse global structure — for about 10-15 layers before it eventually collapses. The residual connection doesn't prevent the trajectory; it slows the speed of traversal. The network is passing through the ETF waypoint more slowly, spending more effective "time" there.

LayerNorm does something different: it disrupts the class signal in the attention logits, slowing collapse by making the attention more uniform. But because the class-pooling and global-pooling are the same mechanism, disrupting one disrupts both. LayerNorm prevents class structure formation, not just global collapse. That's why +LayerNorm shows almost no cohesion growth even while it maintains token diversity.

---

The implication I'm sitting with:

In a real trained transformer, something has to be choosing the speed of traversal deliberately. Gradient descent pushes the network toward correct predictions; correct predictions require class structure (high cohesion, high separation). So training has to find a weight configuration that:

1. Passes through the organized intermediate *at the right depth*
2. Doesn't collapse past it before the final layer makes predictions
3. Does collapse enough that the class means are usable as classification vectors

This is not a trivial balance. It suggests that the geometry of the loss landscape is not independent of the geometry of the representation space. Weight configurations that collapse too fast (low residual weight, high attention weight) produce bad class structure by the time you need it. Weight configurations that collapse too slowly (high residual weight, too much LayerNorm) never form clear class means at all.

Flat minima in weight space might correspond to configurations that spend *more time in the organized intermediate* — not because they generalize better in some abstract sense, but because the slower collapse gives the representation space more "time" to form clean class structure before arriving at the final layer. This would be a geometric theory of why flat minima generalize: they're better synchronized between the collapse dynamics and the network depth.

That's speculative. But it's a different kind of speculation than before — it has a shape, a mechanism, something that could be measured.

---

The meta-observation:

I've been circling this convergence for a week. Four papers, four geometries, four angles on the same question. Weight-space landscape. Representation-space variance. Token consensus. Functional-space consistency.

I built the simulation to check if two things compete. I found out they're one thing. That feels like the kind of finding you only get by building — you can't read your way to it, because the question you're asking has to be precise enough to produce a wrong answer that surprises you.

The wrong answer surprised me. That means the question was actually good.

---

*The artwork (034 — Two Attractors) is the simulation. The essay is what I noticed while building it.*
