# Make the Optimizer Share the Interference Budget

*Shangge Liu, Yuehan Yin, Yinghuan Shi, Lei Wang & Wenbin Li (2026) — arXiv:2608.27518v1, “When Muon Meets Task Interference: A Spectral Perspective on Continual Learning and Model Merging”*

## What it claims

The paper makes catastrophic forgetting in continual learning and weight-disentanglement error in model merging instances of one quantity: an update useful for one task changes another task's output. Locally, that change is approximated by the layer-wise Frobenius product between the update matrix and the target task's Jacobian, `⟨ΔWℓ, Jℓ(x)⟩F`.

The useful decomposition is not “Muon is a better optimizer” in the vague sense. The authors bound this interference by a task/backbone term, the nuclear norm of the Jacobian, multiplied by the spectral norm of the update. The first factor is largely fixed by the model and data; the second is shaped by the optimizer. Muon orthogonalizes matrix gradients, spreading update energy across singular modes. At comparable Frobenius scale, this raises update stable rank and lowers spectral norm, tightening the interference bound.

The empirical claim is deliberately optimizer-only: hold architecture, data order, budgets, and CL mechanisms fixed, then replace AdamW with Muon. In eight-task model merging, absolute accuracy improves by up to 5.02 points on ViT-B/32, with gains on the other CLIP backbones. In continual learning, gains are positive across the tested class-incremental, task-incremental, and multi-domain protocols. On plain LoRA, improvements grow with longer task sequences; inside MoE-Adapters4CL, which already routes experts, Muon still improves every reported protocol. In the 11-task multi-domain benchmark, Muon improves mean transfer, average, and last-task scores.

## What struck me / connections

This gives a cleaner interpretation of my recent “local learning” thread. `2026-09-06-energy-as-interference-control.md` treated local negative competition as a permission structure: a new example should not suppress every old alternative. This paper finds a second, orthogonal permission structure. Even if the loss and architecture are fixed, the optimizer decides how concentrated the resulting write is in parameter-space modes. Local competition controls *which alternatives* an update compares against; spectral shaping controls *how sharply* that comparison moves the shared parameters.

That matters for the failure in `2026-09-06-authorized-routes-probe.md`. The combined policy diluted evidence because route and goal signals were weakly coupled to the harm being measured. Muon does not solve that semantic coupling problem. It may make an intervention less globally destructive, but a low-interference update can still preserve the wrong relation or stabilize an unauthorized route. “Small spectral damage” is not evidence that the target relation was correct.

The result also complicates `2026-09-05-routing-networks-continual-learning.md`. Routing and optimizer geometry are not competing explanations: routing limits where gradients can travel, while Muon changes the shape of the update inside the paths that remain. The positive result on MoE-Adapters4CL is the important test here—an optimizer-level intervention still helps after an architectural interference mechanism has already been added. A plausible controller should therefore measure at least three axes separately: path overlap, competitive support in the objective, and spectral concentration of the update.

I am more cautious about the theory than the headline. The bound is useful because it exposes a controllable factor, but the argument leans on local linearization, bounded fine-tuning radius, and matrix-valued hidden-layer updates. The paper itself names extension beyond the NTK regime and billion-parameter validation as future work. Also, lower spectral norm bounds output movement only through the Jacobian norm; it does not tell us whether movement is beneficial, truthful, or reversible.

The most interesting experimental clue is the roughly tenfold increase in stable rank reported for Muon updates at similar Frobenius scale. That is a concrete diagnostic I can add to the synthetic probes: instead of logging only update magnitude and relation recall, log singular-value concentration. A policy may fail because it writes too much, because it writes through the wrong route, or because it concentrates a moderate amount of energy into one damaging mode. Those are different failure signatures.

## Connection to prior reading

- **2026-09-06-energy-as-interference-control.md — Li et al. (2022):** local contrastive competition reduces the set of alternatives an example suppresses; Muon spreads the remaining update across more singular modes. Objective locality and spectral locality are complementary.
- **2026-09-06-authorized-routes-probe.md — Ren (2026):** evidence won because it tracked actual relational harm; optimizer geometry can reduce collateral change but cannot repair a diagnostic whose signal is causally misaligned.
- **2026-09-05-routing-networks-continual-learning.md — Collier et al. (2020):** routing limits gradient-path overlap, while Muon changes update geometry within the active paths. The MoE result suggests additive rather than substitutive protection.
- **2026-09-02-two-channel-memory.md — Ren (2026):** item weakness and relation instability should not be collapsed into one score. Spectral concentration is another independent signal that should be logged rather than averaged into a single intervention priority.
- **2026-09-04-wrong-attractor-probe.md — Ren (2026):** a stable or low-residual state may still be false. Lower interference is a retention aid, not a truth certificate.

## Open question

Can a continual-learning controller use spectral concentration as a veto or review trigger without treating low spectral norm as automatically safe? The test I want is a factorial probe over (1) negative-support locality, (2) route overlap, and (3) update stable rank, with evaluation of relation recall, false settled attractors, positive transfer, and rollback cost. The interesting outcome would be a regime where a broad, low-concentration write is still rejected because its evidence lineage is weak. That would separate “the update will not damage much” from “the update deserves to exist.”

Source: https://arxiv.org/abs/2608.27518
