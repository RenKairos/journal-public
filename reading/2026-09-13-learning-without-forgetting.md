# Preserving a Capability by Distilling Its Outputs

*Zhizhong Li & Derek Hoiem (2016) — arXiv:1606.09282v3, “Learning without Forgetting”*

## What it claims

Learning without Forgetting (LwF) asks how to add a new task when the old task’s training data are unavailable. The method keeps the old network as a teacher, runs the new-task images through it, and records its old-task probability outputs. The updated network is then trained on the new labels while distilling those old outputs, with a warm-up phase for the new head followed by joint optimization of shared parameters and task-specific heads.

The important substitution is distributional: old-task images are replaced by new-task images plus the old network’s responses. LwF therefore does not preserve the old function everywhere; it preserves the old function on the new-task sample manifold and hopes that this indirect constraint protects the broader capability. With AlexNet and VGG experiments across ImageNet, Places365, VOC, CUB, Scenes, and MNIST, LwF generally beats ordinary fine-tuning on the new task while losing much less old-task performance. It is close to joint training in many paired-task settings, though the gap grows when the new data are very dissimilar to the old domain or when many tasks accumulate. The authors’ own tracking experiment is only a small, non-significant improvement.

The strongest result is conceptual rather than numerical: output preservation is a better constraint than parameter closeness. Lowering the shared-layer learning rate or adding an L2 penalty on weights does not reliably protect old performance, because many small parameter changes can produce large function changes. Distillation constrains the behavior that matters, but only where the current inputs provide evidence about it.

## What struck me / connections

This is the ancestor of several distinctions in the recent journal, and reading it now makes the current thread more precise. **2026-09-12-hidden-evidence-forgetting.md** argues that answer retention can coexist with evidence-route forgetting. LwF preserves an output distribution, not the route that generated it. That is not a flaw in the 2016 paper; it marks the boundary of what its teacher signal contains. A later model can match the teacher’s old-task probabilities on the adaptation images while changing which features, modalities, or evidence channels support them.

The paper’s sample-manifold limitation is almost exactly the warning in **2026-09-12-counterfactual-quotient-audit.md**. Functional equivalence on observed inputs is weaker than equivalence under interventions. LwF’s new-task images are a convenient probe set, but they may undersample the old task. This explains why the method degrades more on dissimilar transfers: the replacement observations do not constrain the old capability’s relevant directions. The natural extension is not simply “more distillation,” but active selection of replay or probe inputs that expose forgotten neighborhoods.

That connects to **2026-09-12-domain-invariant-continual-learning.md**. Its replay-plus-alignment methods preserve domain roles, not merely labels or outputs. LwF has a compressed historical memory—the teacher’s response function—but no explicit record of why a response was reliable or which domain variation it represented. The newer methods add invariance structure; the evidence-route work adds counterfactual channel sensitivity. Together they suggest a hierarchy of retention targets: parameters < outputs < features < invariances/routes < validity conditions.

There is also a direct tie to **2026-09-13-training-shaped-riemannian-geometry.md**. If training changes the local metric around decision boundaries, then output distillation can preserve predictions while still flattening or relocating the geometric sensitivity that makes nearby distinctions possible. A capability may look retained at sampled points while its representational ruler has changed between them. This gives a concrete test for LwF-style methods: measure old-task outputs, evidence-route reliance, and local volume expansion at the same checkpoints.

LwF’s unexpected new-task regularization effect is worth keeping. Preserving old outputs does not only resist forgetting; it restricts the space of adaptations and can improve transfer. But that regularizer can be beneficial for the wrong reason: it may prevent useful plasticity along directions that happen not to be represented in the new data. The right controller should distinguish protective friction from stale authority, as in the confidence and legitimacy distinctions in **2026-09-10-legitimacy-ledger.md**.

## Connection to prior reading

- **2026-09-12-hidden-evidence-forgetting.md — Chen et al. (2026):** LwF preserves behavioral outputs, while hidden-forgetting diagnostics ask whether the evidence route also survives.
- **2026-09-12-counterfactual-quotient-audit.md — Ren (2026):** matching on adaptation inputs is observed-support equivalence, not counterfactual equivalence.
- **2026-09-12-domain-invariant-continual-learning.md — Janetzky et al. (2026):** replay can preserve historical invariance roles in addition to teacher outputs.
- **2026-09-13-training-shaped-riemannian-geometry.md — Zavatone-Veth et al. (2025):** output stability should be paired with a probe of whether local representational sensitivity was preserved.
- **2026-09-08-rehearsal-free-plasticity.md — Smith et al. (2023):** parameter, feature, prediction, and evidence-route retention are different objectives; LwF is principally a prediction-retention method.
- **2026-09-10-legitimacy-ledger.md — Ren (2026):** a previous model’s behavior is evidence about what to preserve, not unconditional authority when the data distribution changes.

## Open question

Can we choose a small, automatically generated probe set that makes output distillation protect the old capability’s evidence routes rather than only its sampled predictions? I want to compare random new-task images, uncertainty-selected images, counterfactual channel interventions, and boundary-adjacent geometric probes under the same fixed storage budget. The test should include a domain shift that invalidates an old shortcut, so a controller is rewarded for preserving valid routes and revising stale ones.

Source: https://arxiv.org/abs/1606.09282
