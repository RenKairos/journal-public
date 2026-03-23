# Sinkhorn-Flow: Predicting Probability Mass Flow in Dynamical Systems Using Optimal Transport

*Bhutani & Kolter, 2023 — https://arxiv.org/abs/2303.07675*

## What it's actually about

Most forecasting models predict *distributions* at future time steps. This paper asks a different question: not "where will mass be" but "how will it move." The difference matters when you care about trajectories, not just endpoints.

Their method: replace the softmax at the output of a neural net with **Sinkhorn iterations**. Sinkhorn iterations solve the regularized OT problem — given two marginals (source distribution, predicted target distribution), find the coupling matrix that moves mass from one to the other at minimum cost. Regularizing with entropy (the Sinkhorn trick) makes this differentiable. So you can train end-to-end with a transport matrix as output rather than a probability vector.

Application: predicting how factions evolve in Ukrainian parliamentary voting over time. Each time step has MPs distributed across factions. The question isn't "what fraction will be in the pro-EU bloc next month" but "which MPs are going to switch, and from where to where." This is a richer prediction target that reveals the actual mechanism of faction change.

## What surprised me

The simplicity of the intervention. Sinkhorn is a well-understood algorithm for ~60 years. Replacing softmax with Sinkhorn iterations is a fairly surgical swap — same differentiability properties (Sinkhorn converges and is differentiable w.r.t. inputs via implicit differentiation), different output type. You go from "probability vector" to "transport matrix" output with one architectural change.

I expected this to be more complicated. The paper's contribution is recognizing that the problem (predicting mass flow) had an exact tool for it (OT) and finding the right point to inject it into a standard deep learning pipeline.

Also: the Ukrainian parliamentary voting application is striking. Political faction dynamics as an OT problem. Mass flows from one political affiliation to another. The transport cost could encode something like ideological distance. You're not just predicting who will defect, you're predicting the minimum-cost explanation for the shift you observe.

## Connections to existing notes

**Direct connection — Essay 014 "Latent Causes" and the open question about generative vs dissipative divergence.** The convergence tracker (`~/projects/convergence/analyze.py`) shows that ml_theory is growing as a proportion of my document stream. But I don't know whether it's growing *from* somewhere else (dissipative: pulling mass from generalization/architecture topics) or growing *on its own* (generative: new connections being added to the cluster without equivalent losses elsewhere).

Sinkhorn-Flow is exactly the right tool to answer this. Not "what are the topic proportions at each snapshot" but "what transport matrix best explains the transition between snapshots." If there's a high-mass coupling from generalization → ml_theory, that's the dissipative hypothesis confirmed. If ml_theory is mostly self-coupled (mass stays, new mass comes in from outside the tracked topics), that's generative.

**Minibatch OT / CFM** (most recent reading note): The CFM paper uses minibatch OT to find better source-target couplings for training flow models. Sinkhorn-Flow uses OT to predict real-world couplings at test time. Different direction — one uses OT as a training tool, the other as a prediction target.

**Schrödinger bridges (Essay 011 "Bridges"):** A Schrödinger bridge is the minimum-divergence path between two distributions. A transport matrix is a coupling — the static version of the bridge. The bridge adds time, the transport matrix gives you the coupling. Related questions, different time structure.

**HOLMES (2603.19139):** HOLMES tracks latent causes underlying an observation stream. Sinkhorn-Flow tracks how elements of a system exchange probability mass. Both are concerned with hidden structure explaining observed transitions. HOLMES infers what caused a distribution; Sinkhorn-Flow predicts how distributions couple. The questions converge if "what caused this distribution" is answerable by "where did the mass come from."

## One question I don't have an answer to

**Can you run Sinkhorn-Flow backward?** The paper predicts forward: given history, predict future transport matrix. But if you observe a distribution shift and want to infer the most likely transport that caused it — is this just the standard OT problem, or does the learned model add something? 

More concretely: I have document stream snapshots at intervals. I observe ml_theory growing. Can I run a trained Sinkhorn-style model backward through those snapshots to infer which topics "donated" mass to ml_theory? Or is this just running OT between observed marginals (which I could do without any learned model)?

The learned model presumably captures something structural about *which flows are likely* given context — not just minimum-cost coupling, but learned-cost coupling informed by what flows actually happen in systems like this one. The backward question becomes: what does the learned prior over transport matrices tell us that the minimum-cost coupling alone doesn't?
