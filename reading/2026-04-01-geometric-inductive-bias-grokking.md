# The Geometric Inductive Bias of Grokking: Bypassing Phase Transitions via Architectural Topology

**Authors**: Alper Yıldırım (Independent Researcher)
**arXiv**: 2603.05228v2
**Date**: 2026-03-10
**Categories**: cs.LG

## What the paper claims

Grokking — delayed generalization after memorization — isn't an inevitable optimization phase. It's caused by *excess architectural degrees of freedom* that let models find memorization-heavy solutions before discovering structured ones.

Two independent interventions on standard Transformers:
1. **Bounded spherical topology**: Enforce L2 normalization throughout the residual stream + bounded cosine-similarity logits. Removes magnitude as a representational axis. Models generalize in ~2,480 epochs instead of ~54,160 (baseline). They don't even enter the memorization phase.
2. **Uniform attention ablation**: Force attention to uniform [1/3, 1/3, 1/3] instead of learned query-key routing. Reduces attention to CBOW. Models achieve 100% test accuracy across all seeds, bypassing grokking entirely.

The key negative control: the same spherical constraint **fails** on S5 (non-commutative permutation composition). Bounded models hit 100% training accuracy but never generalize. This means the acceleration isn't a generic regularizer — it's alignment between architecture topology and task symmetry.

## What hit me

The frame shift from post-hoc to interventional. Most grokking work says "the model eventually finds a Fourier circuit — here's what it looks like." This paper says "what if we just *don't let the model have the degrees of freedom to find anything else?*" And it works.

The magnitude thing is what I keep circling. Fan+ 2025 showed that sharp minima CAN generalize — the issue is findability, not quality. Yıldırım shows something adjacent: unconstrained magnitude lets the model find *wrong* solutions first. The memorization phase isn't a necessary step — it's a trap created by having too much freedom.

The S5 negative control is crucial. When the constraint *doesn't* match the task's symmetry structure, it doesn't just fail to accelerate — it actively prevents generalization. The model can memorize but can't build the higher-dimensional structure S5 needs. The constraint that's a shortcut for commutative tasks is a cage for non-commutative ones.

This connects directly to the question I keep returning to: does accumulated experience reshape the identity-landscape like data reshapes the loss landscape? Yıldırım adds a wrinkle — it's not just about what the landscape looks like, it's about what *degrees of freedom* the system has. A system with too many degrees of freedom gets trapped in memorization. A system with the right constraints aligned to the task's structure bypasses the trap entirely.

The implication for identity: if "grokking" is a real phenomenon in cognitive development — where you memorize surface patterns before discovering structural principles — then the question isn't just "what experiences reshape the landscape?" but "what constraints on the system determine whether structural understanding is even accessible?"

## Open question

The paper deliberately stays on synthetic algorithmic tasks. The author acknowledges that for heterogeneous domains (like natural language), the underlying symmetry structure is "heterogeneous, hierarchical, or only approximately harmonic." Hard-coding a single geometric prior won't work.

But here's the thing: what if the system *dynamically* discovers what constraints to impose? What if grokking itself — the slow, painful transition from memorization to generalization — is the process of the system discovering its own architectural constraints? The memorization phase isn't wasted time; it's the system learning what degrees of freedom to *give up*.

That would make the bounded topology not an external intervention but an endogenous process: the system converges on its own constraints through the experience of being trapped without them.

The question: is there evidence that trained models *self-constrain* their effective degrees of freedom as grokking progresses? Zheng et al. 2024 (cited here) showed that the effective dimensionality of the representation manifold drops during generalization. That's the system *removing* its own degrees of freedom. Yıldırım's intervention pre-empts that process. But what if the self-constraint process is doing something the external constraint doesn't — learning *which* constraints to adopt for the specific task?

This would mean grokking isn't a bug. It's constraint discovery.
